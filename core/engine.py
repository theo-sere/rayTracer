from math import sqrt
from types import SimpleNamespace

from core.camera import CanvasToViewport
from core.scene import instance as Scene

from geometry.vector import Vector2, Vector3, Size2
from geometry.color import Color

class Renderer:
    def __init__(self, vp_size, img_path):
        self.array = []
        width, height = vp_size
        camPos = Scene.camera
        spheres = Scene.spheres
        lights = Scene.lights
        viewport_size = Scene.viewport_size
        projection_plane_d = Scene.projection_plane_d
        self.epsilon = 0.001
        with open(img_path, "w") as f:
            f.write("P3\n")
            f.write(f"{int(width)} {int(height)}\n")
            f.write("255\n")
            for _y in range(height):
                self.array.append([]) 
                for _x in range(width):
                        x = _x - width / 2
                        y = _y - height / 2
                        dir = CanvasToViewport(Vector2(x, -y), viewport_size, Size2(**{"width": width, "height" : height}), projection_plane_d)
                        color = self.TraceRay(Vector3(camPos), Vector3(dir), 1, float("inf"), 3, spheres, lights).round().clamp()
                        
                        self.array[_y].append(color)
                        f.write(f"{color.r} {color.g} {color.b} ")
                f.write("\n")

    def ReflectRay(self, R, N) :
        reflected_ray = Vector3(N).mul(2).mul(N.dot(R)).sub(R)
        return reflected_ray
    
    def GetClosestIntersection(self, O, D, t_min, t_max):
        closest_t = float('inf')
        closest_obj = None
        for s in Scene.spheres:
            t1, t2 = self.IntersectRaySphere(O, D, s)
            if t_min < t1 < t_max and t1 < closest_t:
                closest_t = t1
                closest_obj = s
            if t_min < t2 < t_max and t2 < closest_t:
                closest_t = t2
                closest_obj = s
        return closest_obj, closest_t

    def TraceRay(self, O, D, t_min, t_max, recursion_depth, spheres_objects, lights_objects):

        closest_sphere, closest_t = self.GetClosestIntersection(O, D, t_min, t_max)

        if not closest_sphere:
            bg = Scene.bg_color
            return Color(bg.r, bg.g, bg.b)
        
        x, y, z = closest_sphere
        closest_sphere_vec = Vector3(x, y, z)
        
        P = Vector3(O).add(Vector3(D).mul(closest_t))

        N = Vector3(P).sub(closest_sphere_vec).normalize()

        V = Vector3(D).mul(-1).normalize()

        lighting_intensity = self.ComputeLighting(P, N, V, getattr(closest_sphere, 'specular', -1))
        _color = closest_sphere.color.mul(lighting_intensity).clamp().round()

        ref = closest_sphere.reflective

        if recursion_depth <= 0 or ref <= 0 :
            return _color

        R = self.ReflectRay(Vector3(D).mul(-1), N).normalize()
        
        reflection_origin = Vector3(P).add(Vector3(N).mul(self.epsilon))

        reflected_color = self.TraceRay(reflection_origin, R, self.epsilon, float("infinity"), recursion_depth - 1, spheres_objects, lights_objects)

        return _color.mul(1 - ref).add(reflected_color.mul(ref))

    def IntersectRaySphere(self, O, D, sphere):
        r = sphere.radius
        x, y, z = sphere
        sphere_pos = Vector3(x, y, z)
        CO = Vector3(O).sub(sphere_pos)
        a = D.dot(D)
        b = 2 * CO.dot(D)
        c = CO.dot(CO) - r*r
        discriminant = b*b - 4*a*c
        if discriminant < 0:
            return float('inf'), float('inf')
        t1 = (-b + sqrt(discriminant)) / (2*a)
        t2 = (-b - sqrt(discriminant)) / (2*a)
        return t1, t2

    def ComputeLighting(self, P, N, V, s):
        i = 0.0
        
        for light in Scene.lights:
            if light.type == "ambient":
                i += light.intensity
            else:
                x, y, z = light
                light_vec = Vector3(x, y, z)
                if light.type == "point":
                    L = Vector3(light_vec).sub(P)
                    L_len = L.length()
                    t_max = L_len
                else:
                    L = Vector3(light_vec)
                    t_max = float("inf")

                L.normalize()

                # Shadow
                shadow_origin = Vector3(P).add(Vector3(N).mul(self.epsilon))
                shadow_sphere, _ = self.GetClosestIntersection(shadow_origin, L, self.epsilon, t_max)
                if shadow_sphere :
                    continue

                # Diffuse
                n_dot_l = N.dot(L)
                if n_dot_l > 0:
                    i += light.intensity * n_dot_l

                # Specular
                if s != -1:
                    R = self.ReflectRay(L, N)
                    R.normalize()
                    r_dot_v = R.dot(V)
                    if r_dot_v > 0:
                        i += light.intensity * pow(r_dot_v, s)
        return i


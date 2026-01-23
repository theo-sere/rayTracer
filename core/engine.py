from math import sqrt, pi, sin, cos

import random

from core.camera import CanvasToViewport
from core.scene import instance as Scene

from geometry.vector import Vector2, Vector3, Size2
from geometry.color import Color

class Renderer:
    def __init__(self, pxl_size, img_path):
        self.array = []
        width, height = pxl_size
        scene_obj = Scene.objects
        lights = Scene.lights
        camera = Scene.camera
        self.epsilon = 0.001
        with open(img_path, "w") as f:
            f.write("P3\n")
            f.write(f"{int(width)} {int(height)}\n")
            f.write("255\n")
            for _y in range(height):
                self.array.append([])
                for _x in range(width):
                    total_color = Color(0, 0, 0)

                    for _ in range(camera.samples):
                        x = _x - width / 2
                        y = _y - height / 2

                        dir_vec = CanvasToViewport(
                            Vector2(x, -y),
                            Size2(**{"width": width, "height": height}),
                            camera.projection_plane_d,
                            camera.fov
                        )
                        dir_vec = Vector3(dir_vec).normalize()

                        f_point = Vector3(camera.position).add(dir_vec.mul(camera.focal_distance))

                        angle = 2 * pi * random.random()
                        r = camera.aperture * sqrt(random.random())
                        offset = Vector3(r * cos(angle), r * sin(angle), 0)

                        new_origin = Vector3(camera.position).add(offset)

                        new_dir = f_point.sub(new_origin).normalize()

                        sample_color = self.TraceRay(
                            new_origin, new_dir, 1, float("inf"), 3, scene_obj, lights
                        )
                        total_color = total_color.add(sample_color)

                    avg_color = total_color.mul(1.0 / camera.samples).round().clamp()
                    self.array[_y].append(avg_color)
                    f.write(f"{avg_color.r} {avg_color.g} {avg_color.b} ")
                f.write("\n")

    def ReflectRay(self, R, N) :
        reflected_ray = Vector3(N).mul(2).mul(N.dot(R)).sub(R)
        return reflected_ray
    
    def GetClosestIntersection(self, O, D, t_min, t_max):
        closest_t = float('inf')
        closest_obj = None
        for o in Scene.objects:
            t1, t2 = o.Intersect(O, D)
            if t_min < t1 < t_max and t1 < closest_t:
                closest_t = t1
                closest_obj = o
            if t_min < t2 < t_max and t2 < closest_t:
                closest_t = t2
                closest_obj = o
        return closest_obj, closest_t

    def TraceRay(self, O, D, t_min, t_max, recursion_depth, scene_obj, lights_objects):

        closest_obj, closest_t = self.GetClosestIntersection(O, D, t_min, t_max)

        if not closest_obj:
            bg = Scene.bg_color
            return Color(bg.r, bg.g, bg.b)
                
        P = Vector3(O).add(Vector3(D).mul(closest_t))

        N = closest_obj.ComputeNormal(P)

        V = Vector3(D).mul(-1).normalize()

        lighting_intensity = self.ComputeLighting(P, N, V, getattr(closest_obj, 'specular', -1))
        _color = closest_obj.color.mul(lighting_intensity).clamp().round()

        ref = closest_obj.reflective

        if recursion_depth <= 0 or ref <= 0 :
            return _color

        R = self.ReflectRay(Vector3(D).mul(-1), N).normalize()
        
        reflection_origin = Vector3(P).add(Vector3(N).mul(self.epsilon))

        reflected_color = self.TraceRay(reflection_origin, R, self.epsilon, float("infinity"), recursion_depth - 1, scene_obj, lights_objects)

        return _color.mul(1 - ref).add(reflected_color.mul(ref))

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
                shadow_obj, _ = self.GetClosestIntersection(shadow_origin, L, self.epsilon, t_max)
                if shadow_obj :
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


from math import sqrt
from tools.instancieur import Vector3, Color, JsonReader, Sphere, Light

spheres = []
lights = []

epsilon = 0.001

def CanvasToViewport(x, y):
    Vw = JsonReader.get('viewport_size.width')
    Vh = JsonReader.get('viewport_size.height')
    d = JsonReader.get('projection_plane_d')
    Cw = JsonReader.get('pixel_size.width')
    Ch = JsonReader.get('pixel_size.height')
    return Vector3(x*Vw/Cw, y*Vh/Ch, d)

def ReflectRay(R, N) :
    reflected_ray = Vector3(N).mul(2).mul(N.dot(R)).sub(R)
    return reflected_ray

def GetClosestIntersection(O, D, t_min, t_max):
    closest_t = float('inf')
    closest_sphere = None
    for s in spheres:
        t1, t2 = IntersectRaySphere(O, D, s)
        if t_min < t1 < t_max and t1 < closest_t:
            closest_t = t1
            closest_sphere = s
        if t_min < t2 < t_max and t2 < closest_t:
            closest_t = t2
            closest_sphere = s
    return closest_sphere, closest_t

def TraceRay(O, D, t_min, t_max, recursion_depth, spheres_objects, lights_objects):

    if not spheres:
        for _, i in spheres_objects:
            spheres.append(Sphere(i))
    if not lights:
        for _, i in lights_objects:
            lights.append(Light(i))

    closest_sphere, closest_t = GetClosestIntersection(O, D, t_min, t_max)

    if not closest_sphere:
        bg = JsonReader.get('background_color')
        return Color(bg['r'], bg['g'], bg['b'])
    
    x, y, z = closest_sphere
    closest_sphere_vec = Vector3(x, y, z)
    
    P = Vector3(O).add(Vector3(D).mul(closest_t))

    N = Vector3(P).sub(closest_sphere_vec).normalize()

    V = Vector3(D).mul(-1).normalize()

    lighting_intensity = ComputeLighting(P, N, V, getattr(closest_sphere, 'specular', -1))

    _color = closest_sphere.color.mul(lighting_intensity).clamp().round()

    ref = closest_sphere.reflective

    if recursion_depth <= 0 or ref <= 0 :
        return _color

    R = ReflectRay(Vector3(D).mul(-1), N).normalize()
    
    reflection_origin = Vector3(P).add(Vector3(N).mul(epsilon))

    reflected_color = TraceRay(reflection_origin, R, epsilon, float("infinity"), recursion_depth - 1, spheres_objects, lights_objects)

    return _color.mul(1 - ref).add(reflected_color.mul(ref))

def IntersectRaySphere(O, D, sphere):
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

def ComputeLighting(P, N, V, s):
    i = 0.0
    for light in lights:
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
            shadow_origin = Vector3(P).add(Vector3(N).mul(epsilon))
            shadow_sphere, _ = GetClosestIntersection(shadow_origin, L, epsilon, t_max)
            if shadow_sphere :
                continue

            # Diffuse
            n_dot_l = N.dot(L)
            if n_dot_l > 0:
                i += light.intensity * n_dot_l

            # Specular
            if s != -1:
                R = ReflectRay(L, N)
                R.normalize()
                r_dot_v = R.dot(V)
                if r_dot_v > 0:
                    i += light.intensity * pow(r_dot_v, s)
    return i

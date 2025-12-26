from math import sqrt
from pyray import Vector3
from tool.instancieur import Color, JsonReader, Sphere, Light
from tool.elementaryAlgebra import elementaryAlgebra

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
    reflected_ray = Vector3(2 * N.x * elementaryAlgebra.dot(N, R) - R.x,
                            2 * N.y * elementaryAlgebra.dot(N, R) - R.y,
                            2 * N.z * elementaryAlgebra.dot(N, R) - R.z)
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
    
    P = Vector3(O.x + closest_t * D.x, O.y + closest_t * D.y, O.z + closest_t * D.z)

    N = Vector3(P.x - closest_sphere.x, P.y - closest_sphere.y, P.z - closest_sphere.z)

    N_len = elementaryAlgebra.length(N)
    N.x /= N_len
    N.y /= N_len
    N.z /= N_len

    V_len = elementaryAlgebra.length(D)
    V = Vector3(-D.x/V_len, -D.y/V_len, -D.z/V_len)

    lighting_intensity = ComputeLighting(P, N, V, getattr(closest_sphere, 'specular', -1))

    _color = closest_sphere.color.mul(lighting_intensity).clamp().round()

    ref = closest_sphere.reflective

    if recursion_depth <= 0 or ref <= 0 :
        return _color

    R = ReflectRay(Vector3(-D.x, -D.y, -D.z), N)
    R.x /= elementaryAlgebra.length(R)
    R.y /= elementaryAlgebra.length(R)
    R.z /= elementaryAlgebra.length(R)
    
    reflection_origin = Vector3(P.x + N.x * epsilon, P.y + N.y * epsilon, P.z + N.z * epsilon)

    reflected_color = TraceRay(reflection_origin, R, epsilon, float("infinity"), recursion_depth - 1, spheres_objects, lights_objects)


    return _color.mul(1 - ref).add(reflected_color.mul(ref))

def IntersectRaySphere(O, D, sphere):
    r = sphere.radius
    CO = Vector3(O.x - sphere.x, O.y - sphere.y, O.z - sphere.z)
    a = elementaryAlgebra.dot(D, D)
    b = 2 * elementaryAlgebra.dot(CO, D)
    c = elementaryAlgebra.dot(CO, CO) - r*r
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
            if light.type == "point":
                L = Vector3(light.x - P.x, light.y - P.y, light.z - P.z)
                L_len = elementaryAlgebra.length(L)
                t_max = L_len
            else:
                L = Vector3(light.x, light.y, light.z)
                t_max = float("inf")

            L_len = elementaryAlgebra.length(L)
            L.x /= L_len
            L.y /= L_len
            L.z /= L_len

            # Shadow
            shadow_origin = Vector3(P.x + N.x * epsilon, P.y + N.y * epsilon, P.z + N.z * epsilon)
            shadow_sphere, _ = GetClosestIntersection(shadow_origin, L, epsilon, t_max)
            if shadow_sphere :
                continue

            # Diffuse
            n_dot_l = elementaryAlgebra.dot(N, L)
            if n_dot_l > 0:
                i += light.intensity * n_dot_l

            # Specular
            if s != -1:
                R = ReflectRay(L, N)
                R_len = elementaryAlgebra.length(R)
                R.x /= R_len
                R.y /= R_len
                R.z /= R_len
                r_dot_v = elementaryAlgebra.dot(R, V)
                if r_dot_v > 0:
                    i += light.intensity * pow(r_dot_v, s)
    return i

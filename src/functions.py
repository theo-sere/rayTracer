from math import sqrt
from pyray import Vector3
from tool.instancieur import Color, JsonReader, Sphere, Light
from tool.elementaryAlgebra import elementaryAlgebra

spheres = []
lights = []
def CanvasToViewport(x, y):
    Vw = JsonReader.get('viewport_size.width')
    Vh = JsonReader.get('viewport_size.height')
    d = JsonReader.get('projection_plane_d')
    Cw = JsonReader.get('pixel_size.width')
    Ch = JsonReader.get('pixel_size.height')
    return Vector3(x*Vw/Cw, y*Vh/Ch, d)

def GetClosestIntersection(O, D, t_min, t_max) :
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

def TraceRay(O, D, t_min, t_max, spheres_objects, lights_objects):
    if not spheres:
        for _, i in spheres_objects:
            spheres.append(Sphere(i))
    if not lights:
        for _, i in lights_objects:
            lights.append(Light(i))
    closest_sphere, closest_t = GetClosestIntersection(O, D, t_min, t_max)
    if closest_sphere == None:
        bg = JsonReader.get('background_color')
        return Color(bg['r'], bg['g'], bg['b'])
    P = Vector3(O.x + closest_t * D.x, O.y + closest_t * D.y, O.z + closest_t * D.z)
    N = Vector3(P.x - closest_sphere.x, P.y - closest_sphere.y, P.z - closest_sphere.z)
    N.x = N.x / elementaryAlgebra.length(N)
    N.y = N.y / elementaryAlgebra.length(N)
    N.z = N.z / elementaryAlgebra.length(N)
    lighting_intensity = ComputeLighting(P, N, Vector3(-D.x, -D.y, -D.z), closest_sphere.specular)
    r = min(255, int(closest_sphere.color.r * lighting_intensity))
    g = min(255, int(closest_sphere.color.g * lighting_intensity))
    b = min(255, int(closest_sphere.color.b * lighting_intensity))
    return Color(r, g, b)

def IntersectRaySphere(O, D, sphere):
    r = sphere.radius
    CO = Vector3((O.x - sphere.x),(O.y - sphere.y),(O.z - sphere.z))

    a = elementaryAlgebra.dot(D, D)
    b = 2*elementaryAlgebra.dot(CO, D)
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
        else :
            if light.type == "point":
               L = Vector3(light.x - P.x, light.y - P.y, light.z - P.z)
               t_max = 1
            else:
               L = Vector3(light.x, light.y, light.z)
               t_max = float("inf")

            # Shadow
            shadow_sphere, _ = GetClosestIntersection(P, L, 0.001, t_max)
            if shadow_sphere :
                continue

            # Diffuse
            n_dot_l = elementaryAlgebra.dot(N, L)
            if n_dot_l > 0 :
                i += light.intensity * n_dot_l/(elementaryAlgebra.length(N) * elementaryAlgebra.length(L))

            # Specular
            if s != -1 :
                R = Vector3(2 * N.x * elementaryAlgebra.dot(N, L) - L.x, 2 * N.y * elementaryAlgebra.dot(N, L) - L.y, 2 * N.z * elementaryAlgebra.dot(N, L) - L.z)
                r_dot_v = elementaryAlgebra.dot(R, V)
                if r_dot_v > 0 :
                    i += light.intensity * pow(r_dot_v / (elementaryAlgebra.length(R) * elementaryAlgebra.length(V)), s)
    return i
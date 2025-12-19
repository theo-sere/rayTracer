from math import sqrt
from pyray import Vector3
from tool.instancieur import JsonReader, Sphere
from tool.elementaryAlgebra import elementaryAlgebra

spheres = []

def CanvasToViewport(x, y):
    Vw = JsonReader.get('viewport_size.width')
    Vh = JsonReader.get('viewport_size.height')
    d = JsonReader.get('projection_plane_d')
    Cw = JsonReader.get('pixel_size.width')
    Ch = JsonReader.get('pixel_size.height')
    return Vector3(x*Vw/Cw, y*Vh/Ch, d)

def TraceRay(O, D, t_min, t_max, spheres_objects):
    closest_t = float('inf')
    closest_sphere = None
    if not spheres:
        for _, i in spheres_objects:
            spheres.append(Sphere(i))
    for s in spheres:
        t1, t2 = IntersectRaySphere(O, D, s)
        if t_min < t1 < t_max and t1 < closest_t:
            closest_t = t1
            closest_sphere = s
        if t_min < t2 < t_max and t2 < closest_t:
            closest_t = t2
            closest_sphere = s
    if closest_sphere == None:
        bg = JsonReader.get('background_color')
        return {"r": bg['r'], "g": bg['g'], "b": bg['b']}
    return closest_sphere.color

def IntersectRaySphere(O, D, sphere):
    r = sphere.radius
    # TODO: switch from tuple/dict to object for lisibility
    CO = Vector3((O[0] - sphere.x),(O[1] - sphere.y),(O[2] - sphere.z))

    a = elementaryAlgebra.dot(D, D)
    b = 2*elementaryAlgebra.dot(CO, D)
    c = elementaryAlgebra.dot(CO, CO) - r*r

    discriminant = b*b - 4*a*c
    if discriminant < 0:
        return float('inf'), float('inf')

    t1 = (-b + sqrt(discriminant)) / (2*a)
    t2 = (-b - sqrt(discriminant)) / (2*a)
    return t1, t2
from math import sqrt
from pyray import Vector3
from tool.instancieur import JsonReader
from tool.elementaryAlgebra import elementaryAlgebra

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
    for sphere in spheres_objects:
        t1, t2 = IntersectRaySphere(O, D, sphere)
        if t_min < t1 < t_max and t1 < closest_t:
            closest_t = t1
            closest_sphere = sphere
        if t_min < t2 < t_max and t2 < closest_t:
            closest_t = t2
            closest_sphere = sphere
    if closest_sphere == None:
        bg = JsonReader.get('background_color')
        return (bg['r'], bg['g'], bg['b'])
    return closest_sphere.color

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
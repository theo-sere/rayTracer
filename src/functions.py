from math import sqrt
from pyray import Vector3
<<<<<<< Updated upstream
from tool.instancieur import JsonReader
from tool.elementaryAlgebra import elementaryAlgebra

=======
from tool.instancieur import Color, JsonReader, Sphere, Light
from tool.elementaryAlgebra import elementaryAlgebra

spheres = []
lights = []

>>>>>>> Stashed changes
def CanvasToViewport(x, y):
    Vw = JsonReader.get('viewport_size.width')
    Vh = JsonReader.get('viewport_size.height')
    d = JsonReader.get('projection_plane_d')
    Cw = JsonReader.get('pixel_size.width')
    Ch = JsonReader.get('pixel_size.height')
    return Vector3(x*Vw/Cw, y*Vh/Ch, d)

<<<<<<< Updated upstream
# TODO: Use Sphere Class

def TraceRay(O, D, t_min, t_max, spheres_objects):
    closest_t = float('inf')
    closest_sphere = None
    for sphere in spheres_objects:
        t1, t2 = IntersectRaySphere(O, D, spheres_objects[sphere])
=======
def TraceRay(O, D, t_min, t_max, spheres_objects, lights_objects):
    closest_t = float('inf')
    closest_sphere = None
    if not spheres:
        for _, i in spheres_objects:
            spheres.append(Sphere(i))
    if not lights:
        for _, i in lights_objects:
            lights.append(Light(i))
    for s in spheres:
        t1, t2 = IntersectRaySphere(O, D, s)
>>>>>>> Stashed changes
        if t_min < t1 < t_max and t1 < closest_t:
            closest_t = t1
            closest_sphere = sphere
        if t_min < t2 < t_max and t2 < closest_t:
            closest_t = t2
            closest_sphere = sphere
    if closest_sphere == None:
        bg = JsonReader.get('background_color')
<<<<<<< Updated upstream
        return {"r": bg['r'], "g":bg['g'], "b":bg['b']}
    return spheres_objects[closest_sphere]["color"]
=======
        return Color(bg['r'], bg['g'], bg['b'])
    P = Vector3(O[0] + closest_t * D.x, O[1] + closest_t * D.y, O[2] + closest_t * D.z)
    N = Vector3(P.x - closest_sphere.x, P.y - closest_sphere.y, P.z - closest_sphere.z)
    N.x = N.x / elementaryAlgebra.length(N)
    N.y = N.y / elementaryAlgebra.length(N)
    N.z = N.z / elementaryAlgebra.length(N)
    lighting_intensity = ComputeLighting(P, N)
    r = int(closest_sphere.color.r * lighting_intensity)
    g = int(closest_sphere.color.g * lighting_intensity)
    b = int(closest_sphere.color.b * lighting_intensity)
    return Color(r, g, b)
>>>>>>> Stashed changes

def IntersectRaySphere(O, D, sphere):
    r = sphere['radius']
    # TODO: switch from tuple/dict to object for lisibility
    CO = Vector3((O[0] - sphere["center"]["x"]),(O[1] - sphere["center"]["y"]),(O[2] - sphere["center"]["z"]))

    a = elementaryAlgebra.dot(D, D)
    b = 2*elementaryAlgebra.dot(CO, D)
    c = elementaryAlgebra.dot(CO, CO) - r*r

    discriminant = b*b - 4*a*c
    if discriminant < 0:
        return float('inf'), float('inf')

    t1 = (-b + sqrt(discriminant)) / (2*a)
    t2 = (-b - sqrt(discriminant)) / (2*a)
    return t1, t2

def ComputeLighting(P, N):
    i = 0.0
    for light in lights:
        if light.type == "ambient":
           i += light.intensity
        else :
            if light.type == "point":
               L = Vector3(light.x - P.x, light.y - P.y, light.z - P.z)
            else:
               L = Vector3(light.x, light.y, light.z)

            n_dot_l = elementaryAlgebra.dot(N, L)
            if n_dot_l > 0 :
                i += light.intensity * n_dot_l/(elementaryAlgebra.length(N) * elementaryAlgebra.length(L))
    return i
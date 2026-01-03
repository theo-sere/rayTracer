from geometry.vector import Vector3
from geometry.color import Color

class Sphere:
    def __init__(self, center, radius, color, reflective, specular):
        self.center = Vector3(**center)
        self.x = self.center.x
        self.y = self.center.y
        self.z = self.center.z
        self.radius = radius
        self.color = Color(**color)
        self.reflective = reflective
        self.specular = specular

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z
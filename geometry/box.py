from geometry.vector import Vector3
from geometry.color import Color

class Box:
    def __init__(self, center, width, height, depth, color, reflective, specular):
        self.type = "box"
        self.center = Vector3(**center)
        self.x = self.center.x
        self.y = self.center.y
        self.z = self.center.z
        self.width = width
        self.height = height
        self.depth = depth
        self.color = Color(**color)
        self.reflective = reflective
        self.specular = specular

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z
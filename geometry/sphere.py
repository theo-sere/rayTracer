from geometry.vector import Vector3
from geometry.color import Color
from math import sqrt

class Sphere:
    def __init__(self, center, radius, color, reflective, specular):
        self.type = "sphere"
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

    def Intersect(self, O, D):
        r = self.radius
        x, y, z = self
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

    def ComputeNormal(self, P):
        return Vector3(P).sub(self.center).normalize()
from geometry.vector import Vector3
from geometry.color import Color
from math import sqrt

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

    def Intersect(self, O, D):
        x, y, z = self
        w, h, d = self.width / 2, self.height / 2, self.depth / 2
        xmin, ymin, zmin = x - w, y - h, z - d
        xmax, ymax, zmax = x + w, y + h, z + d
        inverseD = Vector3(1 / D.x if D.x != 0 else float('inf'),
                       1 / D.y if D.y != 0 else float('inf'),
                       1 / D.z if D.z != 0 else float('inf'))
        tx1 = (xmin - O.x) * inverseD.x
        tx2 = (xmax - O.x) * inverseD.x
        ty1 = (ymin - O.y) * inverseD.y
        ty2 = (ymax - O.y) * inverseD.y
        tz1 = (zmin - O.z) * inverseD.z
        tz2 = (zmax - O.z) * inverseD.z
        tmin = max(min(tx1, tx2), min(ty1, ty2), min(tz1, tz2))
        tmax = min(max(tx1, tx2), max(ty1, ty2), max(tz1, tz2))
        if tmax < 0 or tmin > tmax:
            return float('inf'), float('inf')
        return tmin, tmax

    def ComputeNormal(self, P):
        epsilon = 0.0001
        x, y, z = self.center.x, self.center.y, self.center.z
        w, h, d = self.width / 2, self.height / 2, self.depth / 2
        if P.x > x + w - epsilon: return Vector3(1, 0, 0)
        if P.x < x - w + epsilon: return Vector3(-1, 0, 0)
        if P.y > y + h - epsilon: return Vector3(0, 1, 0)
        if P.y < y - h + epsilon: return Vector3(0, -1, 0)
        if P.z > z + d - epsilon: return Vector3(0, 0, 1)
        if P.z < z - d + epsilon: return Vector3(0, 0, -1)
        return Vector3(0, 1,0)
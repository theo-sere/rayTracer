import math

class Size2:
    def __init__(self, width = 0.0, height = 0.0):
            self.width = float(width)
            self.height = float(height)

class Vector2:
    """
    Wrap Vector inside "Vector2" to copy it and avoid modifying it in-place.
    """
    def __init__(self, x = 0.0, y = 0.0):
        if isinstance(x, Vector2):
            self.x = x.x
            self.y = x.y
        else:
            self.x = float(x)
            self.y = float(y)

class Vector3:
    """
    Wrap Vector inside "Vector3" to copy it and avoid modifying it in-place.
    """
    def __init__(self, x = 0.0, y = 0.0, z = 0.0):
        if isinstance(x, Vector3):
            self.x = x.x
            self.y = x.y
            self.z = x.z
        else:
            self.x = float(x)
            self.y = float(y)
            self.z = float(z) 

    def dot(self, b):
        return ((self.x * b.x) + (self.y * b.y) + (self.z * b.z))
    
    def length(self):
        return math.sqrt(self.dot(self))
    
    def add(self, n):
        if isinstance(n, Vector3):
            self.x += n.x
            self.y += n.y
            self.z += n.z
        else:
            self.x += n
            self.y += n
            self.z += n
        return self
    
    def sub(self, n):
        if isinstance(n, Vector3):
            self.add(Vector3(n).mul(-1))
        else:
            self.add(-n)
        return self

    def mul(self, n):
        self.x *= n
        self.y *= n
        self.z *= n
        return self
    
    def div(self, n):
        return self.mul(1/n)
    
    def normalize(self):
        return self.div(self.length())

from geometry.vector import Vector3 

class Light:
    def __init__(self, type, intensity, position = {"x": 0, "y": 0, "z":0}):
        self.type = type
        self.intensity = intensity
        source = Vector3(**position)
        self.x = source.x
        self.y = source.y
        self.z = source.z

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z

from geometry.vector import Vector3 

def CanvasToViewport(coords, V, C, d):
    return Vector3(coords.x * V.width / C.width, coords.y * V.height / C.height, d)
 
class Camera:
    def __init__(self, pos):
        self.x = pos.x
        self.y = pos.y
        self.z = pos.z

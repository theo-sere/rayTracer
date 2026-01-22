from geometry.vector import Vector3 
from math import tan, pi

def CanvasToViewport(coords, C, projection_plane_d, fov):
    vp_width = tan((fov.x / 2) * pi / 180) * projection_plane_d * 2
    vp_height = tan((fov.y / 2) * pi / 180) * projection_plane_d * 2
    return Vector3(coords.x * vp_width / C.width, coords.y * vp_height / C.height, projection_plane_d)
 
class Camera:
    def __init__(self, position=None, final_position = None, fov=None, projection_plane_d = 1):
        if position is None:
            position = {"x": 0, "y": 0, "z": 0}
        if fov is None:
            fov = {"x": 80, "y": 50}

        self.position = Vector3(**position)

        if not final_position or not type(final_position) is Vector3 :
            self.final_position = self.position
        else:
            self.final_position = final_position
        self.projection_plane_d = projection_plane_d

        self.fov = Vector3(**fov)
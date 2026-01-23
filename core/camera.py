from geometry.vector import Vector3 
from math import tan, pi

def CanvasToViewport(coords, C, projection_plane_d, fov):
    vp_width = tan((fov.x / 2) * pi / 180) * projection_plane_d * 2
    vp_height = tan((fov.y / 2) * pi / 180) * projection_plane_d * 2
    return Vector3(coords.x * vp_width / C.width, coords.y * vp_height / C.height, projection_plane_d)
 
class Camera:
    def __init__(self, position = None, final_position = None, fov = None, projection_plane_d = 1, aperture = 0.0, focal_distance = 3, samples = 16):
        self.aperture = aperture
        self.focal_distance = focal_distance
        self.samples = samples
        if position is None:
            self.position = {"x": 0, "y": 0, "z": 0}
        else :
            self.position = Vector3(**position)
        if fov is None:
            fov = {"x": 80, "y": 50}
        if final_position is None:
            self.final_position = self.position
        else:
            self.final_position = Vector3(**final_position)

        self.projection_plane_d = projection_plane_d

        self.fov = Vector3(**fov)
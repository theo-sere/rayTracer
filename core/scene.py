from geometry.sphere import Sphere
from geometry.light import Light
from geometry.vector import Vector3, Size2
from geometry.color import Color

class Scene:
    def __init__(self):
        self.spheres = []
        self.lights = []
        self.camera = None
        self.bg_color = None
        self.viewport_size = None
        self.pixel_size = None
        self.projection_plane_d = None
    def set(self, scene_data):
        self.spheres.extend([Sphere(**s) for s in scene_data["spheres"]])
        self.lights.extend([Light(**l) for l in scene_data["lights"]])
        self.camera = Vector3(**scene_data["camera_position"])
        self.bg_color = Color(**scene_data["bg_color"])
        self.viewport_size = Size2(**scene_data["viewport_size"])
        self.pixel_size = Size2(**scene_data["pixel_size"])
        self.projection_plane_d = scene_data["projection_plane_d"]

instance = Scene()
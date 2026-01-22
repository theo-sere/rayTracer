from geometry.sphere import Sphere
from geometry.box import Box
from geometry.light import Light
from geometry.vector import Vector3, Size2
from geometry.color import Color

from core.camera import Camera

class Scene:
    def __init__(self):
        self.spheres = []
        self.boxes = []
        self.pixel_size = []
        self.lights = []
        self.camera = None
        self.bg_color = None
        self.viewport_size = None
        self.pixel_size = None
        self.projection_plane_d = None
        self.final_cam = None
        self.objects = []
    def set(self, scene_data):
        self.pixel_size = Size2(**scene_data["pixel_size"], isfloat = False)

        self.boxes.extend([Box(**b) for b in scene_data["boxes"]])
        self.spheres.extend([Sphere(**s) for s in scene_data["spheres"]])
        self.lights.extend([Light(**l) for l in scene_data["lights"]])

        self.camera = Camera(**scene_data["camera"])

        self.bg_color = Color(**scene_data["bg_color"])
        self.objects.extend(self.spheres + self.boxes)
instance = Scene()
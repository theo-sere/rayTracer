import json
import os

class Color:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

class JsonReader:
    _data = None

    @staticmethod
    def get(key_path):
        if JsonReader._data is None:
            current_dir = os.path.dirname(__file__)
            root_dir = os.path.abspath(os.path.join(current_dir, "../../"))
            json_path = os.path.join(root_dir, "scene.json")
            with open(json_path, "r") as f:
                JsonReader._data = json.load(f)
        data = JsonReader._data
        keys = key_path.split('.')
        for key in keys:
            data = data[key]
        return data

class Sphere:
    def __init__(self, number):
        sphere = JsonReader.get('spheres.s'+str(number))
        self.x = sphere["center"]["x"]
        self.y = sphere["center"]["y"]
        self.z = sphere["center"]["z"]
        self.radius = sphere["radius"]
        self.color = Color(sphere["color"]["r"], sphere["color"]["g"], sphere["color"]["b"])
        self.specular = sphere["specular"]

class Light:
    def __init__(self, number):
        light = JsonReader.get('lights.l'+str(number))
        self.type = light["type"]
        if self.type == "directional":
            self.x = light["direction"]["x"]
            self.y = light["direction"]["y"]
            self.z = light["direction"]["z"]
        if self.type == "point":
            self.x = light["position"]["x"]
            self.y = light["position"]["y"]
            self.z = light["position"]["z"]
        self.intensity = light["intensity"]

import json
import os

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
        self.color = {"r": sphere["color"]["r"], "g": sphere["color"]["g"], "b": sphere["color"]["b"]}
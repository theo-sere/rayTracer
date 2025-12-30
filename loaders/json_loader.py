import json
import os

class SceneLoader:
    def __init__(self):
        self.data = None
    def __init__(self, key_path):
        current_dir = os.path.dirname(__file__)
        root_dir = os.path.abspath(os.path.join(current_dir, "../"))
        json_path = os.path.join(root_dir, key_path)
        with open(json_path, "r") as f:
            self.data = json.load(f)
    def get(self, key_path):
        keys = key_path.split('.')
        for key in keys:
            data = data[key]
        return data
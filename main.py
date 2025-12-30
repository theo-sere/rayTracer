from loaders.json_loader import SceneLoader
from core.engine import Renderer
from core.scene import instance as Scene

scene_data = SceneLoader("scene.json").data
scene = Scene.set(scene_data)

renderer = Renderer([500, 500])

# renderer.save_ppm("output/image.ppm")
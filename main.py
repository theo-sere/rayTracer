from loaders.json_loader import SceneLoader
from core.engine import Renderer
from core.scene import instance as Scene
import imageio
import os

scene_data = SceneLoader("scene.json").data
Scene.set(scene_data)

print("Image (1) - GIF (2) - Video (3)")
answer = input()

def multiCapture():
    print("How many frames ?")
    nCaptures = int(input())
    print("How long (in seconds) ?")
    duree = int(input())
    frames = []
    tx = (Scene.camera.final_position.x - Scene.camera.position.x) / (nCaptures-1)
    ty = (Scene.camera.final_position.y - Scene.camera.position.y) / (nCaptures-1)
    tz = (Scene.camera.final_position.z - Scene.camera.position.z) / (nCaptures-1)
    for i in range(nCaptures):
        print("Generation of the image number", i+1)
        Renderer([Scene.pixel_size.width, Scene.pixel_size.height], f"image{i}.ppm")
        frames.append(imageio.v3.imread(f"image{i}.ppm"))
        Scene.camera.position.x += tx
        Scene.camera.position.y += ty
        Scene.camera.position.z += tz
    return nCaptures, duree, frames

if answer == "1":
    Renderer([Scene.pixel_size.width, Scene.pixel_size.height], "image.ppm")
elif answer == "2":
    nCaptures, duree, frames = multiCapture()
    imageio.mimsave('animation.gif', frames, fps=nCaptures / duree)
    for i in range(nCaptures):
        os.remove(f"image{i}.ppm")
elif answer == "3":
    nCaptures, duree, frames = multiCapture()
    imageio.mimsave('animation.mp4', frames, fps=nCaptures/duree)
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
    tx = (Scene.final_cam.x - Scene.camera.x) / (nCaptures - 1)
    ty = (Scene.final_cam.y - Scene.camera.y) / (nCaptures - 1)
    tz = (Scene.final_cam.z - Scene.camera.z) / (nCaptures - 1)
    for i in range(nCaptures):
        print("Generation of the image number", i+1)
        renderer = Renderer([Scene.pixel_size.width, Scene.pixel_size.height], f"image{i}.ppm")
        frames.append(imageio.v3.imread(f"image{i}.ppm"))
        Scene.camera.x += tx
        Scene.camera.y += ty
        Scene.camera.z += tz
    return nCaptures, duree, frames

if answer == "1":
    renderer = Renderer([500, 500], "image.ppm")
elif answer == "2":
    nCaptures, duree, frames = multiCapture()
    imageio.mimsave('animation.gif', frames, fps=nCaptures / duree)
    for i in range(nCaptures):
        os.remove(f"image{i}.ppm")
elif answer == "3":
    nCaptures, duree, frames = multiCapture()
    imageio.mimsave('animation.mp4', frames, fps=nCaptures/duree)
    for i in range(nCaptures):
        os.remove(f"image{i}.ppm")
from tool.instancieur import JsonReader
import functions as funcs
from pyray import Vector3
import imageio
import os

width = JsonReader.get('pixel_size.width')
height = JsonReader.get('pixel_size.height')
spheres = JsonReader.get('spheres')
lights = JsonReader.get('lights')
camPos = JsonReader.get('camera_position')
camFinalPos = JsonReader.get('camera_final_position')

def capture(camPos, file):
    with open(file, "w") as f:
        f.write("P3\n")
        f.write(f"{int(width)} {int(height)}\n")
        f.write("255\n")
        for _y in range(height):
            for _x in range(width):
                x = _x - width/2
                y = _y - height/2
                dir = funcs.CanvasToViewport(x, -y)

                color = funcs.TraceRay(Vector3(camPos["x"], camPos["y"], camPos["z"]), dir, 1, float("inf"), 3, spheres, lights).round().clamp()

                f.write(f"{color.r} {color.g} {color.b} ")
            f.write("\n")

print("GIF generation ? (y/n)")
answer = input()
if answer == "n":
    capture(camPos, "image.ppm")
else:
    print("How many frames ?")
    nCaptures = int(input())
    print("How long ?")
    duree = int(input())
    frames = []
    tx = (camFinalPos["x"] - camPos["x"]) / (nCaptures-1)
    ty = (camFinalPos["y"] - camPos["y"]) / (nCaptures-1)
    tz = (camFinalPos["z"] - camPos["z"]) / (nCaptures-1)
    for i in range(nCaptures):
        print("Generation of the image number", i+1)
        capture(camPos, f"image{i}.ppm")
        frames.append(imageio.v3.imread(f"image{i}.ppm"))
        camPos["x"] += tx
        camPos["y"] += ty
        camPos["z"] += tz
    imageio.mimsave('image.gif', frames, fps=nCaptures/duree)
    for i in range(nCaptures):
        os.remove(f"image{i}.ppm")
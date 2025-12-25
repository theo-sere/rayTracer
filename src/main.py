from tool.instancieur import JsonReader
import functions as funcs
from pyray import Vector3

width = JsonReader.get('pixel_size.width')
height = JsonReader.get('pixel_size.height')
spheres = JsonReader.get('spheres')
lights = JsonReader.get('lights')
camPos = JsonReader.get('camera_position')

with open("../image.ppm", "w") as f:
    f.write("P3\n")
    f.write(f"{int(width)} {int(height)}\n")
    f.write("255\n")

    for _y in range(height):
        for _x in range(width):
            x = _x - width/2
            y = _y - height/2
            dir = funcs.CanvasToViewport(x, -y)
            color = funcs.TraceRay(Vector3(camPos["x"], camPos["y"], camPos["z"]), dir, 1, float("inf"), spheres, lights)
            f.write(f"{color.r} {color.g} {color.b} ")
        f.write("\n")


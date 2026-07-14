from pymol import cmd
from pymol.cgo import *

def docking_box(
    name="dockbox",
    center_x=0, center_y=0, center_z=0,
    size_x=20, size_y=20, size_z=20,
    r=1, g=1, b=0,
    linewidth=2
):
    cx, cy, cz = float(center_x), float(center_y), float(center_z)
    sx, sy, sz = float(size_x), float(size_y), float(size_z)

    x0, x1 = cx - sx/2, cx + sx/2
    y0, y1 = cy - sy/2, cy + sy/2
    z0, z1 = cz - sz/2, cz + sz/2

    corners = [
        (x0, y0, z0), (x1, y0, z0),
        (x0, y1, z0), (x1, y1, z0),
        (x0, y0, z1), (x1, y0, z1),
        (x0, y1, z1), (x1, y1, z1),
    ]

    edges = [
        (0,1), (0,2), (1,3), (2,3),
        (4,5), (4,6), (5,7), (6,7),
        (0,4), (1,5), (2,6), (3,7),
    ]

    obj = [
        LINEWIDTH, float(linewidth),
        COLOR, float(r), float(g), float(b),
        BEGIN, LINES,
    ]

    for i, j in edges:
        obj.extend([VERTEX, *corners[i], VERTEX, *corners[j]])

    obj.append(END)
    cmd.load_cgo(obj, name)

cmd.extend("docking_box", docking_box)
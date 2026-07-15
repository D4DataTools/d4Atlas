import math

def rotate(point, angle):
    angle = math.radians(angle)

    return {
        "x": point["x"] * math.cos(angle) - point["y"] * math.sin(angle),
        "y": point["y"] * math.cos(angle) + point["x"] * math.sin(angle),
    }


def translate(point, offset):
    return {
        "x": point["x"] + offset["x"],
        "y": point["y"] + offset["y"],
        "z": point.get("z", 0) + offset.get("z", 0),
    }


def scale(point, sx=None, sy=None):
    if sx is None:
        return point

    if sy is None:
        sy = sx

    return {
        "x": point["x"] * sx,
        "y": point["y"] * sy,
    }
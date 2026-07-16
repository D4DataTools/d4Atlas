import math

#' @title Rotate a Point about an angle 
#' 
#' @description Take a point and rotate it by an angle. 
#' @param point A `dict` with keys "x" and "y"
#' @param angle A `float` of degress 
#' @return a `dict` with keys "x" and "y"
#' 
def rotate(point: dict, angle: float):
    angle = math.radians(angle)

    return {
        "x": point["x"] * math.cos(angle) - point["y"] * math.sin(angle),
        "y": point["y"] * math.cos(angle) + point["x"] * math.sin(angle),
    }

#' Translate a point with an offset
#' 
#' @description Take a point in xy space and translate it with a vector offset. 
#' @param point A `dict` with keys "x" and "y"
#' @param offset A `dict` with keys "x" and "y"
#' @return a `dict` with keys "x" and "y"
#' 
def translate(point: dict, offset: dict):
    return {
        "x": point["x"] + offset["x"],
        "y": point["y"] + offset["y"],
        "z": point.get("z", 0) + offset.get("z", 0),
    }

#' Scale a point with an offset
#' 
#' @description Take a point in xy space and scale it along x and y scalers.  
#' @param point A `dict` with keys "x" and "y"
#' @param sx A `float` with default value of None
#' @param sy A `float` with default value of None
#' @return a `dict` with keys "x" and "y"
#' @details if `sx` is not provided this function returns the original `dict`
#' if `sy` is not provided, this function scales y with the same scaler as x.  
#' 
def scale(point: dict, sx: float=None, sy: float=None):
    if sx is None: return point

    if sy is None: sy = sx

    return {
        "x": point["x"] * sx,
        "y": point["y"] * sy,
    }
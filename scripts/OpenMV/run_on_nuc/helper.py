import numpy as np

# Set the target temp range here
min_temp_in_celsius = -10.0
max_temp_in_celsius = 60.0


def map_g_to_temp(g):
    return ((g * (max_temp_in_celsius - min_temp_in_celsius)) / 255.0) + min_temp_in_celsius


def get_shape_name(CornerNum, w, h):
    if CornerNum == 3:
        objType = "triangle"
    elif CornerNum == 4:
        if w == h:
            objType = "Square"
        else:
            objType = "Rectangle"
    elif CornerNum > 4:
        objType = str(CornerNum)+" polygon"
    else:
        objType = "N"
    return objType


def get_full_paths(path):
    srcPath = path+'/raw/'
    midPath = path+'/middleFile/'
    dstPath = path+'/result/'
    return srcPath, midPath, dstPath

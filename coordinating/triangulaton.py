import sys
import cv2
import numpy as np
import time


def find_location(right_point, left_point, frame_right, frame_left, baseline,f, alpha):

    height_right, width_right, depth_right = frame_right.shape
    height_left, width_left, depth_left = frame_left.shape

    # CONVERT FOCAL LENGTH f FROM [mm] TO [pixel]
    if width_right == width_left:
        f_pixel = (width_right * 0.5) / np.tan(alpha * 0.5 * np.pi/180)

    else:
        print('Left and right camera frames do not have the same pixel width')

    x_right = right_point[0] - width_right//2
    x_left = left_point[0] - width_right//2
    
    y_right = right_point[1] - height_right//2
    y_left = left_point[1] - height_left//2

    # CALCULATE THE DISPARITY:
    disparity = x_left-x_right      #Displacement between left and right frames [pixels]
    
    # CALCULATE LOCATION:
    Z = (baseline*f_pixel)/disparity   #Z in [cm]
    X = (Z*x_left)/f_pixel             #X in [cm]
    Y = (Z*y_left)/f_pixel             #Y in [cm]


    return X, Y, Z
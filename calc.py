import cv2
import math

def contour_center(c):
    """Returns the center point (pixels) of the given contour"""
    (x,y),r = cv2.minEnclosingCircle(c)
    return (int(x),int(y))


def dist_between_contours(c1,c2):
    """Returns the distance between the two contour centers and the
x and y offset of the contours. (distance,dx,dy)"""
    center1 = contour_center(c1)
    center2 = contour_center(c2)
    dx = center1[0] - center2[0]
    dy = center2[1] - center2[1]
    d = math.sqrt(dx**2 + dy**2)
    return (d,dx,dy)



import cv2
import math
import numpy as np

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
    dy = center1[1] - center2[1]
    d = math.sqrt(dx**2 + dy**2)
    return (d,dx,dy)

def avg_dist(cnt_pairs):
    """Takes a list of contour pairs and returns the average distance between
each of them as well as the average dx and dy.
ret: (avg dist, avg dx, avg dy)"""
    mean_d = np.empty(len(cnt_pairs))
    mean_dx = np.empty(len(cnt_pairs))
    mean_dy = np.empty(len(cnt_pairs))
    for i,pair in enumerate(cnt_pairs):
        dist,dx,dy = dist_between_contours(pair[0],pair[1])
        mean_d[i] = dist
        mean_dx[i] = dx
        mean_dy[i] = dy

    return (mean_d.mean(), mean_dx.mean(), mean_dy.mean())


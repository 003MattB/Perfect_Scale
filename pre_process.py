import cv2
import numpy as np

def denoise(img, strength = 5):
    
    kernel = np.ones((3,3),np.uint8)
    cv2.morphologyEx(img,cv2.MORPH_OPEN, kernel)
    return cv2.fastNlMeansDenoising(img, h=strength)


def recolor(img,orig_color,new_color,threshold=10):
    """Takes a grayscale image and changes orig_color to new_color if it is
within a certain threshold. Returns a newly recolored image"""
    ret = img.copy()
    for x in np.nditer(ret, op_flags=['readwrite']):
        if abs(x - orig_color) <= threshold:
            x[...] = new_color
    return ret

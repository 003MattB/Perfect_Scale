import cv2
import numpy as np

def denoise(img, strength = 5):
    
    kernel = np.ones((3,3),np.uint8)
    cv2.morphologyEx(img,cv2.MORPH_OPEN, kernel)
    return cv2.fastNlMeansDenoising(img, h=strength)


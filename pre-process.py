import cv2
import numpy as np

def denoise(img,iterations = 10):
    for i in range(iterations):
        img = cv2.fastNlMeansDenoising(img_gs)
    return img


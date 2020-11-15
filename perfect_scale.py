import cv2

# load the image
img = cv2.imread('img/test2.jpg')

#convert it to gray-scale
img_gs = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

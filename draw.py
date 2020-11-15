import cv2

def draw_box_around_contour(img,cnt, color=(0,255,0), ox = 0, oy = 0):
    """Draws bounding box around contours on the given image.
parameters:
    img: an image to draw on
    cnt: a single contour
    color: the color of the bounding box
    ox: offset x to add to the contour center
    oy: offset y to add to the contour center
return:
    None
"""
    x,y,w,h = cv2.boundingRect(cnt)
    x += ox
    y += oy
    cv2.rectangle(img,(x,y),(x+w,y+h),color,2)

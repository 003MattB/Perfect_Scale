import cv2

def draw_box_around_contour(img,cnt, color=(0,255,0)):
    x,y,w,h = cv2.boundingRect(cnt)
    cv2.rectangle(img,(x,y),(x+w,y+h),color,2)

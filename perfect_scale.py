# code copied from:
# https://www.pyimagesearch.com/2016/04/04/measuring-distance-between-objects-in-an-image-with-opencv/


from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import numpy as np
import argparse
import imutils
import cv2

def midpoint(ptA, ptB):
    return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)

# this is for getting command line arguments
# width is the size of the hole (in inches)

##ap = argparse.ArgumentParser()
##ap.add_argument('-i', '--image', required=True,
##                help="path to the input image")
##ap.add_argument('-w', '--width', type=float, required=True,
##                help='width of the left-most object in the image (in inches)')
##args = vars(ap.parse_args())

# load the image, convert to gray scale, and blurr it a little
#image = cv2.imread(args['image']) # from command line
image = cv2.imread('img/reg2.JPG') # hard coded
# crop the image -- the upper left quadrent
#image = image[0: int(len(image) * 0.5), 0:int(len(image[0]) * 0.5)]
image = image[int(len(image) * 0.5): len(image)-1, int(len(image) * 0.5):len(image[0])-1]
#image = ~image # invert the image
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (7, 7), 0)

# perform edge detection, then perform a dilation + erosion to close gaps
# in between object edges
edged = cv2.Canny(gray, 50, 100)
edged = cv2.dilate(edged, None, iterations=1)
edged = cv2.erode(edged, None, iterations=1)
edged_inv = ~edged

# find the contours in the edge map
cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
                        cv2.CHAIN_APPROX_SIMPLE)
cnts_inv = cv2.findContours(edged_inv.copy(), cv2.RETR_EXTERNAL,
                        cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
cnts_inv = imutils.grab_contours(cnts_inv)

# sort the contours from left to right then initialize the distance colors
# and the reference object
(cnts, _) = contours.sort_contours(cnts)
(cnts_inv, _) = contours.sort_contours(cnts_inv)
colors = ((0,0,255), (240, 0, 159), (0,165, 255), (255,255,0),
          (255,0,255))
refObjs = []
refObjs_inv = []
print("contours")
print(len(cnts))
print(len(cnts_inv))

# loop through the contours
for c in cnts:
    # ignore contours that are too small
    # also ignore contours that are too big - like copper thieving
    if cv2.contourArea(c) < 6 or cv2.contourArea(c) > 40:
        continue
    # compute the rotated bounding box of the contour
    box = cv2.minAreaRect(c)
    box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
    box = np.array(box,dtype='int')


    # order the points in the contour such that they appear
    # in top-left, top-right, bottom-right, and bottom-left
    # order, then draw the outline of the rotated bounding
    # box
    box = perspective.order_points(box)

    # compute the center of the bounding box
    cX = np.average(box[:,0])
    cY = np.average(box[:,1])


    # if this is the first contour we are examining (i.e.,
    # the left-most contour), we presume this is the
    # reference object
##    if refObj is None:
    # unpack the ordered bounding box, then compute the
    # midpoint between the top-left and top-right points,
    # followed by the midpoint between the top-right and
    # bottom-right
    (tl, tr, br, bl) = box
    (tlblX, tlblY) = midpoint(tl,bl)
    (trbrX, trbrY) = midpoint(tr,br)


    # compute the Euclidean distance between the midpoints,
    # then construct the reference objec
    D = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))
    scale = D / 0.0158
    #refObj = (box, (cX, cY), D / args['width'])
    refObjs.append( (box, (cX, cY), scale) )

for c in cnts:
    # ignore contours that are too small
    # also ignore contours that are too big - like copper thieving
    if cv2.contourArea(c) < 6 or cv2.contourArea(c) > 40:
        continue
    # compute the rotated bounding box of the contour
    box = cv2.minAreaRect(c)
    box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
    box = np.array(box,dtype='int')


    # order the points in the contour such that they appear
    # in top-left, top-right, bottom-right, and bottom-left
    # order, then draw the outline of the rotated bounding
    # box
    box = perspective.order_points(box)

    # compute the center of the bounding box
    cX = np.average(box[:,0])
    cY = np.average(box[:,1])


    # if this is the first contour we are examining (i.e.,
    # the left-most contour), we presume this is the
    # reference object
##    if refObj is None:
    # unpack the ordered bounding box, then compute the
    # midpoint between the top-left and top-right points,
    # followed by the midpoint between the top-right and
    # bottom-right
    (tl, tr, br, bl) = box
    (tlblX, tlblY) = midpoint(tl,bl)
    (trbrX, trbrY) = midpoint(tr,br)


    # compute the Euclidean distance between the midpoints,
    # then construct the reference objec
    D = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))
    scale = D / 0.0158
    #refObj = (box, (cX, cY), D / args['width'])
    refObjs_inv.append( (box, (cX, cY), scale) )    

##        continue
    # draw the contours on the image
print("refObjs")
print(refObjs)
print(refObjs_inv)
for r1,r2 in zip(refObjs,refObjs_inv):
    orig = image.copy()
    cv2.drawContours(orig,[r1[0].astype('int')], -1, (0,255,0),2)
    cv2.drawContours(orig,[r2[0].astype('int')], -1, (0,255,0), 2)

    # stack the reference coordinates and the object coordinates
    # to include the object center
    refCoords = np.vstack([r1[0], r1[1]])
    objCoords = np.vstack([r2[0], r2[1]])
    i = 0

    # loop over the original points
    for ((xA, yA), (xB,yB),color) in zip(refCoords, objCoords, colors):
        if i == 4: # only show the mid point
            # draw circles corresponding to the current points and
            # connect them with a line
            cv2.circle(orig, (int(xA), int(yA)), 5, color, -1)
            cv2.circle(orig, (int(xB), int(yB)), 5, color, -1)
            cv2.line(orig, (int(xA), int(yA)), (int(xB), int(yB)), color, 2)

            # compute the Euclidean distance between the coordinates,
            # and then convert the distance in pixels to distance in
            # units
            D = dist.euclidean((xA, yA), (xB, yB)) / r1[2]
            (mX, mY) = midpoint((xA, yA), (xB, yB))
            cv2.putText(orig, "{:.4f}in".format(D), (int(mX), int(mY - 10)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.55, color, 2)

            # show the output image
            cv2.imshow("Image",orig)
            cv2.waitKey(0)

        i += 1
        
        

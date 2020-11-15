import cv2
import numpy as np

import crop
import calc
import pre_process
import draw

# I calculated this ahead of time. I expect all the images to be 640 x 480
# and the features will always be the same scale
# I calculated it by dividing the width (in pixels) of a contour by it's known
# width (in inches)
# x,y,w,h = cv2.boundingRect(contour)
# PIX_PER_INCH = w / width_in_inches
PIX_PER_INCH = 579.7101449275362
PIX_PER_MIL = PIX_PER_INCH / 1000 # pixels per thousandth of an inch


# load the image
img = cv2.imread('img/test2.jpg')

#convert it to gray-scale
img_gs = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

# seperate the image into 4 quadrents
ul = crop.upperLeft(img_gs)
ur = crop.upperRight(img_gs)
ll = crop.lowerLeft(img_gs)
lr = crop.lowerRight(img_gs)

# do some pre-processing
# ...
thresholds = []
for part in (ul,ur,ll,lr):
    _,t = cv2.threshold(part,200,255,0)
    thresholds.append(t)

# get the contours and the hierarchy tree
contours = []
for threshold in thresholds:
    cnts,h = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours.append((cnts,h))
    
# get the pads and drills as parent child pairs
# assumes drills are actually hitting pads
quadrent_pairs = []
for cnt,h in contours:
    pair = pre_process.parent_child_pairs(cnt,h)
    quadrent_pairs.append(pair)

# get the average offset of drills from pad centers for each quadrent
offsets = []
for pairs in quadrent_pairs:
    offset = calc.avg_dist(pairs)
    offsets.append(offset)

ul_avg = (np.array(offsets[0]) / PIX_PER_INCH)
ur_avg = (np.array(offsets[1]) / PIX_PER_INCH)
ll_avg = (np.array(offsets[2]) / PIX_PER_INCH)
lr_avg = (np.array(offsets[3]) / PIX_PER_INCH)
print("average offsets for each quadrent (in inches)".upper())
print("QUADRENT [OFFSET DISTANCE, DX, DY]")
##print("ul [{:.4f}, {:.4f}, {:.4f}]".format(ul_avg[0],ul_avg[1],ul_avg[2]))
##print("ur [{:.4f}, {:.4f}, {:.4f}]".format(ur_avg[0],ur_avg[1],ur_avg[2]))
##print("ll [{:.4f}, {:.4f}, {:.4f}]".format(ll_avg[0],ll_avg[1],ll_avg[2]))
##print("lr [{:.4f}, {:.4f}, {:.4f}]".format(lr_avg[0],lr_avg[1],lr_avg[2]))
print("ul [{:.4f}, {:.4f}, {:.4f}] |".format(ul_avg[0],ul_avg[1],ul_avg[2]), "ur [{:.4f}, {:.4f}, {:.4f}]".format(ur_avg[0],ur_avg[1],ur_avg[2]))
print("-"*29,"+","-"*29)
print("ll [{:.4f}, {:.4f}, {:.4f}] |".format(ll_avg[0],ll_avg[1],ll_avg[2]), "lr [{:.4f}, {:.4f}, {:.4f}]".format(lr_avg[0],lr_avg[1],lr_avg[2]))
# draw bounding boxes around the contours and show the result
for i,quadrent in enumerate(("ul","ur","ll","lr")):
    pair = quadrent_pairs[i]
    for parent,child in pair:
        xoff = 0
        yoff = 0
        if quadrent == 'ur':
            xoff = int(img.shape[1]/2)
        elif quadrent == 'll':
            yoff = int(img.shape[0]/2)
        elif quadrent == 'lr':
            xoff = int(img.shape[1]/2)
            yoff = int(img.shape[0]/2)
        draw.draw_box_around_contour(img, parent, ox = xoff, oy = yoff)
        draw.draw_box_around_contour(img, child, ox = xoff, oy = yoff,
                                     color = (0,0,255))

cv2.imshow('Contours',img)
            

top_scalex = (ul_avg[1]   + ur_avg[1]) / -2
top_offsetx = ur_avg[1] + top_scalex
bot_scalex = (ll_avg[1] + lr_avg[1]) / -2
bot_offsetx = lr_avg[1] + bot_scalex
avg_scalex = (top_scalex + bot_scalex) / 2
avg_offsetx = (top_offsetx + bot_offsetx) / 2

print("-"*80)
print("top x scale: {:.4f}, top x offset: {:.4f}".upper().format(top_scalex,
                                                                 top_offsetx))
print("bot x scale: {:.4f}, bot x offset: {:.4f}".upper().format(bot_scalex,
                                                                 bot_offsetx))
print("avg x scale: {:.4f}, avg x offset: {:.4f}".upper().format(avg_scalex,
                                                                 avg_offsetx))

left_scaley = (ul_avg[2] + ll_avg[2]) / -2
left_offsety = ll_avg[2] + left_scaley
right_scaley = (ur_avg[2] + lr_avg[2]) / -2
right_offsety = lr_avg[2] + right_scaley
avg_scaley = (left_scaley + right_scaley) / 2
avg_offsety = (left_offsety + right_offsety) / 2

print("-"*80)
print("left y scale: {:.4f}, left y offset: {:.4f}".upper().format(left_scaley,
                                                                 left_offsety))
print("right y scale: {:.4f}, right y offset: {:.4f}".upper().format(right_scaley,
                                                                 right_offsety))
print("avg y scale: {:.4f}, avg y offset: {:.4f}".upper().format(avg_scaley,
                                                                 avg_offsety))

print("="*80)
print("PERFECT SCALE")
print("SCALE X: {:.4f} SCALE Y: {:.4f}".format(avg_scalex,avg_scaley))      
print("ZERO X: {:.4f} ZERO Y: {:.4f}".format(avg_offsetx,avg_offsety))

import cv2

import crop
import calc
import pre_process
import draw


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

print("offsets for each quadrent")
print("ul", offsets[0])
print("ur", offsets[1])
print("ll", offsets[2])
print("lr", offsets[3])

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
            


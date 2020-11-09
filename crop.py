DEBUG = False

def getDimensions(img):
    r,c, = (None, None)
    if len(img.shape) == 3:
        r,c,_ = img.shape
    else:
        r,c = img.shape
    return (r,c)

def upperLeft(img):
    r,c = getDimensions(img)
    if DEBUG: print("[0:{rm}, 0:{cm}]".format(r=r,c=c,rm=int(r/2),cm=int(c/2))) 
    return img[0:int(r/2),0:int(c/2)]

def upperRight(img):
    r,c = getDimensions(img)
    if DEBUG: print("[0:{rm}, {cm}:{c}]".format(r=r,c=c,rm=int(r/2),cm=int(c/2)))
    return img[0:int(r/2),int(c/2):c]

def lowerLeft(img):
    r,c = getDimensions(img)
    if DEBUG: print("[{rm}:{r}, 0:{cm}]".format(r=r,c=c,rm=int(r/2),cm=int(c/2)))
    return img[int(r/2):r,0:int(c/2)]

def lowerRight(img):
    r,c = getDimensions(img)
    if DEBUG: print("[{rm}:{r}, {cm}:{c}]".format(r=r,c=c,rm=int(r/2),cm=int(c/2))) 
    return img[int(r/2):r,int(c/2):c]

#Simple Verification that images contain the same pixels
#ie Assignments function properly
#Compare image accuracy between algorithms

import collections
from PIL import Image, ImageCms

def CheckSame(im1: Image.Image, im2: Image.Image):
    im1_data = list(im1.getdata())
    im2_data = list(im2.getdata())

    return(collections.Counter(im1_data) == collections.Counter(im2_data))


#def AverageDistanceLab(im1, im2):
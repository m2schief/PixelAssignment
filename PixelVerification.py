#Simple Verification that images contain the same pixels
#ie Assignments function properly
#Compare image accuracy between algorithms

import collections
from PIL import Image

def CheckSame(im1: Image.Image, im2: Image.Image):
    im1_data = list(im1.getdata())
    im2_data = list(im2.getdata())

    return(collections.Counter(im1_data) == collections.Counter(im2_data))

random50 = Image.open("./images/50random50.bmp")
random_spiral = Image.open("./generated_images/random_spiral.bmp")

print(CheckSame(random50, random_spiral))
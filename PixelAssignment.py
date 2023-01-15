#Functions that load images and apply pixel assignments to create new images

import time
st = time.time()
from PIL import Image, ImageCms
from CostMatrices import *

#create LAB transform (better for sorting than RGB)
srgb_p = ImageCms.createProfile('sRGB')
lab_p = ImageCms.createProfile('LAB')
rgb2lab = ImageCms.buildTransformFromOpenProfiles(srgb_p, lab_p, 'RGB', 'LAB')
lab2rgb = ImageCms.buildTransformFromOpenProfiles(lab_p, srgb_p, 'LAB', 'RGB')



def MakeRandom(width: int, height: int):
    '''
    Makes a width*height sized image out of random RGB pixels
    '''

    rIm = Image.new('RGB', (width, height))
    rData = [(random.randrange(256), random.randrange(256), 
    random.randrange(256)) for i in range(width * height)]
    rIm.putdata(rData)

    return rIm

def HungarianAssignment(im1: Image.Image, im2: Image.Image):
    '''
    Arranges the pixels in im1 to resemble im2 using the Hungarian algorithm
    O(n^3). Images must be of same size.
    '''

    retIm = Image.new('RGB', im1.size)

    im1data = list(im1.getdata())
    im2data = list(im2.getdata())

    #arrange and insert data
    sortedData = AssignMatrix(im1data, im2data)
    retIm.putdata(sortedData)

    return retIm


spiral50 = Image.open("./images/spiral50.bmp")
random50 = Image.open("./images/50random50.bmp")

HungarianAssignment(random50, spiral50).save("./generated_images/random_spiral.bmp")
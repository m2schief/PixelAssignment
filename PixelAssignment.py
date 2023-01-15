#Functions that load images and apply pixel assignments to create new images

import time
st = time.time()
from PIL import Image, ImageCms
from CostMatrices import *
from PixelVerification import *
from MultiArray import *

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

    #data in RGB (for placing pixels) and LAB (for finding assignment)
    im1data = list(im1.getdata())

    im1data_lab = list(ImageCms.applyTransform(im1, rgb2lab).getdata())
    im2data_lab = list(ImageCms.applyTransform(im2, rgb2lab).getdata())
    #note this does affect these images in a way that can't be properly 
    #reversed. Best not to reuse the images after this function is called

    #generate cost matrix
    cost_matrix = TupleMatrixCost(im1data_lab, im2data_lab)

    #arrange data, insert into image
    sorted_data = AssignMatrix(im1data, cost_matrix)
    retIm.putdata(sorted_data)
    
    #print(CheckSame(im1, retIm))
    return retIm


def ArraySortAssignment(im1: Image.Image, im2: Image.Image):
    '''
    Arranges the pixels in im1 to resemble im2 using a custom sorting method
    O(n^2). Images must be of same size.
    '''

    retIm = Image.new('RGB', im1.size)

    #data in RGB (for placing pixels) and LAB (for finding assignment)
    im1data = list(im1.getdata())

    im1data_lab = list(ImageCms.applyTransform(im1, rgb2lab).getdata())
    im2data_lab = list(ImageCms.applyTransform(im2, rgb2lab).getdata())
    
    #encode locations for dat2 and RGB for dat1 (reversing LAB isn't 100% accurate)
    size = len(im1data)
    for i in range(size):
        im2data_lab[i] = (im2data_lab[i][0], im2data_lab[i][1], im2data_lab[i][2], i)
        im1data_lab[i] = (im1data_lab[i][0], im1data_lab[i][1], im1data_lab[i][2], im1data[i])
    
    dat1Array = ThreeArray(im1data_lab, len(im1data_lab), 1, 1)
    dat1Array.cuboidDimensions()
    dat1Array.sorted()
    dat1sort_lab = dat1Array.getData()

    dat2Array = ThreeArray(im2data_lab, len(im2data_lab), 1, 1)
    dat2Array.cuboidDimensions()
    dat2Array.sorted()
    dat2sort = dat2Array.getData()

    locations = [x[3] for x in dat2sort]
    dat1sort = [x[3] for x in dat1sort_lab]
    
    sortedArray = [0] * size
    for i in range(size):
        sortedArray[locations[i]] = dat1sort[i]
    
    retIm.putdata(sortedArray)

    #print(CheckSame(im1, retIm))
    return retIm




if __name__ == "__main__":
    flowers = Image.open("./images/flowers75.bmp")
    flowers_random = ArraySortAssignment(MakeRandom(75, 75), flowers)

    flowers_random.save("./generated_images/sorted_flowers_random.bmp")
    print(time.time() - st)
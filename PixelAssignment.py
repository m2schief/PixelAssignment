#Functions that load images and apply pixel assignments to create new images

import time
st = time.time()
from PIL import Image, ImageCms
from CostMatrices import *
from PixelVerification import *

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
    
if __name__ == "__main__":
    flowers = Image.open("./images/flowers75.bmp")
    flowers_random = HungarianAssignment(MakeRandom(75, 75), flowers)

    flowers_random.save("./generated_images/flowers_random.bmp")
    print(time.time() - st)
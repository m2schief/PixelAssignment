#Simple Verification that images contain the same pixels
#ie Assignments function properly
#Compare image accuracy between algorithms

import collections
from PIL import Image, ImageCms

def CheckSame(im1: Image.Image, im2: Image.Image):
    im1_data = list(im1.getdata())
    im2_data = list(im2.getdata())

    return(collections.Counter(im1_data) == collections.Counter(im2_data))


#create LAB transform (better for sorting than RGB)
srgb_p = ImageCms.createProfile('sRGB')
lab_p = ImageCms.createProfile('LAB')
rgb2lab = ImageCms.buildTransformFromOpenProfiles(srgb_p, lab_p, 'RGB', 'LAB')
lab2rgb = ImageCms.buildTransformFromOpenProfiles(lab_p, srgb_p, 'LAB', 'RGB')

def AverageDistanceLab(im1, im2):
    im1data_lab = list(ImageCms.applyTransform(im1, rgb2lab).getdata())
    im2data_lab = list(ImageCms.applyTransform(im2, rgb2lab).getdata())

    size = min( len(im1data_lab), len(im2data_lab) )
    run_sum = 0
    for i in range(size):
        run_sum += ((im1data_lab[i][0] - im2data_lab[i][0])**2 
        + (im1data_lab[i][1] - im2data_lab[i][1])**2 
        + (im1data_lab[i][2] - im2data_lab[i][2])**2)**(1/2)

    return run_sum/size


if __name__ == "__main__":
    '''
    flowers_sorted = Image.open("./generated_images/random_flowers_arraySort.bmp")
    flowers_hungarian = Image.open("./generated_images/random_flowers_hungarian.bmp")
    random75 = Image.open("./images/random75.bmp")
    flowers75 = Image.open("./images/flowers75.bmp")

    print(CheckSame(flowers_sorted, flowers_hungarian)) #true
    print(CheckSame(flowers_hungarian, random75)) #true

    print(AverageDistanceLab(flowers75, random75)) #94.55
    print(AverageDistanceLab(flowers75, flowers_hungarian)) #38.73
    print(AverageDistanceLab(flowers75, flowers_sorted)) #50.54
    

    lorikeet = Image.open("./images/lorikeet150.jpg")
    lorikeet_sorted = Image.open("./generated_images/lorikeet_arraysort_150.bmp")
    lorikeet_hungarian = Image.open("./generated_images/lorikeet_hungarian_150.bmp")
    random150 = Image.open("./images/random150.bmp")

    print(CheckSame(lorikeet_sorted, lorikeet_hungarian)) #True
    print(CheckSame(lorikeet_hungarian, random150)) #True
    
    print(AverageDistanceLab(lorikeet, random150)) #99.82
    print(AverageDistanceLab(lorikeet, lorikeet_hungarian)) #72.2
    print(AverageDistanceLab(lorikeet, lorikeet_sorted)) #79.83
    '''
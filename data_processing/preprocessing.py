from PIL import Image, ImageOps
import os
import matplotlib.pyplot as plt
import numpy as np
import cv2
import math
from enum import Enum
from Miura.MaximumCurvature import MaximumCurvature
from MATLAB.lee_region import lee_region
from MATLAB.huang_normalise import huang_normalise

class Device(Enum):
    UTSID = 1
    UTFVD = 2

GUIDE = "V1"
DEVICE = Device.UTSID
DATA_DIRECTORY = "C:\\Users\\Gebruiker\\OneDrive - University of Twente\\year 4\\Research Project\\Data\\Captures"
CROP_DIRECTORY = "C:\\Users\\Gebruiker\\OneDrive - University of Twente\\year 4\\Research Project\\Data\\Crop"
TEMPL_DIRECTORY = "C:\\Users\\Gebruiker\\OneDrive - University of Twente\\year 4\\Research Project\\Data\\Templates"
test_filename = "thomas_L_Middle_2_25.png"

FULL_DATA_DIRECTORY = os.path.join(DATA_DIRECTORY, GUIDE)
FULL_CROP_DIRECTORY = os.path.join(CROP_DIRECTORY, GUIDE)
FULL_TEMPL_DIRECTORY = os.path.join(TEMPL_DIRECTORY, GUIDE)
max_curvature = MaximumCurvature()

def preprocess(img, device: Device):

    if device == Device.UTSID:
        #Image cropping
        left = 390
        right = 690
        top = 50
        bottom = 520
    else:
        left = 0
        right = 590
        top = 0
        bottom = 330

    # crop img using points
    img = img.crop((left, top, right, bottom))

    #Image compression
    width, height = img.size
    new_width, new_height =  math.floor(width/1.5), math.floor(height/1.5)
    img = img.resize((new_width, new_height), Image.LANCZOS)

    #Image rotation
    arr = np.array(img)
    if device == Device.UTSID:
        arr = np.rot90(arr)
        arr = cv2.cvtColor(arr, cv2.COLOR_BGR2GRAY) 
    
    #Histogram equalization          
    equ = cv2.equalizeHist(arr)

    #Show images next to each other
    # disp = np.hstack((arr,equ)) #stacking images side-by-side
    # disp = Image.fromarray(disp)
    # disp.show()
   
    # Return as a PIL.img
    result = Image.fromarray(equ)
    return result

# img = Image.open(os.path.join(FULL_DATA_DIRECTORY, test_filename), mode="r")
# preprocess(img, DEVICE)

#TODO: EMPTY FOLDER BEFORE FILLING IT AGAIN
def batch_preprocess(src_directory):
    for file in os.listdir(src_directory):
        filename = os.fsdecode(file)
        img = Image.open(os.path.join(FULL_DATA_DIRECTORY, filename), mode="r")
        result = preprocess(img, DEVICE)
        plt.imsave(os.path.join(FULL_CROP_DIRECTORY, filename), result, cmap="grey")
    print("[INFO] Batch preprocessing completed")

def generate_template(img):
    img = ImageOps.grayscale(img) 
    im_arr = np.array(img)
    region, edges = lee_region(im_arr, 4, 40)
    im_arr, region, _, _ = huang_normalise(im_arr, region, edges)
    templ = max_curvature(im_arr, region)
    print("[INFO] Template Generated")

    return templ

#TODO: EMPTY FOLDER BEFORE FILLING IT AGAIN
def batch_templates(src_directory):
    for file in os.listdir(src_directory):
        filename = os.fsdecode(file)
        img = Image.open(os.path.join(FULL_CROP_DIRECTORY, filename), mode="r")
        result = generate_template(img)
        plt.imsave(os.path.join(FULL_TEMPL_DIRECTORY, filename), result, cmap="grey") #TODO: CMAP?
    print("[INFO] Batch template generation completed")

batch_preprocess(FULL_DATA_DIRECTORY)
batch_templates(FULL_CROP_DIRECTORY)

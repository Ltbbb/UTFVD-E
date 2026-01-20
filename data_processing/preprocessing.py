from PIL import Image
import os
import matplotlib.pyplot as plt
import numpy as np
import cv2
import math

GUIDE = "V11"
DATA_DIRECTORY = "C:\\Users\\Gebruiker\\OneDrive - University of Twente\\year 4\\Research Project\\Data\\Captures"
CROP_DIRECTORY = "C:\\Users\\Gebruiker\\OneDrive - University of Twente\\year 4\\Research Project\\Data\\Crop"
test_filename = "edwin_L_Index_50_1_0.png"

FULL_DATA_DIRECTORY = os.path.join(DATA_DIRECTORY, GUIDE)
FULL_CROP_DIRECTORY = os.path.join(CROP_DIRECTORY, GUIDE)

def preprocess_UTSID(img):

    #Image cropping
    left = 360
    right = 700
    top = 50
    bottom = 600
    # crop img using points
    img = img.crop((left, top, right, bottom))

    #Image compression
    width, height = img.size
    new_width, new_height =  math.floor(width/1.5), math.floor(height/1.5)
    img = img.resize((new_width, new_height), Image.LANCZOS)

    #Image rotation
    arr = np.array(img)
    rotate = np.rot90(arr)
    
    #Histogram equalization
    rotate = cv2.cvtColor(rotate, cv2.COLOR_BGR2GRAY)
    equ = cv2.equalizeHist(rotate)

    #Show images next to each other
    # disp = np.hstack((rotate,equ)) #stacking images side-by-side
    # disp = Image.fromarray(disp)
    # disp.show()
   
    # Return as a PIL.img
    return Image.fromarray(equ)

def preprocess_UTFVD(img):

    #Image compression
    width, height = img.size
    new_width, new_height =  math.floor(width/1.5), math.floor(height/1.5)
    img = img.resize((new_width, new_height), Image.LANCZOS)

    #Image rotation
    arr = np.array(img)
    rotate = np.rot90(arr)
    
    #Histogram equalization
    equ = cv2.equalizeHist(rotate)

    #Show images next to each other
    # disp = np.hstack((rotate,equ)) #stacking images side-by-side
    # disp = Image.fromarray(disp)
    # disp.show()
   
    # Return as a PIL.img
    return Image.fromarray(equ)


# preprocess(test_filename)

def batch_preprocess_UTSID(src_directory):
    for file in os.listdir(src_directory):
        filename = os.fsdecode(file)
        img = Image.open(os.path.join(FULL_DATA_DIRECTORY, filename), mode="r")
        result = preprocess_UTSID(img)
        plt.imsave(os.path.join(FULL_CROP_DIRECTORY, filename), result, cmap="grey")
    print("[INFO] Batch preprocessing completed")

def batch_preprocess_UTFVD(src_directory):
    for file in os.listdir(src_directory):
        filename = os.fsdecode(file)
        img = Image.open(os.path.join(FULL_DATA_DIRECTORY, filename), mode="r")
        result = preprocess_UTFVD(img)
        plt.imsave(os.path.join(FULL_CROP_DIRECTORY, filename), result, cmap="grey")
    print("[INFO] Batch preprocessing completed")

# batch_preprocess(FULL_DATA_DIRECTORY)
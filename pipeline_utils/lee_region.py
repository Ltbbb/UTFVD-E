import cv2
import math
import numpy as np
from PIL import Image

# Localise the finger region using Lee's method

# Parameters:
#  img    - Input vascular image
#  mask_h - Height of the mask
#  mask_w - Width of the mask

# Returns:
#  region - Binary mask indicating the finger region
#  edges  - Matrix containing two rows, first row corresponds to the 
#           y-positions of the upper finger edge and the second row
#           corresponds to the y-positions of the lower finger edge.

# Reference:
# Finger vein recognition using minutia-based alignment and local binary
#   pattern-based feature extraction
# E.C. Lee, H.C. Lee and K.R. Park
# International Journal of Imaging Systems and Technology
#   Volume 19, Issue 3, September 2009, Pages 175-178   
# doi: 10.1002/ima.20193

# Author:  Bram Ton <b.t.ton@alumnus.utwente.nl>
# Date:    20th March 2012
# License: Simplified BSD License

def lee_region(img, mask_h, mask_w): 

    [img_h, img_w] = img.shape
    
    # im = Image.fromarray(img)
    # im.show()

    # Determine lower half starting point
    if img_h % 2 == 0:
        half_img_h = img_h/2
    else:
        half_img_h = math.ceil(img_h/2)

    # Construct mask for filtering
    mask = np.zeros((mask_h,mask_w));
    mask[:int(mask_h/2)] = -1;    
    mask[int(mask_h/2):] = 1;

    # Filter image using mask
    img_filt = cv2.filter2D(img, cv2.CV_32F, mask) #NOTE: this filter returns just slightly different results than the MATLAB function
    # im = Image.fromarray(img_filt)
    # im.show(title="img_filt")

    # Upper part of filtred image
    img_filt_up = img_filt[:int(half_img_h-1), :];
    y_up = np.argmax(img_filt_up, axis=0)

    # Lower part of filtred image
    img_filt_lo = img_filt[int(half_img_h-1):, :];
    y_lo = np.argmin(img_filt_lo, axis=0)

    # Fill region between upper and lower edges
    region = np.zeros(img.shape)
    img_filt_lo_h = img_filt_lo.shape[0]
    for i in range(img_w - 1):
        region[y_up[i] : y_lo[i]+img_filt_lo_h, i] = 255
    # im = Image.fromarray(region)
    # im.show(title="mask")

    # Save y-position of finger edges
    edges = np.zeros((2,img_w))
    edges[0,:] = y_up
    edges[1,:] = np.round(y_lo + img_filt_lo_h)
    
    return region, edges

# testing
# img = cv2.imread("test_imgs/1.png", cv2.IMREAD_GRAYSCALE) #NOTE: reading in grayscale is important!
# lee_region(img, 4, 40)
import cv2
from Miura.MaximumCurvature import MaximumCurvature
from Miura.MiuraMatch import MiuraMatch
from MATLAB.lee_region import lee_region
from MATLAB.huang_normalise import huang_normalise

#create instances of runnable objs
max_curvature = MaximumCurvature()
miura_match = MiuraMatch()

#define imgs
imgpath1 = "test_imgs/1.png"
img1 = cv2.imread(imgpath1, 0)

#get both img templates
region, edges = lee_region(img1, 4, 40)
img, region = huang_normalise(img1, region, edges)



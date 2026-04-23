import cv2
from Miura.MaximumCurvature import MaximumCurvature
from Miura.MiuraMatch import MiuraMatch
from MATLAB.lee_region import lee_region
from MATLAB.huang_normalise import huang_normalise
from MATLAB.miura_match import miura_match
import numpy as np

#create instances of runnable objs
max_curvature = MaximumCurvature()

#define imgs
imgpath1 = "C:\\Users\\Gebruiker\\OneDrive - University of Twente\\year 4\\Research Project\\Data\\Crop\\VU\\jaridza_L_Middle_1_7.png"
img1 = cv2.imread(imgpath1, 0)
imgpath2 = "C:\\Users\\Gebruiker\\OneDrive - University of Twente\\year 4\\Research Project\\Data\\Crop\\VU\\jaridza_L_Middle_1_1.png"
img2 = cv2.imread(imgpath2, 0)

#get both img templates
region1, edges1 = lee_region(img1, 4, 40)
img1, region1, _, _ = huang_normalise(img1, region1, edges1)
templ1 = max_curvature(img1, region1)

region2, edges2 = lee_region(img2, 4, 40)
img2, region2, _, _ = huang_normalise(img2, region2, edges2)
templ2 = max_curvature(img2,region2)

imgpath1 = "C:\\Users\\Gebruiker\\OneDrive - University of Twente\\year 4\\Research Project\\Data\\Templates\\VU\\jaridza_L_Middle_1_7.png"
img1 = cv2.imread(imgpath1, 0)
imgpath2 = "C:\\Users\\Gebruiker\\OneDrive - University of Twente\\year 4\\Research Project\\Data\\Templates\\VU\\jaridza_L_Middle_1_1.png"

img_a = cv2.imread(imgpath1, 0)
templa = np.array([[1 if i == 255 else 0 for i in row] for row in img_a])
img_b = cv2.imread(imgpath2, 0)
templb = np.array([[1 if i == 255 else 0 for i in row] for row in img_b])

score = miura_match(templ1, templ2, 50, 50)
print(score)
score = miura_match(templa, templb, 50, 50)
print(score)

miura_match2 = MiuraMatch()
score, _, _ = miura_match2.score(templ1, templ2)
print(score)
score, _, _ = miura_match2.score(templa, templb)
print(score)





import numpy as np
from sklearn import linear_model
import statsmodels.api as sm
import cv2

# Simple finger normalisation, it aligns the finger to the centre of the 
# image using an affine transformation, Elliptic projection which is
# described in the referenced paper is not included,

# Parameters:
#  img   - Input vascular image
#  region   - Binary image of the finger region
#  edges - Edges of the finger, first row contains the y-coordinates of 
#          the top edge and the second row contains the y-coordinates of
#          the bottom edge,

# Returns:
#  img - Transformed image
#  region - Transformed finger region
#  rot - Rotation in degrees applied by the transformation
#  tr  - Translation in pixels applied in transformation

# Reference:
# Finger-vein authentication based on wide line detector and pattern 
#    normalization
# B. Huang, Y. Dai, R. Li, D. Tang and W. Li
# 20th International Conference on Pattern Recognition (ICPR), 2010 
# doi: 10.1109/ICPR.2010.316

# Author:  Bram Ton <b.t.ton@alumnus.utwente.nl>
# Date:    13th March 2012
# License: Simplified BSD License
def huang_normalise(img, region, edges):
    [img_h, img_w] = img.shape
    bl = edges.mean(axis=0) # Base line

    # Fit a straight line through the base line points
    X = np.arange(1, img_w + 1, 1)

    # Alternative for brob: statsmodels
    # Xc = sm.add_constant(X)
    # model = sm.RLM(bl, Xc)
    # results = model.fit()
    # brob = results.params
    # print(brob)

    #Alternative for brob: sklearn
    Xr = X.reshape(-1,1)
    ransac = linear_model.RANSACRegressor()
    ransac.fit(Xr,bl)
    brob = [ransac.estimator_.intercept_.item(), ransac.estimator_.coef_[0].item()]
    # print(brob)

    #Plot line to show brob
    # m, b = ransac.estimator_.intercept_, ransac.estimator_.coef_
    # x = np.linspace(-100.,100.)
    # _,ax = plt.subplots()
    # ax.plot(x,m*x+b)
    # ax.set_xlim((0,10))
    # ax.set_ylim((0,900))
    # plt.show()

    rot = -1 * np.arctan(brob[1]); # Rotation
    tr = img_h/2 - brob[0]; # Translation

    # Construct the matrix for an affine transform
    affine_matrix = np.array([[np.cos(rot), -np.sin(rot), 0],
                              [np.sin(rot), np.cos(rot), tr],
                              [0,0,1]]) #NOTE: this is a transpose of the matrix in MATLAB

    # Apply affine transformation to img
    img_transformed = cv2.warpPerspective(img, affine_matrix, (img_w, img_h))
    # print(type(img_transformed))
    # disp = Image.fromarray(img_transformed)
    # disp.show()

    # Apply affine transformation to finger vein region (with nearest neighbor interpolation)
    region_transformed = cv2.warpPerspective(region, affine_matrix, (img_w, img_h), flags=cv2.INTER_NEAREST)

    rot = rot*(180/np.pi); # Convert radians to degrees
    return img_transformed, region_transformed, rot, tr

# from MATLAB.lee_region import lee_region

# imgpath1 = "MATLAB/1_comp.png"
# img1 = cv2.imread(imgpath1, 0)
# region, edges = lee_region(img1, 4, 40)
# huang_normalise(img1, region, edges)


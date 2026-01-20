import os, h5py, itertools, datetime
import numpy as np
import seaborn as sns
from PIL import Image
import matplotlib
import matplotlib.pyplot as plt
from MATLAB.lee_region import lee_region
from data_processing.preprocessing import preprocess
from Miura.MaximumCurvature import MaximumCurvature
from Miura.MiuraMatch import MiuraMatch

max_curvature = MaximumCurvature()
miura_match = MiuraMatch()

GUIDE = "VU"
DATA_DIRECTORY = "C:\\Users\\Gebruiker\\OneDrive - University of Twente\\year 4\\Research Project\\Data\\Captures"
CROP_DIRECTORY = "C:\\Users\\Gebruiker\\OneDrive - University of Twente\\year 4\\Research Project\\Data\\Crop"

FULL_DATA_DIRECTORY = os.path.join(DATA_DIRECTORY, GUIDE)
FULL_CROP_DIRECTORY = os.path.join(CROP_DIRECTORY, GUIDE)

def load_imgs(directory):
    dict = {}

    for file in os.listdir(directory):
        #Load image
        filename = os.fsdecode(file)
        im = Image.open(os.path.join(directory, filename))

        #Preprocess the image
        im = preprocess(im)

        im_arr = np.array(im)
        mask, _ = lee_region(im_arr, 4, 40)
        templ = max_curvature(im_arr, mask)

        print("[INFO] Processed Image")

        #Store in dictionary. The key is the filename and the template object the value
        dict[filename] = templ.tolist()

    return dict

def compare_whole_dataset(dict):
    #Function to extract the name and finger portion of the img name
    #Example: Lisa_L_Index
    def split(filename):
        thing = filename.split("_")
        return thing[:3]
    

    matching_values = []
    non_matching_values = []

    print("[INFO] Scoring all combinations in dataset...")
    #Iterate over all combinations
    for a, b in itertools.combinations(dict, 2):
        
        # img1 = cv2.imread(os.path.join(FULL_DATA_DIRECTORY, a))
        # img2 = cv2.imread(os.path.join(FULL_DATA_DIRECTORY, b))

        templ1 = np.array(dict.get(a))
        templ2 = np.array(dict.get(b))

        score, _, _ = miura_match.score(templ1, templ2)
        rounded_score = score.item()

        #If the name + finger are the same, add the found value to the corresponding array
        if split(a) == split(b):
            matching_values.append(rounded_score)
        else:
            non_matching_values.append(rounded_score)
        print("[INFO] Scoring of pair done")

    print("[INFO] Matching done") 

    time = datetime.datetime.now()
    with h5py.File("data_processing/data.hdf5", "w") as file:
        file.create_dataset(str(time) + " " + GUIDE + " matching", data = matching_values)
        file.create_dataset(str(time) + " " + GUIDE + " non_matching", data = non_matching_values)

    return matching_values, non_matching_values

# dictonairy = load_imgs(FULL_DATA_DIRECTORY)
# match, nomatch = compare_whole_dataset(dictonairy)
# print(match,nomatch)

match = [0.24684919600173838, 0.21328531412565027] 
nomatch = [0.08908868001634655, 0.09439788266431408, 0.10506329113924051, 0.10232558139534885, 0.08989266547406083, 0.09339158929546695, 0.09181553801412548, 0.08732737611697808, 0.09001636661211129, 0.09636062861869313, 0.09090909090909093, 0.08726534753932014, 0.11326994625878462, 0.10982658959537572, 0.1079136690647482, 0.09909090909090909, 0.08041329739442948, 0.11826159632260763, 0.11102139685102948, 0.10261914984972093, 0.08593396653098144, 0.09418402777777779, 0.08337303477846593, 0.10524073285044738, 0.10618216139688533, 0.09639953542392567]

range = [0.0,0.5]

plt.hist(match, range=range, density=True, bins=60, alpha=0.5, color='blue', label='Matching')
plt.hist(nomatch, range=range, density=True, bins=60, alpha=0.5, color='red', label='Non-Matching')
plt.title('Normalized Histogram')
plt.xlabel('Correlation Score')
plt.ylabel('Normalized Frequency')
plt.legend(loc='upper right')

plt.show()

def DETCurve(fps,fns):
    """
    Given false positive and false negative rates, produce a DET Curve.
    The false positive rate is assumed to be increasing while the false
    negative rate is assumed to be decreasing.
    """
    axis_min = min(fps[0],fns[-1])
    fig,ax = plt.subplots()
    plt.plot(fps,fns)
    ticks_to_use = [0.001,0.002,0.005,0.01,0.02,0.05,0.1,0.2,0.5,1,2,5,10,20,50]
    ax.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
    ax.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
    ax.set_xticks(ticks_to_use)
    ax.set_yticks(ticks_to_use)
    plt.axis([0.001,50,0.001,50])
    plt.show()

DETCurve(match.mean(), nomatch.mean())



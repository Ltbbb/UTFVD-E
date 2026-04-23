import os, h5py, itertools, datetime, matplotlib
import numpy as np
import cv2
from Miura.MiuraMatch import MiuraMatch
import data_processing.graphs as graphs

miura_match = MiuraMatch(cw=50,ch=50) #NOTE: params are changed 

GUIDE = "VU"
TEMPL_DIRECTORY = "C:\\Users\\Gebruiker\\OneDrive - University of Twente\\year 4\\Research Project\\Data\\Templates"

FULL_TEMPL_DIRECTORY = os.path.join(TEMPL_DIRECTORY, GUIDE)

def compare_dataset(directory):
        #Function to extract the name and finger portion of the img name
        #Example: Lisa_L_Index
        def split(filename):
            thing = filename.split("_")
            return thing[:3]
        
        matching_values = []
        non_matching_values = []

        print("[INFO] Scoring all combinations in dataset...")

        #Iterate over all combinations
        for a, b in itertools.combinations(os.listdir(directory), 2):
            
            # img1 = cv2.imread(os.path.join(FULL_DATA_DIRECTORY, a))
            # img2 = cv2.imread(os.path.join(FULL_DATA_DIRECTORY, b))

            # import the image as pixels
            img_a = cv2.imread(os.path.join(directory, a), 0)
            templ1 = np.array([[1 if i == 255 else 0 for i in row] for row in img_a])
            img_b = cv2.imread(os.path.join(directory, b), 0)
            templ2 = np.array([[1 if i == 255 else 0 for i in row] for row in img_b])

            score, _, _ = miura_match.score(templ1, templ2)
            rounded_score = score.item()

            #If the name + finger are the same, add the found value to the corresponding array
            if split(a) == split(b):
                matching_values.append(rounded_score)
            else:
                non_matching_values.append(rounded_score)
            print(f"[INFO] Scoring of pair done: {rounded_score}")

        print("[INFO] Matching done") 

        time = datetime.datetime.now()
        with h5py.File("data_processing/data.hdf5", "w") as file:
            file.create_dataset(str(time) + " " + GUIDE + " matching", data = matching_values)
            file.create_dataset(str(time) + " " + GUIDE + " non_matching", data = non_matching_values)

        return matching_values, non_matching_values

match, nomatch = compare_dataset(FULL_TEMPL_DIRECTORY)
match = [round(n, 3) for n in match]
nomatch = [round(n, 3) for n in nomatch]

det_curve = graphs.DET_curve(graphs.THRESHOLDS)
det_curve(match, nomatch, GUIDE)
hist = graphs.Histogram()
hist(match,nomatch, GUIDE)

print(np.mean(match))
print(np.mean(nomatch))




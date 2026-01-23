
import os

personname = "person"
directory_path = f"C:\\Users\\Gebruiker\\OneDrive - University of Twente\\year 4\\Research Project\\Data\\Captures\\VU\\{personname}"
# test_file_name = "edwin_L_index_50_1_0.png"

def refactor_file_UTSID(filename):
    filename = filename[:-4]
    separator = "_"
    parts = filename.split(separator)
    pwm = parts[-3]
    parts.remove(pwm)
    parts.append(pwm)
    new_name = separator.join(parts) + ".png"
    return new_name

fingers = ["L_Index", "L_Middle", "L_ring", "R_Index", "R_Middle", "R_ring"]
finger_ctr = 0;
ctr = 0;
SESSION_NUMBER = 1
def refactor_file_UTFVD(personname):
    global finger_ctr, ctr, fingers, SESSION_NUMBER
    finger = fingers[finger_ctr]
    new_name = f"{personname}_{finger}_{SESSION_NUMBER}_{ctr}.png"

    if finger_ctr == 5:
        finger_ctr = 0
    else:
        finger_ctr += 1
    ctr += 1
    return new_name

def refactor_files_UTSID(directory):
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        new_name = refactor_file_UTSID(filename)
        old_filename = os.path.join(directory_path, filename)
        new_filename = os.path.join(directory_path, new_name)
        print(old_filename)
        print(new_filename)
        os.rename(old_filename, new_filename)

def refactor_files_UTFVD(directory):
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        new_name = refactor_file_UTFVD(personname)
        old_filename = os.path.join(directory_path, filename)
        new_filename = os.path.join(directory_path, new_name)
        print(old_filename)
        print(new_filename)
        os.rename(old_filename, new_filename)

# refactor_file(test_file_name)
refactor_files_UTFVD(directory_path)

import os

directory_path = "C:\\Users\\Gebruiker\\OneDrive - University of Twente\\year 4\\Research Project\\Data\\Originals\\V4"
# test_file_name = "edwin_L_index_50_1_0.png"

def refactor_file(filename):
    filename = filename[:-4]
    separator = "_"
    parts = filename.split(separator)
    pwm = parts[-3]
    parts.remove(pwm)
    parts.append(pwm)
    new_name = separator.join(parts) + ".png"
    return new_name

def refactor_files(directory):
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        new_name = refactor_file(filename)
        old_filename = os.path.join(directory_path, filename)
        new_filename = os.path.join(directory_path, new_name)
        print(old_filename)
        print(new_filename)
        os.rename(old_filename, new_filename)

# refactor_file(test_file_name)
refactor_files(directory_path)
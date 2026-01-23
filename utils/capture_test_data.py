import cv2
from picamera2 import Picamera2
import time
import utils.capture_framework as cf
from enum import Enum

KEY_NEXT_FINGER = "j"
KEY_PREV_FINGER = "l"
IMAGE_FOLDER = "img" 
img_ctr = 0

# FINGER_IDX = 0
# FINGER = ["L_Index", "L_Middle", "L_Ring", "R_Index", "R_Middle", "R_Ring"]
# IMG_PATHS_CONTAINER = [[],[],[],[],[],[]] #NOTE! has to contain the same amt of listed lists as len(FINGER)

class Finger(Enum):
    L_INDEX = 1
    L_MIDDLE = 2
    L_RING = 3
    R_INDEX = 4
    R_MIDDLE = 5
    R_RING = 6

class Guide(Enum):
    V1 = 1
    V2 = 2
    V3 = 3
    V4 = 4
    VU = 5

def main():
    picam2 = Picamera2()
    cf.init_cam(picam2)
    cf.capture_images(picam2, capture_test_data)
    # best_img_f, best_img_l = determine_best_img()

    # #Display the best image
    # if best_img_f == best_img_l:
    #     display_img(best_img_f, "Best Image :)")
    # else:
    #     display_img(best_img_l, "Best Image Laplace")
    #     display_img(best_img_f, "Best Image Fourier")

def capture_test_data(frame):
    global FINGER_IDX, FINGER, IMG_PATHS_CONTAINER, KEY_NEXT_FINGER, KEY_PREV_FINGER

    current_guide_name = Guide(1)
    current_finger_name = Finger(1)
    current_finger_array = IMG_PATHS_CONTAINER[FINGER_IDX]

    cf.display_on_frame(f"Capturing {current_finger_name}")

    key = cv2.waitKey(1)   

    match key:
        case ord(cf.KEY_TAKE_PICTURE):
            img_ctr = len(current_finger_array) + 1
            image_name = f'{IMAGE_FOLDER}/{current_finger_name}_{img_ctr}.jpg'
            cv2.imwrite(image_name, frame)
            current_finger_array.append(image_name)
            cf.display_on_frame(f"Image captured and saved as '{image_name}'.")
            time.sleep(1) #TODO: delay to see img captured
        case ord(KEY_NEXT_FINGER):
            if not FINGER_IDX >= len(FINGER) - 1:
                FINGER_IDX += 1
        case ord(KEY_PREV_FINGER):
            if not FINGER_IDX == 0:
                FINGER_IDX -= 1
        case ord(cf.KEY_QUIT):
            cf.turn_off_leds()
            raise Exception("Closing capture!")

#run main
# main()
print(Finger(1))


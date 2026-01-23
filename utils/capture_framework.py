import cv2
from picamera2 import Picamera2
import time

class Framework():

    def __init__(self):
        #set values
        self.frame = None

        #Init picamera
        self.picam2 = Picamera2()
        config = self.picam2.create_still_configuration()  # Use still configuration
        self.picam2.configure(config)
        self.picam2.set_controls({"ExposureTime": 5000})
        self.picam2.start()

        # Give some time to the camera to start
        time.sleep(2)

        print("capturing images...")
        self.capture_images()
        
    def capture_images(self):
        while True:
            # Capture frame-by-frame
            self.frame = self.picam2.capture_array()

            try:
                self.on_frame(self.frame)
            except Exception as e:
                print(e)
                break
            
        # Release resources
        self.picam2.stop()

    def on_frame(self, frame):
        print("frame")
        return frame

    def display_img(self, img_path: str, caption: str):
        if img_path is not None:
            img = cv2.imread(img_path)
            cv2.imshow(caption, img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

    def display_on_frame(self, msg: str):
        print(msg) #TODO: draw on frame

if __name__ == "__main__":
    Framework()
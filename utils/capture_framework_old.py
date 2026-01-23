import cv2
from picamera2 import Picamera2
import time
import read_write as rw

class Framework():

    def __init__(self):
        #set values
        self.brightness = 0
        self.zoom_factor = 1
        self.pwm_val = 0
        self.KEY_TAKE_PICTURE = "i"
        self.KEY_QUIT = "q"

        #Init picamera
        self.picam2 = Picamera2()
        config = self.picam2.create_still_configuration()  # Use still configuration
        self.picam2.configure(config)
        self.picam2.set_controls({"ExposureTime": 5000})
        self.picam2.start()

        print("picam started")

        # Give some time to the camera to start
        time.sleep(2)

        cv2.namedWindow('Camera')
        #cv2.setWindowProperty('Camera',cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)

        # Create trackbars for brightness and zoom
        cv2.createTrackbar('Brightness', 'Camera', 50, 100, self.on_brightness_change)
        cv2.createTrackbar('Zoom', 'Camera', 2, 20, self.on_zoom_change)
        cv2.createTrackbar('PWM', 'Camera', 100, 350, self.on_pwm_change)

        print("capturing images...")
        self.capture_images()
        
    def capture_images(self):
        while True:
            # Capture frame-by-frame
            frame = self.picam2.capture_array()

            # Adjust brightness and zoom
            frame = self.adjust_brightness(frame, self.brightness)
            frame = self.apply_zoom(frame, self.zoom_factor)

            # Display the frame
            cv2.imshow('Camera', frame)

            try:
                self.on_frame(frame)
            except Exception as e:
                print(e)
                break
            
        # Release resources
        cv2.destroyAllWindows()
        self.picam2.stop()

    def on_frame(self, frame):
        return frame

    # Function to adjust the brightness of the image
    def adjust_brightness(self, image, brightness):
        return cv2.convertScaleAbs(image, alpha=1, beta=brightness)

    # Function to apply zoom on the image
    def apply_zoom(self, image, zoom_factor):
        height, width = image.shape[:2]
        center_x, center_y = width // 2, height // 2
        radius_x, radius_y = int(center_x / zoom_factor), int(center_y / zoom_factor)

        min_x, max_x = center_x - radius_x, center_x + radius_x
        min_y, max_y = center_y - radius_y, center_y + radius_y

        # Ensure the coordinates are within bounds
        min_x, max_x = max(min_x, 0), min(max_x, width)
        min_y, max_y = max(min_y, 0), min(max_y, height)

        cropped = image[min_y:max_y, min_x:max_x]
        return cv2.resize(cropped, (width, height))

    # Callback functions for trackbars
    def on_brightness_change(self, val):
        self.brightness = val - 50
        print(f"Brightness changed to: {self.brightness}")

    def on_zoom_change(self, val):
        self.zoom_factor = 1 + val / 10
        print(f"Zoom factor changed to: {self.zoom_factor}")
        
    def on_pwm_change(self, val):
        self.pwm_val= val*10
        print(f"PWM factor changed to: {self.pwm_val}")
        rw.send_to_arduino(self.pwm_val)
        
    def turn_off_leds(self):
        rw.send_to_arduino(0)

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
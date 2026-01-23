from utils.capture_framework import Framework
import cv2
import os
import numpy as np

class CaptureAssess(Framework): #inherit from framework
    KEY_TAKE_PICTURE = "i"
    KEY_QUIT = "q"
    
    def __init__(self):
        self.IMAGE_FOLDER = "img"
        self.img_ctr = 0
        super().__init__() #init framework with capture multiple as callback

    def on_frame(self, frame):
        # Check for key press
        key = cv2.waitKey(1)
            
        if key == ord(self.KEY_TAKE_PICTURE):
            self.img_ctr += 1
            if not os.path.exists(f"{self.IMAGE_FOLDER}"):
                raise Exception(f"There is no folder called '{self.IMAGE_FOLDER}' in the current directory!")
                #TODO: create folder for them?
            #TODO: empty image folder?
            image_name = f'{self.IMAGE_FOLDER}/image_{self.img_ctr}.jpg'
            cv2.imwrite(image_name, frame)
            print(f"Image captured and saved as '{image_name}'.")
        elif key == ord(self.KEY_QUIT):
            Framework.turn_off_leds()
            raise Exception("Closing capture!") #FIXME: is there a better way to do this?
    
    def determine_best_img(self):
        # Determine the best quality image using both Laplacian variance and Fourier sharpness
        best_laplace_img = None
        best_fourier_img = None

        #init to 0
        best_laplacian_variance = 0
        best_fourier_sharpness = 0

        for image_path in os.listdir(self.IMAGE_FOLDER):
            image = cv2.imread(image_path)
            laplacian_var = self.laplacian_variance(image)
            fourier_sharp = self.fourier_sharpness(image)
            print(f"Image: {image_path}, Laplacian Variance: {laplacian_var}, Fourier Sharpness: {fourier_sharp}")

            if laplacian_var > best_laplacian_variance:
                best_laplacian_variance = laplacian_var
                best_laplace_img = image_path

            if fourier_sharp > best_fourier_sharpness:
                best_fourier_sharpness = fourier_sharp
                best_fourier_img = image_path

        #TODO: combine metrics in a better way
        print(f"Best quality fourier: '{best_fourier_img}' with value {best_fourier_sharpness}.")
        print(f"Best quality laplace: '{best_laplace_img} with value {best_laplacian_variance}.") 
        
        return best_fourier_img, best_laplace_img
    
    # Function to calculate the Laplacian variance of an image
    def laplacian_variance(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        laplacian = cv2.Laplacian(gray, cv2.CV_64F)
        variance = laplacian.var()
        return variance

    # Function to calculate the sum of the magnitude spectrum from the Fourier Transform
    def fourier_sharpness(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        dft = cv2.dft(np.float32(gray), flags=cv2.DFT_COMPLEX_OUTPUT)
        dft_shift = np.fft.fftshift(dft)
        magnitude_spectrum = cv2.magnitude(dft_shift[:, :, 0], dft_shift[:, :, 1])
        sharpness = np.sum(magnitude_spectrum)
        return sharpness
    
if __name__ == "__main__":
    CaptureAssess()
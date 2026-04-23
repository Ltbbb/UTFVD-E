import tkinter as tk
from tkinter import ttk
import cv2
from PIL import Image, ImageTk, ImageOps
import threading
# from picamera2 import Picamera2
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror, showwarning, showinfo
from GUI.settings_frame import SettingsFrame


SESSION_NUMBER = 1
HALF_SCREEN_WIDTH = 512

class VideoFrame(ttk.Frame):

    def __init__(self, parent, settingsframe: SettingsFrame):
        s = ttk.Style()
        s.configure("Video.TFrame", background="orange")
        super().__init__(parent, style="Video.TFrame")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=9)
        self.grid_rowconfigure(1, weight=1)

        self.settingsframe = settingsframe

        button = tk.Button(self, text="CAPTURE", command=self.capture_img)
        button.grid(column=0, row=1, sticky="news")

        default_img = Image.open("test_imgs/1.png")
        default_img = ImageTk.PhotoImage(default_img)
        panel_frame = tk.Frame(self)
        panel_frame.grid(column=0, row=0, sticky="nsew")
        self.panel = tk.Label(panel_frame, image=default_img, anchor="center")
        self.panel.grid(sticky="news")
        
        self.video_frame = None
        self.img_ctr = 0

        #create picam object to use for video streaming
        # self.picam2 = Picamera2()
        # config = self.picam2.create_still_configuration()  #TODO: change configuration?
        # self.picam2.configure(config)
        # self.picam2.set_controls({"ExposureTime": 5000})
        # self.picam2.start()

        #start a thread that constantly pools the video sensor for
		# the most recently read frame
        self.stopEvent = threading.Event()
        self.thread = threading.Thread(target=self.videoLoop, args=())
        self.thread.start()
    
    def capture_img(self):
        global SESSION_NUMBER
        currentfinger = self.settingsframe.currentfinger
        currentguide = self.settingsframe.currentguide
        participantname = self.settingsframe.participantname
        print("button press!!!!")
        if currentfinger == None or currentguide == None or participantname == None:
            showwarning("Warning!", "Fill in all fields")
        capture = self.video_frame
        image_name = f'data/{currentguide}/{participantname}_{currentfinger}_{SESSION_NUMBER}_{self.img_ctr}.png' #TODO: Image storage #TODO: impl counter
        print(image_name)
        self.img_ctr += 1
        if not cv2.imwrite(image_name, capture):
            raise Exception("could not write img")

    def videoLoop(self):
		
		# try/except statement is a pretty ugly hack to get around
		# a RunTime error that Tkinter throws due to threading
        try:
            while not self.stopEvent.is_set(): #TODO: stop event
				#use picam to capture the frames and resize
                # self.video_frame = self.picam2.capture_array()
                self.video_frame = cv2.imread("C:\\Users\\Gebruiker\\OneDrive - University of Twente\\year 4\\Research Project\\Data\\Captures\\V1\\thomas_L_Middle_2_25.png")
		
				#Change to image and resize
                image = Image.fromarray(self.video_frame).resize((HALF_SCREEN_WIDTH, 300))
                image = ImageOps.mirror(image)
                # image = Image.open("test_imgs/1.png").resize((50, 50))
                image = ImageTk.PhotoImage(image)
		
				# if the panel is None, we need to initialize it
                self.panel.configure(image=image)
                self.panel.image = image

        except RuntimeError as e:
            print(f"[INFO] caught a RuntimeError: {e}")

from tkinter import ttk
from tkinter import ttk
from GUI.settings_frame import SettingsFrame
from GUI.video_frame import VideoFrame

class CaptureFrame(ttk.Frame): #inherits from frame

    def __init__(self, parent, style_arg):
        super().__init__(parent, style=style_arg) #init as frame

        self.grid_columnconfigure(0, weight=5)
        self.grid_columnconfigure(1, weight=4)
        self.grid_rowconfigure(0, weight=1)

        settings = SettingsFrame(self)
        settings.grid(column=1,row=0, sticky="news")

        video = VideoFrame(self, settings) #TODO: REPLACE
        video.grid(column=0,row=0,sticky="news")


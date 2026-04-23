import tkinter as tk
from tkinter import ttk
import tkinter as tk
from tkinter import ttk
import utils.read_write as rw

class SettingsFrame(ttk.Frame):    

    def __init__(self, parent):
        # s = ttk.Style()
        # s.configure("Settings.TFrame", background="pink")
        super().__init__(parent)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2,weight=1)

        self.currentfinger = None
        self.currentguide = None
        self.participantname = None
        self.currentPWM = None
        self.buttonsdisabled = True

        settingsthing, lf1, lf2 = self.create_settings_block()
        settingsthing.grid(column=0,row=1,columnspan=2, sticky="ews")

        name_label = ttk.Label(self, text="Batch capturing:")
        name_label.grid(column=0,row=0,sticky="news", pady=10)
        button = tk.Button(self, command=self.enable_buttons(lf1, lf2), text="off")
        button.grid(column=0,row=0, sticky="e", padx=10)

        
        sliders = self.create_sliders_block()
        sliders.grid(column=0,row=2,sticky="ews")

    def enable_buttons(self, lf1, lf2):

        for frame in lf1:
            pass

        pass

    def create_settings_block(self):
        def setnamevar(one, two, three): #FIXME: this is given three params?
            name = participant_name_var.get()
            print(name)
            self.participantname = name
        
        # s = ttk.Style()
        # s.configure("Settings2.TFrame", background="cyan")
        settingsthing = ttk.Frame(self)
        settingsthing.grid_columnconfigure(0,weight=1)
        settingsthing.grid_columnconfigure(1,weight=1)

        lf1 = self.create_labelframe(settingsthing, "Guide", ["V1", "V2", "V3", "V4", "VX"])
        lf1.grid(column=0, row=1, sticky="news")

        lf2 = self.create_labelframe(settingsthing, "Finger", ["L_Index", "L_Middle", "L_Ring", "R_Index", "R_Middle", "R_Ring"])
        lf2.grid(column=1, row=1, sticky="news")

        name_label = ttk.Label(settingsthing, text="Name:")
        name_label.grid(column=0,row=0,sticky="news", pady=10)

        participant_name_var = tk.StringVar()
        participant_name_var.trace_add("write", callback=setnamevar)
        namebox = ttk.Entry(settingsthing, textvariable=participant_name_var)
        namebox.grid(column=1,row=0,sticky="news", pady=10)

        return settingsthing, lf1, lf2

    def create_labelframe(self, parent, name, values: list):
            def selected():
                var = name_var.get()
                if var.startswith("V"):
                    self.currentguide = var
                if var.startswith("L") or var.startswith("R"):
                    self.currentfinger = var

            lf = ttk.LabelFrame(parent, text=name)

            name_var = tk.StringVar()

            grid_row = 0

            for val in values:
                # create a radio button
                radio = ttk.Radiobutton(lf, text=val, value=val, variable=name_var, command=selected, state="disabled")
                radio.grid(row=grid_row, column=0, ipadx=10, ipady=10, sticky="nw")
                # grid column
                grid_row += 1
            return lf
            

    def create_sliders_block(self):
        # s = ttk.Style()
        # s.configure("Sliders.TFrame", background="blue")
        sliders = ttk.Frame(self)

        sliders.grid_columnconfigure(0,weight=1)
        sliders.grid_rowconfigure(0, weight=1)
        sliders.grid_rowconfigure(1, weight=1)
        sliders.grid_rowconfigure(2, weight=1)

        self.slider1 = self.create_slider(parent=sliders, name="PWM")
        self.slider1.grid(column=0,row=0,sticky="nsew", pady=10)

        # slider2 = self.create_slider(parent=sliders, name="brightness", callback=None)
        # slider2.grid(column=0,row=1,sticky="nsew", pady=10)

        # slider3 = self.create_slider(parent=sliders, name="zoom", callback=None)
        # slider3.grid(column=0,row=2,sticky="nsew", pady=10)

        return sliders

    # def PWM_callback(self, val):
    #     pwm_val= int(val.split(".")[0]) * 10
    #     print(f"PWM factor changed to: {pwm_val}")
    #     rw.send_to_arduino(pwm_val)

    def create_slider(self, parent, name):
        slider_container = ttk.Frame(parent)
        slider_container.grid_columnconfigure(0,weight=1)
        slider_container.grid_columnconfigure(1,weight=10)
        slider_container.grid_columnconfigure(2,weight=1)
        slider_container.grid_rowconfigure(0,weight=1)
        slider_container.grid_rowconfigure(1,weight=1)

        def on_slider_change(self):
            value_label.configure(text=f"{name}: {'{:.0f}'.format(slider_val.get())}")
            pwm_val = slider_val.get()
            print(f"PWM factor changed to: {pwm_val}")
            rw.send_to_arduino(pwm_val)
            self.currentPWM = pwm_val

        slider_val = tk.IntVar()
        ttk.Scale(
        slider_container,
        from_=1,
        to=200,
        orient='horizontal',  
        variable = slider_val,
        command=on_slider_change,
        ).grid(column=0,row=0,columnspan=3, sticky="nsew")

        # value label
        value_label = ttk.Label(
            slider_container,
            text=f"{name}: 1",
        )
        value_label.grid(row=1,column=1)

        def add():
            new_val = slider_val.get() + 10
            slider_val.set(new_val)
            value_label.configure(text=f"{name}: {'{:.0f}'.format(new_val)}")
            pwm_val = new_val
            print(f"PWM factor changed to: {pwm_val}")
            rw.send_to_arduino(pwm_val)
            self.currentPWM = pwm_val
            
        
        def subtract():
            new_val = slider_val.get() - 10
            slider_val.set(new_val)
            value_label.configure(text=f"{name}: {'{:.0f}'.format(new_val)}")
            pwm_val = new_val
            print(f"PWM factor changed to: {pwm_val}")
            rw.send_to_arduino(pwm_val)
            self.currentPWM = pwm_val

        plus_button = ttk.Button(slider_container,text="+", command=add).grid(row=1, column=2, sticky="n")
        minus_button = ttk.Button(slider_container,text="-", command=subtract).grid(row=1, column=0, sticky="n")

        return slider_container


import tkinter as tk
from tkinter.font import Font

from Demo import *


class DemoGUI(tk.Frame):
    def __init__(self, master, mambo):
        super().__init__()
        self.master = master
        self.master.configure(background='LightSteelBlue1')
        self.square_demo = DemoSquare(mambo)
        self.keyboard_demo = DemoKeyboard(mambo)
        self.autonomy_demo = DemoFlips(mambo)
        self.init_widgets()
        self.draw_widgets()
        self.title_label = None
        self.square_demo_button = None
        self.autonomy_demo_button = None
        self.flips_demo_button = None

    def init_widgets(self):
        font_title = Font(self.master, family="Times", size=25)

        self.title_label = tk.Label(self.master, text="Parrot Drone", font=font_title, bg="LightSteelBlue1")

        buttons_font = Font(self.master, family="Times", size=15)

        self.square_demo_button = tk.Button(self.master, text="Square", font=buttons_font,
                                            width=10, height=1, bg="LightSteelBlue3", command=self.square_demo.execute)

        self.autonomy_demo_button = tk.Button(self.master, text="Autonomous", font=buttons_font,
                                              width=10, height=1, bg="LightSteelBlue3",
                                              command=self.keyboard_demo.execute)

        self.flips_demo_button = tk.Button(self.master, text="Flips", font=buttons_font,
                                           width=10, height=1, bg="LightSteelBlue3", command=self.autonomy_demo.execute)

    def draw_widgets(self):
        self.title_label.pack(pady=35)
        self.square_demo_button.pack(pady=15)
        self.autonomy_demo_button.pack(pady=15)
        self.flips_demo_button.pack(pady=15)

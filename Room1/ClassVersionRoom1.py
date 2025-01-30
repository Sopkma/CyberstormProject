"""
Door (Goal to unlock)
Keypad Lock (Goal to get vigenere key)
Wall (Write caesar cipher)
Floor (Visual)
Clock (Visual)
Lamp (Possible hint when turned off for caesar cipher)
Table (Sit chest on)
Chair (Sit on)
Trash Can (Possible hint)
Chest (Goal to unlock)
Key Lock (Goal to get key)
Key (Goal to get)
Caesar Cipher (On wall)
Vigenère Cipher (In chest)
Window (For lamp hint)
Lighting (Reveals lamp hint)
"""

"""
Whenver we want to "compile" then the following terminal command should be used:

Windows: pyinstaller --onefile --add-data "images;images" Room1.py
Linux (tested with ZorinOS (ubuntu based)): pyinstaller -D -F --windowed --add-data "images:images" --hidden-import=tkinter "Room1.py" 
Mac:

"""

import tkinter as tk
from PIL import Image, ImageTk
import os
import sys

# Function to get the path to the images folder
def resource_path(image_name):
    if getattr(sys, 'frozen', False):
        # If we're running as a bundled executable
        bundled_directory = sys._MEIPASS
    else:
        # If we're running in a normal Python script
        bundled_directory = os.path.dirname(os.path.abspath(__file__))
    
    images_folder_dir = os.path.join(bundled_directory, 'images')
    full_image_path = os.path.join(images_folder_dir, image_name)

    return full_image_path

class Room:

    def __init__(self, name:str, image_path:str):

        self.name = name
        self.image_path = image_path
        self.extra = None


class ThievesJourney(tk.Frame):
    
    INITIAL_WIDTH = 700
    INITIAL_HEIGHT = 700

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        self.canvas = tk.Canvas(root)
        self.canvas.pack(fill = tk.BOTH, expand = True)

    def setup(self):
        Room1 = Room("Room 1", f"{resource_path('Room1.png')}")
        Room2 = Room("Room 2", f"{resource_path('png-transparent-pink-cross-stroke-ink-brush-pen-red-ink-brush-ink-leave-the-material-text.png')}")
        Room1.extra = Room2

        self.current_room = Room1

    def resize_canvas(self, event):
        image_read = Image.open(f"{self.current_room.image_path}")
        
        new_width = event.width
        new_height = event.height

        canvasSize_to_imageSize = image_read.resize((new_width, new_height))
        final_image = ImageTk.PhotoImage(canvasSize_to_imageSize)

        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=final_image)

        self.canvas.image = final_image

    # Function to handle mouse click events
    def on_click(self, event):
        x, y = (event.x * 700) // root.winfo_width(), (event.y * 700) // root.winfo_height()
        print(f"Clicked at ({x}, {y})")
        # Add your conditions here to check the coordinates and perform actions
        if 24 <= x <= 102 and 140 <= y <= 400:
            print("Left Window clicked!")
        elif x==0 and y==0:
            self.current_room = self.current_room.extra
        elif 56 <= x <= 122 and 560 <= y <= 640:
            print("Trashcan clicked!")
        elif 155 <= x <= 190 and 470 <= y <= 495:
            print("Treasue Chest clicked!")
        elif 388 <= x <= 460 and 405 <= y <= 430:
            print("Lock Clicked!")
        elif 375 <= x <= 550 and 220 <= y <= 585:
            print("Door Clicked!")
        elif 125 <= x <= 374 and 225 <= y <= 295:
            print("Caesar Cipher Clicked!")
        elif 340 <= x <= 370 and 365 <= y <= 385:
            print("Light switch clicked!")
        elif 305 <= x <= 380 and 95 <= y <= 150:
            print("Light Clicked!")
        elif 413 <= x <= 502 and 115 <= y <= 185:
            print("Clock Clicked!")
        elif 115 <= x <= 373 and 480 <= y <= 595:
            print("Desk clicked!")
        elif 598 <= x <= 680 and 140 <= y <= 400:
            print("Right Window Clicked!")
        else:
            print("What are you looking for?")

    def play(self):
        self.setup()
        self.canvas.bind("<Configure>", self.resize_canvas)
        self.canvas.bind("<Button-1>", self.on_click)

root = tk.Tk()
root.title("A Thief's Journey") #Top left title of the 
root.geometry("700x700") #Initial size of the window
root.minsize(700,700) #Window must be this size or larger 
root.resizable(True, True)
game = ThievesJourney(root)
game.play()
root.mainloop()
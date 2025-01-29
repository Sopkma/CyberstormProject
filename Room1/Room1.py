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

# Create the main window
root = tk.Tk()

# Set the window size and disable resizing
window_width = 700
window_height = 700
root.geometry(f"{window_width}x{window_height}")
root.minsize(700,700) #Window must be this size or larger 
root.resizable(True, True)

# Load the PNG image
image_path = resource_path("Room1.png")
image_read = Image.open(f"{image_path}")

# Create a Canvas widget
canvas = tk.Canvas(root)
canvas.pack(fill=tk.BOTH, expand=True)

def resize_canvas(event):
   
    new_width = event.width
    new_height = event.height

    canvasSize_to_imageSize = image_read.resize((new_width, new_height))
    final_image = ImageTk.PhotoImage(canvasSize_to_imageSize)

    canvas.delete("all)")
    canvas.create_image(0, 0, anchor=tk.NW, image=final_image)

    canvas.image = final_image

# Function to handle mouse click events
def on_click(event):
    x, y = (event.x * 700) // root.winfo_width(), (event.y * 700) // root.winfo_height()
    print(f"Clicked at ({x}, {y})")
    # Add your conditions here to check the coordinates and perform actions
    if 24 <= x <= 102 and 140 <= y <= 400:
        print("Left Window clicked!")
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

canvas.bind("<Configure>", resize_canvas)

# Bind the mouse click event to the function - will call the function "on_click" when the user left clicks
canvas.bind("<Button-1>", on_click)

# Run the Tkinter event loop
root.mainloop()

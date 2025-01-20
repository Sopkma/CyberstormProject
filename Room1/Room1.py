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
from tkinter import PhotoImage
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
root.resizable(False, False)

# Load the PNG image
image_path = resource_path("Room1.png")
image = PhotoImage(file=image_path)

# Create a Canvas widget
canvas = tk.Canvas(root)
canvas.pack(fill=tk.BOTH, expand=True)


# Function to resize the image to fit the canvas
def resize_image(event):
    canvas_width = event.width
    canvas_height = event.height
    resized_image = image.subsample(
        image.width() // canvas_width, image.height() // canvas_height
    )
    canvas.create_image(0, 0, anchor=tk.NW, image=resized_image)
    canvas.image = resized_image  # Keep a reference to avoid garbage collection


# Function to handle mouse click events
def on_click(event):
    x, y = event.x, event.y
    print(f"Clicked at ({x}, {y})")
    # Add your conditions here to check the coordinates and perform actions
    if 25 <= x <= 125 and 140 <= y <= 400:
        print("Window clicked!")
    elif 65 <= x <= 145 and 560 <= y <= 640:
        print("Trashcan clicked!")
    elif 185 <= x <= 225 and 470 <= y <= 495:
        print("Treasue Chest clicked!")
    elif 465 <= x <= 540 and 405 <= y <= 430:
        print("Lock Clicked!")
    elif 450 <= x <= 650 and 220 <= y <= 585:
        print("Door Clicked!")
    elif 150 <= x <= 440 and 225 <= y <= 295:
        print("Caesar Cipher Clicked!")
    elif 410 <= x <= 430 and 365 <= y <= 385:
        print("Light switch clicked!")
    elif 365 <= x <= 455 and 95 <= y <= 150:
        print("Light Clicked!")
    elif 500 <= x <= 595 and 115 <= y <= 185:
        print("Clock Clicked!")
    elif 145 <= x <= 440 and 480 <= y <= 595:
        print("Desk clicked!")
    else:
        print("What are you looking for?")

# Bind the resize event to the function
canvas.bind("<Configure>", resize_image)

# Bind the mouse click event to the function - will call the function "on_click" when the user left clicks
canvas.bind("<Button-1>", on_click)

# Run the Tkinter event loop
root.mainloop()

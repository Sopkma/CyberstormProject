"""
Room 1:
Step 1. Decipher the caesar cipher on the wall. (Riddle with the answer being 'pearl')
Step 2. Find the key in the trashcan. (Can drag the trashcan to reveal the key.)
Step 3. Open the treasure chest using the key. (Can drag the key to the treasure chest.)
Step 4. Decipher the message in the treasure chest. with the key from the caesar cipher. (Use the key from caesar cipher to decipher the message.)
Step 5. Input the final answer in the door lock. ("A time lock with a 10 digit code.")
Step 6. Open the door. (Enter room 2)
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
    if getattr(sys, "frozen", False):
        # If we're running as a bundled executable
        bundled_directory = sys._MEIPASS
    else:
        # If we're running in a normal Python script
        bundled_directory = os.path.dirname(os.path.abspath(__file__))

    images_folder_dir = os.path.join(bundled_directory, "images")
    full_image_path = os.path.join(images_folder_dir, image_name)

    return full_image_path


class Draggable:
    def __init__(self, canvas, image_path, x, y, size):
        self.canvas = canvas
        self.image = Image.open(image_path)
        self.image = self.image.resize((size, size))
        self.tk_image = ImageTk.PhotoImage(self.image)
        self.x = x
        self.y = y
        self.dragging = False
        self.id = self.canvas.create_image(x, y, image=self.tk_image)
        self.canvas.tag_bind(self.id, "<ButtonPress-1>", self.on_press)
        self.canvas.tag_bind(self.id, "<B1-Motion>", self.on_drag)
        self.canvas.tag_bind(self.id, "<ButtonRelease-1>", self.on_release)

    def on_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.dragging = True

    def on_drag(self, event):
        dx = event.x - self.start_x
        dy = event.y - self.start_y
        self.canvas.move(self.id, dx, dy)
        self.start_x = event.x
        self.start_y = event.y

    def on_release(self, event):
        self.dragging = False


class Room:

    def __init__(
        self, name: str, image_path: str, click_actions: list, drag_items: list
    ):

        self.name = name
        self.image_path = image_path
        self.click_actions = click_actions
        self.drag_items = drag_items
        self.extra = None


class ThievesJourney(tk.Frame):

    INITIAL_WIDTH = 700
    INITIAL_HEIGHT = 700

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.canvas = tk.Canvas(root)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.rooms = []
        self.draggable_objects = []
        self.current_room = None

    def setup(self):
        Room1 = Room(
            "Room 1",
            resource_path("iRoom1.png"),
            [
                # ((x1, x2, y1, y2), action)
                ((24, 102, 140, 400), self.on_left_window_click),
                ((0, 0, 0, 0), self.change_room),
                ((105, 170, 525, 605), self.on_trashcan_click),
                ((155, 190, 470, 495), self.on_treasure_chest_click),
                ((388, 460, 405, 430), self.on_lock_click),
                ((375, 550, 220, 585), self.on_door_click),
                ((125, 374, 225, 295), self.on_caesar_cipher_click),
                ((340, 370, 365, 385), self.on_light_switch_click),
                ((305, 380, 95, 150), self.on_light_click),
                # ((413, 502, 115, 185), self.on_clock_click),
                ((115, 373, 480, 595), self.on_desk_click),
                ((598, 680, 140, 400), self.on_right_window_click),
            ],
            [
                (resource_path("key.png"), 465, 170, 10),
                (resource_path("clock.png"), 465, 170, 75),
            ],
        )

        Room2 = Room("Room 2", resource_path("Room2.png"), [], [])
        Room3 = Room("Room 3", resource_path("Room3.png"), [], [])
        Room4 = Room("Room 4", resource_path("Room4.png"), [], [])

        Room1.next_room = Room2
        Room2.next_room = Room3
        Room3.next_room = Room4

        self.rooms = [Room1, Room2, Room3, Room4]
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

        for item in self.current_room.drag_items:
            Draggable(self.canvas, *item)

    # Function to handle mouse click events
    def on_click(self, event):
        if any(item.dragging for item in self.draggable_objects):
            return
        x, y = (event.x * 700) // root.winfo_width(), (
            event.y * 700
        ) // root.winfo_height()
        for (x1, x2, y1, y2), action in self.current_room.click_actions:
            if x1 <= x <= x2 and y1 <= y <= y2:
                action()
                break
        else:
            print("What are you looking for?")

        print(f"Clicked at ({x}, {y})")

    def change_room(self):
        if self.current_room.next_room:
            self.current_room = self.current_room.next_room
            self.resize_canvas(tk.Event)

    def on_left_window_click(self):
        print("Left Window clicked!")

    def on_trashcan_click(self):
        """Opens a new window displaying the trashcan image with draggable objects."""
        if hasattr(self, "trashcan_window") and self.trashcan_window.winfo_exists():
            print("Trashcan is already open!")
            return  # Prevent opening multiple windows

        print("Opening Trashcan!")

        self.trashcan_window = tk.Toplevel(root)  # Create a new popup window
        self.trashcan_window.title("Trashcan")
        self.trashcan_window.geometry("400x400")  # Adjust as needed

        trashcan_canvas = tk.Canvas(self.trashcan_window, width=400, height=400, bg="gray")
        trashcan_canvas.pack(fill=tk.BOTH, expand=True)

        # Load and display static trashcan image (background)
        img_path = resource_path("TrashcanTV.png")
        img = Image.open(img_path).resize((400, 400))
        self.tk_trashcan_img = ImageTk.PhotoImage(img)

        trashcan_canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_trashcan_img)
        # Add sticky note in trashcan
        note_img_path = resource_path("Stickynote.png")
        note_img = Image.open(note_img_path).resize((100, 100))  # Adjust size
        self.tk_note_img = ImageTk.PhotoImage(note_img)
        self.note_id = trashcan_canvas.create_image(150, 150, anchor=tk.NW, image=self.tk_note_img) # Adjust position
        trashcan_canvas.tag_bind(self.note_id, "<Button-1>", self.on_note_click)
        # Draggable objects inside the trashcan
        self.trashcan_draggables = [
                                                                # X,Y,Size
            Draggable(trashcan_canvas, resource_path("Paper.png"), 150, 150, 100),
            Draggable(trashcan_canvas, resource_path("Paper 2.png"), 150, 250, 100),
            Draggable(trashcan_canvas, resource_path("Paper 3.png"), 225, 140, 100),
            Draggable(trashcan_canvas, resource_path("Paper 4.png"), 225, 180, 100),
            Draggable(trashcan_canvas, resource_path("Paper 5.png"), 275, 225, 100),
            Draggable(trashcan_canvas, resource_path("Paper 6.png"), 225, 275, 100),
        ]

    def on_trashcan_close(self):
        self.trashcan_window.destroy()
        self.trashcan_window = None

    def on_treasure_chest_click(self):
        print("Treasure Chest clicked!")

    def on_lock_click(self):
        print("Lock Clicked!")

    def on_door_click(self):
        print("Door Clicked!")

    def on_caesar_cipher_click(self):
        print("Caesar Cipher Clicked!")

    def on_light_switch_click(self):
        print("Light switch clicked!")

    def on_light_click(self):
        print("Light Clicked!")

    def on_clock_click(self):
        print("Clock Clicked!")

    def on_desk_click(self):
        print("Desk clicked!")

    def on_right_window_click(self):
        print("Right Window Clicked!")

    def on_note_click(self, event):
        print("Note clicked!")

    def play(self):
        self.setup()
        self.canvas.bind("<Configure>", self.resize_canvas)
        self.canvas.bind("<Button-1>", self.on_click)


root = tk.Tk()
root.title("A Thief's Journey")  # Top left title of the
root.geometry("700x700")  # Initial size of the window
root.minsize(700, 700)  # Window must be this size or larger
root.resizable(True, True)
game = ThievesJourney(root)
game.play()
root.mainloop()

from Classes import Draggable
from PIL import Image, ImageTk
from GlobalFunctions import resource_path
import tkinter as tk


def on_trashcan_click(self, root):
    """Opens a new window displaying the trashcan image with draggable objects."""
    if hasattr(self, "trashcan_window") and self.trashcan_window.winfo_exists():
        print("Trashcan is already open!")
        return  # Prevent opening multiple windows

    print("Opening Trashcan!")

    self.trashcan_window = tk.Toplevel(root)  # Create a new popup window
    self.trashcan_window.title("Trashcan")
    self.trashcan_window.geometry("400x400")  # Adjust as needed
    self.trashcan_window.resizable(False, False) #Does not allow for the window to be resizable in both x and y direction

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
    # Draggable objects inside the trashcan
    self.trashcan_draggables = [
        # X,Y,Size
        Draggable(trashcan_canvas, resource_path("Paper.png"), 150, 150, 100, 100),
        Draggable(trashcan_canvas, resource_path("Paper 2.png"), 150, 250, 100, 100),
        Draggable(trashcan_canvas, resource_path("Paper 3.png"), 225, 140, 100, 100),
        Draggable(trashcan_canvas, resource_path("Paper 4.png"), 225, 180, 100, 100),
        Draggable(trashcan_canvas, resource_path("Paper 5.png"), 275, 225, 100, 100),
        Draggable(trashcan_canvas, resource_path("Paper 6.png"), 225, 275, 100, 100),
    ]

    trashcan_canvas.bind("<Configure>", lambda event: self.resize_canvas(event, trashcan_canvas, img_path, self.trashcan_draggables))

    def on_close():
        self.trashcan_window.destroy()  # Destroy window
        self.trashcan_window = None  # Dereference the window
        
    self.trashcan_window.protocol("WM_DELETE_WINDOW", on_close)


#General functions for printing what is pressed on
def on_left_window_click(self):
    print("Left Window clicked!")

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

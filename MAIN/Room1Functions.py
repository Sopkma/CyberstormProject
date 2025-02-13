from Classes import Draggable
from PIL import Image, ImageTk
from GlobalFunctions import resource_path
import tkinter as tk
from tkinter import messagebox
import random
import string
import time


def on_trashcan_click(self, root):
    """Opens a new window displaying the trashcan image with draggable objects."""
    if hasattr(self, "trashcan_window") and self.trashcan_window.winfo_exists():
        print("Trashcan is already open!")
        return  # Prevent opening multiple windows

    print("Opening Trashcan!")

    def on_close():
        self.trashcan_window.destroy()  # Destroy window
        self.trashcan_window = None  # Dereference the window

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
    trashcan_canvas.tag_bind(self.note_id, "<Button-1>", lambda event: on_note_click(self, event))

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

    for item in self.trashcan_draggables:
        trashcan_canvas.tag_bind(item.id, "<ButtonPress-1>", item.on_press)
        trashcan_canvas.tag_bind(item.id, "<B1-Motion>", lambda event, item=item: item.on_drag(event, root))
        
    self.trashcan_window.protocol("WM_DELETE_WINDOW", on_close)


def generate_code(self, length=6):
    current_time = time.time()
    # Change code after a set time interval. (Change time at self.update_code)
    if current_time - self.last_update >= self.update_code:
        self.last_code = "".join(random.choices(string.ascii_uppercase, k=length))
        self.last_update = current_time
    return self.last_code

def check_code_update(self):
    generate_code(self)
    self.after(1000, lambda: check_code_update(self))

def show_code_entry(self, root: 'tk.Frame'):
    self.code_window = tk.Toplevel(root)
    self.code_window.title("Enter Code")
    self.code_window.geometry("200x200")

    tk.Label(self.code_window, text="Enter the code:").pack(pady=10)
    self.code_entry = tk.Entry(self.code_window)
    self.code_entry.pack(pady=10)
    
def check_code(self):
    entered_code = self.code_entry.get()
    if entered_code == self.last_code:
        messagebox.showinfo("Success", "Door unlocked!")
        self.code_window.destroy()
        self.door_locked = False
        self.current_room.tasks[3]["completed"] = True
        self.task_window.update_tasks()
    else:
        messagebox.showerror("Error", "Incorrect code. Try again.")

def on_treasure_chest_click(self):
    print("Treasure Chest clicked!")
    if self.chest_locked:
        messagebox.showwarning("Locked", "You need a key to open the treasure chest!")
    else:
        if self.current_room.game_state["vigenere_message_obtained"]:
            print("Treasure chest already opened.")

def on_lock_click(self, root):
    print("Lock Clicked!")
    show_code_entry(self, root)

def on_door_click(self):
    print("Door Clicked!")
    if self.door_locked:
        messagebox.showinfo("Not Yet", "Enter the code to unlock.")
    else:
        self.change_room()

def on_caesar_cipher_click(self):
    print("Caesar Cipher Clicked!")
    if not self.current_room.game_state["caesar_revealed"]:
        self.current_room.game_state["caesar_revealed"] = True
        self.current_room.tasks[2]["completed"] = True
        self.task_window.update_tasks()
        messagebox.showinfo("Cipher Revealed", "Caesar cipher text has been revealed!")
        self.task_window.update_tasks()

def on_key_drag_end(self, draggable: 'Draggable'):
    chest_x1, chest_x2, chest_y1, chest_y2 = 155, 190, 470, 495  # Treasure chest coordinates
    key_x, key_y = draggable.x_cord, draggable.y_cord
    print("Key realeased at:", key_x, key_y)
    if chest_x1 <= key_x <= chest_x2 and chest_y1 <= key_y <= chest_y2:
        print("Chest unlocked!")
        messagebox.showinfo("Message", "Vigenere Code: [something]!")
        self.chest_locked = False
        self.canvas.delete(draggable.id)
        self.current_room.game_state["vigenere_message_obtained"] = True
        self.current_room.tasks[1]["completed"] = True
        self.task_window.update_tasks()

def on_note_click(self, event):
    if not self.current_room.game_state["sticky_note_found"]:
        self.current_room.game_state["sticky_note_found"] = True
        self.current_room.tasks[0]["completed"] = True
        self.task_window.update_tasks()
        print("Sticky note found!")
        messagebox.showinfo("Found!", f"You found the sticky note!\nCode: {generate_code(self)}")
    elif time.time() - self.last_update >= self.update_code:
        self.current_room.tasks[0]["completed"] = False
        self.current_room.game_state["sticky_note_found"] = False
        self.task_window.update_tasks()
    else:
        remaining_time = int(self.update_code - (time.time() - self.last_update))
        print(f"Sticky note already found. You can check again in {remaining_time} seconds.")

def on_clock_drag_end(self,draggable):
    print("Clock Dragged!")

#General functions for printing what is pressed on
def on_left_window_click(self):
    print("Left Window clicked!")

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

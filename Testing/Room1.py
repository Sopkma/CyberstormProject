"""
Room 1:
Step X. Decipher the caesar cipher on the wall. (Will be used for vignere cipher.)
Step X. Find the sticky note in the trashcan. (Can click the trashcan and drag the trash away to get the code from sticky note.)
        Code changes after 15 seconds
Step X. Drag the clock away to get the key.
Step X. Open the treasure chest using the key. (Can drag the key to the treasure chest.)
Step X. Decipher the message in the treasure chest. with the key from the caesar cipher. (Use the key from caesar cipher to decipher the message.)
Step Goal - 1. Put code in the door lock.
Goal. Open the door. (Enter room 2)

######## Ignore for now ########

Whenever we want to "compile" then the following terminal command should be used:

Windows: pyinstaller --onefile --add-data "images;images" Room1.py
Linux (tested with ZorinOS (ubuntu based)): pyinstaller -D -F --windowed --add-data "images:images" --hidden-import=tkinter "Room1.py" 
Mac: TBD

######## Ignore for now ########
"""

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from Classes import Draggable, Room, TaskWindow
from GlobalFunctions import resource_path
import random
import string
import time

class ThievesJourney(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        self.canvas = tk.Canvas(root)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.rooms = []
        self.current_room = None
        self.windowWidthTracker = 700
        self.windowHeightTracker = 700

        self.game_state = {
            "sticky_note_found": False,  # Points #1
            "vigenere_message_obtained": False,  # Points #1
            "caesar_revealed": False,  # Points #2
            "door_unlocked": False,  # Points #3
        }

        # Task list
        self.tasks = [{"desc": "Find sticky note","completed": False,},
                      {"desc": "Found Vigenère cipher text","completed": False,},
                      {"desc": "Reveal Caesar cipher text","completed": False,},
                      {"desc": "Door unlocked","completed": False,}]
        self.task_window = TaskWindow(parent, self.tasks)
        self.draggable_objects = []
        self.drop_targets = []
        self.interactions = []
        self.dragging = False
        self.chest_locked = True
        self.door_locked = True
        self.last_code = None
        self.last_update = 0
        self.update_code = 15
        self.seed = 8264006
        random.seed(self.seed)

        self.check_code_update()

    def setup(self):
        Room1 = Room(
            "Room 1",
            resource_path("Room1.png"),
            [
                ((24, 102, 140, 400), self.on_left_window_click),
                ((0, 0, 0, 0), self.change_room),
                ((105, 170, 525, 605), self.on_trashcan_click),
                ((155, 190, 470, 495), self.on_treasure_chest_click),
                ((388, 460, 405, 430), self.on_lock_click),
                ((375, 550, 220, 585), self.on_door_click),
                ((125, 374, 225, 295), self.on_caesar_cipher_click),
                ((340, 370, 365, 385), self.on_light_switch_click),
                ((305, 380, 95, 150), self.on_light_click),
                ((115, 373, 480, 595), self.on_desk_click),
                ((598, 680, 140, 400), self.on_right_window_click),
            ],
            # Create instances of a draggable that are tied only to room 1 (key, and the clock)
            [
                Draggable(self.canvas, resource_path("key.png"), 465, 170, 10, 10, self.on_key_drag_end),
                Draggable(self.canvas, resource_path("clock.png"), 465, 170, 75, 75, self.on_clock_drag_end),
            ]
        )

        # For future use
        Room0 = Room("Room 0", resource_path("Room0.png"), [], [])
        Room2 = Room("Room 2", resource_path("Room2.jpg"), [], [])
        Room3 = Room("Room 3", resource_path("Room3.png"), [], [])
        Room4 = Room("Room 4", resource_path("Room4.png"), [], [])

        Room0.next_room = Room1
        Room1.next_room = Room2
        Room2.next_room = Room3
        Room3.next_room = Room4

        self.rooms = [Room0, Room1, Room2, Room3, Room4]
        self.current_room = Room1

    def generate_code(self, length=6):
        current_time = time.time()
        # Change code after a set time interval. (Change time at self.update_code)
        if current_time - self.last_update >= self.update_code:
            self.last_code = "".join(random.choices(string.ascii_uppercase, k=length))
            self.last_update = current_time
        return self.last_code
    def check_code_update(self):
        self.generate_code()
        self.after(1000, self.check_code_update)
    def resize_canvas(self, event, canvas_var: 'tk.Canvas', path_to_image=None, draggables=None):
        print(f"Canvas Type: {type(canvas_var)}")

        if path_to_image is None:
            path_to_image = self.current_room.image_path

        if draggables is None:
            draggables = self.current_room.drag_items
        
        image_read = Image.open(path_to_image)

        new_width = canvas_var.winfo_width()
        new_height = canvas_var.winfo_height()

        if new_width == 1 or new_height == 1:
        # This happens sometimes when the window is resizing; ignore invalid values.
            return
        
        canvasSize_to_imageSize = image_read.resize((new_width, new_height))
        final_image = ImageTk.PhotoImage(canvasSize_to_imageSize)

        canvas_var.delete("all")
        canvas_var.create_image(0, 0, anchor=tk.NW, image=final_image)

        canvas_var.image = final_image

        width_ratio = new_width / self.windowWidthTracker
        height_ratio = new_height / self.windowHeightTracker

        for item in draggables:
            item.x_size, item.x_cord = item.x_size * width_ratio, item.x_cord * width_ratio
            item.y_size, item.y_cord = item.y_size * height_ratio, item.y_cord * height_ratio

            item.image = item.image.resize((int(item.x_size), int(item.y_size)))
            item.tk_image = ImageTk.PhotoImage(item.image)

            item.id = canvas_var.create_image(item.x_cord, item.y_cord, image=item.tk_image)
            canvas_var.tag_bind(item.id, "<ButtonPress-1>", item.on_press)
            canvas_var.tag_bind(item.id, "<B1-Motion>", lambda event, item=item: item.on_drag(event, root))
            canvas_var.tag_bind(item.id, "<ButtonRelease-1>", item.on_release)

        self.windowWidthTracker = new_width
        self.windowHeightTracker = new_height
    def show_code_entry(self):
        self.code_window = tk.Toplevel(root)
        self.code_window.title("Enter Code")
        self.code_window.geometry("200x200")

        tk.Label(self.code_window, text="Enter the code:").pack(pady=10)
        self.code_entry = tk.Entry(self.code_window)
        self.code_entry.pack(pady=10)
        tk.Button(self.code_window, text="Submit", command=self.check_code).pack(pady=10)
    def check_code(self):
        entered_code = self.code_entry.get()
        if entered_code == self.last_code:
            messagebox.showinfo("Success", "Door unlocked!")
            self.code_window.destroy()
            self.door_locked = False
            self.tasks[3]["completed"] = True
            self.task_window.update_tasks()
        else:
            messagebox.showerror("Error", "Incorrect code. Try again.")
    def on_click(self, event):
        x = (event.x * 700) // root.winfo_width()
        y = (event.y * 700) // root.winfo_height()
        for (x1, x2, y1, y2), action in self.current_room.click_actions:
            if x1 <= x <= x2 and y1 <= y <= y2:
                action()
                break
        else:
            print("What are you looking for?")

        print(f"Clicked at ({x}, {y})")
    def on_release(self, event):
        x = (event.x * 700) // root.winfo_width()
        y = (event.y * 700) // root.winfo_height()
        print(f"Released at ({x}, {y})")

    def change_room(self):
        if self.current_room.next_room:
            self.current_room = self.current_room.next_room
            self.resize_canvas(None, self.canvas)
    def on_left_window_click(self):
        print("Left Window clicked!")

    def on_trashcan_click(self):
        if hasattr(self, "trashcan_window") and self.trashcan_window is not None and self.trashcan_window.winfo_exists():
            print("Trashcan is already open!")
            return

        print("Opening Trashcan!")
        self.trashcan_window = tk.Toplevel(root)
        self.trashcan_window.title("Trashcan")
        self.trashcan_window.geometry("400x400")

        trashcan_canvas = tk.Canvas(self.trashcan_window, width=400, height=400, bg="gray")
        trashcan_canvas.pack(fill=tk.BOTH, expand=True)

        img_path = resource_path("TrashcanTV.png")
        img = Image.open(img_path).resize((400, 400))
        self.tk_trashcan_img = ImageTk.PhotoImage(img)

        trashcan_canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_trashcan_img)

        note_img_path = resource_path("Stickynote.png")
        note_img = Image.open(note_img_path).resize((100, 100))
        self.tk_note_img = ImageTk.PhotoImage(note_img)
        self.note_id = trashcan_canvas.create_image(150, 150, anchor=tk.NW, image=self.tk_note_img)
        trashcan_canvas.tag_bind(self.note_id, "<Button-1>", self.on_note_click)

        self.trashcan_draggables = [
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


    def on_trashcan_close(self):
        self.trashcan_window.destroy()
        self.trashcan_window = None

    def on_treasure_chest_click(self):
        print("Treasure Chest clicked!")
        if self.chest_locked:
            messagebox.showwarning("Locked", "You need a key to open the treasure chest!")
        else:
            if self.game_state["vigenere_message_obtained"]:
                print("Treasure chest already opened.")
                

    def on_lock_click(self):
        print("Lock Clicked!")
        self.show_code_entry()

    def on_door_click(self):
        print("Door Clicked!")
        if self.door_locked:
            messagebox.showinfo("Not Yet", "Enter the code to unlock.")
        else:
            self.change_room()

    def on_caesar_cipher_click(self):
        print("Caesar Cipher Clicked!")
        if not self.game_state["caesar_revealed"]:
            self.game_state["caesar_revealed"] = True
            self.tasks[2]["completed"] = True
            self.task_window.update_tasks()
            messagebox.showinfo("Cipher Revealed", "Caesar cipher text has been revealed!")
            self.task_window.update_tasks()

    def on_light_switch_click(self):
        print("Light switch clicked!")

    def on_light_click(self):
        print("Light Clicked!")

    def on_clock_drag_end(self,draggable):
        print("Clock Dragged!")

    def on_key_drag_end(self, draggable):
        chest_x1, chest_x2, chest_y1, chest_y2 = 155, 190, 470, 495  # Treasure chest coordinates
        key_x, key_y = draggable.x_cord, draggable.y_cord
        print("Key realeased at:", key_x, key_y)
        if chest_x1 <= key_x <= chest_x2 and chest_y1 <= key_y <= chest_y2:
            print("Chest unlocked!")
            messagebox.showinfo("Message", "Vigenere Code: [something]!")
            self.chest_locked = False
            self.canvas.delete(draggable.id)
            self.game_state["vigenere_message_obtained"] = True
            self.tasks[1]["completed"] = True
            self.task_window.update_tasks()

    def on_desk_click(self):
        print("Desk clicked!")

    def on_right_window_click(self):
        print("Right Window Clicked!")

    def on_note_click(self, event):
        if not self.game_state["sticky_note_found"]:
            self.game_state["sticky_note_found"] = True
            self.tasks[0]["completed"] = True
            self.task_window.update_tasks()
            print("Sticky note found!")
            messagebox.showinfo("Found!", f"You found the sticky note!\nCode: {self.generate_code()}")
        elif time.time() - self.last_update >= self.update_code:
            self.tasks[0]["completed"] = False
            self.game_state["sticky_note_found"] = False
            self.task_window.update_tasks()
        else:
            remaining_time = int(self.update_code - (time.time() - self.last_update))
            print(f"Sticky note already found. You can check again in {remaining_time} seconds.")

    def play(self):
        self.setup()
        self.canvas.bind("<Configure>", lambda event: self.resize_canvas(event, self.canvas))
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

root = tk.Tk()
root.title("A Thief's Journey")
root.geometry("700x700")
root.minsize(700, 700)
root.resizable(True, True)
game = ThievesJourney(root)
game.play()
root.mainloop()
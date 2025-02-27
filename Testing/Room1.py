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
from Classes import Draggable, Interactive, Room, TaskWindow
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
            "caesar_decoded": False,
            "vigenere_decoded": False,
            "sticky_note_found": False,
            "door_unlocked": False,
            "room1_Completed": False,
            "timo_found": False,
            "anky_found": False,
            "Steg_decoded": False,
            "bookshelf_moved": False,
            "Door2_unlocked": False
        }

        # Task list
        self.tasks = [  
                        {"desc": "Decode Caesar cipher","completed": False, "points": 987},
                        {"desc": "Decode Vigenère cipher","completed": False, "points": 2584},
                        {"desc": "Find sticky note (60 seconds)","completed": False,"points": 610},
                        {"desc": "Door unlocked","completed": False,"points": 6765},
                        {"desc": "Find Timo","completed": False,"points": 55},
                        {"desc": "Find Anky","completed": False,"points": 55},
                        {"desc": "Decode Steg","completed": False,"points": 4181},
                        {"desc": "Move bookshelf","completed": False,"points": 610},
                        {"desc": "Door 2 unlocked","completed": False,"points": 6765},
                        ] 
        self.task_window = None
        self.chest_locked = True
        self.door_locked = True
        self.door2_locked = True
        self.bookLocked = False
        self.last_code = None
        self.last_update = 0
        self.update_code = 300
        self.seed = 8264006
        random.seed(self.seed)
        self.score = 10946
        self.check_code_update()

    def setup(self):
        Room0 = Room(
            "Room 0",
            resource_path("Room0.png"),
            [
                ((332, 362, 563, 630),  self.change_room)
            ], 
            [], 
            [
                Interactive(self.canvas, resource_path("task.png"), 630, 30, 50, 50, self.on_task_click),
            ]
        )
        Room1 = Room(
            "Room 1",
            resource_path("Room1.png"),
            [
                ((24, 102, 140, 400),  self.on_left_window_click),
                ((95, 155, 540, 610),  self.on_trashcan_click),
                ((155, 190, 470, 495), self.on_treasure_chest_click),
                ((388, 460, 405, 430), self.on_lock_click),
                ((375, 550, 220, 585), self.on_door_click),
                ((125, 350, 230, 295), self.on_caesar_cipher_click),
                ((340, 370, 365, 385), self.on_light_switch_click),
                ((305, 380, 95, 150),  self.on_light_click),
                ((115, 373, 480, 595), self.on_desk_click),
                ((598, 680, 140, 400), self.on_right_window_click),
            ],
            # Create instances of a draggable that are tied only to room 1 (key, and the clock)
            [
                Draggable(self.canvas, resource_path("key.png"), 465, 170, 10, 10, self.on_key_drag_end),
                Draggable(self.canvas, resource_path("clock.png"), 465, 170, 75, 75, self.on_clock_drag_end),
            ],
            [
                Interactive(self.canvas, resource_path("task.png"), 630, 50, 50, 50, self.on_task_click),
            ]
        )

        # For future use
        
        Room2 = Room(
            "Room 2",
            resource_path("Room2.png"),
            [
            ((70, 87, 290, 323), self.on_Timo_click),
            ((150, 168, 229, 264), self.on_Anky_click),
            ((5, 190, 10, 530), self.on_bookshelf_click),
            ((45, 130, 100, 500), self.on_door2_clicked),
            ],
            [
            ],
            [
            Interactive(self.canvas, resource_path("clock2.png"), 300, 96, 75, 75, self.passing_function),
            Interactive(self.canvas, resource_path("Bookshelf.png"), 100, 280, 200, 500, self.passing_function),
            Interactive(self.canvas, resource_path("greedbook.png"), 135, 174, 10, 47, self.animate_bookshelf),
            Interactive(self.canvas, resource_path("frame.png"), 500, 165, 100, 100, self.passing_function),
            Interactive(self.canvas, resource_path("picture.png"), 500, 165, 75, 80, self.picture_interact),
            Interactive(self.canvas, resource_path("table.png"), 500, 450, 200, 200, self.passing_function),
            Interactive(self.canvas, resource_path("alarmclock.png"), 550, 355, 50, 25, self.passing_function),
            Interactive(self.canvas, resource_path("task.png"), 630, 30, 50, 50, self.on_task_click),

            ]
        )
        self.bookshelf_obj = Room2.interact_items[1]
        self.book_obj = Room2.interact_items[2]
        print(f"Bookshelf ID: {self.bookshelf_obj}")
        self.bookshelf_coords = self.canvas.coords(self.bookshelf_obj.id)
        self.book_cords = self.canvas.coords(self.book_obj.id)
        print(f"Bookshelf starting coords: {self.bookshelf_coords}")

        Room3 = Room(
            "Room 3", 
            resource_path("Room3.png"), 
            [
                ((324, 364, 444, 480), self.on_final_note_click)
            ], 
            [
            ], 
            [
                Interactive(self.canvas, resource_path("task.png"), 630, 30, 50, 50, self.on_task_click),
            ]
        )
        Room4 = Room("Room 4", resource_path("Room4.png"), [], [], [])

        Room0.next_room = Room1
        Room1.next_room = Room2
        Room2.next_room = Room3
        Room3.next_room = Room4

        self.rooms = [Room0, Room1, Room2, Room3, Room4]
        self.current_room = Room2

        # Draw the current room background and any draggables.
        self.resize_canvas(None, self.canvas)
        
    def on_task_click(self, event):
        if self.task_window is None or not self.task_window.winfo_exists():
            self.task_window = TaskWindow(self, self.tasks, self.score)
        else:
            self.task_window.focus()

    def update_score(self):
        self.score = sum(task["points"] for task in self.tasks if task["completed"])
        if self.task_window:
            self.task_window.update_tasks()
    def generate_code(self, length=20):
        current_time = time.time()
        # Change code after a set time interval. (Change time at self.update_code)
        if current_time - self.last_update >= self.update_code:
            self.last_code = "".join(random.choices(string.hexdigits, k=length))
            self.last_update = current_time
        return self.last_code
    
    def check_code_update(self):
        self.generate_code()
        remaining_time = int(self.update_code - (time.time() - self.last_update))
        if self.game_state["sticky_note_found"] and remaining_time <= 0:
            self.game_state["sticky_note_found"] = False
            self.tasks[2]["completed"] = False
            self.update_score()
        self.after(1000, self.check_code_update)
    def resize_canvas(self, event, canvas_var: 'tk.Canvas', path_to_image=None, draggables=None, interactive_items=None):

        if path_to_image is None:
            path_to_image = self.current_room.image_path

        if draggables is None:
            draggables = self.current_room.drag_items

        if interactive_items is None:
            interactive_items = self.current_room.interact_items
        
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
        for item in interactive_items:
            item.x_size, item.x_cord = item.x_size * width_ratio, item.x_cord * width_ratio
            item.y_size, item.y_cord = item.y_size * height_ratio, item.y_cord * height_ratio

            item.image = item.image.resize((int(item.x_size), int(item.y_size)))
            item.tk_image = ImageTk.PhotoImage(item.image)

            item.id = canvas_var.create_image(item.x_cord, item.y_cord, image=item.tk_image)
            
            canvas_var.tag_bind(item.id, "<ButtonPress-1>", item.interact)
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
        #print(f"Entered code: {self.code_entry.get()}")
        #print(f"Last code: {self.last_code}")
        converter = str(int(self.last_code, 16))
        #print(f"Code converted to decimal: {int(self.last_code, 16)}")
        #get every 3rd character
        third = converter[2::3]
        #print(f"every 3rd character: {third}")
        if entered_code == third:
            messagebox.showinfo("Success", "Door unlocked!")
            self.code_window.destroy()
            self.door_locked = False
            self.tasks[3]["completed"] = True
            self.update_score()
        else:
            messagebox.showerror("Error", "Incorrect code. Try again.")
            print(third)
    def on_click(self, event):
        x = (event.x * 700) // root.winfo_width()
        y = (event.y * 700) // root.winfo_height()

        
        for (x1, x2, y1, y2), action in self.current_room.click_actions:
            if x1 <= x <= x2 and y1 <= y <= y2:
                action()
                break
        else:
            ##print("What are you looking for?")
            pass

        print(f"Clicked at ({x}, {y})")
    def on_release(self, event):
        x = (event.x * 700) // root.winfo_width()
        y = (event.y * 700) // root.winfo_height()
        ##print(f"Released at ({x}, {y})")

    def change_room(self):
        if self.current_room.next_room:
            self.current_room = self.current_room.next_room
            self.resize_canvas(None, self.canvas)

    def on_left_window_click(self):
        ##print("Left Window clicked!")
        pass

    def on_trashcan_click(self):
        if hasattr(self, "trashcan_window") and self.trashcan_window is not None and self.trashcan_window.winfo_exists():
            self.task_window.focus()
            return

        #print("Opening Trashcan!")
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

    def on_treasure_chest_click(self):
        #print("Treasure Chest clicked!")
        if self.chest_locked:
            messagebox.showwarning("Locked", "You need a key to open the treasure chest!")
        else:
            messagebox.showinfo("Message", "Vwim Mcdrfl Fayi Smdyp Wrhlcv Nblxi Imkym Gexjy Iincf Xfjku Ommynzvl Vlzzppd Gjiv Vsymi Fayi Smdyp Dfrupfn Smdyp Mjwbp Dclc Jcfpiu Uyeap Gexjy Tbbpccf Izfp Wrhlcv Hptvgcci Itarl Uyeap Ctbp Gexjy Jcfpiu Eccnb Mjwbp Fmdyi Lpkvi Mgdu Pqtus Ayusjzy Lgci Dfrlmgv Itarl Eccnb Ctbp")
            self.code_window = tk.Toplevel(root)
            self.code_window.title("Flag")
            self.code_window.geometry("200x200")

            tk.Label(self.code_window, text="E for ?").pack(pady=10)
            self.code_entry = tk.Entry(self.code_window)
            self.code_entry.pack(pady=10)
            tk.Button(self.code_window, text="Submit", command=self.check_vigenere_code).pack(pady=10)
            self.update_score()

    def check_vigenere_code(self):
        if self.game_state["vigenere_decoded"]:
            return
        entered_code = self.code_entry.get().strip().lower()
        if entered_code == "echo":
            messagebox.showinfo("Success", "Vigenere cipher revealed!")
            self.code_window.destroy()
            self.game_state["vigenere_decoded"] = True
            self.tasks[1]["completed"] = True
            self.update_score()
        else:
            messagebox.showerror("Error", "Incorrect answer. Try again.")        

    def on_lock_click(self):
        #print("Lock Clicked!")
        self.show_code_entry()

    def on_door_click(self):
        #print("Door Clicked!")
        if self.door_locked:
            messagebox.showinfo("Not Yet", "Enter the code to unlock.")
        else:
            self.change_room()

    def on_caesar_cipher_click(self):
        #print("Caesar Cipher Clicked!")
        if not self.game_state["caesar_decoded"]:
            self.code_window = tk.Toplevel(root)
            self.code_window.title("Flag")
            self.code_window.geometry("200x200")

            tk.Label(self.code_window, text="Enter the answer: ").pack(pady=10)
            self.code_entry = tk.Entry(self.code_window)
            self.code_entry.pack(pady=10)
            tk.Button(self.code_window, text="Submit", command=self.check_caesar_code).pack(pady=10)
            self.update_score()

    def check_caesar_code(self):
        entered_code = self.code_entry.get().strip().lower()
        if self.game_state["caesar_decoded"]:
            return
        if entered_code == "ruby":
            messagebox.showinfo("Success", "Caesar cipher revealed!")
            self.code_window.destroy()
            self.game_state["caesar_decoded"] = True
            self.tasks[0]["completed"] = True
            self.update_score()
        else:
            messagebox.showerror("Error", "Incorrect answer. Try again.")

    def on_light_switch_click(self):
        #print("Light switch clicked!")
        pass
    def on_light_click(self):
        #print("Light Clicked!")
        pass

    def on_clock_drag_end(self,draggable):
        #print("Clock Dragged!")
        pass

    def on_key_drag_end(self, draggable):
        chest_x1, chest_x2, chest_y1, chest_y2 = 155, 190, 470, 495  # Treasure chest coordinates
        key_x, key_y = draggable.x_cord, draggable.y_cord
        #print("Key realeased at:", key_x, key_y)
        if chest_x1 <= key_x <= chest_x2 and chest_y1 <= key_y <= chest_y2:
            messagebox.showinfo("Message", "Vwim Mcdrfl Fayi Smdyp Wrhlcv Nblxi Imkym Gexjy Iincf Xfjku Ommynzvl Vlzzppd Gjiv Vsymi Fayi Smdyp Dfrupfn Smdyp Mjwbp Dclc Jcfpiu Uyeap Gexjy Tbbpccf Izfp Wrhlcv Hptvgcci Itarl Uyeap Ctbp Gexjy Jcfpiu Eccnb Mjwbp Fmdyi Lpkvi Mgdu Pqtus Ayusjzy Lgci Dfrlmgv Itarl Eccnb Ctbp")
            self.chest_locked = False
            self.canvas.delete(draggable.id)
            self.current_room.drag_items.remove(draggable)
            self.code_window = tk.Toplevel(root)
            self.code_window.title("Flag")
            self.code_window.geometry("200x200")

            tk.Label(self.code_window, text="E for ?").pack(pady=10)
            self.code_entry = tk.Entry(self.code_window)
            self.code_entry.pack(pady=10)
            tk.Button(self.code_window, text="Submit", command=self.check_vigenere_code).pack(pady=10)
            self.update_score()


    def on_desk_click(self):
        #print("Desk clicked!")
        pass

    def on_right_window_click(self):
        #print("Right Window Clicked!")
        pass

    def on_note_click(self, event):
        remaining_time = int(self.update_code - (time.time() - self.last_update))
        if self.game_state["sticky_note_found"]:
            #print("Sticky note already found!")
            #print("Code:", self.generate_code())
            messagebox.showinfo("Already found.", f"\nCode: {self.generate_code()} \n Time left: {remaining_time} seconds")
        else:
            self.game_state["sticky_note_found"] = True
            self.tasks[2]["completed"] = True
            self.update_score()
            #print("Sticky note found!")
            
            messagebox.showinfo("Found!", f"You found the sticky note!\nCode: {self.generate_code()} \n ({remaining_time} seconds before code expires)")
            #print(self.generate_code())

    def on_bookshelf_click(self):
        print("Bookshelf clicked!")
        pass
    book_moved = False
    def animate_bookshelf(self, event):
        if not self.bookLocked:
            if not self.book_moved:
                # Move bookshelf to the right
                for _ in range(25):
                    self.canvas.move(self.bookshelf_obj.id, 5, 0)
                    self.canvas.move(self.book_obj.id, 5, 0)
                    self.canvas.update()
                    self.canvas.after(10)
                self.bookshelf_coords = self.canvas.coords(self.bookshelf_obj.id)
                self.book_cords = self.canvas.coords(self.book_obj.id)
                self.book_moved = True
                self.current_room.click_actions = [
                action for action in self.current_room.click_actions
                if action[1] != self.on_bookshelf_click]
                self.game_state["bookshelf_moved"] = True
                self.tasks[7]["completed"] = True
                self.update_score()
            else:
                # Move bookshelf back to its original position
                for _ in range(25):
                    self.canvas.move(self.bookshelf_obj.id, -5, 0)
                    self.canvas.move(self.book_obj.id, -5, 0)
                    self.canvas.update()
                    self.canvas.after(10)
                self.bookshelf_coords = self.canvas.coords(self.bookshelf_obj.id)
                self.book_cords = self.canvas.coords(self.book_obj.id)
                self.book_moved = False
        else:
            self.remaining_time = int(self.cooldown_end_time - time.time())
            messagebox.showinfo("Cooldown", f"Please wait {self.remaining_time} seconds before trying again.")

    def on_door2_clicked(self):
        if not self.bookLocked:
            #print("Door 2 clicked!")
            self.code_window = tk.Toplevel(root)
            self.code_window.title("Locked")
            self.code_window.geometry("200x200")
            tk.Label(self.code_window, text="Code: ").pack(pady=10)
            self.code_entry = tk.Entry(self.code_window)
            self.code_entry.pack(pady=10)
            tk.Button(self.code_window, text="Submit", command=self.door2_check).pack(pady=10)
            self.update_score()

    def door2_check(self):
        entered_code = self.code_entry.get().strip().lower()
        if not self.bookLocked:
            if entered_code == "21011":
                self.door2_locked = False
                self.game_state["door2_unlocked"] = True
                self.tasks[8]["completed"] = True
                self.update_score()
                self.code_window.destroy()
                self.change_room()

            else:
                self.code_window.destroy()
                self.animate_bookshelf(None)
                self.bookLocked = True
                cooldown = 60 * (2 ** self.tasks[7].get("attempts", 0))
                self.tasks[7]["attempts"] = self.tasks[7].get("attempts", 0) + 1
                self.cooldown_end_time = time.time() + cooldown
                self.after(cooldown * 1000, self.unlock_book)

    def unlock_book(self):
        self.bookLocked = False

    
    def on_Timo_click(self):
        #Enter the name of the person
        self.code_window = tk.Toplevel(root)
        self.code_window.title("Easteregg")
        self.code_window.geometry("200x200")
        tk.Label(self.code_window, text="Enter the answer: ").pack(pady=10)
        self.code_entry = tk.Entry(self.code_window)
        self.code_entry.pack(pady=10)
        tk.Button(self.code_window, text="Submit", command=self.check_timo).pack(pady=10)
        self.update_score()

    def check_timo(self):
        if self.game_state["timo_found"]:
            return
        entered_code = self.code_entry.get().strip().lower()
        if entered_code == "timo":
            messagebox.showinfo("Success", "Timo found!")
            self.code_window.destroy()
            self.game_state["timo_found"] = True
            self.tasks[4]["completed"] = True
            self.update_score()
        else:
            messagebox.showerror("Error", "Incorrect answer. Try again.")

    def on_Anky_click(self):
        #Enter the name of the person
        self.code_window = tk.Toplevel(root)
        self.code_window.title("Easteregg")
        self.code_window.geometry("200x200")
        tk.Label(self.code_window, text="Enter the answer: ").pack(pady=10)
        self.code_entry = tk.Entry(self.code_window)
        self.code_entry.pack(pady=10)
        tk.Button(self.code_window, text="Submit", command=self.check_anky).pack(pady=10)
        self.update_score()

    def check_anky(self):
        entered_code = self.code_entry.get().strip().lower()
        if self.game_state["anky_found"]:
            return
        if entered_code == "anky":
            messagebox.showinfo("Success", "Anky found!")
            self.code_window.destroy()
            self.game_state["anky_found"] = True
            self.tasks[5]["completed"] = True
            self.update_score()
        else:
            messagebox.showerror("Error", "Incorrect answer. Try again.")

    def on_final_note_click(self):
        if hasattr(self, "finalNote_window") and self.finalNote_window is not None and self.finalNote_window.winfo_exists():
            self.task_window.focus()
            return

        #print("Opening Trashcan!")
        self.finalNote_window = tk.Toplevel(root)
        self.finalNote_window.title("Note")
        self.finalNote_window.geometry("400x400")
        self.finalNote_window.resizable(False, False)

        finalNote_canvas = tk.Canvas(self.finalNote_window, width=400, height=400, bg="gray")
        finalNote_canvas.pack(fill=tk.BOTH, expand=True)

        img_path = resource_path("Background.png")
        img = Image.open(img_path).resize((400, 400))
        self.tk_finalNote_img = ImageTk.PhotoImage(img)

        finalNote_canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_finalNote_img)
        finalNote_canvas.create_text(30,140,anchor=tk.NW,fill="black",font="Times 15", text="dhvq dhnrevf rfg qhb gnohyngn fhcen")
        finalNote_canvas.create_text(30,160,anchor=tk.NW,fill="black",font="Times 15", text="hov nyvv qvfprer purzvpnyf")
        finalNote_canvas.create_text(30,180,anchor=tk.NW,fill="black",font="Times 15", text="yhpvqn pnrehyrn fho vatragv cerffvbar yhprg")
        finalNote_canvas.create_text(30,200,anchor=tk.NW,fill="black",font="Times 15", text="rg va cnevrgr vairavev cbgrfg")
        finalNote_canvas.create_text(30,220,anchor=tk.NW,fill="black",font="Times 15", text="gbyyr vzntvarz rg qn phfgbqv plcuevf")

    def picture_interact(self, event):
        self.code_window = tk.Toplevel(root)
        self.code_window.title("Flag")
        self.code_window.geometry("200x200")
        tk.Label(self.code_window, text="Enter the answer: ").pack(pady=10)
        self.code_entry = tk.Entry(self.code_window)
        self.code_entry.pack(pady=10)
        tk.Button(self.code_window, text="Submit", command=self.check_steg).pack(pady=10)
        self.update_score()
    def check_steg(self):
        entered_code = self.code_entry.get().strip().lower()
        if self.game_state["Steg_decoded"]:
            return
        if entered_code == "yt":
            self.code_window.destroy()
            self.game_state["Steg_decoded"] = True
            self.tasks[6]["completed"] = True
            self.update_score()
        else:
            messagebox.showerror("Error", "Incorrect answer. Try again.")
    def passing_function(self, event):
        pass


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
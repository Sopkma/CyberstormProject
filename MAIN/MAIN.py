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
from Classes import Draggable, Room, TaskWindow
from GlobalFunctions import resource_path
import random

class ThievesJourney(tk.Frame):

    import Room1Functions
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        self.parent = parent

        self.canvas = tk.Canvas(root)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.rooms = []
        self.current_room = None

        self.windowWidthTracker = 700
        self.windowHeightTracker = 700

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

    def resize_canvas(self, event, canvas_var: 'tk.Canvas', path_to_image=None, draggables=None):

        isOtherWindow = True

        if path_to_image == None:
            path_to_image = self.current_room.image_path
            isOtherWindow = False

        if draggables == None:
            draggables = self.current_room.drag_items
        
        image_read = Image.open(path_to_image)

        #New dimensions of the canvas
        new_width = event.width
        new_height = event.height

        #Changes the size of the image for the room to that of the window
        canvasSize_to_imageSize = image_read.resize((new_width, new_height))
        final_image = ImageTk.PhotoImage(canvasSize_to_imageSize)

        #Removes everything from the canvas
        canvas_var.delete("all")
        #Adds the room image to the canvas
        canvas_var.create_image(0, 0, anchor=tk.NW, image=final_image)

        canvas_var.image = final_image #Keeps track of the image so that is it not garbage collected

        #Iterate through all of the draggables within the current room - when the window is resized, the draggables will stay in their position and not move. They will also be resized accordingly.
        for item in draggables: 
            #If it is the main window/canvas, then resize, otherwise, do not use the width ratio as other windows will be static in size

            if not(isOtherWindow):
                #Ratios for increasing or decreasing the size and location of the draggables

                width_ratio = (new_width / self.windowWidthTracker)
                height_ratio = (new_height / self.windowHeightTracker)
                
                item.x_size, item.x_cord = item.x_size * width_ratio, item.x_cord * width_ratio   #For x size (both moving and resizing)
                item.y_size, item.y_cord = item.y_size * height_ratio, item.y_cord * height_ratio #For y size (both moving and resizing)

            # Resize the draggable item image and update the draggable's internal variables
            item.image = item.image.resize((int(item.x_size), int(item.y_size)))
            item.tk_image = ImageTk.PhotoImage(item.image)

            # Re-create draggable item with the updated position and size
            item.id = canvas_var.create_image(item.x_cord, item.y_cord, image=item.tk_image)
            #Allows for dragging to take place
            canvas_var.tag_bind(item.id, "<ButtonPress-1>", item.on_press)
            canvas_var.tag_bind(item.id, "<B1-Motion>", lambda event, item=item: item.on_drag(event, root))

        #Update the trackers for the next time that things are moved
        self.windowWidthTracker = new_width
        self.windowHeightTracker = new_height

    # Function to handle mouse click events. This essentially keeps everything within the 700x700 plane (the original window size that pops up). If the window is resized then the x and y are correctly sized to the 700x700 plane.
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

    def setup(self):
        
        Room0 = Room
        (
            "Room 0",
            resource_path("Room0.png"),
            [
                ((24, 102, 140, 400), self.Room1Functions.on_left_window_click),
            ],
            [

            ],

            {

            },

            [

            ]


        )

        Room1 = Room
        (
            "Room 1",
            resource_path("Room1.png"),
            [
                ((24, 102, 140, 400), self.Room1Functions.on_left_window_click),
                ((105, 170, 525, 605), lambda: self.Room1Functions.on_trashcan_click(self, root)),
                ((155, 190, 470, 495), lambda: self.Room1Functions.on_treasure_chest_click(self)),
                ((388, 460, 405, 430), lambda: self.Room1Functions.on_lock_click(self, root)),
                ((375, 550, 220, 585), lambda: self.Room1Functions.on_door_click(self)),
                ((125, 374, 225, 295), self.Room1Functions.on_caesar_cipher_click),
                ((340, 370, 365, 385), self.Room1Functions.on_light_switch_click),
                ((305, 380, 95, 150), self.Room1Functions.on_light_click),
                ((115, 373, 480, 595), self.Room1Functions.on_desk_click),
                ((598, 680, 140, 400), self.Room1Functions.on_right_window_click),
            ],
            #Create instances of a draggable that are tied only to room 1 (trashcan, key, and the clock) 
            [
                Draggable(self.canvas, resource_path("key.png"), 465, 170, 10, 10, lambda: self.Room1Functions.on_key_drag_end(self)),
                Draggable(self.canvas, resource_path("clock.png"), 465, 170, 75, 75, self.Room1Functions.on_clock_drag_end)
            ],

            {
                "sticky_note_found": False,  # Points #1
                "vigenere_message_obtained": False,  # Points #1
                "caesar_revealed": False,  # Points #2
                "door_unlocked": False,  # Points #3
            },


            [
                {"desc": "Find sticky note","completed": False,},
                {"desc": "Found Vigenère cipher text","completed": False,},
                {"desc": "Reveal Caesar cipher text","completed": False,},
                {"desc": "Door unlocked","completed": False,}
            ]
        )

        #For future use
        Room2 = Room("Room 2", resource_path("Room2.png"), [], [])
        Room3 = Room("Room 3", resource_path("Room3.png"), [], [])
        Room4 = Room("Room 4", resource_path("Room4.png"), [], [])
        Room5 = Room("Room 4", resource_path("Room5.png"), [], [])

        #
        Room0.exits = [Room1]
        Room1.exits = [Room0, Room2]
        Room2.exits = [Room1, Room3]
        Room3.exits = [Room2, Room4, Room5]

        Room

        self.rooms = [Room1, Room2, Room3, Room4, Room5]
        self.current_room = Room1

    #Sets up the game to be played
    def play(self):
        self.Room1Functions.check_code_update(self)
        self.setup()
        self.task_window = TaskWindow(self.parent, self.current_room.tasks)
        self.canvas.bind("<Configure>", lambda event: self.resize_canvas(event, self.canvas))
        self.canvas.bind("<Button-1>", self.on_click)


root = tk.Tk()
root.title("A Thief's Journey")  #Top left title of the
root.geometry("700x700")  #Initial size of the window
root.minsize(700, 700)  #Window must be this size or larger
root.resizable(True, True) #Allows for the window to be resizable in both x and y direction
game = ThievesJourney(root)
game.play()
root.mainloop()

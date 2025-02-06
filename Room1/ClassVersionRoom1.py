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
from Classes import Draggable, Room
from GlobalFunctions import resource_path

class ThievesJourney(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        self.canvas = tk.Canvas(root)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.rooms = []
        self.current_room = None

        self.windowWidthTracker = 700
        self.windowHeightTracker = 700

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
            #Create instances of a draggable that are tied only to room 1 (trashcan, key, and the clock) 
            [
                Draggable(self.canvas, resource_path("key.png"), 465, 170, 10, 10),
                Draggable(self.canvas, resource_path("clock.png"), 465, 170, 75, 75)
            ]
        )

        #For future use
        Room0 = Room("Room 0", resource_path("Room0.png"), [], [])
        Room2 = Room("Room 2", resource_path("Room2.png"), [], [])
        Room3 = Room("Room 3", resource_path("Room3.png"), [], [])
        Room4 = Room("Room 4", resource_path("Room4.png"), [], [])

        #
        Room1.next_room = Room2
        Room2.next_room = Room3
        Room3.next_room = Room4

        self.rooms = [Room1, Room2, Room3, Room4]
        self.current_room = Room1

    def resize_canvas(self, event, canvas_var: 'tk.Canvas', path_to_image=None, draggables=None):
        #Reads the room's image path

        if path_to_image == None:
            path_to_image = self.current_room.image_path

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

        #Ratios for increasing or decreasing the size and location of the draggables
        width_ratio = (new_width / self.windowWidthTracker)
        height_ratio = (new_height / self.windowHeightTracker)

        #Iterate through all of the draggables within the current room - when the window is resized, the draggables will stay in their position and not move. They will also be resized accordingly.
        for item in draggables:
        #For x size (both moving and resizing) 
            item.x_size, item.x_cord = item.x_size * width_ratio, item.x_cord * width_ratio
        #For y size (both moving and resizing)
            item.y_size, item.y_cord = item.y_size * height_ratio, item.y_cord * height_ratio

            # Resize the draggable item image and update the draggable's internal variables
            item.image = item.image.resize((int(item.x_size), int(item.y_size)))
            item.tk_image = ImageTk.PhotoImage(item.image)

            # Re-create draggable item with the updated position and size
            item.id = canvas_var.create_image(item.x_cord, item.y_cord, image=item.tk_image)
            #Allows for dragging to take place
            canvas_var.tag_bind(item.id, "<ButtonPress-1>", item.on_press)
            canvas_var.tag_bind(item.id, "<B1-Motion>", item.on_drag)

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

    def change_room(self):
        if self.current_room.next_room:
            self.current_room = self.current_room.next_room
            self.resize_canvas(self.canvas, tk.Event)

    #General functions for printing what is pressed on
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

        trashcan_canvas.bind("<Configure>",  lambda event: self.resize_canvas(event, trashcan_canvas, img_path, self.trashcan_draggables))
        trashcan_canvas.tag_bind(self.note_id, "<Button-1>", self.on_note_click)

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

    #Sets up the game to be played
    def play(self):
        self.setup()
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

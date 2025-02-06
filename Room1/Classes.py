import tkinter as tk
from PIL import Image, ImageTk

class Draggable:
    def __init__(self, canvas, image_path, cord_x, cord_y, size_x, size_y):

        self.canvas = canvas
        self.x_size = size_x
        self.y_size = size_y
        
        self.image = Image.open(image_path).resize((self.x_size, self.y_size))
        self.tk_image = ImageTk.PhotoImage(self.image)

        self.x_cord = cord_x
        self.y_cord = cord_y
        self.id = self.canvas.create_image(self.x_cord, self.y_cord, image=self.tk_image)

    def on_press(self, event):
        self.start_x = event.x
        self.start_y = event.y

    def on_drag(self, event):
        dx = event.x - self.start_x
        dy = event.y - self.start_y
        self.canvas.move(self.id, dx, dy)
        self.start_x, self.start_y  = event.x, event.y

        self.x_cord, self.y_cord = self.canvas.coords(self.id)

class Room:

    def __init__(self, name: str, image_path: str, click_actions: list, drag_items: list):

        self.name = name
        self.image_path = image_path
        self.click_actions = click_actions
        self.drag_items = drag_items
        self.extra = None

import tkinter as tk
from PIL import Image, ImageTk

class Draggable:
    def __init__(self, canvas, image_path, cord_x, cord_y, size_x, size_y, on_drag_end=None):
        self.canvas = canvas
        self.x_size = size_x
        self.y_size = size_y
        self.on_drag_end = on_drag_end

        # Open and resize the image.
        self.image = Image.open(image_path).resize((self.x_size, self.y_size))
        self.tk_image = ImageTk.PhotoImage(self.image)

        self.x_cord = cord_x
        self.y_cord = cord_y
        # Create the image on the canvas at the specified coordinates.
        self.id = self.canvas.create_image(self.x_cord, self.y_cord, image=self.tk_image)

        # Bind mouse events for dragging.
        self.canvas.tag_bind(self.id, "<ButtonPress-1>", self.on_press)
        self.canvas.tag_bind(self.id, "<ButtonRelease-1>", self.on_release)

    def on_press(self, event):
        # Record the starting position of the mouse.
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)

    def on_drag(self, event, root: 'tk.Frame'):
        # Convert event coordinates to canvas coordinates.
        new_x = self.canvas.canvasx(event.x)
        new_y = self.canvas.canvasy(event.y)
        # Calculate the change in position.
        dx = new_x - self.start_x
        dy = new_y - self.start_y
        # Move the object on the canvas.
        self.canvas.move(self.id, dx, dy)
        # Update the starting position for the next motion event.
        self.start_x, self.start_y = new_x, new_y
        # Update the stored coordinates.
        self.x_cord, self.y_cord = self.canvas.coords(self.id)
        self.x_cord = (self.x_cord * 700) // root.winfo_width()
        self.y_cord = (self.y_cord * 700) // root.winfo_height()        

    def on_release(self, event):
        
        #print("Mouse released at:", self.x_cord, self.y_cord)
        # When the drag is finished, call the callback function if provided.
        if self.on_drag_end:
            self.on_drag_end(self)

class Room:
    def __init__(self, name: str, image_path: str, click_actions, drag_items: list):
        self.name = name
        self.image_path = image_path
        self.click_actions = click_actions
        self.drag_items = drag_items
        self.exits = []


class TaskWindow(tk.Toplevel):
    def __init__(self, master, tasks):
        super().__init__(master)
        self.title("Tasks")
        # Set a fixed geometry for the task window (e.g., width=250, height=700)
        self.geometry("250x250")
        self.tasks = tasks
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Task List", font=("Arial", 16), bg="gray").pack(pady=10)
        self.task_listbox = tk.Listbox(self, font=("Arial", 10))
        self.task_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.update_tasks()

    def update_tasks(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            #Comment out the if statement to show all tasks (debugging purposes)
            if task ["completed"]:
                status = "[✓]" if task["completed"] else "[ ]"
                self.task_listbox.insert(tk.END, f"{status} {task['desc']}")

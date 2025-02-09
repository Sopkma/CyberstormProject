import tkinter as tk
from PIL import Image, ImageTk


class Draggable:
    def __init__(
        self, canvas, image_path, cord_x, cord_y, size_x, size_y, on_drag_end=None
    ):
        self.canvas = canvas
        self.x_size = size_x
        self.y_size = size_y
        self.on_drag_end = on_drag_end

        # Open and resize the image.
        self.image = Image.open(image_path).resize((self.x_size, self.y_size))
        self.tk_image = ImageTk.PhotoImage(self.image)

        self.x_cord = cord_x
        self.y_cord = cord_y
        # Create the image on the canvas.
        self.id = self.canvas.create_image(
            self.x_cord, self.y_cord, image=self.tk_image
        )

        # Bind mouse events for dragging.
        self.canvas.tag_bind(self.id, "<ButtonPress-1>", self.on_press)
        self.canvas.tag_bind(self.id, "<B1-Motion>", self.on_drag)
        self.canvas.tag_bind(self.id, "<ButtonRelease-1>", self.on_release)

    def on_press(self, event):
        # Record the starting mouse position.
        self.start_x = event.x
        self.start_y = event.y

    def on_drag(self, event):
        # Calculate the delta movement.
        dx = event.x - self.start_x
        dy = event.y - self.start_y
        # Move the image on the canvas.
        self.canvas.move(self.id, dx, dy)
        # Update the starting position.
        self.start_x, self.start_y = event.x, event.y
        # Update the stored coordinates.
        self.x_cord, self.y_cord = self.canvas.coords(self.id)

    def on_release(self, event):
        # When the drag is finished, call the callback if provided.
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
        self.geometry("250x700")
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
            status = "[✓]" if task["completed"] else "[ ]"
            self.task_listbox.insert(tk.END, f"{status} {task['desc']}")

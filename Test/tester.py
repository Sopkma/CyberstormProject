import tkinter as tk


def on_click(event):
    global start_x, start_y
    start_x = event.x
    start_y = event.y


def on_drag(event):
    global start_x, start_y
    delta_x = event.x - start_x
    delta_y = event.y - start_y
    canvas.move("my_shape", delta_x, delta_y)
    start_x = event.x
    start_y = event.y


# Create the main window
root = tk.Tk()
root.title("Tkinter Draggable Shape")

# Create a canvas to draw on
canvas = tk.Canvas(root, width=500, height=300)
canvas.pack()

# Create a shape (rectangle)
start_x = 0
start_y = 0
shape = canvas.create_rectangle(50, 50, 100, 100, fill="blue", tags="my_shape")

# Bind events to the canvas
canvas.bind("<Button-1>", on_click)  # On left mouse button press
canvas.bind("<B1-Motion>", on_drag)  # On mouse motion with left button pressed

root.mainloop()

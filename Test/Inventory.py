import tkinter as tk


class Inventory:
    def __init__(self, root):
        self.root = root
        self.inventory_frame = tk.Frame(root)
        self.inventory_frame.pack(side="left", fill="both", expand=True)

        # Example: List of items (replace with your actual data)
        self.items = [
            {"name": "Sword", "image": "sword.png"},
            {"name": "Shield", "image": "shield.png"},
            {"name": "Potion", "image": "potion.png"},
            {"name": "Key", "image": "key.png"},
        ]

        # Create a canvas to display items
        self.canvas = tk.Canvas(self.inventory_frame, width=200, height=200)
        self.canvas.pack(side="left", fill="both", expand=True)

        # Display items as shapes on the canvas
        self.item_shapes = []
        x, y = 20, 20
        for item in self.items:
            img = tk.PhotoImage(file=item["image"])  # Load image
            item_shape = self.canvas.create_image(x, y, anchor="nw", image=img)
            self.item_shapes.append(item_shape)
            x += 50  # Adjust spacing between items

        # Bind click event to the canvas
        self.canvas.bind("<Button-1>", self.on_item_click)

    def on_item_click(self, event):
        x, y = event.x, event.y
        for i, item_shape in enumerate(self.item_shapes):
            item_bbox = self.canvas.bbox(item_shape)
            if item_bbox[0] <= x <= item_bbox[2] and item_bbox[1] <= y <= item_bbox[3]:
                # Item clicked
                item_name = self.items[i]["name"]
                print(f"Equipped/Used: {item_name}")
                break


# Create the main window
root = tk.Tk()
root.title("Inventory Example")

# Create an instance of the Inventory class
inventory = Inventory(root)

root.mainloop()

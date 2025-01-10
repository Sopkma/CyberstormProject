import tkinter as tk
from tkinter import simpledialog, messagebox

# Function to show a hint screen
def show_hint(hint_num, text, button):
    hint_window = tk.Toplevel()
    hint_window.title(f"Hint {hint_num}")
    hint_window.geometry(f"200x100+{button.winfo_rootx()}+{button.winfo_rooty()}")
    hint_label = tk.Label(hint_window, text=text)
    hint_label.pack(pady=20, padx=20)

# Function to modify the main window to display the second room
def second_room(root):
    for widget in root.winfo_children():
        widget.destroy()

    label = tk.Label(root, text="Welcome to the second room!")
    label.pack(pady=20, padx=20)

    # Add buttons for second room hints
    hint1_button = tk.Button(root, text="Hint 1 (Room 2)", command=lambda: show_hint(1, "This is the first hint for Room 2", hint1_button))
    hint1_button.place(x=100, y=100)

    hint2_button = tk.Button(root, text="Hint 2 (Room 2)", command=lambda: show_hint(2, "This is the second hint for Room 2", hint2_button))
    hint2_button.place(x=500, y=300)

    hint3_button = tk.Button(root, text="Hint 3 (Room 2)", command=lambda: show_hint(3, "This is the third hint for Room 2", hint3_button))
    hint3_button.place(x=900, y=200)

# Function to handle lock interaction
def handle_lock(root):
    code = simpledialog.askstring("Enter Code", "Please enter the code:")
    if code == "1234":  # Replace "1234" with your desired code
        second_room(root)
    else:
        messagebox.showerror("Error", "Incorrect code. Try again!")

# Main function to create the GUI
def main():
    root = tk.Tk()
    root.title("Escape Room")

    # Add buttons for hints
    hint1_button = tk.Button(root, text="Hint 1", command=lambda: show_hint(1, "This is the first hint", hint1_button))
    hint1_button.place(x=100, y=100)

    hint2_button = tk.Button(root, text="Hint 2", command=lambda: show_hint(2, "This is the second hint", hint2_button))
    hint2_button.place(x=500, y=300)

    hint3_button = tk.Button(root, text="Hint 3", command=lambda: show_hint(3, "This is the third hint", hint3_button))
    hint3_button.place(x=900, y=200)

    # Add button for the lock
    lock_button = tk.Button(root, text="Lock", command=lambda: handle_lock(root))
    lock_button.place(x=600, y=500)

    # Set the size of the main window
    root.geometry("1200x650")

    root.mainloop()

if __name__ == "__main__":
    main()

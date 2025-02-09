import os
import sys

# Function to get the path to the images folder
def resource_path(image_name):
    if getattr(sys, "frozen", False):
        # If we're running as a bundled executable
        bundled_directory = sys._MEIPASS
    else:
        # If we're running in a normal Python script
        bundled_directory = os.path.dirname(os.path.abspath(__file__))

    images_folder_dir = os.path.join(bundled_directory, "images")
    full_image_path = os.path.join(images_folder_dir, image_name)

    return full_image_path
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.colorchooser import askcolor
from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont, ImageOps


# Function to open a file dialog and return the selected file path
def select_file(file_type):
    return filedialog.askopenfilename(title=f"Select {file_type}", filetypes=[(file_type, "*.*")])
# Function to create a circular profile image from the given profile image path
def create_circular_profile_image(profile_image_path):
    profile_image = Image.open(profile_image_path).convert("RGBA")  # Open image and convert to RGBA mode
    big_size = (profile_image.size[0] * 3, profile_image.size[1] * 3)  # Create a big size for the mask
    mask = Image.new('L', big_size, 0)  # Create a new grayscale image for the mask
    draw = ImageDraw.Draw(mask)  # Create a draw object for the mask
    draw.ellipse((0, 0) + big_size, fill=255)  # Draw an ellipse (circle) on the mask
    mask = mask.resize(profile_image.size, Image.ANTIALIAS)  # Resize the mask to the profile image size
    profile_image.putalpha(mask)  # Apply the mask to the profile image
    output = ImageOps.fit(profile_image, mask.size, centering=(0.5, 0.5))  # Fit the profile image to the mask size
    output.putalpha(mask)  # Apply the mask again to ensure transparency
    return output  # Return the processed circular profile image
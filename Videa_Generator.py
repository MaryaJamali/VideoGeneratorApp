import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.colorchooser import askcolor
from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont, ImageOps


# Function to open a file dialog and return the selected file path
def select_file(file_type):
    return filedialog.askopenfilename(title=f"Select {file_type}", filetypes=[(file_type, "*.*")])

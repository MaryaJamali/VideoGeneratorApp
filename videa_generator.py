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


# Function to wrap text to fit within a certain width
def wrap_text(text, width):
    lines = []  # Initialize an empty list for lines of text
    while len(text) > width:
        split_index = text.rfind(" ", 0, width)  # Find the index of the last space within the width
        if split_index == -1:
            split_index = width  # If no space found, split at the exact width
        lines.append(text[:split_index].strip())  # Append the line to the list
        text = text[split_index:].strip()  # Update text to the remaining part
    if len(text) > 0:
        lines.append(text.strip())  # Append the last part of the text
    return lines  # Return the wrapped lines of text


# Function to create a video from the given inputs
def create_video(image_path, profile_image_path, audio_path, text, username, text_color, profile_text_color,
                 output_path):
    image = Image.open(image_path).convert("RGBA")  # Load the original image

    # Load and resize circular profile image
    profile_image = create_circular_profile_image(profile_image_path)
    profile_image_size = (100, 100)
    profile_image = profile_image.resize(profile_image_size)

    # Calculate position to place profile image at the top of the background image
    profile_position = (int((image.width - profile_image_size[0]) / 2), 20)  # Adjust Y position as needed

    # Paste profile image onto the background image
    image.paste(profile_image, profile_position, profile_image)

    # Add text to the image
    draw = ImageDraw.Draw(image)
    text_font = ImageFont.truetype("arial.ttf", 18)

    # Wrap text to fit within a certain width
    wrapped_text = wrap_text(text, 20)
    text_lines = len(wrapped_text)

    # Calculate total height needed for text
    total_text_height = text_lines * text_font.getsize("H")[1]

    # Position text at the bottom of the image
    text_position = (int((image.width - profile_image_size[0]) / 2), image.height - total_text_height - 20)

    # Draw wrapped text on the image
    for line in wrapped_text:
        draw.text(text_position, line, fill=text_color, font=text_font)
        text_position = (text_position[0], text_position[1] + text_font.getsize("H")[1])

    # Calculate text width for username
    username_width, username_height = draw.textsize(username, font=text_font)

    # Position username centered below the profile image
    username_position = (int((image.width - username_width) / 2), int(profile_position[1] + profile_image_size[1] + 10))

    # Draw username on the image
    draw.text(username_position, username, fill=profile_text_color, font=text_font)

    # Save the temporary image
    temp_image_path = "temp_image_with_text.png"
    image.save(temp_image_path)

    # Load audio clip
    audio = AudioFileClip(audio_path)

    # Create video clip from the image
    image_clip = ImageClip(temp_image_path, duration=audio.duration)

    # Set frame rate for the clip
    fps = 24
    image_clip = image_clip.set_fps(fps)

    # Set audio to the video
    video_clip = image_clip.set_audio(audio)

    # Write the video file
    video_clip.write_videofile(output_path, codec='libx264', audio_codec='aac', fps=fps)

    # Remove the temporary image file
    os.remove(temp_image_path)

    messagebox.showinfo("Success", "Video has been created successfully!")


# Function to select an image file and update the label
def select_image():
    global image_path  # Declare global variable for image path
    image_path = select_file("Image")  # Call select_file function to get image file path
    image_label.config(text=f"Image: {image_path}")  # Update label text with selected image file path


# Function to select a profile image file and update the label
def select_profile_image():
    global profile_image_path  # Declare global variable for profile image path
    profile_image_path = select_file("Profile Image")  # Call select_file function to get profile image file path
    # Update label text with selected profile image file path
    profile_label.config(text=f"Profile Image: {profile_image_path}")


# Function to select an audio file and update the label
def select_audio():
    global audio_path  # Declare global variable for audio file path
    audio_path = select_file("Audio")  # Call select_file function to get audio file path
    audio_label.config(text=f"Audio: {audio_path}")  # Update label text with selected audio file path


# Function to select an output directory and update the label
def select_output_dir():
    global output_dir  # Declare global variable for output directory path
    output_dir = filedialog.askdirectory(title="Select Output Directory")  # Call filedialog to select output directory
    output_label.config(text=f"Output Directory: {output_dir}")  # Update label text with selected output directory path


# Function to choose text color using color chooser dialog
def choose_text_color():
    global text_color  # Declare global variable for text color
    color = askcolor(title="Choose Text Color")[1]  # Call askcolor function to choose color
    text_color = color  # Update text color variable with selected color
    text_color_label.config(bg=color)  # Update label background color with selected color


# Function to choose profile text color using color chooser dialog
def choose_profile_text_color():
    global profile_text_color  # Declare global variable for profile text color
    color = askcolor(title="Choose Profile Text Color")[1]  # Call askcolor function to choose color
    profile_text_color = color  # Update profile text color variable with selected color
    profile_text_color_label.config(bg=color)  # Update label background color with selected color


# Function to generate video using user inputs
def generate_video():
    text = text_entry.get()  # Get text entered by user
    username = username_entry.get()  # Get username entered by user
    # Check if all necessary fields are filled and files are selected
    if not (image_path and profile_image_path and audio_path and output_dir and text and username):
        messagebox.showerror("Input Error", "Please fill in all fields and select all files.")
        return  # Exit function if any field or file is missing

    output_path = f"{output_dir}/output_video.mp4"  # Define output file path
    create_video(image_path, profile_image_path, audio_path, text, username, text_color, profile_text_color,
                 output_path)  # Call create_video function with all parameters to generate video


# Create the main window
root = tk.Tk()  # Create tkinter root window
root.title("Video Generator")  # Set window title

# Initialize variables for file paths and default colors
image_path = None
profile_image_path = None
audio_path = None
output_dir = None
text_color = "white"
profile_text_color = "white"

# Create buttons and labels for selecting files and inputs
tk.Button(root, text="Select Image", command=select_image).pack(pady=10)
image_label = tk.Label(root, text="No Image Selected", wraplength=300)
image_label.pack()

# Create button to select profile image file and associate it with select_profile_image function
tk.Button(root, text="Select Profile Image", command=select_profile_image).pack(pady=10)
profile_label = tk.Label(root, text="No Profile Image Selected", wraplength=300)
profile_label.pack()

# Create button to select audio file and associate it with select_audio function
tk.Button(root, text="Select Audio", command=select_audio).pack(pady=10)
audio_label = tk.Label(root, text="No Audio Selected", wraplength=300)
audio_label.pack()

# Label and entry for user to enter text
tk.Label(root, text="Enter Text:", font=("Arial", 12)).pack()
text_entry = tk.Entry(root, font=("Arial", 12))
text_entry.pack(pady=5)

# Button to choose text color and associate it with choose_text_color function
tk.Button(root, text="Choose Text Color", command=choose_text_color).pack(pady=10)
text_color_label = tk.Label(root, text="Choose Text Color", bg=text_color)
text_color_label.pack()

# Label and entry for user to enter username
tk.Label(root, text="Enter Username:", font=("Arial", 12)).pack()
username_entry = tk.Entry(root, font=("Arial", 12))
username_entry.pack(pady=5)

# Button to choose profile text color and associate it with choose_profile_text_color function
tk.Button(root, text="Choose Profile Text Color", command=choose_profile_text_color).pack(pady=10)
profile_text_color_label = tk.Label(root, text="Choose Profile Text Color", bg=profile_text_color)
profile_text_color_label.pack()

# Button to select output directory and associate it with select_output_dir function
tk.Button(root, text="Select Output Directory", command=select_output_dir).pack(pady=10)
output_label = tk.Label(root, text="No Output Directory Selected", wraplength=300)
output_label.pack()

# Button to generate video and associate it with generate_video function
generate_button = tk.Button(root, text="Generate Video", command=generate_video, font=("Arial", 14), bg="blue",
                            fg="white")
generate_button.pack(pady=20, ipadx=20, ipady=10)

root.mainloop()  # Start the tkinter main loop to display the GUI

# Name of the programmer: Maryam Jamali
# Email address: m.jamali16@yahoo.com
# GitHub address: https://github.com/MaryaJamali

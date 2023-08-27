import tkinter as tk
from tkinter import Label, Button
from PIL import Image, ImageTk

# Function to destroy the image label
def destroy_image_label():
    image_label.destroy()
    destroy_button.destroy()

# Create a Tkinter window
root = tk.Tk()
root.title("PIL Image Display")

# Add text to the window
text_label = Label(root, text="Hello, PIL Image!")
text_label.pack()

# Load the image using PIL
pil_image = Image.open('/Users/Stas/Downloads/stopmath.png')  # Replace "image.jpg" with your image file

# Convert PIL image to Tkinter PhotoImage
tk_image = ImageTk.PhotoImage(pil_image)

# Create a label to display the image
image_label = Label(root, image=tk_image)
image_label.place(x=0, y=0, relwidth=1, relheight=1)  # Image label covers the entire window

# Create a button to destroy the image label
destroy_button = Button(root, text="Destroy Image", command=destroy_image_label)
# destroy_button.pack()

# Run the Tkinter event loop
root.mainloop()
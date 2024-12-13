import tkinter as tk
from tkinter import filedialog, messagebox
import os
import cv2
# Function to browse input folder
def browse_input_folder():
    folder_selected = filedialog.askdirectory()
    input_folder_entry.delete(0, tk.END)  # Clear existing text
    input_folder_entry.insert(0, folder_selected)  # Insert the new path
# Function to browse output folder
def browse_output_folder():
    folder_selected = filedialog.askdirectory()
    output_folder_entry.delete(0, tk.END)
    output_folder_entry.insert(0, folder_selected)
# Function to process images and detect faces
def process_images():
    input_folder = input_folder_entry.get()
    output_folder = output_folder_entry.get()
    if not input_folder or not output_folder:
        messagebox.showerror("Error", "Please select both input and output folders.")
        return
    # Load pre-trained face detector
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    total_images = 0
    images_with_faces = 0
    # Loop through all images in the folder
    for filename in os.listdir(input_folder):
        img_path = os.path.join(input_folder, filename)
        img = cv2.imread(img_path)
        # Skip non-image files
        if img is None:
            continue
        total_images += 1
        # Convert image to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)
        # Detect faces
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        if len(faces) > 0:
            images_with_faces += 1
            output_img_path = os.path.join(output_folder, filename)
            cv2.imwrite(output_img_path, img)
    # Calculate success percentage
    if total_images > 0:
        success_percentage = (images_with_faces / total_images) * 100
        messagebox.showinfo("Processing Complete", f"Processing complete! {success_percentage:.2f}% images with faces detected.")
    else:
        messagebox.showwarning("No Images", "No images found in the input folder.")
# Set up the Tkinter window
root = tk.Tk()
root.title("Face Detection Script")
# Input Folder
input_folder_label = tk.Label(root, text="Select Input Folder:")
input_folder_label.grid(row=0, column=0, padx=10, pady=10)
input_folder_entry = tk.Entry(root, width=40)
input_folder_entry.grid(row=0, column=1, padx=10, pady=10)
input_folder_button = tk.Button(root, text="Browse", command=browse_input_folder)
input_folder_button.grid(row=0, column=2, padx=10, pady=10)
# Output Folder
output_folder_label = tk.Label(root, text="Select Output Folder:")
output_folder_label.grid(row=1, column=0, padx=10, pady=10)
output_folder_entry = tk.Entry(root, width=40)
output_folder_entry.grid(row=1, column=1, padx=10, pady=10)
output_folder_button = tk.Button(root, text="Browse", command=browse_output_folder)
output_folder_button.grid(row=1, column=2, padx=10, pady=10)
# Process Button
process_button = tk.Button(root, text="Start Processing", command=process_images)
process_button.grid(row=2, column=0, columnspan=3, padx=10, pady=10)
# Run the Tkinter event loop
root.mainloop()
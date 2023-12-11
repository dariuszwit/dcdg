import tkinter as tk
from tkinter import filedialog, messagebox
import os
from threading import Thread
# Import your modules here

def run_processing(input_dir, output_dir, mode):
    # Place your processing logic here
    # For example: process_directory(input_dir, output_dir, config_file, mode)
    print(f"Processing: {input_dir} -> {output_dir} in mode {mode}")
    # Add your processing handling code here

def start_processing_thread(input_dir, output_dir, mode):
    # Create a thread for processing to prevent GUI freezing
    processing_thread = Thread(target=run_processing, args=(input_dir, output_dir, mode))
    processing_thread.start()

def select_input_directory():
    # Open a dialog to select the input directory
    folder_selected = filedialog.askdirectory()
    input_dir_entry.delete(0, tk.END)
    input_dir_entry.insert(0, folder_selected)

def select_output_directory():
    # Open a dialog to select the output directory
    folder_selected = filedialog.askdirectory()
    output_dir_entry.delete(0, tk.END)
    output_dir_entry.insert(0, folder_selected)

# Main window settings
root = tk.Tk()
root.title("File Processing Tool")

# GUI Elements
input_dir_label = tk.Label(root, text="Input Directory:")
input_dir_label.pack()
input_dir_entry = tk.Entry(root, width=50)
input_dir_entry.pack()
input_dir_button = tk.Button(root, text="Select", command=select_input_directory)
input_dir_button.pack()

output_dir_label = tk.Label(root, text="Output Directory:")
output_dir_label.pack()
output_dir_entry = tk.Entry(root, width=50)
output_dir_entry.pack()
output_dir_button = tk.Button(root, text="Select", command=select_output_directory)
output_dir_button.pack()

mode_label = tk.Label(root, text="Processing Mode:")
mode_label.pack()
mode_var = tk.StringVar()
mode_var.set("all")  # Set the default mode
mode_options = tk.OptionMenu(root, mode_var, "all", "ignore", "only", "size_only")
mode_options.pack()

start_button = tk.Button(root, text="Start", command=lambda: start_processing_thread(input_dir_entry.get(), output_dir_entry.get(), mode_var.get()))
start_button.pack()

# Start the main loop
root.mainloop()

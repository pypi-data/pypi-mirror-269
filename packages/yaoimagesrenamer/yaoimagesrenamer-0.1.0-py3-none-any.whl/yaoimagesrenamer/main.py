import os
import glob
import numpy as np

def images_renamer(folder_path):
    # Make sure the folder path is valid
    if not os.path.isdir(folder_path):
        print(f"The specified folder path '{folder_path}' does not exist.")
        return
    
    # Get all PNG files in the folder
    png_files = glob.glob(os.path.join(folder_path, "*.png"))

    if not png_files:
        print("No PNG files found in the specified folder.")
        return

    # Sort the files to ensure consistent order
    png_files.sort()

    # Create a numpy array with sequential numbers starting from 1
    num_files = len(png_files)
    file_indices = np.arange(1, num_files + 1)  # This will give you [1, 2, ..., num_files]

    # Rename the files using the numpy array for indices
    for i, file_path in zip(file_indices, png_files):
        new_name = f"{i}.png"
        new_file_path = os.path.join(folder_path, new_name)
        os.rename(file_path, new_file_path)

    print("Renaming completed successfully!")
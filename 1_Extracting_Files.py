# Problem 1 - Extract all the files from the zip
# Add this to a folder named "Kaggle"
# Make sure there are no zip files in the "Kaggle" folder

# Importing modules required later
import numpy as np
import pandas as pd
import seaborn as sns
# use sparingly - seaborn instead
import matplotlib.pyplot as plt
import os
from zipfile import ZipFile

# Defining the zip
file = "kaggle-survey"
extension = ".zip"

# Open the zip file in read mode
with ZipFile(file + extension, "r") as zip_file:
    # Extract the contents of this zip file into a "Kaggle" folder
    zip_file.extractall()

# Change the folder name to "Kaggle"
os.rename(file, "Kaggle")

# Find the current working directory
new_cwd = os.getcwd() + "\Kaggle"

# Ensure everything within the Kaggle folder is unzipped also
for subdir, dirs, files in os.walk(new_cwd):
    # Go through each file within each sub-directory
    for new_file in files:
        cwd_and_new_file = os.path.join(subdir, new_file)
        # Check whether we have a zip file within this sub-directory
        if new_file.endswith(".zip"):
            # Open the zip file in read mode and extract its contents
            with ZipFile(cwd_and_new_file, "r") as new_zip_file:
                new_zip_file.extractall(os.path.join(subdir, os.path.splitext(new_file)[0]))
            # Delete the original zip file
            os.remove(cwd_and_new_file)

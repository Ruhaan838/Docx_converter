from tkinter import filedialog

def location_folder(file_location):
    file_location_input = filedialog.askdirectory(
        title="Select a folder",
        initialdir=file_location
    )
    return file_location_input
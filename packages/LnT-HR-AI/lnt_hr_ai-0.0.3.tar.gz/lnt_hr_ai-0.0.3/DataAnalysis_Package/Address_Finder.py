import tkinter as tk
from tkinter import filedialog

def Filechooser():
    # Create a root window for the file dialog
    root = tk.Tk()
    root.withdraw() # Hide the root window
    
    # Open the file dialog and get the selected file path
    file_path = filedialog.askopenfilename()
    
    # Print the selected file path
    address=""
    for iterator in file_path:
        if iterator=="/" :
            address+="\\\\"
        else:
            address+=iterator

        
    # Close the application
    root.destroy()
    return(address)

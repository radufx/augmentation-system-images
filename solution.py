import cv2
import os
import numpy as np
import tkinter
from tkinter import filedialog
from matplotlib import pyplot as plt

def select_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        file_list.delete(0, tkinter.END)
        for filename in os.listdir(folder_path):
            file_list.insert(tkinter.END, filename)

root = tkinter.Tk()
root.title("Select Test images folder")


select_button = tkinter.Button(root, text="Select Folder", command=select_folder)
select_button.pack(pady=10)

file_list = tkinter.Listbox(root, selectmode=tkinter.SINGLE)
file_list.pack(fill=tkinter.BOTH, expand=True)

root.mainloop()
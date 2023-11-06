import tkinter
from tkinter import filedialog

from augmentationSystem import AugmentationSystem

CONFIG_FILE = "config.txt"

augmentation_system = AugmentationSystem(CONFIG_FILE)


root = tkinter.Tk()
root.title("Select Test images folder")
input_dir = filedialog.askdirectory()

output_dir = input_dir + "_aug"

augmentations = augmentation_system.read_config()

augmentation_system.process_images(input_dir, output_dir)

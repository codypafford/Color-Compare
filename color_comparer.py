import tkinter as tk
from tkinter import *
import random
from PIL import Image, ImageTk
from tkinter import filedialog
import pyautogui
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000


select_base_color_mode = False
base_color_red = 0
base_color_green = 0
base_color_blue = 0
image_selected = False

def getDifferenceBetweenColors(r2, g2, b2):
    # hardcode base value
    r1 = base_color_red
    g1 = base_color_green
    b1 = base_color_blue

    # Red Color
    color1_rgb = sRGBColor(r1, g1, b1)

    # Blue Color
    color2_rgb = sRGBColor(r2, g2, b2)

    # Convert from RGB to Lab Color Space
    color1_lab = convert_color(color1_rgb, LabColor)

    # Convert from RGB to Lab Color Space
    color2_lab = convert_color(color2_rgb, LabColor)

    # Find the color difference
    delta_e = delta_e_cie2000(color1_lab, color2_lab)

    print("The difference between the 2 color = ", delta_e)
    return delta_e, (100 - delta_e)

def on_click(event):
    global select_base_color_mode
    global base_color_red
    global base_color_green
    global base_color_blue
    global image_selected
    print(event.x,event.y)
    x, y = pyautogui.position()
    pixelColor = pyautogui.screenshot().getpixel((x, y))
    red = pixelColor[0]
    green = pixelColor[1]
    blue = pixelColor[2]
    if select_base_color_mode:
                base_color_red = red
                base_color_green = green
                base_color_blue = blue
                print("Set the base color value to -> " + " Red: " + str(base_color_red) + " Green: " + str(base_color_green) + " Blue: " + str(base_color_blue))
                select_base_color_mode = not select_base_color_mode
                label.configure(text="Now select the color to compare it to")
    else:
        color_difference, color_similarity = getDifferenceBetweenColors(red,green,blue)
        if image_selected:
            label.configure(text="Difference: " + str(round(color_difference, 2)) + "%, Similarity: " + str(round(color_similarity, 2)) + "%")

def open_image():
    global image_selected
    path=filedialog.askopenfilename(filetypes=[("Image File",'.jpg')])
    im = Image.open(path)
    im = im.resize((400, 400), Image.ANTIALIAS)
    tkimage = ImageTk.PhotoImage(im)
    myvar=Label(root,image = tkimage)
    myvar.image = tkimage
    myvar.pack()
    label.configure(text="you selected an image")
    image_selected = True

def selectBaseColor():
    global select_base_color_mode
    select_base_color_mode = True
    print("select base color mode is -> " + str(select_base_color_mode))
    label.configure(text="Click your base color")


root = tk.Tk()
root.geometry("500x500")
root.title('Color Comparer')
picture_chooser_btn = tk.Button(master=root, text='Select Image', command= lambda: open_image())
picture_chooser_btn.pack()
base_color_picker_btn = tk.Button(master=root, text='Choose Base Color', command= lambda: selectBaseColor())
base_color_picker_btn.pack()
label = tk.Label(root, anchor="w")
label.pack(side="top", fill="x") 
root.bind('<ButtonPress-1>', on_click)

root.mainloop()

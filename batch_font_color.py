'''
HSV color selector.
Usage:
  batch_font_color.py <path_to_subfolders>
'''

import Tkinter as tk
import tkFileDialog
import tkMessageBox
from PIL import Image
from PIL import ImageTk
import cv2, glob, os, sys
import numpy as np

root = tk.Tk()
path_to_subfolders = tkFileDialog.askdirectory()

def readyClick():
    if not isInit:
        createBat()
    createFinalBat()

    global img, panelA
    # fn = r'K:\MyPrograms\python2\recipe\simon-crop\tmp.png'
    fn = getNext000()
    if fn is None:
        # make final
        # createFinalBat()
        tkMessageBox.showinfo('Done!', 'final .bat created')
        sys.exit()
    else:
        img = cv2.imread(fn, True)
        img = cv2.pyrUp(img)
        imagePIL = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        imagePIL = Image.fromarray(imagePIL)
        image_tk = ImageTk.PhotoImage(imagePIL)
        if 'panelA' not in globals():
            panelA = tk.Label(image=image_tk)
        panelA.image = image_tk
        # panelA.pack(side=tk.TOP, padx=10, pady=10)
        panelA.grid(row=1, column=1, columnspan=4, padx=10, pady=10)
    if not isInit:
        setRange(None)

def readyClickAll():
    if not isInit:
        # creating .bat for first
        createBat()
        fn = getNext000()
        while fn is not None:
            createBat()
            fn = getNext000()

    tkMessageBox.showinfo('Done!', 'final .bat created')
    sys.exit()
    createFinalBat()

def setRange(event):
    lower = np.array([h_lower.get(), s_lower.get(), v_lower.get()])
    upper = np.array([h_upper.get(), s_upper.get(), v_upper.get()])
    h, w, channels = img.shape[:3]
    hl = np.zeros((h, w, channels), np.uint8)
    hl[:, :, :] = (0, 0, 255)

    hsv = cv2.cvtColor(img.copy(), cv2.COLOR_BGR2HSV)
    color_mask = cv2.inRange(hsv, lower, upper)
    # color_mask2 = (color_mask,)*255
    out = cv2.bitwise_and(hl, img, mask=color_mask)
    flooded = cv2.subtract(img, cv2.merge([color_mask, color_mask, color_mask]))
    flooded = cv2.add(flooded, out)
    # cv2.imshow('font_color', cv2.add(flooded, out))
    imagePIL = cv2.cvtColor(flooded, cv2.COLOR_BGR2RGB)
    imagePIL = Image.fromarray(imagePIL)
    image_tk = ImageTk.PhotoImage(imagePIL)
    panelA.configure(image=image_tk)
    panelA.image = image_tk

def createBat():
    if isInit:
        return
    if karaoke_variable.get() == 'Lyrics':
        command = 'main.exe {} {},{},{},{},{},{}'.format(subfolder_now + os.sep + '*.jpg',
            h_lower.get(), s_lower.get(), v_lower.get(),
            h_upper.get(), s_upper.get(), v_upper.get()
        )
        if line_variable.get() == 'One line':
            command += ' 1'
        command += '\n'
    else:
        ini = """[Movie]
cropX: [0, 0]
cropY: [0, 0]
cropLines: 1
useSymmetry: 0
[Font]
text_lower: [{}, {}, {}]
text_upper: [{}, {}, {}]
font_width: 23
[Th]
minLetterArea: 120
[XLSX]
A_col: time_start
B_col: time_end
C_col: origin
D_col: empty
E_col: prepared"""
        ini = ini.format(
            h_lower.get(), s_lower.get(), v_lower.get(),
            h_upper.get(), s_upper.get(), v_upper.get()
        )
        with open(subfolder_now + '000000.ini', 'w+') as ini_file:
            ini_file.write(ini)
        command = 'main.exe {} {}\n'.format(subfolder_now + '000000.ini', subfolder_now + '*.jpg')
    with open(subfolder_now + '000000.bat', 'w+') as bat:
        bat.write(command)

def createFinalBat():
    full_text = ''
    for subfolder in glob.glob(path_to_subfolders + os.sep + '*' + os.sep):
        # check of .bat already exist
        if not os.path.isfile(subfolder + '000000.bat'):
            continue
        with open(subfolder + '000000.bat', 'r') as bat_now:
            full_text += ''.join(bat_now.readlines())
    with open('final.bat', 'w+') as final_bat:
        final_bat.write(full_text)

subfolder_now = None
def getNext000():
    global subfolder_now
    for subfolder in glob.glob(path_to_subfolders + os.sep + '*' + os.sep):
        # check of .bat already exist
        if os.path.isfile(subfolder + '000000.bat'):
            continue
        if not os.path.isfile(subfolder + '000000.jpg'):
            print('WARNING! 000000.jpg does not exist at '+subfolder)
            continue
        print 'start ' + subfolder
        subfolder_now = subfolder
        return subfolder + '000000.jpg'
    return None

isInit = True
readyClick()
isInit = False

h_lower = tk.Scale(root, from_=0, to=255, length=255, command=setRange, orient=tk.HORIZONTAL)
s_lower = tk.Scale(root, from_=0, to=255, length=255, command=setRange, orient=tk.HORIZONTAL)
v_lower = tk.Scale(root, from_=0, to=255, length=255, command=setRange, orient=tk.HORIZONTAL)
h_upper = tk.Scale(root, from_=0, to=255, length=255, command=setRange, orient=tk.HORIZONTAL)
s_upper = tk.Scale(root, from_=0, to=255, length=255, command=setRange, orient=tk.HORIZONTAL)
v_upper = tk.Scale(root, from_=0, to=255, length=255, command=setRange, orient=tk.HORIZONTAL)

h_lower.set(0) # 0,0,205,200,200,255
s_lower.set(0)
v_lower.set(205)
h_upper.set(200)
s_upper.set(200)
v_upper.set(255)

h_lower.grid(row=2, column=1, columnspan=2)
s_lower.grid(row=3, column=1, columnspan=2)
v_lower.grid(row=4, column=1, columnspan=2)
h_upper.grid(row=2, column=3, columnspan=2)
s_upper.grid(row=3, column=3, columnspan=2)
v_upper.grid(row=4, column=3, columnspan=2)

button = tk.Button(root, text = 'Press for next', command=readyClick)
button.grid(row=5, column=3, pady=20) # columnspan=2

button = tk.Button(root, text = 'Press for all', command=readyClickAll)
button.grid(row=5, column=4, pady=20)

karaoke_variable = tk.StringVar(value='Lyrics')
karaoke = tk.OptionMenu(root, karaoke_variable, 'Subtitle', 'Lyrics')
karaoke.grid(row=5, column=1, pady=20)

line_variable = tk.StringVar(value='One line')
line = tk.OptionMenu(root, line_variable, 'One line', 'Two lines')
line.grid(row=5, column=2, pady=20)

root.mainloop()
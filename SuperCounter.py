import os
import cv2
import math
import numpy as np
from tkinter import *
from tkinter import filedialog 

root = Tk()

def openfn():
    filename = filedialog.askopenfilename(title='open')
    return filename

def open_img():
    x = openfn()
    print(x)
    global img
    img = cv2.imread(str(x))
    global original
    original = img.copy()
    cv2.imshow('ImageWindow', img)
    
    
def get_pos(*arg):

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    h1 = cv2.getTrackbarPos('low_hue', 'settings')
    s1 = cv2.getTrackbarPos('low_satur', 'settings')
    v1 = cv2.getTrackbarPos('low_value', 'settings')
    h2 = cv2.getTrackbarPos('upp_hue', 'settings')
    s2 = cv2.getTrackbarPos('upp_satur', 'settings')
    v2 = cv2.getTrackbarPos('upp_value', 'settings')

    h_min = np.array((h1, s1, v1), np.uint8)
    h_max = np.array((h2, s2, v2), np.uint8)
    
    global mask
    mask = cv2.inRange(hsv, h_min, h_max)
    close()

def close():
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2,2))
    opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
    close = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel, iterations=2)
    global cnts
    cnts = cv2.findContours(close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    cv2.imshow("result", close)

def create_Trackbar():
    cv2.namedWindow("result")  
    cv2.namedWindow("settings")
    cv2.createTrackbar('low_hue', 'settings', 140, 255, get_pos)
    cv2.createTrackbar('low_satur', 'settings', 140, 255, get_pos)
    cv2.createTrackbar('low_value', 'settings', 0, 255, get_pos)
    cv2.createTrackbar('upp_hue', 'settings', 255, 255, get_pos)
    cv2.createTrackbar('upp_satur', 'settings', 255, 255, get_pos)
    cv2.createTrackbar('upp_value', 'settings', 255, 255, get_pos)
    get_pos()
    
def Counter(minimum_area = 500, average_cell_area = 1500, connected_cell_area = 3000):
    cells = 0
    conn_cells=0
    for c in cnts:
        area = cv2.contourArea(c)
        if area > minimum_area:
            if area > connected_cell_area:
                cv2.drawContours(original, [c], -1, (0,0,0), 2)
                M = cv2.moments(c)
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                cv2.putText(original, str(int(math.floor(area / average_cell_area))), (cX - 10, cY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,100,255), 2)            
                conn_cells+=math.floor(area / average_cell_area)
            else: 
                cv2.drawContours(original, [c], -1, (100,255,12), 2)	
                M = cv2.moments(c)
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                cv2.putText(original, "1", (cX - 10, cY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                cells+=1
    newWindow = Toplevel(root)
    newWindow.title("Count result")
    Label(newWindow, text='Cells: {}'.format(cells)).pack()
    Label(newWindow, text='Connected cells: {}'.format(conn_cells)).pack()
    Label(newWindow, text='All cells: {}'.format(conn_cells+cells)).pack()
    cv2.imshow("contours.png", original)


btn_open = Button(root, text='open image', command=open_img).pack()
btn_mask = Button(root, text="create mask", command=create_Trackbar).pack()
btn_count = Button(root, text="count", command=Counter).pack()


cv2.waitKey()
root.mainloop()

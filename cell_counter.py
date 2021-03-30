import cv2
import numpy as np
import math
#import matplotlib.pyplot as plt

image = cv2.imread("6.jpg")
original = image.copy()

hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

hsv_lower = np.array([140,140,0])
hsv_upper = np.array([255,255,255])
mask = cv2.inRange(hsv, hsv_lower, hsv_upper)

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2,2))


opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=2)
close = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel, iterations=2)


cnts = cv2.findContours(close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]

minimum_area = 500
average_cell_area = 1500
connected_cell_area = 3000
cells = 0
conn_cells=0
for c in cnts:
    area = cv2.contourArea(c)
    if area > minimum_area:
        if area > connected_cell_area:
            cv2.drawContours(original, [c], -1, (150,150,20), 1)
            M = cv2.moments(c)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            cv2.putText(original, str(int(math.floor(area / average_cell_area))), (cX - 10, cY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 4)            
            conn_cells+=math.floor(area / average_cell_area)
        else: 
            cv2.drawContours(original, [c], -1, (100,255,12), 2)         
            cells+=1
print('Cells: {}'.format(cells))
print('Connected cells: {}'.format(conn_cells))
#cv2.imwrite("mask.png", close)
#cv2.imwrite("hsv.png", hsv)
cv2.imwrite("contours.png", original)
cv2.waitKey()

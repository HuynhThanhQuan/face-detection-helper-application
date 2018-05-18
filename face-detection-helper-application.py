# -*- coding: utf-8 -*-
"""
Created on Fri May 18 00:17:38 2018

@author: ASUS
"""
import numpy as np
from matplotlib import pyplot as plt 
import matplotlib.patches as patches
from matplotlib.widgets import Button
import cv2 as cv

img = cv.imread('test_image.tiff')

fig, ax = plt.subplots()
ax.imshow(img, interpolation = 'bicubic')
'''preventing plot from rescaling image:'''
ax.set_xlim([0.0, img.shape[1]])
ax.set_ylim([img.shape[0], 0.0])
ax.hold(True)
ax.autoscale = False
#ax.plot(100,100, 'ro')  # This works

class MouseMonitor:
    flag = True
    x = 0.
    y = 0.  
    fig = None
    axes = None

    def __init__(self, fig, ax):
        self.axes = ax
        self.fig = fig
        self.x_rec = []
        self.y_rec = []
        self.num_points = 0
    def __call__(self, event):
        self.num_points += 1
        if event.xdata > 1 and event.ydata > 1:
            if self.flag:
                self.flag = False
            else:
                d = np.linalg.norm([event.xdata - self.x, event.ydata - self.y])
                self.flag = True    
            self.x = event.xdata
            self.y = event.ydata
            self.x_rec.append(self.x)
            self.y_rec.append(self.y)
            self.axes.figure.canvas.draw_idle()
            if self.num_points>1:     
                self.axes.add_patch(
                        patches.Rectangle(
                            (self.x_rec[0], self.y_rec[0]),   # (x,y)
                            self.x - self.x_rec[0],          # width
                            self.y - self.y_rec[0],          # height
                            fill=False
                        )
                )
            self.axes.plot(self.x, self.y, 'ro', linewidth = 3) 
    def remove(self, event):
        self.axes.cla()
        self.axes.imshow(img,interpolation = 'bicubic')
        self.x_rec = []
        self.y_rec = []
    def ok(self,event):
        self.x_rec.append(self.x)
        self.y_rec.append(self.y)
    def get_rec(self):
        return ([self.x_rec[0], self.y_rec[0]], [self.x_rec[1], self.y_rec[1]])

mouse = MouseMonitor(fig, ax)
axre = plt.axes([0.4, 0.9, 0.1, 0.075])
axok = plt.axes([0.6, 0.9, 0.1, 0.075])
btre = Button(axre, 'Remove')
btre.on_clicked(mouse.remove)
btok = Button(axok, "OK")
print(btok.on_clicked(mouse.ok))
cid = fig.canvas.mpl_connect('button_press_event', mouse) 
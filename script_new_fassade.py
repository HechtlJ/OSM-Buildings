"""This Script is still work in progresss. It is the start of an implementation of a phtogrammetry algorithm."""

__author__ = "Johannes Hechtl"
__email__ = "johannes.hechtl@tum.de"
__version__ = "0.1"

from BuildingObject import makeBuilding
from os import read
import FreeCAD, FreeCADGui 
import Part, PartGui 
from PySide import QtGui
#from tr import tr
#from PySide.QtCore import tr
import xml.etree.ElementTree as ET
from Map import Map
import cv2 as cv
import sys
from collections import namedtuple
import numpy as np

IMAGE_MAX_WIDTH = 1200
IMAGE_MAX_HEIGHT = 800



def resize_image(img):

    width = img.shape[1] 
    width_factor = IMAGE_MAX_WIDTH / width

    height = img.shape[0]
    height_factor = IMAGE_MAX_HEIGHT / height

    image_factor = width_factor
    if height_factor < image_factor:
        image_factor = height_factor

    new_width = int(width * image_factor)
    new_height = int(height * image_factor)

    img = cv.resize(img, (new_width, new_height))
    return img

# def draw_circle(event,x,y,flags,param):
#     if event == cv.EVENT_LBUTTONDBLCLK:
#         fassade.corners.append((x,y))
#         update_image()





class NewFassade():
    """My new command"""

    def __init__(self):
        self.fassade = namedtuple("fassade", "src_img corners windows")
        self.fassade.corners = []

    def GetResources(self):
        return {'Pixmap'  : 'My_Command_Icon', # the name of a svg file available in the resources
                'Accel' : "Shift+S", # a default shortcut (optional)
                'MenuText': "Add a Fassade",
                'ToolTip' : "Select an image to add a fassade"}

    def draw_circle(self, event,x,y,flags,param):
        if event == cv.EVENT_LBUTTONDBLCLK:
            point = np.array([x, y])
            self.fassade.corners.append(point)
            self.update_image()

    def empty_method():
        pass

    def update_image(self):
        img = self.fassade.src_img.copy()
        for i in self.fassade.corners:
            x = i[0]
            y = i[1]
            cv.circle(img,(x,y),3,(255,0,0),-1)

        cv.imshow("window", img)

    

    def Activated(self):
        """Do something here"""
        self.fassade = namedtuple("fassade", "src_img corners windows")
        self.fassade.corners = []
        doc=FreeCAD.activeDocument() 
        
        filename = QtGui.QFileDialog().getOpenFileName()[0]

        
        

        # Loading the image
        #img = cv.imread("C:/Users/johan/OneDrive/09_Baurobotik/Code/mycode/Baurobotik/TUM.jpg")
        img = cv.imread(filename)
        if img is None:
            sys.exit("Could not read the image.")

        img = resize_image(img)
        self.fassade.src_img = img

        cv.namedWindow('window')


        cv.setMouseCallback('window', self.draw_circle)
        cv.imshow("window", img)

        # go to next step
        while(1):
            key = cv.waitKeyEx()
            #print(key)
            if key == 110:
                break

        
        cv.setMouseCallback('window',self.empty_method)
        img = self.fassade.src_img.copy()

        if len(self.fassade.corners) != 4:
            sys.exit("Corner size has to be 4")

        for i in range(0, len(self.fassade.corners)):
            j = i+1
            if j >= len(self.fassade.corners):
                j=0

            p1 = self.fassade.corners[i]
            p2 = self.fassade.corners[j]

            x1 = p1[0]
            y1 = p1[1]
            x2 = p2[0]
            y2 = p2[1]
            

            cv.line(img, (x1, y1), (x2, y2), (0,255,0),3)


        cv.imshow("window", img)

        while(1):
            key = cv.waitKeyEx()
            #print(key)
            if key == 110:
                break

        top_left = self.fassade.corners[0]
        top_right = self.fassade.corners[1]
        bot_right = self.fassade.corners[2]
        bot_left = self.fassade.corners[3]


        
        p_h = self.compute_meeting_point_horizontal(top_left, top_right, bot_right, bot_left)
        p_v = self.compute_meeting_point_vertical(top_left, top_right, bot_right, bot_left)


        point = (int(p_h[0]), int(p_h[1]))
        cv.line(img, (top_left[0], top_left[1]), point, (255,255,0),3)
        cv.line(img, (bot_left[0], bot_left[1]), point, (255,255,0),3)

        cv.line(img, (top_left[0], top_left[1]), (int(p_v[0]), int(p_v[1])), (255,255,0),3)
        cv.line(img, (top_right[0], top_right[1]), (int(p_v[0]), int(p_v[1])), (255,255,0),3)

        cv.imshow("window", img)

        doc.recompute()
        return

    def IsActive(self):
        """Here you can define if the command must be active or not (greyed) if certain conditions
        are met or not. This function is optional."""
        return True


    def compute_meeting_point_horizontal(self, top_left, top_right, bot_right, bot_left):
        st = top_left       # s = start, g = gradient, t = top, b = bottom
        gt = top_right - top_left
        sb = bot_left
        gb = bot_right - bot_left


        x = sb[1] * gb[0] + gb[1] * st[0] - sb[0] * gb[1] - st[1] * gb[0]
        x = x / (gt[1] * gb[0] - gb[1] * gt[0])

        intersection = st + gt * x


        string = "Intersection: " + str(intersection[0]) + ", " + str(intersection[1]) + "\n"
        FreeCAD.Console.PrintMessage(string)
        return intersection

    def compute_meeting_point_vertical(self, top_left, top_right, bot_right, bot_left):
        sl = top_left # start left
        gl = top_left - bot_left # gradient left
        sr = top_right # start right
        gr = top_right - bot_right # gradient right


        x = sr[1] * gr[0] + gr[1] * sl[0] - sr[0] * gr[1] - sl[1] * gr[0]
        x = x / (gl[1] * gr[0] - gl[0] * gr[1])

        intersection = x * gl + sl


        string = "Intersection: " + str(intersection[0]) + ", " + str(intersection[1]) + "\n"
        FreeCAD.Console.PrintMessage(string)
        return intersection

FreeCADGui.addCommand('NewFassade',NewFassade())
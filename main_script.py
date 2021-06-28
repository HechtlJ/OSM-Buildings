__author__ = "Johannes Hechtl"
__email__ = "johannes.hechtl@tum.de"
__version__ = "1.0"



from BuildingObject import makeBuilding
from os import read
import FreeCAD, FreeCADGui 
import Part, PartGui 
from PySide import QtGui
import xml.etree.ElementTree as ET
from Map import Map
import cv2 as cv


class MainCommand():
    """This command loads a .osm file and adds 3d models of all buildings to the currently active workspace"""

    def GetResources(self):
        return {'Pixmap'  : 'My_Command_Icon', # the name of a svg file available in the resources
                'Accel' : "Shift+S", # a default shortcut (optional)
                'MenuText': "main command",
                'ToolTip' : "Load .osm file"}

    def Activated(self):
        
        doc=FreeCAD.activeDocument() 
        
        filename = QtGui.QFileDialog().getOpenFileName()[0]

        map = Map(filename)

        doc=FreeCAD.activeDocument() 
        
        # add buildings to FreeCad Document
        for building in map.buildings:
            makeBuilding(building)


        doc.recompute()
        return

    def IsActive(self):
        """Here you can define if the command must be active or not (greyed) if certain conditions
        are met or not. This function is optional."""
        return True

FreeCADGui.addCommand('MainCommand',MainCommand())
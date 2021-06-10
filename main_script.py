from os import read
import FreeCAD, FreeCADGui 
import Part,PartGui 
from PySide import QtGui
#from tr import tr
#from PySide.QtCore import tr
import xml.etree.ElementTree as ET
from osm_reader import read_osm
from Map import Map


class MainCommand():
    """My new command"""

    def GetResources(self):
        return {'Pixmap'  : 'My_Command_Icon', # the name of a svg file available in the resources
                'Accel' : "Shift+S", # a default shortcut (optional)
                'MenuText': "main command",
                'ToolTip' : "What my new command does"}

    def Activated(self):
        """Do something here"""
        doc=FreeCAD.activeDocument() 
        
        #QtGui.QMessageBox.information(None, "Apollo program", "Houston, we have a problem")
        #fileName = QtGui.QFileDialog.getOpenFileName(self, "Open Image", "/home/jana", "")
        #fileName = QtGui.QFileDialog.getOpenFileName(self, "Open Image", "/home", "Image Files (*.png *.jpg *.bmp)")
        #fileIn=open(QtGui.QFileDialog().getOpenFileName()[0],'r')

        filename = QtGui.QFileDialog().getOpenFileName()[0]

        #FreeCAD.Console.PrintMessage(filename)

        #tree = ET.parse(filename)


        #root = tree.getroot()

        #FreeCAD.Console.PrintMessage(root.tag)

        #root[0]
        #read_osm(filename)

        map = Map(filename)

        doc=FreeCAD.activeDocument() 
        

        for building in map.buildings:
            points = building.points

            if len(points)==0:
                #FreeCAD.Console.PrintMessage("Continue Len")
                continue

            start_point = points[0]

            for point in points:
                if point == start_point:
                    #FreeCAD.Console.PrintMessage("Continue equal")
                    continue
                line = Part.LineSegment()
                line.StartPoint = (start_point["x"], start_point["y"], 0)
                line.EndPoint = (point["x"], point["y"], 0)
                doc.addObject("Part::Feature","Line").Shape=line.toShape() 
                start_point = point

            

        doc.recompute()
        return

    def IsActive(self):
        """Here you can define if the command must be active or not (greyed) if certain conditions
        are met or not. This function is optional."""
        return True

FreeCADGui.addCommand('MainCommand',MainCommand())
import FreeCAD, FreeCADGui 
import Part, PartGui 
from BuildingObject import *


class My_Command_Class():
    """My new command"""

    def GetResources(self):
        return {'Pixmap'  : 'My_Command_Icon', # the name of a svg file available in the resources
                'Accel' : "Shift+S", # a default shortcut (optional)
                'MenuText': "My New Command",
                'ToolTip' : "What my new command does"}

    def Activated(self):
        """Do something here"""
        doc=FreeCAD.activeDocument() 
        # add a line element to the document and set its points 
        l=Part.LineSegment()
        l.StartPoint=(0.0,0.0,0.0)
        l.EndPoint=(1.0,1.0,1.0)
        doc.addObject("Part::Feature","Line").Shape=l.toShape() 

        makeBox()

        doc.recompute()
        return

    def IsActive(self):
        """Here you can define if the command must be active or not (greyed) if certain conditions
        are met or not. This function is optional."""
        return True

FreeCADGui.addCommand('My_Command',My_Command_Class())
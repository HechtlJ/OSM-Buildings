"""Command for testing"""

import FreeCAD, FreeCADGui 
import Part, PartGui 
import Draft
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


        length = 2

        v1 = FreeCAD.Vector(0,0,0)
        v2 = FreeCAD.Vector(length,0,0)
        v3 = FreeCAD.Vector(0,length,0)
        v4 = FreeCAD.Vector(length,length,0)
        v5 = FreeCAD.Vector(length/2,length/2,length/2)
        v6 = FreeCAD.Vector(length/2,length/2,-length/2)

        f1 = self.make_face(v2,v1,v5)
        f2 = self.make_face(v4,v2,v5)
        f3 = self.make_face(v3,v4,v5)
        f4 = self.make_face(v1,v3,v5)
        f5 = self.make_face(v1,v2,v6)
        f6 = self.make_face(v2,v4,v6)
        f7 = self.make_face(v4,v3,v6)
        f8 = self.make_face(v3,v1,v6)


        shell=Part.makeShell([f1,f2,f3,f4,f5,f6,f7,f8])
        solid=Part.makeSolid(shell)
        
        doc.addObject("Part::Feature","octagon").Shape=solid



        

        doc.recompute()
        return

    def make_face(self, v1, v2, v3):
        wire = Part.makePolygon([v1,v2,v3,v1])
        face = Part.Face(wire)
        return face

    def IsActive(self):
        """Here you can define if the command must be active or not (greyed) if certain conditions
        are met or not. This function is optional."""
        return True

FreeCADGui.addCommand('My_Command',My_Command_Class())
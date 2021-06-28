""" The code in this file is used to initialize the OSM-Buildings addon with the FreeCAD GUI."""

__author__ = "Johannes Hechtl"
__email__ = "johannes.hechtl@tum.de"
__version__ = "1.0"


import FreeCAD, FreeCADGui 

class ScriptCmd: 
    """Example Class for a simple command."""
    """For every in the GUI selectable command a class has to be written, with at least the two following functions:"""

    def Activated(self): 
        """ This code gets executed when the corresponding button is pressed."""
       
        FreeCAD.Console.PrintMessage('Hello, World!')

    def GetResources(self): 
        """ Return resources for GUI"""
        return {'Pixmap' : 'path_to_an_icon/myicon.png', 'MenuText': 'Short text', 'ToolTip': 'Hello World button.'} 
        # Pixmap is a png icon that is the face of the button.
        # The tooltip gets displayed when hovering over the button
       
# Registering the command with the GUI. This needs to be done before the Workbench is initialized
FreeCADGui.addCommand('Script_Cmd', ScriptCmd())



class OSM_Buildings (Workbench):

    MenuText = "OSM-Buildings"
    ToolTip = "A description of my workbench"
    Icon = "paste here the contents of a 16x16 xpm icon"

    def Initialize(self):
        """This function is executed when FreeCAD starts"""
        #import MyModuleA, MyModuleB # import here all the needed files that create your FreeCAD commands
        
        # if you have command classes in other files, they need to be imported EXACTLY here

        import my_test
        import main_script
        import script_new_fassade

        self.list = ['Script_Cmd', 'My_Command', 'MainCommand', 'NewFassade'] # A list of the command names created
        # commands, that are not listed here, will not show up in the GUI


        self.appendToolbar("My Commands",self.list) # creates a new toolbar with your commands
        self.appendMenu("My New Menu",self.list) # creates a new menu
        self.appendMenu(["An existing Menu","My submenu"],self.list) # appends a submenu to an existing menu

    def Activated(self):
        """This function is executed when the workbench is activated"""
        return

    def Deactivated(self):
        """This function is executed when the workbench is deactivated"""
        return

    def ContextMenu(self, recipient):
        """This is executed whenever the user right-clicks on screen"""
        # "recipient" will be either "view" or "tree"
        self.appendContextMenu("My commands",self.list) # add commands to the context menu

    def GetClassName(self): 
        # This function is mandatory if this is a full python workbench
        # This is not a template, the returned string should be exactly "Gui::PythonWorkbench"
        return "Gui::PythonWorkbench"
       


Gui.addWorkbench(OSM_Buildings())
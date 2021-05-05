import FreeCAD, FreeCADGui 

class ScriptCmd: 
   def Activated(self): 
       # Here your write what your ScriptCmd does...
       FreeCAD.Console.PrintMessage('Hello, World!')
   def GetResources(self): 
       return {'Pixmap' : 'path_to_an_icon/myicon.png', 'MenuText': 'Short text', 'ToolTip': 'More detailed text'} 
       
FreeCADGui.addCommand('Script_Cmd', ScriptCmd())



class OSM_Buildings (Workbench):

    MenuText = "OSM-Buildings"
    ToolTip = "A description of my workbench"
    Icon = """paste here the contents of a 16x16 xpm icon"""

    def Initialize(self):
        """This function is executed when FreeCAD starts"""
        #import MyModuleA, MyModuleB # import here all the needed files that create your FreeCAD commands
        import my_test
        self.list = ['Script_Cmd', 'My_Command'] # A list of command names created in the line above
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
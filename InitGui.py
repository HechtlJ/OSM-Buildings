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
    def Initialize(self):
        #import Scripts # assuming Scripts.py is your module
        list = ['Script_Cmd', 'DemoCommand'] # That list must contain command names, that can be defined in Scripts.py
        self.appendToolbar("My Scripts",list) 

        
Gui.addWorkbench(OSM_Buildings())
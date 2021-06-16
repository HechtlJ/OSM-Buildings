import FreeCAD, FreeCADGui
from pivy import coin
import Part, PartGui

class BuildingObject:
    """This is the class for a custom FreeCadScripted object. This object represents a building."""

    def __init__(self, obj, building):
        '''Add some custom properties to our box feature'''
        
        obj.addProperty('App::PropertyString', 'address', 'BuildingObject', "The adress of the building.").address=building.address
        obj.addProperty('App::PropertyInteger', 'levels', 'BuildingObject', "Number of Levels of the building.").levels=building.levels

        height_vector = FreeCAD.Vector(0, 0, building.height)
        obj.addProperty('App::PropertyVector', 'height', 'BuildingObject', "Height of the building").height=height_vector

        point_vectors_bottom = []

        for point in building.points:
            vector = FreeCAD.Vector(point["x"], point["y"], 0)
            point_vectors_bottom.append(vector)

        obj.addProperty('App::PropertyVectorList', 'corners_bottom', 'BuildingObject', "List of the coordinates of the buildings' bottom corners").corners_bottom=point_vectors_bottom

        point_vectors_top = []
        for top_corner in point_vectors_bottom:
            top_corner = top_corner.add(height_vector)
            point_vectors_top.append(top_corner)

        obj.addProperty('App::PropertyVectorList', 'corners_top', 'BuildingObject', "List of the coordinates of the buildings' top corners").corners_top=point_vectors_top


        obj.addProperty("Part::PropertyPartShape","Shape","BuildingObject", "Shape of the building")

        obj.Proxy = self
   
    def onChanged(self, fp, prop):
        '''Do something when a property has changed'''
        pass


        


 
    def execute(self, fp):
        '''Do something when doing a recomputation, this method is mandatory'''
        if len(fp.corners_bottom) < 3:
            FreeCAD.Console.PrintMessage("Not enough corners" + "\n")
            return


        bottom_face = Part.makePolygon(fp.corners_bottom)

        

        top_face = Part.makePolygon(fp.corners_top)    # the corners have to be a closed loop, this is already the case in the osm data

        faces = []
        faces.append(Part.Face(bottom_face))
        


        """ Now the side faces of the building have to be created. For each face you need four points: the two points on the bottom line (called b1 and b2)
        and the two points on the top line (called t1 and t2)"""
        for i in range(len(fp.corners_bottom)-1):
            b1 = fp.corners_bottom[i]
            b2 = fp.corners_bottom[i+1]

            t1 = fp.corners_top[i]
            t2 = fp.corners_top[i+1]

            face = Part.makePolygon([b1, b2, t2, t1, b1])   # the points have to be a closed loop, therefore b1 again at the end
            faces.append(Part.Face(face))

        faces.append(Part.Face(top_face))
        string = str(faces)
        #FreeCAD.Console.PrintMessage(string + "\n")


        doc=FreeCAD.activeDocument() 
        """for face in faces:
            doc.addObject("Part::Feature","plane").Shape=face"""

        shell = Part.makeShell(faces)   # Combining the surfaces to one Shell

        #doc.addObject("Part::Feature","plane").Shape=shell

        #string = str(shell)
        #FreeCAD.Console.PrintMessage(string + "\n")

        solid = Part.makeSolid(shell)   # Making a solid out of the shell

        fp.Shape = solid
        #doc.addObject("Part::Feature","plane").Shape=solid

        





class ViewProviderBuilding:
    def __init__(self, obj):
        '''Set this object to the proxy object of the actual view provider'''
        obj.addProperty("App::PropertyColor","Color","Box","Color of the box").Color=(1.0,0.0,0.0)
        obj.Proxy = self
 
    def attach(self, obj):
        '''Setup the scene sub-graph of the view provider, this method is mandatory'''
        self.shaded = coin.SoGroup()
        self.wireframe = coin.SoGroup()
        self.color = coin.SoBaseColor()
       
        self.data=coin.SoCoordinate3()
        self.face=coin.SoIndexedFaceSet()

        self.shaded.addChild(self.color)
        self.shaded.addChild(self.data)
        self.shaded.addChild(self.face)
        obj.addDisplayMode(self.shaded,"Shaded");
        style=coin.SoDrawStyle()
        style.style = coin.SoDrawStyle.LINES
        self.wireframe.addChild(style)
        self.wireframe.addChild(self.color)
        self.wireframe.addChild(self.data)
        self.wireframe.addChild(self.face)
        obj.addDisplayMode(self.wireframe,"Wireframe");
        self.onChanged(obj,"Color")

 
    def updateData(self, fp, prop):
        '''If a property of the handled feature has changed we have the chance to handle this here'''
        # fp is the handled feature, prop is the name of the property that has changed

        # see documentation: https://coin3d.github.io/Coin/html/classSoIndexedFaceSet.html


        if prop == "Shape":
            shape = fp.getPropertyByName("Shape")
            
            num_points = len(fp.corners_bottom)
            self.data.point.setNum(num_points*2)


            cnt=0
            for i in fp.corners_bottom:
                self.data.point.set1Value(cnt,i[0],i[1],i[2])
                cnt=cnt+1

            #adding top points
            for i in fp.corners_top:
                self.data.point.set1Value(cnt,i[0],i[1],i[2])
                cnt=cnt+1


            

            

            # adding bottom plane
            cnt = 0
            for i in range(num_points):
                self.face.coordIndex.set1Value(cnt,i)
                cnt = cnt+1

            self.face.coordIndex.set1Value(cnt,-1)
            cnt=cnt+1


            #adding side planes
            for i in range(num_points-1):
                self.face.coordIndex.set1Value(cnt,i+1)
                cnt=cnt+1
                self.face.coordIndex.set1Value(cnt,i)
                cnt=cnt+1
                self.face.coordIndex.set1Value(cnt,i+num_points)
                cnt=cnt+1
                self.face.coordIndex.set1Value(cnt,i+1+num_points)
                cnt=cnt+1
                self.face.coordIndex.set1Value(cnt,-1)
                cnt=cnt+1

            
            #adding top plane
            for i in range(num_points):
                self.face.coordIndex.set1Value(cnt,2*num_points-1-i)    # going counterclockwise, so that the right side of the surface shows
                cnt = cnt+1

            self.face.coordIndex.set1Value(cnt,-1)
            cnt=cnt+1

            





 
    def getDisplayModes(self,obj):
        '''Return a list of display modes.'''
        modes=[]
        modes.append("Shaded")
        modes.append("Wireframe")
        return modes
 
    def getDefaultDisplayMode(self):
        '''Return the name of the default display mode. It must be defined in getDisplayModes.'''
        return "Shaded"
 
    def setDisplayMode(self,mode):
        '''Map the display mode defined in attach with those defined in getDisplayModes.\
                Since they have the same names nothing needs to be done. This method is optional'''
        return mode
 
    def onChanged(self, vp, prop):
        '''Here we can do something when a single property got changed'''
        FreeCAD.Console.PrintMessage("Change property: " + str(prop) + "\n")
        if prop == "Color":
            c = vp.getPropertyByName("Color")
            self.color.rgb.setValue(c[0],c[1],c[2])
 
    def getIcon(self):
        '''Return the icon in XPM format which will appear in the tree view. This method is\
                optional and if not defined a default icon is shown.'''
        return """
            /* XPM */
            static const char * ViewProviderBox_xpm[] = {
            "16 16 6 1",
            "   c None",
            ".  c #141010",
            "+  c #615BD2",
            "@  c #C39D55",
            "#  c #000000",
            "$  c #57C355",
            "        ........",
            "   ......++..+..",
            "   .@@@@.++..++.",
            "   .@@@@.++..++.",
            "   .@@  .++++++.",
            "  ..@@  .++..++.",
            "###@@@@ .++..++.",
            "##$.@@$#.++++++.",
            "#$#$.$$$........",
            "#$$#######      ",
            "#$$#$$$$$#      ",
            "#$$#$$$$$#      ",
            "#$$#$$$$$#      ",
            " #$#$$$$$#      ",
            "  ##$$$$$#      ",
            "   #######      "};
            """
 
    def __getstate__(self):
        '''When saving the document this object gets stored using Python's json module.\
                Since we have some un-serializable parts here -- the Coin stuff -- we must define this method\
                to return a tuple of all serializable objects or None.'''
        return None
 
    def __setstate__(self,state):
        '''When restoring the serialized object from document we have the chance to set some internals here.\
                Since no data were serialized nothing needs to be done here.'''
        return None


def makeBuilding(building):
    doc = FreeCAD.ActiveDocument
    a=FreeCAD.ActiveDocument.addObject("App::FeaturePython","Building")
    BuildingObject(a, building)
    ViewProviderBuilding(a.ViewObject)
    doc.recompute()





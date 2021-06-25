import xml.etree.ElementTree as ET
#from pyproj import Proj
#import utm
import projection
from Building import Building
import FreeCAD

class Map:

    def __init__(self, filename):

        # Loading the file
        tree = ET.parse(filename)
        
        # This is the root of the xml tree.
        root = tree.getroot()

        # placeholder to save all nodes, that are buildings
        building_nodes = []

        # iterate over every node
        for node in tree.iter():
            
            # iterate over every tag in node
            tags = node.findall("tag")
            for tag in tags:
                
                # in the osm file, the attributes that can be 'building' are called 'k'
                # example line:     <tag k="building" v="university"/>

                # getting all 'k' attributes/tags
                attr = tag.attrib
                k_attr = attr.get('k')
                
                # checking if node is building
                if k_attr == "building":

                    # saving the node for later
                    building_nodes.append(node)

        # placeholder for saving dictionaries with the refs to the coordinates to every building. 
        # building_refs[i] is a dictionary with the refs corresponding to buildings[i]
        building_refs = []

        for building_node in building_nodes:
            # under nd are the refs saved in the file
            nds = building_node.findall("nd")
            refs = []
            for nd in nds:
                attr = nd.attrib
                refs.append(attr.get("ref"))
            building_refs.append(refs)


        node_dictionary = {}


        for child in root:
            attr = child.attrib
            id = attr.get("id")
            if id is not None:
                node_dictionary[id] = child

        # in the node_dictionary the combination between a nodes id and the node itself is made


        #print(node_dictionary['539181222'])

        self.buildings = []

        # Zone 32 is advised for the area around munich. If a different part of the world is looked at, the zone needs to be adjusted.
        #projection = Proj(proj='utm',zone=32,ellps='WGS84', preserve_units=False)

        # get reference x and y. The reference is just the first point in the list. a reference point is necessary to center the buildings around the 0 0 0 coordinate
        # this is a dirty solution, but it works
        ref = building_refs[0]
        ref_node = node_dictionary[ref[0]]
        ref_lat = ref_node.attrib.get("lat")
        ref_lon = ref_node.attrib.get("lon")

        ref_lat = float(ref_lat)
        ref_lon = float(ref_lon)

        ref_x, ref_y, zone_number, zone_letter = projection.from_latlon(ref_lat, ref_lon)


        for i in range(len(building_nodes)):
            building = Building()

            #msg = 'Calculating Building ' + str(i)
            #FreeCAD.Console.PrintMessage(msg)

            for ref in building_refs[i]:
                coord_node = node_dictionary[ref]

                lat = coord_node.attrib.get("lat")
                lon = coord_node.attrib.get("lon")

                #x, y = projection(lat, lon)
                lat = float(lat)
                lon = float(lon)

                x, y, zone_number, zone_letter = projection.from_latlon(lat, lon)
                x = x - ref_x
                y = y - ref_y
                building.add_point(x, y)


            street = ""
            housenumber = ""
            postcode = ""
            city = ""

            levels = 3

            for tag in building_nodes[i].findall("tag"):
                attr = tag.attrib
                k_attr = attr.get('k')

                if k_attr == "addr:street":
                    street = attr.get('v')
                elif k_attr == "addr:housenumber":
                    housenumber = attr.get('v')
                elif k_attr == "addr:postcode":
                    postcode = attr.get('v')
                elif k_attr == "addr:city":
                    city = attr.get('v')
                elif k_attr == "building:levels":
                    levels = attr.get('v')


            address = street + " " + housenumber + ", " + postcode + " " + city
            building.set_address(address)
            building.set_levels(levels)
            

            self.buildings.append(building)


        

        
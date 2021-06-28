""" Script for testing the reading of the osm file without the FreeCAD overhang"""


import xml.etree.ElementTree as ET

"""
Todo:
[done] read osm
[done] make list of all buildings
{- remove buildings without coordinates} probably not necessary
- write building class
- make list of buildings
- convert degrees to xyz
- add corners to buildings


"""

# Loading the file
tree = ET.parse("C:/Users/johan/Downloads/map (1).osm")

# This is the root of the xml tree.
root = tree.getroot()

# placeholder to save all nodes, that are buildings
buildings = []

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
            buildings.append(node)

# placeholder for saving dictionaries with the refs to the coordinates to every building. 
# building_refs[i] is a dictionary with the refs corresponding to buildings[i]
building_refs = []

for building in buildings:
    # under nd are the refs saved in the file
    nds = building.findall("nd")
    refs = []
    for nd in nds:
        attr = nd.attrib
        refs.append(attr.get("ref"))
    building_refs.append(refs)


#result = root.findall("./osm/[@id='539181222']")
#print(result)

node_dictionary = {}

#print(root.attrib)

for child in root:
    attr = child.attrib
    id = attr.get("id")
    if id is not None:
        node_dictionary[id] = child

# in the node_dictionary the combination between a nodes id and the node itself is made

print(node_dictionary['539181222'])

# next step: get the longitude and latitude and convert it to cartesian coordinates

coord_node = node_dictionary['539181222']

lat = coord_node.attrib.get("lat")
lon = coord_node.attrib.get("lon")

#print(lat)
#print(lon)

# library: LatLon

from pyproj import Proj

# Zone 32 is advised for t area around munich. If a different part of the world is looked at, the zone needs to be adjusted.
projection = Proj(proj='utm',zone=32,ellps='WGS84', preserve_units=False)

x, y = projection(lat, lon)

#print(x, y)

from Building import Building

building = Building()

building.add_point(x, y)



for ref in building_refs[1]:
    coord_node = node_dictionary[ref]


#print(coord_node.attrib.get("lat"))

for tag in buildings[3].findall("tag"):
    attr = tag.attrib
    k_attr = attr.get('k')

    if k_attr == "addr:street":
        value = attr.get('v')
        print(value)

    #print(attr)




    
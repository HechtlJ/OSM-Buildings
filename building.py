
__author__ = "Johannes Hechtl"
__email__ = "johannes.hechtl@tum.de"
__version__ = "1.0"


HEIGHT_PER_LEVEL = 3    # in meters

class Building:
    """ This class represents a building. It saves all the data of a single building, extracted from the osm file."""

    def __init__(self):
        
        self.points = []    # The corner points of the building. Each point is a dictionary with a x and a y value
        self.address = ""
        self.levels = 3     # self.height MUST BE bigger then 0, therefore self.levels must be positive

        self.height = HEIGHT_PER_LEVEL * self.levels 



    def add_point(self, x, y):
        point = {"x":x, "y":y}
        self.points.append(point)

    def set_address(self, address):
        self.address = address

    def set_levels(self, levels):
        self.levels = int(levels)
        if self.levels < 1:
            self.levels = 1
        self.height = self.levels * HEIGHT_PER_LEVEL


    
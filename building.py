
HEIGHT_PER_LEVEL = 3

class Building:
    """ This class represents a building. It saves all the data of a building."""

    def __init__(self):
        
        self.points = []    # The corner points of the building. Each point is a dictionary with a x and a y value
        self.address = ""
        self.levels = 3 

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


    


class Building:
    """ This class represents a building. It saves all the data of a building."""

    def __init__(self):
        self.height = 0
        self.points = []
        self.address = ""


    def add_point(self, x, y):
        point = {"x":x, "y":y}
        self.points.append(point)

    def set_address(self, address):
        self.address = address


    
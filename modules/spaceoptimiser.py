from shapely.geometry import *

class Optimiser:
    def __init__(self):
        self.width = 2400
        self.height = 1400
        self.edge_offset = 0
        self.hole_offset = 0
        self.holes = []
        self.shape = None
        self.position = [0, 0]
        self.angle = 0

    def setBoardSize(self, dimensions):
        """Sets dimensions of the board as (widht, height)"""
        self.width, self.height = dimensions

    def getBoardSize(self):
        """Returns dimensions of the board as (widht, height)"""
        return (self.width, self.height)

    def getBoardShape(self):
        """Returns coordinates of the board rectangle in counter clocwise
            order, starting from the bottom left
        """
        w = self.width
        h = self.height
        return ((0, 0), (w, 0), (w, h), (0, h), (0, 0))

    def addHole(self, shape):
        """Adds a hole. Expecting a list of points ((x, y), ...)"""
        self.holes.append(Polygon(shape))

    def getHoles(self):
        """Returns the holes as list of lists of points
            [Hole1((x, y), ...), Hole2((x, y), ...)]
        """
        holes = []
        for hole in self.holes:
            holes.append(list(hole.exterior.coords))
        return holes

    def setShape(self, shape):
        """Sets the working shape. Expecting a list of points"""
        self.shape = Polygon(shape)

if __name__ == "__main__":
    opt = Optimiser()
    h = opt.getHoles()
    print(h)
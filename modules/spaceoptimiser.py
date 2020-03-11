from shapely.geometry import *

if __package__ is None or __package__ == '':
    # uses current directory visibility
    from smallestenclosingcircle import make_circle as smallest_circle
else:
    # uses current package visibility
    from .smallestenclosingcircle import make_circle as smallest_circle

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

    def prepare(self):
        _, _, radius = smallest_circle(self.shape.exterior.coords)
        board = Polygon(self.getBoardShape())
        return list(board.buffer(-radius).exterior.coords)

    def step(self):
        pass

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
        """Adds a hole. Expecting a list of points ((x, y), ...)
            If the new hole intersects any existing one, it merges with it"""
        new_hole = Polygon(shape)
        holes_to_remove = []
        for hole in self.holes:
            if new_hole.intersects(hole):
                new_hole = new_hole.union(hole)
                holes_to_remove.append(hole)
        for hole in holes_to_remove:
            self.holes.remove(hole)
        self.holes.append(new_hole)

    def subtractHole(self, shape):
        not_hole = Polygon(shape)
        holes_to_remove = []
        holes_to_add = []
        for hole in self.holes:
            if hole.contains(not_hole):
                return
            if not_hole.contains(hole):
                holes_to_remove.append(hole)
            if not_hole.intersects(hole):
                holes_to_add.append(hole.difference(not_hole))
                holes_to_remove.append(hole)
        for hole in holes_to_remove:
            self.holes.remove(hole)
        for hole in holes_to_add:
            if hasattr(hole, "__getitem__"):
            #if multiple holes result from one subtraction
                for h in hole:
                    self.holes.append(h)    
            else:
                self.holes.append(hole)

    def getHoles(self):
        """Returns the holes as list of lists of points
            [Hole1((x, y), ...), Hole2((x, y), ...)]
        """
        holes = []
        for hole in self.holes:
            holes.append(list(hole.boundary.coords))
        return holes

    def removeHole(self, hole):
        self.holes.remove(hole)

    def queryHole(self, point):
        for hole in self.holes:
            if Point(point[0], point[1]).within(hole):
                return hole
        return None

    def setShape(self, shape):
        """Sets the working shape. Expecting a list of points"""
        self.shape = Polygon(shape)

    def getShape(self):
        return list(self.shape.boundary.coords)

if __name__ == "__main__":
    opt = Optimiser()
    h = opt.getHoles()
    #print(h)
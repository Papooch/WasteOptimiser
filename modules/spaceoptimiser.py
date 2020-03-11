from shapely.geometry import *
from shapely import affinity

if __package__ is None or __package__ == '':
    # uses current directory visibility
    from smallestenclosingcircle import make_circle as smallest_circle
else:
    # uses current package visibility
    from .smallestenclosingcircle import make_circle as smallest_circle

class Optimiser:
    def __init__(self):
        self.width = 2400       # width of the board
        self.height = 1400      # height of the board
        self.edge_offset = 0    # offset from edge of board
        self.hole_offset = 0    # offset from hole
        self.holes = []         # list of hole shapes in the board
        self.shape = None       # shape to be placed
        self.centroid = [0, 0]  # centroid of shape to be placed
        self.position = [0, 0]  # offset position of shape to be placed
        self.angle = 0          # angle (around centroid) of shape to be placed

        self.startpolygons = [] # lsit of possible starting polygons (polygons along which boundaries to start optimisation)

    def init_startpoly(self):
        _, _, radius = smallest_circle(self.shape.exterior.coords)

        dilatedboard = Polygon(self.getBoardShape()).buffer(-radius)
        dilatedholes = [hole.buffer(radius) for hole in self.holes]
        dpolygon = dilatedboard
        for dhole in dilatedholes:
            dpolygon = dpolygon.difference(dhole)
        self.startpolygons = []
        if hasattr(dpolygon, "__getitem__"):
        #if multiple holes result from one subtraction
            for dpoly in dpolygon:
                self.startpolygons.append(dpoly)    
        else:
            self.startpolygons.append(dpolygon)
        
        self.startpolygons.sort(key= lambda x: x.area)
        
        retpoly = []
        for stp in self.startpolygons:
            retpoly.append(list(stp.exterior.coords))
        return retpoly

    def add_startpoly(self):
        pass

    def begin(self):
        beginpoly = self.startpolygons[0]
        beginpoint = list(beginpoly.exterior.coords[0])
        self.position = beginpoint
        print(self.position)

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
        self.centroid = self.shape.centroid

    def getShape(self):
        return list(self.shape.boundary.coords)

    def getShapeOriented(self):
        rotated = affinity.rotate(self.shape, self.angle, origin='centroid')
        translatedrotated = affinity.translate(rotated, self.position[0], self.position[1])
        return list(translatedrotated.boundary.coords)

    def getShapeDilated(self):
        pass

if __name__ == "__main__":
    opt = Optimiser()
    h = opt.getHoles()
    #print(h)
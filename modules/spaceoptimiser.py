from shapely.geometry import *
from shapely.geometry.polygon import orient
from shapely import affinity

if __package__ is None or __package__ == '':
    # uses current directory visibility
    from smallestenclosingcircle import make_circle as smallest_circle
    from libnfporb_interface import genNFP
else:
    # uses current package visibility
    from .smallestenclosingcircle import make_circle as smallest_circle
    from .libnfporb_interface import genNFP

class Optimiser:
    def __init__(self):
        self.width = 2400       # width of the board
        self.height = 1400      # height of the board
        self.edge_offset = 0    # offset from edge of board
        self.hole_offset = 0    # offset from hole
        self.holes = []         # list of hole shapes in the board
        self.shape = None       # shape to be placed
        self.centroid = [0, 0]  # centroid of shape to be placed
        self.circle_center = [0, 0] # center of smallest enclosing circle of shape
        self.circle_radius = 0  # radius of smallest enclosing circle of shape
        self.position = [0, 0]  # offset position of shape to be placed
        self.angle = 0          # angle (around centroid) of shape to be placed

        self.startpolygons = [] # lsit of possible starting polygons (polygons along which boundaries to start optimisation)

    def init_startpoly(self, nfp=True):
        dilatedboard = Polygon(self.getBoardShape()).buffer(-self.circle_radius)
        dilatedholes = []
        if not nfp:
            dilatedholes = [hole.buffer(self.circle_radius + self.hole_offset) for hole in self.holes]
        else: #if yes nfp
            for hole in self.holes:
                shapepoints = list(orient(self.shape.convex_hull.buffer(self.hole_offset, resolution=2)).exterior.coords)
                holepoints = list(orient(hole.simplify(1)).exterior.coords)
                holepoints[0] = (round(holepoints[0][0],2), round(holepoints[0][1],2))
                holepoints[-1] = (round(holepoints[-1][0],2), round(holepoints[-1][1],2)) 
                trans = [- shapepoints[0][0], - shapepoints[0][1]]
                try:
                    nfps = genNFP(holepoints, shapepoints)
                except:
                    pass
                dilatedholes.append(affinity.translate(Polygon(nfps[0], nfps[1:]), trans[0], trans[1]))

        dpolygon = dilatedboard
        for dhole in dilatedholes:
            dpolygon = dpolygon.difference(dhole).simplify(1)
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
            for inner in stp.interiors:
                retpoly.append(list(inner.coords))
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

    def addShapeAsHole(self):
        self.addHole(self.getShapeOriented())

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
        new_hole = orient(Polygon(shape))
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
        self.shape = orient(Polygon(shape).simplify(1))
        *self.circle_center, self.circle_radius = smallest_circle(self.shape.exterior.coords) # [x, y, r]
        self.shape = affinity.translate(self.shape, -self.circle_center[0], -self.circle_center[1])
        centroid = self.shape.centroid
        self.centroid = [centroid.x, centroid.y]

    def getShape(self):
        return list(affinity.translate(self.shape, self.circle_center[0], self.circle_center[1]).boundary.coords)

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
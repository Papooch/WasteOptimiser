import os
import json
from collections import defaultdict
import numpy as np

from wasteoptimiser.parser import gcodeparser
from wasteoptimiser.optimiser import spaceoptimiser
from wasteoptimiser.optimiser.localsearch import LocalSearch


class Settings():
    width = 100
    height = 100
    edge_offset = 0
    hole_offset = 0
    location = 'tl'
    input_path = None
    use_nfp = True
    nfp_rotations = 1
    local_optimisation = True


class Api():
    def __init__(self, logger=None):
        self.settings = Settings()
        self.logger = logger
        self.figure_preview   = None
        self.figure_workspace = None
        self.optimiser = spaceoptimiser.Optimiser(logger)
        self.selected_shape_name = None
        self.shape_dict = defaultdict()
            # key: filename, value: {'count': count, 'shape': shape, 'convex': bool}}

        self.stop_flag = False
        self.num_shapes_to_place = 0
        self.num_placed_shapes = 0

    def placeSelectedShape(self):
        if not self.selected_shape_name: return None# TODO: error code
        if self.getSelectedShapeCount() == 0: return None# TODO: error code
        self.optimiser.setShape(self.getSelectedShape()[-1])
        self.optimiser.convex_hull = self.isSelectedShapeConvex()

        if self.settings.use_nfp:

            if self.optimiser.preffered_pos == 0: # top left
                pref = lambda p: -p[0] + p[1]
            if self.optimiser.preffered_pos == 1: # top right
                pref = lambda p: p[0] + p[1]
            if self.optimiser.preffered_pos == 2: # bottom left
                pref = lambda p: -p[0] - p[1]
            if self.optimiser.preffered_pos == 3: # bottom right
                pref = lambda p: p[0] - p[1]
            if self.optimiser.preffered_pos == 4: # Left
                pref = lambda p: -p[0]
            if self.optimiser.preffered_pos == 5: # Right
                pref = lambda p: p[0]

            angles = list(np.linspace(0, 360, self.settings.nfp_rotations, endpoint=False))
            angles.append(self.optimiser.angle)
            start_points = []
            start_angles = []
            for angle in angles:
                self.optimiser.angle = angle
                self.optimiser.initStartpoly(nfp = True)
                if self.optimiser.begin():
                    print("angle ok: ", angle)
                    start_points.append(self.optimiser.position)
                    start_angles.append(angle)

            print(start_points)
            if not start_points:
                return False# TODO: error code
            max_index, max_value = max(enumerate(start_points), key=lambda p: pref(p[1]))
            print("index: ", max_index, "value: ", max_value)
            self.optimiser.position = max_value
            self.optimiser.angle = start_angles[max_index]
            print("chosen angle: ", self.optimiser.angle)
        else:
            self.optimiser.initStartpoly(nfp = False)
            if not self.optimiser.begin(): return False# TODO: error code

        if self.settings.local_optimisation:
            g_search = LocalSearch(self.optimiser.shape,
                self.optimiser.position,
                self.optimiser.angle,
                self.optimiser.circle_radius,
                self.optimiser.holes,
                self.optimiser.getBoardShape(),
                self.optimiser.hole_offset,
                self.optimiser.edge_offset)
            while g_search.fail_counter < 3:
                g_search.step()
                self.optimiser.position = g_search.offset
                self.optimiser.angle = g_search.angle

        self.optimiser.addShapeAsHole(self.selected_shape_name)
        return True

    def placeAllSelectedShapes(self):
        self.num_shapes_to_place = self.getAllShapesCount()
        self.num_placed_shapes = 0
        shapes_sorted = sorted(
            self.shape_dict.keys(),
            key= lambda k: self.optimiser.getArea(self.shape_dict[k]['shape'][-1]),
            reverse=True) # names of shapes sorted by area, descending
        for shape in shapes_sorted:
            self.selected_shape_name = shape
            for _ in range(self.shape_dict[shape]['count']):
                if self.stop_flag:
                    print("halted by user")
                    return
                if not self.placeSelectedShape():
                    print("no more", self.selected_shape_name, "can be placed")
                    break
                self.num_placed_shapes += 1
                print(self.selected_shape_name, "placed (", self.num_placed_shapes, "/", self.num_shapes_to_place, ")")

    def stopPlacing(self):
        self.stop_flag = True

    def getAllShapesCount(self):
        return sum([l['count'] for l in list(self.shape_dict.values())])

    def getSelectedShapeCount(self):
        return self.shape_dict[self.selected_shape_name]['count']

    def isSelectedShapeConvex(self):
        return self.shape_dict[self.selected_shape_name]['convex']

    def getSelectedShape(self):
        return self.shape_dict[self.selected_shape_name]['shape']

    def setShapeCount(self, shape, count):
        self.shape_dict[shape]['count'] = count

    def setShapeConvex(self, shape, convex):
        print(shape + " convex: " + str(convex))
        self.shape_dict[shape]['convex'] = bool(convex)


    def constructShapeList(self, folder = None):
        """Constructs shape_dict"""
        self.shape_dict.clear()
        for filename in self.getGcodes(folder):
            shape = self.getShapesFromGcode(os.path.join(folder, filename))
            if shape:
                self.shape_dict[filename] = {'count': 0, 'shape': shape, 'convex' : True}


    def getGcodes(self, folder = None):
        """Returns a list of filenames from the given folder"""

        if not folder: folder = self.settings.input_path
        gcode_files = []
        for item in os.listdir(folder):
            if os.path.isfile(os.path.join(folder, item)):
                gcode_files.append(item)
        return gcode_files


    def getShapeDimensions(self, shapes = None):
        """Returns a tuple (w, h) containing the width and height of the last shape in the list
            (because the biggest shape is usually cut out last)
        """
        if not shapes: shapes = self.getSelectedShape()
        x, y = zip(*shapes[-1])
        return (max(x)-min(x), max(y)-min(y))


    def getShapesFromGcode(self, file, axes = None):
        """Returns a list of shapes [Shape1[...], Shape2[...]] or an empty list
            if no shapes were found in the given file
        """
        gcode = None
        try:
            with open(file, 'r') as f:
                gcode = f.read()
            if gcode:
                xtr = gcodeparser.ShapeExtractor(gcode, suppressLeadIn=True, logger=self.logger)
                xtr.run()
        except:
            self.logger.log(f'{os.path.basename(file)} is not a valid NC program', self.logger.logLevel.WARNING, self.logger.logType.PARSER)
            return []

        shapes = xtr.get_shapes()
        return shapes


    def saveWorkspace(self, file):
        """Saves the current optimiser workspace configuration to file"""

        outw = {'width'   : self.optimiser.width,
                'height'  : self.optimiser.height,
                'holes'   : self.optimiser.getHoles(),
                'h_offset': self.optimiser.hole_offset,
                'e_offset': self.optimiser.edge_offset
        }
        with open(file, "w") as outfile:
            json.dump(outw, outfile)


    def loadWorkspace(self, file):
        """Loads optimiser workspace configuration from file"""

        inw = ()
        with open(file, "r") as infile:
            inw = json.load(infile)
        self.optimiser.__init__(self.logger)
        self.optimiser.width = inw['width']
        self.optimiser.height = inw['height']
        for hole in inw['holes']:
            self.optimiser.addHole(hole)
        self.optimiser.hole_offset = inw['h_offset']
        self.optimiser.edge_offset = inw['e_offset']





if __name__ == "__main__":
    #api = Api()
    from __main__ import *





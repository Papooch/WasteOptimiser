import numpy as np
import os
import pickle
import json
from collections import defaultdict

import modules.gcodeparser
import modules.spaceoptimiser

class Settings():
    width = 100
    height = 100
    edge_offset = 0
    hole_offset = 0
    location = 'tl'
    input_path = None
    use_nfp = True
    local_optimisation = True


class Api():
    def __init__(self):
        self.settings = Settings()
        self.logger = None
        self.figure_preview   = None
        self.figure_workspace = None
        self.optimiser = modules.spaceoptimiser.Optimiser()
        self.selected_shape_name = None
        self.shape_dict = defaultdict() # key: filename, value: {'count': count, 'shape': shape}}
        
        self.stop_flag = False

    def placeSelectedShape(self):
        if not self.selected_shape_name: return None# TODO: error code
        if self.getSelectedShapeCount() == 0: return None# TODO: error code
        self.optimiser.setShape(self.getSelectedShape()[-1])
        self.optimiser.initStartpoly(self.settings.use_nfp)
        if not self.optimiser.begin(): return False# TODO: error code
        self.optimiser.addShapeAsHole(self.selected_shape_name)
        print(self.selected_shape_name, "placed")
        return True
    
    def placeAllSelectedShapes(self):
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
                self.placeSelectedShape()

    def stopPlacing(self):
        self.stop_flag = True

    def getSelectedShapeCount(self):
        return self.shape_dict[self.selected_shape_name]['count']


    def getSelectedShape(self):
        return self.shape_dict[self.selected_shape_name]['shape']


    def setShapeCount(self, shape, count):
        self.shape_dict[shape]['count'] = count


    def constructShapeList(self, folder = None):
        """Constructs shape_dict"""
        self.shape_dict.clear()
        for filename in self.getGcodes(folder):
            shape = self.getShapesFromGcode(os.path.join(folder, filename))
            if shape:
                self.shape_dict[filename] = {'count': 0, 'shape': shape}


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
                xtr = modules.gcodeparser.ShapeExtractor(gcode, suppressLeadIn=True)
                xtr.run()
        except:
            print('nope')
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
        self.optimiser.__init__()
        self.optimiser.width = inw['width']
        self.optimiser.height = inw['height']
        for hole in inw['holes']:
            self.optimiser.addHole(hole)
        self.optimiser.hole_offset = inw['h_offset']
        self.optimiser.edge_offset = inw['e_offset']
        




if __name__ == "__main__":
    #api = Api()
    from __main__ import *





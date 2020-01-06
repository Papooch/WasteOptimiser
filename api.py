import numpy as np
import os

import modules.gcodeparser
import modules.spaceoptimiser

class Settings():
    width = 100
    height = 100
    edge_offset = 0
    hole_offset = 0
    location = 'tl'
    input_path = None

class Api():
    def __init__(self):
        self.settings = Settings()
        self.logger = None
        self.figure_preview   = None
        self.figure_workspace = None
        self.optimiser = modules.spaceoptimiser.Optimiser()
        self.selected_shape = None

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

        if not shapes: shapes = self.selected_shape
        x, y = zip(*shapes[-1])
        return (max(x)-min(x), max(y)-min(y))

    def getShapesFromGcode(self, file, axes = None):
        """Returns a list of shapes [Shape1[...], Shape2[...]] or an empty list
            if no shapes were found in the given file
            #TODO: deprecate
            If passed a pyplot axes, draws the found shapes
        """
        gcode = None
        with open(file, 'r') as f:
            gcode = f.read()
        if gcode:
            xtr = modules.gcodeparser.ShapeExtractor(gcode, suppressLeadIn=True)
            xtr.run()

        shapes = xtr.get_shapes()
        if axes:
            for shape in reversed(xtr.get_shapes()):
                x, y = zip(*shape)
                axes.plot(x, y)
        return shapes


if __name__ == "__main__":
    #api = Api()
    from main import *





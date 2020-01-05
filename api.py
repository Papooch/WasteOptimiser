import numpy as np

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
        self.figurePreview   = None
        self.figureWorkspace = None
        self.ShapeExtractor = modules.gcodeparser.ShapeExtractor

    def parseGcode(self, file, axes = None):
        gcode = None
        with open(file, 'r') as f:
            gcode = f.read()
        if gcode:
            xtr = self.ShapeExtractor(gcode)
            xtr.supressLeadIn = True
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
    



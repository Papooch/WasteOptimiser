import numpy as np
from matplotlib.figure import Figure
import warnings
warnings.filterwarnings("ignore", message="tight_layout : falling back to Agg renderer")

class Figures():
    def __init__(self):
        self.figure = Figure()
        self.ax = self.figure.add_subplot(111)
        self.ax.tick_params(
            axis='both',
            which='both',
            bottom = False,
            left = False,
            labelbottom = False,
            labelleft = False
        )
        self.figure.tight_layout(pad=0)
        self.ax.axis('equal')
        self.ax.clear()
    
    def clear(self):
        self.ax.clear()

    def drawShapes(self, shapes, options = '-k', fill=None, gid = None):
        for shape in reversed(shapes):
            self.draw(shape, options, fill=fill, gid=gid)

    def draw(self, points, options = '-k', fill=None, gid = None):
        try:
            if fill is not None:
                self.ax.fill(*zip(*points), fill, gid=gid)
            self.ax.plot(*zip(*points), options, gid=gid)
        except:
            self.ax.plot(points[0], points[1], options, gid=gid)

    def remove(self, gid):
        for c in self.ax.lines:
            if c.get_gid() == gid:
                c.remove()


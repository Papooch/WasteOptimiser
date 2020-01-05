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

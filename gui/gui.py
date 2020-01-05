from PyQt5.uic import loadUiType
from PyQt5 import QtCore, QtGui, QtWidgets

from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)

import os
Ui_MainWindow, QMainWindow = loadUiType(os.path.join(os.path.dirname(__file__), 'WasteOptimiserGUI.ui'))

class MainWindow(Ui_MainWindow, QMainWindow):
    def __init__(self, api):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.api = api

    def setupCanvases(self, fPreview, fWorkspace):
        self.canvasPreview = FigureCanvas(fPreview)
        self.mplPreviewLayout.addWidget(self.canvasPreview)
        self.canvasPreview.draw()
        
        self.canvasWorkspace = FigureCanvas(fWorkspace)
        self.mplWorkspaceLayout.addWidget(self.canvasWorkspace)
        self.canvasWorkspace.draw()

    def test(self):
        self.api.figurePreview.ax.clear()
        self.api.parseGcode('../../gcode/2-drzak.gcode', axes = self.api.figurePreview.ax)
        self.canvasPreview.draw()

    def setupCallbacks(self):
        self.pb_input_browse.clicked.connect(self.test)
        print('Connected')
        

if __name__ == "__main__":
    # import sys

    # import figures
    # figurePreview = figures.Figures()
    # figureWorkspace = figures.Figures()

    # app = QtWidgets.QApplication(sys.argv)
    # mainWindow = MainWindow(None)
    # mainWindow.setupCanvases(figurePreview.figure, figureWorkspace.figure)
    # mainWindow.setupCallbacks()
    # mainWindow.show()

    # sys.exit(app.exec_())
    import sys 
    sys.path.append('...')
    from main import *
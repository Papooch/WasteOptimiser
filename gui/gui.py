from PyQt5.uic import loadUiType
from PyQt5 import QtCore, QtGui, QtWidgets

from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)

import os
Ui_MainWindow, QMainWindow = loadUiType(os.path.join(os.path.dirname(__file__), 'WasteOptimiserGUI.ui'))

def clamp(val, minv, maxv):
    return min(maxv, max(val, minv))

class MainWindow(Ui_MainWindow, QMainWindow):
    def __init__(self, api):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.api = api
        self.drawing_mode = False
        self.drawn_shape = []
        self.first_point = ()
        self.last_point = ()
        self.close_to_last = False
        self.drawn_shape_handle = None

    ## FUNCTIONS ##
    def openFolder(self, folder):
        """Displays files from the given folder in list"""

        self.api.settings.input_path = folder
        items = self.api.getGcodes(self.api.settings.input_path)
        self.lb_input_path.setText('...' + folder[-20:])
        self.lw_input_list.clear()
        self.lw_input_list.addItems(items)

    ## CALLBACKS ##
    def askFolder(self):
        """Opens a select folder dialog and then displays files from that folder"""

        folder = QtWidgets.QFileDialog.getExistingDirectory(self,"Select folder", '../../')
        self.openFolder(folder)
    
    def selectAndDrawShape(self, name):
        """Sets the clicked shape as selected and draws it to the preview figure"""

        self.figure_preview.clear()
        self.lb_preview_info.setText("Loading...")
        shapes = self.api.getShapesFromGcode(self.api.settings.input_path + '/' + name.text())

        if len(shapes)==0:
            self.api.selected_shape = None
            self.lb_preview_info.setText("Invalid gcode file")
        else:
            self.api.selected_shape = shapes
            self.figure_preview.drawShapes(shapes)
            self.figure_preview.draw([[0, 0]], 'r+')
            dimensions = self.api.getShapeDimensions()
            self.lb_preview_info.setText("Dimensions: " + str(round(dimensions[0],3)) + " x " + str(round(dimensions[1], 3)) + " mm")
        self.canvasPreview.draw()

    def applySettings(self):
        """Applies settings to the optimiser module"""

        self.api.optimiser.setBoardSize((self.sb_settings_width.value(), self.sb_settings_height.value()))
        self.api.optimiser.hole_offset = self.sb_settings_hole_offset.value()
        self.api.optimiser.edge_offset = self.sb_settings_edge_offset.value()
        self.drawWorkspace()

    def drawShapeInWorkspace(self):
        if not self.api.selected_shape: return
        self.figure_workspace.drawShapes(self.api.selected_shape)
        self.canvasWorkspace.draw()


    def drawWorkspace(self):
        """Draws everything into workspace"""

        self.figure_workspace.clear()
        self.figure_workspace.draw(self.api.optimiser.getBoardShape())
        holes = self.api.optimiser.getHoles()
        if holes:
            self.figure_workspace.drawShapes(holes, options='b-')
        self.canvasWorkspace.draw()

    def startDrawing(self):
        self.drawing_mode = True
        self.drawn_shape = []
        self.last_point = ()
        self.first_point = ()

    def stopDrawing(self):
        self.drawing_mode = False
        self.figure_workspace.remove('last')
        self.figure_workspace.remove('temp')
        self.figure_workspace.remove('new_shape')
        self.figure_workspace.remove('first_point')

    def cancelShape(self):
        self.stopDrawing()
        self.canvasWorkspace.draw()

    def finishShape(self):
        self.stopDrawing()
        self.drawn_shape.append(self.first_point)
        self.api.optimiser.addHole(self.drawn_shape)
        self.figure_workspace.drawShapes(self.api.optimiser.getHoles(), 'b-')
        self.canvasWorkspace.draw()

    def workspaceMouseMotion(self, event):
        self.lb_workspace_info.setText(str(event.xdata) + " " + str(event.ydata) + " " + str(event.button))
        if self.drawing_mode:
            x = clamp(event.xdata, 0, self.api.optimiser.width)
            y = clamp(event.ydata, 0, self.api.optimiser.height)
            self.figure_workspace.remove('temp')
            if not self.first_point:
                self.figure_workspace.draw((x, y), options='r+', gid = 'temp')
            else:
                self.figure_workspace.draw((self.last_point, (x, y)), options='b--', gid = 'temp')
                self.figure_workspace.remove('last')
                if abs(x-self.first_point[0])<50 and abs(y-self.first_point[1])<50:
                    self.close_to_last = True
                    self.figure_workspace.draw((x, y), options='ro', gid = 'last')
                else:
                    self.close_to_last = False

            self.canvasWorkspace.draw()

    def workspaceMouseClicked(self, event):
        if self.drawing_mode:
            x = clamp(event.xdata, 0, self.api.optimiser.width)
            y = clamp(event.ydata, 0, self.api.optimiser.height)
            if event.button == 1: # left mouse button
                self.figure_workspace.remove('new_shape')
                if not self.first_point:
                    self.first_point = (x, y)
                    self.figure_workspace.draw(self.first_point, 'ro', gid='first_point')
                if self.close_to_last:
                    self.finishShape()
                    return
                else:
                    self.last_point = (x, y)
                    self.drawn_shape.append(self.last_point)
                    self.figure_workspace.draw(self.drawn_shape, gid = 'new_shape')
                    self.canvasWorkspace.draw()
            elif event.button == 3: # right mouse button
                self.cancelShape()


    ## SETUP ##
    def setupCanvases(self, fPreview, fWorkspace):
        self.figure_preview = fPreview
        self.canvasPreview = FigureCanvas(fPreview.figure)
        self.mplPreviewLayout.addWidget(self.canvasPreview)
        self.canvasPreview.draw()
        self.figure_workspace = fWorkspace
        self.canvasWorkspace = FigureCanvas(fWorkspace.figure)
        self.mplWorkspaceLayout.addWidget(self.canvasWorkspace)
        self.canvasWorkspace.draw()

    def setupCallbacks(self):
        # select gcode folder
        self.pb_input_browse.clicked.connect(self.askFolder)
        # shape in list clicked
        self.lw_input_list.itemClicked.connect(self.selectAndDrawShape)
        # appy settings
        self.pb_settings_apply.clicked.connect(self.applySettings)

        self.pb_workspace_add.clicked.connect(self.startDrawing)

        # workspace figure callback
        self.canvasWorkspace.mpl_connect('motion_notify_event', self.workspaceMouseMotion)
        self.canvasWorkspace.mpl_connect('button_press_event', self.workspaceMouseClicked)

        

if __name__ == "__main__":
    # import sys

    # import figures
    # figure_preview = figures.Figures()
    # figure_workspace = figures.Figures()

    # app = QtWidgets.QApplication(sys.argv)
    # mainWindow = MainWindow(None)
    # mainWindow.setupCanvases(figure_preview.figure, figure_workspace.figure)
    # mainWindow.setupCallbacks()
    # mainWindow.show()

    # sys.exit(app.exec_())
    import sys 
    sys.path.append('...')
    from main import *
import sys
from PyQt5 import QtWidgets, QtCore

from wasteoptimiser.api import api
from wasteoptimiser.gui import figures, gui

# create api object
wo = api.Api()

# create figures
wo.figurePreview    = figures.Figures()
wo.figureWorkspace  = figures.Figures()

show_gui = True
if show_gui:
    # create main gui window
    qtgui = QtWidgets.QApplication(sys.argv)
    mainWindow = gui.MainWindow(wo)

    # attach figures to gui
    mainWindow.setupCanvases(wo.figurePreview, wo.figureWorkspace)
    mainWindow.setupCallbacks()
    mainWindow.show()

    # fast startup stuff
    mainWindow.openFolder('D:\Ondra\Stuff\OneDrive\VUT\DP\moje\gcode')
    mainWindow.applySettings()

    sys.exit(qtgui.exec_())
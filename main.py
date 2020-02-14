import api
import gui.figures, gui.gui

from PyQt5 import QtWidgets, QtCore

import sys

# create api object
wo = api.Api()

# create figures
wo.figurePreview    = gui.figures.Figures()
wo.figureWorkspace  = gui.figures.Figures()

show_gui = True
if show_gui:
    # create main gui window
    qtgui = QtWidgets.QApplication(sys.argv)
    mainWindow = gui.gui.MainWindow(wo)

    # attach figures to gui
    mainWindow.setupCanvases(wo.figurePreview, wo.figureWorkspace)
    mainWindow.setupCallbacks()
    mainWindow.show()

    # fast startup stuff
    mainWindow.openFolder('D:\Ondra\Stuff\OneDrive\VUT\DP\moje\gcode')
    mainWindow.applySettings()

    sys.exit(qtgui.exec_())
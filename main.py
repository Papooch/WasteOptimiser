import api
import gui.figures, gui.gui

from PyQt5 import QtWidgets, QtCore

import sys
qtgui = QtWidgets.QApplication(sys.argv)

# create api object
wo = api.Api()

# create figures
wo.figurePreview    = gui.figures.Figures()
wo.figureWorkspace  = gui.figures.Figures()

# create main gui window
mainWindow = gui.gui.MainWindow(wo)

# attach figures to gui
mainWindow.setupCanvases(wo.figurePreview.figure, wo.figureWorkspace.figure)
mainWindow.setupCallbacks()
mainWindow.show()

sys.exit(qtgui.exec_())
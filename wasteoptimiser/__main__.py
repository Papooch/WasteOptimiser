import sys
from PyQt5 import QtWidgets, QtCore

from wasteoptimiser.api import api
from wasteoptimiser.gui import figures, gui
from wasteoptimiser.logger.logger import Logger

logger = Logger("logs", Logger.logLevel.INFO, Logger.logLevel.DEBUG)

# create api object
wo = api.Api(logger)

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

    #logger.setPrintFunction(TODO:)

    # fast startup stuff
    try:
        mainWindow.openFolder('./shapes')
    except:
        pass
    mainWindow.applySettings()

    sys.exit(qtgui.exec_())
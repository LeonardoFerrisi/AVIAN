# AVIAN version 0.8
# Leonardo Ferrisi
# Union College 2021

# With special thanks to Dr. Timothy George

from avian_main_gui import AVIAN_MainWindow
from PyQt5 import QtWidgets
from pyqtgraph.Qt import QtGui

if __name__ == "__main__":
    app = QtGui.QApplication([])
    AVIAN_GUI = QtWidgets.QMainWindow()
    ui = AVIAN_MainWindow()
    ui.setupUi(AVIAN_GUI, app)
    AVIAN_GUI.show()
    QtGui.QApplication.instance().exec_()

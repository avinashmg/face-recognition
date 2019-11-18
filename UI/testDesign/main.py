# This Python file uses the following encoding: utf-8
import sys

from PySide2 import QtCore
from PySide2.QtCore import QFile
from PySide2.QtWidgets import QApplication
from PySide2.QtUiTools import QUiLoader


if __name__ == "__main__":
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    app = QApplication([])
    ui_file = QFile("mainwindow.ui")
    ui_file.open(QFile.ReadOnly)

    loader = QUiLoader()
    window = loader.load(ui_file)
    window.show()
    # ...
    sys.exit(app.exec_())

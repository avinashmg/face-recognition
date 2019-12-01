# This Python file uses the following encoding: utf-8
import sys
import threading
from time import sleep

from PySide2.QtGui import QPixmap, QCloseEvent
from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2.QtCore import Qt
from ui_mainwindow import Ui_MainWindow
from videoController import VideoController

def threaded(fn):
    def wrapper(*args, **kwargs):
        threading.Thread(target=fn, args=args, kwargs=kwargs).start()
    return wrapper

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.threadFlag = True
        self.updateFrame()

    @threaded
    def updateFrame(self):
        while self.threadFlag:
            qtImg = videoController.nextQtFrame()
            pixmap = QPixmap(qtImg)
            self.ui.imgDisplayLabel.setPixmap(
                pixmap.scaled(self.ui.imgDisplayLabel.size(),
                              Qt.KeepAspectRatio,
                              Qt.SmoothTransformation
                              )
            )
        return

    def closeEvent(self, event:QCloseEvent):
        # Closing the video capture thread
        videoController.threadFlag =False
        self.threadFlag = False
        super(MainWindow, self).closeEvent(event)
        app.exit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(True)
    videoController = VideoController()
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
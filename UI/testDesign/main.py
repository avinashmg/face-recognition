# This Python file uses the following encoding: utf-8
import sys
import threading
import time
import json
from time import sleep

from PySide2.QtGui import QPixmap, QCloseEvent, QImage
from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2.QtCore import Qt, QTimer, SIGNAL, QThread, QObject, Signal, Slot
from ui_mainwindow import Ui_MainWindow
from videoController import VideoController
import faulthandler
import dblink as db
faulthandler.enable()

class UpdateThread(QThread):
    sendPixmap = Signal(QImage, int, str)
    def __init__(self, parent):
        super(UpdateThread, self).__init__(parent)
        self.parent = parent
        self.sendPixmap.connect(parent.receiveFrame)

    def run(self):
        print("[OBJECT] UpdateThread run")
        self.counter = 0
        while self.parent.threadFlag:
            self.counter = self.counter + 1
            print("[INFO] Processing")
            start = time.time()
            if self.counter%self.parent.modeVariable == 0:
                qtImg, sNo, key = videoController.nextQtFrame()
                self.parent.transmitStartTime = time.time()
                self.sendPixmap.emit(qtImg, sNo, key)
            end = time.time()
            print("Time taken for processing: ", end - start)
        print("[INFO] update frame finished")

class MainWindow(QMainWindow):
    def __init__(self):
        print("Initialising Main Window")
        start = time.time()
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.responsiveModeRadioButton.toggled.connect(self.modeChanged)
        self.ui.hibernateModeRadioButton.toggled.connect(self.modeChanged)
        self.ui.realTimeModerRadioButton.toggled.connect(self.modeChanged)
        self.ui.lineEdit.textEdited.connect(self.searchIt)
        self.modeVariable = 1
        self.threadFlag = True
        self.thread = UpdateThread(self)
        self.thread.start()
        end = time.time()
        print("Time taken: ",end - start)

    # Status: Complete
    def searchIt(self):
        keyword = self.ui.lineEdit.text()
        result = json.loads(db.search_person(keyword))
        self.ui.listWidget.clear()
        for person in result:
            self.ui.listWidget.addItem(person["personName"])

    def modeChanged(self):
        if self.ui.responsiveModeRadioButton.isChecked() == True:
            print("Responsive Mode Button pressed!----------------------------------")
            if self.thread.isRunning() == False:
                print("[INFO] Starting thread again")
                self.threadFlag = True
                self.thread.start()
            self.modeVariable = 5
        elif self.ui.hibernateModeRadioButton.isChecked() == True:
            print("Hibernate Mode Button pressed!-----------------------------------")
            self.threadFlag = False
            self.thread.exit()
        elif self.ui.realTimeModerRadioButton.isChecked() == True:
            print("Realtime Mode Button pressed!------------------------------------")
            if self.thread.isRunning() == False:
                self.threadFlag = True
                print("[INFO] Starting thread again")
                self.thread.start()
            self.modeVariable = 1
        elif self.ui.lineEdit.focusOutEvent== True:
            print("Search keyword updated")
        else:
            print("[ERROR] Unknown error!")
        print("[INFO] Value changed to :", self.modeVariable)

    @Slot(QImage, int, str)
    def receiveFrame(self, qtImg, sNo, key):
        print("[OBJECT] MainWindow receiveFrame")
        print("[INFO] Updating frame no: ", sNo)
        print("[INFO] Key is: ", key)
        self.transmitEndTime = time.time()
        print("[IMP] Time taken to transmit: ", self.transmitEndTime - self.transmitStartTime)
        start = time.time()
        pixmap = QPixmap(qtImg)
        self.ui.imgDisplayLabel.setPixmap(pixmap.scaled(self.ui.imgDisplayLabel.size(),
                                                        Qt.KeepAspectRatio,
                                                        Qt.SmoothTransformation))
        self.ui.nameLabel.setText(key)
        end = time.time()
        print("Time taken setting pixmap: ",end - start)

    def closeEvent(self, event:QCloseEvent):
        # Closing the video capture thread
        videoController.threadFlag =False
        self.threadFlag = False
        self.thread.wait()
        super(MainWindow, self).closeEvent(event)
        app.exit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(True)
    videoController = VideoController()
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

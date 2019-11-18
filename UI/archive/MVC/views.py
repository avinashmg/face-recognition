import numpy as np

from PyQt5.QtCore import Qt, QThread, QTimer
from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QVBoxLayout, QApplication, QSlider, QLabel
from pyqtgraph import ImageView
from PyQt5.QtGui import QPixmap, QImage


class StartWindow(QMainWindow):
    def __init__(self, camera=None):
        super().__init__()
        self.camera = camera

        self.central_widget = QWidget()
        self.label = QLabel(self.central_widget)
        self.update_image()

        self.layout = QVBoxLayout(self.central_widget)
        self.layout.addWidget(self.label)
        self.setCentralWidget(self.central_widget)
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_image)

        self.start_movie()

    def update_image(self):
        cvImg = self.camera.get_frame()
        height, width, channel = cvImg.shape
        bytesPerLine = 3 * width
        self.qImg = QImage(cvImg.data, width, height,
                           bytesPerLine, QImage.Format_RGB888).rgbSwapped()
        pixmap = QPixmap(self.qImg)
        pixmap = pixmap.scaled(1024, 1024, Qt.KeepAspectRatio)
        # pixmap.detach()
        self.label.setPixmap(pixmap)
        QApplication.processEvents()

    def start_movie(self):
        self.movie_thread = MovieThread(self.camera)
        self.movie_thread.start()
        self.update_timer.start(30)

    def converCv2QtImg(cvImg):
        height, width, channel = cvImg.shape
        bytesPerLine = 3 * width
        qImg = QImage(cvImg.data, width, height, bytesPerLine, QImage.Format_RGB888)
        return qImg


class MovieThread(QThread):
    def __init__(self, camera):
        super().__init__()
        self.camera = camera

    def run(self):
        self.camera.acquire_movie(200)


if __name__ == '__main__':
    app = QApplication([])
    window = StartWindow()
    window.show()
    app.exit(app.exec_())

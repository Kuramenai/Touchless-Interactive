import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QSize, QThread, pyqtSignal
from home_screen.launcher import HomeScreen
from video_processing.gesture_recognition import GestureRecognition


class PiMediaCenter(QMainWindow):
    def __init__(self):
        super(PiMediaCenter, self).__init__()
        self.__initUI()

    def __initUI(self):
        self.setWindowTitle("Pi Media Center")
        self.setFixedSize(QSize(1080, 720))

        # Start gesture recognition in the background
        self.detection = GestureRecognitionThread()
        self.detection.start()
        # Load Home screen
        self.homeScreen = HomeScreen()
        self.setCentralWidget(self.homeScreen)


class GestureRecognitionThread(QThread):
    #gesture_detected = pyqtSignal()
    def run(self):
        gestureRecognition = GestureRecognition()
        gestureRecognition.detect()


if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = PiMediaCenter()
    window.show()

    app.exec_()

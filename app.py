import sys
import cv2
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
        self.detection.gesture_detected.connect(self.gesture_detection_handler)
        # Load Home screen
        self.homeScreen = HomeScreen()
        self.setCentralWidget(self.homeScreen)

    def gesture_detection_handler(self, gesture_id):
        self.homeScreen.homeMenu.show_image_of_index_by_gesture_command(gesture_id % 3)
        self.homeScreen.display_current_selection_by_gesture_command(gesture_id % 3)


class GestureRecognitionThread(QThread):
    gesture_detected = pyqtSignal(int)
    def run(self):
        self.thread_active = True
        self.gestureRecognition = GestureRecognition()
        self.gestureRecognition.videoStream.start()
        while self.thread_active:
            frame = self.gestureRecognition.videoStream.read()
            self.gestureRecognition.frame_processing(frame)
            gesture_detected_id = self.gestureRecognition.detected_gesture_id
            if gesture_detected_id != -1:
                self.gesture_detected.emit(gesture_detected_id)

            key = cv2.waitKey(1)
            if key == ord('q'):
                self.gestureRecognition.videoStream.stop()
                self.thread_active = False
                break

        cv2.destroyAllWindows()



if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = PiMediaCenter()
    window.show()

    app.exec_()

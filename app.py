import sys
import cv2
import settings
from styles import music_player_stylesheet
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QSize, QThread, pyqtSignal
from home_screen.launcher import HomeScreen
from video_processing.gesture_recognition import GestureRecognition


class PiMediaCenter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.flickering_flag = 0
        self.current_window = 0
        self.__init_ui()

    def __init_ui(self):
        self.setWindowTitle("Pi Media Center")
        self.setFixedSize(QSize(1080, 720))

        self.homeScreen = HomeScreen()

        # Start gesture recognition in the background
        self.detection = GestureRecognitionThread()
        self.detection.start()
        self.detection.open_app.connect(self.launch_app)
        self.detection.gesture_detected.connect(self.gesture_detection_handler)

    def launch_app(self, stream_started):
        if stream_started:
            # Load Window
            self.setCentralWidget(self.homeScreen)
            self.show()
        else:
            "Exit app"
            self.close()

    def gesture_detection_handler(self, gesture_id):

        if self.flickering_flag == 0:
            if settings.current_window == 0:
                self.homeScreen.gesture_handler(gesture_id)
            elif settings.current_window == 1:
                self.homeScreen.image_viewer.gesture_handler(gesture_id)
            elif settings.current_window == 2:
                self.homeScreen.music_player.gesture_handler(gesture_id)
            elif settings.current_window == 3:
                self.homeScreen.video_player.gesture_handler(gesture_id)

        # Restrict the number of times we can handle an emitted signal
        # Prevent Flickering
        self.flickering_flag += 1
        if self.flickering_flag == 15:
            self.flickering_flag = 0


class GestureRecognitionThread(QThread):
    open_app = pyqtSignal(bool)
    gesture_detected = pyqtSignal(int)

    def run(self):
        self.thread_active = True
        self.gestureRecognition = GestureRecognition()
        self.gestureRecognition.videoStream.start()
        self.open_app.emit(self.gestureRecognition.videoStream.stream_started)

        while self.thread_active:
            frame = self.gestureRecognition.videoStream.read()
            if frame is not None:
                frame = cv2.flip(frame, 1)
                detected_gesture_id = self.gestureRecognition.frame_processing(frame)
                detected_gesture_label = ''

                if detected_gesture_id >= 30:
                    detected_gesture_label = self.gestureRecognition.index_finger_movement_labels[detected_gesture_id - 30]

                self.gesture_detected.emit(detected_gesture_id)

                # Calculate and display the fps value on the screen
                fps = self.gestureRecognition.get_fps()
                cv2.putText(frame, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
                # Display the detected gesture
                cv2.putText(frame, detected_gesture_label, (10, 110), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
                cv2.imshow("Frame", frame)

                key = cv2.waitKey(1)
                if key == ord('q'):
                    self.gestureRecognition.videoStream.stop()
                    self.thread_active = False
                    break

            else:
                print("No frame detected")

        self.gestureRecognition.videoStream.stop()
        cv2.destroyAllWindows()


if __name__ == "__main__":

    app = QApplication(sys.argv)
    settings.window_manager()
    music_player_stylesheet.initialize_style()
    window = PiMediaCenter()

    app.exec_()

import sys
import cv2
from collections import Counter
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QSize, QThread, pyqtSignal
from home_screen.launcher import HomeScreen
from images_window.image_viewer import ImageViewer
from video_processing.gesture_recognition import GestureRecognition

album_path = './images_window/images/'


class PiMediaCenter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.__initUI()

    def __initUI(self):
        self.setWindowTitle("Pi Media Center")
        self.setFixedSize(QSize(1080, 720))

        # Start gesture recognition in the background
        self.detection = GestureRecognitionThread()
        self.detection.start()
        self.detection.open_app.connect(self.launch_app)
        self.detection.gesture_detected.connect(self.gesture_detection_handler)

        self.flag = 0

    def launch_app(self, stream_started):
        if stream_started:
            # Load Window
            # self.homeScreen = HomeScreen()
            self.viewer = ImageViewer(album_path)
            self.setCentralWidget(self.viewer)
            self.show()
        else:
            "Exit app"
            self.close()

    def gesture_detection_handler(self, gesture_id):

        # btnGroup = self.homeScreen.homeMenu.getButtonGroup()
        # idx = btnGroup.checkedId()
        if self.flag == 0:
        #     if gesture_id == 3:
        #         self.detection.thread_active = False
        #         self.close()
        #     elif gesture_id == 30:
        #         new_idx = (idx - 1) % 3
        #         self.homeScreen.homeMenu.show_image_of_index_by_gesture_command(new_idx)
        #     elif gesture_id == 31:
        #         new_idx = (idx + 1) % 3
        #         self.homeScreen.homeMenu.show_image_of_index_by_gesture_command(new_idx)

            self.viewer.gesture_handler(gesture_id)

        # Restrict the number of times we can handle an emitted signal
        # Prevent Flickering
        self.flag += 1
        if self.flag == 15:
            self.flag = 0


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
                self.gestureRecognition.frame_processing(frame)

                gesture = ''
                gesture2 = ''
                gesture_detected_id = self.gestureRecognition.detected_gesture_id
                if gesture_detected_id == 2 and self.gestureRecognition.index_finger_movement_stopped:
                    most_common_fg_id = Counter(self.gestureRecognition.finger_gesture_history).most_common()
                    if len(most_common_fg_id) > 1:
                        gesture = self.gestureRecognition.index_finger_movement_labels[most_common_fg_id[0][0]]
                        gesture2 = self.gestureRecognition.index_finger_movement_labels[most_common_fg_id[1][0]]
                        if most_common_fg_id[0][0] == 0:
                            print("Signal Received. Moving to left...")
                            self.gesture_detected.emit(30 + most_common_fg_id[0][0])
                        elif most_common_fg_id[0][0] == 1:
                            print("Signal Received. Moving to right...")
                            self.gesture_detected.emit(30 + most_common_fg_id[0][0])
                    else:
                        self.gesture_detected.emit(gesture_detected_id)

                # Calculate and display the fps value on the screen
                fps = self.gestureRecognition.get_fps()
                cv2.putText(frame, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
                # Display the detected gesture
                cv2.putText(frame, gesture, (10, 110), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
                cv2.putText(frame, gesture2, (10, 150), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
                cv2.imshow("Frame", frame)
            else:
                print("No frame detected")

            key = cv2.waitKey(1)
            if key == ord('q'):
                self.gestureRecognition.videoStream.stop()
                self.thread_active = False
                break

        self.gestureRecognition.videoStream.stop()
        cv2.destroyAllWindows()


if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = PiMediaCenter()

    app.exec_()

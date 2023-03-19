import cv2
import time
from video_stream import VideoStream
from hand_tracking_module import HandDetector


class GestureRecognition:
    def __init__(self):
        self.__previous_time, self.__current_time = 0, 0
        self.__fps = 0
        self.__videoStream = VideoStream(0)
        self.__detector = HandDetector()

    def detect(self):
        """Detect gesture from video stream"""
        self.__videoStream.start()
        while True:
            frame = self.__videoStream.read()
            if frame is not None:
                h, w, _ = frame.shape

                frame = self.__detector.find_hands(frame, draw=True)
                landmarks = self.__detector.find_landmarks(frame, draw=True)

                if len(landmarks) != 0:
                    pass

                self.__fps = self.get_fps()
                # Display the fps value on the screen
                cv2.putText(frame, str(int(self.__fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

                cv2.imshow("Frame", frame)

            else:
                print("No frame detected")

            if cv2.waitKey(1) == ord('q'):
                self.__videoStream.stop()
                break

        cv2.destroyAllWindows()

    def get_fps(self):
        self.__current_time = time.time()
        fps = 1 / (self.__current_time - self.__previous_time)
        self.__previous_time = self.__current_time
        return fps


if __name__ == "__main__":
    gestureRecognition = GestureRecognition()
    gestureRecognition.detect()


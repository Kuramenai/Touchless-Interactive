import copy

import cv2
import time
import numpy as np
import itertools
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

                self.get_processed_landmarks(landmarks)

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

    def get_processed_landmarks(self, landmarks: list):
        """Calculate the positions of the landmarks relative to the wrist"""

        # Copy the landmarks list to prevent unwanted changes
        landmarks_copy = copy.deepcopy(landmarks)

        # If wrist is detected calculate the other landmark point positions relative to it
        if landmarks_copy:
            if landmarks[0]:
                wrist_xpos, wrist_ypos = landmarks[0][1], landmarks[0][2]
                for index, landmark_point in enumerate(landmarks_copy):
                    landmarks_copy[index][0] -= wrist_xpos
                    landmarks_copy[index][1] -= wrist_ypos

                landmarks_copy = list(itertools.chain.from_iterable(landmarks_copy))

                # Find the greatest landmark point
                max_value = max(list(map(abs, landmarks_copy)))
                # Normalization
                landmarks_copy = np.copy(landmarks_copy)
                landmarks_copy = landmarks_copy/max_value

        return landmarks_copy









    def get_fps(self):
        """Calculate the frame rate of the pipeline"""
        self.__current_time = time.time()
        fps = 1 / (self.__current_time - self.__previous_time)
        self.__previous_time = self.__current_time
        return fps


if __name__ == "__main__":
    gestureRecognition = GestureRecognition()
    gestureRecognition.detect()


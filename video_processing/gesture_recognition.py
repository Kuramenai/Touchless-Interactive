import copy
import csv
import cv2
import time
import numpy as np
import itertools
from video_processing.video_stream import VideoStream
from video_processing.hand_tracking_module import HandDetector
from video_processing.gesture_classification.gesture_classifier import GestureClassifier


class GestureRecognition:
    def __init__(self):
        self.__previous_time, self.__current_time = 0, 0
        self.__fps = 0
        self.mode = 0
        self.key = 0
        self.gesture_id = -1
        self.detected_gesture_id = -1
        self.processed_landmarks = []
        self.labels = self.get_labels()

        self.videoStream = VideoStream(0)
        self.__detector = HandDetector()
        self.__gestureClassifier = GestureClassifier()

    def select_mode(self):
        if 48 <= self.key <= 57:  # 0 ~ 9
            self.gesture_id = self.key - 48
        if self.key == ord('d'):  # d
            self.mode = 0
        if self.key == ord('s'):  # s
            self.mode = 1

    def frame_processing(self, frame):
        if frame is not None:
            h, w, _ = frame.shape
            frame = self.__detector.find_hands(frame, draw=True)
            landmarks = self.__detector.find_landmarks(frame, draw=False)

            if len(landmarks) != 0:
                self.processed_landmarks = self.get_processed_landmarks(landmarks)
                self.detected_gesture_id = self.__gestureClassifier(self.processed_landmarks)
                # print(landmarks)
                # print(len(self.processed_landmarks))
                # self.calculate_bounding_rect(frame, landmarks)

            self.__fps = self.get_fps()
            # Display the fps value on the screen
            cv2.putText(frame, str(int(self.__fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
            cv2.imshow("Frame", frame)
        else:
            print("No frame detected")

    def get_fps(self):
        """Calculate the frame rate of the pipeline"""
        self.__current_time = time.time()
        fps = 1 / (self.__current_time - self.__previous_time)
        self.__previous_time = self.__current_time
        return fps

    def get_labels(self):
        """Get the labels for the gestures"""
        label_path = "C:/Users/marce/Documents/PycharmProjects/Touchless/video_processing" \
                     "/gesture_classification/gestures_labels.csv"
        with open(label_path, encoding='utf-8-sig') as f:
            labels = csv.reader(f)
            labels = [row[0] for row in labels]

        return labels

    def __calculate_bounding_rect(self, frame, landmarks):

        h, w, _ = frame.shape
        landmark_array = np.empty((0, 2), int)

        for landmark in landmarks:
            landmark_x = min(landmark[1], w - 1)
            landmark_y = min(landmark[2], h - 1)

            landmark_point = [np.array((landmark_x, landmark_y))]
            landmark_array = np.append(landmark_array, landmark_point, axis=0)

        x, y, w, h = cv2.boundingRect(landmark_array)

        return [x, y, x + w, y + h]

    def get_processed_landmarks(self, landmarks: list):
        """Calculate the positions of the landmarks relative to the wrist"""
        # Copy the landmarks list to prevent unwanted changes
        landmarks_copy = copy.deepcopy(landmarks)
        # calculate the other landmark point positions relative to the position of the wrist
        wrist_xpos, wrist_ypos = landmarks[0][0], landmarks[0][1]
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

    def save_landmarks(self):
        """Save landmarks points for training"""
        dataset_path = "C:/Users/marce/Documents/PycharmProjects/Touchless/video_processing/gesture_classification_models/gesture_landmarks_dataset2.csv"
        if self.mode == 1 and (0 <= self.gesture_id <= 9):
            with open(dataset_path,
                      mode='a', newline="") as f:
                landmarks_dataset = csv.writer(f)
                landmarks_dataset.writerow([self.gesture_id, *self.processed_landmarks])

    def detect(self):
        """Detect gesture from video stream"""
        self.videoStream.start()
        while True:
            frame = self.videoStream.read()
            self.frame_processing(frame)

            self.key = cv2.waitKey(1)
            if self.key == ord('q'):
                self.videoStream.stop()
                break

        cv2.destroyAllWindows()

    def get_gesture_landmarks(self):
        self.videoStream.start()
        while True:
            frame = self.videoStream.read()
            self.frame_processing(frame)

            self.key = cv2.waitKey(1)
            if self.key == ord('q'):
                self.videoStream.stop()
                break

            self.select_mode()
            # print(self.mode)
            # print(self.key)
            if self.mode == 1:
                self.save_landmarks()

        cv2.destroyAllWindows()


if __name__ == "__main__":
    gestureRecognition = GestureRecognition()
    gestureRecognition.detect()

import copy
import csv
import cv2
import time
import numpy as np
import itertools
from collections import deque
from collections import Counter
from mouse import move, click
from pyautogui import size
from video_processing.video_stream import VideoStream
from video_processing.hand_tracking_module import HandDetector
from video_processing.gesture_classification.gesture_classifier import GestureClassifier
from video_processing.gesture_classification.index_finger_movement_classifier import PointHistoryClassifier

gesture_labels_path = "video_processing/gesture_classification/labels/gestures_labels.csv"
index_finger_movement_labels_path = "video_processing/gesture_classification/labels/point_history_classifier_labels.csv"


class GestureRecognition:
    def __init__(self):
        self.__previous_time, self.__current_time = 0, 0
        self.mode = 0
        self.key = 0
        self.gesture_id = -1
        self.detected_gesture_id = -1
        self.index_finger_movement_id = -1
        self.index_finger_movement_stopped = False

        self.processed_landmarks = []
        self.processed_points_history = []

        self.gesture_labels = self.get_labels(gesture_labels_path)
        self.index_finger_movement_labels = self.get_labels(index_finger_movement_labels_path)

        self.history_length = 16
        self.point_history = deque(maxlen=self.history_length)
        self.gesture_history = deque(maxlen=2)
        self.previous_gesture, self.current_gesture = -1, -1

        self.videoStream = VideoStream(0)
        self.__detector = HandDetector()
        self.__gestureClassifier = GestureClassifier()
        self.__indexMovementClassifier = PointHistoryClassifier()

    def select_mode(self):
        if 48 <= self.key <= 57:  # 0 ~ 9
            self.gesture_id = self.key - 48
        elif self.key == ord('n'):  # normal
            self.mode = 0
        elif self.key == ord('s'):  # capture static gesture
            self.mode = 1
        elif self.key == ord('d'):  # capture dynamic gesture
            self.mode = 2

    def frame_processing(self, frame):

        h, w, _ = frame.shape
        frame = self.__detector.find_hands(frame, draw=True)
        landmarks = self.__detector.find_landmarks(frame, draw=False)
        detected_gesture_id = -1

        if len(landmarks) != 0:
            self.processed_landmarks = self.get_processed_landmarks(landmarks)
            detected_gesture_id = self.__gestureClassifier(self.processed_landmarks)
            self.previous_gesture = self.current_gesture
            self.current_gesture = detected_gesture_id
            # Pointer Mode:
            if detected_gesture_id == 2:
                screen_width, screen_height = size()
                pointer_xpos = landmarks[8][0]
                pointer_ypos = landmarks[8][1]
                pointer_xpos, pointer_ypos = np.interp(pointer_xpos, (0, w), (0, screen_width)), \
                    np.interp(pointer_ypos, (0, h), (0, screen_height))
                move(pointer_xpos, pointer_ypos)

                self.point_history.append(landmarks[8])
                self.processed_points_history = self.get_processed_points_history(frame, self.point_history, w, h)
                # Index finger movement detection
                if len(self.processed_points_history) == self.history_length * 2:
                    pointer_movement_id = self.__indexMovementClassifier(self.processed_points_history)
                    detected_gesture_id = 30 + pointer_movement_id
            elif self.current_gesture == 4:
                if self.previous_gesture == 2:
                    print("Click")

        return detected_gesture_id

    def get_fps(self):
        """Calculate the frame rate of the pipeline"""
        self.__current_time = time.time()
        fps = 1 / (self.__current_time - self.__previous_time)
        self.__previous_time = self.__current_time
        return fps

    def get_labels(self, path):
        """Get the labels for the gestures"""
        with open(path, encoding='utf-8-sig') as f:
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
        processed_landmarks = np.copy(landmarks)

        # calculate the other landmark point positions relative to the position of the wrist
        wrist_xpos, wrist_ypos = landmarks[0][0], landmarks[0][1]
        processed_landmarks[:, 0], processed_landmarks[:, 1] = processed_landmarks[:, 0] - wrist_xpos, \
                                                               processed_landmarks[:, 1] - wrist_ypos
        # Flatten the array and convert it to a python list
        processed_landmarks = processed_landmarks.ravel()
        # Normalization
        max_value = max(list(map(abs, processed_landmarks)))
        processed_keypoint_landmarks = processed_landmarks / max_value

        return processed_keypoint_landmarks

    def get_processed_points_history(self, image, point_history, image_width: int, image_height: int):

        temp_point_history = np.array(point_history, dtype=float)
        # Convert to relative coordinates
        wrist_xpos, wrist_ypos = temp_point_history[0][0], temp_point_history[0][1]
        temp_point_history[:, 0], temp_point_history[:, 1] = (temp_point_history[:, 0] - wrist_xpos) / image_width, \
                                                             (temp_point_history[:, 1] - wrist_ypos) / image_height

        # Convert to a one-dimensional list
        temp_point_history = temp_point_history.ravel()

        return temp_point_history

    def save_landmarks(self):
        """Save landmarks points for training"""
        if self.mode == 0:
            pass
        if self.mode == 1 and (0 <= self.gesture_id <= 9):
            dataset_path = "video_processing/gesture_classification_models/static_gesture_landmarks_dataset.csv"
            with open(dataset_path,
                      mode='a', newline="") as f:
                landmarks_dataset = csv.writer(f)
                landmarks_dataset.writerow([self.gesture_id, *self.processed_landmarks])
        elif self.mode == 2 and (0 <= self.gesture_id <= 9):
            dataset_path = "video_processing/gesture_classification_models/dynamoc_gesture_landmarks_dataset.csv"
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
            if self.mode == 1:
                self.save_landmarks()

        cv2.destroyAllWindows()


if __name__ == "__main__":
    gestureRecognition = GestureRecognition()
    gestureRecognition.detect()

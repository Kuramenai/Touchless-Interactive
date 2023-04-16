import copy
import csv
import cv2
import time
import numpy as np
import itertools
from collections import deque
from collections import Counter


gesture_labels_path = "video_processing" \
             "/gesture_classification/labels/gestures_labels.csv"

index_finger_movement_labels_path = "video_processing" \
             "/gesture_classification/labels/point_history_classifier_labels.csv"

class GestureRecognition:
    def __init__(self, camera_index):
        self.__previous_time, self.__current_time = 0, 0
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
        self.finger_gesture_history = deque(maxlen=self.history_length)
       
        self.videoStream = VideoStream(camera_index)
        self.__detector = HandDetector()
        self.__gestureClassifier = GestureClassifier()
        self.__indexMovementClassifier = PointHistoryClassifier()

    def frame_processing(self, frame):

        h, w, _ = frame.shape
        self.__detector.find_hands(frame)
        landmarks = self.__detector.find_landmarks(frame)

        if len(landmarks) != 0:
            self.processed_landmarks = self.get_processed_landmarks(landmarks)
            self.processed_points_history = self.get_processed_points_history(frame, self.point_history)

            self.detected_gesture_id = self.__gestureClassifier(self.processed_landmarks)
            
            # Pointer Mode:
            if self.detected_gesture_id == 2: 
                self.point_history.append(landmarks[8])
                # Index finger movement detection
                if len(self.processed_points_history) == self.history_length * 2:
                    self.index_finger_movement_id = self.__indexMovementClassifier(self.processed_points_history)
                    self.finger_gesture_history.append(self.index_finger_movement_id)
                    self.index_finger_movement_stopped = True


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

    def get_processed_points_history(self, image, point_history):
        image_width, image_height = image.shape[1], image.shape[0]

        temp_point_history = copy.deepcopy(point_history)

        # Convert to relative coordinates
        base_x, base_y = 0, 0
        for index, point in enumerate(temp_point_history):
            if index == 0:
                base_x, base_y = point[0], point[1]

            temp_point_history[index][0] = (temp_point_history[index][0] -
                                            base_x) / image_width
            temp_point_history[index][1] = (temp_point_history[index][1] -
                                            base_y) / image_height

        # Convert to a one-dimensional list
        temp_point_history = list(
            itertools.chain.from_iterable(temp_point_history))

        return temp_point_history


if __name__ == "__main__":
    from video_stream import VideoStream
    from hand_tracking_module import HandDetector
    from gesture_classification.gesture_classifier import GestureClassifier
    from gesture_classification.index_finger_movement_classifier import PointHistoryClassifier

    camera_index = 0
    gestureRecognition = GestureRecognition(camera_index)
    gestureRecognition.detect()

else:
    from video_processing.video_stream import VideoStream
    from video_processing.hand_tracking_module import HandDetector
    from video_processing.gesture_classification.gesture_classifier import GestureClassifier
    from video_processing.gesture_classification.index_finger_movement_classifier import PointHistoryClassifier

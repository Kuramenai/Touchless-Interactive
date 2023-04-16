import cv2
import mediapipe as mp


class HandDetector:
    def __init__(self, mode=False, max_num_hands=2, model_complexity=1,
                 min_detection_confidence=0.5, min_tracking_confidence=0.5):
        self.mode = mode
        self.max_num_hands = max_num_hands
        self.model_complexity = model_complexity
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence

        # mediapipe object for hand detection
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.max_num_hands, self.model_complexity,
                                        self.min_detection_confidence, self.min_tracking_confidence)

        # mediapipe object for drawing landmarks
        self.mpDraw = mp.solutions.drawing_utils

        #

    def find_hands(self, frame):

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(frame_rgb)

    def find_landmarks(self, frame, num_hands=0):

        landmarks = []

        if self.results.multi_hand_landmarks:
            my_hand = self.results.multi_hand_landmarks[num_hands]
            for lm in my_hand.landmark:
                h, w, _ = frame.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                landmarks.append([cx, cy])

        return landmarks

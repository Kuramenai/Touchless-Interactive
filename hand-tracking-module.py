import cv2
import mediapipe as mp
import time


class HandDetector():
  def __init__(self, mode=False, max_num_hands=2, model_complexity = 1,
               min_detection_confidence=0.5, min_tracking_confidence=0.5):
    self.mode = mode
    self.max_num_hands = max_num_hands
    self.model_complexity = model_complexity
    self.min_detection_confidence = min_detection_confidence
    self.min_tracking_confidence = min_tracking_confidence

    #mediapipe object for hand detection
    self.mpHands = mp.solutions.hands
    self.hands = self.mpHands.Hands(self.mode, self.max_num_hands,  self.model_complexity,
                                    self.min_detection_confidence, self.min_tracking_confidence)

    #mediapipe object for drawing landmarks
    self.mpDraw = mp.solutions.drawing_utils

  def find_hands(self, frame, draw=True):

    frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = self.hands.process(frameRGB)

    if results.multi_hand_landmarks:
      for handLms in results.multi_hand_landmarks:
        for id, lm in enumerate(handLms.landmark):
          h, w, c = frame.shape
          cx, cy = int(lm.x * w), int(lm.y * h)
          #print(id, cx, cy)

          if id == 0:
            cv2.circle(frame, (cx, cy), 25, (255, 0, 255), cv2.FILLED)
        if draw:
          self.mpDraw.draw_landmarks(frame, handLms, self.mpHands.HAND_CONNECTIONS)

    
    return frame
  

def main():

  previous_time, current_time = 0, 0

  cap = cv2.VideoCapture(0)
  Detector = HandDetector()

  if not cap.isOpened():
    print("Cannot open camera")
    exit()

  while True:
    success, frame =cap.read()

    if not success:
      print("Can't receive frame. Exiting...")
      break

    frame = Detector.find_hands(frame)

    #Calculate the frame rate
    current_time = time.time()
    fps = 1/(current_time - previous_time)
    previous_time = current_time

    #Display the fps value on the screen
    cv2.putText(frame, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    cv2.imshow("Frame", frame)

    if cv2.waitKey(1) == ord('q'):
      break

  cap.release()
  cv2.destroyAllWindows()

if __name__ == "__main__":
  main()

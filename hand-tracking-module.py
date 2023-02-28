import cv2
import mediapipe as mp
import time

previousTime, currentTime = 0, 0


cap = cv2.VideoCapture(0)

#mediapipe object for hand detection
mpHands = mp.solutions.hands
hands = mpHands.Hands()

#mediapipe object for drawing landmarks
mpDraw = mp.solutions.drawing_utils


if not cap.isOpened():
  print("Cannot open camera")
  exit()

while True:
  success, frame =cap.read()

  if not success:
    print("Can't receive frame. Exiting...")
    break

  frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
  results = hands.process(frameRGB)
  if results.multi_hand_landmarks:
    for handLms in results.multi_hand_landmarks:
      for id, lm in enumerate(handLms.landmark):
        h, w, c = frame.shape
        cx, cy = int(lm.x * w), int(lm.y * h)
        print(id, cx, cy)

        if id == 0:
          cv2.circle(frame, (cx, cy), 25, (255, 0, 255), cv2.FILLED)

      mpDraw.draw_landmarks(frame, handLms, mpHands.HAND_CONNECTIONS)

  #Calculate the frame rate
  currentTime = time.time()
  fps = 1/(currentTime - previousTime)
  previousTime = currentTime

  #Display the fps value on the screen
  cv2.putText(frame, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

  cv2.imshow("Frame", frame)

  if cv2.waitKey(1) == ord('q'):
    break

cap.release()
cv2.destroyAllWindows()

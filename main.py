from hand_tracking_module import HandDetector
import time
import cv2


def main():

  previous_time, current_time = 0, 0

  cap = cv2.VideoCapture(0)
  Detector = HandDetector()

  if not cap.isOpened():
    print("Cannot open camera")
    exit()

  while True:
    success, frame = cap.read()

    if not success:
      print("Can't receive frame. Exiting...")
      break

    frame = Detector.find_hands(frame)
    landmarks = Detector.find_landmarks(frame)

    # if len(landmarks) != 0:
    #   print(landmarks[4])

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

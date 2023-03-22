from hand_tracking_module import HandDetector
import time
import cv2
import math
# import alsaaudio
import numpy as np


def main():
    previous_time, current_time = 0, 0

    # Mixer = alsaaudio.Mixer()

    cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
    Detector = HandDetector(min_detection_confidence=0.7)

    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    while True:
        success, frame = cap.read()

        if not success:
            print("Can't receive frame. Exiting...")
            break

        h, w, _ = frame.shape

        frame = Detector.find_hands(frame, draw=False)
        landmarks = Detector.find_landmarks(frame, draw=False)

        if len(landmarks) != 0:
            pass

            # x_index, y_index = landmarks[8][1], landmarks[8][2]
            #
            # cv2.circle(frame, (x_index, y_index), 10, (255, 0, 255), cv2.FILLED)
            #
            # volume = int(((h - y_index) / h) * 100)
            #
            # if volume < 0:
            #     Mixer.setvolume(0)
            # elif volume > 100:
            #     Mixer.setvolume(100)
            # else:
            #     Mixer.setvolume(volume)

            # print(Mixer.getvolume())

            # Display the volume value on the screen
            # cv2.putText(frame, "Volume:" + str(volume), (5, 30), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)

            # Calculate the frame rate
        current_time = time.time()
        fps = 1 / (current_time - previous_time)
        previous_time = current_time

        # Display the fps value on the screen
        cv2.putText(frame, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        cv2.imshow("Frame", frame)

        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

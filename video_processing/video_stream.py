from threading import Thread
import cv2


class VideoStream:

    def __init__(self, camera_index):
        # Initialize the video camera stream and read the first frame of the stream
        self.__camera_index = camera_index
        self.__success, self.__frame = None, None
        self.__stop = False
        self.stream_started = False

        self.__stream = cv2.VideoCapture(camera_index)
        self.__stream_success = self.__is_stream_success()
        self.__has_received_frame(self.__stream_success)

    def __is_stream_success(self):
        """Detect if the video stream has started """
        if self.__stream.isOpened():
            return True

        return False

    def __has_received_frame(self, stream_success):
        if stream_success:
            print("Video Stream Started!")
            self.__success, self.__frame = self.__stream.read()
            if self.__success:
                self.stream_started = True
            else:
                print("No Frame detected")
        else:
            print(f"Cant open camera at index {self.__camera_index}. Exiting...")
            exit()

    def start(self):
        """Start the video stream thread"""
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        """Continuously grabbing new frame from video stream"""
        while True:
            if self.__stop:
                print('Exiting...')
                self.__stream.release()
                return
            self.__success, self.__frame = self.__stream.read()

    def read(self):
        """Return the frame most recently read"""
        grabbed_frame = self.__frame
        return grabbed_frame

    def stop(self):
        """Stop the video stream"""
        self.__stop = True


if __name__ == "__main__":
    videoStream = VideoStream(0)
    videoStream.start()

    while True:
        frame = videoStream.read()
        if frame is not None:
            cv2.imshow("Frame", frame)
        else:
            print("No frame detected")

        if cv2.waitKey(1) == ord('q'):
            videoStream.stop()
            break

    cv2.destroyAllWindows()

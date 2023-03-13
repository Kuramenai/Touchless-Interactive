from threading import Thread
import cv2


class WebCamVideoStream:
    
    def __init__(self):
        #Initialize the video camera stream and read the first frame of the stream
        self.stream = cv2.VideoCapture(0)
        self.success, self.frame = self.stream.read()

        #Variable used to indicate whether or not the thread should be stopped
        self.stopped = None

    def start(self):
        "Start the video strream thread"
        Thread(target=self.update, args=()).start()
        return self
    
    def update(self):
        "Continuously reading new frame from video stream"
        while True:
            if self.stopped:
                return 
            
            self.success, self.frame = self.stream.read()
    
    def read(self):
        "Return the frame most recently read"
        return self.frame
    
    def stop(self):
        "Stop the video stream"
        self.stopped = True

            



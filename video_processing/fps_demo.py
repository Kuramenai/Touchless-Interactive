from fps_counter_module import FPS 
from  webcam_video_stream import WebCamVideoStream
import argparse
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-n", "--num-frames", type=int, default=100,
                help="# of frames to loop over for FPS test")

ap.add_argument("-d", "--display", type=int, default=1,
                help="# Whether or not the fps should be displayed")

args = vars(ap.parse_args())

# Non threaded
print("[INFO] sampling frames from webcam...")
stream = cv2.VideoCapture(0)
MyFPS = FPS()
MyFPS.start()


while MyFPS._num_frames < args["num_frames"]:
    success, frame = stream.read()

    if args["display"] > 0:
        cv2.imshow("Frame", frame)
        input_key = cv2.waitKey(1) & 0xFF

    MyFPS.update()

MyFPS.stop()
print("[INFO] elapsed time: {:.2f}".format(MyFPS.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(MyFPS.fps()))

stream.release()
cv2.destroyAllWindows()

# Threaded
print("[INFO] sampling THREADED frames from webcam...")
ThreadedStream = WebCamVideoStream().start()
MyFps_Threaded = FPS()
MyFps_Threaded.start()


while MyFps_Threaded._num_frames < args["num_frames"]:
    frame = ThreadedStream.read()

    if args["display"] > 0:
        cv2.imshow("Frame", frame)
        input_key = cv2.waitKey(1) & 0xFF

    MyFps_Threaded.update()

MyFps_Threaded.stop()
print("[INFO] elapsed time: {:.2f}".format(MyFps_Threaded.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(MyFps_Threaded.fps()))


cv2.destroyAllWindows()
ThreadedStream.stop()
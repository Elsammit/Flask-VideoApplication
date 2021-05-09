import time
from base_camera import BaseCamera
import cv2

WIDTH=960
HEIGHT=540

class Camera(BaseCamera):
    counter = 0
    speed = 1
    stop = True
    rewindFlg = False
    progress = 0
    MoviePath = 'Forest - 49981.mp4'
    cap = cv2.VideoCapture(MoviePath)

    if (cap.isOpened()== False):
        print("File Open Error")
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT,HEIGHT)

    @staticmethod
    def frames():
        while True:
            if Camera.stop == True:
                continue

            ret, frame2 = Camera.cap.read()
            frame = cv2.resize(frame2,(WIDTH,HEIGHT))
            
            if ret == True:
                Camera.counter = Camera.cap.get(cv2.CAP_PROP_POS_FRAMES)
                Camera.progress = int(Camera.counter / Camera.frame_count * 100)

                if Camera.speed != 0:
                    SpdNum = Camera.speed*30
                        
                    if Camera.rewindFlg==True:
                        Camera.counter-=SpdNum
                        if Camera.counter < 0:
                            Camera.counter = 0
                        Camera.cap.set(cv2.CAP_PROP_POS_FRAMES, Camera.counter)
                    else:
                        Camera.counter+=SpdNum
                        Camera.cap.set(cv2.CAP_PROP_POS_FRAMES, Camera.counter)
                else:
                    time.sleep(1/30)
            else:
                Camera.counter=0
                
            yield cv2.imencode('.png', frame)[1].tobytes()
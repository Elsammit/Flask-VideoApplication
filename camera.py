import time
from base_camera import BaseCamera
import cv2, pafy
import time
import tensorflow as tf
from yolov3_tf2.models import (
    YoloV3, YoloV3Tiny
)
from yolov3_tf2.dataset import transform_images
from yolov3_tf2.utils import draw_outputs

class Camera(BaseCamera):
    counter = 0
    speed = 1
    stop = True
    rewindFlg = False
    progress = 0
    MoviePath = 'ファイル名'
    cap = cv2.VideoCapture(MoviePath)

    if (cap.isOpened()== False):
        print("File Open Error")
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    @staticmethod
    def frames():
        physical_devices = tf.config.experimental.list_physical_devices('GPU')
        for physical_device in physical_devices:
            tf.config.experimental.set_memory_growth(physical_device, True)

        yolo = YoloV3Tiny(classes=80)
        yolo.load_weights("./checkpoints/yolov3-tiny.tf")
        print('weights loaded')
        class_names = [c.strip() for c in open('./data/coco.names').readlines()]
        print('classes loaded')

        times = []

        while True:
            if Camera.stop == True:
                continue

            ret, frame2 = Camera.cap.read()
            
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
            
                img = cv2.resize(frame2,(640,480))
                img_in = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                img_in = tf.expand_dims(img_in, 0)
                img_in = transform_images(img_in, 416)

                t1 = time.time()
                boxes, scores, classes, nums = yolo.predict(img_in)
                t2 = time.time()
                times.append(t2-t1)
                times = times[-20:]
                img = draw_outputs(img, (boxes, scores, classes, nums), class_names)
                img = cv2.putText(img, "Time: {:.2f}ms".format(sum(times)/len(times)*1000), (0, 30),
                          cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255), 2)

                yield cv2.imencode('.png', img)[1].tobytes()
            else:
                Camera.counter=0
                Camera.cap.set(cv2.CAP_PROP_POS_FRAMES, Camera.counter)
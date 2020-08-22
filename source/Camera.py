import cv2
import multiprocessing as mp
import numpy as np
import imutils
from datetime import datetime
import threading

import getpass
user = getpass.getuser()

# defining face detector
face_cascade = cv2.CascadeClassifier("/home/" + user + "/.local/lib/python3.8/site-packages/cv2/data/haarcascade_frontalface_alt.xml")
#face_cascade = cv2.CascadeClassifier("/home/alexandros/.local/lib/python3.8/site-packages/cv2/data/haarcascade_frontalface_alt.xml")
#nested_fn  = args.get('--nested-cascade', "../../data/haarcascades/haarcascade_eye.xml")

ds_factor = 0.6


class Camera:

    # One url per time
    def __init__(self, rtsp_url):
        # load pipe for data transmittion to the process
        self.parent_conn, child_conn = mp.Pipe()
        # load process
        self.p = mp.Process(target=self.update, args=(child_conn, rtsp_url))
        # start process
        self.p.daemon = True
        self.p.start()

    def end(self):
        # send closure request to process
        self.parent_conn.send(2)

    def update(self, conn, rtsp_url):
        # load cam into seperate process
        print("Cam Loading...")
        try:
            self.cap = cv2.VideoCapture(rtsp_url, cv2.CAP_FFMPEG)
            if self.cap.isOpened():
                print("Cam Loaded...")
                self.run = True
                while self.run:
                    # grab frames from the buffer
                    self.cap.grab()
                    # recieve input data
                    rec_dat = conn.recv()
                    if rec_dat == 1:
                        # if frame requested
                        ret, frame = self.cap.read()
                        conn.send(frame)
                    elif rec_dat == 2:
                        # if close requested
                        self.cap.release()
                        self.run = False
                print("Camera Connection Closed")
                conn.close()
        except:
            pass

    def get_frame(self):
        # send request
        self.parent_conn.send(1)
        frame = self.parent_conn.recv()
        # reset request
        self.parent_conn.send(0)
        return frame

    @staticmethod
    def rescale_frame(frame, size=500):
        # return cv2.resize(frame,None,fx=percent,fy=percent)
        imutils.resize(frame, width=size)











class RTSP:

    def __init__(self, urls, window_name=None, size_frame=500):
        self.cam = []
        self.urls = urls
        self.size = size_frame
        self.name = window_name
        self.detected = False
        self.connections = [True, True, True, True]
        if window_name is not None:
            cv2.namedWindow(self.name, cv2.WND_PROP_FULLSCREEN)
            cv2.setWindowProperty(self.name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

        if len(urls) > 0:
            for url in self.urls:  # Create Camera Object
                self.cam.append(Camera(url))

    @staticmethod
    def set_time_show(name, frame):
        cv2.namedWindow(name, cv2.WINDOW_FREERATIO)
        # Shows Date Time
        # Time Setup Variables
        font = cv2.FONT_HERSHEY_SIMPLEX
        org = (50, 50)
        font_scale = 1
        color = (255, 0, 0)
        thickness = 2
        current_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        cv2.putText(frame, current_time, org, font, font_scale,
                    color, thickness, cv2.LINE_AA)
        cv2.imshow(name, frame)

    # Face Detected
    def faceDetected(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face_rects = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in face_rects:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            break
        #print(face_rects)  # Array with the values of the faces it's detecting
        if len(face_rects) != 0:
            return True
        else:
            return False

    # Reconnecting
    def reconecting(self):
        for i in range(len(self.connections)):
            if self.connections[i] == False:
                self.cam[i] = Camera(self.urls[1])
                self.connections[i] = True




    '''
    def show(self):
        if len(self.urls) < 2:  # Url == 1
            while True:
                if self.size is not None:
                    frame_1 = self.cam[0].get_frame(self.size)
                else:
                    frame_1 = self.cam[0].get_frame(1450)  # Screen size
                self.detected = self.faceDetected(frame_1)
                # Shows Date Time
                RTSP.set_time_show(self.name, frame_1, self.org, self.font,
                                   self.fontScale, self.color, self.thickness)
                key = cv2.waitKey(1)
                if key == 13:  # 13 is the Enter Key
                    break
            cv2.destroyAllWindows()
            for i in range(len(self.cam)):
                self.cam[i].end()
        elif len(self.urls) < 3:  # Url == 2
            while True:
                if self.size is not None:
                    frame_1 = self.cam[0].get_frame(self.size)
                    frame_2 = self.cam[1].get_frame(self.size)
                else:
                    frame_1 = self.cam[0].get_frame(960)  # SCreen size / 2
                    frame_2 = self.cam[1].get_frame(960)
                img_concate_hori_1 = np.concatenate((frame_1, frame_2), axis=1)
                self.detected = self.faceDetected(img_concate_hori_1)
                cv2.namedWindow(self.name, cv2.WINDOW_FREERATIO)
                # Shows Date Time
                RTSP.set_time_show(self.name, img_concate_hori_1, self.org, self.font,
                                   self.fontScale, self.color, self.thickness)
                key = cv2.waitKey(1)
                if key == 13:  # 13 is the Enter Key
                    break
            cv2.destroyAllWindows()
            for i in range(len(self.cam)):
                self.cam[i].end()
        elif len(self.urls) < 4:  # Url == 3
            while True:
                if self.size is not None:
                    frame_1 = self.cam[0].get_frame(self.size)
                    frame_2 = self.cam[1].get_frame(self.size)
                    frame_3 = self.cam[2].get_frame(self.size)
                else:
                    frame_1 = self.cam[0].get_frame(725)  # SCreen size / 4
                    frame_2 = self.cam[1].get_frame(725)
                    frame_3 = self.cam[2].get_frame(725)
                img_concate_hori_1 = np.concatenate((frame_1, frame_2), axis=1)
                img_concate_line = np.concatenate((img_concate_hori_1, frame_3), axis=0)
                self.detected = self.faceDetected(img_concate_line)
                cv2.namedWindow(self.name, cv2.WINDOW_FREERATIO)
                # Shows Date Time
                RTSP.set_time_show(self.name, img_concate_line, self.org, self.font,
                                   self.fontScale, self.color, self.thickness)
                key = cv2.waitKey(1)
                if key == 13:  # 13 is the Enter Key
                    break
            cv2.destroyAllWindows()
            for i in range(len(self.cam)):
                self.cam[i].end()
        elif len(self.urls) < 5:  # Url == 4
            while True:
                if self.size is not None:
                    frame_1 = self.cam[0].get_frame(self.size)
                    frame_2 = self.cam[1].get_frame(self.size)
                    frame_3 = self.cam[2].get_frame(self.size)
                    frame_4 = self.cam[3].get_frame(self.size)
                else:
                    frame_1 = self.cam[0].get_frame(725)  # SCreen size / 4
                    frame_2 = self.cam[1].get_frame(725)
                    frame_3 = self.cam[2].get_frame(725)
                    frame_4 = self.cam[3].get_frame(725)
                img_concate_hori_1 = np.concatenate((frame_1, frame_2), axis=1)
                img_concate_hori_2 = np.concatenate((frame_3, frame_4), axis=1)
                img_concate_line = np.concatenate((img_concate_hori_1, img_concate_hori_2), axis=0)
                self.detected = self.faceDetected(img_concate_line)
                cv2.namedWindow(self.name, cv2.WINDOW_FREERATIO)
                # Shows Date Time
                RTSP.set_time_show(self.name, img_concate_line, self.org, self.font,
                                   self.fontScale, self.color, self.thickness)
                key = cv2.waitKey(1)
                if key == 13:  # 13 is the Enter Key
                    break
            cv2.destroyAllWindows()
            for i in range(len(self.cam)):
                self.cam[i].end()
    '''


    def get_bytes(self, local):
        # Thread if lost connection reconct
        #connecting_thread = threading.Thread(target=self.reconecting, args=())
        #connecting_thread.start()
        if len(self.urls) < 2:  # Url == 1
            while True:
                try:
                    frame_1 = self.cam[0].get_frame()
                except:
                    frame_1 = None
                # True
                if frame_1 is not None:
                    Camera.rescale_frame(frame_1, self.size)
                    self.detected = self.faceDetected(frame_1)
                    ret, jpeg = cv2.imencode('.jpg', frame_1)
                    yield b'--frame\r\n'b'Content-Type:image/jpeg\r\n\r\n' + bytearray(jpeg) + b'\r\n'
                    '''
                    if local == False:
                        ret, jpeg = cv2.imencode('.jpg', frame_1)
                        yield b'--frame\r\n'b'Content-Type:image/jpeg\r\n\r\n'+bytearray(jpeg)+b'\r\n'
                    else:
                        # Shows Date Time
                        RTSP.set_time_show(self.name, frame_1)
                        key = cv2.waitKey(1)
                        if key == 13:  # 13 is the Enter Key
                            cv2.destroyAllWindows()
                            for i in range(len(self.cam)):
                                self.cam[i].end()
                            break
                    '''
                # False
                else:
                    self.connections[0] = False
                self.reconecting()
        elif len(self.urls) < 3:  # Url == 2
            while True:
                try:
                    frame_1 = self.cam[0].get_frame()
                except:
                    frame_1 = None
                try:
                    frame_2 = self.cam[1].get_frame()
                except:
                    frame_2 = None
                # True True
                if frame_1 is not None and frame_2 is not None:  # If tow cameras work
                    Camera.rescale_frame(frame_1, self.size)
                    Camera.rescale_frame(frame_2, self.size)
                    img_concate_hori_1 = np.concatenate((frame_1, frame_2), axis=1)
                    self.detected = self.faceDetected(img_concate_hori_1)
                    ret, jpeg = cv2.imencode('.jpg', img_concate_hori_1)
                    yield b'--frame\r\n'b'Content-Type:image/jpeg\r\n\r\n' + bytearray(jpeg) + b'\r\n'
                    '''
                    if local == False:
                        ret, jpeg = cv2.imencode('.jpg', img_concate_hori_1)
                        yield b'--frame\r\n'b'Content-Type:image/jpeg\r\n\r\n' + bytearray(jpeg) + b'\r\n'
                    else:
                        print("Local")
                        # Shows Date Time
                        RTSP.set_time_show(self.name, img_concate_hori_1)
                        key = cv2.waitKey(1)
                        if key == 13:  # 13 is the Enter Key
                            cv2.destroyAllWindows()
                            for i in range(len(self.cam)):
                                self.cam[i].end()
                            break
                    '''
                # True False
                elif frame_1 is not None and frame_2 is None:
                    Camera.rescale_frame(frame_1, self.size)
                    self.detected = self.faceDetected(frame_1)
                    ret, jpeg = cv2.imencode('.jpg', frame_1)
                    yield b'--frame\r\n'b'Content-Type:image/jpeg\r\n\r\n' + bytearray(jpeg) + b'\r\n'
                    '''
                    if local != True:
                        ret, jpeg = cv2.imencode('.jpg', frame_1)
                        yield b'--frame\r\n'b'Content-Type:image/jpeg\r\n\r\n' + bytearray(jpeg) + b'\r\n'
                    else:
                        # Shows Date Time
                        RTSP.set_time_show(self.name, frame_1)
                        key = cv2.waitKey(1)
                        if key == 13:  # 13 is the Enter Key
                            cv2.destroyAllWindows()
                            for i in range(len(self.cam)):
                                self.cam[i].end()
                            break
                    '''
                    self.connections[1] = False
                # False True
                elif frame_1 is None and frame_2 is not None:
                    Camera.rescale_frame(frame_2, self.size)
                    self.detected = self.faceDetected(frame_2)
                    ret, jpeg = cv2.imencode('.jpg', frame_2)
                    yield b'--frame\r\n'b'Content-Type:image/jpeg\r\n\r\n' + bytearray(jpeg) + b'\r\n'
                    '''
                    if local != True:
                        ret, jpeg = cv2.imencode('.jpg', frame_2)
                        yield b'--frame\r\n'b'Content-Type:image/jpeg\r\n\r\n' + bytearray(jpeg) + b'\r\n'
                    else:
                        # Shows Date Time
                        RTSP.set_time_show(self.name, frame_2)
                        key = cv2.waitKey(1)
                        if key == 13:  # 13 is the Enter Key
                            cv2.destroyAllWindows()
                            for i in range(len(self.cam)):
                                self.cam[i].end()
                            break
                    '''
                    self.connections[0] = False
                # Reconnecting
                self.reconecting()
        elif len(self.urls) < 4:  # Url == 3
            while True:
                try:
                    frame_1 = self.cam[0].get_frame()
                except:
                    frame_1 = None
                try:
                    frame_2 = self.cam[1].get_frame()
                except:
                    frame_2 = None
                try:
                    frame_3 = self.cam[2].get_frame()
                except:
                    frame_3 = None
                if frame_1 is not None and frame_2 is not None \
                        and frame_3 is not None:
                    Camera.rescale_frame(frame_1, self.size)
                    Camera.rescale_frame(frame_2, self.size)
                    Camera.rescale_frame(frame_3, self.size)
                    img_concate_hori_1 = np.concatenate((frame_1, frame_2), axis=1)
                    img_concate_line = np.concatenate((img_concate_hori_1, frame_3), axis=0)
                    self.detected = self.faceDetected(img_concate_line)
                    ret, jpeg = cv2.imencode('.jpg', img_concate_line)
                    yield b'--frame\r\n'b'Content-Type:image/jpeg\r\n\r\n' + bytearray(jpeg) + b'\r\n'
                    '''
                    if local != True:
                        ret, jpeg = cv2.imencode('.jpg', img_concate_line)
                        yield b'--frame\r\n'b'Content-Type:image/jpeg\r\n\r\n' + bytearray(jpeg) + b'\r\n'
                    else:
                        # Shows Date Time
                        RTSP.set_time_show(self.name, img_concate_line)
                        key = cv2.waitKey(1)
                        if key == 13:  # 13 is the Enter Key
                            cv2.destroyAllWindows()
                            for i in range(len(self.cam)):
                                self.cam[i].end()
                            break
                    '''
                # True True False
                elif frame_1 is not None and frame_2 is not None \
                        and frame_3 is None:
                    Camera.rescale_frame(frame_1, self.size)
                    Camera.rescale_frame(frame_2, self.size)
                    img_concate_hori_1 = np.concatenate((frame_1, frame_2), axis=1)
                    self.detected = self.faceDetected(img_concate_hori_1)
                    ret, jpeg = cv2.imencode('.jpg', img_concate_hori_1)
                    yield b'--frame\r\n'b'Content-Type:image/jpeg\r\n\r\n' + bytearray(jpeg) + b'\r\n'
                    '''
                    if local == False:
                        ret, jpeg = cv2.imencode('.jpg', img_concate_hori_1)
                        yield b'--frame\r\n'b'Content-Type:image/jpeg\r\n\r\n' + bytearray(jpeg) + b'\r\n'
                    else:
                        # Shows Date Time
                        RTSP.set_time_show(self.name, img_concate_hori_1)
                        key = cv2.waitKey(1)
                        if key == 13:  # 13 is the Enter Key
                            cv2.destroyAllWindows()
                            for i in range(len(self.cam)):
                                self.cam[i].end()
                            break
                    self.connections[2] = False
                    '''
                # True False False
                elif frame_1 is not None and frame_2 is None \
                        and frame_3 is None:
                    Camera.rescale_frame(frame_1, self.size)
                    self.detected = self.faceDetected(frame_1)
                    ret, jpeg = cv2.imencode('.jpg', frame_1)
                    yield b'--frame\r\n'b'Content-Type:image/jpeg\r\n\r\n' + bytearray(jpeg) + b'\r\n'
                    '''
                    if local != True:
                        ret, jpeg = cv2.imencode('.jpg', frame_1)
                        yield b'--frame\r\n'b'Content-Type:image/jpeg\r\n\r\n' + bytearray(jpeg) + b'\r\n'
                    else:
                        # Shows Date Time
                        RTSP.set_time_show(self.name, frame_1)
                        key = cv2.waitKey(1)
                        if key == 13:  # 13 is the Enter Key
                            cv2.destroyAllWindows()
                            for i in range(len(self.cam)):
                                self.cam[i].end()
                            break
                    '''
                    self.connections[1] = False
                    self.connections[2] = False
                # False False False
                elif frame_1 is None and frame_2 is None \
                        and frame_3 is None:
                    self.connections[0] = False
                    self.connections[1] = False
                    self.connections[2] = False
                # False False True
                elif frame_1 is None and frame_2 is None \
                        and frame_3 is not None:
                    Camera.rescale_frame(frame_3, self.size)
                    self.detected = self.faceDetected(frame_3)
                    ret, jpeg = cv2.imencode('.jpg', frame_3)
                    yield b'--frame\r\n'b'Content-Type:image/jpeg\r\n\r\n' + bytearray(jpeg) + b'\r\n'
                    '''
                    if local != True:
                        ret, jpeg = cv2.imencode('.jpg', frame_3)
                        yield b'--frame\r\n'b'Content-Type:image/jpeg\r\n\r\n' + bytearray(jpeg) + b'\r\n'
                    else:
                        # Shows Date Time
                        RTSP.set_time_show(self.name, frame_3)
                        key = cv2.waitKey(1)
                        if key == 13:  # 13 is the Enter Key
                            cv2.destroyAllWindows()
                            for i in range(len(self.cam)):
                                self.cam[i].end()
                            break
                    '''
                    self.connections[0] = False
                    self.connections[1] = False
                # False True True
                elif frame_1 is None and frame_2 is not None \
                        and frame_3 is None:
                    Camera.rescale_frame(frame_2, self.size)
                    Camera.rescale_frame(frame_3, self.size)
                    img_concate_hori_1 = np.concatenate((frame_2, frame_3), axis=1)
                    self.detected = self.faceDetected(img_concate_hori_1)
                    ret, jpeg = cv2.imencode('.jpg', img_concate_hori_1)
                    yield b'--frame\r\n'b'Content-Type:image/jpeg\r\n\r\n' + bytearray(jpeg) + b'\r\n'
                    '''
                    if local == False:
                        ret, jpeg = cv2.imencode('.jpg', img_concate_hori_1)
                        yield b'--frame\r\n'b'Content-Type:image/jpeg\r\n\r\n' + bytearray(jpeg) + b'\r\n'
                    else:
                        # Shows Date Time
                        RTSP.set_time_show(self.name, img_concate_hori_1)
                        key = cv2.waitKey(1)
                        if key == 13:  # 13 is the Enter Key
                            cv2.destroyAllWindows()
                            for i in range(len(self.cam)):
                                self.cam[i].end()
                            break
                    '''
                    self.connections[0] = False
                # False True False
                elif frame_1 is None and frame_2 is not None \
                        and frame_3 is None:
                    Camera.rescale_frame(frame_2, self.size)
                    self.detected = self.faceDetected(frame_2)
                    ret, jpeg = cv2.imencode('.jpg', frame_2)
                    yield b'--frame\r\n'b'Content-Type:image/jpeg\r\n\r\n' + bytearray(jpeg) + b'\r\n'
                    '''
                    if local != True:
                        ret, jpeg = cv2.imencode('.jpg', frame_2)
                        yield b'--frame\r\n'b'Content-Type:image/jpeg\r\n\r\n' + bytearray(jpeg) + b'\r\n'
                    else:
                        # Shows Date Time
                        RTSP.set_time_show(self.name, frame_2)
                        key = cv2.waitKey(1)
                        if key == 13:  # 13 is the Enter Key
                            cv2.destroyAllWindows()
                            for i in range(len(self.cam)):
                                self.cam[i].end()
                            break
                    '''
                    self.connections[0] = False
                    self.connections[2] = False
                # Reconnecting
                #self.reconecting()
        elif len(self.urls) < 5:  # Url == 4
            while True:
                try:
                    frame_1 = self.cam[0].get_frame()
                except:
                    frame_1 = None
                try:
                    frame_2 = self.cam[1].get_frame()
                except:
                    frame_2 = None
                try:
                    frame_3 = self.cam[2].get_frame()
                except:
                    frame_3 = None
                try:
                    frame_4 = self.cam[2].get_frame()
                except:
                    frame_4 = None
                # True True True True
                if frame_1 is not None and frame_2 is not None and \
                        frame_3 is not None and frame_4 is not None:
                    Camera.rescale_frame(frame_1, self.size)
                    Camera.rescale_frame(frame_2, self.size)
                    Camera.rescale_frame(frame_3, self.size)
                    Camera.rescale_frame(frame_4, self.size)
                    img_concate_hori_1 = np.concatenate((frame_1, frame_2), axis=1)
                    img_concate_hori_2 = np.concatenate((frame_3, frame_4), axis=1)
                    img_concate_line = np.concatenate((img_concate_hori_1, img_concate_hori_2), axis=0)
                    self.detected = self.faceDetected(img_concate_line)
                    ret, jpeg = cv2.imencode('.jpg', img_concate_line)
                    yield b'--frame\r\n'b'Content-Type:image/jpeg\r\n\r\n' + bytearray(jpeg) + b'\r\n'
                    '''
                    if local != True:
                        ret, jpeg = cv2.imencode('.jpg', img_concate_line)
                        yield b'--frame\r\n'b'Content-Type:image/jpeg\r\n\r\n' + bytearray(jpeg) + b'\r\n'
                    else:
                        # Shows Date Time
                        RTSP.set_time_show(self.name, img_concate_line)
                        key = cv2.waitKey(1)
                        if key == 13:  # 13 is the Enter Key
                            cv2.destroyAllWindows()
                            for i in range(len(self.cam)):
                                self.cam[i].end()
                            break
                    '''
                # False True True True
                elif frame_1 is None and frame_2 is not None and \
                        frame_3 is not None and frame_4 is not None:
                    Camera.rescale_frame(frame_2, self.size)
                    Camera.rescale_frame(frame_3, self.size)
                    Camera.rescale_frame(frame_4, self.size)
                    img_concate_hori_1 = np.concatenate((frame_2, frame_3), axis=1)
                    img_concate_line = np.concatenate((img_concate_hori_1, frame_4), axis=0)
                    self.detected = self.faceDetected(img_concate_line)
                    ret, jpeg = cv2.imencode('.jpg', img_concate_line)
                    yield b'--frame\r\n'b'Content-Type:image/jpeg\r\n\r\n' + bytearray(jpeg) + b'\r\n'
                    '''
                    if local != True:
                        ret, jpeg = cv2.imencode('.jpg', img_concate_line)
                        yield b'--frame\r\n'b'Content-Type:image/jpeg\r\n\r\n' + bytearray(jpeg) + b'\r\n'
                    else:
                        # Shows Date Time
                        RTSP.set_time_show(self.name, img_concate_line)
                        key = cv2.waitKey(1)
                        if key == 13:  # 13 is the Enter Key
                            cv2.destroyAllWindows()
                            for i in range(len(self.cam)):
                                self.cam[i].end()
                            break
                    '''
                    self.connections[0] = False
                # False False True True
                elif frame_1 is None and frame_2 is None and \
                         frame_3 is not None and frame_4 is not None:
                    Camera.rescale_frame(frame_3, self.size)
                    Camera.rescale_frame(frame_4, self.size)
                    img_concate_hori_1 = np.concatenate((frame_3, frame_4), axis=1)
                    self.detected = self.faceDetected(img_concate_hori_1)
                    ret, jpeg = cv2.imencode('.jpg', img_concate_hori_1)
                    yield b'--frame\r\n'b'Content-Type:image/jpeg\r\n\r\n' + bytearray(jpeg) + b'\r\n'
                    '''
                    if local == False:
                        ret, jpeg = cv2.imencode('.jpg', img_concate_hori_1)
                        yield b'--frame\r\n'b'Content-Type:image/jpeg\r\n\r\n' + bytearray(jpeg) + b'\r\n'
                    else:
                        # Shows Date Time
                        RTSP.set_time_show(self.name, img_concate_hori_1)
                        key = cv2.waitKey(1)
                        if key == 13:  # 13 is the Enter Key
                            cv2.destroyAllWindows()
                            for i in range(len(self.cam)):
                                self.cam[i].end()
                            break
                    '''
                    self.connections[0] = False
                    self.connections[1] = False
                # False False False True
                elif frame_1 is None and frame_2 is None and \
                         frame_3 is None and frame_4 is not None:
                    Camera.rescale_frame(frame_4, self.size)
                    self.detected = self.faceDetected(frame_4)
                    ret, jpeg = cv2.imencode('.jpg', frame_4)
                    yield b'--frame\r\n'b'Content-Type:image/jpeg\r\n\r\n' + bytearray(jpeg) + b'\r\n'
                    '''
                    if local != True:
                        ret, jpeg = cv2.imencode('.jpg', frame_4)
                        yield b'--frame\r\n'b'Content-Type:image/jpeg\r\n\r\n' + bytearray(jpeg) + b'\r\n'
                    else:
                        # Shows Date Time
                        RTSP.set_time_show(self.name, frame_4)
                        key = cv2.waitKey(1)
                        if key == 13:  # 13 is the Enter Key
                            cv2.destroyAllWindows()
                            for i in range(len(self.cam)):
                                self.cam[i].end()
                            break
                    '''
                    self.connections[0] = False
                    self.connections[1] = False
                    self.connections[2] = False
                # False False False False
                elif frame_1 is None and frame_2 is None and \
                         frame_3 is None and frame_4 is None:
                    self.connections[0] = False
                    self.connections[1] = False
                    self.connections[2] = False
                    self.connections[3] = False
                # False True True False
                elif frame_1 is None and frame_2 is not None and \
                         frame_3 is not None and frame_4 is None:
                    Camera.rescale_frame(frame_2, self.size)
                    Camera.rescale_frame(frame_3, self.size)
                    img_concate_hori_1 = np.concatenate((frame_2, frame_3), axis=1)
                    self.detected = self.faceDetected(img_concate_hori_1)
                    ret, jpeg = cv2.imencode('.jpg', img_concate_hori_1)
                    yield b'--frame\r\n'b'Content-Type:image/jpeg\r\n\r\n' + bytearray(jpeg) + b'\r\n'
                    '''
                    if local == False:
                        ret, jpeg = cv2.imencode('.jpg', img_concate_hori_1)
                        yield b'--frame\r\n'b'Content-Type:image/jpeg\r\n\r\n' + bytearray(jpeg) + b'\r\n'
                    else:
                        # Shows Date Time
                        RTSP.set_time_show(self.name, img_concate_hori_1)
                        key = cv2.waitKey(1)
                        if key == 13:  # 13 is the Enter Key
                            cv2.destroyAllWindows()
                            for i in range(len(self.cam)):
                                self.cam[i].end()
                            break
                    '''
                    self.connections[0] = False
                    self.connections[3] = False
                # True False False True
                elif frame_1 is not None and frame_2 is None and \
                         frame_3 is None and frame_4 is not None:
                    Camera.rescale_frame(frame_1, self.size)
                    Camera.rescale_frame(frame_4, self.size)
                    img_concate_hori_1 = np.concatenate((frame_1, frame_4), axis=1)
                    self.detected = self.faceDetected(img_concate_hori_1)
                    ret, jpeg = cv2.imencode('.jpg', img_concate_hori_1)
                    yield b'--frame\r\n'b'Content-Type:image/jpeg\r\n\r\n' + bytearray(jpeg) + b'\r\n'
                    '''
                    if local == False:
                        ret, jpeg = cv2.imencode('.jpg', img_concate_hori_1)
                        yield b'--frame\r\n'b'Content-Type:image/jpeg\r\n\r\n' + bytearray(jpeg) + b'\r\n'
                    else:
                        # Shows Date Time
                        RTSP.set_time_show(self.name, img_concate_hori_1)
                        key = cv2.waitKey(1)
                        if key == 13:  # 13 is the Enter Key
                            cv2.destroyAllWindows()
                            for i in range(len(self.cam)):
                                self.cam[i].end()
                            break
                    '''
                    self.connections[1] = False
                    self.connections[2] = False
                # True False True True
                elif frame_1 is not None and frame_2 is None and \
                         frame_3 is not None and frame_4 is not None:
                    Camera.rescale_frame(frame_1, self.size)
                    Camera.rescale_frame(frame_3, self.size)
                    Camera.rescale_frame(frame_4, self.size)
                    img_concate_hori_1 = np.concatenate((frame_1, frame_3), axis=1)
                    img_concate_line = np.concatenate((img_concate_hori_1, frame_4), axis=0)
                    self.detected = self.faceDetected(img_concate_line)
                    ret, jpeg = cv2.imencode('.jpg', img_concate_line)
                    yield b'--frame\r\n'b'Content-Type:image/jpeg\r\n\r\n' + bytearray(jpeg) + b'\r\n'
                    '''
                    if local != True:
                        ret, jpeg = cv2.imencode('.jpg', img_concate_line)
                        yield b'--frame\r\n'b'Content-Type:image/jpeg\r\n\r\n' + bytearray(jpeg) + b'\r\n'
                    else:
                        # Shows Date Time
                        RTSP.set_time_show(self.name, img_concate_line)
                        key = cv2.waitKey(1)
                        if key == 13:  # 13 is the Enter Key
                            cv2.destroyAllWindows()
                            for i in range(len(self.cam)):
                                self.cam[i].end()
                            break
                    '''
                    self.connections[1] = False
                # True True False True
                elif frame_1 is not None and frame_2 is not None and \
                         frame_3 is None and frame_4 is not None:
                    Camera.rescale_frame(frame_1, self.size)
                    Camera.rescale_frame(frame_2, self.size)
                    Camera.rescale_frame(frame_4, self.size)
                    img_concate_hori_1 = np.concatenate((frame_1, frame_2), axis=1)
                    img_concate_line = np.concatenate((img_concate_hori_1, frame_4), axis=0)
                    self.detected = self.faceDetected(img_concate_line)
                    ret, jpeg = cv2.imencode('.jpg', img_concate_line)
                    yield b'--frame\r\n'b'Content-Type:image/jpeg\r\n\r\n' + bytearray(jpeg) + b'\r\n'
                    '''
                    if local != True:
                        ret, jpeg = cv2.imencode('.jpg', img_concate_line)
                        yield b'--frame\r\n'b'Content-Type:image/jpeg\r\n\r\n' + bytearray(jpeg) + b'\r\n'
                    else:
                        # Shows Date Time
                        RTSP.set_time_show(self.name, img_concate_line)
                        key = cv2.waitKey(1)
                        if key == 13:  # 13 is the Enter Key
                            cv2.destroyAllWindows()
                            for i in range(len(self.cam)):
                                self.cam[i].end()
                            break
                    '''
                    self.connections[2] = False
                # False True False False
                elif frame_1 is None and frame_2 is not None and \
                         frame_3 is None and frame_4 is None:
                    Camera.rescale_frame(frame_2, self.size)
                    self.detected = self.faceDetected(frame_2)
                    ret, jpeg = cv2.imencode('.jpg', frame_2)
                    yield b'--frame\r\n'b'Content-Type:image/jpeg\r\n\r\n' + bytearray(jpeg) + b'\r\n'
                    '''
                    if local != True:
                        ret, jpeg = cv2.imencode('.jpg', frame_2)
                        yield b'--frame\r\n'b'Content-Type:image/jpeg\r\n\r\n' + bytearray(jpeg) + b'\r\n'
                    else:
                        # Shows Date Time
                        RTSP.set_time_show(self.name, frame_2)
                        key = cv2.waitKey(1)
                        if key == 13:  # 13 is the Enter Key
                            cv2.destroyAllWindows()
                            for i in range(len(self.cam)):
                                self.cam[i].end()
                            break
                    '''
                    self.connections[0] = False
                    self.connections[2] = False
                    self.connections[3] = False
                # False False True False
                elif frame_1 is None and frame_2 is None and \
                         frame_3 is not None and frame_4 is None:
                    Camera.rescale_frame(frame_3, self.size)
                    self.detected = self.faceDetected(frame_3)
                    ret, jpeg = cv2.imencode('.jpg', frame_3)
                    yield b'--frame\r\n'b'Content-Type:image/jpeg\r\n\r\n' + bytearray(jpeg) + b'\r\n'
                    '''
                    if local != True:
                        ret, jpeg = cv2.imencode('.jpg', frame_3)
                        yield b'--frame\r\n'b'Content-Type:image/jpeg\r\n\r\n' + bytearray(jpeg) + b'\r\n'
                    else:
                        # Shows Date Time
                        RTSP.set_time_show(self.name, frame_3)
                        key = cv2.waitKey(1)
                        if key == 13:  # 13 is the Enter Key
                            cv2.destroyAllWindows()
                            for i in range(len(self.cam)):
                                self.cam[i].end()
                            break
                    '''
                    self.connections[0] = False
                    self.connections[1] = False
                    self.connections[3] = False
                # True False False False
                elif frame_1 is not None and frame_2 is None and \
                         frame_3 is None and frame_4 is None:
                    Camera.rescale_frame(frame_1, self.size)
                    self.detected = self.faceDetected(frame_1)
                    ret, jpeg = cv2.imencode('.jpg', frame_1)
                    yield b'--frame\r\n'b'Content-Type:image/jpeg\r\n\r\n' + bytearray(jpeg) + b'\r\n'
                    '''
                    if local != True:
                        ret, jpeg = cv2.imencode('.jpg', frame_1)
                        yield b'--frame\r\n'b'Content-Type:image/jpeg\r\n\r\n' + bytearray(jpeg) + b'\r\n'
                    else:
                        # Shows Date Time
                        RTSP.set_time_show(self.name, frame_1)
                        key = cv2.waitKey(1)
                        if key == 13:  # 13 is the Enter Key
                            cv2.destroyAllWindows()
                            for i in range(len(self.cam)):
                                self.cam[i].end()
                            break
                    '''
                    self.connections[1] = False
                    self.connections[2] = False
                    self.connections[3] = False
                # True True False False
                elif frame_1 is not None and frame_2 is not None and \
                         frame_3 is None and frame_4 is None:
                    Camera.rescale_frame(frame_1, self.size)
                    Camera.rescale_frame(frame_2, self.size)
                    img_concate_hori_1 = np.concatenate((frame_1, frame_2), axis=1)
                    self.detected = self.faceDetected(img_concate_hori_1)
                    ret, jpeg = cv2.imencode('.jpg', img_concate_hori_1)
                    yield b'--frame\r\n'b'Content-Type:image/jpeg\r\n\r\n' + bytearray(jpeg) + b'\r\n'
                    '''
                    if local == False:
                        ret, jpeg = cv2.imencode('.jpg', img_concate_hori_1)
                        yield b'--frame\r\n'b'Content-Type:image/jpeg\r\n\r\n' + bytearray(jpeg) + b'\r\n'
                    else:
                        # Shows Date Time
                        RTSP.set_time_show(self.name, img_concate_hori_1)
                        key = cv2.waitKey(1)
                        if key == 13:  # 13 is the Enter Key
                            cv2.destroyAllWindows()
                            for i in range(len(self.cam)):
                                self.cam[i].end()
                            break
                    '''
                    self.connections[2] = False
                    self.connections[3] = False
                # True True True False
                elif frame_1 is not None and frame_2 is not None and \
                         frame_3 is not None and frame_4 is None:
                    Camera.rescale_frame(frame_1, self.size)
                    Camera.rescale_frame(frame_2, self.size)
                    Camera.rescale_frame(frame_3, self.size)
                    img_concate_hori_1 = np.concatenate((frame_1, frame_2), axis=1)
                    img_concate_line = np.concatenate((img_concate_hori_1, frame_3), axis=0)
                    self.detected = self.faceDetected(img_concate_line)
                    ret, jpeg = cv2.imencode('.jpg', img_concate_line)
                    yield b'--frame\r\n'b'Content-Type:image/jpeg\r\n\r\n' + bytearray(jpeg) + b'\r\n'
                    '''
                    if local == False:
                        ret, jpeg = cv2.imencode('.jpg', img_concate_line)
                        yield b'--frame\r\n'b'Content-Type:image/jpeg\r\n\r\n' + bytearray(jpeg) + b'\r\n'
                    else:
                        # Shows Date Time
                        RTSP.set_time_show(self.name, img_concate_line)
                        key = cv2.waitKey(1)
                        if key == 13:  # 13 is the Enter Key
                            cv2.destroyAllWindows()
                            for i in range(len(self.cam)):
                                self.cam[i].end()
                            break
                    '''
                    self.connections[3] = False
                # Reconnecting
                #self.reconecting()


'''
#print(f"Camera is alive?: {cam.p.is_alive()}")
if __name__ == "__main__":
    try:
        urls = ["rtsp://37.6.233.82:151/mjpeg/1", "rtsp://37.6.233.82:153/mjpeg/1"] # , "rtsp://37.6.233.82:153/mjpeg/1"
        screen = getRTSP(urls, "Monitor") # , size , 950
        screen.show()
    except:
        print("Pleace check youre cameras connectivity.")
'''

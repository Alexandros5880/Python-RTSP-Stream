import cv2
import multiprocessing as mp
import numpy as np
import imutils
from datetime import datetime
'''
import py_compile
py_compile.compile('Camera.py')
'''

# defining face detector
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")
ds_factor = 0.6


class Camera:

    def __init__(self, rtsp_url):
        # load pipe for data transmittion to the process
        self.parent_conn, child_conn = mp.Pipe()
        # load process
        self.p = mp.Process(target=Camera.update, args=(child_conn, rtsp_url))
        # start process
        self.p.daemon = True
        self.p.start()

    def end(self):
        # send closure request to process
        self.parent_conn.send(2)

    @staticmethod
    def update(conn, rtsp_url):
        # load cam into seperate process
        print("Cam Loading...")
        cap = cv2.VideoCapture(rtsp_url, cv2.CAP_FFMPEG)
        print("Cam Loaded...")
        run = True
        while run:
            # grab frames from the buffer
            cap.grab()
            # recieve input data
            rec_dat = conn.recv()
            if rec_dat == 1:
                # if frame requested
                ret, frame = cap.read()
                conn.send(frame)
            elif rec_dat == 2:
                # if close requested
                cap.release()
                run = False
            # ret, jpeg = cv2.imencode('.jpg', frame)
            # self.bytes = jpeg.toBytes()
        print("Camera Connection Closed")
        conn.close()

    def get_frame(self, resize=None):
        # used to grab frames from the cam connection process
        # [resize] param : % of size reduction or increase i.e
        # 0.65 for 35% reduction  or 1.5 for a 50% increase
        # send request
        self.parent_conn.send(1)
        frame = self.parent_conn.recv()
        # reset request
        self.parent_conn.send(0)
        # resize if needed
        if resize is None:
            return frame
        else:
            return Camera.rescale_frame(frame, resize)

    @staticmethod
    def rescale_frame(frame, size=500):
        # return cv2.resize(frame,None,fx=percent,fy=percent)
        frame = imutils.resize(frame, width=size)
        return frame


class RTSP:

    def __init__(self, urls, window_name=None, size_frame=None):
        self.cam = []
        self.urls = urls
        self.size = size_frame
        self.name = window_name
        if window_name is not None:
            cv2.namedWindow(self.name, cv2.WND_PROP_FULLSCREEN)
            cv2.setWindowProperty(self.name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
            self.font = cv2.FONT_HERSHEY_SIMPLEX
            self.org = (50, 50)
            self.fontScale = 1
            self.color = (255, 0, 0)
            self.thickness = 2
        if len(urls) > 0:
            for url in self.urls:
                self.cam.append(Camera(url))

    @staticmethod
    def set_time_show(name, frame, org, font, font_scale, color, thickness):
        cv2.namedWindow(name, cv2.WINDOW_FREERATIO)
        # Shows Date Time
        current_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        cv2.putText(frame, current_time, org, font, font_scale,
                    color, thickness, cv2.LINE_AA)
        cv2.imshow(name, frame)

    def show(self):
        if len(self.urls) < 2:  # Url == 1
            while True:
                if self.size is not None:
                    frame_1 = self.cam[0].get_frame(self.size)
                else:
                    frame_1 = self.cam[0].get_frame(1450)  # Screen size
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
    
    def get_bytes(self):
        if len(self.urls) < 2:  # Url == 1
            while True:
                if self.size is not None:
                    frame_1 = self.cam[0].get_frame(self.size)
                else:
                    frame_1 = self.cam[0].get_frame(1450)  # Screen size
                '''
                # Face Detected
                gray = cv2.cvtColor(frame_1,cv2.COLOR_BGR2GRAY)    
                face_rects = face_cascade.detectMultiScale(gray,1.3,5)
                for (x,y,w,h) in face_rects:
                    cv2.rectangle(frame_1,(x,y),(x+w,y+h),(0,255,0),2)
                    break
                '''
                ret, jpeg = cv2.imencode('.jpg', frame_1)
                yield b'--frame\r\n'b'Content-Type:image/jpeg\r\n\r\n'+bytearray(jpeg)+b'\r\n'
        elif len(self.urls) < 3:  # Url == 2
            while True:
                if self.size is not None:
                    frame_1 = self.cam[0].get_frame(self.size)
                    frame_2 = self.cam[1].get_frame(self.size)
                else:
                    frame_1 = self.cam[0].get_frame(960)  # SCreen size / 2
                    frame_2 = self.cam[1].get_frame(960)
                img_concate_hori_1 = np.concatenate((frame_1, frame_2), axis=1)
                '''
                # Face Detected
                gray = cv2.cvtColor(img_concate_Hori_1,cv2.COLOR_BGR2GRAY)           
                face_rects = face_cascade.detectMultiScale(gray,1.3,5)
                for (x,y,w,h) in face_rects:
                    cv2.rectangle(img_concate_Hori_1,(x,y),(x+w,y+h),(0,255,0),2)
                    break
                '''
                ret, jpeg = cv2.imencode('.jpg', img_concate_hori_1)
                yield b'--frame\r\n'b'Content-Type:image/jpeg\r\n\r\n'+bytearray(jpeg)+b'\r\n'
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
                '''
                # Face Detected
                gray = cv2.cvtColor(img_concate_Line,cv2.COLOR_BGR2GRAY)           
                face_rects = face_cascade.detectMultiScale(gray,1.3,5)
                for (x,y,w,h) in face_rects:
                    cv2.rectangle(img_concate_Line,(x,y),(x+w,y+h),(0,255,0),2)
                    break
                '''
                ret, jpeg = cv2.imencode('.jpg', img_concate_line)
                yield b'--frame\r\n'b'Content-Type:image/jpeg\r\n\r\n'+bytearray(jpeg)+b'\r\n'
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
                '''
                # Face Detected
                gray = cv2.cvtColor(img_concate_Line,cv2.COLOR_BGR2GRAY)           
                face_rects = face_cascade.detectMultiScale(gray,1.3,5)
                for (x,y,w,h) in face_rects:
                    cv2.rectangle(img_concate_Line,(x,y),(x+w,y+h),(0,255,0),2)
                    break
                '''
                ret, jpeg = cv2.imencode('.jpg', img_concate_line)
                yield b'--frame\r\n'b'Content-Type:image/jpeg\r\n\r\n'+bytearray(jpeg)+b'\r\n'


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

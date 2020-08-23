from flask import Response
from source import Camera as cam


def showCamLocal(urls = None):
    if urls is None or len(urls) == 0:
        urls = ["rtsp://37.6.233.82:153/mjpeg/1"]  #    "rtsp://37.6.233.82:151/mjpeg/1",
    try:
        # screen.show()
        screen = cam.RTSP(urls, "Monitor")  # , size , 950
        screen.get_data()
    except:
        pass

def showCamWeb(urls = None):
    if urls is None or len(urls) == 0:
        urls = ["rtsp://37.6.233.82:151/mjpeg/1", "rtsp://37.6.233.82:153/mjpeg/1"]
    try:
        screen = cam.RTSP(urls)  # , size , 950
        return Response(screen.get_bytes(), mimetype = "multipart/x-mixed-replace; boundary=frame")
    except:
        # Show An Error Page
        print("Error")
        pass


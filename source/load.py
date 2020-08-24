from flask import Response
from source import Camera as cam
import cv2

# Shows local window with the rtsp url cams from 0 - 4
def showCamLocal(urls = None):
    if urls is None or len(urls) == 0:
        urls = ["rtsp://37.6.233.82:151/mjpeg/1","rtsp://37.6.233.82:153/mjpeg/1"]
    try:
        screen = cam.RTSP(urls, "Monitor")  # , size , 950
        screen.show()

    except:
        print("Error")
        pass

# Shows on server html window with the rtsp url cams from 0 - 4
def showCamWeb(urls = None):
    if urls is None or len(urls) == 0:
        urls = ["rtsp://37.6.233.82:151/mjpeg/1", "rtsp://37.6.233.82:153/mjpeg/1"]
    try:
        screen = cam.RTSP(urls, None, 1000)  # , size , 950
        return Response(screen.get_html_format(), mimetype = "multipart/x-mixed-replace; boundary=frame")
    except:
        # Show An Error Page
        print("Error")
        pass

# Shows one per time rtsp url cam
def showOneCamHTML(url):
    try:
        size = 150
        return Response(cam.RTSP.get_html_format_one(url, size), mimetype = "multipart/x-mixed-replace; boundary=frame")
    except:
        print("Error")
        pass




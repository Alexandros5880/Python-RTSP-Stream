from flask import Response
from source import Camera as cam


class Load:

    def __init__(self):
        self.rtsp = None
        self.screen = None
        self.screen_local = None

    # Setup One By One WEB
    def setup_showOneCamHTML(self, url, size_frame=1000):
        self.rtsp = cam.RTSP(url, size_frame)

    # Run One By One WEB
    def showOneCamHTML(self):
        return Response(self.rtsp.get_html_format_one(), mimetype="multipart/x-mixed-replace; boundary=frame")

    # Setup Many WEB   NOT USED
    def setup_showCamWeb(self, urls, window_name=None, size_frame=500):
        self.screen = cam.RTSPS(urls, window_name, size_frame)  # , size , 950

    # Run Many WEB     NOT USED
    def showCamWeb(self):
        return Response(self.screen.get_html_format(), mimetype="multipart/x-mixed-replace; boundary=frame")

    # Setup Many Local
    def setup_local(self, urls, window_name, size_screen=500):
        self.screen_local = cam.RTSPS(urls, window_name, size_screen)

    # Show Many Local
    def show_local(self):
        self.screen_local.show()

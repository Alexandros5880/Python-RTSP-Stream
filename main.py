from flask import Flask, render_template, request
import sys
from source import load
# Update my Global Ip in a server
from source import UpdateGlobalIp
from source import myThread
from source.myThread import scheduled

'''
import py_compile
py_compile.compile('main.py')
'''



app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

ip_s_active = []




"""
#  http://127.0.0.1:5000/set_cam
@app.route("/set_cam", methods=["GET", "POST"])  # , methods=["GET", "POST"]
def set_cam():
    try:
        global ip_s_active
        if request.method == 'POST':
            req = request.form
            if req.get('submit_btn') == "submit":
                ip1 = req.get('ip1')
                ip2 = req.get('ip2')
                ip3 = req.get('ip3')
                ip4 = req.get('ip4')
                ip_s = [ip1, ip2, ip3, ip4]
                for i in range(len(ip_s)):
                    if ip_s[i] != '':
                        ip_s_active.append(str(ip_s[i]))
                if not len(ip_s_active) == 0:
                    return render_template("index.html")
                else:
                    return render_template("Error_Message.html")
        elif request.method == 'GET':
            return render_template("set_rtsp.html")
    except:
        return render_template("Error_Message.html")
"""








# Setup Cameras
def setup_web_cameras(option):
    global load_rtsp_1
    global load_rtsp_2
    global load_rtsps
    if option == "1":
        load_rtsp_1 = load.Load()
        load_rtsp_2 = load.Load()
        load_rtsp_1.setup_showOneCamHTML("rtsp://37.6.233.82:151/mjpeg/1")
        load_rtsp_2.setup_showOneCamHTML("rtsp://37.6.233.82:153/mjpeg/1")
    elif option == "2":
        load_rtsps = load.Load()
        url_s = ["rtsp://37.6.233.82:151/mjpeg/1", "rtsp://37.6.233.82:153/mjpeg/1"]
        load_rtsps.setup_showCamWeb(url_s, None, 500)  # "Glifada House"





# Rub the server 2
#  https://trackingpackage.000webhostapp.com/?ID=221397455373948&action=getAll
#  http://37.6.233.82:5000/stream
@app.route("/stream")
def index():
    global load_rtsps
    return load_rtsps.showCamWeb()

# Rub the server 1
#  https://trackingpackage.000webhostapp.com/?ID=221397455373948&action=video_feed_1
#  http://37.6.233.82:5000/video_feed_1
@app.route("/video_feed_1")  # video_feed
def video_feed_1():
    global load_rtsp_1
    return load_rtsp_1.showOneCamHTML()

#  https://trackingpackage.000webhostapp.com/?ID=221397455373948&action=video_feed_2
#  http://37.6.233.82:5000/video_feed_2
@app.route("/video_feed_2")  # video_feed
def video_feed_2():
    global load_rtsp_2
    return load_rtsp_2.showOneCamHTML()









def startApp(host):
    app.run(host=host, debug=False)



if __name__ == '__main__':
    try:
        server = str(sys.argv[1])  # Open a window Local or start the server
        if server == "0":
            load_local = load.Load()
            urls = ["rtsp://37.6.233.82:151/mjpeg/1", "rtsp://37.6.233.82:153/mjpeg/1"]
            load_local.setup_local(urls, "Glifada House", 500)
            load_local.show_local()
            pass
        elif server == "1":  # StartThe server
            option = str(sys.argv[2])  # Open the first finction of the server veideo feed ot open the second ALL
            setup_web_cameras(option)
            # Scheduled Job every 1 hour upgrade the global ip on the get and way server PHP
            updaterIP = scheduled(1, UpdateGlobalIp.make_http_request, None)
            server = scheduled(0, app.run, '192.168.1.26')  # Threading the aplication flask server
            updaterIP.start()
            server.start()
        else:
            pass
    except:
        print("Unexpected error:", sys.exc_info()[0])
        pass



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


'''
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
'''







#  http://192.168.1.26:5000/stream
@app.route("/stream")
def index():
    try:
        # index read urls from file
        return render_template("index.html")
    except:
        return render_template("Error_Message.html")


'''
#  http://127.0.0.1:5000/
@app.route("/")  # video_feed
def video_feed():
    try:
        global ip_s_active
        return load.showCamWeb(ip_s_active)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        return render_template("Error_Message.html")
'''









load_rtsp_1 = load.Load("rtsp://37.6.233.82:151/mjpeg/1")
load_rtsp_2 = load.Load("rtsp://37.6.233.82:153/mjpeg/1")

#  http://37.6.233.82:5000/video_feed_1
@app.route("/video_feed_1")  # video_feed
def video_feed_1():
    try:
        global ip_s_active
        return load_rtsp_1.showOneCamHTML()
    except:
        print("Unexpected error:", sys.exc_info()[0])
        return render_template("Error_Message.html")

#  http://37.6.233.82:5000/video_feed_2
@app.route("/video_feed_2")  # video_feed
def video_feed_2():
    try:
        global ip_s_active
        return load_rtsp_2.showOneCamHTML()
    except:
        print("Unexpected error:", sys.exc_info()[0])
        return render_template("Error_Message.html")









def startApp(host):
    app.run(host=host, debug=False)



if __name__ == '__main__':
    try:
        arg = str(sys.argv[1])
        if arg == "0":
            #load.showCamLocal()
            pass
        elif arg == "1":
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



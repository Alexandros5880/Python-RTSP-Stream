from flask import Flask, render_template, request
import sys
from source import load


'''
import py_compile
py_compile.compile('main.py')
'''



app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

ip_s_active = []


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


#  http://127.0.0.1:5000/
@app.route("/")
def index():
    try:
        # index read urls from file
        return render_template("index.html")
    except:
        return render_template("Error_Message.html")


#  http://127.0.0.1:5000/video_feed
@app.route("/video_feed")
def video_feed():
    try:
        global ip_s_active
        return load.showCamWeb(ip_s_active)
    except:
        return render_template("Error_Message.html")


if __name__ == '__main__':
    arg = str(sys.argv[1])
    if arg == "0":
        load.showCamLocal()
    elif arg == "1":
        app.run()
    else:
        pass

#  https://rtsp-python.herokuapp.com/
#  https://rtsp-python.herokuapp.com/set_cam
#  https://rtsp-python.herokuapp.com/video_feed


#  libgl1-mesa-glx

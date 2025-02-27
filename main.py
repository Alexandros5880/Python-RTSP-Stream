#!/usr/bin/python3
from flask import Flask, render_template, request, jsonify
import sys
from source import load
# Update my Global Ip in a server
from source import UpdateGlobalIp
from source.myThread import scheduled

'''
import py_compile
py_compile.compile('main.py')
'''

# Flask object
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# Camers in ram memory
ip_s_active = []

# Urls file path
urls_data_path = "data/urls.txt"
# Users file path
users_data_path = "data/users.txt"


# Write to file 'get a list ass parameter'
def write_file(file_path, value):
    f = open(file_path, 'w')
    f.seek(0)
    for i in range(len(value)):
        f.write("%s\n" % value[i])
    f.close()


# Read from file 'return list'
def read_file(file_path):
    f = open(file_path, 'r')
    values = f.readlines()
    lines = []
    for i in range(len(values)):
        lines.insert(i, str(values[i]).rstrip())
    f.close()
    return lines


# Get the users ips
users = read_file(users_data_path)
# The current visitor
visitor = ""


#  http://192.168.1.26:5000/set_cam
@app.route("/set_cam", methods=["GET", "POST"])  # , methods=["GET", "POST"]
def set_cam():
    global visitor
    visitor = str(request.remote_addr).strip()
    if visitor in users:
        try:
            global ip_s_active
            global urls_data_path
            if request.method == 'POST':
                req = request.form
                if req.get('submit_btn') == "submit":
                    ip1 = req.get('ip1')
                    ip2 = req.get('ip2')
                    ip3 = req.get('ip3')
                    ip4 = req.get('ip4')
                    ip_s = [ip1, ip2, ip3, ip4]
                    ip_s_active.clear()  # Clear the list
                    for i in range(len(ip_s)):
                        if ip_s[i]:
                            ip_s_active.insert(i, ip_s[i])
                    print(str(ip_s_active))
                    #  Save the urls in a file
                    write_file(urls_data_path, ip_s_active)  # Write to file
                    if not len(ip_s_active) == 0:
                        opt = str(sys.argv[2])
                        setup_web_cameras(opt)
                        return render_template("index.html")
                    else:
                        return render_template("Error_Message.html")
            elif request.method == 'GET':
                return render_template("set_rtsp.html")
        except:
            pass

"""
load_rtsp_1 = ""
load_rtsp_2 = ""
load_rtsp_3 = ""
load_rtsp_4 = ""
load_rtsps = ""
"""

# Setup Cameras
def setup_web_cameras(opt):
    global load_rtsp_1
    global load_rtsp_2
    global load_rtsp_3
    global load_rtsp_4
    global load_rtsps
    global urls_data_path
    global ip_s_active
    # Get from File the Urls
    ip_s_active = read_file(urls_data_path)
    if opt == "1":
        if len(ip_s_active) == 1:
            #del load_rtsp_1
            load_rtsp_1 = load.Load()  # "rtsp://37.6.233.82:151/mjpeg/1"
            load_rtsp_1.setup_showOneCamHTML(ip_s_active[0])
        elif len(ip_s_active) == 2:
            #del load_rtsp_1
            load_rtsp_1 = load.Load()  # "rtsp://37.6.233.82:151/mjpeg/1"
            load_rtsp_1.setup_showOneCamHTML(ip_s_active[0])
            #del load_rtsp_2
            load_rtsp_2 = load.Load()  # "rtsp://37.6.233.82:153/mjpeg/1"
            load_rtsp_2.setup_showOneCamHTML(ip_s_active[1])
        elif len(ip_s_active) == 3:
            #del load_rtsp_1
            load_rtsp_1 = load.Load()  # "rtsp://37.6.233.82:151/mjpeg/1"
            load_rtsp_1.setup_showOneCamHTML(ip_s_active[0])
            #del load_rtsp_2
            load_rtsp_2 = load.Load()  # "rtsp://37.6.233.82:153/mjpeg/1"
            load_rtsp_2.setup_showOneCamHTML(ip_s_active[1])
            #del load_rtsp_3
            load_rtsp_3 = load.Load()
            load_rtsp_3.setup_showOneCamHTML(ip_s_active[2])
        elif len(ip_s_active) == 4:
            #del load_rtsp_1
            load_rtsp_1 = load.Load()  # "rtsp://37.6.233.82:151/mjpeg/1"
            load_rtsp_1.setup_showOneCamHTML(ip_s_active[0])
            #del load_rtsp_2
            load_rtsp_2 = load.Load()  # "rtsp://37.6.233.82:153/mjpeg/1"
            load_rtsp_2.setup_showOneCamHTML(ip_s_active[1])
            #del load_rtsp_3
            load_rtsp_3 = load.Load()
            load_rtsp_3.setup_showOneCamHTML(ip_s_active[2])
            #del load_rtsp_4
            load_rtsp_4 = load.Load()
            load_rtsp_4.setup_showOneCamHTML(ip_s_active[3])
    elif opt == "2":
        #del load_rtsps
        load_rtsps = load.Load()
        url_s = ip_s_active
        load_rtsps.setup_showCamWeb(url_s, None, 500)  # "Glifada House"


# Rub the server 2
#  https://trackingpackage.000webhostapp.com/?ID=221397455373948&action=getAll
#  http://37.6.233.82:5000/stream
@app.route("/stream")
def index():
    global visitor
    visitor = str(request.remote_addr)
    if any(visitor in s for s in users):
        global load_rtsps
        return load_rtsps.showCamWeb()


# Rub the server 1
#  https://trackingpackage.000webhostapp.com/?ID=221397455373948&action=video_feed_1
#  http://37.6.233.82:5000/video_feed_1
@app.route("/video_feed_1")  # video_feed
def video_feed_1():
    try:
        global visitor
        visitor = str(request.remote_addr).strip()
        if visitor in users:
            if len(ip_s_active) >= 1:
                return load_rtsp_1.showOneCamHTML()
    except:
        pass


#  https://trackingpackage.000webhostapp.com/?ID=221397455373948&action=video_feed_2
#  http://37.6.233.82:5000/video_feed_2
@app.route("/video_feed_2")  # video_feed
def video_feed_2():
    try:
        global visitor
        visitor = str(request.remote_addr).strip()
        if visitor in users:
            if len(ip_s_active) == 2:
                return load_rtsp_2.showOneCamHTML()
    except:
        pass


#  https://trackingpackage.000webhostapp.com/?ID=221397455373948&action=video_feed_3
#  http://37.6.233.82:5000/video_feed_3
@app.route("/video_feed_3")  # video_feed
def video_feed_3():
    try:
        global visitor
        visitor = str(request.remote_addr).strip()
        if visitor in users:
            if len(ip_s_active) == 3:
                return load_rtsp_3.showOneCamHTML()
    except:
        pass


#  https://trackingpackage.000webhostapp.com/?ID=221397455373948&action=video_feed_4
#  http://37.6.233.82:5000/video_feed_4
@app.route("/video_feed_4")  # video_feed
def video_feed_4():
    try:
        global visitor
        visitor = str(request.remote_addr).strip()
        if visitor in users:
            if len(ip_s_active) == 4:
                return load_rtsp_4.showOneCamHTML()
    except:
        pass


def startApp(host):
    app.run(host=host, debug=True)


if __name__ == '__main__':
    try:
        server = str(sys.argv[1])  # Open a window Local or start the server
        if server == "0":
            load_local = load.Load()  # Run Local
            print("URLS: ", str(ip_s_active))
            urls = ["rtsp://37.6.233.82:151/mjpeg/1", "rtsp://37.6.233.82:153/mjpeg/1"]
            load_local.setup_local(urls, "Glifada House", 500)
            load_local.show_local()
        elif server == "1":  # StartThe server
            option = str(sys.argv[2])  # Open the first function of the server video feed ot open the second ALL
            setup_web_cameras(option)
            # Scheduled Job every 1 hour upgrade the global ip on the get and way server PHP
            updaterIP = scheduled(1, UpdateGlobalIp.make_http_request, None)
            server = scheduled(0, app.run, '192.168.1.26')  # Threading the aplicattion flask server
            updaterIP.start()
            server.start()
        else:
            pass
    except:
        print("Unexpected error:", sys.exc_info()[0])
        pass

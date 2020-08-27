#!/usr/bin/python3
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


# Urls file path
urls_data_path = "data/urls.txt"



def write_file(file_path, value):
    f = open(file_path, "w+")
    for i in range(len(value)):
        f.write("%s\n" %value[i])
    f.close()

def read_file(file_path):
    f = open(file_path, "r+")
    values = f.readlines()
    lines = []
    for i in range(len(values)):
        lines.insert(i, str(values[i]).rstrip())
    f.close()
    return lines


#  http://192.168.1.26:5000/set_cam
@app.route("/set_cam", methods=["GET", "POST"])  # , methods=["GET", "POST"]
def set_cam():
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
                print("SAVING: " , str(ip_s))
                for i in range(len(ip_s)):
                    if ip_s[i]:
                        ip_s_active.insert(i, ip_s[i])
                print("ip_s_active: " , str(ip_s_active))
                #  Save the urls in a file
                print("WRITE TO FILE")
                write_file(urls_data_path, ip_s_active)
                if not len(ip_s_active) == 0:
                    option = str(sys.argv[2])
                    setup_web_cameras(option)
                    return render_template("index.html")
                else:
                    return render_template("Error_Message.html")
        elif request.method == 'GET':
            return render_template("set_rtsp.html")
    except:
        pass




load_rtsp_1 = None
load_rtsp_2 = None
load_rtsp_3 = None
load_rtsp_4 = None
load_rtsps = None



# Setup Cameras
def setup_web_cameras(option):
    global load_rtsp_1
    global load_rtsp_2
    global load_rtsp_3
    global load_rtsp_4
    global load_rtsps
    global urls_data_path
    global ip_s_active
    # Get from File the Urls
    ip_s_active = read_file(urls_data_path)
    print("SIZE: ", str(len(ip_s_active)))
    for i in range( len(ip_s_active) ):
        print("%s" % str(ip_s_active[i]))
    if option == "1":
        if len(ip_s_active) == 1:
            del load_rtsp_1
            load_rtsp_1 = load.Load()  #  "rtsp://37.6.233.82:151/mjpeg/1"
            load_rtsp_1.setup_showOneCamHTML(ip_s_active[0])
        elif len(ip_s_active) == 2:
            del load_rtsp_1
            load_rtsp_1 = load.Load()  # "rtsp://37.6.233.82:151/mjpeg/1"
            load_rtsp_1.setup_showOneCamHTML(ip_s_active[0])
            del load_rtsp_2
            load_rtsp_2 = load.Load()  #  "rtsp://37.6.233.82:153/mjpeg/1"
            load_rtsp_2.setup_showOneCamHTML(ip_s_active[1])
        elif len(ip_s_active) == 3:
            del load_rtsp_1
            load_rtsp_1 = load.Load()  # "rtsp://37.6.233.82:151/mjpeg/1"
            load_rtsp_1.setup_showOneCamHTML(ip_s_active[0])
            del load_rtsp_2
            load_rtsp_2 = load.Load()  #  "rtsp://37.6.233.82:153/mjpeg/1"
            load_rtsp_2.setup_showOneCamHTML(ip_s_active[1])
            del load_rtsp_3
            load_rtsp_3 = load.Load()
            load_rtsp_3.setup_showOneCamHTML(ip_s_active[2])
        elif len(ip_s_active) == 4:
            del load_rtsp_1
            load_rtsp_1 = load.Load()  # "rtsp://37.6.233.82:151/mjpeg/1"
            load_rtsp_1.setup_showOneCamHTML(ip_s_active[0])
            del load_rtsp_2
            load_rtsp_2 = load.Load()  # "rtsp://37.6.233.82:153/mjpeg/1"
            load_rtsp_2.setup_showOneCamHTML(ip_s_active[1])
            del load_rtsp_3
            load_rtsp_3 = load.Load()
            load_rtsp_3.setup_showOneCamHTML(ip_s_active[2])
            del load_rtsp_4
            load_rtsp_4 = load.Load()
            load_rtsp_4.setup_showOneCamHTML(ip_s_active[3])
    elif option == "2":
        if len(ip_s_active) == 1:
            del load_rtsp_1
            load_rtsp_1 = load.Load()  #  "rtsp://37.6.233.82:151/mjpeg/1"
            load_rtsp_1.setup_showOneCamHTML(ip_s_active[0])
        elif len(ip_s_active) == 2:
            del load_rtsp_1
            load_rtsp_1 = load.Load()  # "rtsp://37.6.233.82:151/mjpeg/1"
            load_rtsp_1.setup_showOneCamHTML(ip_s_active[0])
            del load_rtsp_2
            load_rtsp_2 = load.Load()  #  "rtsp://37.6.233.82:153/mjpeg/1"
            load_rtsp_2.setup_showOneCamHTML(ip_s_active[1])
        elif len(ip_s_active) == 3:
            del load_rtsp_1
            load_rtsp_1 = load.Load()  # "rtsp://37.6.233.82:151/mjpeg/1"
            load_rtsp_1.setup_showOneCamHTML(ip_s_active[0])
            del load_rtsp_2
            load_rtsp_2 = load.Load()  #  "rtsp://37.6.233.82:153/mjpeg/1"
            load_rtsp_2.setup_showOneCamHTML(ip_s_active[1])
            del load_rtsp_3
            load_rtsp_3 = load.Load()
            load_rtsp_3.setup_showOneCamHTML(ip_s_active[2])
        elif len(ip_s_active) == 4:
            del load_rtsp_1
            load_rtsp_1 = load.Load()  # "rtsp://37.6.233.82:151/mjpeg/1"
            load_rtsp_1.setup_showOneCamHTML(ip_s_active[0])
            del load_rtsp_2
            load_rtsp_2 = load.Load()  # "rtsp://37.6.233.82:153/mjpeg/1"
            load_rtsp_2.setup_showOneCamHTML(ip_s_active[1])
            del load_rtsp_3
            load_rtsp_3 = load.Load()
            load_rtsp_3.setup_showOneCamHTML(ip_s_active[2])
            del load_rtsp_4
            load_rtsp_4 = load.Load()
            load_rtsp_4.setup_showOneCamHTML(ip_s_active[3])
        del load_rtsps
        load_rtsps = load.Load()
        url_s = ip_s_active
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
    global ip_s_active
    if len(ip_s_active) == 1:
        return load_rtsp_1.showOneCamHTML()

#  https://trackingpackage.000webhostapp.com/?ID=221397455373948&action=video_feed_2
#  http://37.6.233.82:5000/video_feed_2
@app.route("/video_feed_2")  # video_feed
def video_feed_2():
    global load_rtsp_2
    global ip_s_active
    if len(ip_s_active) == 2:
        return load_rtsp_2.showOneCamHTML()

#  https://trackingpackage.000webhostapp.com/?ID=221397455373948&action=video_feed_3
#  http://37.6.233.82:5000/video_feed_3
@app.route("/video_feed_3")  # video_feed
def video_feed_3():
    global load_rtsp_3
    global ip_s_active
    if len(ip_s_active) == 3:
        return load_rtsp_3.showOneCamHTML()

#  https://trackingpackage.000webhostapp.com/?ID=221397455373948&action=video_feed_4
#  http://37.6.233.82:5000/video_feed_4
@app.route("/video_feed_4")  # video_feed
def video_feed_4():
    global load_rtsp_4
    global ip_s_active
    if len(ip_s_active) == 4:
        return load_rtsp_4.showOneCamHTML()







def startApp(host):
    app.run(host=host, debug=False)



if __name__ == '__main__':
    try:
        server = str(sys.argv[1])  # Open a window Local or start the server
        if server == "0":
            load_local = load.Load()  # Run Local
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



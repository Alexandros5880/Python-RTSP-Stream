excecution:    python3 main.py

Balconi:   "rtsp://37.6.233.82:151/mjpeg/1"
Camera_2:  "rtsp://37.6.233.82:153/mjpeg/1"

Flask Main Root:  http://127.0.0.1:5000/
Flask Cams Root:  http://127.0.0.1:5000/video_feed



ProckFile:
    web: gunicorn main:app
    worker: python3 main.py 0
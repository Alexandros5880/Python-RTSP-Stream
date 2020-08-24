# Instalation:
    make install-requarements
#Linux:
    make setup-lib
#Windows:
Download the libgl1-mesa-dev

# If you don't have Statis router ip:
Create a server and upload the /PHP/Global Server Aplication
on the server, setup your url ID parameter for global ip updates
and modify the: "echo ...;" with your flask url.

# Setup cameras on the application for you:
-> Open /Python-RTSP-Stream/ main.py and add a function like 
the function in line 76, change the number on the name and put one number up and put your rtsp url
-> Open /Python-RTSP-Stream/templates/index.html and modify the table with 
the same way as the example in table, add your new functions

#Excecution server Linux:
    make run-server
#Excecution Local Linux:
    make run-local
    

# Example of Flask URL:
Flask Main Root:  http://127.0.0.1:5000/
Flask Cams Root:  http://127.0.0.1:5000/video_feed
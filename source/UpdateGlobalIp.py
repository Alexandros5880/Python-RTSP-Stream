#!/usr/bin/python3
#  https://trackingpackage.000webhostapp.com/

import requests

global_ip = requests.get('http://ip.42.pl/raw').text

#  https://trackingpackage.000webhostapp.com/?ID=221397455373948
def make_http_request():
    print("Request send my global Ip")
    r = requests.get('https://trackingpackage.000webhostapp.com/?ID=221397455373948')  # /public_html/getMyDynamicIp.php
    print("Responce Status: " + str(r.status_code))
    '''
    print("Headers: " + str(r.headers))
    print("Responce: " + str(r.text))
    '''


#make_http_request()
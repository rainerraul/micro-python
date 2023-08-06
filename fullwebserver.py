import io
import sys
import machine
import socket
import network
import time
import os
import re

ssid = "kellerbereich"
password = "54826106"

adc0 = machine.ADC(machine.Pin(26))

html = """<!DOCTYPE html>
<html>
<head> <title>Pico W</title> </head>
<body> <h1>Pico W</h1>
<p></p><p><b>%1.3f V</b></p>
</body>
</html>
"""
posthtml = """
<html><head><title>post test</title></head><body>
<h3>Testdata Post</h3>
<form method='post' action='postdata.html'>
<input type='submit' name='test' value='start' />
<input type='text' name='value' value='content' />
<input type='hidden' name='dummy' value='test' />
</form>
<table border='1'><th>key</th><th>value</th><tr>
<td>%s</td><td>%s</td></tr>
<tr><td>%s</td><td>%s</td></tr></table>
</body></html>
"""

def connect_to_wlan(on, ssid = None, password = None) :
    global wait
    wait = 0
        
    wlan = network.WLAN(network.STA_IF)
    if(on == 1) :
        wlan.active(on)
        wlan.connect(ssid, password)

        while (wlan.status() != 3) :
                wait += 1
        
                if (wait == 10) :
                    print("keine Verbindung!!")
                    return False
                time.sleep(1)
        
        return True, wlan.ifconfig()

    elif(on == 0) :
        wlan.disconnect()
        return False
    
def handle_requests(req, maxpairs) :
    
    key = [" "] * maxpairs * 2
    value = [" "] * maxpairs * 2
    keyvalues = [" "] * maxpairs
    
    getdata = ""
    startGetrequest = 0
    n = 0
        
    requestlen = len(req)
    requestfile = req.split(" ", 3)
    requestfile[1] = requestfile[1][1:len(requestfile[1])]
        
    if(req.find("POST") == 2) :
        postdata = req.split('\\r\\n\\r\\n')
        keyvalues = postdata[1].split("&")
                            
    elif(req.find("GET") == 2) :
        startGetrequest = req.find("?") + 1
        requestfile1 = requestfile[1].split("?")
                
        if (startGetrequest > 0) :
            requestfile[1] = requestfile1[0]
            getdata = req[startGetrequest:(requestlen - startGetrequest)]
            keyvalues = getdata.split("&")
        
        else :
            return requestfile, key, value
             
    for n in range(0, len(keyvalues) - 1) :
        splitdata = keyvalues[n].split("=", 1)
        key[n] = splitdata[0]
        space = splitdata[1].find(" ", 1)
        value[n] = splitdata[1][0:len(splitdata[1]) - space]
    
    return  requestfile, key, value


def start_server() :
       
    if(connect_to_wlan(1, ssid, password)) :
        print("verbunden!!")
    
    addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(addr)
    server.listen(1)
    
    while True :
        response = ""
        cl, addr = server.accept()
        request = cl.recv(1024)
        request = str(request)
                   
        file, k, v = handle_requests(request, 5)
            
        if(file[1] == "index.html") :
            print(k)
            print(v)
            print(file[1])
            adc0value = ((adc0.read_u16() & 0xFFFF) / 65536) * 3.33
            response = html % (adc0value)
        
        elif(file[1] == "postdata.html") :
            print(k)
            print(v)
            print(file[1])
            response = posthtml % (k[0], v[0], k[1], v[1])
      
        cl.send("HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n")
        cl.send(response)
        cl.close()
        
try :        
    start_server()

except OSError :
    print("Error!!")
    connect_to_wlan(0)
    time.sleep(0.5)
    if(connect_to_wlan(1, ssid, password)) :
        print("reconnected!!")
    start_server()
    pass
    
    






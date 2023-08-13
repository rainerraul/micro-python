import io
import sys
import machine
import socket
import network
import time
import os

ssid = "########"
password = "########"

adc0 = machine.ADC(machine.Pin(26))
adc1 = machine.ADC(machine.Pin(27))
adc2 = machine.ADC(machine.Pin(28))

html = """<!DOCTYPE html>
<html>
<head> <title>Pico W</title> </head>
<body> <h3>Analog conversion values</h3>
<table border='1'><tr><td>ADC0</td><td><b>%1.3f V</td></tr>
<tr><td>ADC1</td><td><b>%1.3f V</td></tr>
<tr><td>ADC2</td><td><b>%1.3f V</td></tr></table>
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
scanhtml = """
<!DOCTYPE HTML><html><head><title>Scan SSID</title></head><body>
<h3>Scanresult of Infrastructure networks</h3>
<table border='1'><th>SSID</th><th>MAC</th><th>SIGNAL</th>%s</table>
<br><br>
<table border='1'><tr><td>Server IP</td><td>%s</td></tr>
<tr><td>Subnetmask</td><td>%s</td></tr>
<tr><td>Gateway</td><td>%s</td></tr>
</body></html>
"""

def connect_to_wlan(on=None, ssid=None, password=None):
    global wait
    wait = 0
    
    wlan = network.WLAN(network.STA_IF)
    wlan.active(on)
    result = wlan.scan()
        
    if on == 1:
        wlan.connect(ssid, password)

        while wlan.status() != 3:
            wait += 1

            if wait == 10:
                print("can not connect!!")
                return False, 0, result
            time.sleep(1)

    elif on == 0:
        wlan.disconnect()
        while wlan.status() > 0:
            wait += 1

            if wait == 10:
                print("disconnected")
                return False

            time.sleep(1)
        wlan.active(on)
        return False
  
    return True, wlan.ifconfig(), result


def handle_requests(req, maxpairs):

    key = [" "] * maxpairs
    value = [" "] * maxpairs
    keyvalues = [" "] * maxpairs

    getdata = ""
    startGetrequest = 0
    n = 0

    requestlen = len(req)
    requestfile = req.split(" ", 3)
    requestfile[1] = requestfile[1][1 : len(requestfile[1])]

    if req.find("POST") == 2:
        postdata = req.split("\\r\\n\\r\\n")
        keyvalues = postdata[1].split("&")

    elif req.find("GET") == 2:
        startGetrequest = req.find("?") + 1
        requestfile1 = requestfile[1].split("?")

        if startGetrequest > 0:
            requestfile[1] = requestfile1[0]
            getdata = req[startGetrequest : (requestlen - startGetrequest)]
            keyvalues = getdata.split("&")

        else:
            return requestfile, key, value

    for n in range(0, len(keyvalues) - 1):
        splitdata = keyvalues[n].split("=", 1)
        key[n] = splitdata[0]
        space = splitdata[1].find(" ", 1)
        value[n] = splitdata[1][0 : len(splitdata[1]) - space]

    return requestfile, key, value


def start_server():
    status = False
    config = 0
    scanresult = ""
    scantable = ""
    
    status, config, scanresult = connect_to_wlan(1, ssid, password)

    if status:
        print("connected!!")

    try:

        addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(addr)
        server.listen(1)

        while True:
            response = ""
            cl, addr = server.accept()
            request = cl.recv(1024)
            request = str(request)
            

            file, k, v = handle_requests(request, 5)

            if file[1] == "index.html":
                print(k)
                print(v)
                print(file[1])
                adc0value = ((adc0.read_u16() & 0xFFFF) / 65536) * 3.33
                adc1value = ((adc1.read_u16() & 0xFFFF) / 65536) * 3.33
                adc2value = ((adc2.read_u16() & 0xFFFF) / 65536) * 3.33
                
                response = html % (adc0value, adc1value, adc2value)

            elif file[1] == "postdata.html":
                print(k)
                print(v)
                print(file[1])
                response = posthtml % (k[0], v[0], k[1], v[1])
            
            elif file[1] == "scan.html":
                print()
                print(k)
                print(v)
                print(file[1])
                print()
                
                status, config, scanresult = connect_to_wlan()
                
                for result in scanresult:
                    scantable = scantable + "<tr>"
                    scantable = scantable + "<td>" + str(result[0].decode("utf8")) + "</td><td>" + str(result[1].hex(" ")) + "</td><td>" + str(result[3]) + "dB</td>"
                    scantable = scantable + "</tr>"
                
                print("Serveraddress: %s" % (config[0]))
                print("Netmask: %s" % (config[1]))
                print("Gateway: %s" % (config[2]))
                print("Clientaddress: %s" % (addr[0]))
                               
                response = scanhtml % (scantable, str(config[0]), str(config[1]), str(config[2]))
                scantable = ""

            cl.send("HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n")
            cl.send(response)
            cl.close()

    except Exception as e:
        print("exception: ", e)
        time.sleep(5)
        machine.reset()

start_server()

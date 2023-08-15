# micro-python
<h3>Examples for pico W esp32 esp8266</h3>
<b>05 08 2023</b><br>
This is a full webserver example, what can handle post and get requests, within extracting the requeststring from client in key-value Params. In addition you have to send a dummy key-value pair, because the last parameter will not be evaluated. 
<br><br>
<b>06 08 2023</b><br>
I have added a Parameter called <strong>on</strong> in function <strong>connect_to_wlan</strong> for connecting, reconnecting and disconnecting to wlan.
<br><br>
<b>13 08 2023</b><br>
Created a website <b>(scan.html)</b> containing the scanresult of infrastructure network stations and the own connection data, like serveraddress, netmask and routeraddress. The function <strong>connect_to_wlan</strong> scan also incidentally the enviroment of possible network stations. The indexfile displays the voltages, coming from the three adc channels, attached on pin26-pin28 (raspberry pico W).
<br><br>
<b>14 08 2023</b><br>
Create a website <b>mcu.html</b>, to access the GPIO Pins for writing and reading a one or zero level and also the GPIO0-Pin, where the builtin LED of raspberry pico W is connected, can be accessed, too. Only the range between Pin0-Pin28 and the "LED"-string is allowed.
<br><br>


# micropython
<!DOCTYPE html>
<html>
  <head>
  </head>
  <body>
<h3>Examples for pico W esp32 esp8266</h3>
<b>05 08 2023</b><br>
This is a full webserver example, what can handle post and get requests, within extracting the requeststring from client in key-value Params. In addition you have to send a dummy key-value pair, because the last parameter will not be evaluated. 
<br><br>
<b>06 08 2023</b><br>
I have added a Parameter called <strong>on</strong> in function <strong>connect_to_wlan</strong> for connecting, reconnecting and disconnecting to wlan.
<br><br>
<b>13 08 2023</b><br>
Created a website (scan.html) containing the scanresult of infrastructure network stations and the own connection data, like serveraddress, netmask and routeraddress. The function <strong>connect_to_wlan</strong> scan also incidentally the enviroment of possible network stations. The indexfile displays the voltage, coming from the three adc channels, attached on pin26-pin28 (raspberry pico W).
    <br><br>
  </body>
</html>

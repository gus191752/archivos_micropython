from machine import Pin
import utime
import dht

s= dht.DHT11(Pin(15))

while (True):
    s.measure()
#     temperatura= s.temperature()
#     humedad= s.humidity()
    print("temperatura: "+str(s.temperature()))
    print("humedad:" +str(s.humidity()))
    utime.sleep(2)
from machine import Pin
import utime
import dht

s= dht.DHT11(Pin(15))

while (True):
    s.measure()
    temperatura= s.temperature()
    humedad= s.humidity()
    print("temperatura: "+str(temperatura)+"°C")
    print("humedad relativa: "  +str(humedad)+"%")
    #print("T={:02f}°C,H={:02f}%".format(temperatura,humedad))
    utime.sleep(1)
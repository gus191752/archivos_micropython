from machine import Pin
import utime

trig=Pin(22,Pin.OUT)
eco= Pin(23,Pin.IN)

trig.value(0)

while (True):
    
    trig.value(1)
    utime.sleep_us(10)
    trig.value(0)
    
    t1=utime.ticks_us()
    while (eco.value()==0):
        t1=utime.ticks_us()
    while (eco.value()==1):
        t2=utime.ticks_us()
    t=t2-t1
    d=(17*t)/1000
    print("distancia: ", d,"cms")
    utime.sleep(1)
    
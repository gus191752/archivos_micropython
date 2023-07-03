import utime
import machine
import _thread
led = machine.Pin(2,machine.Pin.OUT)     ## habilita el pin 2 como salida para el led indicador

boton_sensor1= machine.Pin(22,machine.Pin.IN,machine.Pin.PULL_UP)        # entrada de señales por PULL-UP
boton_sensor2= machine.Pin(23,machine.Pin.IN,machine.Pin.PULL_UP)           # entrada de señales por PULL-UP
    
global entrada
global salida
global cont
entrada=0
salida=0
cont=0

def blink():
    led.on()                             
    utime.sleep(0.5)                         # FUNCION que hace titilar el led cuando el algoritmo envia datos
    led.off()
    utime.sleep(1)

def hilo_conteo():                          #  <<<< bucle while de trabajo >>>>
    global entrada
    global salida
    global cont         
    sensor1=int(boton_sensor1.value())          # sensa el estado del pin 22
    sensor2=int(boton_sensor2.value())                # sensa el estado del pin 23
    while (True):
        if (sensor1==0 and salida==0):
            entrada=1
        if (entrada==1 and sensor2==0):
            utime.sleep(1)
            print("entrando")
            print("*******************")
            entrada=0
            salida=0
            sensor1=1
            sensor2=1
            cont+=1
            print("cont: " + str(cont))
            print("sensor1= "+str(sensor1))
            print("sensor2= "+str(sensor2))
            print("entrada= "+str(entrada))
            print("salida= "+str(salida))
        if (sensor2==0 and entrada==0):
            salida=1
        if (salida==1 and sensor1==0):
            utime.sleep(1)
            print("saliendo")
            print("-----------------")
            entrada=0
            salida=0
            sensor1=1
            sensor2=1
            cont-=1
            print("cont: " + str(cont))
            print("sensor1= "+str(sensor1))
            print("sensor2= "+str(sensor2))
            print("entrada= "+str(entrada))
            print("salida= "+str(salida))
_thread.start_new_thread(hilo_conteo,())        
        
while (True):
    blink()
    utime.sleep(1)
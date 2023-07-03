import utime
from machine import Timer,Pin
import _thread

led = Pin(2,Pin.OUT)     ## habilita el pin 2 como salida para el led indicador

boton_sensor1= Pin(22,Pin.IN,Pin.PULL_UP)        # entrada de señales por PULL-UP
boton_sensor2= Pin(23,Pin.IN,Pin.PULL_UP)           # entrada de señales por PULL-UP
boton_continuar_hilo=Pin(21,Pin.IN,Pin.PULL_UP)

global entrada
global salida
global cont
global continuar
global sensor1
global sensor2
global cont 
entrada=0
salida=0
cont=0

def blink():
    led.on()                             
    utime.sleep(0.5)                         # FUNCION que hace titilar el led cuando el algoritmo envia datos
    led.off()
    utime.sleep(1)

def temporizador():
    global cont
    if (cont>5):
        print("van mas de 5 personas")
        print("ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ")
        cont=0

def hilo_conteo():                          #  <<<< bucle while de trabajo >>>>
    global entrada
    global salida
    global cont
    global sensor1
    global sensor2
   
    while (True):
        sensor1=int(boton_sensor1.value())          # sensa el estado del pin 22
        sensor2=int(boton_sensor2.value())                # sensa el estado del pin 23        
        utime.sleep(0.1)
        if (sensor1==0 and salida==0):
            entrada=1
        if (entrada==1 and sensor2==0):
            utime.sleep(0.5)
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
            utime.sleep(0.5)
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

# tim0 = Timer(0)
# tim0.init(mode=Timer.ONE_SHOT,period=5000,callback=lambda t:temporizador())

tim1 = Timer(1)
tim1.init(mode=Timer.PERIODIC,period=5000,callback=lambda t:temporizador())

while (True):
       
    blink()
    utime.sleep(1)
    
    
    
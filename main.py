import utime
import machine 
import _thread

led = machine.Pin(2,machine.Pin.OUT)     ## habilita el pin 2 como salida para el led indicador

boton_sensor1_puerta= machine.Pin(22,machine.Pin.IN,machine.Pin.PULL_UP)        # entrada de señales por PULL-UP
boton_sensor2_puerta= machine.Pin(23,machine.Pin.IN,machine.Pin.PULL_UP)           # entrada de señales por PULL-UP
global sensor1_puerta
global sensor2_puerta

def blink():
    led.on()                             
    utime.sleep(0.5)                         # FUNCION que hace titilar el led cuando el algoritmo envia datos
    led.off()
    utime.sleep(1)
    
def hilo_conteo_trafico():
    salida=0
    entrada=0
    while (True):
        sensor1_puerta=int(boton_sensor1_puerta.value())                # sensa el estado del pin 2
        sensor2_puerta=int(boton_sensor2_puerta.value())                # sensa el estado del pin 4
        print("entrada: " + str(entrada))
        print("salida: " + str(salida))
        print("sensor1_puerta: " + str(sensor1_puerta))
        print("sensor2_puerta: " + str(sensor2_puerta))
        utime.sleep(1)
        print("*************************************** ")
        if (sensor1_puerta==0 and salida==0):
            entrada=1
        if (entrada==1 and sensor2_puerta==0):
            utime.sleep(1)
    #        contador_trafico=(contador_trafico)+1
            print("=>Entrando")
    #        print("personas entrando: " + contador_trafico)
            entrada=0
            salida=0
            print("---------------------------------- ")
            
        if (sensor2_puerta==0 and entrada==0):
            salida=1
        if (salida==1 and sensor1_puerta==0):
            utime.sleep(1)
    #        contador_trafico=(contador_trafico)-1
            print("<=Saliendo")
            entrada=0
            salida=0
            print("////////////////////////////////////////// ")
_thread.start_new_thread(hilo_conteo_trafico,())

###########################################################################################################    

continuar=True            
while (continuar):
    
    blink()                                     # hace destellar el led de la tarjeta
    utime.sleep(2)



import utime
import machine 

boton_sensor1_puerta= machine.Pin(22,machine.Pin.IN,machine.Pin.PULL_UP)        # entrada de señales por PULL-UP
boton_sensor2_puerta= machine.Pin(23,machine.Pin.IN,machine.Pin.PULL_UP)           # entrada de señales por PULL-UP
cont=0

def int_ext(pin):
    print("ocurrio la interrupcion")
    #cont+=1
    #print("contador= "+str(cont))
    
def int_ext1(pin):
    print("ocurrio la interrupcion1")

boton_sensor1_puerta.irq(trigger=machine.Pin.IRQ_FALLING,handler=int_ext)
boton_sensor2_puerta.irq(trigger=machine.Pin.IRQ_RISING,handler=int_ext1)
         
while (True):
    utime.sleep(5)
    print("--------------------- ")
    #print("contador= "+str(cont))

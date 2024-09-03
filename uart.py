from machine import Pin, UART
import time

#   Creamos el objeto Puerto_1
#   En el cual declaramos los pines a utilizar, en este caso GPIO 18 y 19
#Puerto_1 = UART(1,9600, tx =18, rx=19)
Puerto_1 = UART(0,9600)

#   Inicializamos el PUERTO 1
Puerto_1.init(9600, bits=8, parity=None, stop=1)

#   Creamos un objeto de tipo string donde se almacenrá lo recibido en el buffer
buffer_ = ""

#   Creamos el bucle para probar el funcionamienta de RX y TX
while True:
    time.sleep_ms(1000)
    #   Enviamos por TX
    Puerto_1.write('Texto de salida')

    if Puerto_1.any() > 0:  #Si se recibe algo en RX
        
        buffer_ = Puerto_1.readline()   #Se guarda en el objeto buffer_
        
        print('Dato recibido en Puerto_1: ')    #Se imprime en CONSOLA (UART0)
        print(buffer_)

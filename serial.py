import machine
import utime

uart= machine.UART(2,9600)
uart.init(9600,bits=8,parity=None,stop=1)

dato=''
cont=0
while (True):
    
    if (uart.any()>0):
        cont=cont+1
        dato=uart.readline().decode('utf-8')         ## recibe informacion 
        #dato=uart.readline()
        print(dato)
        print("contador: "+str(cont))
        uart.write('mujica perez '+str(cont))                  ## transmite informacion
        utime.sleep(2)
        
        
        

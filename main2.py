import network
import utime
import machine 
import urequests
import gc
import esp
import urandom
import _thread

# conexion = network.WLAN(network.STA_IF)  ## crea objeto de la conexion wifi
# gc.enable()                              ## habilita el recolector de basura, limpia la memoria ram del esp32
# esp.osdebug(None)                        ## funcion avanzada para la deteccion de errores que no usaremos
# wdt=machine.WDT(timeout=90000)           ## WATCHODOG TIMER, si el sistema no lo alimenta en el tiempo estipulado reinicia la aplicacion
led = machine.Pin(2,machine.Pin.OUT)     ## habilita el pin 2 como salida para el led indicador

# boton_chiller= machine.Pin(22,machine.Pin.IN,machine.Pin.PULL_UP)        # entrada de señales por PULL-UP
# boton_acs1= machine.Pin(23,machine.Pin.IN,machine.Pin.PULL_UP)           # entrada de señales por PULL-UP
# boton_planta= machine.Pin(19,machine.Pin.IN,machine.Pin.PULL_UP)         # entrada de señales por PULL-UP
# boton_temperatura= machine.Pin(18,machine.Pin.IN,machine.Pin.PULL_UP)    # entrada de señales por PULL-UP

boton_sensor1_puerta= machine.Pin(2,machine.Pin.IN,machine.Pin.PULL_UP)        # entrada de señales por PULL-UP
boton_sensor2_puerta= machine.Pin(4,machine.Pin.IN,machine.Pin.PULL_UP)           # entrada de señales por PULL-UP

def conexion_wifi():                                   #FUNCION de conexion al wifi
    try:
        print("estableciendo conexion a la red")
        conexion.active(True)                          # activa la conexion al wifi 
        lista = conexion.scan()                        # scanea las redes wifi disponibles
        for red in lista:
            print(red[0].decode())                     # crea una lista con las redes disponibles
        conexion.connect("TP-Link_A3C8","77131478")    # se conecta a la red, se debe ingresar aqui usuario y clave de la red conocida
#        conexion.connect("prueba","12345678")
#        conexion.connect("gus","854317gm")
        while not conexion.isconnected():
            print(".")                                 # mientras no haya coneccion imprime un .
            utime.sleep(1)            
        print(conexion.ifconfig())                     # devuelve los valores de la conexion (direccion ip, mascara, dns, etc)
        print(conexion.config("mac"))
    except:                                            # si la tarjeta detecta un error
        print("error en la conexion")
        utime.sleep(3)                                 # espera 3 seg
        conexion.disconnect()                          # se desconecta de la red
        utime.sleep(6)                                 # espera 6 seg para cerrar totalmente
        print("... reconectando")
        continuar1=False                               # rompe el bucle while principal

def blink():
    led.on()                             
    utime.sleep(0.5)                         # FUNCION que hace titilar el led cuando el algoritmo envia datos
    led.off()
    utime.sleep(1)
    
def hilo_conteo_trafico():
    salida=0
    entrada=0
    sensor1_puerta=int(boton_sensor1_puerta.value())                # sensa el estado del pin 2
    sensor2_puerta=int(boton_sensor2_puerta.value())                # sensa el estado del pin 4
    while True
        if (sensor1_puerta==1 and salida==0):
            entrada=1
        if (entrada==1 and sensor2_puerta==1):
    #        contador_trafico=(contador_trafico)+1
            print("=>Entrando")
    #        print("personas entrando: " + contador_trafico)
            print("entrada: " + str(entrada))
            print("salida: " + str(salida))
            print("sensor1_puerta: " + str(sensor1_puerta))
            print("sensor2_puerta: " + str(sensor2_puerta))
            entrada=0
            salida=0
            #utime.sleep(1)
            print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX ")
        if (sensor2_puerta==1 and entrada==0):
            salida=1
        if (salida==1 and sensor1_puerta==1):
    #        contador_trafico=(contador_trafico)-1
            print("<=Saliendo")
            entrada=0
            salida=0
            #utime.sleep(1)
_thread.start_new_thread(hilo_conteo_trafico,())

###########################################################################################################    

global continuar1                                     # se declaran las variables
global continuar2
continuar1=True    # bandera del bucle de conexion al wifi
continuar2=False   # bandera del bucle de trabajo
contador=0         # contador de envios fallidos del metodo post
contador2=0        # contador de recepciones fallidas del metodo get
contador3=0        # contador de envios exitosos del metodo post
         
contador_trafico=0


# while (continuar1):                              #  <<<< bucle while principal >>>>
#     conexion_wifi()                                     # activa la conexion al wifi
#     if (conexion.isconnected()):                        # si la conexion esta correcta activa la bandera del bucle de trabajo
#         continuar2=True            
#     while (continuar2):                          #  <<<< bucle while de trabajo >>>>
  
continuar2=True            
while (continuar2):  
  
#         dato_tarjeta='tarjeta5'                     #       <<<==========   nombre de la tarjeta desde donde se envian los datos      
#         chiller=int(boton_chiller.value())          # sensa el estado del pin 22
#         asc1=int(boton_acs1.value())                # sensa el estado del pin 23
#         planta=int(boton_planta.value())            # sensa el estado del pin 19
#         temperatura=int(boton_temperatura.value())  # sensa el estado del pin 18
#
    
    
#             
#         print("boton_chiller= "+str(chiller))
#         print("boton_asc= "+str(asc1))
#         print("boton_planta= "+str(planta))
#         print("boton_temperatura= "+str(temperatura))
#     
#         gc.collect()                                # limpia la basura de la memoria ram
#         print(gc. mem_free ( ))                     # imprime cuanta memoria hay disponible
#
    blink()                                     # hace destellar el led de la tarjeta
    utime.sleep(2)
########################################################  METODO GET  #########################################       
#         try:
#             print("realizando peticion GET")            
#             peticion=urequests.get('https://ingenieriamcy.000webhostapp.com/prueba_recibe2.php')  # envia la solicitud a la pagina indicada
#             utime.sleep(10)
#             print(peticion.status_code)                                                          # codigo de respuesta de la pagina
#             print(peticion.text)                                                                 # sin esta linea el codigo da error
#         except:
#             print("====>no hay respuesta GET")
#             contador2=contador2+1
#             print(str(contador2) + " de intentos de solicitud fallida")            
#             if ((contador2)>4):
#                 print("...reiniciando conexion")
#                 conexion.disconnect()
#                 utime.sleep(10)
#                 continuar2=False
#                 contador2=0            
######################################################### METODO POST  #####################################################################
#         try: 
#             dato= ('&device_label='+ str(dato_tarjeta) + '&chiller='+ str(chiller) + '&ascensor1='+ str(asc1) + '&planta_sur='+ str(planta) + '&temperature='+str(temperatura))  # datos a enviar al formulario del host
#             datos=dato
#             print("realizando peticion POST")
#             cabezera={'Content-Type':'application/x-www-form-urlencoded'}    # cabezera de la pagina a enviar los datos del formulario                                                                                                                    # tiempo de muestreo
#             
#             
#             #envio_datos= urequests.post('https://ingenieriamcy.000webhostapp.com/prueba_recibe2.php',data=datos,headers=cabezera)  # envio de datos metodo post
#             envio_datos= urequests.post('https://iotgus.000webhostapp.com//prueba_recibe2.php',data=datos,headers=cabezera)  # envio de datos metodo post
#             
# 
#             utime.sleep(10)
#             print(envio_datos.status_code)  # imprime codigo de respuesta
#             print(envio_datos.text)         # imprime la respuesta de la pagina
#             contador3=contador3+1
#             print("================================>"+ str(contador3)+" envios exitosos")                       
#         except:
#             print("====>no hay respuesta POST")            
#             contador=contador+1
#             print(str(contador) + " de intentos de envios fallidos")
#             utime.sleep(10)
#             if ((contador)>4):                                 # si el numero de intentos de envios post fallidos supera lo establecido
#                 print("...reiniciando conexion")            
#                 conexion.disconnect()                          # se desconecta del wifi
#                 utime.sleep(10)                                # espera 10 seg
#                 continuar2=False                               # rompe el bucle de trabajo
#                 contador=0                                     # vuelve a cero el contador de envios fallidos
# ###########################################################################################################################  
#         wdt.feed()                               # <<<<====  activa el impulso para el watchdog timer "IMPORTANTISIMO", fin del programa

import network
import utime
import machine 
import urequests
import gc
import esp

conexion = network.WLAN(network.STA_IF)  ## crea objeto de la conexion wifi
gc.enable()                              ## habilita el recolector de basura, limpia la memoria ram del esp32
esp.osdebug(None)                        ## funcion avanzada para la deteccion de errores que no usaremos
wdt=machine.WDT(timeout=90000)           ## WATCHODOG TIMER, si el sistema no lo alimenta en el tiempo estipulado reinicia la aplicacion
led = machine.Pin(2,machine.Pin.OUT)     ## habilita el pin 2 como salida para el led indicador

boton_energizado_asc_corp= machine.Pin(22,machine.Pin.IN,machine.Pin.PULL_UP)                 # entrada de señales por PULL-UP
boton_funcionamiento_asc_corp= machine.Pin(21,machine.Pin.IN,machine.Pin.PULL_UP)             # entrada de señales por PULL-UP
boton_falla_asc_corp= machine.Pin(18,machine.Pin.IN,machine.Pin.PULL_UP)                      # entrada de señales por PULL-UP
                                        

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
###########################################################################################################    

global continuar1                                     # se declaran las variables
global continuar2
continuar1=True    # bandera del bucle de conexion al wifi
continuar2=False   # bandera del bucle de trabajo
contador=0         # contador de envios fallidos del metodo post
contador2=0        # contador de recepciones fallidas del metodo get
contador3=0        # contador de envios exitosos del metodo post

######### tarjeta 1 #######
compresor1_chiller1=0
compresor2_chiller1=0
compresor3_chiller1=0
flujo_chiller1=0
temperatura_chiller1=0
######### tarjeta 2 #######
compresor1_chiller2=0
compresor2_chiller2=0
compresor3_chiller2=0
flujo_chiller2=0
switch_chiller2=0
corpoelec_440v=0
######### tarjeta 3 #######
switch_bomba1_chiller=0
motor_bomba1_chiller=0
falla_bomba1_chiller=0
switch_bomba2_chiller=0
motor_bomba2_chiller=0
falla_bomba2_chiller=0
switch_bomba3_chiller=0
motor_bomba3_chiller=0
falla_bomba3_chiller=0
######### tarjeta 4 #######
switch_uma40ton=0
motor_uma40ton=0
falla_uma40ton=0
reloj_uma40ton=0
######### tarjeta 5 #######
chiller=0
asc1=0
planta=0
temperatura=0
######### tarjeta 6 #######
switch_extractor1=0
motor_extractor1=0
falla_extractor1=0
reloj_estractor1=0
######### tarjeta 7 #######
switch_extractor2=0
motor_extractor2=0
falla_extractor2=0
reloj_extractor2=0
corpoelec_220v=0
######### tarjeta 8 #######
#energizado_asc_corp=0
#funcionamiento_asc_corp=0
#falla_asc_corp=0
######### tarjeta 9 #######
energizado_asc_lobbynorte=0
funcionamiento_asc_lobbynorte=0
falla_asc_lobbynorte=0
######### tarjeta 10 #######
energizado_asc_lobbysur=0
funcionamiento_asc_lobbysur=0
falla_asc_lobbysur=0
######### tarjeta 11 #######
energizado_asc_carganorte=0
funcionamiento_asc_carganorte=0
falla_asc_carganorte=0
######### tarjeta 12 #######
reloj_uma_sala17=0
motor_uma_sala17=0
falla_uma_sala17=0
## en total 52 variables programadas #######################


while (continuar1):                              #  <<<< bucle while principal >>>>
    conexion_wifi()                                     # activa la conexion al wifi
    if (conexion.isconnected()):                        # si la conexion esta correcta activa la bandera del bucle de trabajo
        continuar2=True            
    while (continuar2):                          #  <<<< bucle while de trabajo >>>>
        
        dato_tarjeta='tarjeta8'                     #       <<<==========   nombre de la tarjeta desde donde se envian los datos      
        energizado_asc_corp=int(boton_energizado_asc_corp.value())          # sensa el estado del pin 22
        funcionamiento_asc_corp=int(boton_funcionamiento_asc_corp.value())                # sensa el estado del pin 23
        falla_asc_corp=int(boton_falla_asc_corp.value())            # sensa el estado del pin 19
        
       
        print("energizado= "+str(energizado_asc_corp))
        print("funcionamiento= "+str(funcionamiento_asc_corp))
        print("falla= "+str(falla_asc_corp))
    
        gc.collect()                                # limpia la basura de la memoria ram
        print(gc. mem_free ( ))                     # imprime cuanta memoria hay disponible
        
        blink()                                     # hace destellar el led de la tarjeta
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
        try:
            
            #dato= ('&device_label='+ str(dato_tarjeta) + '&chiller='+ str(chiller) + '&ascensor1='+ str(asc1) + '&planta_sur='+ str(planta) + '&temperature='+str(temperatura)+ '&compresor1_chiller1='+ str(compresor1_chiller1) + '&compresor2_chiller1='+ str(compresor2_chiller1) + '&compresor3_chiller1='+ str(compresor3_chiller1) +'&flujo_chiller1='+ str(flujo_chiller1) + '&temperatura_chiller1='+str(temperatura_chiller1)+ '&energizado_asc_corp='+ str(energizado_asc_corp) +'&funcionamiento_asc_corp='+ str(funcionamiento_asc_corp) + '&falla_asc_corp='+str(falla_asc_corp))  # datos a enviar al formulario del host
#             dato= ('&device_label='+ str(dato_tarjeta) + '&chiller='+ str(chiller) + '&ascensor1='+ str(asc1) + '&planta_sur='+ str(planta) + '&temperature='+str(temperatura)+
#                    '&compresor1_chiller1='+ str(compresor1_chiller1) + '&compresor2_chiller1='+ str(compresor2_chiller1) + '&compresor3_chiller1='+ str(compresor3_chiller1) +'&flujo_chiller1='+ str(flujo_chiller1) + '&temperatura_chiller1='+str(temperatura_chiller1)+
#                    '&compresor1_chiller2='+ str(compresor1_chiller2) + '&compresor2_chiller2='+ str(compresor2_chiller2) + '&compresor3_chiller2='+ str(compresor3_chiller2) +'&flujo_chiller2='+ str(flujo_chiller2) + '&switch_chiller2='+str(switch_chiller2)+'&corpoelec_440v='+str(corpoelec_440v) +
#                    '&energizado_asc_corp='+ str(energizado_asc_corp) + '&funcionamiento_asc_corp='+ str(funcionamiento_asc_corp) + '&falla_asc_corp='+str(falla_asc_corp))
#

            dato= ('&device_label='+ str(dato_tarjeta) + '&compresor1_chiller1='+ str(compresor1_chiller1) + '&compresor2_chiller1='+ str(compresor2_chiller1) + '&compresor3_chiller1='+ str(compresor3_chiller1) +'&flujo_chiller1='+ str(flujo_chiller1) + '&temperatura_chiller1='+str(temperatura_chiller1) +
                   '&compresor1_chiller2='+ str(compresor1_chiller2) + '&compresor2_chiller2='+ str(compresor2_chiller2) + '&compresor3_chiller2='+ str(compresor3_chiller2) +'&flujo_chiller2='+ str(flujo_chiller2) + '&switch_chiller2='+str(switch_chiller2)+'&corpoelec_440v='+str(corpoelec_440v) +
                   '&switch_bomba1_chiller='+str(switch_bomba1_chiller)+'&motor_bomba1_chiller='+str(motor_bomba1_chiller) + '&falla_bomba1_chiller='+str(falla_bomba1_chiller) + '&switch_bomba2_chiller='+str(switch_bomba2_chiller) + '&motor_bomba2_chiller='+str(motor_bomba2_chiller) + '&falla_bomba2_chiller='+str(falla_bomba2_chiller) + '&switch_bomba3_chiller='+str(switch_bomba3_chiller) + '&motor_bomba3_chiller='+str(motor_bomba3_chiller) + '&falla_bomba3_chiller='+str(falla_bomba3_chiller) +
                   '&switch_uma40ton='+str(switch_uma40ton) + '&motor_uma40ton='+str(motor_uma40ton) + '&falla_uma40ton='+str(falla_uma40ton) + '&reloj_uma40ton='+str(reloj_uma40ton) +
                   '&chiller='+ str(chiller) + '&ascensor1='+ str(asc1) + '&planta_sur='+ str(planta) + '&temperature='+str(temperatura) +
                   '&switch_extractor1='+str(switch_extractor1) + '&motor_extractor1='+str(motor_extractor1) + '&falla_extractor1='+str(falla_extractor1) + '&reloj_estractor1='+str(reloj_estractor1) +
                   '&switch_extractor2='+str(switch_extractor2) + '&motor_extractor2='+str(motor_extractor2) + '&falla_extractor2='+str(falla_extractor2) + '&reloj_extractor2='+str(reloj_extractor2) + '&corpoelec_220v='+str(corpoelec_220v) +                  
                   '&energizado_asc_corp='+ str(energizado_asc_corp) + '&funcionamiento_asc_corp='+ str(funcionamiento_asc_corp) + '&falla_asc_corp='+str(falla_asc_corp) +
                   '&energizado_asc_lobbynorte='+str(energizado_asc_lobbynorte) + '&funcionamiento_asc_lobbynorte='+str(funcionamiento_asc_lobbynorte) + '&falla_asc_lobbynorte='+str(falla_asc_lobbynorte) +
                   '&energizado_asc_lobbysur='+str(energizado_asc_lobbysur) + '&funcionamiento_asc_lobbysur='+str(funcionamiento_asc_lobbysur) + '&falla_asc_lobbysur='+str(falla_asc_lobbysur) +
                   '&energizado_asc_carganorte='+str(energizado_asc_carganorte) + '&funcionamiento_asc_carganorte='+str(funcionamiento_asc_carganorte) + '&falla_asc_carganorte='+str(falla_asc_carganorte) +
                   '&reloj_uma_sala17='+str(reloj_uma_sala17) + '&motor_uma_sala17='+str(motor_uma_sala17) + '&falla_uma_sala17='+str(falla_uma_sala17)
                   )
         

            datos=dato
            print("realizando peticion POST")
            cabezera={'Content-Type':'application/x-www-form-urlencoded'}    # cabezera de la pagina a enviar los datos del formulario                                                                                                                    # tiempo de muestreo
            
            
            #envio_datos= urequests.post('https://ingenieriamcy.000webhostapp.com/prueba_recibe2.php',data=datos,headers=cabezera)  # envio de datos metodo post
            envio_datos= urequests.post('https://iotgus.000webhostapp.com//prueba_recibe2.php',data=datos,headers=cabezera)  # envio de datos metodo post
            

            utime.sleep(10)
            print(envio_datos.status_code)  # imprime codigo de respuesta
            print(envio_datos.text)         # imprime la respuesta de la pagina
            contador3=contador3+1
            print("================================>"+ str(contador3)+" envios exitosos")                       
        except:
            print("====>no hay respuesta POST")            
            contador=contador+1
            print(str(contador) + " de intentos de envios fallidos")
            utime.sleep(10)
            if ((contador)>4):                                 # si el numero de intentos de envios post fallidos supera lo establecido
                print("...reiniciando conexion")            
                conexion.disconnect()                          # se desconecta del wifi
                utime.sleep(10)                                # espera 10 seg
                continuar2=False                               # rompe el bucle de trabajo
                contador=0                                     # vuelve a cero el contador de envios fallidos
###########################################################################################################################  
        wdt.feed()                               # <<<<====  activa el impulso para el watchdog timer "IMPORTANTISIMO", fin del programa

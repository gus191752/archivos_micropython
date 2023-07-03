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

led = machine.Pin(2,machine.Pin.OUT)     ## habilita el pin 2  y pin 23 como salida 
tin= machine.Pin(23,machine.Pin.OUT)

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


while (continuar1):                              #  <<<< bucle while principal >>>>
    conexion_wifi()                                     # activa la conexion al wifi
    if (conexion.isconnected()):                        # si la conexion esta correcta activa la bandera del bucle de trabajo
        continuar2=True            
    while (continuar2):                          #  <<<< bucle while de trabajo >>>>
        
        gc.collect()                                # limpia la basura de la memoria ram
        print(gc. mem_free ( ))                     # imprime cuanta memoria hay disponible
        
        #blink()                                     # hace destellar el led de la tarjeta
########################################################  METODO GET  #########################################       
        try:
            print("realizando peticion GET")            
            #peticion=urequests.get('https://ingenieriamcy.000webhostapp.com/prueba_recibe2.php')  # envia la solicitud a la pagina indicada           
            peticion= urequests.get('https://iotgus.000webhostapp.com/prueba_recibe2.php')
            
            utime.sleep(10)
            print(peticion.status_code)                                                          # codigo de respuesta de la pagina
            print(peticion.text)
            
            ############################################ falla asc corp############################
            x=peticion.text.find("Afalla_asc_corp")
            print(x)
            inicio=(peticion.text.find("Afalla_asc_corp")+len("Afalla_asc_corp")+1)
            fin=(peticion.text.find("Afalla_asc_corp")+len("Afalla_asc_corp")+2)
            Afalla_asc_corp= int(peticion.text[inicio:fin])
            print("Afalla_asc_corp= ",Afalla_asc_corp)
            
            if (Afalla_asc_corp==1):
                led.on()
            if (Afalla_asc_corp==0):
                led.off()
            ############################################ temperatura ############################
            y=peticion.text.find("Atemperatura")
            print(y)
            inicioy=(peticion.text.find("Atemperatura")+len("Atemperatura")+1)
            finy=(peticion.text.find("Atemperatura")+len("Atemperatura")+3)
            Atemperatura = int(peticion.text[inicioy:finy])
            print("Atemperatura= ",Atemperatura)
            
            if (Atemperatura<27):
                tin.on()
            if (Atemperatura>27):
                tin.off()
            ########################################################################    
            #utime.sleep(60)
            # sin esta linea el codigo da error
        except:
            print("====>no hay respuesta GET")
            contador2=contador2+1
            print(str(contador2) + " de intentos de solicitud fallida")            
            if ((contador2)>4):
                print("...reiniciando conexion")
                conexion.disconnect()
                utime.sleep(10)
                continuar2=False
                contador2=0            
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
###########################################################################################################################  
        wdt.feed()                               # <<<<====  activa el impulso para el watchdog timer "IMPORTANTISIMO", fin del programa
      
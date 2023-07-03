from machine import Pin
import onewire
import utime
import ds18x20
import binascii

ow=onewire.OneWire(Pin(23))
ds=ds18x20.DS18X20(ow)
roms=ds.scan()

while (True):
    ds.convert_temp()
    utime.sleep(1)
    for rom in roms:
        idhex=binascii.hexlify(rom)
        #print("id=",idhex)
        temperatura=ds.read_temp(rom)
        print("temperatura="+str(temperatura))
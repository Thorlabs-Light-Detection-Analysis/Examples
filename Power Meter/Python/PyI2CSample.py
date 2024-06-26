from PyTLPMX import TLPMX
import sys
import time

#Sample for Sensor HDC1080

# Standard address of the HDC sensor: hex number
HDC_ADDR = 128

# Registers storing temperature and humidity (see data sheet):
TMP_REG = "00"
HUM_REG = "01"

# Measurment frequency in seconds:
DELAY = 2

def init_i2C():
    inst = TLPMX()

    deviceCount = inst.findRsrc()

    print("devices found: " + str(deviceCount))
    
    found = False
    resourceName = ""
    for i in range(0, deviceCount):
        localName = inst.getRsrcName( i)
        print(localName)
        resourceName = localName
        found = True
        break

    inst.close()

    if(found == False):
         print('Power meter not found')
         sys.exit()

    inst = TLPMX(resourceName, True, False)

    inst.writeRaw("*IDN?\n")
    print(inst.readRaw(1024))
    time.sleep(1)
    #set mode to SLOW to start measurement.
    inst.setI2CMode(1)

    return inst


def get_temperature():
    # Point to temperature register:
    inst.I2CWrite(HDC_ADDR, TMP_REG)
    # Hold on (conversion time, data sheet):
    time.sleep(0.0635)
    # Read two bytes:
    tmp_bytes = inst.I2CRead(HDC_ADDR, 2) 
    tmp_deg_c = (tmp_bytes / 2**16) * 165 - 40
    return(tmp_deg_c)


def get_humidity():  
    # Point to humidity register:
    inst.I2CWrite(HDC_ADDR, HUM_REG)
    # Hold on (conversion time, data sheet):
    time.sleep(0.065)
    # Read two bytes:
    hum_bytes = inst.I2CRead(HDC_ADDR, 2) 
    hum_p_rel = (hum_bytes / 2**16) * 100
    return(hum_p_rel)
  
def log_data(): 
    count = 0
    while count < 10:   
        tmp_deg_c = get_temperature()
        hum_p_rel = get_humidity()
        # print data 
        print('{:.2f} °C'.format(tmp_deg_c))
        print('{:.2f} percent rel. humidity'.format(hum_p_rel))
        time.sleep(DELAY)
        count+=1
 
if __name__ == "__main__":
    inst = init_i2C()
    log_data()
    #IMPORTANT: set mode to INTER again. This enables the power meter to use the I2C sensor again.
    inst.setI2CMode(0)
    inst.close()

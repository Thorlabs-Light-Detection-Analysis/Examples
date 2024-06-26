from PyTLPMX import TLPMX
import time
 
tlPM = TLPMX()

deviceCount = tlPM.findRsrc()

print("devices found: " + str(deviceCount))
 
resourceName = ""
for i in range(0, deviceCount):
    localName = tlPM.getRsrcName( i)
    print(localName)
    resourceName = localName
    break

tlPM.close()
  
tlPM = TLPMX(resourceName, True, False)
 
message = tlPM.getCalibrationMsg()
print( message)

time.sleep(1)
 
times = []
count = 0
while count < 20: 
    power = tlPM.measPower() 
    print(power)
    count+=1
    time.sleep(0.2)

tlPM.writeRaw("*IDN?\n")
rawValue = tlPM.readRaw(1024)

print(rawValue)

tlPM.close()
print('End program')

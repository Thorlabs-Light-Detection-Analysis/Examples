
from datetime import datetime 
from PyTLPMX import TLPMX
from ctypes import c_float, c_int
import time 
 
#Only for PM103 and PM5020

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
 
tlPM.setFreqMode(0)
#auto range must be set to false before finding the range and trigger level.
tlPM.setCurrentAutoRange(False)
#Input filter state must be set to high before finding the range and trigger level.
tlPM.setInputFilterState(False)

time.sleep(1)

tlPM.setFreqMode(1)

#Start autoset
tlPM.startPeakDetector()

isRunning = True
while isRunning:
    time.sleep(1)
    isRunning = tlPM.isPeakDetectorRunning()
 
tlPM.setFreqMode(0)

trgSource = 1
averaging = 1
horPos = 0 
tlPM.confCurrentMeasurementSequenceHWTrigger(trgSource, averaging, horPos) 
 
autoTriggerDelay = 0
triggerForced = tlPM.startMeasurementSequence(autoTriggerDelay)

baseTime = 10
dataSize = baseTime * 100

timeStamps = (c_float * dataSize)()
data = (c_float * dataSize)()  
tlPM.getMeasurementSequence(baseTime, timeStamps, data, None)

with open("CurrentData.csv", "w") as txt_file:
	for i in range(dataSize):
		txt_file.write("{:.3f}".format(timeStamps[i]) + ";" + "{:.5e}".format(data[i]) + "\n")
 
tlPM.close()
print('End program')

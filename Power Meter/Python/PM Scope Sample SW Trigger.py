from datetime import datetime
from ctypes import cdll,c_long, c_ulong, c_uint16, c_uint32,byref,create_string_buffer,c_bool,c_char_p,c_int,c_int16,c_double,c_float, sizeof, c_voidp
from TLPMX import TLPMX
import time
import csv

from TLPMX import TLPM_DEFAULT_CHANNEL

#Only for PM103 and PM5020

tlPM = TLPMX()
deviceCount = c_uint32()
tlPM.findRsrc(byref(deviceCount))

print("devices found: " + str(deviceCount.value))

resourceName = create_string_buffer(1024)

for i in range(0, deviceCount.value):
    tlPM.getRsrcName(c_int(i), resourceName)
    print(c_char_p(resourceName.raw).value)
    break

tlPM.close()

tlPM = TLPMX()
#resourceName = create_string_buffer(b"COM1::115200")
#print(c_char_p(resourceName.raw).value)
tlPM.open(resourceName, c_bool(True), c_bool(False))

#Set to CW mode 
tlPM.setFreqMode(0, TLPM_DEFAULT_CHANNEL)
#auto range must be set to false before finding the range and trigger level.
tlPM.setCurrentAutoRange(c_bool(False), TLPM_DEFAULT_CHANNEL)
#Input filter state must be set to high before finding the range and trigger level.
tlPM.setInputFilterState(c_bool(False), TLPM_DEFAULT_CHANNEL)
 
time.sleep(1)

tlPM.setFreqMode(1, TLPM_DEFAULT_CHANNEL)

#Start autoset
tlPM.startPeakDetector(TLPM_DEFAULT_CHANNEL)
time.sleep(1)

isRunning = c_bool(True)
while isRunning.value:
	tlPM.isPeakDetectorRunning(byref(isRunning), TLPM_DEFAULT_CHANNEL)
	
tlPM.setFreqMode(0, TLPM_DEFAULT_CHANNEL)
#End autoset

averaging = c_uint32(1) 
tlPM.confCurrentMeasurementSequence(averaging, TLPM_DEFAULT_CHANNEL) 

triggerForced = c_bool(True)
autoTriggerDelay = c_uint16(0)
tlPM.startMeasurementSequence(autoTriggerDelay, byref(triggerForced))

baseTime = c_int(10)
dataSize = baseTime.value * 100

timeStamps = (c_float * dataSize)()
currentData = (c_float * dataSize)()

tlPM.getMeasurementSequence(baseTime, timeStamps, currentData, None)

with open("CurrentData.csv", "w") as txt_file:
	for i in range(dataSize):
		txt_file.write("{:.3f}".format(timeStamps[i]) + ";" + "{:.5e}".format(currentData[i]) + "\n")
 
tlPM.close()
print('End program')

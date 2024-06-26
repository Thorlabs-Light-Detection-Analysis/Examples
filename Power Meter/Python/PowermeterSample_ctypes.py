# -*- coding: utf-8 -*-
"""
Uses the Thorlabs TLPMX_64.dll in order to communicate with the power meters
"""
import os
from ctypes import *
from datetime import datetime
import time

# load the DLL- if your path is different, this may need to change.
#os.add_dll_directory(r"C:\Program Files\IVI Foundation\VISA\Win64\Lib_x64\msc")
lib = cdll.LoadLibrary("C:\Program Files\IVI Foundation\VISA\Win64\Bin\TLPMX_64.dll")

# find out if there are devices connected
deviceCount = c_ulong()
lib.TLPMX_findRsrc(0, byref(deviceCount))

# if there are devices connected, determine their names
if deviceCount.value >= 1:
    meterName = create_string_buffer(256)


    # if there's only one device, open it- otherwise, ask which one
    if deviceCount.value == 1:
        lib.TLPMX_getRsrcName(0, 0, meterName)
    else:
        print("Which Device?")
        for i in range(deviceCount.value):
            lib.TLPMX_getRsrcName(0, i, meterName)
            print('#' + str(i + 1) + " " + meterName.value)
        device_num = input(">>>")
        lib.TLPMX_getRsrcName(0, (device_num - 1), meterName)

    # Initialize the device- see manual for description of what arguments do
    sessionHandle = c_ulong(0)
    lib.TLPMX_init(meterName, 1, 0, byref(sessionHandle))


    wavelength=c_double()
    # Set Wavelength (given in nm)
    lib.TLPMX_setWavelength(sessionHandle, c_double(1064.0), 1);
    # Set Averaging count
    lib.TLPMX_setAvgCnt(sessionHandle, c_ushort(1000), 1)
    # Set Unit- below sets to Watts
    lib.TLPMX_setPowerUnit(sessionHandle, 0, 1)
    # Measure Power
    power = c_longdouble()
    lib.TLPMX_measPower(sessionHandle, byref(power), 1)
    print('Power: ' + str(power.value) + " W")


    

    # close
    lib.TLPMX_close(sessionHandle)
else:
    print("No connected power meters were detected. Check connections and installed drivers.")

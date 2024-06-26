/****************************************************************************

   Thorlabs PM100x/PM10x/PM160/PM200/PM400/PM5020 Driver Sample Application

   Source file

   Date:          Jan-25-2022
   Version:       1.1.0
   Copyright:     Copyright(c) 2022, Thorlabs GmbH (www.thorlabs.com)

   Disclaimer:

   This program is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 2 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program; if not, write to the Free Software
   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA


   How to setup the compiler project
   =================================
   
   1. Requirements:
      +  Thorlabs TLPM Instrument Driver installed.
            After installation the driver files can be found in 
            "$(VXIPNPPATH)WinNT\"
            This is typically 'C:\VXIPNP\WinNT\' or 
            'C:\Program Files\IVI Foundation\VISA\WinNT\'
   
   2. Create a new project in your IDE.
   
   3. Add the following files to the project:
      +  sample.c
      +  TLPMX.h
   
   4. The IDE needs to be pointed to these .LIB files:
      +  TLPMX_32.lib
      Some IDEs need the .LIB files added to the project. Others require
      different steps. Please refer to your compiler manual.
   
   5. Depending on your compiler you may need to set your compiler include 
      search path to the VXIPNP include directory.
      This is typically 'C:\VXIPNP\WinNT\include' or 
      'C:\Program Files\IVI Foundation\VISA\WinNT\include'
      
   6. Project settings in Microsoft Visual Studio C++:
      To use the Thorlabs PM100x Series VISA Instrument Driver successfully 
      in a Visual C++ project some paths and dependencies have to be included
      in the Project settings (both, in Debug and in Release configuration).
      +  Configuration > C/C++ > General settings: Additional include 
         directories: "$(VXIPNPPATH)WinNT\include"
      +  Configuration > Linker > General settings: Additional library 
         directories: "$(VXIPNPPATH)WinNT\lib\msc"
      +  Configuration > Linker > Input: Additional dependencies: 
         "TLPMX_32.lib"
                                    
   
****************************************************************************/
#ifdef _WIN32
	#ifndef _WIN32_WINNT
		#define _WIN32_WINNT 0x600
	#endif 


#ifndef _MSC_VER
#define _MSC_VER 1000
#endif 
	#include <windows.h>
#endif

#include "TLPMX.h"
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

/*===========================================================================
 Type definitions
===========================================================================*/

/*===========================================================================
 Macros
===========================================================================*/
#define NUM_MULTI_READING  1000


#ifndef VI_ERROR_RSRC_NFOUND
#define VI_ERROR_RSRC_NFOUND 111
#endif

/*===========================================================================
 Prototypes
===========================================================================*/
ViStatus findInstrument(ViChar **resource);
void error_exit(ViSession instrHdl, ViStatus err);
void waitKeypress(void);

ViStatus get_device_id(ViSession ihdl); 

ViStatus get_beam_diameter(ViSession ihdl); 
ViStatus set_beam_diameter(ViSession ihdl);
ViStatus get_date(ViSession ihdl);
ViStatus set_date(ViSession ihdl);
ViStatus get_line_frequency(ViSession ihdl); 
ViStatus set_line_frequency(ViSession ihdl);
ViStatus get_power(ViSession ihdl);
ViStatus get_power_multi(ViSession ihdl);
ViStatus get_energy(ViSession ihdl); 
ViStatus get_frequency(ViSession ihdl);
ViStatus get_power_density(ViSession ihdl);
ViStatus get_energy_density(ViSession ihdl);
ViStatus get_sensor_information(ViSession ihdl); 
ViStatus get_4QPositions(ViSession ihdl);
ViStatus get_arrayMeasurment(ViSession ihdl);   
ViStatus get_burstArrayMeasurement(ViSession ihdl);   
ViStatus userPowerCalibration(ViSession ihdl); 

/*===========================================================================
 Functions
===========================================================================*/
int main(int argc, char **argv)
{
   ViStatus    err;
   ViChar      *rscPtr;
   ViSession   instrHdl = VI_NULL;
   int         c, done;
   
   printf("---------------------------------------------------------\n");
   printf(" PM100x/PM160/PM200/PM5020/PM60 Driver Sample Application\n");
   printf("-------------------------------------------------------\n\n"); 
   
   
   // Parameter checking / Resource scanning
   if(argc < 2)
   {
		// Find resources
		if((err = findInstrument(&rscPtr)))  error_exit(VI_NULL, err);
			if(rscPtr == NULL) exit(EXIT_SUCCESS); // No instrument found
   }
   else
   {
     	// resource is in command line (e.g."USB0::0x1313:0x8072:P2506201:0:INSTR")
      	rscPtr = argv[1];
   }
   
   // Open session to PM100x/PM160/PM200 instrument
   printf("Opening session to '%s' ...\n\n", rscPtr);
   if((err = TLPMX_init(rscPtr, VI_ON, VI_OFF, &instrHdl))) error_exit(instrHdl, err);

   printf("Closing session to '%s' ...\n\n", rscPtr);
   err = TLPMX_close (instrHdl);
   printf("Closing session to '%s' returned 0x%08X\n\n", rscPtr, (unsigned int)err);

   printf("Re-Opening session to '%s' ...\n\n", rscPtr);
   err = TLPMX_init(rscPtr, VI_ON, VI_OFF, &instrHdl);
   printf("Re-Opening session to '%s' returned 0x%08X\n\n", rscPtr, (unsigned int)err);
   
   // Operations
   done = 0;
   do
   {
      printf("Operations:\n\n");
      printf("I: Read instrument information\n");
      printf("b: Get Beam Diameter\n");
      printf("B: Set Beam Diameter\n");
      printf("d: Get Date and Time\n");
      printf("D: Set Date and Time\n");
      printf("l: Get Line Frequency\n");
      printf("L: Set Line Frequency\n"); 
      printf("p: Get Power\n");
      printf("P: Get Power Density\n"); 
      printf("e: Get Energy\n");
      printf("E: Get Energy Density\n");
      printf("f: Get Frequency\n");
      printf("s: Get Sensor Information\n"); 
      printf("w: Read Power %d times\n", NUM_MULTI_READING);
      printf("r: USB488 Deassert REN line               (VI_GPIB_REN_DEASSERT)\n");
      printf("R: USB488 Assert REN line                 (VI_GPIB_REN_ASSERT)\n");
      printf("G: USB488 Go To Local                     (VI_GPIB_REN_DEASSERT_GTL)\n");
      printf("A: USB488 Assert REN line + addr. dev.    (VI_GPIB_REN_ASSERT_ADDRESS)\n");
      printf("h: USB488 LLO to addressed listener devs. (VI_GPIB_REN_ASSERT_LLO)\n");
      printf("H: USB488 Address dev. + send LLO         (VI_GPIB_REN_ASSERT_ADDRESS_LLO)\n");
      printf("g: USB488 Send GTL to device              (VI_GPIB_REN_ADDRESS_GTL)\n");
	  printf("u: User Power Calibration\n"); 
	  printf("x: Get Positions of 4Q sensor\n");
	  printf("a: Get Power Array Measurement\n");  
	  printf("m: Get Burst Array Measurement\n");
      printf("Q: Quit\n");
      printf("\n");
   
      printf("\nPlease select: ");
      while((c = getchar()) == EOF);
      fflush(stdin);
      printf("\n");

      switch(c)
      {
         case 'i':
         case 'I':
            if((err = get_device_id(instrHdl))) error_exit(instrHdl, err);
            break;

         case 'b':
            if((err = get_beam_diameter(instrHdl))) error_exit(instrHdl, err);
            break;
            
         case 'B':
            if((err = set_beam_diameter(instrHdl))) error_exit(instrHdl, err);
            break;
            
         case 'd':
            if((err = get_date(instrHdl))) error_exit(instrHdl, err);
            break;
            
         case 'D':
            if((err = set_date(instrHdl))) error_exit(instrHdl, err);
            break;
            
         case 'l':
            if((err = get_line_frequency(instrHdl))) error_exit(instrHdl, err);
            break;
            
         case 'L':
            if((err = set_line_frequency(instrHdl))) error_exit(instrHdl, err);
            break;
         
         case 'p':
            if((err = get_power(instrHdl))) error_exit(instrHdl, err);
            break;
         
         case 'w':
         case 'W':
            if((err = get_power_multi(instrHdl))) error_exit(instrHdl, err);
            break;
         
         case 'P':
            if((err = get_power_density(instrHdl))) error_exit(instrHdl, err);
            break;
            
         case 'e':
            if((err = get_energy(instrHdl))) error_exit(instrHdl, err);
            break;
            
         case 'E':
            if((err = get_energy_density(instrHdl))) error_exit(instrHdl, err);
            break;
            
         case 'f':
            if((err = get_frequency(instrHdl))) error_exit(instrHdl, err);
            break;
            
         case 's':
            if((err = get_sensor_information(instrHdl))) error_exit(instrHdl, err);
            break;
			
		case 'u':
            if((err = userPowerCalibration(instrHdl))) error_exit(instrHdl, err);
            break;	
			
		case 'x':
            if((err = get_4QPositions(instrHdl))) error_exit(instrHdl, err);
            break;
			
		case 'a':
            if((err = get_arrayMeasurment(instrHdl))) error_exit(instrHdl, err);
            break;
		
		case 'm':
            if((err = get_burstArrayMeasurement(instrHdl))) error_exit(instrHdl, err);
            break;

         case 'q':
         case 'Q':
            done = 1;
            if(instrHdl != VI_NULL) TLPMX_close(instrHdl);
            break;

         default:
            printf("Invalid selection\n\n");
            break;      
      }
   } while(!done);
   
   return VI_SUCCESS;
}


/*---------------------------------------------------------------------------
  Get Beam Diameter
---------------------------------------------------------------------------*/
ViStatus get_beam_diameter(ViSession ihdl)
{
   ViStatus err = VI_SUCCESS; 
   ViReal64 beam_diameter_set, beam_diameter_min, beam_diameter_max, beam_diameter_default;
   
   printf("Get Beam Diameter ...\n");
   err = TLPMX_getBeamDia (ihdl, TLPM_ATTR_SET_VAL,  &beam_diameter_set, TLPM_DEFAULT_CHANNEL);  
   err = TLPMX_getBeamDia (ihdl, TLPM_ATTR_MIN_VAL,  &beam_diameter_min, TLPM_DEFAULT_CHANNEL);
   err = TLPMX_getBeamDia (ihdl, TLPM_ATTR_MAX_VAL,  &beam_diameter_max, TLPM_DEFAULT_CHANNEL);
   err = TLPMX_getBeamDia (ihdl, TLPM_ATTR_DFLT_VAL, &beam_diameter_default, TLPM_DEFAULT_CHANNEL);
   if(!err) printf("Beam Diameter: Set: %.3f Min: %.3f Max: %.3f Default: %.3f mm\r",beam_diameter_set, beam_diameter_min, beam_diameter_max, beam_diameter_default);
   printf("\n\n");
   fflush(stdin);
   return (err);
}


/*---------------------------------------------------------------------------
  Set Beam Diameter
---------------------------------------------------------------------------*/
ViStatus set_beam_diameter(ViSession ihdl)
{
   ViStatus err = VI_SUCCESS; 
   ViReal64 beam_diameter; 
   char     buf[1000];
   
   printf("Set Beam Diameter in mm...\n");
   printf("Enter new Beam Diameter\n");   
   scanf("%s", buf);
   sscanf(buf, "%lf\n", &beam_diameter);
   err = TLPMX_setBeamDia (ihdl, beam_diameter, TLPM_DEFAULT_CHANNEL);     
   printf("\n\n");
   fflush(stdin);
   return (err);
}


/*---------------------------------------------------------------------------
  Get Date and Time
---------------------------------------------------------------------------*/
ViStatus get_date(ViSession ihdl)
{
   ViStatus err = VI_SUCCESS; 
   ViInt16  year, month, day, hour, minute, second;
   
   printf("Get Date and Time ...\n");                 
   err = TLPMX_getTime (ihdl, &year, &month, &day, &hour, &minute, &second);

   if(!err) printf("Date and Time %02d.%02d.%02d %02d:%02d:%02d\r", day, month, year, hour, minute, second);
   printf("\n\n");
   fflush(stdin);
   return (err);
}


/*---------------------------------------------------------------------------
  Set Date and Time
---------------------------------------------------------------------------*/
ViStatus set_date(ViSession ihdl)
{
   ViStatus err = VI_SUCCESS; 
   ViInt16  year, month, day, hour, minute, second;
   char     buf[1000];
   
   printf("Set Date and Time ...\n");
   printf("Enter new Date and Time (YYYY,MM,DD,HH,MM,SS)\n");
   scanf("%s", buf);
   sscanf(buf, "%hd,%hd,%hd,%hd,%hd,%hd\n", &year, &month, &day, &hour, &minute, &second);
   
   err = TLPMX_setTime (ihdl, year, month, day, hour, minute, second);
   printf("\n\n");
   fflush(stdin);
   return (err);
}


/*---------------------------------------------------------------------------
  Get Line Frequency
---------------------------------------------------------------------------*/
ViStatus get_line_frequency(ViSession ihdl)
{
   ViStatus err = VI_SUCCESS; 
   ViInt16  line_frequency;
   
   printf("Get Line Frequency ...\n");
   err = TLPMX_getLineFrequency (ihdl, &line_frequency);      
   if(!err) printf("Line Frequency %d Hz\r",line_frequency);
   printf("\n\n");
   fflush(stdin);
   return (err);
}


/*---------------------------------------------------------------------------
  Set Line Frequency
---------------------------------------------------------------------------*/
ViStatus set_line_frequency(ViSession ihdl)
{
   ViStatus err = VI_SUCCESS; 
   ViInt16  line_frequency;
   char     buf[1000];
   
   printf("Set Line Frequency in Hz (50 / 60)...\n");
   printf("Enter new Line Frequency\n");  
   scanf("%s", buf);
   sscanf(buf, "%hd\n", &line_frequency);
   err = TLPMX_setLineFrequency (ihdl, line_frequency);    
   printf("\n\n");
   fflush(stdin);
   return (err);
}


/*---------------------------------------------------------------------------
  Measure Power
---------------------------------------------------------------------------*/
ViStatus get_power(ViSession ihdl)
{
	ViStatus       err = VI_SUCCESS; 
	ViReal64       power = 0.0;
	ViInt16        power_unit;
	char           *unit;

	err = TLPMX_getPowerUnit(ihdl, &power_unit, TLPM_DEFAULT_CHANNEL);
	switch(power_unit)
	{
	  	case TLPM_POWER_UNIT_DBM: unit = "dBm";break;
	  	default: unit = "W";break;
	}
	if(!err) err = TLPMX_measPower(ihdl, &power, TLPM_DEFAULT_CHANNEL);
	if(!err) printf("Power reading : %15.9f %s\n\n", power, unit);
	return (err);
}


/*---------------------------------------------------------------------------
  Measure Power
---------------------------------------------------------------------------*/
ViStatus get_power_multi(ViSession ihdl)
{
   ViStatus    err = VI_SUCCESS; 
   ViReal64    power;
   ViInt16     power_unit;
   char        *unit;
   int         i;

   err = TLPMX_getPowerUnit(ihdl, &power_unit, TLPM_DEFAULT_CHANNEL);
   if(!err)
   {
      switch(power_unit)
      {
         case TLPM_POWER_UNIT_DBM:   unit = "dBm";  break;
         default:                      unit = "W";    break;
      }
   }
   else
      unit = "?";

   i = 0;
   while ((i < NUM_MULTI_READING) && !err)
   {
      err = TLPMX_measPower(ihdl, &power, TLPM_DEFAULT_CHANNEL);
      if(!err) printf("Power reading #%04d: %15.9f %s\r", i+1, power, unit);
      i++;
   }
   printf("\n\n");
   return (err);
}


/*---------------------------------------------------------------------------
  Measure Energy
---------------------------------------------------------------------------*/
ViStatus get_energy(ViSession ihdl)
{
   	ViStatus       err = VI_FALSE; 
   	ViReal64       energy;
   	ViUInt32 cnt = 0;
   
	do
   	{
		err = TLPMX_measEnergy(ihdl, &energy, TLPM_DEFAULT_CHANNEL);  
		if (VI_SUCCESS != err )
		{
			printf("Energy code: %d\n", (int)err);
			Sleep(1000);
		}
	   
   	}while (cnt++ < 10 &&  VI_SUCCESS != err );
   
   	if(!err) printf("Energy reading: %15.9f J\n\n", energy);
   	return (err);
}                                         


/*---------------------------------------------------------------------------
  Measure Frequency
---------------------------------------------------------------------------*/
ViStatus get_frequency(ViSession ihdl)
{
   ViStatus       err = VI_SUCCESS; 
   ViReal64       frequency;
   
   err = TLPMX_measFreq(ihdl, &frequency, TLPM_DEFAULT_CHANNEL);
   if(!err) printf("Frequency reading: %15.9f Hz\n\n", frequency);
   return (err);
}


/*---------------------------------------------------------------------------
  Measure Power Density
---------------------------------------------------------------------------*/
ViStatus get_power_density(ViSession ihdl)
{
   ViStatus       err = VI_SUCCESS; 
   ViReal64       power_density;

   err = TLPMX_measPowerDens(ihdl, &power_density, TLPM_DEFAULT_CHANNEL);
   if(!err) printf("Power Density reading: %15.9f W/cm*cm\n\n", power_density);
   return (err);
}


/*---------------------------------------------------------------------------
  Measure Energy Density
---------------------------------------------------------------------------*/
ViStatus get_energy_density(ViSession ihdl)
{
   ViStatus       err = VI_SUCCESS; 
   ViReal64       energy_density;
   
   err = TLPMX_measEnergyDens(ihdl, &energy_density, TLPM_DEFAULT_CHANNEL);
   if(!err) printf("Energy Density reading: %15.9f J/cm*cm\n\n", energy_density);
   return (err);
}


/*---------------------------------------------------------------------------
  Get Sensor Information
---------------------------------------------------------------------------*/
ViStatus get_sensor_information(ViSession ihdl)
{
   ViStatus       err = VI_SUCCESS;
   ViChar _VI_FAR sensor_name[1000], serial_number[1000], cal_message[1000];
   ViInt16        sens_type, sens_subtype, flags;

   printf("Get Sensor Information...\n");                ;
   err = TLPMX_getSensorInfo(ihdl, sensor_name, serial_number, cal_message, &sens_type, &sens_subtype, &flags, TLPM_DEFAULT_CHANNEL);
   if(!err) printf("Sensor Name: %s \r\n", sensor_name);
   if(!err) printf("Serial Number: %s \r\n", serial_number); 
   if(!err) printf("Calibration Message: %s \r\n", cal_message);
   if(!err) printf("Sensor Type: %d Sub-Type: %d  Flags: 0x%x \r", sens_type, sens_subtype, flags);
   printf("\n\n");
   fflush(stdin);
   return (err);
}

/*---------------------------------------------------------------------------
  User Power Calibration
---------------------------------------------------------------------------*/
ViStatus userPowerCalibration(ViSession ihdl)
{
	ViStatus err = VI_SUCCESS;
	ViUInt16	memoryPosition;
	ViChar 	sensorSerialNumber[TLPM_BUFFER_SIZE];
	ViChar 	calibrationDate[TLPM_BUFFER_SIZE];
	ViUInt16 calibrationPointsCount;
	ViChar 	author[TLPM_BUFFER_SIZE];  
	ViUInt16 sensorPosition;
	ViBoolean state;
	ViReal64 wavelength[10];
	ViReal64 power[10];
	ViReal64 responsitivity;
	ViReal64 actWvelength;
	ViUInt16 point;

	memoryPosition = TLPM_INDEX_4;

	printf("User Power Calibration...\n");   

	// get the calibration at the first memory position
	err = TLPMX_getPowerCalibrationPointsInformation(ihdl, memoryPosition, sensorSerialNumber, calibrationDate, &calibrationPointsCount, author, &sensorPosition, TLPM_DEFAULT_CHANNEL);
	if(!err) printf("Sensor Serial Number: %s \r\n", sensorSerialNumber); 
	if(!err) printf("Calibration Date: %s \r\n", calibrationDate);
	if(!err) printf("Author: %s \r\n", author);  
	if(!err) printf("Calibration Points: %d \r\n", calibrationPointsCount); 
	if(!err) printf("Sensor Position: %d \r\n", sensorPosition);
	fflush(stdin);

	err = TLPMX_getPowerCalibrationPointsState(ihdl, memoryPosition, &state, TLPM_DEFAULT_CHANNEL);
	if(!err) printf("Calibration State: %s \r\n", state == VI_ON? "ON" : "OFF"); 
	fflush(stdin);

	err = TLPMX_getPowerCalibrationPoints(ihdl, memoryPosition, calibrationPointsCount, wavelength, power, TLPM_DEFAULT_CHANNEL);
	for(point = 0; point < calibrationPointsCount; point++)
	{
	  if(!err) printf("Wavelength: %.2f, Power: %f \r\n", wavelength[point], power[point]);
	} 
	fflush(stdin);

	// get the currently used wavelength
	err = TLPMX_getWavelength(ihdl, TLPM_ATTR_SET_VAL, &actWvelength, TLPM_DEFAULT_CHANNEL); 
	if(!err) printf("Wavelength: %f \r\n", actWvelength); 

	// get the currently used power factor
	err = TLPMX_getPhotodiodeResponsivity(ihdl, TLPM_ATTR_SET_VAL, &responsitivity, TLPM_DEFAULT_CHANNEL);
	if(!err) printf("Responsitivity before calibration: %f \r\n", responsitivity); 

	// overwrite the first memory position with a new calibration
	printf("\nStarting User Power Calibration...\n"); 
	sprintf(author, "My Name");
	wavelength[0] = 500.0;
	power[0] = 0.87;
	wavelength[1] = 725.0;
	power[1] = 0.95;
	err = TLPMX_setPowerCalibrationPoints(ihdl, memoryPosition, 2, wavelength, power, author, SENSOR_SWITCH_POS_1, TLPM_DEFAULT_CHANNEL); 
	if(VI_SUCCESS != err) return err; 

	printf("\nUser Power Calibration finished.\n"); 
   
	// activate the user power calibration for this sensor
	err = TLPMX_setPowerCalibrationPointsState(ihdl, memoryPosition, VI_ON, TLPM_DEFAULT_CHANNEL);

	// the sensor has to be reinitialized to use the power calibration
	err = TLPMX_reinitSensor(ihdl, TLPM_DEFAULT_CHANNEL);

	// wait until the sensor has been reinitialized
	Sleep(3000);

	// get the currently used power factor
	err = TLPMX_getPhotodiodeResponsivity(ihdl, TLPM_ATTR_SET_VAL, &responsitivity, TLPM_DEFAULT_CHANNEL);
	if(!err) printf("Responsitivity after calibration: %f \r\n", responsitivity); 
   
	printf("\n\n");
	fflush(stdin);
	return (err);
}
	
ViStatus get_4QPositions(ViSession instrHdl)
{
	ViStatus	err = VI_SUCCESS; 
   	ViReal64    positionX;
	ViReal64    positionY; 
	ViReal64	voltage1;
	ViReal64	voltage2;
	ViReal64	voltage3;
	ViReal64	voltage4;
   
	err = TLPMX_meas4QPositions(instrHdl, &positionX, &positionY, 1);
	if(!err) printf("4Q Position x: %.2f um, y: %.2f um \n\n", positionX, positionY);
	
	err = TLPMX_meas4QVoltages(instrHdl, &voltage1, &voltage2, &voltage3, &voltage4, 1);
	if(!err) printf("4Q Voltages: %f V, %f V, %f V, %f V \n\n", voltage1, voltage2, voltage3, voltage4);
	
	return (err);
}

#define BaseTime 10
#define DataSizeBaseTime BaseTime*100
ViStatus get_arrayMeasurment(ViSession instrHdl)
{
	ViStatus	err = VI_SUCCESS;
	ViUInt32 	measurementIndex = 0;
	ViReal32 timeStamps[DataSizeBaseTime];  
	ViReal32 powerValues[DataSizeBaseTime]; 
	ViBoolean isRunning = VI_TRUE;
	ViUInt32 averaging = 1;
	ViUInt32 autoTriggerDelay = 0;
	ViBoolean triggerForced = VI_FALSE;

	//search trigger level and range								 
   	err = TLPMX_setFreqMode(instrHdl, TLPM_FREQ_MODE_PEAK, TLPM_DEFAULT_CHANNEL);
	if(err < 0) return err;  

	Sleep(2000);   
   
	err = TLPMX_startPeakDetector(instrHdl, TLPM_DEFAULT_CHANNEL);			 
	if(err < 0) return err;  

   	Sleep(1000);   	  							 
			 
	while (isRunning)
	{
		err = TLPMX_isPeakDetectorRunning(instrHdl, &isRunning, TLPM_DEFAULT_CHANNEL);			 
		if(err < 0) return err;  
	}

    //Set to CW mode for normal measurement
   	TLPMX_setFreqMode(instrHdl, TLPM_FREQ_MODE_CW, TLPM_DEFAULT_CHANNEL);		
	
	TLPMX_confPowerMeasurementSequence(instrHdl, averaging, TLPM_DEFAULT_CHANNEL);	

	TLPMX_startMeasurementSequence(instrHdl, autoTriggerDelay, &triggerForced, TLPM_DEFAULT_CHANNEL);
					 
	err = TLPMX_getMeasurementSequence(instrHdl, BaseTime, timeStamps, powerValues, VI_NULL, TLPM_DEFAULT_CHANNEL);
	if(!err)
	{
		for(measurementIndex = 0; measurementIndex < DataSizeBaseTime; measurementIndex++) 
			printf("Power Value %u: %f ; %E W\n", (unsigned int)measurementIndex, timeStamps[measurementIndex], powerValues[measurementIndex]);
	}
	
	return (err); 
}

ViStatus get_burstArrayMeasurement(ViSession instrHdl)
{
	ViStatus err = VI_SUCCESS;
	ViUInt32 timeStamps[DataSizeBaseTime];  
	ViReal32 powerValues[DataSizeBaseTime]; 
	ViReal32 powerValues2[DataSizeBaseTime]; 
	ViUInt32 samplesCount = 0;


	// 1. Configure unit for channel 1. Skip if not connected or not needed. (will automatically abort ongoing measurements)
	err = TLPMX_confBurstArrayMeasPowerChannel(instrHdl, 1);
	if(err < 0) return err;  

	// 2. Configure unit for channel 2. Skip if not connected or not needed. (will automatically abort ongoing measurements)
	err = TLPMX_confBurstArrayMeasPowerChannel(instrHdl, 2);
	if(err < 0) return err;  

	// 3. Configure hardware front AUX triggered burst mode with initDelay = 1, BustCount = 2 and Averaging = 3.
	err = TLPMX_confBurstArrayMeasTrigger(instrHdl, 3, 1, 2, 3);
	if(err < 0) return err;  
	
	// 4. Starts a burst measurement 
	err = TLPMX_startBurstArrayMeasurement(instrHdl);
	if(err < 0) return err;  

	// 5. Trigger is active and burst sequences are stored in device buffer

	// 6.  Stops burst measurement. Triggers are not longer observed
	err = TLPMX_writeRaw(instrHdl, "ABOR");
	if(err < 0) return err;  
	
	// 7. Reads amount of samples in buffer
	err = TLPMX_getBurstArraySamplesCount(instrHdl, &samplesCount);
	if(samplesCount == 0 || err < 0) return err;
	
	// 8. Reads all samples of burst sequence
	err = TLPMX_getBurstArraySamples(instrHdl, 0, samplesCount, timeStamps, powerValues, powerValues2);
	if(err < 0) return err;
	
	return VI_SUCCESS;
}

/*---------------------------------------------------------------------------
  Exit with error message
---------------------------------------------------------------------------*/
void error_exit(ViSession instrHdl, ViStatus err)
{
   ViChar buf[TLPM_ERR_DESCR_BUFFER_SIZE];
   
   // Print error
   TLPMX_errorMessage (instrHdl, err, buf);
   fprintf(stderr, "ERROR: %s\n", buf);
   // Close instrument hande if open
   if(instrHdl != VI_NULL) TLPMX_close(instrHdl);
   // Exit program
   waitKeypress();
   exit (EXIT_FAILURE);
}


/*---------------------------------------------------------------------------
  Print keypress message and wait
---------------------------------------------------------------------------*/
void waitKeypress(void)
{
   printf("Press <ENTER> to exit\n");
   while(getchar() == EOF);
}


/*---------------------------------------------------------------------------
  Find Instruments
---------------------------------------------------------------------------*/
ViStatus findInstrument(ViChar **resource)
{
   ViStatus err;
   ViUInt32 deviceCount;
   ViUInt32 done, cnt;
   int i;
   static ViChar rsrcDescr[TLPM_BUFFER_SIZE];
   ViChar name[TLPM_BUFFER_SIZE], sernr[TLPM_BUFFER_SIZE];
   ViBoolean available;
                      
   printf("Scanning for instruments ...\n");
   
   // prepare return value
   rsrcDescr[0] = '\0';
   *resource = rsrcDescr;

   err = TLPMX_setEnableBthSearch(VI_NULL, VI_TRUE);
   if(VI_SUCCESS != err)
	   return err;

   err = TLPMX_findRsrc (0, &deviceCount);
   switch(err)
   {
      case VI_SUCCESS:
         // At least one device was found. Nothing to do here. Continue with device selection menu.
         break;

      case VI_ERROR_RSRC_NFOUND:
         printf("No matching instruments found\n\n"); 
         return (err);
                 
      default:
         return (err);
   }
   
   if(deviceCount < 2)
   {
      // Found only one matching instrument - return this
      err = TLPMX_getRsrcName (0, 0, rsrcDescr);
      return (err);
   }

   // Found multiple instruments - Display list of instruments
   done = 0;
   do
   {
      printf("Found %u matching instruments:\n\n", (unsigned int)deviceCount);
   
      // Print device list
      for(cnt = 0; cnt < deviceCount; cnt++)
      {
         err = TLPMX_getRsrcInfo (0, cnt, name, sernr, VI_NULL, &available);
         if(err) return (err);         
         printf("%u(%s): S/N:%s \t%s\n", (unsigned int)(cnt+1), (available) ? "FREE" : "LOCK", sernr, name);
      }
   
      printf("\nPlease select, press q to exit: ");
      while((i = getchar()) == EOF);
      fflush(stdin);
      switch(i)
      {
         case 'q':
         case 'Q':
            printf("User abort\n\n");
            return (VI_ERROR_RSRC_NFOUND);

         default:
            break;   // do nothing
      }

      // an integer is expected
      i -= '0';      
      printf("\n");
      if((i < 1) || ((ViUInt32)i > cnt))
      {
         printf("Invalid selection\n\n");
      }     
      else
      {
         done = VI_TRUE;
      }
      
      printf("\nPlease select: ");
      while((i = getchar()) == EOF);
      i -= '0';      
      fflush(stdin);
      printf("\n");
      if((i < 1) || ((ViUInt32)i > cnt))
      {
         printf("Invalid selection\n\n");
      }     
      else
      {
         done = 1;
      }
   }
   while(!done);
   
   // Copy resource string to static buffer
   err = TLPMX_getRsrcName(0, (ViUInt32)(i-1), rsrcDescr);
   
   return (err);
}


/*===========================================================================
 GET ID
===========================================================================*/
ViStatus get_device_id(ViSession ihdl)
{  
   ViStatus err;
   ViChar   nameBuf[TLPM_BUFFER_SIZE];
   ViChar   snBuf[TLPM_BUFFER_SIZE];
   ViChar   revBuf[TLPM_BUFFER_SIZE];

   if((err = TLPMX_identificationQuery (ihdl, VI_NULL, nameBuf, snBuf, revBuf))) return(err);
   printf("Instrument:    %s\n", nameBuf);
   printf("Serial number: %s\n", snBuf);
   printf("Firmware:      V%s\n", revBuf);
   if((err = TLPMX_revisionQuery (ihdl, revBuf, VI_NULL))) return(err);
   printf("Driver:        V%s\n", revBuf);
   if((err = TLPMX_getCalibrationMsg (ihdl, revBuf, TLPM_DEFAULT_CHANNEL))) return(err);
   printf("Cal message:   %s\n\n", revBuf);

   return VI_SUCCESS;
}


/****************************************************************************
  End of Source file
****************************************************************************/

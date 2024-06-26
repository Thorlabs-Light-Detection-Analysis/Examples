#include <stdlib.h>
#include <stdio.h>
#include <stdarg.h>
#include <string.h>

#include "TLPM.h"
#include "visatype.h"

#define FAST_MEAS_BUF_SIZE		10000

ViUInt32 time[FAST_MEAS_BUF_SIZE];
ViReal32 val[FAST_MEAS_BUF_SIZE];

static int returnErr(ViSession instrHdl, ViStatus status, const char* format, ...)
{
    if(instrHdl != VI_NULL)
	    TLPM_close(instrHdl);

    va_list args;
    va_start (args, format);
    vprintf (format, args);
    va_end (args);


	ViChar rsrcDescr[TLPM_BUFFER_SIZE];
    if(TLPM_errorMessage (instrHdl, status, rsrcDescr) == VI_SUCCESS)
		printf("Details: %s\n", rsrcDescr);
    else
    	printf("Details: %ld\n", status);
	return status;
}


int main(void)
{
	printf("Thorlabs Powermeter fast measure stream sample code\n");
	printf("===================================================\n");

	ViStatus stat;
	ViUInt32 resourceCount = 0;
	stat = TLPM_findRsrc (0, &resourceCount);
	if(stat != VI_SUCCESS)
		return returnErr(VI_NULL, stat, "Failed to init PM driver.\n");

	ViChar rsrcDescr[TLPM_BUFFER_SIZE];
	stat = TLPM_getRsrcName(0, 0, rsrcDescr);
	if(stat != VI_SUCCESS)
		return returnErr(VI_NULL, stat, "Failed to get resource name.\n");

	//open the powermeter supporting fast measurement
	ViSession instrHandle;
	stat = TLPM_init (rsrcDescr, VI_TRUE, VI_FALSE, &instrHandle);
	if(stat != VI_SUCCESS)
		return returnErr(VI_NULL, stat, "Failed to open PM.\n");

	//Note: Powermeter supports two different measure modus for continuous (non peak) measurements:
	//		1: Normal measure system (MEAS?, MEAS:CURR?) can be configured by averaging up to 1kHz
	//		2: Fast measure stream always 100kHz. The device buffers up to 10ms internally.
	//		   If the PC application is slower stream information will be lost! The stream info contains
	//		   a relative timestamps to allow correct XY plots even if data is missing. KEEP IN MIND
	//		   WINDOWS IS NO REALTIME OPERATING SYSTEM

	//Do not limit bandwidth
	stat = TLPM_setInputFilterState(instrHandle, VI_FALSE);
	if(stat != VI_SUCCESS)
		return returnErr(instrHandle, stat, "Failed to set filter to full bandwidth.\n");

	//enable auto ranging: Keep in mind changing the range will interrupt the entire measurement for multiple milliseconds to
	//					   stabilize amplifier hardware in the powermeter.
	stat = TLPM_setPowerAutoRange(instrHandle, VI_FALSE);
	if(stat != VI_SUCCESS)
		return returnErr(instrHandle, stat, "Failed to disable autoranging.\n");

	//Configure the fast measure stream for power.
	//Invalidates old device measure stream buffer.
	stat = TLPM_confPowerFastArrayMeasurement(instrHandle);
	if(stat != VI_SUCCESS)
		return returnErr(instrHandle, stat, "Failed to configure fast measure stream.\n");

	//This needs to run fast. Do nothing else within the loop to keep query speed at its maximum
	for(uint32_t totalCnt = 0; totalCnt < FAST_MEAS_BUF_SIZE;)
	{
		//Use temporary buffers to prevent reading out of bounds.
		static ViUInt32 timestamps[202];
		static ViReal32 values[202];

		ViUInt16 count = 0;
		stat = TLPM_getNextFastArrayMeasurement(instrHandle, &count, timestamps, values);
		if(stat != VI_SUCCESS)
			return returnErr(instrHandle, stat, "Failed to query fast measure stream.\n");

		//limit result buffer to total buffer length
		if(totalCnt + count > FAST_MEAS_BUF_SIZE)
			count = FAST_MEAS_BUF_SIZE - totalCnt;

		//Copy temporary results to final result buffers
		memcpy(&time[totalCnt], timestamps, count * sizeof(ViUInt32));
		memcpy(&val[totalCnt],  values, 	count * sizeof(ViReal32));

		totalCnt += count;
	}

	//Do whatever you want to to with fast measure data
	for(uint32_t i = 0; i < FAST_MEAS_BUF_SIZE; i += 100)
		printf("%010lu, %f mW\n", time[i], val[i] * 1000);

	printf("--------------");

	//Be careful relative time will wrap around
	if(time[FAST_MEAS_BUF_SIZE - 1] > time[0])
		printf("Total time: %ld us", time[FAST_MEAS_BUF_SIZE - 1] - time[0]);

	printf("--------------");

	for(uint32_t i = 1; i < FAST_MEAS_BUF_SIZE; i ++)
		if(time[i] - time[i - 0] > 10)
			printf("Time delta %ld > 10 us @ %d\n", time[i] - time[i - 0], i);

	TLPM_close (instrHandle);
	return 1;
}

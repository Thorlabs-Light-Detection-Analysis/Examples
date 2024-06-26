import os
from ctypes import cdll,c_long,c_uint32,c_uint16,c_uint8,byref,create_string_buffer,c_bool, c_char, c_char_p,c_int,c_int16,c_int8,c_double,c_float, c_wchar_p,sizeof,c_voidp, Structure

_VI_ERROR = (-2147483647-1)
VI_ON = 1
VI_OFF = 0
TLPM_VID_THORLABS = (0x1313)  # Thorlabs
TLPM_PID_TLPM_DFU = (0x8070)  # PM100D with DFU interface enabled
TLPM_PID_PM100A_DFU = (0x8071)  # PM100A with DFU interface enabled
TLPM_PID_PM100USB = (0x8072)  # PM100USB with DFU interface enabled
TLPM_PID_PM160USB_DFU = (0x8073)  # PM160 on USB with DFU interface enabled
TLPM_PID_PM160TUSB_DFU = (0x8074)  # PM160T on USB with DFU interface enabled
TLPM_PID_PM400_DFU = (0x8075)  # PM400 on USB with DFU interface enabled
TLPM_PID_PM101_DFU = (0x8076)  # PM101 on USB with DFU interface enabled (Interface 0 TMC, Interface 1 DFU)
TLPM_PID_PM102_DFU = (0x8077)  # PM102 on USB with DFU interface enabled (Interface 0 TMC, Interface 1 DFU)
TLPM_PID_PM103_DFU = (0x807A)  # PM103 on USB with DFU interface enabled (Interface 0 TMC, Interface 1 DFU)
TLPM_PID_PM100D = (0x8078)  # PM100D w/o DFU interface
TLPM_PID_PM100A = (0x8079)  # PM100A w/o DFU interface
TLPM_PID_PM160USB = (0x807B)  # PM160 on USB w/o DFU interface
TLPM_PID_PM160TUSB = (0x807C)  # PM160T on USB w/o DFU interface
TLPM_PID_PM400 = (0x807D)  # PM400 on USB w/o DFU interface
TLPM_PID_PM101 = (0x807E)  # reserved
TLPM_PID_PMTest = (0x807F)  # PM Test Platform
TLPM_PID_PM200 = (0x80B0)  # PM200
TLPM_PID_PM5020 = (0x80BB)  # PM5020 1 channel benchtop powermeter (Interface 0 TMC, Interface 1 DFU)
TLPM_PID_PM6x_DFU = (0x80B4)  # PM6x on USB with DFU interface enabled (Interface 0 TMC, Interface 1 DFU)
TLPM_FIND_PATTERN = "USB?*INSTR{VI_ATTR_MANF_ID==0x1313 && (VI_ATTR_MODEL_CODE==0x8070 || VI_ATTR_MODEL_CODE==0x8078)}"
PM100A_FIND_PATTERN = "USB?*INSTR{VI_ATTR_MANF_ID==0x1313 && (VI_ATTR_MODEL_CODE==0x8071 || VI_ATTR_MODEL_CODE==0x8079)}"
PM100USB_FIND_PATTERN = "USB?*INSTR{VI_ATTR_MANF_ID==0x1313 && VI_ATTR_MODEL_CODE==0x8072}"
PM160USB_FIND_PATTERN = "USB?*INSTR{VI_ATTR_MANF_ID==0x1313 && (VI_ATTR_MODEL_CODE==0x8073 || VI_ATTR_MODEL_CODE==0x807B)}"
PM160TUSB_FIND_PATTERN = "USB?*INSTR{VI_ATTR_MANF_ID==0x1313 && (VI_ATTR_MODEL_CODE==0x8074 || VI_ATTR_MODEL_CODE==0x807C)}"
PM200_FIND_PATTERN = "USB?*INSTR{VI_ATTR_MANF_ID==0x1313 && VI_ATTR_MODEL_CODE==0x80B0}"
PM400_FIND_PATTERN = "USB?*INSTR{VI_ATTR_MANF_ID==0x1313 && (VI_ATTR_MODEL_CODE==0x8075 || VI_ATTR_MODEL_CODE==0x807D)}"
PM101_FIND_PATTERN = "USB?*INSTR{VI_ATTR_MANF_ID==0x1313 && (VI_ATTR_MODEL_CODE==0x8076)}"
PM102_FIND_PATTERN = "USB?*INSTR{VI_ATTR_MANF_ID==0x1313 && (VI_ATTR_MODEL_CODE==0x8077)}"
PM103_FIND_PATTERN = "USB?*INSTR{VI_ATTR_MANF_ID==0x1313 && VI_ATTR_MODEL_CODE==0x807A}"
PMTest_FIND_PATTERN = "USB?*INSTR{VI_ATTR_MANF_ID==0x1313 && VI_ATTR_MODEL_CODE==0x807F}"
PM100_FIND_PATTERN = "USB?*::0x1313::0x807?::?*::INSTR"
PM5020_FIND_PATTERN = "USB?*INSTR{VI_ATTR_MANF_ID==0x1313 && VI_ATTR_MODEL_CODE==0x80BB}"
PMxxx_FIND_PATTERN = "USB?*INSTR{VI_ATTR_MANF_ID==0x1313 && (VI_ATTR_MODEL_CODE==0x8070 || VI_ATTR_MODEL_CODE==0x8078 || " \
"VI_ATTR_MODEL_CODE==0x8071 || VI_ATTR_MODEL_CODE==0x8079 || " \
"VI_ATTR_MODEL_CODE==0x8072 || " \
"VI_ATTR_MODEL_CODE==0x8073 || VI_ATTR_MODEL_CODE==0x807B || " \
"VI_ATTR_MODEL_CODE==0x8074 || VI_ATTR_MODEL_CODE==0x807C || " \
"VI_ATTR_MODEL_CODE==0x8075 || VI_ATTR_MODEL_CODE==0x807D || " \
"VI_ATTR_MODEL_CODE==0x8076 || VI_ATTR_MODEL_CODE==0x807E || " \
"VI_ATTR_MODEL_CODE==0x8077 || VI_ATTR_MODEL_CODE==0x807F || " \
"VI_ATTR_MODEL_CODE==0x807A || VI_ATTR_MODEL_CODE==0x80BB ||" \
"VI_ATTR_MODEL_CODE==0x80B0 || VI_ATTR_MODEL_CODE==0x80B4)}"
PMBT_FIND_PATTERN = "ASRL?*::INSTR{VI_ATTR_MANF_ID==0x1313 && (VI_ATTR_MODEL_CODE==0x807C || VI_ATTR_MODEL_CODE==0x807B)}"
PMUART_FIND_PATTERN_VISA = "ASRL?*::INSTR"
PMUART_FIND_PATTERN_COM = "COM?*"
PMNET_FIND_PATTERN = "TCPIP?*:INSTR{VI_ATTR_TCPIP_DEVICE_NAME==\"PM5020\" || VI_ATTR_TCPIP_DEVICE_NAME==\"PM103E\"}"
PMBTH_FIND_PATTERN = "BTHLE?*"
TLPM_BUFFER_SIZE = 256  # General buffer size
TLPM_ERR_DESCR_BUFFER_SIZE = 512  # Buffer size for error messages
VI_INSTR_WARNING_OFFSET = (0x3FFC0900 )
VI_INSTR_ERROR_OFFSET = (_VI_ERROR + 0x3FFC0900 )
VI_INSTR_ERROR_NOT_SUPP_INTF = (VI_INSTR_ERROR_OFFSET + 0x01 )
VI_INSTR_WARN_OVERFLOW = (VI_INSTR_WARNING_OFFSET + 0x01 )
VI_INSTR_WARN_UNDERRUN = (VI_INSTR_WARNING_OFFSET + 0x02 )
VI_INSTR_WARN_NAN = (VI_INSTR_WARNING_OFFSET + 0x03 )
TLPM_ATTR_SET_VAL = (0)
TLPM_ATTR_MIN_VAL = (1)
TLPM_ATTR_MAX_VAL = (2)
TLPM_ATTR_DFLT_VAL = (3)
TLPM_ATTR_AUTO_VAL = (9)
TLPM_DEFAULT_CHANNEL = (1)
TLPM_SENSOR_CHANNEL1 = (1)
TLPM_SENSOR_CHANNEL2 = (2)
TLPM_TRIGGER_SRC_CHANNEL_1 = (1)
TLPM_TRIGGER_SRC_CHANNEL_2 = (2)
TLPM_TRIGGER_SRC_FRONT_AUX = (3)
TLPM_TRIGGER_SRC_REAR = (4)
TLPM_INDEX_1 = (1)
TLPM_INDEX_2 = (2)
TLPM_INDEX_3 = (3)
TLPM_INDEX_4 = (4)
TLPM_INDEX_5 = (5)
TLPM_PEAK_FILTER_NONE = (0)
TLPM_PEAK_FILTER_OVER = (1)
TLPM_REG_STB = (0)  # < Status Byte Register
TLPM_REG_SRE = (1)  # < Service Request Enable
TLPM_REG_ESB = (2)  # < Standard Event Status Register
TLPM_REG_ESE = (3)  # < Standard Event Enable
TLPM_REG_OPER_COND = (4)  # < Operation Condition Register
TLPM_REG_OPER_EVENT = (5)  # < Operation Event Register
TLPM_REG_OPER_ENAB = (6)  # < Operation Event Enable Register
TLPM_REG_OPER_PTR = (7)  # < Operation Positive Transition Filter
TLPM_REG_OPER_NTR = (8)  # < Operation Negative Transition Filter
TLPM_REG_QUES_COND = (9)  # < Questionable Condition Register
TLPM_REG_QUES_EVENT = (10)  # < Questionable Event Register
TLPM_REG_QUES_ENAB = (11)  # < Questionable Event Enable Reg.
TLPM_REG_QUES_PTR = (12)  # < Questionable Positive Transition Filter
TLPM_REG_QUES_NTR = (13)  # < Questionable Negative Transition Filter
TLPM_REG_MEAS_COND = (14)  # < Measurement Condition Register
TLPM_REG_MEAS_EVENT = (15)  # < Measurement Event Register
TLPM_REG_MEAS_ENAB = (16)  # < Measurement Event Enable Register
TLPM_REG_MEAS_PTR = (17)  # < Measurement Positive Transition Filter
TLPM_REG_MEAS_NTR = (18)  # < Measurement Negative Transition Filter
TLPM_REG_AUX_COND = (19)  # < Auxiliary Condition Register
TLPM_REG_AUX_EVENT = (20)  # < Auxiliary Event Register
TLPM_REG_AUX_ENAB = (21)  # < Auxiliary Event Enable Register
TLPM_REG_AUX_PTR = (22)  # < Auxiliary Positive Transition Filter
TLPM_REG_AUX_NTR = (23)  # < Auxiliary Negative Transition Filter
TLPM_REG_OPER_COND_1 = (24)  # < Operation Condition Register Channel 1
TLPM_REG_OPER_COND_2 = (25)  # < Operation Condition Register Channel 2
TLPM_REG_AUX_DET_COND = (26)  # < Auxiliary Condition Register DET
TLPM_STATBIT_STB_AUX = (0x01)  # < Auxiliary summary
TLPM_STATBIT_STB_MEAS = (0x02)  # < Device Measurement Summary
TLPM_STATBIT_STB_EAV = (0x04)  # < Error available
TLPM_STATBIT_STB_QUES = (0x08)  # < Questionable Status Summary
TLPM_STATBIT_STB_MAV = (0x10)  # < Message available
TLPM_STATBIT_STB_ESB = (0x20)  # < Event Status Bit
TLPM_STATBIT_STB_MSS = (0x40)  # < Master summary status
TLPM_STATBIT_STB_OPER = (0x80)  # < Operation Status Summary
TLPM_STATBIT_ESR_OPC = (0x01)  # < Operation complete
TLPM_STATBIT_ESR_RQC = (0x02)  # < Request control
TLPM_STATBIT_ESR_QYE = (0x04)  # < Query error
TLPM_STATBIT_ESR_DDE = (0x08)  # < Device-Specific error
TLPM_STATBIT_ESR_EXE = (0x10)  # < Execution error
TLPM_STATBIT_ESR_CME = (0x20)  # < Command error
TLPM_STATBIT_ESR_URQ = (0x40)  # < User request
TLPM_STATBIT_ESR_PON = (0x80)  # < Power on
TLPM_STATBIT_QUES_VOLT = (0x0001)  # < questionable voltage measurement
TLPM_STATBIT_QUES_CURR = (0x0002)  # < questionable current measurement
TLPM_STATBIT_QUES_TIME = (0x0004)  # < questionable time measurement
TLPM_STATBIT_QUES_POW = (0x0008)  # < questionable power measurement
TLPM_STATBIT_QUES_TEMP = (0x0010)  # < questionable temperature measurement
TLPM_STATBIT_QUES_FREQ = (0x0020)  # < questionable frequency measurement
TLPM_STATBIT_QUES_PHAS = (0x0040)  # < questionable phase measurement
TLPM_STATBIT_QUES_MOD = (0x0080)  # < questionable modulation measurement
TLPM_STATBIT_QUES_CAL = (0x0100)  # < questionable calibration
TLPM_STATBIT_QUES_ENER = (0x0200)  # < questionable energy measurement
TLPM_STATBIT_QUES_10 = (0x0400)  # < reserved
TLPM_STATBIT_QUES_11 = (0x0800)  # < reserved
TLPM_STATBIT_QUES_12 = (0x1000)  # < reserved
TLPM_STATBIT_QUES_INST = (0x2000)  # < instrument summary
TLPM_STATBIT_QUES_WARN = (0x4000)  # < command warning
TLPM_STATBIT_QUES_15 = (0x8000)  # < reserved
TLPM_STATBIT_OPER_CAL = (0x0001)  # < The instrument is currently performing a calibration.
TLPM_STATBIT_OPER_SETT = (0x0002)  # < The instrument is waiting for signals it controls to stabilize enough to begin measurements.
TLPM_STATBIT_OPER_RANG = (0x0004)  # < The instrument is currently changing its range.
TLPM_STATBIT_OPER_SWE = (0x0008)  # < A sweep is in progress.
TLPM_STATBIT_OPER_MEAS = (0x0010)  # < The instrument is actively measuring.
TLPM_STATBIT_OPER_TRIG = (0x0020)  # < The instrument is in a �wait for trigger� state of the trigger model.
TLPM_STATBIT_OPER_ARM = (0x0040)  # < The instrument is in a �wait for arm� state of the trigger model.
TLPM_STATBIT_OPER_CORR = (0x0080)  # < The instrument is currently performing a correction (Auto-PID tune).
TLPM_STATBIT_OPER_SENS = (0x0100)  # < Optical powermeter sensor connected and operable.
TLPM_STATBIT_OPER_DATA = (0x0200)  # < Measurement data ready for fetch.
TLPM_STATBIT_OPER_THAC = (0x0400)  # < Thermopile accelerator active.
TLPM_STATBIT_OPER_11 = (0x0800)  # < reserved
TLPM_STATBIT_OPER_12 = (0x1000)  # < reserved
TLPM_STATBIT_OPER_INST = (0x2000)  # < One of n multiple logical instruments is reporting OPERational status.
TLPM_STATBIT_OPER_PROG = (0x4000)  # < A user-defined programming is currently in the run state.
TLPM_STATBIT_OPER_15 = (0x8000)  # < reserved
TLPM_STATBIT_MEAS_0 = (0x0001)  # < reserved
TLPM_STATBIT_MEAS_1 = (0x0002)  # < reserved
TLPM_STATBIT_MEAS_2 = (0x0004)  # < reserved
TLPM_STATBIT_MEAS_3 = (0x0008)  # < reserved
TLPM_STATBIT_MEAS_4 = (0x0010)  # < reserved
TLPM_STATBIT_MEAS_5 = (0x0020)  # < reserved
TLPM_STATBIT_MEAS_6 = (0x0040)  # < reserved
TLPM_STATBIT_MEAS_7 = (0x0080)  # < reserved
TLPM_STATBIT_MEAS_8 = (0x0100)  # < reserved
TLPM_STATBIT_MEAS_9 = (0x0200)  # < reserved
TLPM_STATBIT_MEAS_10 = (0x0400)  # < reserved
TLPM_STATBIT_MEAS_11 = (0x0800)  # < reserved
TLPM_STATBIT_MEAS_12 = (0x1000)  # < reserved
TLPM_STATBIT_MEAS_13 = (0x2000)  # < reserved
TLPM_STATBIT_MEAS_14 = (0x4000)  # < reserved
TLPM_STATBIT_MEAS_15 = (0x8000)  # < reserved
TLPM_STATBIT_AUX_NTC = (0x0001)  # < Auxiliary NTC temperature sensor connected.
TLPM_STATBIT_AUX_EMM = (0x0002)  # < External measurement module connected.
TLPM_STATBIT_AUX_UPCS = (0x0004)  # < User Power Calibration supported by this instrument
TLPM_STATBIT_AUX_UPCA = (0x0008)  # < User Power Calibration active status
TLPM_STATBIT_AUX_EXPS = (0x0010)  # < External power supply connected
TLPM_STATBIT_AUX_BATC = (0x0020)  # < Battery charging
TLPM_STATBIT_AUX_BATL = (0x0040)  # < Battery low
TLPM_STATBIT_AUX_IPS = (0x0080)  # < Apple(tm) authentification supported. True if an authentification co-processor is installed.
TLPM_STATBIT_AUX_IPF = (0x0100)  # < Apple(tm) authentification failed. True if the authentification setup procedure failed.
TLPM_STATBIT_AUX_9 = (0x0200)  # < reserved
TLPM_STATBIT_AUX_10 = (0x0400)  # < reserved
TLPM_STATBIT_AUX_11 = (0x0800)  # < reserved
TLPM_STATBIT_AUX_12 = (0x1000)  # < reserved
TLPM_STATBIT_AUX_13 = (0x2000)  # < reserved
TLPM_STATBIT_AUX_14 = (0x4000)  # < reserved
TLPM_STATBIT_AUX_15 = (0x8000)  # < reserved
TLPM_WINTERTIME = (0)
TLPM_SUMMERTIME = (1)
TLPM_LINE_FREQ_50 = (50)  # < line frequency in Hz
TLPM_LINE_FREQ_60 = (60)  # < line frequency in Hz
TLPM_INPUT_FILTER_STATE_OFF = (0)
TLPM_INPUT_FILTER_STATE_ON = (1)
TLPM_ACCELERATION_STATE_OFF = (0)
TLPM_ACCELERATION_STATE_ON = (1)
TLPM_ACCELERATION_MANUAL = (0)
TLPM_ACCELERATION_AUTO = (1)
TLPM_STAT_DARK_ADJUST_FINISHED = (0)
TLPM_STAT_DARK_ADJUST_RUNNING = (1)
TLPM_AUTORANGE_CURRENT_OFF = (0)
TLPM_AUTORANGE_CURRENT_ON = (1)
TLPM_CURRENT_REF_OFF = (0)
TLPM_CURRENT_REF_ON = (1)
TLPM_ENERGY_REF_OFF = (0)
TLPM_ENERGY_REF_ON = (1)
TLPM_FREQ_MODE_CW = (0)
TLPM_FREQ_MODE_PEAK = (1)
TLPM_AUTORANGE_POWER_OFF = (0)
TLPM_AUTORANGE_POWER_ON = (1)
TLPM_POWER_REF_OFF = (0)
TLPM_POWER_REF_ON = (1)
TLPM_POWER_UNIT_WATT = (0)
TLPM_POWER_UNIT_DBM = (1)
SENSOR_SWITCH_POS_1 = (1)
SENSOR_SWITCH_POS_2 = (2)
TLPM_AUTORANGE_VOLTAGE_OFF = (0)
TLPM_AUTORANGE_VOLTAGE_ON = (1)
TLPM_VOLTAGE_REF_OFF = (0)
TLPM_VOLTAGE_REF_ON = (1)
TLPM_ANALOG_ROUTE_PUR = (0)
TLPM_ANALOG_ROUTE_CBA = (1)
TLPM_ANALOG_ROUTE_CMA = (2)
TLPM_ANALOG_ROUTE_GEN = (3)
TLPM_MEAS_POWER = (0)
TLPM_MEAS_CURRENT = (1)
TLPM_MEAS_VOLTAGE = (2)
TLPM_MEAS_PDENSITY = (3)
TLPM_MEAS_ENERGY = (4)
TLPM_MEAS_EDENSITY = (5)
TLPM_IODIR_INP = (VI_OFF)
TLPM_IODIR_OUTP = (VI_ON)
TLPM_IOLVL_LOW = (VI_OFF)
TLPM_IOLVL_HIGH = (VI_ON)
DIGITAL_IO_CONFIG_INPUT = (0)
DIGITAL_IO_CONFIG_OUTPUT = (1)
DIGITAL_IO_CONFIG_INPUT_ALT = (2)
DIGITAL_IO_CONFIG_OUTPUT_ALT = (3)
I2C_OPER_INTER = (0)
I2C_OPER_SLOW = (1)
I2C_OPER_FAST = (2)
FAN_OPER_OFF = (0)
FAN_OPER_FULL = (1)
FAN_OPER_OPEN_LOOP = (2)
FAN_OPER_CLOSED_LOOP = (3)
FAN_OPER_TEMPER_CTRL = (4)
FAN_TEMPER_SRC_HEAD = (0)
FAN_TEMPER_SRC_EXT_NTC = (1)
SENSOR_TYPE_NONE = 0x0  # No sensor. This value is used to mark sensor data for 'no sensor connected'.
SENSOR_TYPE_PD_SINGLE = 0x1  # Single photodiode sensor. Only one ipd input active at the same time.
SENSOR_TYPE_THERMO = 0x2  # Thermopile sensor
SENSOR_TYPE_PYRO = 0x3  # Pyroelectric sensor
SENSOR_TYPE_4Q = 0x4  # 4Q Sensor
SENSOR_SUBTYPE_NONE = 0x0  # No sensor. This value is used to mark RAM data structure for 'no sensor connected'. Do not write this value to the EEPROM.
SENSOR_SUBTYPE_PD_ADAPTER = 0x01  # Photodiode adapter (no temperature sensor)
SENSOR_SUBTYPE_PD_SINGLE_STD = 0x02  # Standard single photodiode sensor (no temperature sensor)
SENSOR_SUBTYPE_PD_SINGLE_FSR = 0x03  # One single photodiode. Filter position set by a slide on the sensor selects responsivity data set to use. (no temperature sensor)
SENSOR_SUBTYPE_PD_SINGLE_STD_T = 0x12  # Standard single photodiode sensor (with temperature sensor)
SENSOR_SUBTYPE_THERMO_ADAPTER = 0x01  # Thermopile adapter (no temperature sensor)
SENSOR_SUBTYPE_THERMO_STD = 0x02  # Standard thermopile sensor (no temperature sensor)
SENSOR_SUBTYPE_THERMO_STD_T = 0x12  # Standard thermopile sensor (with temperature sensor)
SENSOR_SUBTYPE_PYRO_ADAPTER = 0x01  # Pyroelectric adapter (no temperature sensor)
SENSOR_SUBTYPE_PYRO_STD = 0x02  # Standard pyroelectric sensor (no temperature sensor)
SENSOR_SUBTYPE_PYRO_STD_T = 0x12  # Standard pyroelectric sensor (with temperature sensor)
TLPM_SENS_FLAG_IS_UNDEFINED = 0x0000  # Undefined sensor
TLPM_SENS_FLAG_IS_POWER = 0x0001  # Power sensor
TLPM_SENS_FLAG_IS_ENERGY = 0x0002  # Energy sensor
TLPM_SENS_FLAG_IS_RESP_SET = 0x0010  # Responsivity settable
TLPM_SENS_FLAG_IS_WAVEL_SET = 0x0020  # Wavelength settable
TLPM_SENS_FLAG_IS_TAU_SET = 0x0040  # Time constant tau settable
TLPM_SENS_FLAG_HAS_TEMP = 0x0100  # Temperature sensor included

class TLPMX:

	def __init__(self, resourceName = None, IDQuery = False, resetDevice = False):
		"""
		This function initializes the instrument driver session and performs the following initialization actions:
		
		(1) Opens a session to the Default Resource Manager resource and a session to the specified device using the Resource Name.
		(2) Performs an identification query on the instrument.
		(3) Resets the instrument to a known state.
		(4) Sends initialization commands to the instrument.
		(5) Returns an instrument handle which is used to distinguish between different sessions of this instrument driver.
		
		Notes:
		(1) Each time this function is invoked a unique session is opened.  
		
		Args:
			resourceName
			IDQuery (bool):This parameter specifies whether an identification query is performed during the initialization process.
			
			VI_TRUE  (1): Do query (default).
			VI_FALSE (0): Skip query.
			
			
			resetDevice (bool):This parameter specifies whether the instrument is reset during the initialization process.
			
			VI_TRUE  (1) - instrument is reset (default)
			VI_FALSE (0) - no reset 
			
			
		"""
		if sizeof(c_voidp) == 4:
			dll_name = "TLPMX_32.dll"
			dllabspath = os.path.dirname(os.path.abspath(__file__)) + os.path.sep + dll_name
			self.dll = cdll.LoadLibrary(dllabspath)
		else:
			dll_name = "TLPMX_64.dll"
			dllabspath = os.path.dirname(os.path.abspath(__file__)) + os.path.sep + dll_name
			self.dll = cdll.LoadLibrary(dllabspath)

		self.devSession = c_long()
		self.devSession.value = 0
		if resourceName!= None:
			pInvokeResult = self.dll.TLPMX_init( create_string_buffer(resourceName), c_bool(IDQuery), c_bool(resetDevice), byref(self.devSession))
			self.__testForError(pInvokeResult)


	def __testForError(self, status):
		if status < 0:
			self.__throwError(status)
		return status

	def __throwError(self, code):
		msg = create_string_buffer(1024)
		self.dll.TLPMX_errorMessage(self.devSession, c_int(code), msg)
		raise NameError(c_char_p(msg.raw).value)

	def initWithEncryption(self, IDQuery, reset):
		"""
		This function initializes the instrument driver session and performs the following initialization actions:
		
		(1) Opens a session to the Default Resource Manager resource and a session to the specified device using the Resource Name.
		(2) Performs an identification query on the instrument.
		(3) Resets the instrument to a known state.
		(4) Sends initialization commands to the instrument.
		(5) Returns an instrument handle which is used to distinguish between different sessions of this instrument driver.
		
		Notes:
		(1) Each time this function is invoked a unique session is opened.  
		
		Args:
			IDQuery(int16) : This parameter specifies whether an identification query is performed during the initialization process.
			
			VI_TRUE  (1): Do query (default).
			VI_FALSE (0): Skip query.
			
			
			reset(int16) : This parameter specifies whether the instrument is reset during the initialization process.
			
			VI_TRUE  (1) - instrument is reset (default)
			VI_FALSE (0) - no reset 
			
			
		Returns:
			password(string) : Password for encryption over ethernet communication.
			pInstr(PSession) : This parameter returns an instrument handle that is used in all subsequent calls to distinguish between different sessions of this instrument driver.
		"""
		pypassword = create_string_buffer(1024)
		pypInstr = ViPSession(0)
		pInvokeResult = self.dll.TLPMX_initWithEncryption(self.devSession, c_int16(IDQuery), c_int16(reset), pypassword, byref(pypInstr))
		self.__testForError(pInvokeResult)
		return c_char_p(pypassword.raw).value, pypInstr.value

	def close(self):
		"""
		This function closes the instrument driver session.
		
		Note: The instrument must be reinitialized to use it again.
		
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPMX_close(self.devSession)
		return pInvokeResult

	def findRsrc(self):
		"""
		This function finds all driver compatible devices attached to the PC and returns the number of found devices.
		
		Note:
		(1) The function additionally stores information like system name about the found resources internally. This information can be retrieved with further functions from the class, e.g. <Get Resource Description> and <Get Resource Information>.
		
		
		Args:
			
		Returns:
			resourceCount(uint32) : The number of connected devices that are supported by this driver.
		"""
		pyresourceCount = c_uint32(0)
		pInvokeResult = self.dll.TLPMX_findRsrc(self.devSession, byref(pyresourceCount))
		self.__testForError(pInvokeResult)
		return  pyresourceCount.value

	def getRsrcName(self, index):
		"""
		This function gets the resource name string needed to open a device with <Initialize>.
		
		Notes:
		(1) The data provided by this function was updated at the last call of <Find Resources>.
		
		Args:
			index(uint32) : This parameter accepts the index of the device to get the resource descriptor from.
			
			Notes: 
			(1) The index is zero based. The maximum index to be used here is one less than the number of devices found by the last call of <Find Resources>.
			
			
			Notes:
			(1) The array must contain at least TLPM_BUFFER_SIZE (256) elements ViChar[256].
		Returns:
			resourceName(string) : This parameter returns the resource descriptor. Use this descriptor to specify the device in <Initialize>.
		"""
		pyresourceName = create_string_buffer(1024)
		pInvokeResult = self.dll.TLPMX_getRsrcName(self.devSession, c_uint32(index), pyresourceName)
		self.__testForError(pInvokeResult)
		return c_char_p(pyresourceName.raw).value

	def getRsrcInfo(self, index):
		"""
		This function gets information about a connected resource.
		
		Notes:
		(1) The data provided by this function was updated at the last call of <Find Resources>.
		
		Args:
			index(uint32) : This parameter accepts the index of the device to get the resource descriptor from.
			
			Notes: 
			(1) The index is zero based. The maximum index to be used here is one less than the number of devices found by the last call of <Find Resources>.
			
			
			Notes:
			(1) The array must contain at least TLPM_BUFFER_SIZE (256) elements ViChar[256].
			(2) You may pass VI_NULL if you do not need this parameter.
			(3) Serial interfaces over Bluetooth will return the interface name instead of the device model name.
			
			Notes:
			(1) The array must contain at least TLPM_BUFFER_SIZE (256) elements ViChar[256].
			(2) You may pass VI_NULL if you do not need this parameter.
			(3) The serial number is not available for serial interfaces over Bluetooth.
			
			Notes:
			(1) The array must contain at least TLPM_BUFFER_SIZE (256) elements ViChar[256].
			(2) You may pass VI_NULL if you do not need this parameter.
			(3) The manufacturer name is not available for serial interfaces over Bluetooth.
			Devices that are not available are used by other applications.
			
			Notes:
			(1) You may pass VI_NULL if you do not need this parameter.
			
		Returns:
			modelName(string) : This parameter returns the model name of the device.
			serialNumber(string) : This parameter returns the serial number of the device.
			manufacturer(string) : This parameter returns the manufacturer name of the device.
			deviceAvailable(int16) : Returns the information if the device is available.
		"""
		pymodelName = create_string_buffer(1024)
		pyserialNumber = create_string_buffer(1024)
		pymanufacturer = create_string_buffer(1024)
		pydeviceAvailable = c_int16(0)
		pInvokeResult = self.dll.TLPMX_getRsrcInfo(self.devSession, c_uint32(index), pymodelName, pyserialNumber, pymanufacturer, byref(pydeviceAvailable))
		self.__testForError(pInvokeResult)
		return c_char_p(pymodelName.raw).value, c_char_p(pyserialNumber.raw).value, c_char_p(pymanufacturer.raw).value, pydeviceAvailable.value

	def writeRegister(self, reg, value):
		"""
		This function writes the content of any writable instrument register. Refer to your instrument's user's manual for more details on status structure registers.
		
		
		Args:
			reg(int16) : Specifies the register to be used for operation. This parameter can be any of the following constants:
			
			  TLPM_REG_SRE         (1): Service Request Enable
			  TLPM_REG_ESE         (3): Standard Event Enable
			  TLPM_REG_OPER_ENAB   (6): Operation Event Enable Register
			  TLPM_REG_OPER_PTR    (7): Operation Positive Transition
			  TLPM_REG_OPER_NTR    (8): Operation Negative Transition
			  TLPM_REG_QUES_ENAB  (11): Questionable Event Enable Reg.
			  TLPM_REG_QUES_PTR   (12): Questionable Positive Transition
			  TLPM_REG_QUES_NTR   (13): Questionable Negative Transition
			  TLPM_REG_MEAS_ENAB  (16): Measurement Event Enable Register
			  TLPM_REG_MEAS_PTR   (17): Measurement Positive Transition
			  TLPM_REG_MEAS_NTR   (18): Measurement Negative Transition
			  TLPM_REG_AUX_ENAB   (21): Auxiliary Event Enable Register
			  TLPM_REG_AUX_PTR    (22): Auxiliary Positive Transition
			  TLPM_REG_AUX_NTR    (23): Auxiliary Negative Transition 
			
			value(int16) : This parameter specifies the new value of the selected register.
			
			These register bits are defined:
			
			STATUS BYTE bits (see IEEE488.2-1992 §11.2)
			TLPM_STATBIT_STB_AUX        (0x01): Auxiliary summary
			TLPM_STATBIT_STB_MEAS       (0x02): Device Measurement Summary
			TLPM_STATBIT_STB_EAV        (0x04): Error available
			TLPM_STATBIT_STB_QUES       (0x08): Questionable Status Summary
			TLPM_STATBIT_STB_MAV        (0x10): Message available
			TLPM_STATBIT_STB_ESB        (0x20): Event Status Bit
			TLPM_STATBIT_STB_MSS        (0x40): Master summary status
			TLPM_STATBIT_STB_OPER       (0x80): Operation Status Summary
			
			STANDARD EVENT STATUS REGISTER bits (see IEEE488.2-1992 §11.5.1)
			TLPM_STATBIT_ESR_OPC        (0x01): Operation complete
			TLPM_STATBIT_ESR_RQC        (0x02): Request control
			TLPM_STATBIT_ESR_QYE        (0x04): Query error
			TLPM_STATBIT_ESR_DDE        (0x08): Device-Specific error
			TLPM_STATBIT_ESR_EXE        (0x10): Execution error
			TLPM_STATBIT_ESR_CME        (0x20): Command error
			TLPM_STATBIT_ESR_URQ        (0x40): User request
			TLPM_STATBIT_ESR_PON        (0x80): Power on
			
			QUESTIONABLE STATUS REGISTER bits (see SCPI 99.0 §9)
			TLPM_STATBIT_QUES_VOLT      (0x0001): Questionable voltage measurement
			TLPM_STATBIT_QUES_CURR      (0x0002): Questionable current measurement
			TLPM_STATBIT_QUES_TIME      (0x0004): Questionable time measurement
			TLPM_STATBIT_QUES_POW       (0x0008): Questionable power measurement
			TLPM_STATBIT_QUES_TEMP      (0x0010): Questionable temperature measurement
			TLPM_STATBIT_QUES_FREQ      (0x0020): Questionable frequency measurement
			TLPM_STATBIT_QUES_PHAS      (0x0040): Questionable phase measurement
			TLPM_STATBIT_QUES_MOD       (0x0080): Questionable modulation measurement
			TLPM_STATBIT_QUES_CAL       (0x0100): Questionable calibration
			TLPM_STATBIT_QUES_ENER      (0x0200): Questionable energy measurement
			TLPM_STATBIT_QUES_10        (0x0400): Reserved
			TLPM_STATBIT_QUES_11        (0x0800): Reserved
			TLPM_STATBIT_QUES_12        (0x1000): Reserved
			TLPM_STATBIT_QUES_INST      (0x2000): Instrument summary
			TLPM_STATBIT_QUES_WARN      (0x4000): Command warning
			TLPM_STATBIT_QUES_15        (0x8000): Reserved
			
			OPERATION STATUS REGISTER bits (see SCPI 99.0 §9)
			TLPM_STATBIT_OPER_CAL       (0x0001): The instrument is currently performing a calibration.
			TLPM_STATBIT_OPER_SETT      (0x0002): The instrument is waiting for signals to stabilize for measurements.
			TLPM_STATBIT_OPER_RANG      (0x0004): The instrument is currently changing its range.
			TLPM_STATBIT_OPER_SWE       (0x0008): A sweep is in progress.
			TLPM_STATBIT_OPER_MEAS      (0x0010): The instrument is actively measuring.
			TLPM_STATBIT_OPER_TRIG      (0x0020): The instrument is in a “wait for trigger” state of the trigger model.
			TLPM_STATBIT_OPER_ARM       (0x0040): The instrument is in a “wait for arm” state of the trigger model.
			TLPM_STATBIT_OPER_CORR      (0x0080): The instrument is currently performing a correction (Auto-PID tune).
			TLPM_STATBIT_OPER_SENS      (0x0100): Optical powermeter sensor connected and operable.
			TLPM_STATBIT_OPER_DATA      (0x0200): Measurement data ready for fetch.
			TLPM_STATBIT_OPER_THAC      (0x0400): Thermopile accelerator active.
			TLPM_STATBIT_OPER_11        (0x0800): Reserved
			TLPM_STATBIT_OPER_12        (0x1000): Reserved
			TLPM_STATBIT_OPER_INST      (0x2000): One of n multiple logical instruments is reporting OPERational status.
			TLPM_STATBIT_OPER_PROG      (0x4000): A user-defined programming is currently in the run state.
			TLPM_STATBIT_OPER_15        (0x8000): Reserved
			
			Thorlabs defined MEASRUEMENT STATUS REGISTER bits
			TLPM_STATBIT_MEAS_0         (0x0001): Reserved
			TLPM_STATBIT_MEAS_1         (0x0002): Reserved
			TLPM_STATBIT_MEAS_2         (0x0004): Reserved
			TLPM_STATBIT_MEAS_3         (0x0008): Reserved
			TLPM_STATBIT_MEAS_4         (0x0010): Reserved
			TLPM_STATBIT_MEAS_5         (0x0020): Reserved
			TLPM_STATBIT_MEAS_6         (0x0040): Reserved
			TLPM_STATBIT_MEAS_7         (0x0080): Reserved
			TLPM_STATBIT_MEAS_8         (0x0100): Reserved
			TLPM_STATBIT_MEAS_9         (0x0200): Reserved
			TLPM_STATBIT_MEAS_10        (0x0400): Reserved
			TLPM_STATBIT_MEAS_11        (0x0800): Reserved
			TLPM_STATBIT_MEAS_12        (0x1000): Reserved
			TLPM_STATBIT_MEAS_13        (0x2000): Reserved
			TLPM_STATBIT_MEAS_14        (0x4000): Reserved
			TLPM_STATBIT_MEAS_15        (0x8000): Reserved
			
			Thorlabs defined Auxiliary STATUS REGISTER bits
			TLPM_STATBIT_AUX_NTC        (0x0001): Auxiliary NTC temperature sensor connected.
			TLPM_STATBIT_AUX_EMM        (0x0002): External measurement module connected.
			TLPM_STATBIT_AUX_2          (0x0004): Reserved
			TLPM_STATBIT_AUX_3          (0x0008): Reserved
			TLPM_STATBIT_AUX_EXPS       (0x0010): External power supply connected
			TLPM_STATBIT_AUX_BATC       (0x0020): Battery charging
			TLPM_STATBIT_AUX_BATL       (0x0040): Battery low
			TLPM_STATBIT_AUX_IPS        (0x0080): Apple(tm) authentification supported.
			TLPM_STATBIT_AUX_IPF        (0x0100): Apple(tm) authentification failed.
			TLPM_STATBIT_AUX_9          (0x0200): Reserved
			TLPM_STATBIT_AUX_10         (0x0400): Reserved
			TLPM_STATBIT_AUX_11         (0x0800): Reserved
			TLPM_STATBIT_AUX_12         (0x1000): Reserved
			TLPM_STATBIT_AUX_13         (0x2000): Reserved
			TLPM_STATBIT_AUX_14         (0x4000): Reserved
			TLPM_STATBIT_AUX_15         (0x8000): Reserved
			
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_writeRegister(self.devSession, c_int16(reg), c_int16(value))
		self.__testForError(pInvokeResult)

	def readRegister(self, reg):
		"""
		This function reads the content of any readable instrument register. Refer to your instrument's user's manual for more details on status structure registers.
		
		
		Args:
			reg(int16) : Specifies the register to be used for operation. This parameter can be any of the following constants:
			
			  TLPM_REG_STB         (0): Status Byte Register
			  TLPM_REG_SRE         (1): Service Request Enable
			  TLPM_REG_ESB         (2): Standard Event Status Register
			  TLPM_REG_ESE         (3): Standard Event Enable
			  TLPM_REG_OPER_COND   (4): Operation Condition Register
			  TLPM_REG_OPER_EVENT  (5): Operation Event Register
			  TLPM_REG_OPER_ENAB   (6): Operation Event Enable Register
			  TLPM_REG_OPER_PTR    (7): Operation Positive Transition
			  TLPM_REG_OPER_NTR    (8): Operation Negative Transition
			  TLPM_REG_QUES_COND   (9): Questionable Condition Register
			  TLPM_REG_QUES_EVENT (10): Questionable Event Register
			  TLPM_REG_QUES_ENAB  (11): Questionable Event Enable Reg.
			  TLPM_REG_QUES_PTR   (12): Questionable Positive Transition
			  TLPM_REG_QUES_NTR   (13): Questionable Negative Transition
			  TLPM_REG_MEAS_COND  (14): Measurement Condition Register
			  TLPM_REG_MEAS_EVENT (15): Measurement Event Register
			  TLPM_REG_MEAS_ENAB  (16): Measurement Event Enable Register
			  TLPM_REG_MEAS_PTR   (17): Measurement Positive Transition
			  TLPM_REG_MEAS_NTR   (18): Measurement Negative Transition
			  TLPM_REG_AUX_COND   (19): Auxiliary Condition Register
			  TLPM_REG_AUX_EVENT  (20): Auxiliary Event Register
			  TLPM_REG_AUX_ENAB   (21): Auxiliary Event Enable Register
			  TLPM_REG_AUX_PTR    (22): Auxiliary Positive Transition
			  TLPM_REG_AUX_NTR    (23): Auxiliary Negative Transition 
			
			
			These register bits are defined:
			
			STATUS BYTE bits (see IEEE488.2-1992 §11.2)
			TLPM_STATBIT_STB_AUX        (0x01): Auxiliary summary
			TLPM_STATBIT_STB_MEAS       (0x02): Device Measurement Summary
			TLPM_STATBIT_STB_EAV        (0x04): Error available
			TLPM_STATBIT_STB_QUES       (0x08): Questionable Status Summary
			TLPM_STATBIT_STB_MAV        (0x10): Message available
			TLPM_STATBIT_STB_ESB        (0x20): Event Status Bit
			TLPM_STATBIT_STB_MSS        (0x40): Master summary status
			TLPM_STATBIT_STB_OPER       (0x80): Operation Status Summary
			
			STANDARD EVENT STATUS REGISTER bits (see IEEE488.2-1992 §11.5.1)
			TLPM_STATBIT_ESR_OPC        (0x01): Operation complete
			TLPM_STATBIT_ESR_RQC        (0x02): Request control
			TLPM_STATBIT_ESR_QYE        (0x04): Query error
			TLPM_STATBIT_ESR_DDE        (0x08): Device-Specific error
			TLPM_STATBIT_ESR_EXE        (0x10): Execution error
			TLPM_STATBIT_ESR_CME        (0x20): Command error
			TLPM_STATBIT_ESR_URQ        (0x40): User request
			TLPM_STATBIT_ESR_PON        (0x80): Power on
			
			QUESTIONABLE STATUS REGISTER bits (see SCPI 99.0 §9)
			TLPM_STATBIT_QUES_VOLT      (0x0001): Questionable voltage measurement
			TLPM_STATBIT_QUES_CURR      (0x0002): Questionable current measurement
			TLPM_STATBIT_QUES_TIME      (0x0004): Questionable time measurement
			TLPM_STATBIT_QUES_POW       (0x0008): Questionable power measurement
			TLPM_STATBIT_QUES_TEMP      (0x0010): Questionable temperature measurement
			TLPM_STATBIT_QUES_FREQ      (0x0020): Questionable frequency measurement
			TLPM_STATBIT_QUES_PHAS      (0x0040): Questionable phase measurement
			TLPM_STATBIT_QUES_MOD       (0x0080): Questionable modulation measurement
			TLPM_STATBIT_QUES_CAL       (0x0100): Questionable calibration
			TLPM_STATBIT_QUES_ENER      (0x0200): Questionable energy measurement
			TLPM_STATBIT_QUES_10        (0x0400): Reserved
			TLPM_STATBIT_QUES_11        (0x0800): Reserved
			TLPM_STATBIT_QUES_12        (0x1000): Reserved
			TLPM_STATBIT_QUES_INST      (0x2000): Instrument summary
			TLPM_STATBIT_QUES_WARN      (0x4000): Command warning
			TLPM_STATBIT_QUES_15        (0x8000): Reserved
			
			OPERATION STATUS REGISTER bits (see SCPI 99.0 §9)
			TLPM_STATBIT_OPER_CAL       (0x0001): The instrument is currently performing a calibration.
			TLPM_STATBIT_OPER_SETT      (0x0002): The instrument is waiting for signals to stabilize for measurements.
			TLPM_STATBIT_OPER_RANG      (0x0004): The instrument is currently changing its range.
			TLPM_STATBIT_OPER_SWE       (0x0008): A sweep is in progress.
			TLPM_STATBIT_OPER_MEAS      (0x0010): The instrument is actively measuring.
			TLPM_STATBIT_OPER_TRIG      (0x0020): The instrument is in a “wait for trigger” state of the trigger model.
			TLPM_STATBIT_OPER_ARM       (0x0040): The instrument is in a “wait for arm” state of the trigger model.
			TLPM_STATBIT_OPER_CORR      (0x0080): The instrument is currently performing a correction (Auto-PID tune).
			TLPM_STATBIT_OPER_SENS      (0x0100): Optical powermeter sensor connected and operable.
			TLPM_STATBIT_OPER_DATA      (0x0200): Measurement data ready for fetch.
			TLPM_STATBIT_OPER_THAC      (0x0400): Thermopile accelerator active.
			TLPM_STATBIT_OPER_11        (0x0800): Reserved
			TLPM_STATBIT_OPER_12        (0x1000): Reserved
			TLPM_STATBIT_OPER_INST      (0x2000): One of n multiple logical instruments is reporting OPERational status.
			TLPM_STATBIT_OPER_PROG      (0x4000): A user-defined programming is currently in the run state.
			TLPM_STATBIT_OPER_15        (0x8000): Reserved
			
			Thorlabs defined MEASRUEMENT STATUS REGISTER bits
			TLPM_STATBIT_MEAS_0         (0x0001): Reserved
			TLPM_STATBIT_MEAS_1         (0x0002): Reserved
			TLPM_STATBIT_MEAS_2         (0x0004): Reserved
			TLPM_STATBIT_MEAS_3         (0x0008): Reserved
			TLPM_STATBIT_MEAS_4         (0x0010): Reserved
			TLPM_STATBIT_MEAS_5         (0x0020): Reserved
			TLPM_STATBIT_MEAS_6         (0x0040): Reserved
			TLPM_STATBIT_MEAS_7         (0x0080): Reserved
			TLPM_STATBIT_MEAS_8         (0x0100): Reserved
			TLPM_STATBIT_MEAS_9         (0x0200): Reserved
			TLPM_STATBIT_MEAS_10        (0x0400): Reserved
			TLPM_STATBIT_MEAS_11        (0x0800): Reserved
			TLPM_STATBIT_MEAS_12        (0x1000): Reserved
			TLPM_STATBIT_MEAS_13        (0x2000): Reserved
			TLPM_STATBIT_MEAS_14        (0x4000): Reserved
			TLPM_STATBIT_MEAS_15        (0x8000): Reserved
			
			Thorlabs defined Auxiliary STATUS REGISTER bits
			TLPM_STATBIT_AUX_NTC        (0x0001): Auxiliary NTC temperature sensor connected.
			TLPM_STATBIT_AUX_EMM        (0x0002): External measurement module connected.
			TLPM_STATBIT_AUX_2          (0x0004): Reserved
			TLPM_STATBIT_AUX_3          (0x0008): Reserved
			TLPM_STATBIT_AUX_EXPS       (0x0010): External power supply connected
			TLPM_STATBIT_AUX_BATC       (0x0020): Battery charging
			TLPM_STATBIT_AUX_BATL       (0x0040): Battery low
			TLPM_STATBIT_AUX_IPS        (0x0080): Apple(tm) authentification supported.
			TLPM_STATBIT_AUX_IPF        (0x0100): Apple(tm) authentification failed.
			TLPM_STATBIT_AUX_9          (0x0200): Reserved
			TLPM_STATBIT_AUX_10         (0x0400): Reserved
			TLPM_STATBIT_AUX_11         (0x0800): Reserved
			TLPM_STATBIT_AUX_12         (0x1000): Reserved
			TLPM_STATBIT_AUX_13         (0x2000): Reserved
			TLPM_STATBIT_AUX_14         (0x4000): Reserved
			TLPM_STATBIT_AUX_15         (0x8000): Reserved
			
		Returns:
			value(int16) : This parameter returns the value of the selected register.
		"""
		pyvalue = c_int16(0)
		pInvokeResult = self.dll.TLPMX_readRegister(self.devSession, c_int16(reg), byref(pyvalue))
		self.__testForError(pInvokeResult)
		return  pyvalue.value

	def presetRegister(self):
		"""
		This function presets all status registers to default.
		
		"""
		pInvokeResult = self.dll.TLPMX_presetRegister(self.devSession)
		self.__testForError(pInvokeResult)

	def sendNTPRequest(self, timeMode, timeZone):
		"""
		This function sets the system date and time of the powermeter.
		
		Notes:
		(1) Date and time are displayed on instruments screen and are used as timestamp for data saved to memory card.
		(2) The function is only available on PM100D, PM200, PM400.
		
		Args:
			timeMode(int16)
			timeZone(int16)
		Returns:
			IPAddress(string)
		"""
		pyIPAddress = create_string_buffer(1024)
		pInvokeResult = self.dll.TLPMX_sendNTPRequest(self.devSession, c_int16(timeMode), c_int16(timeZone), pyIPAddress)
		self.__testForError(pInvokeResult)
		return c_char_p(pyIPAddress.raw).value

	def setTime(self, year, month, day, hour, minute, second):
		"""
		This function sets the system date and time of the powermeter.
		
		Notes:
		(1) Date and time are displayed on instruments screen and are used as timestamp for data saved to memory card.
		(2) The function is only available on PM100D, PM200, PM400.
		
		Args:
			year(int16) : This parameter specifies the actual year in the format yyyy e.g. 2009.
			month(int16) : This parameter specifies the actual month in the format mm e.g. 01.
			day(int16) : This parameter specifies the actual day in the format dd e.g. 15.
			
			hour(int16) : This parameter specifies the actual hour in the format hh e.g. 14.
			
			minute(int16) : This parameter specifies the actual minute in the format mm e.g. 43.
			
			second(int16) : This parameter specifies the actual second in the format ss e.g. 50.
			
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_setTime(self.devSession, c_int16(year), c_int16(month), c_int16(day), c_int16(hour), c_int16(minute), c_int16(second))
		self.__testForError(pInvokeResult)

	def getTime(self):
		"""
		This function returns the system date and time of the powermeter.
		
		Notes:
		(1) Date and time are displayed on instruments screen and are used as timestamp for data saved to memory card.
		(2) The function is only available on PM100D, PM200, PM400.
		
		Args:
		Returns:
			year(int16) : This parameter specifies the actual year in the format yyyy.
			month(int16) : This parameter specifies the actual month in the format mm.
			day(int16) : This parameter specifies the actual day in the format dd.
			hour(int16) : This parameter specifies the actual hour in the format hh.
			minute(int16) : This parameter specifies the actual minute in the format mm.
			second(int16) : This parameter specifies the actual second in the format ss.
		"""
		pyyear = c_int16(0)
		pymonth = c_int16(0)
		pyday = c_int16(0)
		pyhour = c_int16(0)
		pyminute = c_int16(0)
		pysecond = c_int16(0)
		pInvokeResult = self.dll.TLPMX_getTime(self.devSession, byref(pyyear), byref(pymonth), byref(pyday), byref(pyhour), byref(pyminute), byref(pysecond))
		self.__testForError(pInvokeResult)
		return  pyyear.value, pymonth.value, pyday.value, pyhour.value, pyminute.value, pysecond.value

	def setSummertime(self, timeMode):
		"""
		This function sets the clock to summertime.
		
		Notes:
		(1) Date and time are displayed on instruments screen and are used as timestamp for data saved to memory card.
		(2) The function is only available on PM5020
		
		Args:
			timeMode(int16)
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_setSummertime(self.devSession, c_int16(timeMode))
		self.__testForError(pInvokeResult)

	def getSummertime(self):
		"""
		This function returns if the device uses the summertime.
		
		Notes:
		(1) Date and time are displayed on instruments screen and are used as timestamp for data saved to memory card.
		(2) The function is only available on PM5020.
		
		Args:
		Returns:
			timeMode(int16)
		"""
		pytimeMode = c_int16(0)
		pInvokeResult = self.dll.TLPMX_getSummertime(self.devSession, byref(pytimeMode))
		self.__testForError(pInvokeResult)
		return  pytimeMode.value

	def setLineFrequency(self, lineFrequency):
		"""
		This function selects the line frequency.
		
		Notes:
		(1) The function is only available on PM100A, PM100D, PM100USB, PM200.
		
		
		Args:
			lineFrequency(int16) : This parameter specifies the line frequency.
			
			Accepted values:
			  TLPM_LINE_FREQ_50 (50): 50Hz
			  TLPM_LINE_FREQ_60 (60): 60Hz
			
			
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_setLineFrequency(self.devSession, c_int16(lineFrequency))
		self.__testForError(pInvokeResult)

	def getLineFrequency(self):
		"""
		This function returns the selected line frequency.
		
		Notes:
		(1) The function is only available on PM100A, PM100D, PM100USB, PM200.
		
		
		Args:
		Returns:
			lineFrequency(int16) : This parameter returns the selected line frequency in Hz.
		"""
		pylineFrequency = c_int16(0)
		pInvokeResult = self.dll.TLPMX_getLineFrequency(self.devSession, byref(pylineFrequency))
		self.__testForError(pInvokeResult)
		return  pylineFrequency.value

	def getBatteryVoltage(self):
		"""
		This function is used to obtain the battery voltage readings from the instrument.
		
		Remark:
		(1) This function is only supported with the PM160 and PM160T.
		(2) This function obtains the latest battery voltage measurement result.
		(3) With the USB cable connected this function will obtain the loading voltage. Only with USB cable disconnected (Bluetooth connection) the actual battery voltage can be read. 
		
		Args:
		Returns:
			voltage(double) : This parameter returns the battery voltage in volts [V].
		"""
		pyvoltage = c_double(0)
		pInvokeResult = self.dll.TLPMX_getBatteryVoltage(self.devSession, byref(pyvoltage))
		self.__testForError(pInvokeResult)
		return  pyvoltage.value

	def setDispBrightness(self, val):
		"""
		This function sets the display brightness.
		
		Args:
			val(double) : This parameter specifies the display brightness.
			
			Range   : 0.0 .. 1.0
			Default : 1.0
			
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_setDispBrightness(self.devSession, c_double(val))
		self.__testForError(pInvokeResult)

	def getDispBrightness(self):
		"""
		This function returns the display brightness.
		
		
		Args:
		Returns:
			pVal(double) : This parameter returns the display brightness. Value range is 0.0 to 1.0.
		"""
		pypVal = c_double(0)
		pInvokeResult = self.dll.TLPMX_getDispBrightness(self.devSession, byref(pypVal))
		self.__testForError(pInvokeResult)
		return  pypVal.value

	def setDispContrast(self, val):
		"""
		This function sets the display contrast of a PM100D.
		
		Note: The function is available on PM100D only.
		
		Args:
			val(double) : This parameter specifies the display contrast.
			
			Range   : 0.0 .. 1.0
			Default : 0.5
			
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_setDispContrast(self.devSession, c_double(val))
		self.__testForError(pInvokeResult)

	def getDispContrast(self):
		"""
		This function returns the display contrast of a PM100D.
		
		Note: This function is available on PM100D only
		
		Args:
		Returns:
			pVal(double) : This parameter returns the display contrast (0..1).
		"""
		pypVal = c_double(0)
		pInvokeResult = self.dll.TLPMX_getDispContrast(self.devSession, byref(pypVal))
		self.__testForError(pInvokeResult)
		return  pypVal.value

	def beep(self):
		"""
		Plays a beep sound.
		
		Note: Only supported by PM5020.
		"""
		pInvokeResult = self.dll.TLPMX_beep(self.devSession)
		self.__testForError(pInvokeResult)

	def setInputFilterState(self, inputFilterState, channel = 1):
		"""
		This function sets the instrument's photodiode input filter state.
		
		Notes:
		(1) The function is only available on PM100D, PM100A, PM100USB, PM200, PM400.
		
		
		Args:
			inputFilterState(int16) : This parameter specifies the input filter mode.
			
			Acceptable values:
			  TLPM_INPUT_FILTER_STATE_OFF (0) input filter off
			  TLPM_INPUT_FILTER_STATE_ON  (1) input filter on
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_setInputFilterState(self.devSession, c_int16(inputFilterState), c_uint16(channel))
		self.__testForError(pInvokeResult)

	def getInputFilterState(self, channel = 1):
		"""
		This function returns the instrument's photodiode input filter state.
		
		Notes:
		(1) The function is only available on PM100D, PM100A, PM100USB, PM200, PM400.
		
		
		Args:
			
			Return values:
			  TLPM_INPUT_FILTER_STATE_OFF (0) input filter off
			  TLPM_INPUT_FILTER_STATE_ON  (1) input filter on
			
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			inputFilterState(int16) : This parameter returns the input filter state.
		"""
		pyinputFilterState = c_int16(0)
		pInvokeResult = self.dll.TLPMX_getInputFilterState(self.devSession, byref(pyinputFilterState), c_uint16(channel))
		self.__testForError(pInvokeResult)
		return  pyinputFilterState.value

	def setAccelState(self, accelState, channel = 1):
		"""
		This function sets the thermopile acceleration state.
		
		Notes:
		(1) The function is only available on PM100D, PM100A, PM100USB, PM160T, PM200.
		
		
		Args:
			accelState(int16) : This parameter specifies the thermopile acceleration mode.
			
			Acceptable values:
			  TLPM_ACCELERATION_STATE_OFF (0): thermopile acceleration off
			  TLPM_ACCELERATION_STATE_ON  (1): thermopile acceleration on
			
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_setAccelState(self.devSession, c_int16(accelState), c_uint16(channel))
		self.__testForError(pInvokeResult)

	def getAccelState(self, channel = 1):
		"""
		This function returns the thermopile acceleration state.
		
		Notes:
		(1) The function is only available on PM100D, PM100A, PM100USB, PM160T, PM200, PM400.
		
		
		Args:
			
			Return values:
			  TLPM_ACCELERATION_STATE_OFF (0): thermopile acceleration off
			  TLPM_ACCELERATION_STATE_ON  (1): thermopile acceleration on
			
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			accelState(int16) : This parameter returns the thermopile acceleration mode.
		"""
		pyaccelState = c_int16(0)
		pInvokeResult = self.dll.TLPMX_getAccelState(self.devSession, byref(pyaccelState), c_uint16(channel))
		self.__testForError(pInvokeResult)
		return  pyaccelState.value

	def setAccelMode(self, accelMode, channel = 1):
		"""
		This function sets the thermopile acceleration auto mode.
		
		While thermopile acceleration improves displaying changing measurement values it unfortunately adds extra noise which can become noticeable on constant values measurements. With acceleration mode set to AUTO the instrument enables the acceleration circuitry after big measurement value changes for five times of "Tau". See also functions <Set Thermopile Accelerator Tau> and <Set Thermopile Accelerator State>.
		
		With calling <Set Thermopile Accelerator State> the accelerator mode will always be reset to MANUAL.
		
		Notes:
		(1) The function is only available on PM100D, PM100A, PM100USB, PM160T, PM200, PM400.
		
		
		Args:
			accelMode(int16) : This parameter specifies the thermopile acceleration mode.
			
			Acceptable values:
			  TLPM_ACCELERATION_MANUAL (0): auto acceleration off
			  TLPM_ACCELERATION_AUTO   (1): auto acceleration on
			
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_setAccelMode(self.devSession, c_int16(accelMode), c_uint16(channel))
		self.__testForError(pInvokeResult)

	def getAccelMode(self, channel = 1):
		"""
		This function returns the thermopile acceleration mode.
		
		Notes:
		(1) The function is only available on PM100D, PM100A, PM100USB, PM160T, PM200, PM400.
		
		
		Args:
			
			Return values:
			  TLPM_ACCELERATION_MANUAL (0): auto acceleration off
			  TLPM_ACCELERATION_AUTO   (1): auto acceleration on
			
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			accelMode(int16) : This parameter returns the thermopile acceleration mode.
		"""
		pyaccelMode = c_int16(0)
		pInvokeResult = self.dll.TLPMX_getAccelMode(self.devSession, byref(pyaccelMode), c_uint16(channel))
		self.__testForError(pInvokeResult)
		return  pyaccelMode.value

	def setAccelTau(self, accelTau, channel = 1):
		"""
		This function sets the thermopile acceleration time constant in seconds [s].
		
		Notes:
		(1) The function is only available on PM100D, PM100A, PM100USB, PM200, PM400.
		
		
		Args:
			accelTau(double) : This parameter specifies the thermopile acceleration time constant in seconds [s].
			
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_setAccelTau(self.devSession, c_double(accelTau), c_uint16(channel))
		self.__testForError(pInvokeResult)

	def getAccelTau(self, attribute, channel = 1):
		"""
		This function returns the thermopile acceleration time constant in seconds [s].
		
		Notes:
		(1) The function is only available on PM100D, PM100A, PM100USB, PM200, PM400.
		
		
		Args:
			attribute(int16) : This parameter specifies the value to be queried.
			
			Acceptable values:
			  TLPM_ATTR_SET_VAL  (0): Set value
			  TLPM_ATTR_MIN_VAL  (1): Minimum value
			  TLPM_ATTR_MAX_VAL  (2): Maximum value
			  TLPM_ATTR_DFLT_VAL (3): Default value
			
			
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			accelTau(double) : This parameter returns the thermopile acceleration time constant in seconds [s].
		"""
		pyaccelTau = c_double(0)
		pInvokeResult = self.dll.TLPMX_getAccelTau(self.devSession, c_int16(attribute), byref(pyaccelTau), c_uint16(channel))
		self.__testForError(pInvokeResult)
		return  pyaccelTau.value

	def setInputAdapterType(self, type, channel = 1):
		"""
		This function sets the sensor type to assume for custom sensors without calibration data memory connected to the instrument.
		
		Notes:
		(1) The function is only available on PM100D, PM100A, PM100USB, PM200, PM400.
		
		
		Args:
			type(int16) : This parameter specifies the custom sensor type.
			
			Acceptable values:
			 SENSOR_TYPE_PD_SINGLE (1): Photodiode sensor
			 SENSOR_TYPE_THERMO    (2): Thermopile sensor
			 SENSOR_TYPE_PYRO      (3): Pyroelectric sensor
			
			Value SENSOR_TYPE_PYRO is only available for energy meter instruments.
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_setInputAdapterType(self.devSession, c_int16(type), c_uint16(channel))
		self.__testForError(pInvokeResult)

	def getInputAdapterType(self, channel = 1):
		"""
		This function returns the assumed sensor type for custom sensors without calibration data memory connected to the instrument.
		
		Notes:
		(1) The function is only available on PM100D, PM100A, PM100USB, PM200, PM400.
		
		
		Args:
			
			Remark:
			The meanings of the obtained sensor type are:
			
			Sensor Types:
			 SENSOR_TYPE_PD_SINGLE (1): Photodiode sensor
			 SENSOR_TYPE_THERMO    (2): Thermopile sensor
			 SENSOR_TYPE_PYRO      (3): Pyroelectric sensor
			 SENSOR_TYPE_4Q        (4): 4 Quadrant sensor
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			type(int16) : This parameter returns the custom sensor type.
		"""
		pytype = c_int16(0)
		pInvokeResult = self.dll.TLPMX_getInputAdapterType(self.devSession, byref(pytype), c_uint16(channel))
		self.__testForError(pInvokeResult)
		return  pytype.value

	def setAvgTime(self, avgTime, channel = 1):
		"""
		This function sets the average time for measurement value generation.
		
		Args:
			avgTime(double) : This parameter specifies the average time in seconds.
			
			The value will be rounded to the closest multiple of the device's internal sampling rate.
			
			Remark: 
			To get an measurement value from the device the timeout in your application has to be longer than the average time.
			
			
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_setAvgTime(self.devSession, c_double(avgTime), c_uint16(channel))
		self.__testForError(pInvokeResult)

	def getAvgTime(self, attribute, channel = 1):
		"""
		This function returns the average time for measurement value generation.
		
		
		Args:
			attribute(int16) : This parameter specifies the value to be queried.
			
			Acceptable values:
			  TLPM_ATTR_SET_VAL  (0): Set value
			  TLPM_ATTR_MIN_VAL  (1): Minimum value
			  TLPM_ATTR_MAX_VAL  (2): Maximum value
			  TLPM_ATTR_DFLT_VAL (3): Default value
			
			
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			avgTime(double) : This parameter returns the specified average time in seconds.
		"""
		pyavgTime = c_double(0)
		pInvokeResult = self.dll.TLPMX_getAvgTime(self.devSession, c_int16(attribute), byref(pyavgTime), c_uint16(channel))
		self.__testForError(pInvokeResult)
		return  pyavgTime.value

	def setAvgCnt(self, averageCount, channel = 1):
		"""
		This function sets the average count for measurement value generation.
		
		Notes:
		(1) The function is only available on PM100A, PM100D, PM100USB, PM200, PM400.
		(2) The function is deprecated and kept for legacy reasons. Its recommended to use TLPM_setAvgTime() instead.
		
		
		Args:
			averageCount(int16) : This parameter specifies the average count.
			The default value is 1.
			
			Remark: 
			Depending on the powermeter model internal there are taken up to 3000 measurements per second.
			In this example   Average Time = Average Count / 3000 [s].
			To get an measurement value from the device the timeout in your application has to be longer than the calculated average time.
			
			
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_setAvgCnt(self.devSession, c_int16(averageCount), c_uint16(channel))
		self.__testForError(pInvokeResult)

	def getAvgCnt(self, channel = 1):
		"""
		This function returns the average count for measurement value generation.
		
		Notes:
		(1) The function is only available on PM100A, PM100D, PM100USB, PM200, PM400.
		(2) The function is deprecated and kept for legacy reasons. Its recommended to use TLPM_getAvgTime() instead.
		
		
		Args:
			
			Remark: 
			Depending on the powermeter model internal there are taken up to 3000 measurements per second.
			In this example   Average Time = Average Count / 3000 [s].
			To get an measurement value from the device the timeout in your application has to be longer than the calculated average time.
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			averageCount(int16) : This parameter returns the actual Average Count.
		"""
		pyaverageCount = c_int16(0)
		pInvokeResult = self.dll.TLPMX_getAvgCnt(self.devSession, byref(pyaverageCount), c_uint16(channel))
		self.__testForError(pInvokeResult)
		return  pyaverageCount.value

	def setAttenuation(self, attenuation, channel = 1):
		"""
		This function sets the input attenuation.
		
		Notes:
		(1) The function is only available on PM100A, PM100D, PM100USB, PM200, PM400.
		
		
		Args:
			attenuation(double) : This parameter specifies the input attenuation in dezibel [dB].
			
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_setAttenuation(self.devSession, c_double(attenuation), c_uint16(channel))
		self.__testForError(pInvokeResult)

	def getAttenuation(self, attribute, channel = 1):
		"""
		This function returns the input attenuation.
		
		Notes:
		(1) The function is only available on PM100A, PM100D, PM100USB, PM200, PM400.
		
		
		Args:
			attribute(int16) : This parameter specifies the value to be queried.
			
			Acceptable values:
			  TLPM_ATTR_SET_VAL  (0): Set value
			  TLPM_ATTR_MIN_VAL  (1): Minimum value
			  TLPM_ATTR_MAX_VAL  (2): Maximum value
			  TLPM_ATTR_DFLT_VAL (3): Default value
			
			
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			attenuation(double) : This parameter returns the specified input attenuation in dezibel [dB].
		"""
		pyattenuation = c_double(0)
		pInvokeResult = self.dll.TLPMX_getAttenuation(self.devSession, c_int16(attribute), byref(pyattenuation), c_uint16(channel))
		self.__testForError(pInvokeResult)
		return  pyattenuation.value

	def startDarkAdjust(self, channel = 1):
		"""
		This function starts the dark current/zero offset adjustment procedure.
		
		Remark: 
		(1) You have to darken the input before starting dark/zero adjustment.
		(2) You can get the state of dark/zero adjustment with <Get Dark Adjustment State>
		(3) You can stop dark/zero adjustment with <Cancel Dark Adjustment>
		(4) You get the dark/zero value with <Get Dark Offset>
		(5) Energy sensors do not support this function
		
		Args:
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_startDarkAdjust(self.devSession, c_uint16(channel))
		self.__testForError(pInvokeResult)

	def cancelDarkAdjust(self, channel = 1):
		"""
		This function cancels a running dark current/zero offset adjustment procedure.
		
		
		Args:
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_cancelDarkAdjust(self.devSession, c_uint16(channel))
		self.__testForError(pInvokeResult)

	def getDarkAdjustState(self, channel = 1):
		"""
		This function returns the state of a dark current/zero offset adjustment procedure previously initiated by <Start Dark Adjust>.
		
		
		Args:
			
			Possible return values are:
			TLPM_STAT_DARK_ADJUST_FINISHED (0) : no dark adjustment running
			TLPM_STAT_DARK_ADJUST_RUNNING  (1) : dark adjustment is running
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			state(int16) : This parameter returns the dark adjustment state.
		"""
		pystate = c_int16(0)
		pInvokeResult = self.dll.TLPMX_getDarkAdjustState(self.devSession, byref(pystate), c_uint16(channel))
		self.__testForError(pInvokeResult)
		return  pystate.value

	def setDarkOffset(self, darkOffset, channel = 1):
		"""
		This function returns the dark/zero offset.
		
		The function is not supported with energy sensors.
		
		Args:
			darkOffset(double) : This parameter returns the dark/zero offset.
			
			The unit of the returned offset value depends on the sensor type. Photodiodes return the dark offset in ampere [A]. Thermal sensors return the dark offset in volt [V].
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_setDarkOffset(self.devSession, c_double(darkOffset), c_uint16(channel))
		self.__testForError(pInvokeResult)

	def getDarkOffset(self, channel = 1):
		"""
		This function returns the dark/zero offset.
		
		The function is not supported with energy sensors.
		
		Args:
			
			The unit of the returned offset value depends on the sensor type. Photodiodes return the dark offset in ampere [A]. Thermal sensors return the dark offset in volt [V].
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			darkOffset(double) : This parameter returns the dark/zero offset.
		"""
		pydarkOffset = c_double(0)
		pInvokeResult = self.dll.TLPMX_getDarkOffset(self.devSession, byref(pydarkOffset), c_uint16(channel))
		self.__testForError(pInvokeResult)
		return  pydarkOffset.value

	def startZeroPos(self, channel = 1):
		"""
		Use this command to start a background task to measure the actual beam position and use it as position correction in the future. Before starting the correction ensure light source is hitting the sensor area. Position is floating if no beam is hitting the sensor. This command only starts the zeroing procedure running in background for at least one second. During zero procedure, measuring is not possible. To test if zeroing is still running use SENS#:CORR:COLL:ZERO:STAT? or poll for Zeroing flag in STAT:OPER:COND?. If you want to abort previously started procedure use the SENS#:CORR:COLL:POS:ZERO:ABOR command. If zeroing is complete (by error or success) you may want to test for error using SYST:ERR? command. If you want to set a custom zero value use command. Zero parameter is not stored persistently. It will be lost after reboot!
		
		Supported by PM400 firmware 1.5.0 and newer.
		
		Args:
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_startZeroPos(self.devSession, c_uint16(channel))
		self.__testForError(pInvokeResult)

	def cancelZeroPos(self, channel = 1):
		"""
		Use this command to abort a previously started position zero correction. The zeroing of position is running as asynchronous background operation. Aborting the sequence will end the background operation and enables measuring with the old zero value. To start a new zeroing use SENS#:CORR:COLL:POS:ZERO command.
		
		
		Args:
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_cancelZeroPos(self.devSession, c_uint16(channel))
		self.__testForError(pInvokeResult)

	def setZeroPos(self, zeroX, zeroY, channel = 1):
		"""
		Use this command to set beam position zero correction coordinate in um. Zero parameter is not stored persistently. It will be lost after reboot!
		
		Args:
			zeroX(double) : This parameter set the zero x in µm.
			zeroY(double) : This parameter set the zero y in µm.
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_setZeroPos(self.devSession, c_double(zeroX), c_double(zeroY), c_uint16(channel))
		self.__testForError(pInvokeResult)

	def getZeroPos(self, channel = 1):
		"""
		Use this command to get beam position zero correction coordinate in um. To update the zero value you can either call SENS#:CORR:COLL:POS:ZERO or the command. Zero parameter is not stored persistently. It will be lost after reboot!
		
		Args:
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			pZeroX(double) : This parameter returns the zero x value in µm.
			pZeroY(double) : This parameter returns the zero y value in µm.
		"""
		pypZeroX = c_double(0)
		pypZeroY = c_double(0)
		pInvokeResult = self.dll.TLPMX_getZeroPos(self.devSession, byref(pypZeroX), byref(pypZeroY), c_uint16(channel))
		self.__testForError(pInvokeResult)
		return  pypZeroX.value, pypZeroY.value

	def setBeamDia(self, beamDiameter, channel = 1):
		"""
		This function sets the users beam diameter in millimeter [mm].
		
		Notes:
		(1) The function is only available on PM100A, PM100D, PM100USB, PM200, PM400.
		(2) Beam diameter set value is used for calculating power and energy density.
		
		
		Args:
			beamDiameter(double) : This parameter specifies the users beam diameter in millimeter [mm].
			
			Remark:
			Beam diameter set value is used for calculating power and energy density.
			
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_setBeamDia(self.devSession, c_double(beamDiameter), c_uint16(channel))
		self.__testForError(pInvokeResult)

	def getBeamDia(self, attribute, channel = 1):
		"""
		This function returns the users beam diameter in millimeter [mm].
		
		Notes:
		(1) The function is only available on PM100A, PM100D, PM100USB, PM200, PM101, PM102, PM400.
		(2) Beam diameter set value is used for calculating power and energy density.
		
		
		Args:
			attribute(int16) : This parameter specifies the value to be queried.
			
			Acceptable values:
			  TLPM_ATTR_SET_VAL  (0): Set value
			  TLPM_ATTR_MIN_VAL  (1): Minimum value
			  TLPM_ATTR_MAX_VAL  (2): Maximum value
			
			
			Remark:
			Beam diameter set value is used for calculating power and energy density.
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			beamDiameter(double) : This parameter returns the specified beam diameter in millimeter [mm].
		"""
		pybeamDiameter = c_double(0)
		pInvokeResult = self.dll.TLPMX_getBeamDia(self.devSession, c_int16(attribute), byref(pybeamDiameter), c_uint16(channel))
		self.__testForError(pInvokeResult)
		return  pybeamDiameter.value

	def setWavelength(self, wavelength, channel = 1):
		"""
		This function sets the users wavelength in nanometer [nm].
		
		Remark:
		Wavelength set value is used for calculating power.
		
		
		Args:
			wavelength(double) : This parameter specifies the users wavelength in nanometer [nm].
			
			Remark:
			Wavelength set value is used for calculating power.
			
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_setWavelength(self.devSession, c_double(wavelength), c_uint16(channel))
		self.__testForError(pInvokeResult)

	def getWavelength(self, attribute, channel = 1):
		"""
		This function returns the users wavelength in nanometer [nm].
		
		Remark:
		Wavelength set value is used for calculating power.
		
		
		Args:
			attribute(int16) : This parameter specifies the value to be queried.
			
			Acceptable values:
			  TLPM_ATTR_SET_VAL  (0): Set value
			  TLPM_ATTR_MIN_VAL  (1): Minimum value
			  TLPM_ATTR_MAX_VAL  (2): Maximum value
			
			
			Remark:
			Wavelength set value is used for calculating power.
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			wavelength(double) : This parameter returns the specified wavelength in nanometer [nm].
		"""
		pywavelength = c_double(0)
		pInvokeResult = self.dll.TLPMX_getWavelength(self.devSession, c_int16(attribute), byref(pywavelength), c_uint16(channel))
		self.__testForError(pInvokeResult)
		return  pywavelength.value

	def setPhotodiodeResponsivity(self, response, channel = 1):
		"""
		This function sets the photodiode responsivity in ampere per watt [A/W].
		
		Notes:
		(1) The function is only available on PM100A, PM100D, PM100USB, PM200, PM400.
		
		
		Args:
			response(double) : This parameter specifies the photodiode responsivity in ampere per watt [A/W].
			
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_setPhotodiodeResponsivity(self.devSession, c_double(response), c_uint16(channel))
		self.__testForError(pInvokeResult)

	def getPhotodiodeResponsivity(self, attribute, channel = 1):
		"""
		This function returns the photodiode responsivity in ampere per watt [A/W].
		
		Notes:
		(1) The function is only available on PM100A, PM100D, PM100USB, PM200, PM400.
		
		
		Args:
			attribute(int16) : This parameter specifies the value to be queried.
			
			Acceptable values:
			  TLPM_ATTR_SET_VAL  (0): Set value
			  TLPM_ATTR_MIN_VAL  (1): Minimum value
			  TLPM_ATTR_MAX_VAL  (2): Maximum value
			  TLPM_ATTR_DFLT_VAL (3): Default value
			
			
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			responsivity(double) : This parameter returns the specified photodiode responsivity in ampere per watt [A/W].
		"""
		pyresponsivity = c_double(0)
		pInvokeResult = self.dll.TLPMX_getPhotodiodeResponsivity(self.devSession, c_int16(attribute), byref(pyresponsivity), c_uint16(channel))
		self.__testForError(pInvokeResult)
		return  pyresponsivity.value

	def setThermopileResponsivity(self, response, channel = 1):
		"""
		This function sets the thermopile responsivity in volt per watt [V/W]
		
		Notes:
		(1) The function is only available on PM100A, PM100D, PM100USB, PM200, PM400.
		
		
		Args:
			response(double) : This parameter specifies the thermopile responsivity in volt per watt [V/W]
			
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_setThermopileResponsivity(self.devSession, c_double(response), c_uint16(channel))
		self.__testForError(pInvokeResult)

	def getThermopileResponsivity(self, attribute, channel = 1):
		"""
		This function returns the thermopile responsivity in volt per watt [V/W]
		
		Notes:
		(1) The function is only available on PM100A, PM100D, PM100USB, PM160T, PM200, PM400.
		
		
		Args:
			attribute(int16) : This parameter specifies the value to be queried.
			
			Acceptable values:
			  TLPM_ATTR_SET_VAL  (0): Set value
			  TLPM_ATTR_MIN_VAL  (1): Minimum value
			  TLPM_ATTR_MAX_VAL  (2): Maximum value
			  TLPM_ATTR_DFLT_VAL (3): Default value
			
			
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			responsivity(double) : This parameter returns the specified thermopile responsivity in volt per watt [V/W]
		"""
		pyresponsivity = c_double(0)
		pInvokeResult = self.dll.TLPMX_getThermopileResponsivity(self.devSession, c_int16(attribute), byref(pyresponsivity), c_uint16(channel))
		self.__testForError(pInvokeResult)
		return  pyresponsivity.value

	def setPyrosensorResponsivity(self, response, channel = 1):
		"""
		This function sets the pyrosensor responsivity in volt per joule [V/J]
		
		Notes:
		(1) The function is only available on PM100A, PM100D, PM100USB, PM200, PM400.
		
		
		Args:
			response(double) : This parameter specifies the pyrosensor responsivity in volt per joule [V/J]
			
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_setPyrosensorResponsivity(self.devSession, c_double(response), c_uint16(channel))
		self.__testForError(pInvokeResult)

	def getPyrosensorResponsivity(self, attribute, channel = 1):
		"""
		This function returns the pyrosensor responsivity in volt per joule [V/J]
		
		Notes:
		(1) The function is only available on PM100A, PM100D, PM100USB, PM200, PM400.
		
		
		Args:
			attribute(int16) : This parameter specifies the value to be queried.
			
			Acceptable values:
			  TLPM_ATTR_SET_VAL  (0): Set value
			  TLPM_ATTR_MIN_VAL  (1): Minimum value
			  TLPM_ATTR_MAX_VAL  (2): Maximum value
			  TLPM_ATTR_DFLT_VAL (3): Default value
			
			
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			responsivity(double) : This parameter returns the specified pyrosensor responsivity in volt per joule [V/J]
		"""
		pyresponsivity = c_double(0)
		pInvokeResult = self.dll.TLPMX_getPyrosensorResponsivity(self.devSession, c_int16(attribute), byref(pyresponsivity), c_uint16(channel))
		self.__testForError(pInvokeResult)
		return  pyresponsivity.value

	def setCurrentAutoRange(self, currentAutorangeMode, channel = 1):
		"""
		This function sets the current auto range mode.
		
		Notes:
		(1) The function is only available on PM100A, PM100D, PM100USB, PM160, PM200, PM400.
		
		
		Args:
			currentAutorangeMode(int16) : This parameter specifies the current auto range mode.
			
			Acceptable values:
			  TLPM_AUTORANGE_CURRENT_OFF (0): current auto range disabled
			  TLPM_AUTORANGE_CURRENT_ON  (1): current auto range enabled
			
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_setCurrentAutoRange(self.devSession, c_int16(currentAutorangeMode), c_uint16(channel))
		self.__testForError(pInvokeResult)

	def getCurrentAutorange(self, channel = 1):
		"""
		This function returns the current auto range mode.
		
		Notes:
		(1) The function is only available on PM100A, PM100D, PM100USB, PM160, PM200, PM400.
		
		
		Args:
			
			Return values:
			  TLPM_AUTORANGE_CURRENT_OFF (0): current auto range disabled
			  TLPM_AUTORANGE_CURRENT_ON  (1): current auto range enabled
			
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			currentAutorangeMode(int16) : This parameter returns the current auto range mode.
		"""
		pycurrentAutorangeMode = c_int16(0)
		pInvokeResult = self.dll.TLPMX_getCurrentAutorange(self.devSession, byref(pycurrentAutorangeMode), c_uint16(channel))
		self.__testForError(pInvokeResult)
		return  pycurrentAutorangeMode.value

	def setCurrentRange(self, current_to_Measure, channel = 1):
		"""
		This function sets the sensor's current range.
		
		Notes:
		(1) The function is only available on PM100A, PM100D, PM100USB, PM160, PM200, PM400.
		
		
		Args:
			current_to_Measure(double) : This parameter specifies the current value to be measured in ampere [A].
			
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_setCurrentRange(self.devSession, c_double(current_to_Measure), c_uint16(channel))
		self.__testForError(pInvokeResult)

	def getCurrentRange(self, attribute, channel = 1):
		"""
		This function returns the actual current range value.
		
		Notes:
		(1) The function is only available on PM100A, PM100D, PM100USB, PM160, PM200, PM400.
		
		
		Args:
			attribute(int16) : This parameter specifies the value to be queried.
			
			Acceptable values:
			  TLPM_ATTR_SET_VAL  (0): Set value
			  TLPM_ATTR_MIN_VAL  (1): Minimum value
			  TLPM_ATTR_MAX_VAL  (2): Maximum value
			
			
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			currentValue(double) : This parameter returns the specified current range value in ampere [A].
		"""
		pycurrentValue = c_double(0)
		pInvokeResult = self.dll.TLPMX_getCurrentRange(self.devSession, c_int16(attribute), byref(pycurrentValue), c_uint16(channel))
		self.__testForError(pInvokeResult)
		return  pycurrentValue.value

	def getCurrentRanges(self, currentValues, channel = 1):
		"""
		This function returns the actual voltage range value.
		
		Notes:
		(1) The function is only available on PM100D, PM100A, PM100USB, PM160T, PM200, PM400, PM5020, PM6x.
		
		
		Args:
			currentValues( (c_double * arrayLength)()) : This parameter returns the specified voltage range value in volts [V].
			
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			rangeCount(uint16)
		"""
		pyrangeCount = c_uint16(0)
		pInvokeResult = self.dll.TLPMX_getCurrentRanges(self.devSession, currentValues, byref(pyrangeCount), c_uint16(channel))
		self.__testForError(pInvokeResult)
		return  pyrangeCount.value

	def setCurrentRangeSearch(self, channel = 1):
		"""
		This function returns the actual voltage range value.
		
		Notes:
		(1) The function is only available on PM100D, PM100A, PM100USB, PM160T, PM200, PM400.
		
		
		Args:
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_setCurrentRangeSearch(self.devSession, c_uint16(channel))
		self.__testForError(pInvokeResult)

	def setCurrentRef(self, currentReferenceValue, channel = 1):
		"""
		This function sets the current reference value.
		
		Notes:
		(1) The function is only available on PM100A, PM100D, PM100USB, PM160, PM200, PM400.
		
		
		Args:
			currentReferenceValue(double) : This parameter specifies the current reference value in amperes [A].
			
			Remark:
			This value is used for calculating differences between the actual current value and this current reference value if Current Reference State is ON.
			
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_setCurrentRef(self.devSession, c_double(currentReferenceValue), c_uint16(channel))
		self.__testForError(pInvokeResult)

	def getCurrentRef(self, attribute, channel = 1):
		"""
		This function returns the current reference value.
		
		Notes:
		(1) The function is only available on PM100A, PM100D, PM100USB, PM160, PM200, PM400.
		
		
		Args:
			attribute(int16) : This parameter specifies the value to be queried.
			
			Acceptable values:
			  TLPM_ATTR_SET_VAL  (0): Set value
			  TLPM_ATTR_MIN_VAL  (1): Minimum value
			  TLPM_ATTR_MAX_VAL  (2): Maximum value
			  TLPM_ATTR_DFLT_VAL (3): Default value
			
			
			Remark:
			This value is used for calculating differences between the actual current value and this current reference value if Current Reference State is ON.
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			currentReferenceValue(double) : This parameter returns the specified current reference value in amperes [A].
		"""
		pycurrentReferenceValue = c_double(0)
		pInvokeResult = self.dll.TLPMX_getCurrentRef(self.devSession, c_int16(attribute), byref(pycurrentReferenceValue), c_uint16(channel))
		self.__testForError(pInvokeResult)
		return  pycurrentReferenceValue.value

	def setCurrentRefState(self, currentReferenceState, channel = 1):
		"""
		This function sets the current reference state.
		
		Notes:
		(1) The function is only available on PM100A, PM100D, PM100USB, PM160, PM200, PM400.
		
		
		Args:
			currentReferenceState(int16) : This parameter specifies the current reference state.
			
			Acceptable values:
			  TLPM_CURRENT_REF_OFF (0): Current reference disabled. Absolute measurement.
			  TLPM_CURRENT_REF_ON  (1): Current reference enabled. Relative measurement.
			
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_setCurrentRefState(self.devSession, c_int16(currentReferenceState), c_uint16(channel))
		self.__testForError(pInvokeResult)

	def getCurrentRefState(self, channel = 1):
		"""
		This function returns the current reference state.
		
		Notes:
		(1) The function is only available on PM100A, PM100D, PM100USB, PM160, PM200, PM400.
		
		
		Args:
			
			Return values:
			  TLPM_CURRENT_REF_OFF (0): Current reference disabled. Absolute measurement.
			  TLPM_CURRENT_REF_ON  (1): Current reference enabled. Relative measurement.
			
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			currentReferenceState(int16) : This parameter returns the current reference state.
		"""
		pycurrentReferenceState = c_int16(0)
		pInvokeResult = self.dll.TLPMX_getCurrentRefState(self.devSession, byref(pycurrentReferenceState), c_uint16(channel))
		self.__testForError(pInvokeResult)
		return  pycurrentReferenceState.value

	def setEnergyRange(self, energyToMeasure, channel = 1):
		"""
		This function sets the pyro sensor's energy range.
		
		Notes:
		(1) The function is only available on PM100D, PM100USB, PM200, PM400.
		
		
		Args:
			energyToMeasure(double) : This parameter specifies the energy value in joule [J] to be measured.
			
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_setEnergyRange(self.devSession, c_double(energyToMeasure), c_uint16(channel))
		self.__testForError(pInvokeResult)

	def getEnergyRange(self, attribute, channel = 1):
		"""
		This function returns the pyro sensor's energy range.
		
		Notes:
		(1) The function is only available on PM100D, PM100USB, PM200, PM400.
		
		
		Args:
			attribute(int16) : This parameter specifies the value to be queried.
			
			Acceptable values:
			  TLPM_ATTR_SET_VAL  (0): Set value
			  TLPM_ATTR_MIN_VAL  (1): Minimum value
			  TLPM_ATTR_MAX_VAL  (2): Maximum value
			
			
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			energyValue(double) : This parameter returns the specified pyro sensor's energy value in joule [J].
		"""
		pyenergyValue = c_double(0)
		pInvokeResult = self.dll.TLPMX_getEnergyRange(self.devSession, c_int16(attribute), byref(pyenergyValue), c_uint16(channel))
		self.__testForError(pInvokeResult)
		return  pyenergyValue.value

	def setEnergyRef(self, energyReferenceValue, channel = 1):
		"""
		This function sets the pyro sensor's energy reference value
		
		Notes:
		(1) The function is only available on PM100D, PM100USB, PM200, PM400.
		(2) This value is used for calculating differences between the actual energy value and this energy reference value.
		
		
		Args:
			energyReferenceValue(double) : This parameter specifies the pyro sensor's energy reference value in joule [J].
			
			Remark:
			This value is used for calculating differences between the actual energy value and this energy reference value if Energy Reference State is ON.
			
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_setEnergyRef(self.devSession, c_double(energyReferenceValue), c_uint16(channel))
		self.__testForError(pInvokeResult)

	def getEnergyRef(self, attribute, channel = 1):
		"""
		This function returns the specified pyro sensor's energy reference value.
		
		Notes:
		(1) The function is only available on PM100D, PM100USB, PM200, PM400.
		(2) The set value is used for calculating differences between the actual energy value and this energy reference value.
		
		
		Args:
			attribute(int16) : This parameter specifies the value to be queried.
			
			Acceptable values:
			  TLPM_ATTR_SET_VAL  (0): Set value
			  TLPM_ATTR_MIN_VAL  (1): Minimum value
			  TLPM_ATTR_MAX_VAL  (2): Maximum value
			  TLPM_ATTR_DFLT_VAL (3): Default value
			
			
			Remark:
			The set value is used for calculating differences between the actual energy value and this energy reference value if Energy Reference State is ON.
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			energyReferenceValue(double) : This parameter returns the specified pyro sensor's energy reference value in joule [J].
		"""
		pyenergyReferenceValue = c_double(0)
		pInvokeResult = self.dll.TLPMX_getEnergyRef(self.devSession, c_int16(attribute), byref(pyenergyReferenceValue), c_uint16(channel))
		self.__testForError(pInvokeResult)
		return  pyenergyReferenceValue.value

	def setEnergyRefState(self, energyReferenceState, channel = 1):
		"""
		This function sets the instrument's energy reference state.
		
		Notes:
		(1) The function is only available on PM100D, PM100USB, PM200, PM400.
		
		
		Args:
			energyReferenceState(int16) : This parameter specifies the energy reference state.
			
			Acceptable values:
			  TLPM_ENERGY_REF_OFF (0): Energy reference disabled. Absolute measurement.
			  TLPM_ENERGY_REF_ON  (1): Energy reference enabled. Relative measurement.
			
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_setEnergyRefState(self.devSession, c_int16(energyReferenceState), c_uint16(channel))
		self.__testForError(pInvokeResult)

	def getEnergyRefState(self, channel = 1):
		"""
		This function returns the instrument's energy reference state.
		
		Notes:
		(1) The function is only available on PM100D, PM100USB, PM200, PM400.
		
		
		Args:
			
			Return values:
			  TLPM_ENERGY_REF_OFF (0): Energy reference disabled. Absolute measurement.
			  TLPM_ENERGY_REF_ON  (1): Energy reference enabled. Relative measurement.
			
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			energyReferenceState(int16) : This parameter returns the energy reference state.
		"""
		pyenergyReferenceState = c_int16(0)
		pInvokeResult = self.dll.TLPMX_getEnergyRefState(self.devSession, byref(pyenergyReferenceState), c_uint16(channel))
		self.__testForError(pInvokeResult)
		return  pyenergyReferenceState.value

	def getFreqRange(self, channel = 1):
		"""
		This function returns the instruments frequency measurement range.
		
		Remark:
		The frequency of the input signal is calculated over at least 0.3s. So it takes at least 0.3s to get a new frequency value from the instrument.
		
		Notes:
		(1) The function is only available on PM100D, PM100A, and PM100USB.
		
		
		Args:
			
			
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			lowerFrequency(double) : This parameter returns the lower instruments frequency in [Hz].
			upperFrequency(double) : This parameter returns the upper instruments frequency in [Hz].
		"""
		pylowerFrequency = c_double(0)
		pyupperFrequency = c_double(0)
		pInvokeResult = self.dll.TLPMX_getFreqRange(self.devSession, byref(pylowerFrequency), byref(pyupperFrequency), c_uint16(channel))
		self.__testForError(pInvokeResult)
		return  pylowerFrequency.value, pyupperFrequency.value

	def setFreqMode(self, frequencyMode, channel = 1):
		"""
		This function sets the instruments frequency measurement mode. Only for photodiodes.
		
		Notes:
		(1) The function is only available on PM103
		
		
		Args:
			frequencyMode(uint16) : This parameter returns the frequency mode.
			
			CW (0)
			PEAK (1)
			
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_setFreqMode(self.devSession, c_uint16(frequencyMode), c_uint16(channel))
		self.__testForError(pInvokeResult)

	def getFreqMode(self, channel = 1):
		"""
		This function returns the instruments frequency measurement mode. 
		
		Notes:
		(1) The function is only available on PM103
		
		
		Args:
			
			CW (0)
			PEAK (1)
			
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			frequencyMode(uint16) : This parameter returns the frequency mode.
		"""
		pyfrequencyMode = c_uint16(0)
		pInvokeResult = self.dll.TLPMX_getFreqMode(self.devSession, byref(pyfrequencyMode), c_uint16(channel))
		self.__testForError(pInvokeResult)
		return  pyfrequencyMode.value

	def setPowerAutoRange(self, powerAutorangeMode, channel = 1):
		"""
		This function sets the power auto range mode.
		
		
		Args:
			powerAutorangeMode(int16) : This parameter specifies the power auto range mode.
			
			Acceptable values:
			  TLPM_AUTORANGE_POWER_OFF (0): power auto range disabled
			  TLPM_AUTORANGE_POWER_ON  (1): power auto range enabled
			
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_setPowerAutoRange(self.devSession, c_int16(powerAutorangeMode), c_uint16(channel))
		self.__testForError(pInvokeResult)

	def getPowerAutorange(self, channel = 1):
		"""
		This function returns the power auto range mode.
		
		
		Args:
			
			Return values:
			  TLPM_AUTORANGE_POWER_OFF (0): power auto range disabled
			  TLPM_AUTORANGE_POWER_ON  (0): power auto range enabled
			
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			powerAutorangeMode(int16) : This parameter returns the power auto range mode.
		"""
		pypowerAutorangeMode = c_int16(0)
		pInvokeResult = self.dll.TLPMX_getPowerAutorange(self.devSession, byref(pypowerAutorangeMode), c_uint16(channel))
		self.__testForError(pInvokeResult)
		return  pypowerAutorangeMode.value

	def setPowerRange(self, power_to_Measure, channel = 1):
		"""
		This function sets the sensor's power range.
		
		
		Args:
			power_to_Measure(double) : This parameter specifies the most positive signal level expected for the sensor input in watt [W].
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_setPowerRange(self.devSession, c_double(power_to_Measure), c_uint16(channel))
		self.__testForError(pInvokeResult)

	def getPowerRange(self, attribute, channel = 1):
		"""
		This function returns the actual power range value.
		
		
		Args:
			attribute(int16) : This parameter specifies the value to be queried.
			
			Acceptable values:
			  TLPM_ATTR_SET_VAL  (0): Set value
			  TLPM_ATTR_MIN_VAL  (1): Minimum value
			  TLPM_ATTR_MAX_VAL  (2): Maximum value
			
			
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			powerValue(double) : This parameter returns the specified power range value in watt [W].
		"""
		pypowerValue = c_double(0)
		pInvokeResult = self.dll.TLPMX_getPowerRange(self.devSession, c_int16(attribute), byref(pypowerValue), c_uint16(channel))
		self.__testForError(pInvokeResult)
		return  pypowerValue.value

	def setPowerRef(self, powerReferenceValue, channel = 1):
		"""
		This function sets the power reference value.
		
		
		Args:
			powerReferenceValue(double) : This parameter specifies the power reference value.
			
			Remark:
			(1) The power reference value has the unit specified with <Set Power Unit>.
			(2) This value is used for calculating differences between the actual power value and this power reference value if Power Reference State is ON.
			
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_setPowerRef(self.devSession, c_double(powerReferenceValue), c_uint16(channel))
		self.__testForError(pInvokeResult)

	def getPowerRef(self, attribute, channel = 1):
		"""
		This function returns the power reference value.
		
		
		Args:
			attribute(int16) : This parameter specifies the value to be queried.
			
			Acceptable values:
			  TLPM_ATTR_SET_VAL  (0): Set value
			  TLPM_ATTR_MIN_VAL  (1): Minimum value
			  TLPM_ATTR_MAX_VAL  (2): Maximum value
			  TLPM_ATTR_DFLT_VAL (3): Default value
			
			
			Remark:
			(1) The power reference value has the unit specified with <Set Power Unit>.
			(2) This value is used for calculating differences between the actual power value and this power reference value if Power Reference State is ON.
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			powerReferenceValue(double) : This parameter returns the specified power reference value.
		"""
		pypowerReferenceValue = c_double(0)
		pInvokeResult = self.dll.TLPMX_getPowerRef(self.devSession, c_int16(attribute), byref(pypowerReferenceValue), c_uint16(channel))
		self.__testForError(pInvokeResult)
		return  pypowerReferenceValue.value

	def setPowerRefState(self, powerReferenceState, channel = 1):
		"""
		This function sets the power reference state.
		
		
		Args:
			powerReferenceState(int16) : This parameter specifies the power reference state.
			
			Acceptable values:
			  TLPM_POWER_REF_OFF (0): Power reference disabled. Absolute measurement.
			  TLPM_POWER_REF_ON  (1): Power reference enabled. Relative measurement.
			
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_setPowerRefState(self.devSession, c_int16(powerReferenceState), c_uint16(channel))
		self.__testForError(pInvokeResult)

	def getPowerRefState(self, channel = 1):
		"""
		This function returns the power reference state.
		
		
		Args:
			
			Return values:
			  TLPM_POWER_REF_OFF (0): Power reference disabled. Absolute measurement.
			  TLPM_POWER_REF_ON  (1): Power reference enabled. Relative measurement.
			
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			powerReferenceState(int16) : This parameter returns the power reference state.
		"""
		pypowerReferenceState = c_int16(0)
		pInvokeResult = self.dll.TLPMX_getPowerRefState(self.devSession, byref(pypowerReferenceState), c_uint16(channel))
		self.__testForError(pInvokeResult)
		return  pypowerReferenceState.value

	def setPowerUnit(self, powerUnit, channel = 1):
		"""
		This function sets the unit of the power value.
		
		
		Args:
			powerUnit(int16) : This parameter specifies the unit of the pover value.
			
			Acceptable values:
			  TLPM_POWER_UNIT_WATT (0): power in Watt
			  TLPM_POWER_UNIT_DBM  (1): power in dBm
			
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_setPowerUnit(self.devSession, c_int16(powerUnit), c_uint16(channel))
		self.__testForError(pInvokeResult)

	def getPowerUnit(self, channel = 1):
		"""
		This function returns the unit of the power value.
		
		
		Args:
			
			Return values:
			  TLPM_POWER_UNIT_WATT (0): power in Watt
			  TLPM_POWER_UNIT_DBM  (1): power in dBm
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			powerUnit(int16) : This parameter returns the unit of the power value.
		"""
		pypowerUnit = c_int16(0)
		pInvokeResult = self.dll.TLPMX_getPowerUnit(self.devSession, byref(pypowerUnit), c_uint16(channel))
		self.__testForError(pInvokeResult)
		return  pypowerUnit.value

	def getPowerCalibrationPointsInformation(self, index, channel = 1):
		"""
		Queries the customer adjustment header like serial nr, cal date, nr of points at given index
		
		
		Args:
			index(uint16) : Index of the power calibration (range 1...5)
			Please provide a buffer of 256 characters.
			Please provide a buffer of 256 characters.
			1 = 5mW
			2 = 500mW
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			serialNumber(string) : Serial Number of the sensor.
			calibrationDate(string) : Last calibration date of this sensor
			calibrationPointsCount(uint16) : Number of calibration points of the power calibration with this sensor
			author(string)
			sensorPosition(uint16) : The position of the sencor switch of a Thorlabs S130C
		"""
		pyserialNumber = create_string_buffer(1024)
		pycalibrationDate = create_string_buffer(1024)
		pycalibrationPointsCount = c_uint16(0)
		pyauthor = create_string_buffer(1024)
		pysensorPosition = c_uint16(0)
		pInvokeResult = self.dll.TLPMX_getPowerCalibrationPointsInformation(self.devSession, c_uint16(index), pyserialNumber, pycalibrationDate, byref(pycalibrationPointsCount), pyauthor, byref(pysensorPosition), c_uint16(channel))
		self.__testForError(pInvokeResult)
		return c_char_p(pyserialNumber.raw).value, c_char_p(pycalibrationDate.raw).value, pycalibrationPointsCount.value, c_char_p(pyauthor.raw).value, pysensorPosition.value

	def getPowerCalibrationPointsState(self, index, channel = 1):
		"""
		Queries the state if the power calibration of this sensor is activated.
		
		
		Args:
			index(uint16)
			
			VI_ON: The user power calibration is used
			VI_OFF: The user power calibration is ignored in the power measurements
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			state(int16) : State if the user power calibration is activated and used for the power measurements.
		"""
		pystate = c_int16(0)
		pInvokeResult = self.dll.TLPMX_getPowerCalibrationPointsState(self.devSession, c_uint16(index), byref(pystate), c_uint16(channel))
		self.__testForError(pInvokeResult)
		return  pystate.value

	def setPowerCalibrationPointsState(self, index, state, channel = 1):
		"""
		This function activates/inactivates the power calibration of this sensor.
		
		
		Args:
			index(uint16) : Index of the power calibration (range 1...5)
			state(int16) : State if the user power calibration is activated and used for the power measurements.
			
			VI_ON: The user power calibration is used
			VI_OFF: The user power calibration is ignored in the power measurements
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_setPowerCalibrationPointsState(self.devSession, c_uint16(index), c_int16(state), c_uint16(channel))
		self.__testForError(pInvokeResult)

	def getPowerCalibrationPoints(self, index, pointCounts, wavelengths, powerCorrectionFactors, channel = 1):
		"""
		Returns a list of wavelength and the corresponding power correction factor.
		
		
		Args:
			index(uint16)
			pointCounts(uint16) : Number of points that are submitted in the wavelength and power correction factors arrays.
			Maximum of 8 wavelength - power correction factors pairs can be calibrated for each sensor.
			wavelengths( (c_double * arrayLength)()) : Array of wavelengths in nm. Requires ascending wavelength order.
			The array must contain <points counts> entries.
			powerCorrectionFactors( (c_double * arrayLength)()) : Array of power correction factorw that correspond to the wavelength array. 
			The array must contain <points counts> entries, same as wavelenght to build wavelength - power correction factors pairs.
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_getPowerCalibrationPoints(self.devSession, c_uint16(index), c_uint16(pointCounts), wavelengths, powerCorrectionFactors, c_uint16(channel))
		self.__testForError(pInvokeResult)

	def setPowerCalibrationPoints(self, index, pointCounts, wavelengths, powerCorrectionFactors, sensorPosition, channel = 1):
		"""
		Sumbits a list of wavelength and the corresponding measured power correction factors to calibrate the power measurement.
		
		
		Args:
			index(uint16) : Index of the power calibration (range 1...5)
			pointCounts(uint16) : Number of points that are submitted in the wavelength and power correction factors arrays.
			Maximum of 8 wavelength - power correction factors  pairs can be calibrated for each sensor.
			wavelengths( (c_double * arrayLength)()) : Array of wavelengths in nm. Requires ascending wavelength order.
			The array must contain <points counts> entries.
			powerCorrectionFactors( (c_double * arrayLength)()) : Array of powers correction factors that correspond to the wavelength array. 
			The array must contain <points counts> entries, same as wavelenght to build wavelength - power correction factors  pairs.
			Name of Author limited to 19 chars + ''
			sensorPosition(uint16) : The position of the sencor switch of a Thorlabs S130C
			1 = 5mW
			2 = 500mW
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			author(string) : Buffer that contains the name of the editor of the calibration.
		"""
		pyauthor = create_string_buffer(1024)
		pInvokeResult = self.dll.TLPMX_setPowerCalibrationPoints(self.devSession, c_uint16(index), c_uint16(pointCounts), wavelengths, powerCorrectionFactors, pyauthor, c_uint16(sensorPosition), c_uint16(channel))
		self.__testForError(pInvokeResult)
		return c_char_p(pyauthor.raw).value

	def reinitSensor(self, channel = 1):
		"""
		To use the user power calibration, the sensor has to be reconnected.
		Either manually remove and reconnect the sensor to the instrument or use this funtion.
		
		This function will wait 2 seconds until the sensor has been reinitialized.
		
		Args:
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_reinitSensor(self.devSession, c_uint16(channel))
		self.__testForError(pInvokeResult)

	def setVoltageAutoRange(self, voltageAutorangeMode, channel = 1):
		"""
		This function sets the voltage auto range mode.
		
		Notes:
		(1) The function is only available on PM100D, PM100A, PM100USB, PM160T, PM200, PM400.
		
		
		Args:
			voltageAutorangeMode(int16) : This parameter specifies the voltage auto range mode.
			
			Acceptable values:
			  TLPM_AUTORANGE_VOLTAGE_OFF (0): voltage auto range disabled
			  TLPM_AUTORANGE_VOLTAGE_ON  (1): voltage auto range enabled
			
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_setVoltageAutoRange(self.devSession, c_int16(voltageAutorangeMode), c_uint16(channel))
		self.__testForError(pInvokeResult)

	def getVoltageAutorange(self, channel = 1):
		"""
		This function returns the voltage auto range mode.
		
		Notes:
		(1) The function is only available on PM100D, PM100A, PM100USB, PM160T, PM200, PM400.
		
		
		Args:
			
			Return values:
			  TLPM_AUTORANGE_VOLTAGE_OFF (0): voltage auto range disabled
			  TLPM_AUTORANGE_VOLTAGE_ON  (1): voltage auto range enabled
			
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			voltageAutorangeMode(int16) : This parameter returns the voltage auto range mode.
		"""
		pyvoltageAutorangeMode = c_int16(0)
		pInvokeResult = self.dll.TLPMX_getVoltageAutorange(self.devSession, byref(pyvoltageAutorangeMode), c_uint16(channel))
		self.__testForError(pInvokeResult)
		return  pyvoltageAutorangeMode.value

	def setVoltageRange(self, voltage_to_Measure, channel = 1):
		"""
		This function sets the sensor's voltage range.
		
		Notes:
		(1) The function is only available on PM100D, PM100A, PM100USB, PM160T, PM200, PM400.
		
		
		Args:
			voltage_to_Measure(double) : This parameter specifies the voltage value to be measured in volts [V].
			
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_setVoltageRange(self.devSession, c_double(voltage_to_Measure), c_uint16(channel))
		self.__testForError(pInvokeResult)

	def getVoltageRange(self, attribute, channel = 1):
		"""
		This function returns the actual voltage range value.
		
		Notes:
		(1) The function is only available on PM100D, PM100A, PM100USB, PM160T, PM200, PM400.
		
		
		Args:
			attribute(int16) : This parameter specifies the value to be queried.
			
			Acceptable values:
			  TLPM_ATTR_SET_VAL  (0): Set value
			  TLPM_ATTR_MIN_VAL  (1): Minimum value
			  TLPM_ATTR_MAX_VAL  (2): Maximum value
			
			
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			voltageValue(double) : This parameter returns the specified voltage range value in volts [V].
		"""
		pyvoltageValue = c_double(0)
		pInvokeResult = self.dll.TLPMX_getVoltageRange(self.devSession, c_int16(attribute), byref(pyvoltageValue), c_uint16(channel))
		self.__testForError(pInvokeResult)
		return  pyvoltageValue.value

	def getVoltageRanges(self, voltageValues, channel = 1):
		"""
		This function returns the actual voltage range value.
		
		Notes:
		(1) The function is only available on PM100D, PM100A, PM100USB, PM160T, PM200, PM400.
		
		
		Args:
			voltageValues( (c_double * arrayLength)()) : This parameter returns the specified voltage range value in volts [V].
			
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			rangeCount(uint16)
		"""
		pyrangeCount = c_uint16(0)
		pInvokeResult = self.dll.TLPMX_getVoltageRanges(self.devSession, voltageValues, byref(pyrangeCount), c_uint16(channel))
		self.__testForError(pInvokeResult)
		return  pyrangeCount.value

	def setVoltageRangeSearch(self, channel = 1):
		"""
		This function returns the actual voltage range value.
		
		Notes:
		(1) The function is only available on PM100D, PM100A, PM100USB, PM160T, PM200, PM400.
		
		
		Args:
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_setVoltageRangeSearch(self.devSession, c_uint16(channel))
		self.__testForError(pInvokeResult)

	def setVoltageRef(self, voltageReferenceValue, channel = 1):
		"""
		This function sets the voltage reference value.
		
		Notes:
		(1) The function is only available on PM100D, PM100A, PM100USB, PM160T, PM200, PM400.
		
		
		Args:
			voltageReferenceValue(double) : This parameter specifies the voltage reference value in volts [V].
			
			Remark:
			This value is used for calculating differences between the actual voltage value and this voltage reference value if Voltage Reference State is ON.
			
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_setVoltageRef(self.devSession, c_double(voltageReferenceValue), c_uint16(channel))
		self.__testForError(pInvokeResult)

	def getVoltageRef(self, attribute, channel = 1):
		"""
		This function returns the voltage reference value.
		
		Notes:
		(1) The function is only available on PM100D, PM100A, PM100USB, PM160T, PM200, PM400.
		
		
		Args:
			attribute(int16) : This parameter specifies the value to be queried.
			
			Acceptable values:
			  TLPM_ATTR_SET_VAL  (0): Set value
			  TLPM_ATTR_MIN_VAL  (1): Minimum value
			  TLPM_ATTR_MAX_VAL  (2): Maximum value
			  TLPM_ATTR_DFLT_VAL (3): Default value
			
			
			Remark:
			This value is used for calculating differences between the actual voltage value and this voltage reference value if Voltage Reference State is ON.
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			voltageReferenceValue(double) : This parameter returns the specified voltage reference value in volts [V].
		"""
		pyvoltageReferenceValue = c_double(0)
		pInvokeResult = self.dll.TLPMX_getVoltageRef(self.devSession, c_int16(attribute), byref(pyvoltageReferenceValue), c_uint16(channel))
		self.__testForError(pInvokeResult)
		return  pyvoltageReferenceValue.value

	def setVoltageRefState(self, voltageReferenceState, channel = 1):
		"""
		This function sets the voltage reference state.
		
		Notes:
		(1) The function is only available on PM100D, PM100A, PM100USB, PM160T, PM200, PM400.
		
		
		Args:
			voltageReferenceState(int16) : This parameter specifies the voltage reference state.
			
			Acceptable values:
			  TLPM_VOLTAGE_REF_OFF (0): Voltage reference disabled. Absolute measurement.
			  TLPM_VOLTAGE_REF_ON  (1): Voltage reference enabled. Relative measurement.
			
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_setVoltageRefState(self.devSession, c_int16(voltageReferenceState), c_uint16(channel))
		self.__testForError(pInvokeResult)

	def getVoltageRefState(self, channel = 1):
		"""
		This function returns the voltage reference state.
		
		Notes:
		(1) The function is only available on PM100D, PM100A, PM100USB, PM160T, PM200, PM400.
		
		
		Args:
			
			Return values:
			  TLPM_VOLTAGE_REF_OFF (0): Voltage reference disabled. Absolute measurement.
			  TLPM_VOLTAGE_REF_ON  (1): Voltage reference enabled. Relative measurement.
			
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			voltageReferenceState(int16) : This parameter returns the voltage reference state.
		"""
		pyvoltageReferenceState = c_int16(0)
		pInvokeResult = self.dll.TLPMX_getVoltageRefState(self.devSession, byref(pyvoltageReferenceState), c_uint16(channel))
		self.__testForError(pInvokeResult)
		return  pyvoltageReferenceState.value

	def setPeakThreshold(self, peakThreshold, channel = 1):
		"""
		This function sets the peak detector threshold.
		
		Remark:
		Peak detector threshold is in percent [%] of the maximum from the actual measurements range.
		
		Notes:
		(1) The function is only available on PM100D, PM100USB, PM200, PM400.
		
		
		Args:
			peakThreshold(double) : This parameter specifies the peak detector threshold.
			
			Remark:
			Peak detector threshold is in percent [%] of the maximum from the actual measurements range.
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_setPeakThreshold(self.devSession, c_double(peakThreshold), c_uint16(channel))
		self.__testForError(pInvokeResult)

	def getPeakThreshold(self, attribute, channel = 1):
		"""
		This function returns the peak detector threshold.
		
		Notes:
		(1) The function is only available on PM100D, PM100USB, PM200, PM400.
		
		
		Args:
			attribute(int16) : This parameter specifies the value to be queried.
			
			Acceptable values:
			  TLPM_ATTR_SET_VAL  (0): Set value
			  TLPM_ATTR_MIN_VAL  (1): Minimum value
			  TLPM_ATTR_MAX_VAL  (2): Maximum value
			  TLPM_ATTR_DFLT_VAL (3): Default value
			
			
			Remark:
			Peak detector threshold is in percent [%] of the maximum from the actual measurements range.
			
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			peakThreshold(double) : This parameter returns the peak detector threshold.
		"""
		pypeakThreshold = c_double(0)
		pInvokeResult = self.dll.TLPMX_getPeakThreshold(self.devSession, c_int16(attribute), byref(pypeakThreshold), c_uint16(channel))
		self.__testForError(pInvokeResult)
		return  pypeakThreshold.value

	def startPeakDetector(self, channel = 1):
		"""
		Starts peak finder. For pyro or photodiode in pulse mode.
		
		Notes:
		(1) The function is only available on PM103
		
		Args:
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_startPeakDetector(self.devSession, c_uint16(channel))
		self.__testForError(pInvokeResult)

	def isPeakDetectorRunning(self, channel = 1):
		"""
		Tests if peak finder is active at the moment. Same as polling status operation register of sensor and checking for bit 3.
		
		Notes:
		(1) The function is only available on PM103
		
		Args:
			
			VI_TRUE: peak detector is running
			VI_FALSE: peak detector is stopped.
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			isRunning(int16) : returns the running state of the peak detector.
		"""
		pyisRunning = c_int16(0)
		pInvokeResult = self.dll.TLPMX_isPeakDetectorRunning(self.devSession, byref(pyisRunning), c_uint16(channel))
		self.__testForError(pInvokeResult)
		return  pyisRunning.value

	def setPeakFilter(self, filter, channel = 1):
		"""
		
		Args:
			filter(int16) : Valid valus for this parameter are
			0 = NONE
			1 = OVER
			Use OVER if the signal measured is a rectangular signal.
			If it is a sinus or triangle signal use NONE.
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_setPeakFilter(self.devSession, c_int16(filter), c_uint16(channel))
		self.__testForError(pInvokeResult)

	def getPeakFilter(self, channel = 1):
		"""
		
		Args:
			0 = NONE
			1 = OVER
			Use OVER if the signal measured is a rectangular signal.
			If it is a sinus or triangle signal use NONE.
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			filter(int16) : Valid valus for this parameter are
		"""
		pyfilter = c_int16(0)
		pInvokeResult = self.dll.TLPMX_getPeakFilter(self.devSession, byref(pyfilter), c_uint16(channel))
		self.__testForError(pInvokeResult)
		return  pyfilter.value

	def setExtNtcParameter(self, r0Coefficient, betaCoefficient, channel = 1):
		"""
		This function sets the temperature calculation coefficients for the NTC sensor externally connected to the instrument (NTC IN).
		
		Notes:
		(1) The function is only available on PM400.
		
		
		Args:
			r0Coefficient(double) : This parameter specifies the R0 coefficient in [Ohm] for calculating the temperature from the sensor's resistance by the beta parameter equation. R0 is the NTC's resistance at T0 (25 °C = 298.15 K).
			betaCoefficient(double) : This parameter specifies the B coefficient in [K] for calculating the temperature from the sensor's resistance by the beta parameter equation.
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_setExtNtcParameter(self.devSession, c_double(r0Coefficient), c_double(betaCoefficient), c_uint16(channel))
		self.__testForError(pInvokeResult)

	def getExtNtcParameter(self, attribute, channel = 1):
		"""
		This function gets the temperature calculation coefficients for the NTC sensor externally connected to the instrument (NTC IN).
		
		Notes:
		(1) The function is only available on PM400.
		
		
		Args:
			attribute(int16) : This parameter specifies the values to be queried.
			
			Acceptable values:
			  TLPM_ATTR_SET_VAL  (0): Set value
			  TLPM_ATTR_MIN_VAL  (1): Minimum value
			  TLPM_ATTR_MAX_VAL  (2): Maximum value
			  TLPM_ATTR_DFLT_VAL (3): Default value
			
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			r0Coefficient(double) : This parameter returns the specified R0 coefficient in [Ohm].
			betaCoefficient(double) : This parameter returns the specified B coefficient in [K].
		"""
		pyr0Coefficient = c_double(0)
		pybetaCoefficient = c_double(0)
		pInvokeResult = self.dll.TLPMX_getExtNtcParameter(self.devSession, c_int16(attribute), byref(pyr0Coefficient), byref(pybetaCoefficient), c_uint16(channel))
		self.__testForError(pInvokeResult)
		return  pyr0Coefficient.value, pybetaCoefficient.value

	def setFilterPosition(self, filterPosition):
		"""
		This function sets the current filter position
		
		Notes:
		(1) The function is only available on PM160 with firmware version 1.5.4 and higher
		
		
		Args:
			filterPosition(int16) : This parameter specifies the current filter position
			
			Acceptable values:
			  VI_OFF (0): Filter position OFF. The filter value will not be used in the power calculation
			  VI_ON  (1): Filter position ON, The filter value will be used in the power correction
			
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_setFilterPosition(self.devSession, c_int16(filterPosition))
		self.__testForError(pInvokeResult)

	def getFilterPosition(self):
		"""
		This function returns the current filter position
		
		Notes:
		(1) The function is only available on PM160 with firmware version 1.5.4 and higher
		
		
		Args:
			
			Acceptable values:
			  VI_OFF (0): Filter position OFF. The filter value will not be used in the power calculation
			  VI_ON  (1): Filter position ON, The filter value will be used in the power correction
			
		Returns:
			filterPosition(int16) : This parameter returns the current filter position
		"""
		pyfilterPosition = c_int16(0)
		pInvokeResult = self.dll.TLPMX_getFilterPosition(self.devSession, byref(pyfilterPosition))
		self.__testForError(pInvokeResult)
		return  pyfilterPosition.value

	def setFilterAutoMode(self, filterAutoPositionDetection):
		"""
		This function enables / disables the automatic filter position detection
		
		Notes:
		(1) The function is only available on PM160 with firmware version 1.5.4 and higher
		
		
		Args:
			filterAutoPositionDetection(int16) : This parameter specifies if the automatic filter position detection is enabled/disabled
			
			Acceptable values:
			  VI_OFF (0): Filter position detection is OFF. The manual set fitler position is used
			  VI_ON  (1): Filter position detection is ON, The filter position will be automatically detected
			
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_setFilterAutoMode(self.devSession, c_int16(filterAutoPositionDetection))
		self.__testForError(pInvokeResult)

	def getFilterAutoMode(self):
		"""
		This function returns if the automatic filter position detection is used
		
		Notes:
		(1) The function is only available on PM160 with firmware version 1.5.4 and higher
		
		
		Args:
			
			Acceptable values:
			  VI_OFF (0): Filter position detection is OFF. The manual set fitler position is used
			  VI_ON  (1): Filter position detection is ON, The filter position will be automatically detected
			
		Returns:
			filterAutoPositionDetection(int16) : This parameter returns if the automatic filter position detection is enabled/disabled
		"""
		pyfilterAutoPositionDetection = c_int16(0)
		pInvokeResult = self.dll.TLPMX_getFilterAutoMode(self.devSession, byref(pyfilterAutoPositionDetection))
		self.__testForError(pInvokeResult)
		return  pyfilterAutoPositionDetection.value

	def getAnalogOutputSlopeRange(self, channel = 1):
		"""
		This function returns range of the responsivity in volts per watt [V/W] for the analog output.
		
		Notes:
		(1) The function is only available on PM101 and PM102
		
		
		
		Args:
			Lower voltage is clipped to the minimum.
			
			Higher voltage values are clipped to the maximum.
			
			channel(uint16) : Number of the Pin
			
			Default: 1 for non multi channel devices
		Returns:
			minSlope(double) : This parameter returns the minimum voltage in Volt [V/W] of the analog output.
			maxSlope(double) : This parameter returns the maximum voltage in Volt [V/W] of the analog output.
		"""
		pyminSlope = c_double(0)
		pymaxSlope = c_double(0)
		pInvokeResult = self.dll.TLPMX_getAnalogOutputSlopeRange(self.devSession, byref(pyminSlope), byref(pymaxSlope), c_uint16(channel))
		self.__testForError(pInvokeResult)
		return  pyminSlope.value, pymaxSlope.value

	def setAnalogOutputSlope(self, slope, channel = 1):
		"""
		This function sets the responsivity in volts per watt [V/W] for the analog output.
		
		Notes:
		(1) The function is only available on PM101 and PM102
		
		
		Args:
			slope(double) : This parameter specifies the responsivity in volts per watt [V/W].
			
			channel(uint16) : Number of the Pin
			
			Default: 1 for non multi channel devices
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_setAnalogOutputSlope(self.devSession, c_double(slope), c_uint16(channel))
		self.__testForError(pInvokeResult)

	def getAnalogOutputSlope(self, attribute, channel = 1):
		"""
		This function returns the responsivity in volts per watt [V/W] for the analog output.
		
		Notes:
		(1) The function is only available on PM101 and PM102
		
		
		
		Args:
			attribute(int16) : This parameter specifies the value to be queried.
			
			Acceptable values:
			  TLPM_ATTR_SET_VAL  (0): Set value
			  TLPM_ATTR_MIN_VAL  (1): Minimum value
			  TLPM_ATTR_MAX_VAL  (2): Maximum value
			  TLPM_ATTR_DFLT_VAL (3): Default value
			
			
			channel(uint16) : Number of the Pin
			
			Default: 1 for non multi channel devices
		Returns:
			slope(double) : This parameter returns the specified responsivity in volts per watt [V/W].
		"""
		pyslope = c_double(0)
		pInvokeResult = self.dll.TLPMX_getAnalogOutputSlope(self.devSession, c_int16(attribute), byref(pyslope), c_uint16(channel))
		self.__testForError(pInvokeResult)
		return  pyslope.value

	def getAnalogOutputVoltageRange(self, channel = 1):
		"""
		This function returns the range in Volt [V] of the analog output.
		
		Notes:
		(1) The function is only available on PM101 and PM102
		
		
		
		Args:
			Lower voltage is clipped to the minimum.
			
			Higher voltage values are clipped to the maximum.
			
			channel(uint16) : Number of the Pin
			
			Default: 1 for non multi channel devices
		Returns:
			minVoltage(double) : This parameter returns the minimum voltage in Volt [V] of the analog output.
			maxVoltage(double) : This parameter returns the maximum voltage in Volt [V] of the analog output.
		"""
		pyminVoltage = c_double(0)
		pymaxVoltage = c_double(0)
		pInvokeResult = self.dll.TLPMX_getAnalogOutputVoltageRange(self.devSession, byref(pyminVoltage), byref(pymaxVoltage), c_uint16(channel))
		self.__testForError(pInvokeResult)
		return  pyminVoltage.value, pymaxVoltage.value

	def getAnalogOutputVoltage(self, attribute, channel = 1):
		"""
		This function returns the analog output in Volt [V].
		
		Notes:
		(1) The function is only available on PM101 and PM102
		
		
		
		Args:
			attribute(int16) : This parameter specifies the value to be queried.
			
			Acceptable values:
			  TLPM_ATTR_SET_VAL  (0): Set value
			  TLPM_ATTR_MIN_VAL  (1): Minimum value
			  TLPM_ATTR_MAX_VAL  (2): Maximum value
			  TLPM_ATTR_DFLT_VAL (3): Default value
			
			
			channel(uint16) : Number of the Pin
			
			Default: 1 for non multi channel devices
		Returns:
			voltage(double) : This parameter returns the analog output in Volt [V].
		"""
		pyvoltage = c_double(0)
		pInvokeResult = self.dll.TLPMX_getAnalogOutputVoltage(self.devSession, c_int16(attribute), byref(pyvoltage), c_uint16(channel))
		self.__testForError(pInvokeResult)
		return  pyvoltage.value

	def getAnalogOutputGainRange(self, channel = 1):
		"""
		This function returns the analog output hub in Volt [V].
		
		Notes:
		(1) The function is only available on PM103
		
		
		
		Args:
			channel(uint16) : Number of the Pin
			
			Default: 1 for non multi channel devices
		Returns:
			gainRangeIndex(int16)
		"""
		pygainRangeIndex = c_int16(0)
		pInvokeResult = self.dll.TLPMX_getAnalogOutputGainRange(self.devSession, byref(pygainRangeIndex), c_uint16(channel))
		self.__testForError(pInvokeResult)
		return  pygainRangeIndex.value

	def setAnalogOutputGainRange(self, gainRangeIndex, channel = 1):
		"""
		This function returns the analog output hub in Volt [V].
		
		Notes:
		(1) The function is only available on PM103
		
		
		
		Args:
			gainRangeIndex(int16)
			channel(uint16) : Number of the Pin
			
			Default: 1 for non multi channel devices
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_setAnalogOutputGainRange(self.devSession, c_int16(gainRangeIndex), c_uint16(channel))
		self.__testForError(pInvokeResult)

	def getAnalogOutputRoute(self, channel = 1):
		"""
		This function returns the analog output hub in Volt [V].
		
		Notes:
		(1) The function is only available on PM103
		
		
		
		Args:
			channel(uint16) : Number of the Pin
			
			Default: 1 for non multi channel devices
		Returns:
			routeName(string)
		"""
		pyrouteName = create_string_buffer(1024)
		pInvokeResult = self.dll.TLPMX_getAnalogOutputRoute(self.devSession, pyrouteName, c_uint16(channel))
		self.__testForError(pInvokeResult)
		return c_char_p(pyrouteName.raw).value

	def setAnalogOutputRoute(self, routeStrategy, channel = 1):
		"""
		This function returns the analog output hub in Volt [V].
		
		Notes:
		(1) The function is only available on PM103
		
		
		
		Args:
			routeStrategy(uint16) : TLPM_ANALOG_ROUTE_PUR  (0)  (Direct Route): The raw amplified signal is output. This signal is related to the photo current or voltage. It is not wavelength or zero compensated.
			TLPM_ANALOG_ROUTE_CBA  (1)  (Compensated Base Unit): The raw amplified signal is multiplied with a correction factor in hardware to compensate the dark current/voltage. The signal is the photo current or voltage and is not wavelength compensated.
			TLPM_ANALOG_ROUTE_CMA  (2) (Compensated Main Unit): The raw amplified signal is multiplied with a correction factor in hardware to output a analogue voltage related to power or energy. The signal is zero and wavelength compensated.
			channel(uint16) : Number of the Pin
			
			Default: 1 for non multi channel devices
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_setAnalogOutputRoute(self.devSession, c_uint16(routeStrategy), c_uint16(channel))
		self.__testForError(pInvokeResult)

	def getPositionAnalogOutputSlopeRange(self, channel = 1):
		"""
		This function returns range of the responsivity in volts per µm [V/µm] for the analog output.
		
		Notes:
		(1) The function is only available on PM102
		
		
		
		Args:
			
			
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			minSlope(double) : This parameter returns the minimum slope in [V/µm] of the analog output.
			maxSlope(double) : This parameter returns the maximum slope in [V/µm] of the analog output.
		"""
		pyminSlope = c_double(0)
		pymaxSlope = c_double(0)
		pInvokeResult = self.dll.TLPMX_getPositionAnalogOutputSlopeRange(self.devSession, byref(pyminSlope), byref(pymaxSlope), c_uint16(channel))
		self.__testForError(pInvokeResult)
		return  pyminSlope.value, pymaxSlope.value

	def setPositionAnalogOutputSlope(self, slope, channel = 1):
		"""
		This function sets the responsivity in volts per µm [V/µm] for the analog output.
		
		Notes:
		(1) The function is only available on PM102
		
		
		Args:
			slope(double) : This parameter specifies the responsivity in volts per µm [V/µm] for the AO2 and AO3 channel 
			
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_setPositionAnalogOutputSlope(self.devSession, c_double(slope), c_uint16(channel))
		self.__testForError(pInvokeResult)

	def getPositionAnalogOutputSlope(self, attribute, channel = 1):
		"""
		This function returns the responsivity in volts per µm [V/µm] for the analog output channels.
		
		Notes:
		(1) The function is only available on PM102
		
		
		
		Args:
			attribute(int16) : This parameter specifies the value to be queried.
			
			Acceptable values:
			  TLPM_ATTR_SET_VAL  (0): Set value
			  TLPM_ATTR_MIN_VAL  (1): Minimum value
			  TLPM_ATTR_MAX_VAL  (2): Maximum value
			  TLPM_ATTR_DFLT_VAL (3): Default value
			
			
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			slope(double) : This parameter returns the specified responsivity in volts per µm [V/µm] for the AO2 and AO3 channel 
		"""
		pyslope = c_double(0)
		pInvokeResult = self.dll.TLPMX_getPositionAnalogOutputSlope(self.devSession, c_int16(attribute), byref(pyslope), c_uint16(channel))
		self.__testForError(pInvokeResult)
		return  pyslope.value

	def getPositionAnalogOutputVoltageRange(self, channel = 1):
		"""
		This function returns the range in Volt [V] of the analog output.
		
		Notes:
		(1) The function is only available on PM102
		
		
		
		Args:
			Lower voltage is clipped to the minimum.
			
			Higher voltage values are clipped to the maximum.
			
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			minVoltage(double) : This parameter returns the minimum voltage in Volt [V] of the analog output.
			maxVoltage(double) : This parameter returns the maximum voltage in Volt [V] of the analog output.
		"""
		pyminVoltage = c_double(0)
		pymaxVoltage = c_double(0)
		pInvokeResult = self.dll.TLPMX_getPositionAnalogOutputVoltageRange(self.devSession, byref(pyminVoltage), byref(pymaxVoltage), c_uint16(channel))
		self.__testForError(pInvokeResult)
		return  pyminVoltage.value, pymaxVoltage.value

	def getPositionAnalogOutputVoltage(self, attribute, channel = 1):
		"""
		This function returns the analog output in Volt [V].
		
		Notes:
		(1) The function is only available on PM102
		
		
		
		Args:
			attribute(int16) : This parameter specifies the value to be queried.
			
			Acceptable values:
			  TLPM_ATTR_SET_VAL  (0): Set value
			  TLPM_ATTR_MIN_VAL  (1): Minimum value
			  TLPM_ATTR_MAX_VAL  (2): Maximum value
			  TLPM_ATTR_DFLT_VAL (3): Default value
			
			
			
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			voltageX(double) : This parameter returns the analog output in Volt [V] for the AO2 channel ( x direction)
			voltageY(double) : This parameter returns the analog output in Volt [V] for the AO3 channel ( y direction)
		"""
		pyvoltageX = c_double(0)
		pyvoltageY = c_double(0)
		pInvokeResult = self.dll.TLPMX_getPositionAnalogOutputVoltage(self.devSession, c_int16(attribute), byref(pyvoltageX), byref(pyvoltageY), c_uint16(channel))
		self.__testForError(pInvokeResult)
		return  pyvoltageX.value, pyvoltageY.value

	def getMeasPinMode(self, channel = 1):
		"""
		This function returns the meas pin state
		
		Notes:
		(1) The function is only available on PM103
		
		
		
		Args:
			
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			state(int16) : This parameter returns the analog output hub in Volt [V].
		"""
		pystate = c_int16(0)
		pInvokeResult = self.dll.TLPMX_getMeasPinMode(self.devSession, byref(pystate), c_uint16(channel))
		self.__testForError(pInvokeResult)
		return  pystate.value

	def getMeasPinPowerLevel(self, channel = 1):
		"""
		This function returns the meas pin power level in [W]
		
		Notes:
		(1) The function is only available on PM103
		
		
		
		Args:
			
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			level(double) : This parameter returns the measure pin output power level in Watt [W].
		"""
		pylevel = c_double(0)
		pInvokeResult = self.dll.TLPMX_getMeasPinPowerLevel(self.devSession, byref(pylevel), c_uint16(channel))
		self.__testForError(pInvokeResult)
		return  pylevel.value

	def setMeasPinPowerLevel(self, level, channel = 1):
		"""
		This function returns the meas pin state
		
		Notes:
		(1) The function is only available on PM103
		
		
		
		Args:
			level(double) : This parameter sets the measure pin output power level in Watt [W].
			
			
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_setMeasPinPowerLevel(self.devSession, c_double(level), c_uint16(channel))
		self.__testForError(pInvokeResult)

	def getMeasPinEnergyLevel(self, channel = 1):
		"""
		This function returns the meas pin energy level in [J]
		
		Notes:
		(1) The function is only available on PM103
		
		
		
		Args:
			
			
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			level(double) : This parameter returns the measure pin output energy level in  [J].
		"""
		pylevel = c_double(0)
		pInvokeResult = self.dll.TLPMX_getMeasPinEnergyLevel(self.devSession, byref(pylevel), c_uint16(channel))
		self.__testForError(pInvokeResult)
		return  pylevel.value

	def setMeasPinEnergyLevel(self, level, channel = 1):
		"""
		This function returns the meas pin state
		
		Notes:
		(1) The function is only available on PM103
		
		
		
		Args:
			level(double) : This parameter returns the measurement pin energy level in [J].
			
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_setMeasPinEnergyLevel(self.devSession, c_double(level), c_uint16(channel))
		self.__testForError(pInvokeResult)

	def setNegativePulseWidth(self, pulseDuration, channel = 1):
		"""
		This function sets the low pulse duration in Seconds
		
		Notes:
		(1) The function is only available on PM103
		
		
		Args:
			pulseDuration(double) : low pulse duration in Seconds
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_setNegativePulseWidth(self.devSession, c_double(pulseDuration), c_uint16(channel))
		self.__testForError(pInvokeResult)

	def setPositivePulseWidth(self, pulseDuration, channel = 1):
		"""
		This function sets the high pulse duration in Seconds
		
		Notes:
		(1) The function is only available on PM103
		
		
		Args:
			pulseDuration(double) : high pulse duration in Seconds
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_setPositivePulseWidth(self.devSession, c_double(pulseDuration), c_uint16(channel))
		self.__testForError(pInvokeResult)

	def setNegativeDutyCycle(self, dutyCycle, channel = 1):
		"""
		This function sets the low duty cycle in Percent
		
		Notes:
		(1) The function is only available on PM103
		
		
		Args:
			dutyCycle(double) : low pulse duty cycle in Percent
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_setNegativeDutyCycle(self.devSession, c_double(dutyCycle), c_uint16(channel))
		self.__testForError(pInvokeResult)

	def setPositiveDutyCycle(self, dutyCycle, channel = 1):
		"""
		This function sets the high duty cycle in Percent
		
		Notes:
		(1) The function is only available on PM103
		
		
		Args:
			dutyCycle(double) : high pulse duty cycle in Percent
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_setPositiveDutyCycle(self.devSession, c_double(dutyCycle), c_uint16(channel))
		self.__testForError(pInvokeResult)

	def measCurrent(self, channel = 1):
		"""
		This function is used to obtain current readings from the instrument. 
		
		Remark:
		This function starts a new measurement cycle and after finishing measurement the result is received. Subject to the actual Average Count this may take up to seconds. Refer to <Set/Get Average Count>. 
		
		Notes:
		(1) The function is only available on PM100D, PM100A, PM100USB, PM160, PM200, PM400.
		
		
		Args:
			
			Remark:
			This function starts a new measurement cycle and after finishing measurement the result is received. Subject to the actual Average Count this may take up to seconds. Refer to <Set/Get Average Count>. 
			
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			current(double) : This parameter returns the current in amperes [A].
		"""
		pycurrent = c_double(0)
		pInvokeResult = self.dll.TLPMX_measCurrent(self.devSession, byref(pycurrent), c_uint16(channel))
		self.__testForError(pInvokeResult)
		return  pycurrent.value

	def measVoltage(self, channel = 1):
		"""
		This function is used to obtain voltage readings from the instrument. 
		
		Remark:
		This function starts a new measurement cycle and after finishing measurement the result is received. Subject to the actual Average Count this may take up to seconds. Refer to <Set/Get Average Count>. 
		
		Notes:
		(1) The function is only available on PM100D, PM100A, PM100USB, PM160T, PM200, PM400.
		
		
		Args:
			
			Remark:
			This function starts a new measurement cycle and after finishing measurement the result is received. Subject to the actual Average Count this may take up to seconds. Refer to <Set/Get Average Count>. 
			
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			voltage(double) : This parameter returns the voltage in volts [V].
		"""
		pyvoltage = c_double(0)
		pInvokeResult = self.dll.TLPMX_measVoltage(self.devSession, byref(pyvoltage), c_uint16(channel))
		self.__testForError(pInvokeResult)
		return  pyvoltage.value

	def measPower(self, channel = 1):
		"""
		This function is used to obtain power readings from the instrument. 
		
		Remark:
		This function starts a new measurement cycle and after finishing measurement the result is received. Subject to the actual Average Count this may take up to seconds. Refer to <Set/Get Average Count>. 
		
		Args:
			
			Remark:
			(1) This function starts a new measurement cycle and after finishing measurement the result is received. Subject to the actual Average Count this may take up to seconds. Refer to <Set/Get Average Count>. 
			(2) Select the unit with <Set Power Unit>.
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			power(double) : This parameter returns the power in the selected unit.
		"""
		pypower = c_double(0)
		pInvokeResult = self.dll.TLPMX_measPower(self.devSession, byref(pypower), c_uint16(channel))
		self.__testForError(pInvokeResult)
		return  pypower.value

	def measEnergy(self, channel = 1):
		"""
		This function is used to obtain energy readings from the instrument. 
		
		Notes:
		(1) The function is only available on PM100D, PM100USB, PM200, PM400.
		
		
		Args:
			
			Remark:
			This function starts a new measurement cycle and after finishing measurement the result is received. Subject to the actual Average Count this may take up to seconds. Refer to <Set/Get Average Count>. 
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			energy(double) : This parameter returns the actual measured energy value in joule [J].
		"""
		pyenergy = c_double(0)
		pInvokeResult = self.dll.TLPMX_measEnergy(self.devSession, byref(pyenergy), c_uint16(channel))
		self.__testForError(pInvokeResult)
		return  pyenergy.value

	def measFreq(self, channel = 1):
		"""
		This function is used to obtain frequency readings from the instrument. 
		
		Notes:
		(1) The function is only available on PM100D, PM100A, PM100USB, PM200, PM400.
		
		
		Args:
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			frequency(double) : This parameter returns the actual measured frequency of the input signal. 
		"""
		pyfrequency = c_double(0)
		pInvokeResult = self.dll.TLPMX_measFreq(self.devSession, byref(pyfrequency), c_uint16(channel))
		self.__testForError(pInvokeResult)
		return  pyfrequency.value

	def measPowerDens(self, channel = 1):
		"""
		This function is used to obtain power density readings from the instrument. 
		
		Notes:
		(1) The function is only available on PM100D, PM100A, PM100USB, PM200, PM400.
		
		
		Args:
			
			Remark:
			This function starts a new measurement cycle and after finishing measurement the result is received. Subject to the actual Average Count this may take up to seconds. Refer to <Set/Get Average Count>.
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			powerDensity(double) : This parameter returns the actual measured power density in watt per square centimeter [W/cm²].
		"""
		pypowerDensity = c_double(0)
		pInvokeResult = self.dll.TLPMX_measPowerDens(self.devSession, byref(pypowerDensity), c_uint16(channel))
		self.__testForError(pInvokeResult)
		return  pypowerDensity.value

	def measEnergyDens(self, channel = 1):
		"""
		This function is used to obtain energy density readings from the instrument. 
		
		Notes:
		(1) The function is only available on PM100D, PM100USB, PM200, PM400.
		
		
		Args:
			
			Remark:
			This function starts a new measurement cycle and after finishing measurement the result is received. Subject to the actual Average Count this may take up to seconds. Refer to <Set/Get Average Count>.
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			energyDensity(double) : This parameter returns the actual measured energy in joule per square centimeter [J/cm²].
		"""
		pyenergyDensity = c_double(0)
		pInvokeResult = self.dll.TLPMX_measEnergyDens(self.devSession, byref(pyenergyDensity), c_uint16(channel))
		self.__testForError(pInvokeResult)
		return  pyenergyDensity.value

	def measDualChannelSimultaneous(self, measurement):
		"""
		This function is used to obtain frequency readings from the instrument. 
		
		Notes:
		(1) The function is only available on PM100D, PM100A, PM100USB, PM200, PM400.
		
		
		Args:
			measurement(uint16)
		Returns:
			resultChannel1(double) : This parameter returns the actual measured frequency of the input signal. 
			resultChannel2(double) : This parameter returns the actual measured frequency of the input signal. 
		"""
		pyresultChannel1 = c_double(0)
		pyresultChannel2 = c_double(0)
		pInvokeResult = self.dll.TLPMX_measDualChannelSimultaneous(self.devSession, c_uint16(measurement), byref(pyresultChannel1), byref(pyresultChannel2))
		self.__testForError(pInvokeResult)
		return  pyresultChannel1.value, pyresultChannel2.value

	def measAuxAD0(self, channel = 1):
		"""
		This function is used to obtain voltage readings from the instrument's auxiliary AD0 input. 
		
		Notes:
		(1) The function is only available on PM200, PM400.
		
		
		Args:
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			voltage(double) : This parameter returns the voltage in volt.
		"""
		pyvoltage = c_double(0)
		pInvokeResult = self.dll.TLPMX_measAuxAD0(self.devSession, byref(pyvoltage), c_uint16(channel))
		self.__testForError(pInvokeResult)
		return  pyvoltage.value

	def measAuxAD1(self, channel = 1):
		"""
		This function is used to obtain voltage readings from the instrument's auxiliary AD1 input. 
		
		Notes:
		(1) The function is only available on PM200, PM400.
		
		
		Args:
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			voltage(double) : This parameter returns the voltage in volt.
		"""
		pyvoltage = c_double(0)
		pInvokeResult = self.dll.TLPMX_measAuxAD1(self.devSession, byref(pyvoltage), c_uint16(channel))
		self.__testForError(pInvokeResult)
		return  pyvoltage.value

	def measEmmHumidity(self, channel = 1):
		"""
		This function is used to obtain relative humidity readings from the Environment Monitor Module (EMM) connected to the instrument. 
		
		Notes:
		(1) The function is only available on PM200, PM400.
		(2) The function will return an error when no EMM is connected.
		
		Args:
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			humidity(double) : This parameter returns the relative humidity in %.
		"""
		pyhumidity = c_double(0)
		pInvokeResult = self.dll.TLPMX_measEmmHumidity(self.devSession, byref(pyhumidity), c_uint16(channel))
		self.__testForError(pInvokeResult)
		return  pyhumidity.value

	def measEmmTemperature(self, channel = 1):
		"""
		This function is used to obtain temperature readings from the Environment Monitor Module (EMM) connected to the instrument. 
		
		Notes:
		(1) The function is only available on PM200, PM400.
		(2) The function will return an error when no EMM is connected.
		
		Args:
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			temperature(double) : This parameter returns the temperature in °C
		"""
		pytemperature = c_double(0)
		pInvokeResult = self.dll.TLPMX_measEmmTemperature(self.devSession, byref(pytemperature), c_uint16(channel))
		self.__testForError(pInvokeResult)
		return  pytemperature.value

	def measExtNtcTemperature(self, channel = 1):
		"""
		This function gets temperature readings from the external thermistor sensor connected to the instrument (NTC IN). 
		
		Notes:
		(1) The function is only available on PM400.
		(2) The function will return an error when no external sensor is connected.
		
		
		Args:
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			temperature(double) : This parameter returns the temperature in °C
		"""
		pytemperature = c_double(0)
		pInvokeResult = self.dll.TLPMX_measExtNtcTemperature(self.devSession, byref(pytemperature), c_uint16(channel))
		self.__testForError(pInvokeResult)
		return  pytemperature.value

	def measExtNtcResistance(self, channel = 1):
		"""
		This function gets resistance readings from the external thermistor sensor connected to the instrument (NTC IN). 
		
		Notes:
		(1) The function is only available on PM400.
		(2) The function will return an error when no external sensor is connected.
		
		
		Args:
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			resistance(double) : This parameter returns the resistance in Ohm
		"""
		pyresistance = c_double(0)
		pInvokeResult = self.dll.TLPMX_measExtNtcResistance(self.devSession, byref(pyresistance), c_uint16(channel))
		self.__testForError(pInvokeResult)
		return  pyresistance.value

	def measHeadResistance(self, channel = 1):
		"""
		This function is used to obtain frequency readings from the instrument. 
		
		Notes:
		(1) The function is only available on PM100D, PM100A, PM100USB, PM200, PM400.
		
		
		Args:
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			frequency(double) : This parameter returns the resistance in Ohm
		"""
		pyfrequency = c_double(0)
		pInvokeResult = self.dll.TLPMX_measHeadResistance(self.devSession, byref(pyfrequency), c_uint16(channel))
		self.__testForError(pInvokeResult)
		return  pyfrequency.value

	def measHeadTemperature(self, channel = 1):
		"""
		This function is used to obtain frequency readings from the instrument. 
		
		Notes:
		(1) The function is only available on PM100D, PM100A, PM100USB, PM200, PM400.
		
		
		Args:
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			frequency(double) : This parameter returns the temperature in °C
		"""
		pyfrequency = c_double(0)
		pInvokeResult = self.dll.TLPMX_measHeadTemperature(self.devSession, byref(pyfrequency), c_uint16(channel))
		self.__testForError(pInvokeResult)
		return  pyfrequency.value

	def meas4QPositions(self, channel = 1):
		"""
		This function returns the x and position of a 4q sensor
		
		Notes:
		(1) The function is only available on PM101, PM102, PM400.
		
		
		Args:
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			xPosition(double) : This parameter returns the actual measured x position in µm
			yPosition(double) : This parameter returns the actual measured y position in µm
		"""
		pyxPosition = c_double(0)
		pyyPosition = c_double(0)
		pInvokeResult = self.dll.TLPMX_meas4QPositions(self.devSession, byref(pyxPosition), byref(pyyPosition), c_uint16(channel))
		self.__testForError(pInvokeResult)
		return  pyxPosition.value, pyyPosition.value

	def meas4QVoltages(self, channel = 1):
		"""
		This function returns the voltage of each sector of a 4q sensor
		
		Notes:
		(1) The function is only available on PM101, PM102, PM400.
		
		
		Args:
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			voltage1(double) : This parameter returns the actual measured voltage of the upper left sector of a 4q sensor.
			voltage2(double)
			voltage3(double)
			voltage4(double)
		"""
		pyvoltage1 = c_double(0)
		pyvoltage2 = c_double(0)
		pyvoltage3 = c_double(0)
		pyvoltage4 = c_double(0)
		pInvokeResult = self.dll.TLPMX_meas4QVoltages(self.devSession, byref(pyvoltage1), byref(pyvoltage2), byref(pyvoltage3), byref(pyvoltage4), c_uint16(channel))
		self.__testForError(pInvokeResult)
		return  pyvoltage1.value, pyvoltage2.value, pyvoltage3.value, pyvoltage4.value

	def measNegPulseWidth(self, channel = 1):
		"""
		This function returns the negative pulse width in µsec.
		Notes:
		(1) The function is only available on PM103.
		
		
		Args:
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			negativePulseWidth(double) : Negative Pulse Width in µsec.
		"""
		pynegativePulseWidth = c_double(0)
		pInvokeResult = self.dll.TLPMX_measNegPulseWidth(self.devSession, byref(pynegativePulseWidth), c_uint16(channel))
		self.__testForError(pInvokeResult)
		return  pynegativePulseWidth.value

	def measPosPulseWidth(self, channel = 1):
		"""
		This function returns the positive pulse width in µsec.
		Notes:
		(1) The function is only available on PM103.
		
		
		Args:
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			positivePulseWidth(double) : Positive Pulse Width in µsec.
		"""
		pypositivePulseWidth = c_double(0)
		pInvokeResult = self.dll.TLPMX_measPosPulseWidth(self.devSession, byref(pypositivePulseWidth), c_uint16(channel))
		self.__testForError(pInvokeResult)
		return  pypositivePulseWidth.value

	def measNegDutyCycle(self, channel = 1):
		"""
		This function returns the negative duty cycle in percentage.
		Notes:
		(1) The function is only available on PM103.
		
		
		Args:
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			negativeDutyCycle(double) : Negative Duty Cycle in percentage.
		"""
		pynegativeDutyCycle = c_double(0)
		pInvokeResult = self.dll.TLPMX_measNegDutyCycle(self.devSession, byref(pynegativeDutyCycle), c_uint16(channel))
		self.__testForError(pInvokeResult)
		return  pynegativeDutyCycle.value

	def measPosDutyCycle(self, channel = 1):
		"""
		This function returns the positive duty cycle in percentage.
		Notes:
		(1) The function is only available on PM103.
		
		
		Args:
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			positiveDutyCycle(double) : Positive Duty Cycle in percentage.
		"""
		pypositiveDutyCycle = c_double(0)
		pInvokeResult = self.dll.TLPMX_measPosDutyCycle(self.devSession, byref(pypositiveDutyCycle), c_uint16(channel))
		self.__testForError(pInvokeResult)
		return  pypositiveDutyCycle.value

	def measPowerMeasurementSequence(self, baseTime, channel = 1):
		"""
		This function send the SCPI Command "MEAS:ARR" to the device.
		To receive the measurement data, call "getMeasurementSequence".
		
		PM101, PM400:
		Starts a software triggered power measurement sequence. The array mode always stores 10000 power samples in Watt or dBm with 10 kHz in an internal buffer. So max time resolution between the samples is 100 us. Once the buffer is full the command will return the first sample. During the measurement the remote interface will block and can not process any further SCPI requests. To query the rest of samples continue to call FETC? with an index. Alternatively call FETC:ARR? multiple times afterwards. This SCPI command is a convenience function that includes the SCPI command sequence ABOR, MEAS:ARR:CURR?, INIT and finally FETC:ARR?. Ensure the product of BaseTime / 100 * samples is always smaller or equal 10000. Normally it makes sense to disable bandwidth limitation for this measurement mode DIAG#:INP:PDI:BWID. SENS#:AVER is not applied for array mode. Also relative power measurements (See SENS#:POW:REF) are not supported in array mode.
		
		PM103:
		This software triggered scope mode is only available for photodiode power sensors in CW mode. For checking measure mode of photodiode use command SENS#:FREQ:MODE?. The scope mode stores 10k power samples in Watt with given averaging at max 100 kHz in an internal buffer. So max time resolution between the samples is 10 us. With the internal sample buffer of 10000 will end up in a capture time of 100 ms with highest resolution. For example, setting an averaging of 2 will give 200 ms capture time. Once the buffer is full the command will return the first 100 samples as binary tuples. To query the rest of samples call FETC:ARR? multiple times afterwards. Please read this FETC:ARR? for data format description. This SCPI command is a convenience function that includes the SCPI command sequence ABOR#, CONF#:ARR, INIT# and finally FETC:ARR?. If you want to use a hardware trigger to horizontal lock the signal use MEAS#:ARR:HWT?.
		
		PM5020, PM6x:
		This software triggered scope mode is only available for thermal and photodiode power sensors in CW mode. For checking measure mode of photodiode use command SENS#:FREQ:MODE?. The scope mode stores 10k samples with given averaging at max 100 kHz in an internal buffer. So max time resolution between the samples is 10 us. With the internal sample buffer of 10000 will end up in a capture time of 100 ms with highest resolution. For example, setting an averaging of 2 will give 200 ms capture time. The function will configure all channels that are connected and in a valid mode for power scope measurement. If none of the channels support this mode an error will be issued. Once the buffer is full the command will return the first 100 samples as binary triples. To query the rest of samples call FETC:ARR? multiple times afterwards. Please read this FETC:ARR? for data format description. This SCPI command is a convenience function that includes the SCPI command sequence ABOR#, CONF#:ARR:CHA, CONF:ARR, INIT# and finally FETC:ARR?. If you want to use a hardware trigger to horizontal lock the signal use MEAS#:ARR:HWT?.
		
		Note: The function is only available on PM101, PM400, PM103x, PM6x and PM5020.
		
		
		Args:
			baseTime(uint32) : interval between two measurements in the array in µsec.
			The maximum resolution is defined in the device specifications.
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_measPowerMeasurementSequence(self.devSession, c_uint32(baseTime), c_uint16(channel))
		self.__testForError(pInvokeResult)

	def measPowerMeasurementSequenceHWTrigger(self, baseTime, hPos, channel = 1):
		"""
		This function send the SCPI Command "MEAS:ARR:HWT" to the device.
		To receive the measurement data, call "getMeasurementSequence".
		
		PM103:
		This function send the SCPI Command "CONF:ARR:HWTrig:POW" to the device.
		Then is possible to call the methods 'startMeasurementSequence' and  'getMeasurementSequenceHWTrigger' to get the power data.
		 
		Set the bandwidth to high (setInputFilterState to OFF) and disable auto ranging (setPowerAutoRange to OFF)
		
		
		Note: The function is only available on PM5020, PM103x, PM6x.
		
		
		Args:
			baseTime(uint32) : PM103:
			interval between two measurements in the array in µsec. The maximum resolution is defined in the device specifications..
			
			PM101 special:
			time to collect measurements.
			hPos(uint32) : PM103:
			Sets the horizontal position of trigger condition in the scope catpure (Between 1 and 9999)
			
			PM101 special:
			Interval between measurements.
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_measPowerMeasurementSequenceHWTrigger(self.devSession, c_uint32(baseTime), c_uint32(hPos), c_uint16(channel))
		self.__testForError(pInvokeResult)

	def measureCurrentMeasurementSequence(self, baseTime, channel = 1):
		"""
		This function send the SCPI Command "MEAS:ARR:CURR" to the device.
		Then is possible to call the method 'getMeasurementSequence' to get the power data.
		 
		Duration of measurement in µsec = Count* Interval
		The maximum capture time is 1 sec regardless of the used interval
		
		Set the bandwidth to high(setInputFilterState to OFF) and disable auto ranging(setPowerAutoRange to OFF)
		
		Note: The function is only available on PM103, PM6x and PM5020.
		
		
		Args:
			baseTime(uint32) : interval between two measurements in the array in µsec.
			The maximum resolution is defined in the device specifications.
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_measureCurrentMeasurementSequence(self.devSession, c_uint32(baseTime), c_uint16(channel))
		self.__testForError(pInvokeResult)

	def measureCurrentMeasurementSequenceHWTrigger(self, baseTime, hPos, channel = 1):
		"""
		This function send the SCPI Command "MEAS:ARR:HWTrig:CURR" to the device.
		Then is possible to call the method 'getMeasurementSequenceHWTrigger' to get the current data.
		 
		Set the bandwidth to high (setInputFilterState to OFF) and disable auto ranging ( setPowerAutoRange to OFF)
		
		
		Note: The function is only available on PM103, PM6x and PM5020.
		
		
		Args:
			baseTime(uint32) : PM103:
			interval between two measurements in the array in µsec. The maximum resolution is defined in the device specifications.
			
			PM101 special:
			time to collect measurements.
			hPos(uint32) : PM103:
			Sets the horizontal position of trigger condition in the scope catpure (Between 1 and 9999)
			
			PM101 special:
			Interval between measurements.
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_measureCurrentMeasurementSequenceHWTrigger(self.devSession, c_uint32(baseTime), c_uint32(hPos), c_uint16(channel))
		self.__testForError(pInvokeResult)

	def measureVoltageMeasurementSequence(self, baseTime, channel = 1):
		"""
		This function send the SCPI Command "MEAS:ARR:VOLT" to the device.
		Then is possible to call the method 'getMeasurementSequence' to get the power data.
		 
		Duration of measurement in µsec = Count* Interval
		The maximum capture time is 1 sec regardless of the used interval
		
		Set the bandwidth to high(setInputFilterState to OFF) and disable auto ranging(setPowerAutoRange to OFF)
		
		Note: The function is only available on PM5020.
		
		
		Args:
			baseTime(uint32) : interval between two measurements in the array in µsec.
			The maximum resolution is defined in the device specifications.
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_measureVoltageMeasurementSequence(self.devSession, c_uint32(baseTime), c_uint16(channel))
		self.__testForError(pInvokeResult)

	def measureVoltageMeasurementSequenceHWTrigger(self, baseTime, hPos, channel = 1):
		"""
		This function send the SCPI Command "MEAS:ARR:HWTrig:VOLT" to the device.
		Then is possible to call the method 'getMeasurementSequenceHWTrigger' to get the current data.
		 
		Set the bandwidth to high (setInputFilterState to OFF) and disable auto ranging ( setPowerAutoRange to OFF)
		
		Note: The function is only available on PM5020.
		
		
		Args:
			baseTime(uint32) : PM103:
			interval between two measurements in the array in µsec. The maximum resolution is defined in the device specifications.
			
			PM101 special:
			time to collect measurements.
			hPos(uint32) : PM103:
			Sets the horizontal position of trigger condition in the scope catpure (Between 1 and 9999)
			
			PM101 special:
			Interval between measurements.
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_measureVoltageMeasurementSequenceHWTrigger(self.devSession, c_uint32(baseTime), c_uint32(hPos), c_uint16(channel))
		self.__testForError(pInvokeResult)

	def getFetchState(self, channel = 1):
		"""
		This function can be used to get the measurement state information before doing a fetch.
		
		Notes:
		(1) The function is only available on PM103, PM5020.
		
		
		Args:
			
			VI_FALSE = no new measurement is ready
			VI_TRUE  = a new measurement is ready and can be get by "FETCH#?" ( replace # with the number of the channel)
			
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			state(int16) : This parameter returns the fetch state
		"""
		pystate = c_int16(0)
		pInvokeResult = self.dll.TLPMX_getFetchState(self.devSession, byref(pystate), c_uint16(channel))
		self.__testForError(pInvokeResult)
		return  pystate.value

	def blockFetch(self, timeout, channel = 1):
		"""
		Blocks defined time until previously initiated measurement is complete and returns result finally.
		Same as FETC#? but waits for result only defined of time. In case of timeout the function return 0. Otherwise recent measurement result is returned. In case of timeout you might want to call ABOR# to discard the measurement. 
		
		Notes:
		(1) The function is only available on PM103, PM5020.
		
		
		Args:
			timeout(uint32) :  time in ms to wait for data to be fetched.
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			result(double) :  measurement result. May be 0 for timeout, INFINITY or -INFINITY if signal out of measurement range.
		"""
		pyresult = c_double(0)
		pInvokeResult = self.dll.TLPMX_blockFetch(self.devSession, c_uint32(timeout), byref(pyresult), c_uint16(channel))
		self.__testForError(pInvokeResult)
		return  pyresult.value

	def resetFastArrayMeasurement(self, channel = 1):
		"""
		This function resets the array measurement.
		
		Note: The function is only available on PM103, PM5020.
		
		
		Args:
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_resetFastArrayMeasurement(self.devSession, c_uint16(channel))
		self.__testForError(pInvokeResult)

	def confFastArrayMeasurement(self, measurement, channel = 1):
		"""
		This function is used to conffiure the fast array measurement of power values
		After calling this method, wait some milliseconds to call the method TLPM_getNextFastArrayMeasurement.
		
		Remark:
		This function starts a new measurement cycle and after finishing measurement the result is received. Subject to the actual Average Count this may take up to seconds.   
		
		Args:
			measurement(uint16)
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_confFastArrayMeasurement(self.devSession, c_uint16(measurement), c_uint16(channel))
		self.__testForError(pInvokeResult)

	def confPowerFastArrayMeasurement(self, channel = 1):
		"""
		This function is used to conffiure the fast array measurement of power values
		After calling this method, wait some milliseconds to call the method TLPM_getNextFastArrayMeasurement.
		
		Remark:
		This function starts a new measurement cycle and after finishing measurement the result is received. Subject to the actual Average Count this may take up to seconds.   
		
		Args:
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_confPowerFastArrayMeasurement(self.devSession, c_uint16(channel))
		self.__testForError(pInvokeResult)

	def confCurrentFastArrayMeasurement(self, channel = 1):
		"""
		This function is used to conffiure the fast array measurement of current values
		After calling this method, wait some milliseconds to call the method TLPM_getNextFastArrayMeasurement.
		
		Remark:
		This function starts a new measurement cycle and after finishing measurement the result is received. Subject to the actual Average Count this may take up to seconds. 
		
		Args:
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_confCurrentFastArrayMeasurement(self.devSession, c_uint16(channel))
		self.__testForError(pInvokeResult)

	def confVoltageFastArrayMeasurement(self, channel = 1):
		"""
		This function is used to conffiure the fast array measurement of voltage values
		After calling this method, wait some milliseconds to call the method TLPM_getNextFastArrayMeasurement.
		
		Remark:
		This function starts a new measurement cycle and after finishing measurement the result is received. Subject to the actual Average Count this may take up to seconds.  
		
		Args:
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_confVoltageFastArrayMeasurement(self.devSession, c_uint16(channel))
		self.__testForError(pInvokeResult)

	def confPDensityFastArrayMeasurement(self, channel = 1):
		"""
		This function is used to conffiure the fast array measurement of P density values
		After calling this method, wait some milliseconds to call the method TLPM_getNextFastArrayMeasurement.
		
		Remark:
		This function starts a new measurement cycle and after finishing measurement the result is received. Subject to the actual Average Count this may take up to seconds. 
		
		Args:
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_confPDensityFastArrayMeasurement(self.devSession, c_uint16(channel))
		self.__testForError(pInvokeResult)

	def confEnergyFastArrayMeasurement(self, channel = 1):
		"""
		This function is used to configure the fast array measurement of energy values
		After calling this method, wait some milliseconds to call the method TLPM_getNextFastArrayMeasurement.
		
		Remark:
		This function starts a new measurement cycle and after finishing measurement the result is received. Subject to the actual Average Count this may take up to seconds. 
		
		Args:
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_confEnergyFastArrayMeasurement(self.devSession, c_uint16(channel))
		self.__testForError(pInvokeResult)

	def confEDensityFastArrayMeasurement(self, channel = 1):
		"""
		This function is used to configure the fast array measurement of E density values.
		After calling this method, wait some milliseconds to call the method TLPM_getNextFastArrayMeasurement.
		
		
		Remark:
		This function starts a new measurement cycle and after finishing measurement the result is received. Subject to the actual Average Count this may take up to seconds. 
		
		Args:
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_confEDensityFastArrayMeasurement(self.devSession, c_uint16(channel))
		self.__testForError(pInvokeResult)

	def getNextFastArrayMeasurement(self, timestamps, values, channel = 1):
		"""
		This function is used to obtain measurements from the instrument. 
		The result are timestamp - value pairs.
		
		
		Remark:
		This function starts a new measurement cycle and after finishing measurement the result is received. Subject to the actual Average Count this may take up to seconds.
		
		Args:
			The value will be 200
			timestamps( (c_uint32 * arrayLength)()) : Buffer containing up to 200 timestamps.
			This are raw timestamps and are NOT in ms.
			values( (c_float * arrayLength)()) : Buffer containing up to 200 measurement values.
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			count(uint32) : The count of timestamp - measurement value pairs
		"""
		pycount = c_uint32(0)
		pInvokeResult = self.dll.TLPMX_getNextFastArrayMeasurement(self.devSession, byref(pycount), timestamps, values, c_uint16(channel))
		self.__testForError(pInvokeResult)
		return  pycount.value

	def getNextFastArrayMeasurementRelativeTime(self, timestamps, values, channel = 1):
		"""
		This function is used to obtain measurements from the instrument. 
		The result are timestamp - value pairs.
		The timestamps are relative to the first timestamp in µsec.
		
		
		Remark:
		This function starts a new measurement cycle and after finishing measurement the result is received. Subject to the actual Average Count this may take up to seconds.
		
		Args:
			The value will be 200
			timestamps( (c_uint32 * arrayLength)()) : Buffer containing up to 200 timestamps.
			This are timestamps in µsec relative to the first timestamp.
			
			e.g.
			timestamp [0] = 0
			timestamp [1] = 10
			timestamp [2] = 20
			
			means that the time difference between the samples are 10 µsec.
			
			values( (c_float * arrayLength)()) : Buffer containing up to 200 measurement values.
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			count(uint32) : The count of timestamp - measurement value pairs
		"""
		pycount = c_uint32(0)
		pInvokeResult = self.dll.TLPMX_getNextFastArrayMeasurementRelativeTime(self.devSession, byref(pycount), timestamps, values, c_uint16(channel))
		self.__testForError(pInvokeResult)
		return  pycount.value

	def getFastMaxSamplerate(self, channel = 1):
		"""
		This function is used to obtain the maximal possible sample rate (Hz) 
		
		Args:
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			pVal(uint32) : Max possible sample rate (Hz)
		"""
		pypVal = c_uint32(0)
		pInvokeResult = self.dll.TLPMX_getFastMaxSamplerate(self.devSession, byref(pypVal), c_uint16(channel))
		self.__testForError(pInvokeResult)
		return  pypVal.value

	def confPowerMeasurementSequence(self, baseTime, channel = 1):
		"""
		This function send the SCPI Command "CONF:ARR:POW" to the device.
		Then is possible to call the method 'getMeasurementSequence' to get the power data.
		
		Duration of measurement in µsec = Count * Interval
		The maximum capture time is 1 sec regardless of the used interval
		
		Set the bandwidth to high(setInputFilterState to OFF) and disable auto ranging(setPowerAutoRange to OFF)
		
		Note: The function is only available on PM101, PM103, PM5020, PM400, PM6x.
		
		
		Args:
			baseTime(uint32) : PM101:
			The array mode always stores 10000 power values in W or dBm with 10 kHz in an internal buffer. So max time resolution between the samples is 100 us. Ensure the product of BaseTime / 100 * samples is always smaller or equal 10000. Also keep BaseTime a multiple of 100
			
			time in us between the samples. Needs to be >= 100
			
			PM103, PM5020, PM6x:
			scope capture devisor for 100 kHz sample rate of scope mode. 0 is not allowed.
			
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_confPowerMeasurementSequence(self.devSession, c_uint32(baseTime), c_uint16(channel))
		self.__testForError(pInvokeResult)

	def confPowerMeasurementSequenceHWTrigger(self, trigSrc, baseTime, hPos, channel = 1):
		"""
		This function send the SCPI Command "CONF:ARR:HWT" to the device.
		Then is possible to call the method 'getMeasurementSequence' to get the power data.
		
		Note: The function is only available on PM5020, PM103, PM6x.
		
		
		Args:
			trigSrc(uint16)
			baseTime(uint32) : PM103:
			interval between two measurements in the array in µsec. The maximum resolution is defined in the device specifications.
			
			PM101 special:
			time to collect measurements.
			hPos(uint32) : PM103:
			Sets the horizontal position of trigger condition in the scope catpure (Between 1 and 9999)
			
			PM101 special:
			Interval between measurements.
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_confPowerMeasurementSequenceHWTrigger(self.devSession, c_uint16(trigSrc), c_uint32(baseTime), c_uint32(hPos), c_uint16(channel))
		self.__testForError(pInvokeResult)

	def confCurrentMeasurementSequence(self, baseTime, channel = 1):
		"""
		This function send the SCPI Command "CONF:ARR:CURR" to the device.
		Then is possible to call the method 'getMeasurementSequence' to get the power data.
		 
		Duration of measurement in µsec = Count* Interval
		The maximum capture time is 1 sec regardless of the used interval
		
		Set the bandwidth to high(setInputFilterState to OFF) and disable auto ranging(setPowerAutoRange to OFF)
		
		Note: The function is only available on  PM101, PM103, PM400, PM6x, PM5020.
		
		
		Args:
			baseTime(uint32) : interval between two measurements in the array in µsec.
			The maximum resolution is defined in the device specifications.
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_confCurrentMeasurementSequence(self.devSession, c_uint32(baseTime), c_uint16(channel))
		self.__testForError(pInvokeResult)

	def confCurrentMeasurementSequenceHWTrigger(self, trigSrc, baseTime, hPos, channel = 1):
		"""
		This function send the SCPI Command "CONF:ARR:HWTrig:CURR" to the device.
		Then is possible to call the method 'getMeasurementSequenceHWTrigger' to get the current data.
		 
		Set the bandwidth to high (setInputFilterState to OFF) and disable auto ranging ( setPowerAutoRange to OFF)
		
		Note: The function is only available on PM103, PM5020, PM6x.
		
		
		Args:
			trigSrc(uint16)
			baseTime(uint32) : PM103:
			interval between two measurements in the array in µsec. The maximum resolution is defined in the device specifications.
			
			PM101 special:
			time to collect measurements.
			hPos(uint32) : PM103:
			Sets the horizontal position of trigger condition in the scope catpure (Between 1 and 9999)
			
			PM101 special:
			Interval between measurements.
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_confCurrentMeasurementSequenceHWTrigger(self.devSession, c_uint16(trigSrc), c_uint32(baseTime), c_uint32(hPos), c_uint16(channel))
		self.__testForError(pInvokeResult)

	def confVolatgeMeasurementSequence(self, baseTime, channel = 1):
		"""
		
		Args:
			baseTime(uint32)
			channel(uint16)
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_confVolatgeMeasurementSequence(self.devSession, c_uint32(baseTime), c_uint16(channel))
		self.__testForError(pInvokeResult)

	def confVolatgeMeasurementSequenceHWTrigger(self, trigSrc, baseTime, hPos, channel = 1):
		"""
		
		Args:
			trigSrc(uint16)
			baseTime(uint32)
			hPos(uint32)
			channel(uint16)
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_confVolatgeMeasurementSequenceHWTrigger(self.devSession, c_uint16(trigSrc), c_uint32(baseTime), c_uint32(hPos), c_uint16(channel))
		self.__testForError(pInvokeResult)

	def confPDENMeasurementSequence(self, baseTime, channel = 1):
		"""
		Configures power density array measurement.
		
		Use this command to configure the measure system for array power density measurement in W/cm^2. The command does not start the measurement. The configuration is only required once. Afterwards you control the measure system by using ABOR, INIT and FETC:ARR? finally.
		The array mode always stores 10000 power values in W or dBm with 10 kHz in an internal buffer. So max time resolution between the samples is 100 us. Ensure the product of delta_t / 100 * samples is always smaller or equal 10000. Also keep delta_t a multiple of 100. Normally it makes sense to disable bandwidth limitation for this measurement mode by using DIAG#:INP:PDI:BWID. SENS#:AVER is not applied for array mode. Also relative power measurements (See SENS#:POW:REF) are not supported in array mode.
		
		Note: The function is only available on PM101, PM400.
		
		
		Args:
			baseTime(uint32) : interval between two measurements in the array in µsec.
			The maximum resolution is defined in the device specifications.
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_confPDENMeasurementSequence(self.devSession, c_uint32(baseTime), c_uint16(channel))
		self.__testForError(pInvokeResult)

	def startMeasurementSequence(self, autoTriggerDelay):
		"""
		This function send the SCPI Command "INIT" to the device.
		
		PM103:
		Then it calls TLPM_readRegister for the register TLPM_REG_OPER_COND if there is new data to read
		
		If this method is successfull you can call getMeasurementSequence or getMeasurementSequenceHWTrigger
		
		PM101 special:
		Just the INIT command is send to the device.
		
		
		Note: The function is only available on PM103, PM6x, PM5020 and PM101. 
		
		
		
		Args:
			autoTriggerDelay(uint32) : PM103:
			The unit of this parameter is milliseconds.
			If this parameter bigger then zero, the method will
			wait the time in milliseconds to send the SCPI command:"TRIGer:ARRay:FORce".
			
			This command will force the measurement. 
			
			PM101 special:
			Not used.
			Return parameter is TRUE if the command:"TRIGer:ARRay:FORce". was internally send to the device. See parameter "AutoTriggerDelay".
			
			PM101 special:
			Not used.
		Returns:
			triggerForced(int16) : PM103:
		"""
		pytriggerForced = c_int16(0)
		pInvokeResult = self.dll.TLPMX_startMeasurementSequence(self.devSession, c_uint32(autoTriggerDelay), byref(pytriggerForced))
		self.__testForError(pInvokeResult)
		return  pytriggerForced.value

	def getMeasurementSequence(self, baseTime, timeStamps, values, values2):
		"""
		 Should be called if the methods confPowerMeasurementSequence and startMeasurementSequence were called first.
		 
		This function filles the given array with (100 * baseTime) measurements from the device.
		
		Duration of measurement in µsec = Count* Interval
		The maximum capture time is 1 sec regardless of the used inteval
		Set the bandwidth to high(setInputFilterState to OFF) and disable auto ranging(setPowerAutoRange to OFF)
		
		Note: The function is only available on PM103x, PM6x, PM5020 and PM101.
		
		
		Args:
			baseTime(uint32) : The amount of samples to collect in the internal interation of the method.
			The value can be from 1 to 100.
			
			Every sample is 10µs for PM5020.
			timeStamps( (c_float * arrayLength)()) : Array of time stamps in ms. The size of this array is 100 * baseTime.
			values( (c_float * arrayLength)()) : Array of power/current measurements. The size of this array is 100 * baseTime.
			values2( (c_float * arrayLength)()) : Array of power/current measurements. The size of this array is 100 * baseTime.
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_getMeasurementSequence(self.devSession, c_uint32(baseTime), timeStamps, values, values2)
		self.__testForError(pInvokeResult)

	def confBurstArrayMeasPowerChannel(self, channel = 1):
		"""
		This function is used to configure the burst array measurement of each channel.
		
		
		Args:
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_confBurstArrayMeasPowerChannel(self.devSession, c_uint16(channel))
		self.__testForError(pInvokeResult)

	def confBurstArrayMeasCurrentChannel(self, channel = 1):
		"""
		Use this command during scope mode configuration to configure channel of scope for current measurement.
		
		
		Args:
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_confBurstArrayMeasCurrentChannel(self.devSession, c_uint16(channel))
		self.__testForError(pInvokeResult)

	def confBurstArrayMeasVoltageChannel(self, channel = 1):
		"""
		Use this command during scope mode configuration to configure channel of scope for voltage measurement.
		
		
		Args:
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_confBurstArrayMeasVoltageChannel(self.devSession, c_uint16(channel))
		self.__testForError(pInvokeResult)

	def confBurstArrayMeasTrigger(self, trgSource, initDelay, burstCount, averaging):
		"""
		This function is used to configure the burst array measurement trigger.
		All entered values are multiplied internally by 10µs. The sum of all values is the burst sequence time.
		
		E.g. 
		Init Delay 5
		Burst Count 2
		Averaging 3
		=> Burst Sequence time = (InitDelay + (Burst Count * Averaging))*10µs = (5+2*3)*10µs =110µs
		
		
		Args:
			trgSource(uint32) : Trigger source. 
			
			1(default) signal of channel 1
			2 signal of channel 2
			3 signal of front AUX 
			4 signal of rear trigger
			initDelay(uint32) : Init Delay time in 10µs.
			E.g. 5 means 5*10µs = 50µs 
			burstCount(uint32) : Enter the Sequence Count in 10µs for the burst sequence time.
			E.g. Sequence count = 2: Burst Sequence time = (InitDelay + (SequenceCount * Averaging)) * 10µs
			averaging(uint32) : Average time in 10µs
			E.g. Entered 3 means averaging of 30µs
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_confBurstArrayMeasTrigger(self.devSession, c_uint32(trgSource), c_uint32(initDelay), c_uint32(burstCount), c_uint32(averaging))
		self.__testForError(pInvokeResult)

	def startBurstArrayMeasurement(self):
		"""
		Starts a burst array measurement
		"""
		pInvokeResult = self.dll.TLPMX_startBurstArrayMeasurement(self.devSession)
		self.__testForError(pInvokeResult)

	def getBurstArraySamplesCount(self):
		"""
		Read the amount of samples in the burst array buffer
		
		Args:
		Returns:
			samplesCount(uint32) : Amount of samples measure in burst mode.
		"""
		pysamplesCount = c_uint32(0)
		pInvokeResult = self.dll.TLPMX_getBurstArraySamplesCount(self.devSession, byref(pysamplesCount))
		self.__testForError(pInvokeResult)
		return  pysamplesCount.value

	def getBurstArraySamples(self, startIndex, sampleCount, timeStamps, values, values2):
		"""
		Read scope buffer content at index 
		
		Args:
			startIndex(uint32)
			sampleCount(uint32)
			timeStamps( (c_uint32 * arrayLength)()) : Buffer containing the samples.
			
			Buffer size: Samples Count * 2
			values( (c_float * arrayLength)())
			values2( (c_float * arrayLength)())
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_getBurstArraySamples(self.devSession, c_uint32(startIndex), c_uint32(sampleCount), timeStamps, values, values2)
		self.__testForError(pInvokeResult)

	def disableArrayMeasurementChannel(self, channel = 1):
		"""
		Use this command during scope mode configuration to disable measurement of channel of scope or burst mode. 
		If no sensor is connected disabling channel is not possible.
		
		
		Args:
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_disableArrayMeasurementChannel(self.devSession, c_uint16(channel))
		self.__testForError(pInvokeResult)

	def setDigIoDirection(self, IO0, IO1, IO2, IO3):
		"""
		This function sets the digital I/O port direction.
		
		Note: The function is only available on PM200 and PM400.
		
		Args:
			IO0(int16) : This parameter specifies the I/O port #0 direction.
			
			Input:  VI_OFF (0)
			Output: VI_ON  (1)
			
			IO1(int16) : This parameter specifies the I/O port #1 direction.
			
			Input:  VI_OFF (0)
			Output: VI_ON  (1)
			
			IO2(int16) : This parameter specifies the I/O port #2 direction.
			
			Input:  VI_OFF (0)
			Output: VI_ON  (1)
			
			IO3(int16) : This parameter specifies the I/O port #3 direction.
			
			Input:  VI_OFF (0)
			Output: VI_ON  (1)
			
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_setDigIoDirection(self.devSession, c_int16(IO0), c_int16(IO1), c_int16(IO2), c_int16(IO3))
		self.__testForError(pInvokeResult)

	def getDigIoDirection(self):
		"""
		This function returns the digital I/O port direction.
		
		Note: The function is only available on PM200 and PM400.
		
		Args:
			
			Note: You may pass VI_NULL if you don't need this value.
			
			
			Note: You may pass VI_NULL if you don't need this value.
			
			
			Note: You may pass VI_NULL if you don't need this value.
			
			
			Note: You may pass VI_NULL if you don't need this value.
			
		Returns:
			IO0(int16) : This parameter returns the I/O port #0 direction where VI_OFF (0) indicates input and VI_ON (1) indicates output.
			IO1(int16) : This parameter returns the I/O port #1 direction where VI_OFF (0) indicates input and VI_ON (1) indicates output.
			IO2(int16) : This parameter returns the I/O port #2 direction where VI_OFF (0) indicates input and VI_ON (1) indicates output.
			IO3(int16) : This parameter returns the I/O port #3 direction where VI_OFF (0) indicates input and VI_ON (1) indicates output.
		"""
		pyIO0 = c_int16(0)
		pyIO1 = c_int16(0)
		pyIO2 = c_int16(0)
		pyIO3 = c_int16(0)
		pInvokeResult = self.dll.TLPMX_getDigIoDirection(self.devSession, byref(pyIO0), byref(pyIO1), byref(pyIO2), byref(pyIO3))
		self.__testForError(pInvokeResult)
		return  pyIO0.value, pyIO1.value, pyIO2.value, pyIO3.value

	def setDigIoOutput(self, IO0, IO1, IO2, IO3):
		"""
		This function sets the digital I/O outputs.
		
		Notes:
		(1) Only ports configured as outputs are affected by this function. Use <Set Digital I/O Direction> to configure ports as outputs.
		(2) The function is only available on PM200 and PM400.
		
		Args:
			IO0(int16) : This parameter specifies the I/O port #0 output.
			
			Low level:  VI_OFF (0)
			High level: VI_ON  (1)
			
			IO1(int16) : This parameter specifies the I/O port #1 output.
			
			Low level:  VI_OFF (0)
			High level: VI_ON  (1)
			
			IO2(int16) : This parameter specifies the I/O port #2 output.
			
			Low level:  VI_OFF (0)
			High level: VI_ON  (1)
			
			IO3(int16) : This parameter specifies the I/O port #3 output.
			
			Low level:  VI_OFF (0)
			High level: VI_ON  (1)
			
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_setDigIoOutput(self.devSession, c_int16(IO0), c_int16(IO1), c_int16(IO2), c_int16(IO3))
		self.__testForError(pInvokeResult)

	def getDigIoOutput(self):
		"""
		This function returns the digital I/O output settings.
		
		Note: The function is only available on PM200 and PM400.
		
		Args:
			
			Note: You may pass VI_NULL if you don't need this value.
			
			
			Note: You may pass VI_NULL if you don't need this value.
			
			
			Note: You may pass VI_NULL if you don't need this value.
			
			
			Note: You may pass VI_NULL if you don't need this value.
			
		Returns:
			IO0(int16) : This parameter returns the I/O port #0 output where VI_OFF (0) indicates low level and VI_ON (1) indicates high level.
			IO1(int16) : This parameter returns the I/O port #1 output where VI_OFF (0) indicates low level and VI_ON (1) indicates high level.
			IO2(int16) : This parameter returns the I/O port #2 output where VI_OFF (0) indicates low level and VI_ON (1) indicates high level.
			IO3(int16) : This parameter returns the I/O port #3 output where VI_OFF (0) indicates low level and VI_ON (1) indicates high level.
		"""
		pyIO0 = c_int16(0)
		pyIO1 = c_int16(0)
		pyIO2 = c_int16(0)
		pyIO3 = c_int16(0)
		pInvokeResult = self.dll.TLPMX_getDigIoOutput(self.devSession, byref(pyIO0), byref(pyIO1), byref(pyIO2), byref(pyIO3))
		self.__testForError(pInvokeResult)
		return  pyIO0.value, pyIO1.value, pyIO2.value, pyIO3.value

	def getDigIoPort(self):
		"""
		This function returns the actual digital I/O port level.
		
		Note: The function is only available on PM200 and PM400.
		
		Args:
			
			Note: You may pass VI_NULL if you don't need this value.
			
			
			Note: You may pass VI_NULL if you don't need this value.
			
			
			Note: You may pass VI_NULL if you don't need this value.
			
			
			Note: You may pass VI_NULL if you don't need this value.
			
		Returns:
			IO0(int16) : This parameter returns the I/O port #0 level where VI_OFF (0) indicates low level and VI_ON (1) indicates high level.
			IO1(int16) : This parameter returns the I/O port #1 level where VI_OFF (0) indicates low level and VI_ON (1) indicates high level.
			IO2(int16) : This parameter returns the I/O port #2 level where VI_OFF (0) indicates low level and VI_ON (1) indicates high level.
			IO3(int16) : This parameter returns the I/O port #3 level where VI_OFF (0) indicates low level and VI_ON (1) indicates high level.
		"""
		pyIO0 = c_int16(0)
		pyIO1 = c_int16(0)
		pyIO2 = c_int16(0)
		pyIO3 = c_int16(0)
		pInvokeResult = self.dll.TLPMX_getDigIoPort(self.devSession, byref(pyIO0), byref(pyIO1), byref(pyIO2), byref(pyIO3))
		self.__testForError(pInvokeResult)
		return  pyIO0.value, pyIO1.value, pyIO2.value, pyIO3.value

	def setDigIoPinMode(self, pinNumber, pinMode):
		"""
		This function sets the digital I/O port direction.
		
		Note: The function is only available on PM200, PM400 and PM103
		
		Args:
			pinNumber(int16) : Number of the Pin.
			
			Range: 1-7
			pinMode(uint16) : This parameter specifies the I/O port direction.
			
			Input:       DIGITAL_IO_CONFIG_INPUT   (0)
			Output:      DIGITAL_IO_CONFIG_OUTPUT  (1)
			Alternative: DIGITAL_IO_CONFIG_ALT     (2)
			
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_setDigIoPinMode(self.devSession, c_int16(pinNumber), c_uint16(pinMode))
		self.__testForError(pInvokeResult)

	def getDigIoPinMode(self, pinNumber):
		"""
		This function returns the digital I/O port direction.
		
		Note: The function is only available on PM200, PM400 and PM103
		
		Args:
			pinNumber(int16) : Number of the Pin.
			
			Range: 1-7
			
			Note: You may pass VI_NULL if you don't need this value.
			
			Input:              DIGITAL_IO_CONFIG_INPUT      (0)
			Output:             DIGITAL_IO_CONFIG_OUTPUT     (1)
			Input Alternative:  DIGITAL_IO_CONFIG_INPUT_ALT  (2)
			Output Alternative: DIGITAL_IO_CONFIG_OUTPUT_ALT (3)
			
			
			
		Returns:
			pinMode(uint16) : This parameter returns the I/O port #0 direction.
		"""
		pypinMode = c_uint16(0)
		pInvokeResult = self.dll.TLPMX_getDigIoPinMode(self.devSession, c_int16(pinNumber), byref(pypinMode))
		self.__testForError(pInvokeResult)
		return  pypinMode.value

	def setDigIoOutput2(self, IO0, IO1, IO2, IO3):
		"""
		
		Args:
			IO0(int16)
			IO1(int16)
			IO2(int16)
			IO3(int16)
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_setDigIoOutput(self.devSession, c_int16(IO0), c_int16(IO1), c_int16(IO2), c_int16(IO3))
		self.__testForError(pInvokeResult)

	def getDigIoOutput2(self):
		"""
		
		Args:
		Returns:
			IO0(int16)
			IO1(int16)
			IO2(int16)
			IO3(int16)
		"""
		pyIO0 = c_int16(0)
		pyIO1 = c_int16(0)
		pyIO2 = c_int16(0)
		pyIO3 = c_int16(0)
		pInvokeResult = self.dll.TLPMX_getDigIoOutput(self.devSession, byref(pyIO0), byref(pyIO1), byref(pyIO2), byref(pyIO3))
		self.__testForError(pInvokeResult)
		return  pyIO0.value, pyIO1.value, pyIO2.value, pyIO3.value

	def getDigIoPinInput(self):
		"""
		This function returns the actual digital I/O port level.
		
		Note: The function is only available on PM200 and PM400.
		
		Args:
			
			Note: You may pass VI_NULL if you don't need this value.
			
			
			Note: You may pass VI_NULL if you don't need this value.
			
			
			Note: You may pass VI_NULL if you don't need this value.
			
			
			Note: You may pass VI_NULL if you don't need this value.
			
		Returns:
			IO0(int16) : This parameter returns the I/O port #0 level where VI_OFF (0) indicates low level and VI_ON (1) indicates high level.
			IO1(int16) : This parameter returns the I/O port #1 level where VI_OFF (0) indicates low level and VI_ON (1) indicates high level.
			IO2(int16) : This parameter returns the I/O port #2 level where VI_OFF (0) indicates low level and VI_ON (1) indicates high level.
			IO3(int16) : This parameter returns the I/O port #3 level where VI_OFF (0) indicates low level and VI_ON (1) indicates high level.
		"""
		pyIO0 = c_int16(0)
		pyIO1 = c_int16(0)
		pyIO2 = c_int16(0)
		pyIO3 = c_int16(0)
		pInvokeResult = self.dll.TLPMX_getDigIoPinInput(self.devSession, byref(pyIO0), byref(pyIO1), byref(pyIO2), byref(pyIO3))
		self.__testForError(pInvokeResult)
		return  pyIO0.value, pyIO1.value, pyIO2.value, pyIO3.value

	def getShutterInterlock(self):
		"""
		This function sets the state of the fan to 
		
		OFF (0)
		FULL (1)
		
		Note: The function is only available on PM5020
		
		Args:
		Returns:
			interlockState(int16)
		"""
		pyinterlockState = c_int16(0)
		pInvokeResult = self.dll.TLPMX_getShutterInterlock(self.devSession, byref(pyinterlockState))
		self.__testForError(pInvokeResult)
		return  pyinterlockState.value

	def setShutterPosition(self, position):
		"""
		This function sets the state of the fan to 
		
		OFF (0)
		FULL (1)
		
		Note: The function is only available on PM5020
		
		Args:
			position(int16)
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_setShutterPosition(self.devSession, c_int16(position))
		self.__testForError(pInvokeResult)

	def getShutterPosition(self):
		"""
		This function sets the state of the fan to 
		
		OFF (0)
		FULL (1)
		
		Note: The function is only available on PM5020
		
		Args:
		Returns:
			position(int16)
		"""
		pyposition = c_int16(0)
		pInvokeResult = self.dll.TLPMX_getShutterPosition(self.devSession, byref(pyposition))
		self.__testForError(pInvokeResult)
		return  pyposition.value

	def setI2CMode(self, mode):
		"""
		This setter changes the I2C speed and operating mode. By dafault I2C is controlled by the powermeter and SCPI I2C commands are disabled. It is mandatory to select a manual mode before SCPI I2C commands are enabled. The configuraiton is not stored for next boot. Be aware in manual mode the optional external environmental sensor will not longer be queried by the powermeter. The following modes are supported
		INTER: I2C controlled by powermeter. SCPI I2C disabled.
		SLOW: I2C controlled by SCPI commands in 100k standard speed. Powermeter does not access bus.
		FAST: I2C controlled by SCPI commands in 400k fast speed. Powermeter does not access bus.
		
		Note: The function is only available on PM5020
		
		Args:
			mode(uint16) : INTER,SLOW,FASTnew I2C operating mode and speed. See list in detail section.
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_setI2CMode(self.devSession, c_uint16(mode))
		self.__testForError(pInvokeResult)

	def getI2CMode(self):
		"""
		The command queries the I2C speed and operating mode. 
		INTER: I2C controlled by powermeter. SCPI I2C disabled.
		SLOW: I2C controlled by SCPI commands in 100k standard speed. Powermeter does not access bus.
		FAST: I2C controlled by SCPI commands in 400k fast speed. Powermeter does not access bus.
		
		Note: The function is only available on PM5020
		
		Args:
		Returns:
			mode(int16) : INTER,SLOW,FASTI2C operating mode and speed
		"""
		pymode = c_int16(0)
		pInvokeResult = self.dll.TLPMX_getI2CMode(self.devSession, byref(pymode))
		self.__testForError(pInvokeResult)
		return  pymode.value

	def I2CRead(self, address, count):
		"""
		The command receives data from slave with given address. The function requires TLPMX_setI2CMode to be called once previously. The command returns data as integer. Data is read synchronously with the SCPI command.
		
		Note: The function is only available on PM5020
		
		Args:
			address(uint32) : I2C slave address. Address are bit 7 to bit 1. Bit 0 is ignored.
			count(uint32) : amount of bytes to read from address. Needs to be less than 128.
		Returns:
			dataRead(uint32) : received data.
		"""
		pydataRead = c_uint32(0)
		pInvokeResult = self.dll.TLPMX_I2CRead(self.devSession, c_uint32(address), c_uint32(count), byref(pydataRead))
		self.__testForError(pInvokeResult)
		return  pydataRead.value

	def I2CWrite(self, address, hexData):
		"""
		The command transmits given data to slave with given address. The function requires TLPMX_setI2CMode  to be called once previously. The transmission data is given as hexadecimal string parameter. The length needs to be a multiple of two as two hex digits encode a single byte. Leading zeros are mandatory. So to transfer byte 2 and 75 use string 024B. Hex digits are support upper or lowercase letters. The maximal length are 128 Bytes. Data is transferred synchronously with the SCPI command. If you want to read after writing some data you may use TLPMX_I2CWriteRead.
		
		Note: The function is only available on PM5020
		
		Args:
			address(uint32) : I2C slave address. Address are bit 7 to bit 1. Bit 0 is ignored.
			hexData(char_p) : transmission data as hexadecimal string without byte separator. Length always multiple of 2.
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_I2CWrite(self.devSession, c_uint32(address), c_char_p(hexData.encode('utf-8')))
		self.__testForError(pInvokeResult)

	def I2CWriteRead(self, address, hexSendData, count):
		"""
		The command transmits given data to slave with given address following a bus reception from same device if transmission was successful. This command is a convenience function for a CON:I2C#:WRIT followed by a CON:I2C#:READ? command sequence. The maximal transmission and reception byte count is 128. For closer details of hexString format read TLPMX_I2CWrite command description.
		
		Note: The function is only available on PM5020
		
		Args:
			address(uint32) : I2C slave address. Address are bit 7 to bit 1. Bit 0 is ignored.
			hexSendData(char_p) : transmission data as hexadecimal string without byte separator. Length always multiple of 2.
			count(uint32) : amount of bytes to read from address.
		Returns:
			dataRead(uint32) : received data.
		"""
		pydataRead = c_uint32(0)
		pInvokeResult = self.dll.TLPMX_I2CWriteRead(self.devSession, c_uint32(address), c_char_p(hexSendData.encode('utf-8')), c_uint32(count), byref(pydataRead))
		self.__testForError(pInvokeResult)
		return  pydataRead.value

	def getFanState(self, channel = 1):
		"""
		This function returns if the fan is running
		
		Note: The function is only available on PM5020
		
		Args:
			
			VI_OFF (0) Fan is still
			VI_ON  (1) Fan is running
			channel(uint16) : Number of the fan channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			isRunning(int16) : Returns the fan running state
		"""
		pyisRunning = c_int16(0)
		pInvokeResult = self.dll.TLPMX_getFanState(self.devSession, byref(pyisRunning), c_uint16(channel))
		self.__testForError(pInvokeResult)
		return  pyisRunning.value

	def setFanMode(self, mode, channel = 1):
		"""
		This function sets the state of the fan to 
		
		FAN_OPER_OFF         (0)
		FAN_OPER_FULL        (1)
		FAN_OPER_OPEN_LOOP   (2)
		FAN_OPER_CLOSED_LOOP (3)
		FAN_OPER_TEMPER_CTRL (4)
		
		Note: The function is only available on PM5020
		
		Args:
			mode(uint16)
			channel(uint16) : Number of the fan channel. 
			
			Default: 1 for non multi channel devices
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_setFanMode(self.devSession, c_uint16(mode), c_uint16(channel))
		self.__testForError(pInvokeResult)

	def getFanMode(self, channel = 1):
		"""
		This function gets the state of the fan of
		
		FAN_OPER_OFF         (0)
		FAN_OPER_FULL        (1)
		FAN_OPER_OPEN_LOOP   (2)
		FAN_OPER_CLOSED_LOOP (3)
		FAN_OPER_TEMPER_CTRL (4)
		
		Note: The function is only available on PM5020
		
		Args:
			channel(uint16) : Number of the fan channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			mode(uint16)
		"""
		pymode = c_uint16(0)
		pInvokeResult = self.dll.TLPMX_getFanMode(self.devSession, byref(pymode), c_uint16(channel))
		self.__testForError(pInvokeResult)
		return  pymode.value

	def setFanVoltage(self, voltage, channel = 1):
		"""
		This function sets the state of the fan to 
		
		OFF (0)
		FULL (1)
		
		Note: The function is only available on PM5020
		
		Args:
			voltage(double)
			channel(uint16) : Number of the fan channel. 
			
			Default: 1 for non multi channel devices
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_setFanVoltage(self.devSession, c_double(voltage), c_uint16(channel))
		self.__testForError(pInvokeResult)

	def getFanVoltage(self, channel = 1):
		"""
		This function sets the state of the fan to 
		
		OFF (0)
		FULL (1)
		
		Note: The function is only available on PM5020
		
		Args:
			channel(uint16) : Number of the fan channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			voltage(double)
		"""
		pyvoltage = c_double(0)
		pInvokeResult = self.dll.TLPMX_getFanVoltage(self.devSession, byref(pyvoltage), c_uint16(channel))
		self.__testForError(pInvokeResult)
		return  pyvoltage.value

	def setFanRpm(self, maxRPM, targetRPM, channel = 1):
		"""
		This function sets the state of the fan to 
		
		OFF (0)
		FULL (1)
		
		Note: The function is only available on PM5020
		
		Args:
			maxRPM(double) : Max RPM of the Fan
			targetRPM(double) : Target RPM of the Fan
			channel(uint16) : Number of the fan channel. 
			
			Default: 1 for non multi channel devices
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_setFanRpm(self.devSession, c_double(maxRPM), c_double(targetRPM), c_uint16(channel))
		self.__testForError(pInvokeResult)

	def getFanRpm(self, channel = 1):
		"""
		This function sets the state of the fan to 
		
		OFF (0)
		FULL (1)
		
		Note: The function is only available on PM5020
		
		Args:
			channel(uint16) : Number of the fan channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			maxRPM(double) : Max RPM of the fan
			targetRPM(double) : Target RPM of the fan
		"""
		pymaxRPM = c_double(0)
		pytargetRPM = c_double(0)
		pInvokeResult = self.dll.TLPMX_getFanRpm(self.devSession, byref(pymaxRPM), byref(pytargetRPM), c_uint16(channel))
		self.__testForError(pInvokeResult)
		return  pymaxRPM.value, pytargetRPM.value

	def getActFanRpm(self, channel = 1):
		"""
		Gets the current rpm of the fan
		
		Note: The function is only available on PM5020
		
		Args:
			channel(uint16) : Number of the fan channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			RPM(double) : Current RPM of the fan
		"""
		pyRPM = c_double(0)
		pInvokeResult = self.dll.TLPMX_getActFanRpm(self.devSession, byref(pyRPM), c_uint16(channel))
		self.__testForError(pInvokeResult)
		return  pyRPM.value

	def setFanTemperatureSource(self, source, channel = 1):
		"""
		This function sets the source for the temperature control
		
		FAN_TEMPER_SRC_HEAD (0)    ///< Sensor head temper source
		FAN_TEMPER_SRC_EXT_NTC (1) ///< External NTC temper source
		
		Note: The function is only available on PM5020
		
		Args:
			source(uint16) : Source for the temperature control
			
			FAN_TEMPER_SRC_HEAD (0)    ///< Sensor head temper source
			FAN_TEMPER_SRC_EXT_NTC (1) ///< External NTC temper source
			channel(uint16) : Number of the fan channel. 
			
			Default: 1 for non multi channel devices
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_setFanTemperatureSource(self.devSession, c_uint16(source), c_uint16(channel))
		self.__testForError(pInvokeResult)

	def getFanTemperatureSource(self, channel = 1):
		"""
		This function gets the source for the temperature control
		
		FAN_TEMPER_SRC_HEAD (0)    ///< Sensor head temper source
		FAN_TEMPER_SRC_EXT_NTC (1) ///< External NTC temper source
		
		Note: The function is only available on PM5020
		
		Args:
			
			FAN_TEMPER_SRC_HEAD (0)    ///< Sensor head temper source
			FAN_TEMPER_SRC_EXT_NTC (1) ///< External NTC temper source
			channel(uint16) : Number of the fan channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			source(uint16) : Source for the temperature control
		"""
		pysource = c_uint16(0)
		pInvokeResult = self.dll.TLPMX_getFanTemperatureSource(self.devSession, byref(pysource), c_uint16(channel))
		self.__testForError(pInvokeResult)
		return  pysource.value

	def setFanAdjustParameters(self, voltageMin, voltageMax, temperatureMin, temperatureMax, channel = 1):
		"""
		This function sets the state of the fan to 
		
		OFF (0)
		FULL (1)
		
		Note: The function is only available on PM5020
		
		Args:
			voltageMin(double)
			voltageMax(double)
			temperatureMin(double)
			temperatureMax(double)
			channel(uint16) : Number of the fan channel. 
			
			Default: 1 for non multi channel devices
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_setFanAdjustParameters(self.devSession, c_double(voltageMin), c_double(voltageMax), c_double(temperatureMin), c_double(temperatureMax), c_uint16(channel))
		self.__testForError(pInvokeResult)

	def getFanAdjustParameters(self, channel = 1):
		"""
		This function sets the state of the fan to 
		
		OFF (0)
		FULL (1)
		
		Note: The function is only available on PM5020
		
		Args:
			channel(uint16) : Number of the fan channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			voltageMin(double)
			voltageMax(double)
			temperatureMin(double)
			temperatureMax(double)
		"""
		pyvoltageMin = c_double(0)
		pyvoltageMax = c_double(0)
		pytemperatureMin = c_double(0)
		pytemperatureMax = c_double(0)
		pInvokeResult = self.dll.TLPMX_getFanAdjustParameters(self.devSession, byref(pyvoltageMin), byref(pyvoltageMax), byref(pytemperatureMin), byref(pytemperatureMax), c_uint16(channel))
		self.__testForError(pInvokeResult)
		return  pyvoltageMin.value, pyvoltageMax.value, pytemperatureMin.value, pytemperatureMax.value

	def setLaserState(self, state, frequency, duration):
		"""
		Use this command to enable or disable the fibre laser in CW or TTL modulated mode. The function allows to enable the timer for a defined period or endless for CW and TTL mode. The time resolution is limited by the modulation frequency in TTL mode. The maximal duration is 10 seconds. Modulation is limited to 100 Hz. Use frequency 0 for CW mode. The laser might be disabled in any case.
		
		Note: The function is only available on PM61.
		
		Args:
			state(int16) : 1 to enable. 0 for disable.
			frequency(uint32) : Optional! modulation frequency <= 100Hz. 0 for CW.
			duration(uint32) :  Optional! duration of laser sequence in ms. Resolution depends on frequ. Set to 65535 for endless.
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_setLaserState(self.devSession, c_int16(state), c_uint32(frequency), c_uint32(duration))
		self.__testForError(pInvokeResult)

	def getLaserState(self):
		"""
		Use this command to enable or disable the fibre laser in CW or TTL modulated mode. The function allows to enable the timer for a defined period or endless for CW and TTL mode. The time resolution is limited by the modulation frequency in TTL mode. The maximal duration is 10 seconds. Modulation is limited to 100 Hz. Use frequency 0 for CW mode. The laser might be disabled in any case.
		
		Note: The function is only available on PM61.
		
		Args:
		Returns:
			state(int16) :  1 if enabled. 0 for disabled.
		"""
		pystate = c_int16(0)
		pInvokeResult = self.dll.TLPMX_getLaserState(self.devSession, byref(pystate))
		self.__testForError(pInvokeResult)
		return  pystate.value

	def errorMessage(self, statusCode):
		"""
		This function takes the error code returned by the instrument driver functions interprets it and returns it as an user readable string. 
		
		Status/error codes and description:
		
		--- Instrument Driver Errors and Warnings ---
		Status      Description
		-------------------------------------------------
		         0  No error (the call was successful).
		0x3FFF0085  Unknown Status Code     - VI_WARN_UNKNOWN_STATUS
		0x3FFC0901  WARNING: Value overflow - VI_INSTR_WARN_OVERFLOW
		0x3FFC0902  WARNING: Value underrun - VI_INSTR_WARN_UNDERRUN
		0x3FFC0903  WARNING: Value is NaN   - VI_INSTR_WARN_NAN
		0xBFFC0001  Parameter 1 out of range. 
		0xBFFC0002  Parameter 2 out of range.
		0xBFFC0003  Parameter 3 out of range.
		0xBFFC0004  Parameter 4 out of range.
		0xBFFC0005  Parameter 5 out of range.
		0xBFFC0006  Parameter 6 out of range.
		0xBFFC0007  Parameter 7 out of range.
		0xBFFC0008  Parameter 8 out of range.
		0xBFFC0012  Error Interpreting instrument response.
		
		--- Instrument Errors --- 
		Range: 0xBFFC0700 .. 0xBFFC0CFF.
		Calculation: Device error code + 0xBFFC0900.
		Please see your device documentation for details.
		
		--- VISA Errors ---
		Please see your VISA documentation for details.
		
		
		Args:
			statusCode(int) : This parameter accepts the error codes returned from the instrument driver functions.
			
			Default Value: 0 - VI_SUCCESS
			
			Notes:
			(1) The message buffer has to be initalized with 256 bytes.
			
		Returns:
			description(string) : This parameter returns the interpreted code as an user readable message string.
		"""
		pydescription = create_string_buffer(1024)
		pInvokeResult = self.dll.TLPMX_errorMessage(self.devSession, c_int(statusCode), pydescription)
		self.__testForError(pInvokeResult)
		return c_char_p(pydescription.raw).value

	def errorQuery(self):
		"""
		This function queries the instrument's error queue manually. 
		Use this function to query the instrument's error queue if the driver's error query mode is set to manual query. 
		
		Notes:
		(1) The returned values are stored in the drivers error store. You may use <Error Message> to get a descriptive text at a later point of time.
		
		Args:
			
			Notes:
			(1) You may pass VI_NULL if you don't need this value.
			
			
			Notes:
			(1) The array must contain at least 256 elements ViChar[256] including the null byte.
			(2) You may pass VI_NULL if you do not need this value.
			
		Returns:
			errorNumber(int) : This parameter returns the instrument error number.
			errorMessage(string) : This parameter returns the instrument error message.
		"""
		pyerrorNumber = c_int(0)
		pyerrorMessage = create_string_buffer(1024)
		pInvokeResult = self.dll.TLPMX_errorQuery(self.devSession, byref(pyerrorNumber), pyerrorMessage)
		self.__testForError(pInvokeResult)
		return  pyerrorNumber.value, c_char_p(pyerrorMessage.raw).value

	def errorQueryMode(self, mode):
		"""
		This function selects the driver's error query mode.
		
		Args:
			mode(int16) : This parameter specifies the driver's error query mode. 
			
			If set to Automatic each driver function queries the instrument's error queue and in case an error occured returns the error number.
			
			If set to Manual the driver does not query the instrument for errors and therefore a driver function does not return instrument errors. You should use <Error Query> to manually query the instrument's error queue.
			
			VI_OFF (0): Manual error query.
			VI_ON  (1): Automatic error query (default).
			
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_errorQueryMode(self.devSession, c_int16(mode))
		self.__testForError(pInvokeResult)

	def errorCount(self):
		"""
		This function returns the number of errors in the queue.
		
		Args:
			
			Notes:
			(1) You may pass VI_NULL if you don't need this value.
			
		Returns:
			count(uint32) : This parameter returns the instrument error number.
		"""
		pycount = c_uint32(0)
		pInvokeResult = self.dll.TLPMX_errorCount(self.devSession, byref(pycount))
		self.__testForError(pInvokeResult)
		return  pycount.value

	def reset(self):
		"""
		Places the instrument in a default state.
		"""
		pInvokeResult = self.dll.TLPMX_reset(self.devSession)
		self.__testForError(pInvokeResult)

	def selfTest(self):
		"""
		This function runs the device self test routine and returns the test result.
		
		Args:
			
			Notes:
			(1) The array must contain at least 256 elements ViChar[256].
			
		Returns:
			selfTestResult(int16) : This parameter contains the value returned from the device self test routine. A retured zero value indicates a successful run, a value other than zero indicates failure.
			description(string) : This parameter returns the interpreted code as an user readable message string.
		"""
		pyselfTestResult = c_int16(0)
		pydescription = create_string_buffer(1024)
		pInvokeResult = self.dll.TLPMX_selfTest(self.devSession, byref(pyselfTestResult), pydescription)
		self.__testForError(pInvokeResult)
		return  pyselfTestResult.value, c_char_p(pydescription.raw).value

	def revisionQuery(self):
		"""
		This function returns the revision numbers of the instrument driver and the device firmware.
		
		Args:
			
			Notes:
			(1) The array must contain at least 256 elements ViChar[256].
			(2) You may pass VI_NULL if you do not need this value.
			
			
			Notes:
			(1) The array must contain at least 256 elements ViChar[256].
			(2) You may pass VI_NULL if you do not need this value.
			
		Returns:
			instrumentDriverRevision(string) : This parameter returns the Instrument Driver revision.
			firmwareRevision(string) : This parameter returns the device firmware revision. 
		"""
		pyinstrumentDriverRevision = create_string_buffer(1024)
		pyfirmwareRevision = create_string_buffer(1024)
		pInvokeResult = self.dll.TLPMX_revisionQuery(self.devSession, pyinstrumentDriverRevision, pyfirmwareRevision)
		self.__testForError(pInvokeResult)
		return c_char_p(pyinstrumentDriverRevision.raw).value, c_char_p(pyfirmwareRevision.raw).value

	def identificationQuery(self):
		"""
		This function returns the device identification information.
		
		Args:
			
			Notes:
			(1) The array must contain at least 256 elements ViChar[256].
			(2) You may pass VI_NULL if you do not need this value.
			
			
			Notes:
			(1) The array must contain at least 256 elements ViChar[256].
			(2) You may pass VI_NULL if you do not need this value.
			
			
			Notes:
			(1) The array must contain at least 256 elements ViChar[256].
			(2) You may pass VI_NULL if you do not need this value.
			
			
			Notes:
			(1) The array must contain at least 256 elements ViChar[256].
			(2) You may pass VI_NULL if you do not need this value.
			
		Returns:
			manufacturerName(string) : This parameter returns the manufacturer name.
			deviceName(string) : This parameter returns the device name.
			serialNumber(string) : This parameter returns the device serial number.
			firmwareRevision(string) : This parameter returns the device firmware revision.
		"""
		pymanufacturerName = create_string_buffer(1024)
		pydeviceName = create_string_buffer(1024)
		pyserialNumber = create_string_buffer(1024)
		pyfirmwareRevision = create_string_buffer(1024)
		pInvokeResult = self.dll.TLPMX_identificationQuery(self.devSession, pymanufacturerName, pydeviceName, pyserialNumber, pyfirmwareRevision)
		self.__testForError(pInvokeResult)
		return c_char_p(pymanufacturerName.raw).value, c_char_p(pydeviceName.raw).value, c_char_p(pyserialNumber.raw).value, c_char_p(pyfirmwareRevision.raw).value

	def getCalibrationMsg(self, channel = 1):
		"""
		This function returns a human readable calibration message.
		
		
		Args:
			
			Notes:
			(1) The array must contain at least TLPM_BUFFER_SIZE (256) elements ViChar[256].
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			message(string) : This parameter returns the calibration message.
		"""
		pymessage = create_string_buffer(1024)
		pInvokeResult = self.dll.TLPMX_getCalibrationMsg(self.devSession, pymessage, c_uint16(channel))
		self.__testForError(pInvokeResult)
		return c_char_p(pymessage.raw).value

	def setDisplayName(self):
		"""
		This method send the SCPI command SYST:COMM:NET:HOST %S
		This name is used by the PM400 as custom display name
		and by the PM103E as network hostname.
		
		Args:
			
		Returns:
			name(string) : This parameter specifies the baudrate in bits/sec.
		"""
		pyname = create_string_buffer(1024)
		pInvokeResult = self.dll.TLPMX_setDisplayName(self.devSession, pyname)
		self.__testForError(pInvokeResult)
		return c_char_p(pyname.raw).value

	def getDisplayName(self):
		"""
		This method send the SCPI command SYST:COMM:NET:HOST?
		This name is used by the PM400 as custom display name
		and by the PM103E as network hostname.
		
		Args:
		Returns:
			name(string)
		"""
		pyname = create_string_buffer(1024)
		pInvokeResult = self.dll.TLPMX_getDisplayName(self.devSession, pyname)
		self.__testForError(pInvokeResult)
		return c_char_p(pyname.raw).value

	def getChannels(self):
		"""
		This function returns the number of supported sensor channels.
		
		Args:
		Returns:
			channelCount(uint16) : Number of supported sensor channels.
		"""
		pychannelCount = c_uint16(0)
		pInvokeResult = self.dll.TLPMX_getChannels(self.devSession, byref(pychannelCount))
		self.__testForError(pInvokeResult)
		return  pychannelCount.value

	def getSensorInfo(self, channel = 1):
		"""
		This function is used to obtain informations from the connected sensor like sensor name, serial number, calibration message, sensor type, sensor subtype and sensor flags.  
		
		Remark:
		The meanings of the obtained sensor type, subtype and flags are:
		
		Sensor Types:
		 SENSOR_TYPE_NONE               0x00 // No sensor
		 SENSOR_TYPE_PD_SINGLE          0x01 // Photodiode sensor
		 SENSOR_TYPE_THERMO             0x02 // Thermopile sensor
		 SENSOR_TYPE_PYRO               0x03 // Pyroelectric sensor
		
		Sensor Subtypes:
		 SENSOR_SUBTYPE_NONE            0x00 // No sensor
		 
		Sensor Subtypes Photodiode:
		 SENSOR_SUBTYPE_PD_ADAPTER      0x01 // Photodiode adapter
		 SENSOR_SUBTYPE_PD_SINGLE_STD   0x02 // Photodiode sensor
		 SENSOR_SUBTYPE_PD_SINGLE_FSR   0x03 // Photodiode sensor with 
		                                        integrated filter
		                                        identified by position 
		 SENSOR_SUBTYPE_PD_SINGLE_STD_T 0x12 // Photodiode sensor with
		                                        temperature sensor
		Sensor Subtypes Thermopile:
		 SENSOR_SUBTYPE_THERMO_ADAPTER  0x01 // Thermopile adapter
		 SENSOR_SUBTYPE_THERMO_STD      0x02 // Thermopile sensor
		 SENSOR_SUBTYPE_THERMO_STD_T    0x12 // Thermopile sensor with 
		                                        temperature sensor
		Sensor Subtypes Pyroelectric Sensor:
		 SENSOR_SUBTYPE_PYRO_ADAPTER    0x01 // Pyroelectric adapter
		 SENSOR_SUBTYPE_PYRO_STD        0x02 // Pyroelectric sensor
		 SENSOR_SUBTYPE_PYRO_STD_T      0x12 // Pyroelectric sensor with
		                                        temperature sensor
		Sensor Flags:
		 TLPM_SENS_FLAG_IS_POWER     0x0001 // Power sensor
		 TLPM_SENS_FLAG_IS_ENERGY    0x0002 // Energy sensor
		 TLPM_SENS_FLAG_IS_RESP_SET  0x0010 // Responsivity settable
		 TLPM_SENS_FLAG_IS_WAVEL_SET 0x0020 // Wavelength settable
		 TLPM_SENS_FLAG_IS_TAU_SET   0x0040 // Time constant settable
		 TLPM_SENS_FLAG_HAS_TEMP     0x0100 // With Temperature sensor 
		
		Args:
			
			
			
			Remark:
			The meanings of the obtained sensor type are:
			
			Sensor Types:
			 SENSOR_TYPE_NONE               0x00 // No sensor
			 SENSOR_TYPE_PD_SINGLE          0x01 // Photodiode sensor
			 SENSOR_TYPE_THERMO             0x02 // Thermopile sensor
			 SENSOR_TYPE_PYRO               0x03 // Pyroelectric sensor
			
			Remark:
			The meanings of the obtained sensor subtype are:
			
			Sensor Subtypes:
			 SENSOR_SUBTYPE_NONE            0x00 // No sensor
			 
			Sensor Subtypes Photodiode:
			 SENSOR_SUBTYPE_PD_ADAPTER      0x01 // Photodiode adapter
			 SENSOR_SUBTYPE_PD_SINGLE_STD   0x02 // Photodiode sensor
			 SENSOR_SUBTYPE_PD_SINGLE_FSR   0x03 // Photodiode sensor with 
			                                        integrated filter
			                                        identified by position 
			 SENSOR_SUBTYPE_PD_SINGLE_STD_T 0x12 // Photodiode sensor with
			                                        temperature sensor
			Sensor Subtypes Thermopile:
			 SENSOR_SUBTYPE_THERMO_ADAPTER  0x01 // Thermopile adapter
			 SENSOR_SUBTYPE_THERMO_STD      0x02 // Thermopile sensor
			 SENSOR_SUBTYPE_THERMO_STD_T    0x12 // Thermopile sensor with 
			                                        temperature sensor
			Sensor Subtypes Pyroelectric Sensor:
			 SENSOR_SUBTYPE_PYRO_ADAPTER    0x01 // Pyroelectric adapter
			 SENSOR_SUBTYPE_PYRO_STD        0x02 // Pyroelectric sensor
			 SENSOR_SUBTYPE_PYRO_STD_T      0x12 // Pyroelectric sensor with
			                                        temperature sensor
			
			Remark:
			The meanings of the obtained sensor flags are:
			
			Sensor Flags:
			 TLPM_SENS_FLAG_IS_POWER     0x0001 // Power sensor
			 TLPM_SENS_FLAG_IS_ENERGY    0x0002 // Energy sensor
			 TLPM_SENS_FLAG_IS_RESP_SET  0x0010 // Responsivity settable
			 TLPM_SENS_FLAG_IS_WAVEL_SET 0x0020 // Wavelength settable
			 TLPM_SENS_FLAG_IS_TAU_SET   0x0040 // Time constant settable
			 TLPM_SENS_FLAG_HAS_TEMP     0x0100 // With Temperature sensor
			channel(uint16) : Number of the sensor channel. 
			
			Default: 1 for non multi channel devices
		Returns:
			name(string) : This parameter returns the name of the connected sensor.
			snr(string) : This parameter returns the serial number of the connected sensor.
			message(string) : This parameter returns the calibration message of the connected sensor.
			pType(int16) : This parameter returns the sensor type of the connected sensor.
			pStype(int16) : This parameter returns the subtype of the connected sensor.
			pFlags(int16) : This parameter returns the flags of the connected sensor.
		"""
		pyname = create_string_buffer(1024)
		pysnr = create_string_buffer(1024)
		pymessage = create_string_buffer(1024)
		pypType = c_int16(0)
		pypStype = c_int16(0)
		pypFlags = c_int16(0)
		pInvokeResult = self.dll.TLPMX_getSensorInfo(self.devSession, pyname, pysnr, pymessage, byref(pypType), byref(pypStype), byref(pypFlags), c_uint16(channel))
		self.__testForError(pInvokeResult)
		return c_char_p(pyname.raw).value, c_char_p(pysnr.raw).value, c_char_p(pymessage.raw).value, pypType.value, pypStype.value, pypFlags.value

	def importSettingsFromJson(self, adapt):
		"""
		Use this function to import a previously stored parameter set again. The command will parse the JSON input and apply the parameter value. To export use the function exportSettingsAsJson. 
		It is possible to import parameters within a sensor family. For example you might import parameters exported for a photodiode when another photodiode is currenlty connected. 
		Use the adapt parameter to allow the command to change the parameters when out of range.
		When adaption is not allowed or input data is invalid for any other reason a SCPI error is enqueued. Use SYST:ERR? to check if import was successful.
		If JSON input string is longer than 240 chars the input data needs to be split into multiple calls of this command.The JSON fragment data is buffered and reassembled in the device memory.
		Once all data is transmited(detected by curly bracket counting) it gets parsed and executed.You can obmit any buffered input data by sending magic character #.
		
		Args:
			adapt(int16) : true to adapt parameters to ranges. False to generate error when out of range. 
			
		Returns:
			settings(string) :  device parameters as single line JSON format string. May be a substring of json line if larger 240 chars.
		"""
		pysettings = create_string_buffer(1024)
		pInvokeResult = self.dll.TLPMX_importSettingsFromJson(self.devSession, c_int16(adapt), pysettings)
		self.__testForError(pInvokeResult)
		return c_char_p(pysettings.raw).value

	def exportSettingsAsJson(self, settingsSize):
		"""
		Use this command to export the persistently stored device parameters as single line JSON string.
		Some parameters like zeroing are not exported as the value is not valid for future imports. Use importSettingsFromJson to import the parameter set again.
		
		
		Args:
			settingsSize(uint32) : Size of buffer used to get the parameters
		Returns:
			settings(string) : Device parameters as single line JSON string 
		"""
		pysettings = create_string_buffer(1024)
		pInvokeResult = self.dll.TLPMX_exportSettingsAsJson(self.devSession, pysettings, c_uint32(settingsSize))
		self.__testForError(pInvokeResult)
		return c_char_p(pysettings.raw).value

	def writeRaw(self, command):
		"""
		This function writes directly to the instrument.
		
		Args:
			command(char_p) : Null terminated command string to send to the instrument.
			
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_writeRaw(self.devSession, c_char_p(command.encode('utf-8')))
		self.__testForError(pInvokeResult)

	def readRaw(self, size):
		"""
		This function reads directly from the instrument.
		
		
		Args:
			
			Notes:
			(1) If received data is less than buffer size, the buffer is additionaly terminated with a '' character.
			(2) If received data is same as buffer size no '' character is appended. Its the caller's responsibility to make sure a buffer is '' terminated if the caller wants to interprete the buffer as string.
			size(uint32) : This parameter specifies the buffer size.
			
			
			Notes:
			(1) You may pass VI_NULL if you don't need this value.
			
		Returns:
			buffer(string) : Byte buffer that receives the data read from the instrument.
			returnCount(uint32) : Number of bytes actually transferred and filled into Buffer. This number doesn't count the additional termination '' character. If Return Count == size the buffer content will not be '' terminated.
		"""
		pybuffer = create_string_buffer(1024)
		pyreturnCount = c_uint32(0)
		pInvokeResult = self.dll.TLPMX_readRaw(self.devSession, pybuffer, c_uint32(size), byref(pyreturnCount))
		self.__testForError(pInvokeResult)
		return c_char_p(pybuffer.raw).value, pyreturnCount.value

	def setTimeoutValue(self, value):
		"""
		This function sets the interface communication timeout value.
		
		Args:
			value(uint32) : This parameter specifies the communication timeout value in ms.
			
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_setTimeoutValue(self.devSession, c_uint32(value))
		self.__testForError(pInvokeResult)

	def getTimeoutValue(self):
		"""
		This function gets the interface communication timeout value.
		
		
		Args:
			
		Returns:
			value(uint32) : This parameter returns the communication timeout value in ms.
		"""
		pyvalue = c_uint32(0)
		pInvokeResult = self.dll.TLPMX_getTimeoutValue(self.devSession, byref(pyvalue))
		self.__testForError(pInvokeResult)
		return  pyvalue.value

	def setIPAddress(self):
		"""
		Tell the instrument which ip address the device has to commuicate with.
		This value is stored inside the instrument. 
		
		
		
		Args:
			
		Returns:
			IPAddress(string) : This parameter specifies the baudrate in bits/sec.
		"""
		pyIPAddress = create_string_buffer(1024)
		pInvokeResult = self.dll.TLPMX_setIPAddress(self.devSession, pyIPAddress)
		self.__testForError(pInvokeResult)
		return c_char_p(pyIPAddress.raw).value

	def getIPAddress(self):
		"""
		Tell the instrument which ip address the device has to commuicate with.
		This value is stored inside the instrument. 
		
		
		
		Args:
			
		Returns:
			IPAddress(string) : This parameter specifies the baudrate in bits/sec.
		"""
		pyIPAddress = create_string_buffer(1024)
		pInvokeResult = self.dll.TLPMX_getIPAddress(self.devSession, pyIPAddress)
		self.__testForError(pInvokeResult)
		return c_char_p(pyIPAddress.raw).value

	def setIPMask(self):
		"""
		Use this command to change IPv4 netmask of device. If DHCP is enabled the function simply updates the static IPv4 netmask without applying configuration to the network interface. If DHCP is disabled the command also applies configuration to the network interface.
		
		
		
		Args:
			
		Returns:
			IPMask(string) : Pv4 netmask string. Bytes separated by fullstop.
		"""
		pyIPMask = create_string_buffer(1024)
		pInvokeResult = self.dll.TLPMX_setIPMask(self.devSession, pyIPMask)
		self.__testForError(pInvokeResult)
		return c_char_p(pyIPMask.raw).value

	def getIPMask(self):
		"""
		Use this command to query IPv4 netmask of device. If DHCP is enabled and no IP has been assigned yet the result might be "0.0.0.0". If DHCP is disabled the static IPv4 netmask will be returned.
		
		
		
		Args:
			
		Returns:
			IPMask(string) : IPv4 netmask string. Bytes separated by fullstop.
		"""
		pyIPMask = create_string_buffer(1024)
		pInvokeResult = self.dll.TLPMX_getIPMask(self.devSession, pyIPMask)
		self.__testForError(pInvokeResult)
		return c_char_p(pyIPMask.raw).value

	def getMACAddress(self):
		"""
		Tell the instrument which ip address the device has to commuicate with.
		This value is stored inside the instrument. 
		
		
		
		Args:
			
		Returns:
			MACAddress(string) : This parameter specifies the baudrate in bits/sec.
		"""
		pyMACAddress = create_string_buffer(1024)
		pInvokeResult = self.dll.TLPMX_getMACAddress(self.devSession, pyMACAddress)
		self.__testForError(pInvokeResult)
		return c_char_p(pyMACAddress.raw).value

	def setDHCP(self):
		"""
		Tell the instrument which ip address the device has to commuicate with.
		This value is stored inside the instrument. 
		
		
		
		Args:
			
		Returns:
			DHCP(string) : This parameter specifies the baudrate in bits/sec.
		"""
		pyDHCP = create_string_buffer(1024)
		pInvokeResult = self.dll.TLPMX_setDHCP(self.devSession, pyDHCP)
		self.__testForError(pInvokeResult)
		return c_char_p(pyDHCP.raw).value

	def getDHCP(self):
		"""
		Tell the instrument which ip address the device has to commuicate with.
		This value is stored inside the instrument. 
		
		
		
		Args:
			
		Returns:
			DHCP(string) : This parameter specifies the baudrate in bits/sec.
		"""
		pyDHCP = create_string_buffer(1024)
		pInvokeResult = self.dll.TLPMX_getDHCP(self.devSession, pyDHCP)
		self.__testForError(pInvokeResult)
		return c_char_p(pyDHCP.raw).value

	def setHostname(self):
		"""
		Tell the instrument which ip address the device has to commuicate with.
		This value is stored inside the instrument. 
		
		
		
		Args:
			
		Returns:
			hostname(string) : This parameter specifies the baudrate in bits/sec.
		"""
		pyhostname = create_string_buffer(1024)
		pInvokeResult = self.dll.TLPMX_setHostname(self.devSession, pyhostname)
		self.__testForError(pInvokeResult)
		return c_char_p(pyhostname.raw).value

	def getHostname(self):
		"""
		Tell the instrument which ip address the device has to commuicate with.
		This value is stored inside the instrument. 
		
		
		
		Args:
			
		Returns:
			hostname(string) : This parameter specifies the baudrate in bits/sec.
		"""
		pyhostname = create_string_buffer(1024)
		pInvokeResult = self.dll.TLPMX_getHostname(self.devSession, pyhostname)
		self.__testForError(pInvokeResult)
		return c_char_p(pyhostname.raw).value

	def setWebPort(self, port):
		"""
		Tell the instrument which ip address the device has to commuicate with.
		This value is stored inside the instrument. 
		
		
		
		Args:
			port(uint32) : This parameter specifies the baudrate in bits/sec.
			
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_setWebPort(self.devSession, c_uint32(port))
		self.__testForError(pInvokeResult)

	def getWebPort(self):
		"""
		Tell the instrument which ip address the device has to commuicate with.
		This value is stored inside the instrument. 
		
		
		
		Args:
			
		Returns:
			port(uint32) : This parameter specifies the baudrate in bits/sec.
		"""
		pyport = c_uint32(0)
		pInvokeResult = self.dll.TLPMX_getWebPort(self.devSession, byref(pyport))
		self.__testForError(pInvokeResult)
		return  pyport.value

	def setSCPIPort(self, port):
		"""
		Tell the instrument which ip address the device has to commuicate with.
		This value is stored inside the instrument. 
		
		
		
		Args:
			port(uint32) : This parameter specifies the baudrate in bits/sec.
			
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_setSCPIPort(self.devSession, c_uint32(port))
		self.__testForError(pInvokeResult)

	def getSCPIPort(self):
		"""
		Tell the instrument which ip address the device has to commuicate with.
		This value is stored inside the instrument. 
		
		
		
		Args:
			
		Returns:
			port(uint32) : This parameter specifies the baudrate in bits/sec.
		"""
		pyport = c_uint32(0)
		pInvokeResult = self.dll.TLPMX_getSCPIPort(self.devSession, byref(pyport))
		self.__testForError(pInvokeResult)
		return  pyport.value

	def setDFUPort(self, port):
		"""
		Tell the instrument which ip address the device has to commuicate with.
		This value is stored inside the instrument. 
		
		
		
		Args:
			port(uint32) : This parameter specifies the baudrate in bits/sec.
			
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_setDFUPort(self.devSession, c_uint32(port))
		self.__testForError(pInvokeResult)

	def getDFUPort(self):
		"""
		Tell the instrument which ip address the device has to commuicate with.
		This value is stored inside the instrument. 
		
		
		
		Args:
			
		Returns:
			port(uint32) : This parameter specifies the baudrate in bits/sec.
		"""
		pyport = c_uint32(0)
		pInvokeResult = self.dll.TLPMX_getDFUPort(self.devSession, byref(pyport))
		self.__testForError(pInvokeResult)
		return  pyport.value

	def setEncryption(self, oldPassword, newPassword, encryption):
		"""
		Overwrites the system password used for authentication, Default password ist THORlabs
		
		
		
		Args:
			oldPassword(char_p) : old ASCII passwort string. Max length is 25. Min length is 5
			
			newPassword(char_p) : new ASCII passwort string. Max length is 25. Min length is 5
			
			encryption(int16) : True if SCPI LAN interface should be crypted
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_setEncryption(self.devSession, c_char_p(oldPassword.encode('utf-8')), c_char_p(newPassword.encode('utf-8')), c_int16(encryption))
		self.__testForError(pInvokeResult)

	def getEncryption(self):
		"""
		Queries password used for authentication. Default password ist THORlabs. Only supported by local serial interface.
		
		
		Args:
			
		Returns:
			password(string) : used password
			encryption(int16) : True if SCPI LAN interface should be crypted
		"""
		pypassword = create_string_buffer(1024)
		pyencryption = c_int16(0)
		pInvokeResult = self.dll.TLPMX_getEncryption(self.devSession, pypassword, byref(pyencryption))
		self.__testForError(pInvokeResult)
		return c_char_p(pypassword.raw).value, pyencryption.value

	def setLANPropagation(self, enable):
		"""
		Use this command to enable/disable LAN service propagation via UDP broadcast on port 270378. The broadcast is send as heatbeat every 800ms.
		
		
		
		Args:
			enable(int16) : 1 to enable service propagation. False to disable
			
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_setLANPropagation(self.devSession, c_int16(enable))
		self.__testForError(pInvokeResult)

	def getLANPropagation(self):
		"""
		Use this command to test if LAN service propagation via UDP broadcast on port 270378 is active. The broadcast is send as heatbeat every 800ms.
		
		
		
		Args:
			
		Returns:
			enable(int16) : 1 to enable service propagation. False to disable
		"""
		pyenable = c_int16(0)
		pInvokeResult = self.dll.TLPMX_getLANPropagation(self.devSession, byref(pyenable))
		self.__testForError(pInvokeResult)
		return  pyenable.value

	def setEnableNetSearch(self, enable):
		"""
		Enables the ethernet devices search for the actual instance.
		
		
		
		
		Args:
			enable(int16)
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_setEnableNetSearch(self.devSession, c_int16(enable))
		self.__testForError(pInvokeResult)

	def getEnableNetSearch(self):
		"""
		Disables the ethernet devices search for the actual instance.
		
		
		
		Args:
		Returns:
			enable(int16)
		"""
		pyenable = c_int16(0)
		pInvokeResult = self.dll.TLPMX_getEnableNetSearch(self.devSession, byref(pyenable))
		self.__testForError(pInvokeResult)
		return  pyenable.value

	def setLookForInfoOnSearch(self, enable):
		"""
		Enables or disables the posibility to get information on TLPMX_findRsrc.
		If this is set to false the method TLPMX_getRsrcInfo will not retrive any information after TLPMX_findRsrc.
		
		
		
		
		Args:
			enable(int16) : Enables or disables the posibility to get information on TLPMX_findRsrc.
			If this is set to false the method TLPMX_getRsrcInfo will not retrive any information after TLPMX_findRsrc.
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_setLookForInfoOnSearch(self.devSession, c_int16(enable))
		self.__testForError(pInvokeResult)

	def getLookForInfoOnSearch(self):
		"""
		Get if the posibility to get information on TLPMX_findRsrc is enabled.
		If this is set to false the method TLPMX_getRsrcInfo will not retrive any information after TLPMX_findRsrc.
		
		
		Args:
			If this is set to false the method TLPMX_getRsrcInfo will not retrive any information after TLPMX_findRsrc.
		Returns:
			enable(int16) : Get if the posibility to get information on TLPMX_findRsrc is enabled.
		"""
		pyenable = c_int16(0)
		pInvokeResult = self.dll.TLPMX_getLookForInfoOnSearch(self.devSession, byref(pyenable))
		self.__testForError(pInvokeResult)
		return  pyenable.value

	def setNetSearchMask(self, netMask):
		"""
		Sets the default network mask for search ethernet devices on the computer.
		
		
		
		Args:
			netMask(char_p) : The default net mask on the computer for network search.
			
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_setNetSearchMask(self.devSession, c_char_p(netMask.encode('utf-8')))
		self.__testForError(pInvokeResult)

	def setEnableBthSearch(self, enable):
		"""
		Enables the bluetooth devices search for the actual instance.
		
		
		
		
		Args:
			enable(int16)
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_setEnableBthSearch(self.devSession, c_int16(enable))
		self.__testForError(pInvokeResult)

	def getEnableBthSearch(self):
		"""
		Disables the bluetooth devices search for the actual instance.
		
		
		
		Args:
		Returns:
			enable(int16)
		"""
		pyenable = c_int16(0)
		pInvokeResult = self.dll.TLPMX_getEnableBthSearch(self.devSession, byref(pyenable))
		self.__testForError(pInvokeResult)
		return  pyenable.value

	def setDeviceBaudrate(self, baudrate):
		"""
		Tell the instrument which baudrate has to be used for the serial communication.
		This value is stored inside the instrument. 
		
		If the RS232 interface is currently used for the communication, call the function setDriverBaudrate to adapt to the new baudrate.
		
		Args:
			baudrate(uint32) : This parameter specifies the baudrate in bits/sec.
			
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_setDeviceBaudrate(self.devSession, c_uint32(baudrate))
		self.__testForError(pInvokeResult)

	def getDeviceBaudrate(self):
		"""
		This function returns the baudrate that is used for the serial communication inside the instrument
		
		
		Args:
			
		Returns:
			baudrate(uint32) : This parameter returns the baudrate in bist/sec.
		"""
		pybaudrate = c_uint32(0)
		pInvokeResult = self.dll.TLPMX_getDeviceBaudrate(self.devSession, byref(pybaudrate))
		self.__testForError(pInvokeResult)
		return  pybaudrate.value

	def setDriverBaudrate(self, baudrate):
		"""
		This function sets the baudrate for the serial interface on the PC side
		
		Args:
			baudrate(uint32) : This parameter specifies the baudrate in bits/sec.
			
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_setDriverBaudrate(self.devSession, c_uint32(baudrate))
		self.__testForError(pInvokeResult)

	def getDriverBaudrate(self):
		"""
		This function returns the baudrate that is used for the serial communication on the PC side
		
		
		Args:
			
		Returns:
			baudrate(uint32) : This parameter returns the baudrate in bist/sec.
		"""
		pybaudrate = c_uint32(0)
		pInvokeResult = self.dll.TLPMX_getDriverBaudrate(self.devSession, byref(pybaudrate))
		self.__testForError(pInvokeResult)
		return  pybaudrate.value

	def listDirectory(self, path, offset):
		"""
		Browses flash file system content
		
		Notes:
		(1) The function is only available on PM6x.
		
		
		Args:
			path(char_p) : path of folder to list. Has to end with wildcard.
			offset(uint32) :  offset to list content. 0 for start.
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_listDirectory(self.devSession, c_char_p(path.encode('utf-8')), c_uint32(offset))
		self.__testForError(pInvokeResult)

	def fileOpen(self, path):
		"""
		Openes a file from flash file system for reading
		
		Notes:
		(1) The function is only available on PM6x.
		
		
		Args:
			path(char_p) :  path of file to open
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_fileOpen(self.devSession, c_char_p(path.encode('utf-8')))
		self.__testForError(pInvokeResult)

	def fileRead(self, offset, length, asHex):
		"""
		Reads block out of flash file system file
		
		Notes:
		(1) The function is only available on PM6x.
		
		
		Args:
			offset(uint32) : offset in file where to start reading. 0 for start.
			length(uint32)
			asHex(int16) :  Optional! 1 to return file content as hex string. Use 0 for binary files. Use 1 for text files (Default)
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_fileRead(self.devSession, c_uint32(offset), c_uint32(length), c_int16(asHex))
		self.__testForError(pInvokeResult)

	def fileClose(self):
		"""
		Call this method initially to open a file from device flash memory for reading via remote interface. It is the first command of the sequence SYST:FILE:OPEN?, SYST:FILE:READ? and SYST:FILE:CLOSE. Only one file can be opened for reading at the same time. If the memory is currely mounted to USB interface this method will result in an error.Binary and text files can be opened for reading.
		
		Notes:
		(1) The function is only available on PM6x.
		
		"""
		pInvokeResult = self.dll.TLPMX_fileClose(self.devSession)
		self.__testForError(pInvokeResult)

	def deviceParamsImport(self, adapt, JSONData):
		"""
		Use this command to import a previously stored parameter set again. The command will parse the JSON input and apply the parameter value. To export parameter set use SYST:PARA:EXPO:JSON?. It is possible to import parameters within a sensor family. For example you might import parameters exported for a photodiode when another photodiode is currenlty connected. Use the adapt parameter to allow the command to change the parameters when out of range. When adaption is not allowed or input data is invalid for any other reason a SCPI error is enqueued. Use SYST:ERR? to check if import was successful.
		If JSON input string is longer than 240 chars the input data needs to be split into multiple calls of this command. The JSON fragment data is buffered and reassembled in the device memory. Once all data is transmited (detected by curly bracket counting) it gets parsed and executed. You can obmit any buffered input data by sending magic character #. 
		
		Notes:
		(1) The function is only available on PM6x, PM103, PM5020.
		
		
		Args:
			adapt(int16) : true to adapt parameters to ranges. False to generate error when out of range.
			JSONData(char_p) :  device parameters as single line JSON format string. May be a substring of json line if larger 240 chars.
		Returns:
		"""
		pInvokeResult = self.dll.TLPMX_deviceParamsImport(self.devSession, c_int16(adapt), c_char_p(JSONData.encode('utf-8')))
		self.__testForError(pInvokeResult)

	def deviceParamsExport(self):
		"""
		Use this command to export the persistently stored device parameters as single line JSON string. Some parameters like zeroing are not exported as the value is not valid for future imports. Use SYST:PARA:IMPO:JSON to import the parameter set again.
		
		Notes:
		(1) The function is only available on PM6x, PM103, PM5020.
		
		
		Args:
		Returns:
			JSONData(string) : device parameters as single line JSON string.
		"""
		pyJSONData = create_string_buffer(1024)
		pInvokeResult = self.dll.TLPMX_deviceParamsExport(self.devSession, pyJSONData)
		self.__testForError(pInvokeResult)
		return c_char_p(pyJSONData.raw).value


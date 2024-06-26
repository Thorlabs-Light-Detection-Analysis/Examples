
namespace PM101R_Serial_Communication_1
{
    using System;
    using System.Collections.Generic;
    using System.IO.Ports;
    using System.Runtime.InteropServices;
    using System.Text;
    using Thorlabs.TLPMX_32.Interop;

    class Program
    {
        /*
         * This sample uses the Thorlabs.TLPM_32.Interop.dll and the TLPM_32.dll for the serial communication.
         * So it is possible to communicate with the power meter without knowing the SCPI-commands. 
         * https://www.thorlabs.com/drawings/72bbc865da9caf75-4668AE64-0027-B19B-CE8F2C2366F4CBAA/PM101R-WriteYourOwnApplication.pdf
         * */

        [StructLayout(LayoutKind.Sequential)]
        public struct COMMPROP
        {
            short wPacketLength;
            short wPacketVersion;
            int dwServiceMask;
            int dwReserved1;
            int dwMaxTxQueue;
            int dwMaxRxQueue;
            int dwMaxBaud;
            int dwProvSubType;
            int dwProvCapabilities;
            int dwSettableParams;
            public int dwSettableBaud;
            short wSettableData;
            short wSettableStopParity;
            int dwCurrentTxQueue;
            int dwCurrentRxQueue;
            int dwProvSpec1;
            int dwProvSpec2;
            string wcProvChar;
        }

        [DllImport("kernel32.dll")]
        static extern bool CloseHandle(IntPtr hFile);
        [DllImport("kernel32.dll")]
        static extern bool GetCommProperties(IntPtr hFile, ref COMMPROP lpCommProp);
        [DllImport("kernel32.dll", CharSet = CharSet.Auto, SetLastError = true)]
        static extern IntPtr CreateFile(string lpFileName, int dwDesiredAccess,
                   int dwShareMode, IntPtr securityAttrs, int dwCreationDisposition,
                   int dwFlagsAndAttributes, IntPtr hTemplateFile);

        static Dictionary<string, uint> BaudRates = new Dictionary<string, uint>()
        {
            { "75 bps" , 0x00000001 },
            { "110 bps", 0x00000002 },
            { "134.5 bps", 0x00000004},
            { "150 bps" , 0x00000008},
            { "300 bps" , 0x00000010},
            { "600 bps" , 0x00000020},
            { "1200 bps" , 0x00000040},
            { "1800 bps" , 0x00000080},
            { "2400 bps" , 0x00000100},
            { "4800 bps" , 0x00000200},
            { "7200 bps" , 0x00000400},
            { "9600 bps" , 0x00000800},
            { "14400 bps" , 0x00001000},
            { "19200 bps" , 0x00002000},
            { "38400 bps" , 0x00004000},
            { "56K bps" , 0x00008000},
            { "57600 bps" , 0x00040000},
            { "115200 bps" , 0x00020000},
            { "128K bps" , 0x00010000}
        };

        static void Main(string[] args)
        { 
            string[] ps = null;

            try
            {
                ps = SerialPort.GetPortNames();
            }
            catch (Exception ePort)
            {
                Console.WriteLine("Error on getting serial ports: " + ePort.Message);
                return;
            }

            string selectedPort = string.Empty;
              
            if(ps.Length > 0)
            {
                selectedPort = ps[0];

                Console.WriteLine("The first serial port found is selected: " + selectedPort);
                Console.WriteLine("");

                COMMPROP commProp = new COMMPROP();
                IntPtr hFile = CreateFile(@"\\.\" + selectedPort, 0, 0, IntPtr.Zero, 3, 0x80, IntPtr.Zero);
                GetCommProperties(hFile, ref commProp);
                CloseHandle(hFile);

                int availableBautRates = commProp.dwSettableBaud;

                Console.WriteLine("Available baud rates for port " + selectedPort + ":");
                foreach (var item in BaudRates)
                {
                    if ((item.Value & availableBautRates) > 0)
                    {
                        Console.WriteLine("Baud rate: " + item.Key);
                    }
                }

                Console.WriteLine("");
                Console.WriteLine("Important: Baud rates under 9600Bit/s and over 256000 Bit/s are not supported by the device.");
                Console.WriteLine("");

                TLPMX device = null;
                //If the baudrate is wrong, you wont be able to open the port. Be carefull when you change the baudrate on the device.
                int baudrate = 115200;

                try
                {
                    //always use true for ID Query
                    device = new TLPMX(selectedPort + "::" + baudrate, true, false);
                    Console.WriteLine("Open Device");

                    StringBuilder sensorName = new StringBuilder(1024);
                    StringBuilder sensorSerialnumber = new StringBuilder(1024);
                    StringBuilder sensorCalibration = new StringBuilder(1024);
                    short sensortype;
                    short sensorSubtype;
                    short sensorFlags;
                    device.getSensorInfo(sensorName, sensorSerialnumber, sensorCalibration, out sensortype, out sensorSubtype, out sensorFlags, TLPMConstants.Default_Channel);
                    Console.WriteLine("Sensor name: " + sensorName.ToString());
                    Console.WriteLine("Sensor serial number: " + sensorSerialnumber.ToString());
                    Console.WriteLine("Sensor calibration: " + sensorCalibration.ToString());
                    Console.WriteLine("");

                    Console.WriteLine("Read power 10 times");

                    int count = 10;
                    for(int i = 0; i < count; i++)
                    {
                        double power;
                        device.measPower(out power, TLPMConstants.Default_Channel);
                        Console.WriteLine("{0}. Power: {1} W" , (i + 1), power.ToString("G5"));
                    }

                    Console.WriteLine("");
                    Console.WriteLine("Changing the baudrate....");

                    //Changing baudrate
                    //Options: 9600, 14400, 19200, 22800, 33600, 38400, 57600, 115200, 128000, 230400} only if the serial port supports this baud rates too.
                    int newBaudRate = 115200;
                    device.writeRaw("SYST:SER:TRAN:BAUD " + newBaudRate.ToString());

                    //Changing the baudrate needs to close and reopen the port with the correct baudrate
                    device.Dispose();
                    Console.WriteLine("Closing connection...");

                    device = new TLPMX(selectedPort + "::" + newBaudRate, true, false);
                    Console.WriteLine("Serial port reopen with the new baudrate {0}.", newBaudRate);

                    device.getSensorInfo(sensorName, sensorSerialnumber, sensorCalibration, out sensortype, out sensorSubtype, out sensorFlags, TLPMConstants.Default_Channel);
                    Console.WriteLine("Sensor name: " + sensorName.ToString());
                    Console.WriteLine("Sensor serial number: " + sensorSerialnumber.ToString());
                    Console.WriteLine("Sensor calibration: " + sensorCalibration.ToString());
                    Console.WriteLine("");
                }
                catch(Exception e)
                {
                    Console.WriteLine("Error on communication with the power meter: " + e.Message);
                }
                finally
                {
                    //device?.Dispose();
                    if (null != device)
                        device.Dispose();
                }
            } 
        }
    }
}

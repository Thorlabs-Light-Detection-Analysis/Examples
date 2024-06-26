
namespace PM101R_Serial_Communication_2
{
    using System;
    using System.Collections.Generic;
    using System.IO.Ports;
    using System.Runtime.InteropServices;

    class Program
    {
        /*
        * This sample uses only C# for the serial communication and no extern libraries
        * For the communication we need the SCPI-commands. 
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
            const string terminationsequence = "\n";

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

            if (ps.Length > 0) 
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
                foreach(var item in BaudRates)
                {
                    if((item.Value & availableBautRates) > 0)
                    {
                        Console.WriteLine("Baud rate: " + item.Key);
                    }
                }
                 
                Console.WriteLine("");
                Console.WriteLine("Important: Baud rates under 9600Bit/s and over 256000 Bit/s are not supported by the device.");
                Console.WriteLine("");

                SerialPort port = null;

                try
                {
                    port = new SerialPort
                    {
                        PortName = selectedPort,
                        BaudRate = 115200, //<--- If the baudrate is wrong, you wont be able to open the port. Be carefull when you change the baudrate on the device.
                        Parity = Parity.None,
                        DataBits = 8,
                        StopBits = StopBits.One,
                        Handshake = Handshake.None,
                        ReadTimeout = 3000,
                        WriteTimeout = 3000,
                        ReadBufferSize = 409600,
                        NewLine = terminationsequence
                    };

                    port.Open();

                    port.DiscardInBuffer();
                    port.DiscardOutBuffer();

                    //Get power meter information
                    ReadData(port, "*IDN?", "Power meter information: {0}");

                    //Get power meter calibration info
                    ReadData(port, "CAL:STR?","Power meter calibration: {0}");

                    //Get sensor information
                    ReadData(port, "SYSTem:SENSor:IDN?", "Sensor information: {0}");

                    //Get power meter serial communication baud rate
                    ReadData(port, "SYST:SER:TRAN:BAUD?", "Baudrate: {0}");

                    //Get error information
                    ReadData(port, "SYST:ERR?", "{0}");

                    Console.WriteLine("");

                    Console.WriteLine("Read power 10 times");

                    int count = 10;
                    for (int i = 0; i < count; i++)
                    {
                        ReadData(port, "MEAS:POW?", (i+1).ToString() + ". {0} W");
                    }

                    Console.WriteLine("");
                    Console.WriteLine("Changing the baudrate....");

                    //Changing baudrate
                    //Options: 9600, 14400, 19200, 22800, 33600, 38400, 57600, 115200, 128000, 230400} only if the serial port supports this baud rates too.
                    int newBaudRate = 115200;
                    port.WriteLine("SYST:SER:TRAN:BAUD " + newBaudRate.ToString());

                    //Changing the baudrate needs to close and reopen the port with the correct baudrate
                    port.Close();
                    Console.WriteLine("Closing connection...");

                    port = new SerialPort
                    {
                        PortName = selectedPort,
                        BaudRate = newBaudRate,
                        Parity = Parity.None,
                        DataBits = 8,
                        StopBits = StopBits.One,
                        Handshake = Handshake.None,
                        ReadTimeout = 1000,
                        WriteTimeout = 1000,
                        ReadBufferSize = 2048,
                        NewLine = terminationsequence
                    };
                
                    port.Open();
                    Console.WriteLine("Serial port reopen with the new baudrate {0}.", newBaudRate);

                    port.DiscardInBuffer();
                    port.DiscardOutBuffer();

                    //Get power meter information
                    ReadData(port, "*IDN?", "Power meter information: {0}");
                }
                catch (Exception e)
                {
                    Console.WriteLine("Error on communication with the power meter: " + e.Message);
                }
                finally
                {
                    if (null != port)
                        port.Close();

                    //port?.Close();
                }
            }
        }

        static void ReadData(SerialPort port, string command, string outmessage)
        {
            port.WriteLine(command);
            string answer = port.ReadLine();
            Console.WriteLine(outmessage, answer);
        }
    }
}

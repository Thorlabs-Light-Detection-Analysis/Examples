
namespace PM5020_I2C_Control
{
    using System;
    using System.Runtime.InteropServices;
    using System.Text;
    using Thorlabs.TLPMX_32.Interop;

    internal class Program
    {
        //Sample for Sensor HDC1080

        // Standard address of the HDC sensor: hex number
        static uint HDC_ADDR = 128;

        // Registers storing temperature and humidity (see data sheet):
        static string TMP_REG = "00";
        static string HUM_REG = "01";

        static void Main(string[] args)
        {
            TLPMX device = Init();

            if (device == null) return;

            //set mode to SLOW to start measurement.
            device.setI2CMode(1);

            LogData(device);

            //IMPORTANT: set mode to INTER again. This enables the power meter to use the I2C sensor again.
            device.setI2CMode(0);

            if (null != device)
                device.Dispose(); 
        }

        static TLPMX Init()
        {
            HandleRef Instrument_Handle = new HandleRef();

            TLPMX searchDevice = new TLPMX(Instrument_Handle.Handle);

            uint count = 0;

            string firstPowermeterFound = "";

            try
            {
                int pInvokeResult = searchDevice.findRsrc(out count);

                if (count > 0)
                {
                    StringBuilder descr = new StringBuilder(1024);

                    searchDevice.getRsrcName(0, descr);

                    firstPowermeterFound = descr.ToString();
                }
            }
            catch { }

            if (count == 0)
            {
                searchDevice.Dispose();
                Console.WriteLine("No power meter could be found.");
                return null;
            }

            //always use true for ID Query
            TLPMX device = new TLPMX(firstPowermeterFound, true, false);  //  For valid Ressource_Name see NI-Visa documentation.

            return device;

        }

        static double GetTemperature(TLPMX device)
        {
            // Point to temperature register:
            device.I2CWrite(HDC_ADDR, TMP_REG);

            // Hold on (conversion time, data sheet):
            System.Threading.Thread.Sleep(63);

            // Read two bytes:
            uint tmp_bytes; 
            device.I2CRead(HDC_ADDR, 2, out tmp_bytes);
            double tmp_deg_c = (tmp_bytes / Math.Pow(2,16)) * 165 - 40;
            return (tmp_deg_c); 
        }

        static double GetHumidity(TLPMX device)
        {
            // Point to humidity register:
            device.I2CWrite(HDC_ADDR, HUM_REG);

            // Hold on (conversion time, data sheet):
            System.Threading.Thread.Sleep(65);

            // Read two bytes:
            uint tmp_bytes;
            device.I2CRead(HDC_ADDR, 2, out tmp_bytes);
            double tmp_deg_c = (tmp_bytes / Math.Pow(2, 16)) * 100;
            return (tmp_deg_c);
        }

        static void LogData(TLPMX device)
        {
            int counter = 0;

            while(counter < 10)
            {
                double tmp_deg_c = GetTemperature(device);
                double hum_p_rel = GetHumidity(device);

                Console.WriteLine("{0:F2} °C", tmp_deg_c);
                Console.WriteLine("{0:F2} percent rel. humidity", hum_p_rel);

                System.Threading.Thread.Sleep(1000);

                counter++; 
            }
        }
    }
}

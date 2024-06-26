
namespace PM103_Peak_Search_Sample
{
    using System;
    using System.Runtime.InteropServices;
    using System.Text;
    using Thorlabs.TLPMX_32.Interop;

    class Program
    {
        static void Main(string[] args)
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
                return;
            }

            //always use true for ID Query
            TLPMX device = new TLPMX(firstPowermeterFound, true, false);  //  For valid Ressource_Name see NI-Visa documentation.

            //Set to PEAK mode for peak measurement
            device.setFreqMode(1, TLPMConstants.Default_Channel);
             
            device.writeRaw("ABORT");
            device.writeRaw("CONF:CURR"); 
            device.writeRaw("INIT");

            //Start autoset
            autoset(device);
             
            StringBuilder response = new StringBuilder(256);
             
            for(int i = 0; i < 10; i++)
            {
                short regValue;
                device.readRegister(4, out regValue);

                if ((regValue & 512) != 0)
                {
                    device.writeRaw("FETC?");

                    uint returnCount;
                    device.readRaw(response, 256, out returnCount);

                    Console.WriteLine("Current [A]: " + response.ToString());

                    device.writeRaw("ABORT");
                    device.writeRaw("INIT");
                }

                System.Threading.Thread.Sleep(500);
            }

            //Set to CW mode for normal measurement
            device.setFreqMode(0, TLPMConstants.Default_Channel);

            //device?.Dispose();
            if (null != device)
                device.Dispose();            

            Console.ReadKey();
        }

        private static void autoset(TLPMX device)
        {
            device.startPeakDetector(TLPMConstants.Default_Channel);
            System.Threading.Thread.Sleep(1000);

            bool isRunning = true;

            while(isRunning)
            {
                device.isPeakDetectorRunning(out isRunning, TLPMConstants.Default_Channel);
            }
        }
    }
}


namespace PM103_100kS_per_second_Sample
{
    using System;
    using System.Collections.Generic;
    using System.Diagnostics;
    using System.Globalization;
    using System.IO;
    using System.Reflection;
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

            device.resetFastArrayMeasurement(TLPMConstants.Default_Channel);

            device.confCurrentFastArrayMeasurement(TLPMConstants.Default_Channel);

            Stopwatch wachtTime = new Stopwatch(); 
            wachtTime.Start();

            int arraySize = 200;
            uint[] timeStamps = new uint[arraySize]; // time stamps in microseconds.
            float[] values = new float[arraySize];   // current data in A

            List<uint> measuredTimeStamps = new List<uint>();
            List<float> measuredValues = new List<float>();

            while (wachtTime.Elapsed.TotalSeconds < 3)
            {
                uint dataSize = 0;
                device.getNextFastArrayMeasurement(out dataSize, timeStamps, values, TLPMConstants.Default_Channel);

                for (int i = 0; i < dataSize; i++)
                {
                    measuredTimeStamps.Add(timeStamps[i]);
                    measuredValues.Add(values[i]);
                }
            }

            string directory = Path.GetDirectoryName(Assembly.GetExecutingAssembly().Location);

            string delimiter = ";";

            string path = directory + "//CurrentData.csv";

            using (StreamWriter outStream = new StreamWriter(path, false, Encoding.UTF8))
            {
                for (int i = 0; i < measuredTimeStamps.Count; i++)
                {
                    CultureInfo cultInfo = CultureInfo.InstalledUICulture;
                    outStream.WriteLine(measuredTimeStamps[i].ToString("F3", cultInfo) + delimiter + measuredValues[i].ToString("G5", cultInfo));
                }
            }

            Console.WriteLine("Measurement current data at 100kS/s:");
            Console.WriteLine(path);

            if (File.Exists(path))
            {
                try
                {
                   Process.Start(path);
                }
                catch { }
            }

            //device?.Dispose();
            if (null != device)
                device.Dispose();            

            Console.ReadKey();
        }
    }
}

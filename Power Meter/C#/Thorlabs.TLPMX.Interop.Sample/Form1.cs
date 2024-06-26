namespace Thorlabs.TLPM_32.Interop.Sample
{
    using System;
    using System.Runtime.InteropServices;
    using System.Text;
    using System.Windows.Forms;
    using Thorlabs.TLPMX_32.Interop;

    /// <summary>
    /// GUI with a TLPMX sample
    /// </summary>
    public partial class Form1 : Form
    {
        private TLPMX tlpm;

        /// <summary>
        /// Inisialize the GUI
        /// </summary>
        public Form1()
        {
            InitializeComponent();

            try
            {
                HandleRef Instrument_Handle = new HandleRef();

                TLPMX searchDevice = new TLPMX(Instrument_Handle.Handle);

                uint count = 0;

                string firstPowermeterFound = "";

                try
                {
                    int pInvokeResult = searchDevice.findRsrc(out count);

                    if(count > 0)
                    {
                        StringBuilder descr = new StringBuilder(1024);

                        searchDevice.getRsrcName(0, descr);

                        firstPowermeterFound = descr.ToString();
                    }
                }
                catch { }

                if(count == 0)
                {
                    searchDevice.Dispose();
                    labelPower.Text = "No power meter could be found.";
                    return;
                }

                //always use true for ID Query
                tlpm = new TLPMX(firstPowermeterFound, true, false);  //  For valid Ressource_Name see NI-Visa documentation.
                double powerValue;
                int err = tlpm.measPower(out powerValue, TLPMConstants.Default_Channel);
                labelPower.Text = powerValue.ToString();
            }
            catch (BadImageFormatException bie)
            {
                labelPower.Text = bie.Message;
            }
            catch (NullReferenceException nre)
            {
                labelPower.Text = nre.Message;
            }
            catch (ExternalException ex)
            {
                labelPower.Text = ex.Message;
            }
            finally
            {
                if(tlpm != null)
                    tlpm.Dispose();
            }
        }
    }
}

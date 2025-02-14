This is the RoGeorge fork of python-ivi <- from nicedwarf/python-ivi <- from alexforencich/python-ivi <- from python-ivi/python-ivi

- Needed it for its included drivers supporting Rigol instruments, particularly looking at the DS1000Z, DG4000 and the DP800 series (DS1104Z, DG4202, DP832A), because their corresponding drivers from alexforencich/python-ivi were absent or not working, i.e. the DS1000Z drivers not working for meas:item type of commands (2022).  
- There were 108 forks of python-ivi before creating this 109'th one, while the main python-ivi was not updated for many years now.
- Another reason is the attempt to add (partial) support for Rigol DG4000 series of Function/Arbitrary Waveform Generators (AWG).  For now, some basic commands are working already (e.g. setting the frequency) if a DG4202 AWG is connected as a MSO1074Z MSO.

## Installation of Python-IVI from the RoGeorge/python-ivi fork

    pip install python-vxi11
    pip install pyvisa
    pip install pyvisa-py
    
    mkdir python-ivi_RoGeorge_fork && cd python-ivi_RoGeorge_fork
    git clone https://github.com/RoGeorge/python-ivi.git
    cd python-ivi
    pip install -e .

\
----------------
To uninstall it:

    pip uninstall python-ivi
\
\
\
----------------

# Python IVI Readme

For more information and updates:
http://alexforencich.com/wiki/en/python-ivi/start

GitHub repository:
https://github.com/python-ivi/python-ivi

Google group:
https://groups.google.com/d/forum/python-ivi

## Introduction

Python IVI is a Python-based interpretation of the Interchangeable Virtual
Instrument standard from the [IVI foundation](http://www.ivifoundation.org/).

## Included drivers

  * Oscilloscopes (scope):
    * Agilent InfiniiVision 2000A X-series
    * Agilent InfiniiVision 3000A X-series
    * Agilent InfiniiVision 4000A X-series
    * Agilent InfiniiVision 6000A series
    * Agilent InfiniiVision 7000A/B series
    * Agilent Infiniium 90000A/90000X series
    * LeCroy WaveRunner Xi-A series
    * Rigol DS1000Z series (and other Rigol MSO and DSO series)
    * Tektronix MDO3000 series
    * Tektronix DPO4000 series
    * Tektronix MDO4000 series
    * Tektronix MSO4000 series
  * Digital Multimeters (dmm):
    * Agilent 34401A
    * Agilent 34410A
  * Function Generators (fgen):
    * Agilent InfiniiVision 2000A X-series (Wavegen option)
    * Agilent InfiniiVision 3000A X-series (Wavegen option)
    * Agilent InfiniiVision 4000A X-series (Wavegen option)
    * Rigol DG4000 series (partially working as a MSO1074Z)
    * Tektronix MDO3000 series (AFG option)
    * Tektronix AWG2000 series
  * DC Power Supplies (dcpwr):
    * Agilent E3600A series
    * Agilent 603xA series
    * Chroma 62000P series
    * Rigol DP800 series
    * Rigol DP1000 series
    * Tektronix PS2520G/PS2521G
  * RF Power Meters (pwrmeter):
    * Agilent 436A
    * Agilent 437B
    * Agilent U2000 series
  * Spectrum Analyzers (specan):
    * Agilent 859xA/B series
    * Agilent 859xE/EM/C/L series
  * RF Signal Generators (rfsiggen):
    * Agilent 8340/1 A/B
    * Agilent 8642 A/B
    * Agilent ESG E4400B series
  * Other
    * Agilent 8156A optical attenuator
    * Agilent 85644/5A tracking source
    * Agilent 86140B series optical spectrum analyzer
    * Colby Instruments PDL10A Programmable Delay Line
    * DiCon Fiberoptics GP700 Programmable Fiberoptic Instrument
    * JDS Uniphase TB9 Series Optical Grating Filter
    * Tektronix AM5030 programmable current probe amplifier
    * Tektronix OA5000 series optical attenuator

## Instrument communication

Python IVI can use Python VXI-11, Python USBTMC, PyVISA, pySerial and
linux-gpib to connect to instruments.  The implementation of the initialize
method takes a VISA resource string and attempts to connect to an instrument.
If the resource string starts with TCPIP, then Python IVI will attempt to use
Python VXI-11. If it starts with USB, it attempts to use Python USBTMC.  If it
starts with GPIB, it will attempt to use linux-gpib's python interface.  If it
starts with ASRL, it attemps to use pySerial.  Python IVI will fall back on
PyVISA if it is detected.  It is also possible to configure IVI to prefer
PyVISA over the other supported interfaces.  

## A note on standards compliance

As the IVI standard only specifies the API for C, COM, and .NET, a Python
implementation is inherently not compliant and hence this is not an
implementation of the standard, but an interpretation that tries to remain
as faithful as possibe while presenting a uniform, easy-to-use, sensible,
python-style interface.

The Python IVI library is a Pythonized version of the .NET and COM IVI API
specifications, with the CamelCase for everything but the class names replaced
with lowercase_with_underscores.  The library most closely follows the .NET
standard, with the calls that would require the .NET helper classes follwing
the corresponding COM specifications.  There are some major deviations from
the specification in order to be consistent with the spirit of the other IVI
specifications.  The fgen class is the most obvious example of this, using
properties instead of the getters and setters as required by the IVI
specification.  

## Requirements

* Python 2 or Python 3
* [NumPy](http://www.numpy.org)
* One or more communication extensions

## Installation

Extract and run

    # python setup.py install

### Instrument Communication Extensions

Python IVI does not contain any IO drivers itself.  In order to communicate
with an instrument, you must install one or more of the following drivers:

#### Python VXI11

Python VXI11 provides a pure python TCP/IP driver for LAN based instruments
that support the VXI11 protocol.  This includes most LXI instruments and also
devices like the Agilent E2050 GPIB to LAN converter.  

Home page:
http://www.alexforencich.com/wiki/en/python-vxi11/start

GitHub repository:
https://github.com/python-ivi/python-vxi11

#### Python USBTMC

Python USBTMC provides a pure python USBTMC driver for instruments that
support the USB Test and Measurement Class.  Python USBTMC uses PyUSB to
connect to the instrument in a platform-independent manner.

Home page:
http://alexforencich.com/wiki/en/python-usbtmc/start

GitHub repository:
https://github.com/python-ivi/python-usbtmc

#### PyVISA

A Python package for support of the Virtual Instrument Software Architecture
(VISA), in order to control measurement devices and test equipment via GPIB,
RS232, or USB.

Home page:
http://pyvisa.readthedocs.org/

Python IVI will use PyVISA as a fallback for all connections, if it is
detected.  If a connection with PyVISA is preferred, then there are two ways
of changing this.  First, the prefer_pyvisa option can be set when
initalizing an instrument:

    mso = ivi.agilent.agilentMSO7104A("TCPIP0::192.168.1.104::INSTR", prefer_pyvisa = True)

or equivalently:

    mso = ivi.agilent.agilentMSO7104A()
    mso.initialize("TCPIP0::192.168.1.104::INSTR", prefer_pyvisa = True)

Second, the prefer_pyvisa option can be set globally:

    ivi.set_prefer_pyvisa(True)
    mso = ivi.agilent.agilentMSO7104A("TCPIP0::192.168.1.104::INSTR")

#### Linux GPIB

Python IVI provides an interface wrapper for the Linux GPIB driver.  If the
Linux GPIB driver and its included Python interface available, Python IVI can
use it to communicate with instruments via any GPIB interface supported by
Linux GPIB.  

Home page:
http://linux-gpib.sourceforge.net/

#### pySerial

Python IVI provides an interface wrapper for the pySerial library.  If
pySerial is installed, Python IVI can use it to communicate with instruments
via the serial port.  

Home page:
http://pyserial.sourceforge.net/

## Built-in Help

Python IVI has a built-in help feature.  This can be used in three ways:

Call the help method with no parameters:

    import ivi
    instr = ivi.Driver()
    instr.help()

This will print a list of all of the available methods and properties, like this:

    close
    initialized
    initialize
    identity.get_supported_instrument_models
    identity.get_group_capabilities
    identity.specification_major_version
    ...

The higher level groups can also be passed to the help method:

    import ivi
    instr = ivi.Driver()
    instr.help(instr.identity)

This will output everything inside of the sub group:

    get_supported_instrument_models
    get_group_capabilities
    specification_major_version
    ...

Finally, individual methods and properties can be passed as strings:

    import ivi
    instr = ivi.Driver()
    instr.help("identity.supported_instrument_models")

This will result in the complete documentation:

    Returns a comma-separated list of names of instrument models with which
    the IVI specific driver is compatible. The string has no white space
    ...

## Usage examples

This sample Python code will use Python IVI to connect to an oscilloscope
(either an Agilent MSO7104A or a Tektronix MDO4104) over LXI (VXI-11) or
USBTMC, configure the timebase, trigger, and channel 1, capture a waveform,
and read it out of the instrument.

    # import Python IVI
    import ivi
    # connect to scope
    scope = ivi.agilent.agilentMSO7104A("TCPIP0::192.168.1.104::INSTR")
    #scope = ivi.tektronix.tektronixMDO4104("TCPIP0::192.168.1.108::INSTR")
    #scope = ivi.agilent.agilentMSO7104A("USB0::2391::5973::MY********::INSTR")
    #scope = ivi.tektronix.tektronixMDO4104("USB0::1689::1036::C******::INSTR")
    # configure timebase
    scope.acquisition.time_per_record = 1e-3
    # configure triggering
    scope.trigger.type = 'edge'
    scope.trigger.source = scope.channels[0]
    scope.trigger.coupling = 'dc'
    scope.trigger.edge.slope = 'positive'
    scope.trigger.level = 0
    # configure channels
    for ch in scope.channels[0:1]:
        ch.enabled = True
        ch.offset = 0
        ch.range = 4
        ch.coupling = 'dc'
    # initiate measurement
    scope.measurement.initiate()
    # read out channel 1 waveform data
    waveform = scope.channels[0].measurement.fetch_waveform()
    # measure peak-to-peak voltage
    vpp = scope.channels[0].measurement.fetch_waveform_measurement("voltage_peak_to_peak")
    # measure phase
    phase = scope.channels[0].measurement.fetch_waveform_measurement("phase", scope.channels[1])
    # save screenshot to file
    png = scope.display.fetch_screenshot()
    with open('screenshot.png', 'wb') as f:
        f.write(png)
    # save setup to file
    setup = scope.system.fetch_setup()
    with open('setup.dat', 'wb') as f:
        f.write(setup)
    # restore setup from file
    with open('setup.dat', 'rb') as f:
        setup = f.read()
    scope.system.load_setup(setup)

This sample Python code will use Python IVI to connect to a Tektronix AWG2021,
generate a sinewave with numpy, and transfer it to channel 1.  

    # import Python IVI
    import ivi
    # import numpy
    from numpy import *
    # connect to AWG2021 via GPIB
    #awg = ivi.tektronix.tektronixAWG2021("GPIB0::25::INSTR")
    # connect to AWG2021 via E2050A GPIB to VXI11 bridge
    awg = ivi.tektronix.tektronixAWG2021("TCPIP0::192.168.1.105::gpib,25::INSTR")
    # connect to AWG2021 via serial
    #awg = ivi.tektronix.tektronixAWG2021("ASRL::/dev/ttyUSB0,9600::INSTR")
    # create a waveform
    n = 128
    f = 1
    a = 1
    wfm = a*sin(2*pi/n*f*arange(0,n))
    # transfer to AWG2021
    awg.outputs[0].arbitrary.create_waveform(wfm)
    # 2 volts peak to peak
    awg.outputs[0].arbitrary.gain = 2.0
    # zero offset
    awg.outputs[0].arbitrary.offset = 0.0
    # sample rate 128 MHz
    arb.arbitrary.sample_rate = 128e6
    # enable ouput
    awg.outputs[0].enabled = True

This sample Python code will use Python IVI to connect to an Agilent E3649A
and configure an output.

    # import Python IVI
    import ivi
    # connect to E3649A via GPIB
    #psu = ivi.agilent.agilentE3649A("GPIB0::5::INSTR")
    # connect to E3649A via E2050A GPIB to VXI11 bridge
    psu = ivi.agilent.agilentE3649A("TCPIP0::192.168.1.105::gpib,5::INSTR")
    # connect to E3649A via serial
    #psu = ivi.agilent.agilentE3649A("ASRL::/dev/ttyUSB0,9600::INSTR")
    # configure output
    psu.outputs[0].configure_range('voltage', 12)
    psu.outputs[0].voltage_level = 12.0
    psu.outputs[0].current_limit = 1.0
    psu.outputs[0].ovp_limit = 14.0
    psu.outputs[0].ovp_enabled = True
    psu.outputs[0].enabled = True


It is also possible to control multiple instruments.  This example configures
an Agilent ESG E4433B vector signal generator to output an IQ modulated multitone
waveform which is then received on an Agilent 8593E spectrum analyzer.

    # import Python IVI
    import ivi
    # import numpy
    import numpy as np
    # connect to E4433B via E2050A
    esg = ivi.agilent.agilentE4433B("TCPIP::192.168.1.110::gpib,19::INSTR")
    # connect to 8593E via E2050A
    sa = ivi.agilent.agilent8593E("TCPIP::192.168.1.110::gpib,18::INSTR")
    # create multitone IQ waveform
    n = 2000
    f1 = 1
    a1 = 0.5
    f2 = 3
    a2 = 0.5
    t = np.arange(0,n)
    yi = a1*np.sin(2*np.pi/n*f1*t)+a2*np.sin(2*np.pi/n*f2*t)
    yq = np.zeros(n)
    # configure ESG
    esg.rf.frequency = 4e9
    esg.rf.level = -10
    esg.digital_modulation.arb.write_waveform('wfm', yi, yq)
    esg.digital_modulation.arb.selected_waveform = 'wfm'
    esg.digital_modulation.arb.clock_frequency = 10e6
    esg.iq.source = 'arb_generator'
    esg.iq.enabled = True
    esg.rf.output_enabled = True
    # configure SA
    sa.frequency.configure_center_span(4e9, 100e3)

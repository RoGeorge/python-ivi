"""

Python Interchangeable Virtual Instrument Library

Copyright (c) 2016 Alex Forencich

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

"""

from .tektronixBaseScope import *

class tektronixDPO7000(tektronixBaseScope):
    "Tektronix DPO7000 series IVI oscilloscope driver"

    def __init__(self, *args, **kwargs):
        self.__dict__.setdefault('_instrument_id', 'DPO7000')

        super(tektronixDPO7000, self).__init__(*args, **kwargs)

        self._analog_channel_count = 4
        self._digital_channel_count = 0
        self._channel_count = self._analog_channel_count + self._digital_channel_count
        self._bandwidth = 3.5e9

        self._identity_description = "Tektronix DPO7000 series IVI oscilloscope driver"
        self._identity_supported_instrument_models = ['DPO7354C']

        self._init_channels()

        self._add_property('acquisition.horizontal_mode',
                        self._get_acquisition_horizontal_mode,
                        self._set_acquisition_horizontal_mode,
                        None,
                        ivi.Doc("""
                        This command set or queries the horizontal mode. Auto mode is the factory
                        default. There are three horizontal modes:
                        * 'auto': AUTO selects the automatic horizontal model. Auto mode attempts to keep record
                        length constant as you change the time per division setting.  Record length is
                        read only.
                        * 'constant' selects the constant horizontal model. Constant mode attempts to keep
                        sample rate constant as you change the time per division setting. Record length
                        is read only.
                        * 'manual' selects the manual horizontal model. Manual mode lets you change
                        sample mode and record length. Time per division or Horizontal scale is read only.
                        """))

        self._add_property('acquisition.sample_rate',
                        self._get_acquisition_sample_rate,
                        self._set_acquisition_sample_rate,
                        None,
                        ivi.Doc("""
                        Returns the effective sample rate of the acquired waveform using the
                        current configuration. The units are samples per second.
                        """))

        self._add_property('acquisition.horizontal_roll',
                        self._get_acquisition_horizontal_roll,
                        self._set_acquisition_horizontal_roll,
                        None,
                        ivi.Doc("""
                        This command sets or queries the Roll Mode status. Use Roll Mode when you
                        want to view data at very slow sweep speeds. It is useful for observing data
                        samples on the screen as they occur.  There are three modes:
                        * 'auto': AUTO enables Roll Mode, if the time/division is set appropriately.
                        * 'off': OFF disables Roll Mode.
                        * 'on': ON enables Roll Mode, if the time/division is set approprately.
                        """))

    def _get_acquisition_horizontal_mode(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._acquisition_horizontal_mode = self._ask(":horizontal:mode?")
            self._set_cache_valid()
        return self._aquisition_horizontal_mode

    def _set_acquisition_horizontal_mode(self, value):
        if not self._driver_operation_simulate:
            self._write(":horizontal:mode %e" % value)
        self._acquisition_horizontal_mode = value
        self._set_cache_valid()

    def _get_acquisition_sample_rate(self):
        return self._get_acquisition_record_length() / self._get_acquisition_time_per_record()

    def _set_acquisition_sample_rate(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write(":horizontal:mode:samplerate %e" % value)
        self._acquisition_sample_rate = value
        self._set_cache_valid()

    def _get_acquisition_horizontal_roll(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._horizontal_roll = self._ask(":horizontal:roll?")
            self._set_cache_valid()
        return self._acquisition_horizontal_roll

    def _set_acquisition_horizontal_roll(self, value):
        if not self._driver_operation_simulate:
            self._write(":horizontal:roll %e" % value)
        self._acquisition_horizontal_roll = value
        self._set_cache_valid()

    def _get_timebase_scale(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._timebase_scale = float(self._ask(":horizontal:mode:scale?"))
            self._timebase_range = self._timebase_scale * self._horizontal_divisions
            self._set_cache_valid()
        return self._timebase_scale

    def _set_timebase_scale(self, value):
        value = float(value)
        if not self._driver_operation_simulate:
            self._write(":horizontal:mode:scale %e" % value)
        self._timebase_scale = value
        self._timebase_range = value * self._horizontal_divisions
        self._set_cache_valid()
        self._set_cache_valid(False, 'timebase_window_range')

    def _get_acquisition_number_of_points_minimum(self):
        if not self._driver_operation_simulate and not self._get_cache_valid():
            self._acquisition_number_of_points_minimum = int(self._ask(":horizontal:mode:recordlength?"))
            self._set_cache_valid()
        return self._acquisition_number_of_points_minimum

    def _set_acquisition_number_of_points_minimum(self, value):
        value = int(value)
        # coerce value?
        if not self._driver_operation_simulate:
            self._write(":horizontal:mode:recordlength %d" % value)
        self._acquisition_number_of_points_minimum = value
        self._set_cache_valid()

    def _measurement_fetch_waveform(self, index):
        index = ivi.get_index(self._channel_name, index)

        if self._driver_operation_simulate:
            return ivi.TraceYT()

        self._write(":data:source %s" % self._channel_name[index])
        self._write(":data:encdg fastest")
        self._write(":data:width 2")
        self._write(":data:start 1")
        self._write(":data:stop 1e10")

        trace = ivi.TraceYT()

        # Read preamble
        pre = self._ask(":wfmoutpre?").split(';')
        # print "pre = ",self._ask("WFMOutpre?")
        # print "byt_nr", self._ask("WFMOUTpre:BYT_NR?")
        # print "bit_nr", self._ask("WFMOUTpre:BIT_NR?")
        # print "ENCDG", self._ask("WFMOUTpre:ENCDG?")
        # print "BNFMT", self._ask("WFMOUTpre:BN_FMT?")
        # print "BYTOR", self._ask("WFMOUTpre:BYT_OR?")
        # print "NRFMT", self._ask("WFMOUTpre:NR_PT?")
        # print "PTFMT", self._ask("WFMOUTpre:PT_FMT?")
        # print "XINC", self._ask("WFMOUTpre:XINCR?")
        # print "XZERO", self._ask("WFMOUTpre:XZERO?")
        # print "PTOFF", self._ask("WFMOUTpre:PT_OFF?")
        # print "YMULT", self._ask("WFMOUTpre:YMULT?")
        # print "YOFOF", self._ask("WFMOUTpre:YOFF?")
        # print "YZERO", self._ask("WFMOUTpre:YZERO?")
        # print "NR_nr", self._ask("WFMOUTpre:NR_FR?")
        acq_format = pre[7].strip().upper()
        points = int(pre[6])
        point_size = int(pre[0])
        point_enc = pre[2].strip().upper()
        point_fmt = pre[3].strip().upper()
        byte_order = pre[4].strip().upper()
        trace.x_reference = float(pre[11]) #pt_off
        trace.x_increment = float(pre[9])  #xincr
        trace.x_origin = float(pre[10])  #xzero
        trace.y_increment = float(pre[13])  #ymult
        trace.y_reference = int(float(pre[14])) #yoff
        trace.y_origin = (float(pre[15])) #yzero

        if acq_format != 'Y':
            raise UnexpectedResponseException()

        if point_enc != 'BINARY':
            raise UnexpectedResponseException()

        # Read waveform data
        raw_data = self._ask_for_ieee_block(":curve?")
        self._read_raw() # flush buffer

        # Store in trace object
        if point_fmt == 'RP' and point_size == 1:
            trace.y_raw = array.array('B', raw_data[0:points*2])
        elif point_fmt == 'RP' and point_size == 2:
            trace.y_raw = array.array('H', raw_data[0:points*2])
        elif point_fmt == 'RI' and point_size == 1:
            trace.y_raw = array.array('b', raw_data[0:points*2])
        elif point_fmt == 'RI' and point_size == 2:
            trace.y_raw = array.array('h', raw_data[0:points*2])
        elif point_fmt == 'FP' and point_size == 4:
            trace.y_increment = 1
            trace.y_reference = 0
            trace.y_origin = 0
            trace.y_raw = array.array('f', raw_data[0:points*4])
        else:
            raise UnexpectedResponseException()

        if (byte_order == 'LSB') != sys.byteorder == 'little':
            trace.y_raw.byteswap()

        trace.y_raw.byteswap()

        return trace

    def _display_fetch_screenshot(self, format='png', invert=False):
        if self._driver_operation_simulate:
            return b''

        if format not in self._display_screenshot_image_format_mapping:
            raise ivi.ValueNotSupportedException()

        format = self._display_screenshot_image_format_mapping[format]

        self._write("HARDCopy:PORT FILE;")
        self._write("EXPort:FORMat PNG")

        self._write("HARDCopy:FILEName \"C:\\Temp.png\"")
        self._write("HARDCopy STARt")

        self._write("FILESystem:READFile \"C:\\Temp.png\"")

        screenshot = self._read_raw()

        self._write("FILESystem:DELEte \"C:\\Temp.png\"")

        return screenshot

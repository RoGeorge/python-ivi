"""

Python Interchangeable Virtual Instrument Library

Copyright (c) 2017 Alex Forencich

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

from .rigolDS5000 import *

MeasurementFunctionMappingDigital = {
        'frequency': 'frequency',
        'period': 'period',}

class rigolMSO5072(rigolDS5000):
    "Rigol MSO5072 IVI oscilloscope driver"
    
    def __init__(self, *args, **kwargs):
        cls = 'IviScope'
        grp = 'Base'
        self.__dict__.setdefault('_instrument_id', 'MSO5072')

        super(rigolMSO5072, self).__init__(*args, **kwargs)

        self._analog_channel_count = 2
        self._digital_channel_count = 16
        self._channel_count = self._analog_channel_count + self._digital_channel_count
        self._bandwidth = 100e6
        self._bandwidth_limit = {'20M': 20e6}
        self._output_count = 2
        self._add_method('measurement.fetch_waveform_digital', self._measurement_fetch_waveform_digital, ivi.Doc("""description goes here""", cls, grp, '4.3.13'))
        self._init_channels()
        self._init_outputs()

    def _measurement_fetch_waveform_digital(self, index):
        raw_data = []

        if self._driver_operation_simulate:
            return list()
        self._write(":waveform:source %s" % index)
        # Read preamble
        pre = self._ask(":waveform:preamble?").split(',')

        xinc = float(pre[4])
        xorg = float(pre[5])
        xref = int(float(pre[6]))

#        if format != 0:
#            raise UnexpectedResponseException()

        # Read waveform data
        raw_data.append(self._ask_for_ieee_block(':WAVeform:DATA?'))
        self._read_raw() # flush buffer

        # convert string of hex values to list of hex strings
        data_list = list(raw_data[0])

        # convert to times
        data = [((((k-xref)*xinc) + xorg), e) for k,e in enumerate(data_list)]
        return data

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

from .rigolBaseScope import *
from .rigolDSSource import *

ScreenshotImageFormatMapping = {
        'bmp': 'bmp',
        'bmp24': 'bmp24'}

class rigolDS2000A(rigolBaseScope, rigolDSSource):
    "Rigol DS2000A series IVI oscilloscope driver"

    def __init__(self, *args, **kwargs):
        super(rigolDS2000A, self).__init__(*args, **kwargs)

        self._analog_channel_count = 2
        self._digital_channel_count = 16
        self._bandwidth = 300e6
        self._bandwidth_limit = {'20M': 20e6, '100M': 100e6}
        self._max_averages = 8192

        self._horizontal_divisions = 14
        self._vertical_divisions = 8

        # Internal source
        self._output_count = 2

        self._display_screenshot_image_format_mapping = ScreenshotImageFormatMapping

        self._identity_description = "Rigol DS2000A series IVI oscilloscope driver"
        self._identity_supported_instrument_models = ['DS2074A', 'DS2104A', 'DS2204A',
                'DS2304A', 'MSO2074A', 'MSO2104A', 'MSO2204A', 'MSO2304A']

        self._init_channels()
        self._init_outputs()

    def _display_fetch_screenshot(self, format='bmp', invert=False):
        if self._driver_operation_simulate:
            return b''

        if format not in self._display_screenshot_image_format_mapping:
            raise ivi.ValueNotSupportedException()

        self._write(":display:data?")

        data = self._read_raw()

        return ivi.decode_ieee_block(data)

    def _get_channel_probe_attenuation(self, index):
        index = ivi.get_index(self._analog_channel_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            self._channel_probe_attenuation[index] = float(self._ask(":%s:probe?" % self._channel_name[index]))
            self._set_cache_valid(index=index)
        return self._channel_probe_attenuation[index]

    def _set_channel_probe_attenuation(self, index, value):
        index = ivi.get_index(self._analog_channel_name, index)
        value = float(value)
        if not self._driver_operation_simulate:
            self._write(":%s:probe %s" % (self._channel_name[index], ("%f" %value).rstrip('0').rstrip('.')))
        self._channel_probe_attenuation[index] = value
        self._set_cache_valid(index=index)
        self._set_cache_valid(False, 'channel_offset', index)
        self._set_cache_valid(False, 'channel_scale', index)
        self._set_cache_valid(False, 'channel_range', index)
        self._set_cache_valid(False, 'trigger_level')

    def _measurement_fetch_waveform_measurement(self, index, measurement_function, ref_channel = None):
        print 'index is ', index
        index = ivi.get_index(self._channel_name, index)
        if index < self._analog_channel_count:
            if measurement_function not in MeasurementFunctionMapping:
                raise ivi.ValueNotSupportedException()
            func = MeasurementFunctionMapping[measurement_function]
        else:
            if measurement_function not in MeasurementFunctionMappingDigital:
                raise ivi.ValueNotSupportedException()
            func = MeasurementFunctionMappingDigital[measurement_function]
        if not self._driver_operation_simulate:
            # l = func.split(' ')
            # l[0] = l[0] + '?'
            # if len(l) > 1:
            #     l[-1] = l[-1] + ','
            # func = ' '.join(l)
            query = ":measure:%s? %s" % (func, self._channel_name[index])
            print 'query is ', query
            if measurement_function in ['phase', 'delay']:
                ref_index = ivi.get_index(self._channel_name, ref_channel)
                query += ", %s" % self._channel_name[ref_index]
            meas = self._ask(query)
            if meas == 'measure error!':
                return meas
            else:
                return float(meas)
        return 0
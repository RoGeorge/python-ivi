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

import numpy as np
import struct

from .. import ivi
from .. import fgen

OutputMode = set(['function', 'arbitrary'])
OperationMode = set(['continuous'])
StandardWaveformMapping = {
        'sin': 'sin',
        'squ': 'squ',
        'ramp': 'ramp',
        'dc': 'dc',
        'puls': 'puls',
        'nois': 'nois',
        'sinc': 'sinc',
        'exprise': 'exprise',
        'expfall': 'expfall',
        'ecg': 'ecg',
        'gaussian': 'gaussian',
        'lorentz': 'lorentz',
        'haversine': 'haversine',
        }

class rigolBaseWG(fgen.Base, fgen.StdFunc, fgen.ArbWfm, fgen.ArbFrequency,
                fgen.ArbChannelWfm):
    "Rigol Oscilloscope WG option IVI waveform generator driver"

    def __init__(self, *args, **kwargs):
        self.__dict__.setdefault('_instrument_id', 'DS1074Z')

        self._output_standard_waveform_pulse_width = list()
        self._output_standard_waveform_symmetry = list()
        self._output_noise_enabled = list()
        self._output_noise_percent = list()

        super(rigolBaseWG, self).__init__(*args, **kwargs)

        # WG option
        self._output_count = 2
        self._arbitrary_sample_rate = 0
        self._arbitrary_waveform_number_waveforms_max = 0
        self._arbitrary_waveform_size_max = 131072
        self._arbitrary_waveform_size_min = 2
        self._arbitrary_waveform_quantum = 1

        self._add_property('outputs[].standard_waveform.symmetry',
                        self._get_output_standard_waveform_symmetry,
                        self._set_output_standard_waveform_symmetry,
                        None,
                        """
                        Specifies the symmetry for a ramp or triangle waveform. This attribute
                        affects function generator behavior only when the Waveform attribute is
                        set to Waveform Triangle, Ramp Up, or Ramp Down. The value is expressed
                        as a percentage.
                        """)


        self._identity_description = "Rigol Oscilloscope WG option IVI function generator driver"
        self._identity_supported_instrument_models = ['DS1074Z', 'DS1104Z', 'DS1074ZPlus',
        'DS1104ZPlus', 'MSO1074Z', 'MSO1104Z', 'DS2072A', 'MSO2072A', 'MSO5072', 'MSO5074',
        'DS7014', 'MSO7014', 'MSO8064']

        self._init_outputs()

    def _init_outputs(self):
        try:
            super(rigolBaseWG, self)._init_outputs()
        except AttributeError:
            pass
        self._output_name = list()
        self._source_name = list()
        self._output_operation_mode = list()
        self._output_enabled = list()
        self._output_impedance = list()
        self._output_mode = list()
        self._output_reference_clock_source = list()
        self._output_standard_waveform_pulse_width = list()
        self._output_standard_waveform_ramp_symmetry = list()
        self._output_noise_enabled = list()
        self._output_noise_percent = list()
        for i in range(self._output_count):
            if self._output_count == 1:
                self._output_name.append("output")
            else:
                self._output_name.append("output%d" % (i+1))
            self._output_operation_mode.append('continuous')
            self._output_enabled.append(False)
            self._output_impedance.append(50)
            self._output_mode.append('function')
            self._output_reference_clock_source.append('internal')
            self._output_standard_waveform_pulse_width.append(100e-6)
            self._output_standard_waveform_symmetry.append(50.0)
            self._output_noise_enabled.append(False)
            self._output_noise_percent.append(10.0)

        #create source channels
        for i in range(self._output_count):
            if self._output_count == 1:
                self._source_name.append("source")
            else:
                self._source_name.append("source%d" % (i+1))

        self.outputs._set_list(self._output_name)


    # AFG option
    def _get_output_enabled(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            resp = self._ask(":%s?" % (self._output_name[index]))
            self._output_enabled[index] = bool(int(resp))
            self._set_cache_valid(index=index)
        return self._output_enabled[index]

    def _set_output_enabled(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = bool(value)
        if not self._driver_operation_simulate:
            self._write(":%s %d" % (self._output_name[index], value))
        self._output_enabled[index] = value
        self._set_cache_valid(index=index)


    def _get_output_impedance(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            val = self._ask(":%s:impedance?" % self._output_name[index])
            if val == 'OMEG':
                self._output_impedance[index] = "HighZ"
            elif val == 'FIFT':
                self._output_impedance[index] = "50Ohms"
            self._set_cache_valid(index=index)
        return self._output_impedance[index]

    def _set_output_impedance(self, index, value):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate:
            if value == "HighZ":
                self._write(":%s:impedance OMEG" % self._output_name[index])
            elif value == "50Ohms":
                self._write(":%s:impedance FIFTY" % self._output_name[index])
        self._output_impedance[index] = value
        self._set_cache_valid(index=index)

    def _get_output_settings(self, index):
        index = ivi.get_index(self._output_name, index)
        self._output_settings = {}
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            resp = self._ask(":%s:apply?" % self._source_name[index])
            settings = resp.split(',')
            wtype = settings[0].lower()
            wtype = [k for k,v in StandardWaveformMapping.items() if v==wtype][0]
            self._output_settings["wtype"] = wtype
            self._output_settings["amplitude"] = settings[2]
            self._output_settings["offset"] = settings[3]
            if wtype != 'noise':
                self._output_settings["freq"] = settings[1]
                self._output_settings["startphase"] = settings[4]
            self._set_cache_valid(index=index)
        return self._output_settings

    def _set_output_settings(self, index, wtype, amplitude, offset, freq = "",  startphase = ""):
        #fix source index
        index = ivi.get_index(self._output_name, index)
        wtype = StandardWaveformMapping[wtype]
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            if wtype == "NOISE":
                self._write(":%s:APPLY:NOISE %s, %s" % (self._source_name[index], amplitude, offset))
            else:
                self._write(":%s:APPLY:%s %s, %s, %s, %s" % (self._source_name[index], wtype, freq, amplitude, offset, startphase))
            self._set_cache_valid(index=index)
        self._set_cache_valid(index=index)

    def _get_output_standard_waveform_frequency(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            resp = self._ask(":%s:frequency?" % self._source_name[index])
            self._output_standard_waveform_frequency[index] = float(resp)
            self._set_cache_valid(index=index)
        return self._output_standard_waveform_frequency[index]

    def _set_output_standard_waveform_frequency(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = float(value)
        if value < 0.1 or value > 50e6:
            raise ivi.OutOfRangeException()
        if not self._driver_operation_simulate:
            self._write(":%s:frequency %e" % (self._source_name[index], value))
        self._output_standard_waveform_frequency[index] = value
        self._set_cache_valid(index=index)

    def _get_output_standard_waveform_start_phase(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            resp = self._ask(":%s:phase?" % self._source_name[index])
            self._output_standard_waveform_start_phase[index] = float(resp)
            self._set_cache_valid(index=index)
        return self._output_standard_waveform_start_phase[index]

    def _set_output_standard_waveform_start_phase(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = float(value)
        if value < -180.0 or value > 180.0:
            raise ivi.OutOfRangeException()
        if not self._driver_operation_simulate:
            self._write(":%s:phase %e" % (self._source_name[index], value))
        self._output_standard_waveform_start_phase[index] = value
        self._set_cache_valid(index=index)


    def _get_output_standard_waveform_waveform(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            resp = self._ask(":%s:function?" % self._source_name[index]).lower()
            if resp == 'arbitrary':
                resp = 'sine'
            resp = [k for k,v in StandardWaveformMapping.items() if v==resp][0]
            if resp == 'ramp_up':
                if self._get_output_standard_waveform_symmetry(index) <= 10.0:
                    resp = 'ramp_down'
                elif self._get_output_standard_waveform_symmetry(index) >= 90.0:
                    resp = 'ramp_up'
                else:
                    resp = 'triangle'
            self._output_standard_waveform_waveform[index] = resp
            self._set_cache_valid(index=index)
        return self._output_standard_waveform_waveform[index]

    def _set_output_standard_waveform_waveform(self, index, value):
        index = ivi.get_index(self._output_name, index)
        if value not in StandardWaveformMapping:
            raise ivi.ValueNotSupportedException()
        if not self._driver_operation_simulate:
            self._write(":%s:function %s" % (self._source_name[index], StandardWaveformMapping[value]))
            if value == 'triangle':
                if self._get_output_standard_waveform_symmetry(index) <= 10.0 or self._get_output_standard_waveform_symmetry(index) >= 90:
                    self._set_output_standard_waveform_symmetry(index, 50.0)
            elif value == 'ramp_up':
                self._set_output_standard_waveform_symmetry(index, 100.0)
            elif value == 'ramp_down':
                self._set_output_standard_waveform_symmetry(index, 0.0)
        self._output_standard_waveform_waveform[index] = value
        self._set_cache_valid(index=index)
        self._output_mode[index] = 'function'
        self._set_cache_valid(True, 'output_mode', index=index)

    def _get_output_standard_waveform_symmetry(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            resp = self._ask(":%s:function:ramp:symmetry?" % self._source_name[index])
            self._output_standard_waveform_symmetry[index] = float(resp)
            self._set_cache_valid(index=index)
        return self._output_standard_waveform_symmetry[index]

    def _set_output_standard_waveform_symmetry(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = float(value)
        if value < 0.0 or value > 100.0:
            raise ivi.OutOfRangeException()
        if not self._driver_operation_simulate:
            self._write(":%s:function:ramp:symmetry %e" % (self._source_name[index], value))
        self._output_standard_waveform_symmetry[index] = value
        self._set_cache_valid(index=index)

    def _get_output_standard_waveform_amplitude(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            resp = self._ask(":%s:voltage?" % self._source_name[index])
            self._output_standard_waveform_amplitude[index] = float(resp)
            self._set_cache_valid(index=index)
        return self._output_standard_waveform_amplitude[index]

    def _set_output_standard_waveform_amplitude(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = float(value)
        if value < 0.01 or value > 5.0:
            raise ivi.OutOfRangeException()
        if not self._driver_operation_simulate:
            self._write(":%s:voltage %e" % (self._source_name[index], value))
        self._output_standard_waveform_amplitude[index] = value
        self._set_cache_valid(index=index)

    def _get_output_standard_waveform_dc_offset(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            resp = self._ask(":%s:voltage:offset?" % self._source_name[index])
            self._output_standard_waveform_dc_offset[index] = float(resp)
            self._set_cache_valid(index=index)
        return self._output_standard_waveform_dc_offset[index]

    def _set_output_standard_waveform_dc_offset(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = float(value)
        if not self._driver_operation_simulate:
            self._write(":%s:voltage:offset %e" % (self._source_name[index], value))
        self._output_standard_waveform_dc_offset[index] = value
        self._set_cache_valid(index=index)

    def _get_output_standard_waveform_duty_cycle_high(self, index):
        index = ivi.get_index(self._output_name, index)
        if not self._driver_operation_simulate and not self._get_cache_valid(index=index):
            resp = self._ask(":%s:pulse:dcycle?" % self._source_name[index])
            self._output_standard_waveform_duty_cycle_high[index] = float(resp)
            self._set_cache_valid(index=index)
        return self._output_standard_waveform_duty_cycle_high[index]

    def _set_output_standard_waveform_duty_cycle_high(self, index, value):
        index = ivi.get_index(self._output_name, index)
        value = float(value)
        # print value
        if value < 10.0 or value > 90.0:
            raise ivi.OutOfRangeException()
        if not self._driver_operation_simulate:
            self._write(":%s:pulse:dcycle %e" % (self._source_name[index], value))
        self._output_standard_waveform_duty_cycle_high[index] = value
        self._set_cache_valid(index=index)

# distutils: language = c++
# cython: language_level=3

from cpython.mem cimport PyMem_Malloc, PyMem_Free
from libc.stdlib cimport malloc, free
from libc.string cimport memcpy, strcpy

from libcpp.vector cimport vector
from libcpp.string cimport string
from libcpp.pair cimport pair

import pathlib

cdef extern from "limedriver.h":
    cdef struct LimeConfig_t:
        string device

        float srate
        int channel
        int TX_matching
        int RX_matching
        float frq
        float frq_set
        float RX_LPF
        float TX_LPF
        int RX_gain
        int TX_gain
        int TX_IcorrDC
        int TX_QcorrDC
        int TX_IcorrGain
        int TX_QcorrGain
        int TX_IQcorrPhase
        int RX_IcorrGain
        int RX_QcorrGain
        int RX_IQcorrPhase
        int RX_gain_rback[4]
        int TX_gain_rback[3]

        int Npulses
        double *p_dur
        int *p_dur_smp
        int *p_offs
        double *p_amp
        double *p_frq
        double *p_frq_smp
        double *p_pha
        int *p_phacyc_N
        int *p_phacyc_lev
        
        double *am_frq
        double *am_pha
        double *am_depth
        int *am_mode
        double *am_frq_smp
        double *fm_frq
        double *fm_pha
        double *fm_width
        int *fm_mode
        double *fm_frq_smp

        int *p_c0_en
        int *p_c1_en
        int *p_c2_en
        int *p_c3_en

        int c0_tim[4]
        int c1_tim[4]
        int c2_tim[4]
        int c3_tim[4]

        int c0_synth[5]
        int c1_synth[5]
        int c2_synth[5]
        int c3_synth[5]

        int averages
        int repetitions
        int pcyc_bef_avg
        double reptime_secs
        double rectime_secs
        int reptime_smps
        int rectime_smps
        int buffersize
        
        int override_init
        int override_save

        string file_pattern
        string file_stamp
        string save_path

        string stamp_start
        string stamp_end

    cdef LimeConfig_t initializeLimeConfig(int Npulses)

    cdef int run_experiment_from_LimeCfg(LimeConfig_t config)

    cdef pair[int, int] getChannelsFromInfo(string device)

    cdef vector[string] getDeviceList()
        

cdef class PyLimeConfig:
    cdef LimeConfig_t _config

    def __cinit__(self, Npulses):
        self._config = initializeLimeConfig(Npulses)

    @property
    def srate(self):
        return self._config.srate

    @srate.setter
    def srate(self, float value):
        self._config.srate = value

    @property
    def channel(self):
        return self._config.channel

    @channel.setter
    def channel(self, int value):
        self._config.channel = value

    @property
    def TX_matching(self):
        return self._config.TX_matching

    @TX_matching.setter
    def TX_matching(self, int value):
        self._config.TX_matching = value

    @property
    def RX_matching(self):
        return self._config.RX_matching

    @RX_matching.setter
    def RX_matching(self, int value):
        self._config.RX_matching = value

    @property
    def frq(self):
        return self._config.frq

    @frq.setter
    def frq(self, float value):
        self._config.frq = value

    @property
    def frq_set(self):
        return self._config.frq_set

    @frq_set.setter
    def frq_set(self, float value):
        self._config.frq_set = value

    @property
    def RX_LPF(self):
        return self._config.RX_LPF

    @RX_LPF.setter
    def RX_LPF(self, float value):
        self._config.RX_LPF = value

    @property
    def TX_LPF(self):
        return self._config.TX_LPF

    @TX_LPF.setter
    def TX_LPF(self, float value):
        self._config.TX_LPF = value

    @property
    def RX_gain(self):
        return self._config.RX_gain

    @RX_gain.setter
    def RX_gain(self, int value):
        self._config.RX_gain = value

    @property
    def TX_gain(self):
        return self._config.TX_gain

    @TX_gain.setter
    def TX_gain(self, int value):
        self._config.TX_gain = value

    @property
    def TX_IcorrDC(self):
        return self._config.TX_IcorrDC

    @TX_IcorrDC.setter
    def TX_IcorrDC(self, int value):
        self._config.TX_IcorrDC = value

    @property
    def TX_QcorrDC(self):
        return self._config.TX_QcorrDC

    @TX_QcorrDC.setter
    def TX_QcorrDC(self, int value):
        self._config.TX_QcorrDC = value

    @property
    def TX_IcorrGain(self):
        return self._config.TX_IcorrGain

    @TX_IcorrGain.setter
    def TX_IcorrGain(self, int value):
        self._config.TX_IcorrGain = value

    @property
    def TX_QcorrGain(self):
        return self._config.TX_QcorrGain

    @TX_QcorrGain.setter
    def TX_QcorrGain(self, int value):
        self._config.TX_QcorrGain = value

    @property
    def TX_IQcorrPhase(self):
        return self._config.TX_IQcorrPhase

    @TX_IQcorrPhase.setter
    def TX_IQcorrPhase(self, int value):
        self._config.TX_IQcorrPhase = value

    @property
    def RX_IcorrGain(self):
        return self._config.RX_IcorrGain
    
    @RX_IcorrGain.setter
    def RX_IcorrGain(self, int value):
        self._config.RX_IcorrGain = value

    @property
    def RX_QcorrGain(self):
        return self._config.RX_QcorrGain

    @RX_QcorrGain.setter
    def RX_QcorrGain(self, int value):
        self._config.RX_QcorrGain = value

    @property
    def RX_IQcorrPhase(self):
        return self._config.RX_IQcorrPhase

    @RX_IQcorrPhase.setter
    def RX_IQcorrPhase(self, int value):
        self._config.RX_IQcorrPhase = value

    @property
    def Npulses(self):
        return self._config.Npulses

    @Npulses.setter
    def Npulses(self, int value):
        self._config.Npulses = value

    @property
    def averages(self):
        return self._config.averages

    @averages.setter
    def averages(self, int value):
        self._config.averages = value

    @property
    def repetitions(self):
        return self._config.repetitions

    @repetitions.setter
    def repetitions(self, int value):
        self._config.repetitions = value

    @property
    def pcyc_bef_avg(self):
        return self._config.pcyc_bef_avg

    @pcyc_bef_avg.setter
    def pcyc_bef_avg(self, int value):
        self._config.pcyc_bef_avg = value

    @property
    def reptime_secs(self):
        return self._config.reptime_secs

    @reptime_secs.setter
    def reptime_secs(self, float value):
        self._config.reptime_secs = value

    @property
    def rectime_secs(self):
        return self._config.rectime_secs

    @rectime_secs.setter
    def rectime_secs(self, float value):
        self._config.rectime_secs = value

    @property
    def reptime_smps(self):
        return self._config.reptime_smps

    @reptime_smps.setter
    def reptime_smps(self, int value):
        self._config.reptime_smps = value

    @property
    def rectime_smps(self):
        return self._config.rectime_smps

    @rectime_smps.setter
    def rectime_smps(self, int value):
        self._config.rectime_smps = value

    @property
    def buffersize(self):
        return self._config.buffersize

    @buffersize.setter
    def buffersize(self, int value):
        self._config.buffersize = value

    @property
    def override_init(self):
        return self._config.override_init

    @override_init.setter
    def override_init(self, int value):
        self._config.override_init = value

    @property
    def override_save(self):
        return self._config.override_save

    @override_save.setter
    def override_save(self, int value):
        self._config.override_save = value

    # Pointers

    @property
    def p_dur(self):
        return [self._config.p_dur[i] for i in range(self._config.Npulses)]

    @p_dur.setter
    def p_dur(self, list value):
        for i in range(len(value)):
            self._config.p_dur[i] = value[i]

    @property
    def p_dur_smp(self):
        return [self._config.p_dur_smp[i] for i in range(self._config.Npulses)]

    @p_dur_smp.setter
    def p_dur_smp(self, list value):
        for i in range(len(value)):
            self._config.p_dur_smp[i] = value[i]

    @property
    def p_offs(self):
        return [self._config.p_offs[i] for i in range(self._config.Npulses)]

    @p_offs.setter
    def p_offs(self, list value):
        for i in range(len(value)):
            self._config.p_offs[i] = value[i]

    @property
    def p_amp(self):
        return [self._config.p_amp[i] for i in range(self._config.Npulses)]

    @p_amp.setter
    def p_amp(self, list value):
        for i in range(len(value)):
            self._config.p_amp[i] = value[i]

    @property
    def p_frq(self):
        return [self._config.p_frq[i] for i in range(self._config.Npulses)]

    @p_frq.setter
    def p_frq(self, list value):
        for i in range(len(value)):
            self._config.p_frq[i] = value[i]

    @property
    def p_frq_smp(self):
        return [self._config.p_frq_smp[i] for i in range(self._config.Npulses)]

    @p_frq_smp.setter
    def p_frq_smp(self, list value):
        for i in range(len(value)):
            self._config.p_frq_smp[i] = value[i]

    @property
    def p_pha(self):
        return [self._config.p_pha[i] for i in range(self._config.Npulses)]

    @p_pha.setter
    def p_pha(self, list value):
        for i in range(len(value)):
            self._config.p_pha[i] = value[i]

    @property
    def p_phacyc_N(self):
        return [self._config.p_phacyc_N[i] for i in range(self._config.Npulses)]

    @p_phacyc_N.setter
    def p_phacyc_N(self, list value):
        for i in range(len(value)):
            self._config.p_phacyc_N[i] = value[i]

    @property
    def p_phacyc_lev(self):
        return [self._config.p_phacyc_lev[i] for i in range(self._config.Npulses)]

    @p_phacyc_lev.setter
    def p_phacyc_lev(self, list value):
        for i in range(len(value)):
            self._config.p_phacyc_lev[i] = value[i]

    @property
    def am_frq(self):
        return [self._config.am_frq[i] for i in range(self._config.Npulses)]

    @am_frq.setter
    def am_frq(self, list value):
        for i in range(len(value)):
            self._config.am_frq[i] = value[i]

    @property
    def am_pha(self):
        return [self._config.am_pha[i] for i in range(self._config.Npulses)]

    @am_pha.setter
    def am_pha(self, list value):
        for i in range(len(value)):
            self._config.am_pha[i] = value[i]

    @property
    def am_depth(self):
        return [self._config.am_depth[i] for i in range(self._config.Npulses)]

    @am_depth.setter
    def am_depth(self, list value):
        for i in range(len(value)):
            self._config.am_depth[i] = value[i]

    @property
    def am_mode(self):
        return [self._config.am_mode[i] for i in range(self._config.Npulses)]

    @am_mode.setter
    def am_mode(self, list value):
        for i in range(len(value)):
            self._config.am_mode[i] = value[i]

    @property
    def am_frq_smp(self):
        return [self._config.am_frq_smp[i] for i in range(self._config.Npulses)]

    @am_frq_smp.setter
    def am_frq_smp(self, list value):
        for i in range(len(value)):
            self._config.am_frq_smp[i] = value[i]

    @property
    def fm_frq(self):
        return [self._config.fm_frq[i] for i in range(self._config.Npulses)]

    @fm_frq.setter
    def fm_frq(self, list value):
        for i in range(len(value)):
            self._config.fm_frq[i] = value[i]

    @property
    def fm_pha(self):
        return [self._config.fm_pha[i] for i in range(self._config.Npulses)]

    @fm_pha.setter
    def fm_pha(self, list value):
        for i in range(len(value)):
            self._config.fm_pha[i] = value[i]

    @property
    def fm_width(self):
        return [self._config.fm_width[i] for i in range(self._config.Npulses)]

    @fm_width.setter
    def fm_width(self, list value):
        for i in range(len(value)):
            self._config.fm_width[i] = value[i]

    @property
    def fm_mode(self):
        return [self._config.fm_mode[i] for i in range(self._config.Npulses)]

    @fm_mode.setter
    def fm_mode(self, list value):
        for i in range(len(value)):
            self._config.fm_mode[i] = value[i]

    @property
    def fm_frq_smp(self):
        return [self._config.fm_frq_smp[i] for i in range(self._config.Npulses)]

    @fm_frq_smp.setter
    def fm_frq_smp(self, list value):
        for i in range(len(value)):
            self._config.fm_frq_smp[i] = value[i]

    @property
    def p_c0_en(self):
        return [self._config.p_c0_en[i] for i in range(self._config.Npulses)]

    @p_c0_en.setter
    def p_c0_en(self, list value):
        for i in range(len(value)):
            self._config.p_c0_en[i] = value[i]

    @property
    def p_c1_en(self):
        return [self._config.p_c1_en[i] for i in range(self._config.Npulses)]

    @p_c1_en.setter
    def p_c1_en(self, list value):
        for i in range(len(value)):
            self._config.p_c1_en[i] = value[i]

    @property
    def p_c2_en(self):
        return [self._config.p_c2_en[i] for i in range(self._config.Npulses)]

    @p_c2_en.setter
    def p_c2_en(self, list value):
        for i in range(len(value)):
            self._config.p_c2_en[i] = value[i]

    @property
    def p_c3_en(self):
        return [self._config.p_c3_en[i] for i in range(self._config.Npulses)]

    @p_c3_en.setter
    def p_c3_en(self, list value):
        for i in range(len(value)):
            self._config.p_c3_en[i] = value[i]

    # Arrays

    @property
    def RX_gain_rback(self):
        # Return the contents of 'RX_gain_rback' array as a Python list
        return [self._config.RX_gain_rback[i] for i in range(4)]

    @RX_gain_rback.setter
    def RX_gain_rback(self, values):
        # Expected 'values' to be a list with 4 integer elements
        if not isinstance(values, list) or len(values) != 4:
            raise ValueError("RX_gain_rback must be a list with 4 integers.")
        for i in range(4):
            self._config.RX_gain_rback[i] = values[i]

    @property
    def TX_gain_rback(self):
        return [self._config.TX_gain_rback[i] for i in range(3)]

    @TX_gain_rback.setter
    def TX_gain_rback(self, values):
        if not isinstance(values, list) or len(values) != 3:
            raise ValueError("TX_gain_rback must be a list with 3 integers.")
        for i in range(3):
            self._config.TX_gain_rback[i] = values[i]

    @property
    def c0_tim(self):
        return [self._config.c0_tim[i] for i in range(4)]

    @c0_tim.setter
    def c0_tim(self, values):
        if not isinstance(values, list) or len(values) != 4:
            raise ValueError("c0_tim must be a list with 4 integers.")
        for i in range(4):
            self._config.c0_tim[i] = values[i]

    @property
    def c1_tim(self):
        return [self._config.c1_tim[i] for i in range(4)]

    @c1_tim.setter
    def c1_tim(self, values):
        if not isinstance(values, list) or len(values) != 4:
            raise ValueError("c1_tim must be a list with 4 integers.")
        for i in range(4):
            self._config.c1_tim[i] = values[i]

    @property
    def c2_tim(self):
        return [self._config.c2_tim[i] for i in range(4)]

    @c2_tim.setter
    def c2_tim(self, values):
        if not isinstance(values, list) or len(values) != 4:
            raise ValueError("c2_tim must be a list with 4 integers.")
        for i in range(4):
            self._config.c2_tim[i] = values[i]

    @property
    def c3_tim(self):
        return [self._config.c3_tim[i] for i in range(4)]

    @c3_tim.setter
    def c3_tim(self, values):
        if not isinstance(values, list) or len(values) != 4:
            raise ValueError("c3_tim must be a list with 4 integers.")
        for i in range(4):
            self._config.c3_tim[i] = values[i]

    @property
    def c0_synth(self):
        return [self._config.c0_synth[i] for i in range(5)]

    @c0_synth.setter
    def c0_synth(self, values):
        if not isinstance(values, list) or len(values) != 5:
            raise ValueError("c0_synth must be a list with 5 integers.")
        for i in range(5):
            self._config.c0_synth[i] = values[i]

    @property
    def c1_synth(self):
        return [self._config.c1_synth[i] for i in range(5)]

    @c1_synth.setter
    def c1_synth(self, values):
        if not isinstance(values, list) or len(values) != 5:
            raise ValueError("c1_synth must be a list with 5 integers.")
        for i in range(5):
            self._config.c1_synth[i] = values[i]

    @property
    def c2_synth(self):
        return [self._config.c2_synth[i] for i in range(5)]

    @c2_synth.setter
    def c2_synth(self, values):
        if not isinstance(values, list) or len(values) != 5:
            raise ValueError("c2_synth must be a list with 5 integers.")
        for i in range(5):
            self._config.c2_synth[i] = values[i]

    @property
    def c3_synth(self):
        return [self._config.c3_synth[i] for i in range(5)]

    @c3_synth.setter
    def c3_synth(self, values):
        if not isinstance(values, list) or len(values) != 5:
            raise ValueError("c3_synth must be a list with 5 integers.")
        for i in range(5):
            self._config.c3_synth[i] = values[i]
 
    # String properties
    @property
    def device(self):
        return self._config.device.decode('utf-8')
    
    @device.setter
    def device(self, str value):
        self._config.device = value.encode('utf-8')

    @property
    def file_pattern(self):
        return self._config.file_pattern.decode()

    @file_pattern.setter
    def file_pattern(self, value):
        self._config.file_pattern = value.encode()

    @property
    def file_stamp(self):
        return self._config.file_stamp.decode('utf-8')

    @file_stamp.setter
    def file_stamp(self, value):
        self._config.file_stamp = value.encode('utf-8')

    @property
    def save_path(self):
        return self._config.save_path.decode('utf-8')

    @save_path.setter
    def save_path(self, str value):
        self._config.save_path = value.encode('utf-8')

    @property
    def stamp_start(self):
        return self._config.stamp_start.decode('utf-8')

    @stamp_start.setter
    def stamp_start(self, value):
        self._config.stamp_start = value.encode('utf-8')

    @property
    def stamp_end(self):
        return self._config.stamp_end.decode('utf-8')

    @stamp_end.setter
    def stamp_end(self, value):
        self._config.stamp_end = value.encode('utf-8')

    def run(self):
        return run_experiment_from_LimeCfg(self._config)

    def get_path(self):
        path = self.save_path + self.file_stamp + '_' + self.file_pattern + '.h5'
        path = pathlib.Path(path).absolute()
        return path
 
def get_device_list():
    cdef vector[string] devices = getDeviceList()
    return [device.decode('utf-8') for device in devices] 

def get_channels_for_device(device = ""):
    cdef pair[int, int] channels = getChannelsFromInfo(device.encode())
    return channels.first, channels.second

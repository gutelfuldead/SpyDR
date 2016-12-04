############    ####################    ############
# Tx2.fifo # -> # tx_4_qpsk_mod.py # -> # tx3.fifo #
############    ####################    ############

from __future__ import division
import numpy as np
import math
from fifo_ops import *

def lrange(r1, inc, r2):
    """Provide spacing as an input and receive samples back by wrapping `
    numpy.linspace (basically colon operator in matlab r1:inc:r2)"""
    n = ((r2-r1)+2*np.spacing(r2-r1))//inc
    return np.linspace(r1,r1+inc*n,n+1)

def NRZ_Encoder(data, Rb, amplitude):
    """ Input a stream of bits and specify bit-rate and the amplitude of output signal
    Outputs the NRZ stream"""
    Fs = 10*Rb # sampling freq w/ oversampling factor
    Ts = 1/Fs  # Sampling Period
    Tb = 1/Rb  # Bit periodoutput
    a=0        # stupid person tax (index)
    output = np.zeros(len(data)*int(Tb/Ts))
    time = np.zeros(len(data)*int(Tb/Ts))
    time[0] = 0
    for i in range(0,len(data)):
        for j in range(0,int(Tb/Ts)):
            output[a] = amplitude*(-1)**(1+data[i])
            if a == 0:
                time[a] = 0
            time[a] = time[a-1]+Ts
            a += 1
    return [time, output, Fs]

INPUT_NAME = "tx2.fifo"
OUTPUT_NAME = "tx3.fifo"
Rb=1e3 # bit rate
amplitude = 1 # amp of NRZ data
Fc = 2*Rb;
Tb = 1/Rb

data = read_pipe(INPUT_NAME)
N = len(data)
odd_bits = np.zeros(int(N/2),dtype=np.int8)
even_bits = np.zeros(int(N/2),dtype=np.int8)
# Split into I and Q streams
even_bits = data[0::2] # I (even)
odd_bits = data[1::2] # Q (odd)

even_time, even_NRZ_data, Fs = NRZ_Encoder(even_bits, Rb, amplitude)
odd_time, odd_NRZ_data, Fs = NRZ_Encoder(odd_bits, Rb, amplitude)

in_phase_osc = 1/np.sqrt(2)*np.cos(2*np.pi*Fc*even_time)
quad_phase_osc = 1/np.sqrt(2)*np.sin(2*np.pi*Fc*odd_time)
qpskMod = np.multiply(odd_NRZ_data,quad_phase_osc) + np.multiply(even_NRZ_data,in_phase_osc)

write_pipe(qpskMod, OUTPUT_NAME)
np.save("in_phase_osc.npy",in_phase_osc)
np.save("quad_phase_osc.npy",quad_phase_osc)

variables = np.array( [ N, Fs, Rb ])
np.save("tx_vars.npy",variables)

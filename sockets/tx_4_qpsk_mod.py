#!/usr/bin/python2.7

############    ####################    ############
# Tx2.fifo # -> # tx_4_qpsk_mod.py # -> # tx3.fifo #
############    ####################    ############

from __future__ import division
import numpy as np
import math
from socket_funcs import *
from bool_func import *

def lrange(r1, inc, r2):
    """
    Provide spacing as an input and receive samples back by wrapping
    numpy.linspace (basically colon operator in matlab r1:inc:r2)
    """
    n = ((r2-r1)+2*np.spacing(r2-r1))//inc
    return np.linspace(r1,r1+inc*n,n+1)

def NRZ_Encoder(data, Rb, amplitude):
    """ Input a stream of bits and specify bit-rate and the amplitude of output signal
    Outputs the NRZ stream
    Returns:
    time   == the time vector associated with the sampled bits
    output == the magnitude of the sampled bits
    Fs     == the sampling frequency used to create the bits
    """
    Fs = 10*Rb # sampling freq w/ oversampling factor
    Ts = 1/Fs  # Sampling Period
    Tb = 1/Rb  # Bit periodoutput
    a=0        # stupid person tax (index)
    output = np.empty(len(data)*int(Tb/Ts))
    time = np.empty(len(data)*int(Tb/Ts))
    time[0] = 0
    for i in range(0,len(data)):
        for j in range(0,int(Tb/Ts)):
            output[a] = amplitude*(-1)**(1+data[i])
            if a == 0:
                time[a] = 0
            time[a] = time[a-1]+Ts
            a += 1
    return [time, output, Fs]

socket_in = './tx3_send.uds'
socket_out = './tx4_send.uds'

# Open Server Socket
s = open_socket_serv(socket_out)

Rb=1e3 # bit rate
amplitude = 1 # amp of NRZ data
Fc = 2*Rb;
Tb = 1/Rb

# Load predefined in/quad phase oscillators
# Load in_phase_osc.npy
I_osc_file = "in_phase_osc.npy"
if os.path.isfile(I_osc_file):
    in_phase_osc = np.load(I_osc_file)
    I_osc_exist = True
else:
    print("Missing file {}, generating").format(I_osc_file)
    I_osc_exist = False

# Load quad_phase_osc.npy
Q_osc_file = "quad_phase_osc.npy"
if os.path.isfile(Q_osc_file):
    quad_phase_osc = np.load(Q_osc_file)
    Q_osc_exist = True
else:
    print("Missing file {}, generating").format(Q_osc_file)
    Q_osc_exist = False

# Load tx_vars.npy
var_file = "tx_vars.npy"
if os.path.isfile(var_file):
    vars_exist = True
else:
    print("Missing file {}, generating").format(var_file)
    vars_exist = False

while(1):
    data = socket_recv(socket_in)
    # data = unpack_bits(data)
    N = len(data)
    odd_bits = np.empty(int(N/2),dtype=np.int8)
    even_bits = np.empty(int(N/2),dtype=np.int8)

    # Split into I and Q streams
    even_bits = data[0::2] # I (even)
    odd_bits = data[1::2] # Q (odd)

    even_time, even_NRZ_data, Fs = NRZ_Encoder(even_bits, Rb, amplitude)
    odd_time, odd_NRZ_data, Fs = NRZ_Encoder(odd_bits, Rb, amplitude)

    # Generate new in/quad phase oscillators
    if(I_osc_exist == False):
        in_phase_osc = 1/np.sqrt(2)*np.cos(2*np.pi*Fc*even_time)
        np.save("in_phase_osc.npy",in_phase_osc)
    if(Q_osc_exist == False):
        quad_phase_osc = 1/np.sqrt(2)*np.sin(2*np.pi*Fc*odd_time)
        np.save("quad_phase_osc.npy",quad_phase_osc)
    if(vars_exist == False):
        variables = np.array( [ N, Fs, Rb ])
        np.save("tx_vars.npy",variables)

    qpskMod = np.multiply(odd_NRZ_data,quad_phase_osc) + np.multiply(even_NRZ_data,in_phase_osc)

    socket_serv(s, qpskMod)

s.close()

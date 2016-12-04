from __future__ import division
import numpy as np
import random
import math
import matplotlib.pyplot as plt

def lrange(r1, inc, r2):
    """Provide spacing as an input and receive samples back by wrapping `
    numpy.linspace (basically colon operator in matlab r1:inc:r2)"""
    n = ((r2-r1)+2*np.spacing(r2-r1))//inc
    return np.linspace(r1,r1+inc*n,n+1)

#################
# QPSK Receiver #
#################
FILE_NAME_IN = "channel.npy"
FILE_NAME_OUT = "rx1.npy"
qpskMod = np.load(FILE_NAME_IN)

var = np.load("tx_vars.npy")
N = var[0]
Fs = var[1]
Rb = var[2]
Fc = 2*Rb
Tb = 1/Rb

in_phase_osc = np.load("in_phase_osc.npy") # FROM qpsk mod
quad_phase_osc = np.load("quad_phase_osc.npy") # FROM qpsk mod

i_signal = np.array(len(qpskMod))
q_signal = np.zeros(len(qpskMod))
# Multiply received signal with the reference oscillators
i_signal = np.multiply(qpskMod,in_phase_osc)
q_signal = np.multiply(qpskMod,quad_phase_osc)

# The multiplied output is integrated over one bit period using an
# integrator. A threshold detector makes a decision on each integrated bit based on a threshold. Since an
# NRZ signaling format is used with equal amplitudes in positive and negative direction, the threshold for
# this case would be 0
integration_base = lrange(0, 1/Fs, Tb - 1/Fs)
in_phase_component = np.zeros(int(len(i_signal)/(Tb*Fs)+1))
quad_phase_component = np.zeros(int(len(i_signal)/(Tb*Fs)+1))
for i in range(0, int( len(i_signal)/(Tb*Fs) )):
    in_phase_component[i] = np.trapz(y = i_signal[ int(i*Tb*Fs) : int((i+1)*Tb*Fs) ], x=integration_base)
for i in range(0,int( len(q_signal)/(Tb*Fs) )):
    quad_phase_component[i] = np.trapz(y = q_signal[ int(i*Tb*Fs) : int((i+1)*Tb*Fs)], x=integration_base)

# Threshold Detector
estimated_in_bits = np.zeros(int(N/2))
estimated_in_bits = (in_phase_component >= 0)
estimated_in_bits = estimated_in_bits.astype(int)

estimated_quad_bits = np.zeros(int(N/2))
estimated_quad_bits = (quad_phase_component >= 0)
estimated_quad_bits = estimated_quad_bits.astype(int)

data_out = np.hstack( zip(estimated_in_bits, estimated_quad_bits) )

np.save(FILE_NAME_OUT,data_out)

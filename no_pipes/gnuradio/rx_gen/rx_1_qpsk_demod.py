from __future__ import division
import numpy as np
import random
import scipy
import math
import os
import matplotlib.pyplot as plt

def lrange(r1, inc, r2):
	"""Provide spacing as an input and receive samples back by wrapping `
	numpy.linspace (basically colon operator in matlab r1:inc:r2)"""
	n = ((r2-r1)+2*np.spacing(r2-r1))//inc
	return np.linspace(r1,r1+inc*n,n+1)

#################
# QPSK Receiver #
#################
FILE_NAME_OUT = "rx1.npy"

qpskModfile = scipy.fromfile(open("tx_out.bin"), dtype=scipy.float32)
# max length that can be used is 569940 based on the imported oscillators
MAX = 569940
iterations = len(qpskModfile)/MAX
if len(qpskModfile)%MAX != 0:
    pad = MAX - len(qpskModfile)%MAX
else:
    pad = 0
qpskMod = np.empty(len(qpskModfile) + pad, dtype=np.float32)
for i in range(0, len(qpskMod)):
	if i < len(qpskModfile):
		qpskMod[i] = qpskModfile[i]
	else:
		qpskMod[i] = 0

var = np.load("tx_vars.npy")
N = var[0]
Fs = var[1]
Rb = var[2]
Fc = 2*Rb
Tb = 1/Rb

in_phase_osc = np.load("in_phase_osc.npy") # FROM qpsk mod
quad_phase_osc = np.load("quad_phase_osc.npy") # FROM qpsk mod

i_signal = np.array(MAX)
q_signal = np.zeros(MAX)
data_out = np.zeros(0,dtype=np.int)
# Multiply received signal with the reference oscillators

for i in range(0,int(iterations)):

    i_signal = np.multiply(qpskMod[i*MAX:i*MAX+MAX],in_phase_osc)
    q_signal = np.multiply(qpskMod[i*MAX:i*MAX+MAX],quad_phase_osc)

    # The multiplied output is integrated over one bit period using an
    # integrator. A threshold detector makes a decision on each integrated bit based on a threshold. Since an
    # NRZ signaling format is used with equal amplitudes in positive and negative direction, the threshold for
    # this case would be 0
    integration_base = lrange(0, 1/Fs, Tb - 1/Fs)
    in_phase_component = np.zeros(int(len(i_signal)/(Tb*Fs)+1))
    quad_phase_component = np.zeros(int(len(i_signal)/(Tb*Fs)+1))
    for i in range(0, int( len(i_signal)/(Tb*Fs) )):
    	in_phase_component[i] = np.trapz(y = i_signal[ int(i*Tb*Fs) : int((i+1)*Tb*Fs) ], x=integration_base)
    for i in range(0, int( len(q_signal)/(Tb*Fs) )):
    	quad_phase_component[i] = np.trapz(y = q_signal[ int(i*Tb*Fs) : int((i+1)*Tb*Fs)], x=integration_base)

    # Threshold Detector
    estimated_in_bits = np.zeros(int(N/2))
    estimated_in_bits = (in_phase_component >= 0)
    estimated_in_bits = estimated_in_bits.astype(int)

    estimated_quad_bits = np.zeros(int(N/2))
    estimated_quad_bits = (quad_phase_component >= 0)
    estimated_quad_bits = estimated_quad_bits.astype(int)

    merged = np.hstack( zip(estimated_in_bits, estimated_quad_bits) )
    data_out = np.append(data_out,merged)

	print data_out
	
np.save(FILE_NAME_OUT,data_out)

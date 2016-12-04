from __future__ import division
import numpy as np
import random
import math
import matplotlib.pyplot as plt
from scipy.fftpack import fft

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

##########
# Gen Data
##########
N = 50
data = np.zeros(N,dtype=np.int)
for i in range(0,N-1):
    if(random.randint(0,999) >= 500):
        data[i] = 1

##################
# QPSK Modulator #
##################

# N=100 # data bits
Rb=1e3 # bit rate
amplitude = 1 # amp of NRZ data
odd_bits = np.zeros(N/2,dtype=np.int)
even_bits = np.zeros(N/2,dtype=np.int)

# Split into I and Q streams
even_bits = data[0::2] # I (even)
odd_bits = data[1::2] # Q (odd)

plt.subplot(2,2,1)
plt.stem(data)
plt.title("Input Data")
plt.xlabel("Samples")
plt.ylabel("mag")
plt.axis([0, N, -.25, 1.25])

even_time, even_NRZ_data, Fs = NRZ_Encoder(even_bits, Rb, amplitude)
odd_time, odd_NRZ_data, Fs = NRZ_Encoder(odd_bits, Rb, amplitude)

Fc = 2*Rb;
in_phase_osc = 1/np.sqrt(2)*np.cos(2*np.pi*Fc*even_time)
quad_phase_osc = 1/np.sqrt(2)*np.sin(2*np.pi*Fc*odd_time)
qpskMod = np.multiply(odd_NRZ_data,quad_phase_osc) + np.multiply(even_NRZ_data,in_phase_osc)
Tb = 1/Rb

plt.subplot(2,2,2)
plt.plot(qpskMod)
plt.title("Modulated Data")
plt.xlabel("time")
plt.ylabel("mag")

#################
# Add some AWGN #
#################
var = 0.3
mean = 0.5
noise = np.random.normal(mean,var,len(qpskMod))
received = noise + qpskMod

plt.subplot(2,2,3)
plt.plot(received)
plt.title("Modulated Data w/ AWGN")
plt.xlabel("time")
plt.ylabel("mag")

#################
# QPSK Receiver #
#################
i_signal = np.array(len(qpskMod))
q_signal = np.zeros(len(qpskMod))
# Multiply received signal with the reference oscillators
i_signal = np.multiply(received,in_phase_osc)
q_signal = np.multiply(received,quad_phase_osc)

# The multiplied output is integrated over one bit period using an
# integrator. A threshold detector makes a decision on each integrated bit based on a threshold. Since an
# NRZ signaling format is used with equal amplitudes in positive and negative direction, the threshold for
# this case would be 0
integration_base = lrange(0, 1/Fs, Tb - 1/Fs)
in_phase_component = np.zeros(len(i_signal)/(Tb*Fs)+1)
quad_phase_component = np.zeros(len(i_signal)/(Tb*Fs)+1)
for i in range(0, int( len(i_signal)/(Tb*Fs) )):
    in_phase_component[i] = np.trapz(y = i_signal[ int(i*Tb*Fs) : int((i+1)*Tb*Fs) ], x=integration_base)
    print(int(i*Tb*Fs))
for i in range(0,int( len(q_signal)/(Tb*Fs) )):
    quad_phase_component[i] = np.trapz(y = q_signal[ int(i*Tb*Fs) : int((i+1)*Tb*Fs)], x=integration_base)

# Threshold Detector
estimated_in_bits = np.zeros(N/2)
estimated_in_bits = (in_phase_component >= 0)
estimated_in_bits = estimated_in_bits.astype(int)

estimated_quad_bits = np.zeros(N/2)
estimated_quad_bits = (quad_phase_component >= 0)
estimated_quad_bits = estimated_quad_bits.astype(int)

data_out = np.hstack( zip(estimated_in_bits, estimated_quad_bits) )
BER = sum(1 for a,b in zip(data, data_out) if a != b)/N*100
print "BER = {}%".format(BER)

plt.subplot(2,2,4)
plt.stem(data_out)
plt.title("Output Data")
plt.xlabel("Samples")
plt.ylabel("mag")
plt.axis([0, N, -.25, 1.25])
plt.show()

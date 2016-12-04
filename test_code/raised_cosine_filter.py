# Raised Cosine Filter

# todo: compare runs to C implementation

from __future__ import division # makes all division true mathematical div
import numpy as np              # for arrays
import matplotlib.pyplot as plt # for debug plotting
import math                     # for science
import random

L     = 100      # filter length
R     = 1*10**6  # data rate = 1 Mbps
Fs    = 8*R      # oversampling by 8
T     = 1/R
Ts    = 1/Fs
alpha = 0.5      # design factor for RCF; determines BW of pulse and how rapidly tails cut off
pi    = math.pi

################
# Filter Design
################
# check if even or odd number of taps
if(L%2 == 0):
	M = int(L/2)
else:
	M = int((L-1)/2)
g = np.zeros(L) # place holder for the TF

# Generate Transfer Function
for n in range(-M,M):
	if((1-(2*alpha*n*Ts*pi/T)**2) == 0):
		g[n+M] = pi/4 * math.sin(pi*n*Ts/T)/(pi*n*Ts/T)
	if (n==0):
		g[n+M] = math.cos(alpha*pi*n*Ts/T)/(1-(2*alpha*n*Ts/T)**2)
	else:
		num = math.sin(pi*n*Ts/T)*math.cos(alpha*pi*n*Ts/T)
		den = (pi*n*Ts/T)*(1-(2*alpha*n*Ts/T)**2)
		if den == 0:
				den = prevDen
		g[n+M] = num/den
		prevDen = den

# Plot Transfer Function
plt.subplot(2,2,1)
plt.plot(range(0,L),g)
title = "Raised Cosine Transfer Function: alpha = "+str(alpha)
plt.title(title)
plt.grid(True)
plt.xlabel('samples')
plt.ylabel('magnitude')

####################
# Generate Test Data
####################
data_size = 100
data = np.zeros(data_size) # polar encoding: 1 = +1V, 0 = -1V
for i in range(0,data_size):
	if(random.randint(0,1000) >= 500):
		data[i] = 1
	else:
		data[i] = -1

# Plot input data
plt.subplot(2,2,2)
plt.plot(range(0,len(data)),data, linestyle='steps--')
plt.ylim(-2,2)
plt.title('Input data')
plt.xlabel('samples')
plt.ylabel('magnitude: +1V = 1, -1V = 0')

# up sample test-data by factor of Fs/R, or the oversampling value
up_data = np.zeros(data_size*Fs/R)
for i in range(0,data_size):
	up_data[i*Fs/R] = data[i]
	for j in range(1,int(Fs/R)):
		up_data[i*Fs/R + j] = 0

###########################
# Convolve data with filter
###########################
output = np.convolve(g,up_data)

# Plot Result
plt.subplot(2,2,3)
plt.plot(range(0,len(output)),output)
plt.title('Data Convolved with Filter')
plt.grid(True)
plt.xlabel('samples')
plt.ylabel('magnitude')

# re-convolve and plot
plt.subplot(2,2,4)
gp = g[::-1]
received = np.convolve(gp,output)
plt.plot(range(0,len(received)),received)
plt.title('Received after reconvolution')
plt.grid(True)
plt.xlabel('samples')
plt.ylabel('magnitude')
plt.show()

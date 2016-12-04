#!/bin/bash/python2.7

#######################
# Convolutional Encoder
# (stand alone)
# http://users.ece.utexas.edu/~gerstl/ee382v-ics_f09/lectures/Viterbi.pdf
# http://users.ece.utexas.edu/~gerstl/ee382v-ics_f09/lectures/Viterbi_Tutorial.pdf
# http://web.mit.edu/6.02/www/f2011/handouts/8.pdf
#######################

# TODO: Need to standardize size of packets... packets MUST be a power of 2 for
# the interleaver to work probably

import numpy as np
import random
import math

packet_size = 5
input_stream = np.empty(packet_size,dtype=np.int)
for i in range(0,packet_size):
    if(random.randint(0,999)>500):
        input_stream[i] = 1
    else:
        input_stream[i] = 0
output_stream = np.zeros(len(input_stream)*2+2, dtype=np.int)   # len_2x+2
selA = np.zeros(len(input_stream)+2, dtype=np.int)
selB = np.zeros(len(input_stream)+2, dtype=np.int)

# r=1/2 k=3 Convolutional Encoder
# ff0 = ff1 = 0
# for i in range(0,len(input_stream)+2):
#     if i>=len(input_stream):
#         selA[i] = 0 ^ ff0 ^ ff1
#         selB[i] = 0 ^ ff1
#         ff1 = ff0
#         ff0 = 0
#     else:
#         selA[i] = input_stream[i] ^ ff0 ^ ff1
#         selB[i] = input_stream[i] ^ ff1
#         ff1 = ff0
#         ff0 = input_stream[i]
# output_stream = np.hstack( zip(selA,selB) )

# r=1/2 k=6 [171,133] Convolutional Encoder
ff1 = ff2 = ff3 = ff4 = ff5 = ff6 = 0
for i in range(0,len(input_stream)+2):
    if i>=len(input_stream):
        selA[i] = 0 ^ ff2 ^ ff3 ^ ff5 ^ ff6
        selB[i] = 0 ^ ff1 ^ ff2 ^ ff3 ^ ff6
        ff6 = ff5
        ff5 = ff4
        ff4 = ff3
        ff3 = ff2
        ff2 = ff1
        ff1 = 0
    else:
        selA[i] = input_stream[i] ^ ff2 ^ ff3 ^ ff5 ^ ff6
        selB[i] = input_stream[i] ^ ff1 ^ ff2 ^ ff3 ^ ff6
        ff6 = ff5
        ff5 = ff4
        ff4 = ff3
        ff3 = ff2
        ff2 = ff1
        ff1 = input_stream[i]
output_stream = np.hstack( zip(selA,selB) )
print output_stream

#############
# Interleaver
#############
# print("before interleaver...")
# print(len(output_stream))
# print("")
#
# mat_dim = int(math.sqrt(len(output_stream)))
# print(np.sqrt(len(output_stream)))
# mat_dim = int(math.sqrt(len(output_stream)))
# interleave_mat = np.zeros((mat_dim,mat_dim), dtype=np.int)
# interleave_out = np.zeros(mat_dim**2, dtype=np.int)
#
# for i in range(0,mat_dim):
#     for j in range(0,mat_dim):
#         interleave_mat[i][j] = output_stream[i*mat_dim + j]
# for i in range(0,mat_dim):
#     for j in range(0,mat_dim):
#         interleave_out[i*mat_dim + j] = interleave_mat[j][i]

# #######################
# # Simulate Burst Errors
# #######################
# errors = packet_size/4
# print "simulating with {} burst errors".format(errors)
# for i in range(0,errors):
#     interleave_out[len(interleave_out)/2+i] = 0
# # output_stream = interleave_out

################
# De-Interleaver
################
# deinterleave_mat = np.zeros((mat_dim,mat_dim), dtype=np.int)
# deinterleave_out = np.zeros(mat_dim**2, dtype=np.int)
# for i in range(0,mat_dim):
#     for j in range(0,mat_dim):
#         deinterleave_mat[i][j] = interleave_out[i*mat_dim + j]
# for i in range(0,mat_dim):
#     for j in range(0,mat_dim):
#         deinterleave_out[i*mat_dim + j] = deinterleave_mat[j][i]
# output_stream = deinterleave_out
#
# print("after interleaver")
# print(output_stream)

#######################################
# Simulate Burst Errors w/o interleaver
# (comment out the sim burst errors code AND output_stream)
#######################################
# errors = 75
# print "simulating with no interleaving and {} burst errors".format(errors)
# for i in range(0,errors):
#     output_stream[len(output_stream)/2+i] = 0

###################
# Viterbi Decoder #
###################

# returns hamming distance between two INTEGERS (by calculating binary hamming)
def ham10(x,y):
    '''
    x is first value, y is the second value
    IE 110 and 001 = hamming distance of 3 then
       6   and 1   = hamming distance of 3
    '''
    return bin(x^y).count('1')


# Convert (binary) symbols in output stream to 0,1,2,3
sym = np.zeros(len(output_stream)/2, dtype=np.int)
j = i = 0
while i < len(output_stream):
    if output_stream[i] == 0 and output_stream[i+1] == 0:
        sym[j] = 0
    elif output_stream[i] == 0 and output_stream[i+1] == 1:
        sym[j] = 1
    elif output_stream[i] == 1 and output_stream[i+1] == 0:
        sym[j] = 2
    elif output_stream[i] == 1 and output_stream[i+1] == 1:
        sym[j] = 3
    i += 2
    j += 1

########################
# Generate symbol errors
########################
# sym[2]=3
# sym[11]=0
# sym[6]=3

# calculate Accumulated Error Metrics (aem)
aem = np.zeros((len(sym),4), dtype=np.int) # (index, state#0-3)

# t0->t1
aem[0,0] = ham10(sym[0], 0)
aem[0,1] = aem[0,3] = 666  # these will never be a valid starting state
aem[0,2] = ham10(sym[0], 3)

# t1->t2
aem[1,0] = ham10(sym[1], 0) + aem[0,0]
aem[1,1] = ham10(sym[1], 2) + aem[0,2]
aem[1,2] = ham10(sym[1], 3) + aem[0,0]
aem[1,3] = ham10(sym[1], 1) + aem[0,2]

# t2 -> t_end
for i in range(2,len(sym)):

    # aem for state zero
    if ( ham10(sym[i], 0) + aem[(i-1),0] <= ham10(sym[i], 3) + aem[(i-1),1] ):
        aem[i,0] = ham10(sym[i], 0) + aem[(i-1),0]
    else:
        aem[i,0] = ham10(sym[i], 3) + aem[(i-1),1]

    # aem for state one
    if ( ham10(sym[i], 2) + aem[(i-1),2] <= ham10(sym[i], 1) + aem[(i-1),3] ):
        aem[i,1] = ham10(sym[i], 2) + aem[(i-1),2]
    else:
        aem[i,1] = ham10(sym[i], 1) + aem[(i-1),3]

    # aem for state two
    if ( ham10(sym[i], 3) + aem[(i-1),0] <= ham10(sym[i], 0) + aem[(i-1),1] ):
        aem[i,2] = ham10(sym[i], 3) + aem[(i-1),0]
    else:
        aem[i,2] = ham10(sym[i], 0) + aem[(i-1),1]

    # aem for state three
    if ( ham10(sym[i], 1) + aem[(i-1),2] <= ham10(sym[i], 2) + aem[(i-1),3] ):
        aem[i,3] = ham10(sym[i], 1) + aem[(i-1),2]
    else:
        aem[i,3] = ham10(sym[i], 2) + aem[(i-1),3]

# These states are invalid choices for traceback == inf
aem[len(sym)-1,3] = aem[len(sym)-1,2] = aem[len(sym)-1,1] = aem[len(sym)-2,3] = \
aem[len(sym)-2,2] = 666

# Traceback to receive origin states
stht = np.zeros(len(sym),dtype=np.int) # state history table
current_state = 0 # current best path state
for i in range(len(sym)-1,0,-1):
    if current_state == 0: # prev possible states are 0 and 1
        if aem[i,0] < aem[i,1]:
            stht[i] = 0
        elif aem[i,0] > aem[i,1]:
            stht[i] = 1
        else:
            print("Error S0: equal error metrics during traceback")
            stht[i] = 0 # arbitrary assignment
    elif current_state == 1: # prev possible states are 2 and 3
        if aem[i,2] < aem[i,3]:
            stht[i] = 2
        elif aem[i,2] > aem[i,3]:
            stht[i] = 3
        else:
            print("Error S1: equal error metrics during traceback")
            stht[i] = 3 # arbitrary assignment
    elif current_state == 2: # prev possible states are 0 and 1
        if aem[i,0] < aem[i,1]:
            stht[i] = 0
        elif aem[i,0] > aem[i,1]:
            stht[i] = 1
        else:
            print("Error S2: equal error metrics during traceback")
            stht[i]=0 # arbitrary assignment
    else: # prev possible states are 2 and 3
        if aem[i,2] < aem[i,3]:
            stht[i] = 2
        elif aem[i,2] > aem[i,3]:
            stht[i] = 3
        else:
            print("Error S3: equal error metrics during traceback")
            stht[i] = 3 # arbitrary assignment
    current_state = stht[i]

# Inserts the (guaranteed) initial first zero state
stht = np.insert(stht,0,0)

# Decode bitstream from state history table
decoded_message = np.zeros(len(sym),dtype=np.int)
for i in range(0,len(stht)-1):
    if stht[i+1] < stht[i] or stht[i+1] == stht[i] and stht[i] == 0:
        decoded_message[i] = 0
    elif stht[i+1] > stht[i] or stht[i+1] == stht[i] and stht[i] == 3:
        decoded_message[i] = 1
decoded_message = np.delete(decoded_message,-1)

# print input and decoded streams
print("input stream (len {}): ").format(len(input_stream))
print(input_stream)
print("decoded message (len {}): ").format(len(decoded_message))
print(decoded_message)

# count errors
error_count = sum(1 for a,b in zip(input_stream, decoded_message) if a != b)
print "number of errors = {}".format(error_count)

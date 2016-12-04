import numpy as np
import math
from fifo_ops import *

# returns hamming distance between two INTEGERS (by calculating binary hamming)
def ham10(x,y):
    '''
    x is first value, y is the second value
    IE 110 and 001 = hamming distance of 3 then
       6   and 1   = hamming distance of 3
    '''
    return bin(x^y).count('1')

FILE_NAME_IN = "rx1.fifo"
FILE_NAME_OUT = "rx2.fifo"

output_stream = read_pipe(FILE_NAME_IN)

###################
# Viterbi Decoder #
###################

# Convert (binary) symbols in output stream to 0,1,2,3
sym = np.zeros(len(output_stream)/2, dtype=np.int8)
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

# calculate Accumulated Error Metrics (aem)
aem = np.zeros((len(sym),4), dtype=np.int8) # (index, state#0-3)

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
stht = np.zeros(len(sym),dtype=np.int8) # state history table
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
decoded_message = np.zeros(len(sym),dtype=np.int8)

for i in range(0,len(stht)-1):
    if stht[i+1] < stht[i] or stht[i+1] == stht[i] and stht[i] == 0:
        decoded_message[i] = 0
    elif stht[i+1] > stht[i] or stht[i+1] == stht[i] and stht[i] == 3:
        decoded_message[i] = 1
decoded_message = np.delete(decoded_message,-1)

write_pipe(decoded_message, FILE_NAME_OUT)

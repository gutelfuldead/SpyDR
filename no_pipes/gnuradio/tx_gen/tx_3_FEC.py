#!/bin/bash/python2.7

import numpy as np
import math

############    ###############    ############
# Tx1.fifo # -> # tx_3_FEC.py # -> # tx2.fifo #
############    ###############    ############

# tx_3_FEC.py Does R=1/2 convolutional encoding and 1D Interleaving
# Packet size must be power of 2 MINUS 2

################
# Conv Encoder #
################
FILE_NAME_IN = "tx1.npy" # replace w/ tx1.fifo
FILE_NAME_OUT = "tx2.npy"

input_stream = np.load(FILE_NAME_IN)
N = len(input_stream)
output_stream = np.zeros(len(input_stream)*2+2, dtype=np.int)   # len_2x
selA = np.zeros(len(input_stream)+2, dtype=np.int)
selB = np.zeros(len(input_stream)+2, dtype=np.int)

# r=1/2 k=3 Convolutional Encoder
ff0 = ff1 = 0
for i in range(0,len(input_stream)+2):
    if i>=len(input_stream):
        selA[i] = 0 ^ ff0 ^ ff1
        selB[i] = 0 ^ ff1
        ff1 = ff0
        ff0 = 0
    else:
        selA[i] = input_stream[i] ^ ff0 ^ ff1
        selB[i] = input_stream[i] ^ ff1
        ff1 = ff0
        ff0 = input_stream[i]
output_stream = np.hstack( zip(selA,selB) )

print("fec len = {}").format(len(output_stream))
#############
# Interleaver
#############

## FIXME: Interleaver is broken because it relies on symmetric nxn sized matrices
## however workaround is using original message lengths of 2**2 - 2 bytes

# mat_dim = int(math.sqrt(len(output_stream)))
# interleave_mat = np.zeros((mat_dim,mat_dim), dtype=np.int)
# interleave_out = np.zeros(mat_dim**2, dtype=np.int)
# for i in range(0,mat_dim):
#     for j in range(0,mat_dim):
#         interleave_mat[i][j] = output_stream[i*mat_dim + j]
# for i in range(0,mat_dim):
#     for j in range(0,mat_dim):
#         interleave_out[i*mat_dim + j] = interleave_mat[j][i]


np.save(FILE_NAME_OUT,output_stream)

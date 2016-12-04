#!/bin/bash/python2.7

import numpy as np
import math
from fifo_ops import *

############    ###############    ############
# Tx1.fifo # -> # tx_3_FEC.py # -> # tx2.fifo #
############    ###############    ############
INPUT_NAME = "tx1.fifo"
OUTPUT_NAME = "tx2.fifo"

input_stream = read_pipe(INPUT_NAME)
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

write_pipe(output_stream, OUTPUT_NAME)

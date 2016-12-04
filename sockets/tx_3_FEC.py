#!/usr/bin/python2.7

import numpy as np
import math
import time
import os
from socket_funcs import *
from bool_func import *

############    ###############    ############
# Tx1.fifo # -> # tx_3_FEC.py # -> # tx2.fifo #
############    ###############    ############
socket_in = './tx2_send.uds'
socket_out= './tx3_send.uds'

# Open Server Socket
s = open_socket_serv(socket_out)

while (1):
    input_stream = socket_recv(socket_in)
    data = int_to_bool(input_stream)

    N = len(data)
    output_stream = np.empty(len(data)*2+2, dtype=np.int8)
    selA = np.empty(len(data)+1, dtype=np.int8)
    selB = np.empty(len(data)+1, dtype=np.int8)

    # r=1/2 k=3 Convolutional Encoder
    ff0 = ff1 = 0
    for i in range(0,len(data)+1):
        if i>=len(data):
            selA[i] = 0 ^ ff0 ^ ff1
            selB[i] = 0 ^ ff1
            ff1 = ff0
            ff0 = 0
        else:
            selA[i] = data[i] ^ ff0 ^ ff1
            selB[i] = data[i] ^ ff1
            ff1 = ff0
            ff0 = data[i]

    output_stream = np.hstack( zip(selA,selB) )
    # output_stream = pack_bits(output_stream)
    socket_serv(s, output_stream)

s.close()

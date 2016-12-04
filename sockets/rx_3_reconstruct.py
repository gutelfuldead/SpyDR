#!/usr/bin/python2.7

import numpy as np
import os
from socket_funcs import *
from bool_func import *
import time

socket_in = './rx2_send.uds'

while(1):

    t0 = time.time()
    data = socket_recv(socket_in)
    ttl = time.time() - t0

    # data = unpack_bits(in_stream)
    decode=[]
    a = ''
    for i in range(0,len(data)):
        a = a + str(data[i])
        if ((i+1)%8 == 0 and i !=0):
            decode.append(a)
            a = ''
    # print decode
    message=''
    for i in range(0,len(decode)):
        message = message + chr(int(decode[i],2))

    Bps = int(2*len(message)/ttl)
    print("Total time (tx and rx): %0.3fs, size of data: %d bytes :: %d Bps")%(ttl, len(message), Bps)

    path = os.getcwd()
    path = path + '/output_data.bin'
    data_file = open(path, "wb")
    data_file.write(message)
    data_file.close()

#
# while (1):
#
#     t0 = time.time()
#     data = socket_recv(socket_in)
#     ttl = time.time() - t0
#
#     # data = unpack_bits(data)
#
#     decode=[]
#     a = ''
#     for i in range(0,len(data)):
#         a += str(data[i])
#         if ((i+1)%8 == 0 and i !=0):
#             decode.append(a)
#             a = ''
#
#     message=''
#     for i in range(0,len(decode)):
#         message += chr(int(decode[i],2))
#     Bps = int(2*len(message)/ttl)
#     # print("Total time (tx and rx): %0.3fs, size of data: %d bytes :: %d Bps")%(ttl, len(message), Bps)
#
#     print "\n\nTX\n\n"
#     print message
#
#     # path = os.getcwd()
#     # path = path + '/output_data.bin'
#     # data_file = open(path, "a")
#     # data_file.write(message)
#     # # data_file.write("\n\nTX\n\n")
#     # data_file.close()

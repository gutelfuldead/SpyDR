# import numpy as np
# import os
#
# ##################    #####################    ############
# # Input bin file # -> # tx_2_read_data.py # -> # tx1.fifo #
# ##################    #####################    ############
#
# FILE_NAME = "tx1.npy" # replace w/ tx1.fifo
# zz
# path = os.getcwd()
# path = path + '/' + "input_data.bin"
# fifo = open(path, "rb")
# for i in fifo:
# 		data = i
# fifo.close()
# # Make numpy vector of binary data from input bin
# a = np.zeros(8,dtype=np.int)
# bin_data = np.zeros(len(data)*8,dtype=np.int)
# for i in range(0,len(data)):
#     a = format(ord(data[i]),'b').zfill(8) # formats data in 8bit binary without the 0b prefix
#     for j in range(0,len(a)):
#         bin_data[i*len(a) + j] = a[j]
#
# np.save(FILE_NAME,bin_data)
# print("bit data size = {}").format(len(bin_data))

import numpy as np
import os

FILE_NAME = "tx1.npy" # replace w/ tx1.fifo

INPUT_NAME = 'raven_input.txt'

path = os.getcwd()
path = path + '/' + INPUT_NAME
data = ''
for d in range(0,2):
	fifo = open(path, "r")
	for i in fifo:
			data += i
	fifo.close()

# Make numpy vector of binary data from input bin
a = np.zeros(8,dtype=np.int)
bin_data = np.zeros(len(data)*8,dtype=np.int)
for i in range(0,len(data)):
    a = format(ord(data[i]),'b').zfill(8) # formats data in 8bit binary without the 0b prefix
    for j in range(0,len(a)):
        bin_data[i*len(a) + j] = a[j]

np.save(FILE_NAME,bin_data)
print("bit data size = {}").format(len(bin_data))

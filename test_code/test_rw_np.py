# using numpy save/load make this bullshit work

import numpy as np
import random
import os

##################    #####################    ############
# Input bin file # -> # tx_2_read_data.py # -> # tx1.fifo #
##################    #####################    ############

FILE_NAME = "tx1.bin" # replace w/ tx1.fifo

path = os.getcwd()
path = path + '/' + "input_data.bin"
fifo = open(path, "rb")
for i in fifo:
		data = i
fifo.close()
# Make numpy vector of binary data from input bin
a = np.zeros(8,dtype=np.int)
bin_data = np.zeros(len(data)*8,dtype=np.int)
ind = 0
for i in range(0,len(data)):
    a = format(ord(data[i]),'b').zfill(8) # formats data in 8bit binary without the 0b prefix
    for j in range(0,len(a)):
        bin_data[ind] = a[j]
        ind += 1

np.save("test_data.npy", bin_data)
# write_fifo(bin_data, FILE_NAME)
a = np.load("test_data.npy")
print(a)

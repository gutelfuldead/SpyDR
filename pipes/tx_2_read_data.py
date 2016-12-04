"""
This block reads an input binary file and converts the message to a sequence of
binary files saved as a numpy int8 array and passed to a FIFO pipe

Runs until broken

##################    #####################    ############
# Input bin file # -> # tx_2_read_data.py # -> # tx1.fifo #
##################    #####################    ############
"""
import numpy as np
import os
from fifo_ops import write_pipe

INPUT_NAME = "input_data.bin"
OUTPUT_NAME = "tx1.fifo"
path = os.getcwd()
path = path + '/' + INPUT_NAME
a = np.zeros(8,dtype=np.int8)

# Read binary file and format it to 1s and 0s for further processing
fifo = open(path, "r")
for i in fifo:
		data = i
fifo.close()

# print "Input Data: {}".format(data)

bin_data = np.zeros(len(data)*8,dtype=np.int8)
# each i is a character byte in data string
for i in range(0,len(data)):
	# formats data in 8bit binary without the 0b prefix
    a = format(ord(data[i]),'b').zfill(8)
    for j in range(0,len(a)):
        bin_data[i*len(a) + j] = a[j]

write_pipe(bin_data,OUTPUT_NAME)

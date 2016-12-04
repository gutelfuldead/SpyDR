#!/bin/bash/python2.7

###################################
# Create test data for transmission
###################################

# import numpy as np
# import random
# import os
# from fifo_ops import write_fifo
#
# data_size = 10
# fl = float(12.23)
# integer = int(123456789)
# # data = "This is a test, here are some float values: {}, here are some int values: {}".format(fl,integer)
# data = "This is a test {} {}".format(fl, integer) # MESSAGE LENGTH IS 2**2 - 2 BYTES
#
# write_fifo(data, "input_data.bin")

import numpy as np
import random
import os

data_size = 512
data = np.random.randint(0,2,data_size)
tx=''
for i in range(0,data_size):
    tx += str(data[i])

print "Input data length = {} bytes".format(len(tx))
path = os.getcwd()
path = path + '/input_data.bin'
data_file = open(path, "wb")
data_file.write(tx)
data_file.close()

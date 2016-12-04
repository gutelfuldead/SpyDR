import numpy as np
import os

def read_fifo(file_name):
    """
    Reads from a file and converts whatever the contents are to a binary represented
    numpy vector without the "0b" prefix and standard width of 8.
    IE 3 --> [0,0,0,0,0,0,1,1]
    """
    path = os.getcwd()
    path = path + '/' + file_name
    fifo = open(path, "r")
    data = []
    for i in fifo:
    		data.append(i)
    data = np.array(data)
    # data = data.astype('i8')
    fifo.close()
    # # Make numpy vector of binary data from input bin
    # a = np.zeros(8,dtype=np.int)
    # bin_data = np.zeros(len(data)*8,dtype=np.int)
    # ind = 0
    # for i in range(0,len(data)):
    #     a = format(ord(data[i]),'b').zfill(8) # formats data in 8bit binary without the 0b prefix
    #     for j in range(0,len(a)):
    #         bin_data[ind] = a[j]
    #         ind += 1
    # return bin_data
    return data

def write_fifo(input_data, file_name):
    """
    Writes input_data to file_name
    """
    path = os.getcwd() + '/' + file_name
    fifo = open(path, "w")
    fifo.write(input_data)
    fifo.close()

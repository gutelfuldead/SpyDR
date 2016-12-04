#!/usr/bin/python2.7
# buffer interface for data passing

import cPickle as pickle
import json
import os

def getSize(filename):
    st = os.stat(filename)
    return st.st_size

# holds data in file buffer
def write_buffer(buff_name, data):
    data_p = pickle.dumps(data)
    N = str(len(data_p))
    N += '\n'

    with open(buff_name, "wb") as myfile:
        myfile.write(N) # length of data section
        myfile.write(data_p)
        myfile.write("\nIM STILL ALIVE\0")
    return

def read_buffer(buff_name):
    size = getSize(buff_name)
    print size
    with open(buff_name, "r+b") as myfile:
        N = int(myfile.readline())
        data_p = myfile.read(N)
        # myfile.seek(N,2)
        # myfile.truncate()
    data = pickle.loads(data_p)
    return data

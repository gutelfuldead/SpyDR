#!/bin/python
import os
import numpy as np
import cPickle as pickle

def write_pipe(data,pipename):
    try:
        os.mkfifo(pipename)
        print("Pipe {} was created by write_pipe").format(pipename)
    except:
        pass

    pipe = os.open(pipename, os.O_WRONLY)
    data_l = data.tolist()

    # Send pickled Array size
    data_p = pickle.dumps(data_l)
    Np = str(len(data_p))
    Np = Np.rjust(6,'0') # pad str(N) to be 6 char
    os.write(pipe,Np)

    #### TEST data
    with open("input.txt","w") as text_file:
        text_file.write(data_p)

    os.write(pipe, data_p)

    print("serv: raw data len = {}, pickld len = {}").format(len(data),len(data_p))
    os.close(pipe)
    return

def read_pipe(pipename):
    pipe = os.open(pipename, os.O_RDONLY)
    Np = int(os.read(pipe,6)) # total size of file to be sent
    data_p = ''
    data_p = os.read(pipe, Np)
    os.close(pipe)

    with open("output.txt","w") as text_file:
        text_file.write(data_p)

    data_l = pickle.loads(data_p)
    data = np.asarray(data_l)

    print("recv: raw data len = {}, pickld len = {}").format(len(data),len(data_p))
    return data

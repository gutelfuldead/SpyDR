#!/usr/bin/python2.7
import os
import numpy as np
import cPickle as pickle

MAX_PACKET = 4096

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

    if int(Np) > MAX_PACKET:
        A = int(Np)/MAX_PACKET
        for i in range(0,A):
            os.write(pipe, data_p[i*MAX_PACKET:i*MAX_PACKET+MAX_PACKET])
        os.write(pipe, data_p[ -(int(Np) % MAX_PACKET) : ]) # send leftover data
    else:
        os.write(pipe, data_p)

    print("serv: raw data len = {}, pickld len = {}").format(len(data),len(data_p))
    os.close(pipe)
    return

def read_pipe(pipename):
    pipe = os.open(pipename, os.O_RDONLY)
    Np = int(os.read(pipe,6)) # total size of file to be sent

    data_p = ''
    if Np > MAX_PACKET:
        A = Np/MAX_PACKET
        for i in range(0,A):
            data_p += os.read(pipe, MAX_PACKET )  # recv A packets of size Np/MAX_PACKET
        data_p += os.read(pipe, Np % MAX_PACKET ) # recv leftover data
    else:
        data_p = os.read(pipe,Np)
    os.close(pipe)
    data_l = pickle.loads(data_p)
    data = np.asarray(data_l)

    with open("output.txt","w") as text_file:
        text_file.write(data_p)

    print("recv: raw data len = {}, pickld len = {}").format(len(data),len(data_p))
    return data


# import os
# import numpy as np
#
# def write_np_int_fifo(data, fifoname):
#     """
#     Input is dtype=np.int8,
#     first writes the length of the array then
#     ints individually as a chr
#     BLOCKING
#     """
#     try:
#         os.mkfifo(fifoname)
#     except:
#         pass
#
#     N = str(len(data))
#     N = N.rjust(4,'0') # pad str(N) to be 4 char long if it isn't
#     pipe = os.open(fifoname, os.O_WRONLY)
#     os.write(pipe, N) # First thing read is the length of the array
#
#     # Sequentially write array to pipe
#     for i in range(0,int(N)):
#         os.write(pipe, chr(data[i]))
#     os.close(pipe)
#     return
#
# def read_np_int_fifo(fifoname):
#     """
#     Returns size of array, N, then dtype=np.int8 values
#     reads chr input and converts to int with ord
#     BLOCKING
#     """
#     try:
#         os.mkfifo(fifoname)
#     except:
#         pass
#
#     pipe = os.open(fifoname, os.O_RDONLY)
#     N = int(os.read(pipe,4)) # recover N
#     read = np.empty(N,dtype=np.int8)
#
#     for i in range(0,N):
#         read[i] = ord(os.read(pipe,1))
#     os.close(pipe)
#     return read
#
# def write_np_flt_fifo(data, fifoname):
#     """
#     Input is dtype=np.float16,
#     first writes the length of the array then
#     writes %1.4f formatted float values as string of 6 bytes
#     BLOCKING
#     """
#     try:
#         os.mkfifo(fifoname)
#     except:
#         pass
#
#     N = str(len(data))
#     N = N.rjust(4, '0')
#     pipe = os.open(fifoname, os.O_WRONLY)
#     os.write(pipe, N) # send length of the array
#
#     for i in range(0,int(N)):
#         os.write(pipe, str("%+1.4f" % data[i]))
#     os.close(pipe)
#     return
#
# def read_np_flt_fifo(fifoname):
#     """
#     Reads float values from pipe and saves as dtype=np.float16
#     BLOCKING
#     """
#     try:
#         os.mkfifo(fifoname)
#     except:
#         pass
#
#     pipe = os.open(fifoname, os.O_RDONLY)
#     N = int(os.read(pipe,4)) # recover N
#
#     read = np.empty(N,dtype=np.float16)
#     for i in range(0,N):
#         read[i] = float(os.read(pipe,7))
#     os.close(pipe)
#     return read

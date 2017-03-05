# UNIX DOMAIN SOCKETS (UDS) CODE OPENING SOCKETS LOCALLY
'''
$ cat /proc/sys/net/ipv4/tcp_rmem # ubuntu 14.04lts 64x
4096	87380	6291456
$ cat /proc/sys/net/ipv4/tcp_wmem # ubuntu 14.04lts 64x
4096	16384	4194304
min      def      max    memory size values in byte for buffers sizes
'''
import socket
import os
import sys
import cPickle as pickle
import numpy as np
import errno
from socket import error as socket_error
import time

def open_socket_serv(addr):
    try:
        os.unlink(addr)
    except OSError:
        if os.path.exists(addr):
            raise
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.bind(addr)
    return s


def socket_serv(s, data):
    """
    Uses cPickle to send data to connected client port at addr
    """

    s.listen(1) # One maximum connection at a time
    c, addr = s.accept()

    # print len(data)

    data_l = data.tolist() # convert to list
    data_p = pickle.dumps(data_l) # serialize with pickle
    Np = str(len(data_p))
    Np = Np.rjust(10,'0') # left pad 0 to 10 bytes
    c.send(str(Np)) # send how much data to expect
    c.send(data_p)  # send data
    c.close()

    return

def socket_recv(addr):
    """
    Uses cPickle to unpickle the data received from server port @ addr
    returns the data set (numpy or otherwise)
    """
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    # Keep checking for data an ignore the connection refused error
    connected = False
    while (connected != None):
        try:
            connected = s.connect(addr)
        except socket_error as serr:
            pass
    # Receive Np Bytes into data_p
    Np = int(s.recv(10)) # INITAL PICKLE SIZE
    data_p = ''
    while(len(data_p) < Np):
        data_p += s.recv(Np)

    # Check if all data was received before unpickling
    if (len(data_p) != Np):
        print "All data was not received"
        s.close()
        sys.exit()
    else:
        # Convert back to numpy
        data_l = pickle.loads(data_p)
        data = np.asarray(data_l)

    s.close()

    # if( isinstance(data[0],np.int64) ):
    #     data = data.astype(dtype=np.int8)
    # if( isinstance(data[0],np.float64) ):
    #     data = data.astype(dtype=np.float16)

    return data

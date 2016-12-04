# UNIX DOMAIN SOCKETS (UDS) CODE OPENING SOCKETS LOCALLY
'''
$ cat /proc/sys/net/ipv4/tcp_rmem # ubuntu 14.04lts 64x
4096	87380	6291456
$ cat /proc/sys/net/ipv4/tcp_wmem # ubuntu 14.04lts 64x
4096	16384	4194304
min      def      max    memory size values in byte for buffers sizes

Maximum size of (N) for floating point 16380
Maximum size of (N) for int is 10k????
'''
import socket
import os
import sys
import cPickle as pickle
import numpy as np
import time
import errno
from socket import error as socket_error

MAX_PACKET = 32768

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

    t0 = time.time()

    s.listen(1) # One maximum connection at a time
    c, addr = s.accept()

    # Send pickled Array size, convert to list
    data_l = data.tolist()
    data_p = pickle.dumps(data_l)
    Np = str(len(data_p))
    Np = Np.rjust(10,'0') # pad str(N) to be 6 char
    c.send(str(Np))
    c.send(data_p)

    c.close()

    ttl_time = time.time() - t0
    print("serv: pack_size = {}, raw data len = {}, pickld len = {}, ttl_time = {}, elem_1 = {}").format(MAX_PACKET, len(data),len(data_p),ttl_time,data[0])

    return

def socket_recv(addr):
    """
    Uses cPickle to unpickle the data received from server port @ addr
    returns the data set (numpy or otherwise)
    """
    t0 = time.time()

    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

    a = 1
    while (a != None):
        try:
            a = s.connect(addr)
        except socket_error as serr:
            pass


    Np = int(s.recv(10)) # INITAL PICKLE SIZE
    data_p = ''
    while(len(data_p) < Np):
        data_p += s.recv(Np)

    # Convert back to numpy
    data_l = pickle.loads(data_p)
    data = np.asarray(data_l)

    ttl_time = time.time() - t0

    print("recv: pack_size = {}, raw data len = {}, pickld len = {}, ttl_time = {}, elem_1 = {}").format(MAX_PACKET, len(data),len(data_p),ttl_time,data[0])
    s.close
    return data

# # UNIX DOMAIN SOCKETS (UDS) CODE
# '''
# $ cat /proc/sys/net/ipv4/tcp_rmem # ubuntu 14.04lts 64x
# 4096	87380	6291456
# $ cat /proc/sys/net/ipv4/tcp_wmem # ubuntu 14.04lts 64x
# 4096	16384	4194304
# min      def      max    memory size values in byte for buffers sizes
#
# Maximum size of (N) for floating point 16380
# Maximum size of (N) for int is 10k????
# '''
# import socket
# import os
# import sys
# import cPickle as pickle
# import numpy as np
# import time
#
# MAX_PACKET = 32768
#
# def socket_serv(addr, data):
#     """
#     Uses cPickle to send data to connected client port at addr
#     """
#     try:
#         os.unlink(addr)
#     except OSError:
#         if os.path.exists(addr):
#             raise
#
#     s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
#     # prevents socket blocking on next connection
#     s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#
#     s.bind(addr)
#     s.listen(1) # One maximum connection at a time
#     c, addr = s.accept()
#
#     # Send pickled Array size, convert to list
#     data_l = data.tolist()
#     data_p = pickle.dumps(data_l)
#     Np = str(len(data_p))
#     Np = Np.rjust(10,'0') # pad str(N) to be 6 char
#     c.send(str(Np))
#
#     # OK! Find out how to send in chunks of 10k or less
#     # if N <= 10k no problem just send!
#     # if N > 10k send in groups of A...
#     # A = N/10k; send A packets then one packet of N%10k
#     if int(Np) > MAX_PACKET:
#         A = int(Np)/MAX_PACKET
#         for i in range(0,A):
#             c.send(data_p[i*MAX_PACKET:i*MAX_PACKET+MAX_PACKET])
#         c.send(data_p[-(int(Np) % MAX_PACKET):]) # send leftover data
#     else:
#         c.send(data_p)
#     c.close()
#     s.close()
#
#     ttl_time = time.time() - t0
#     print("serv: pack_size = {}, raw data len = {}, pickld len = {}, ttl_time = {}, elem_1 = {}").format(MAX_PACKET, len(data),len(data_p),ttl_time,data[0])
#
#     return
#
# def socket_recv(addr):
#     """
#     Uses cPickle to unpickle the data received from server port @ addr
#     returns the data set (numpy or otherwise)
#     """
#
#     t0 = time.time()
#
#     s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
#     s.connect(addr)
#
#
#     Np = int(s.recv(10)) # INITAL PICKLE SIZE
#     data_p = ''
#     if Np > MAX_PACKET:
#         A = Np/MAX_PACKET
#         for i in range(0,A):
#             data_p += s.recv( MAX_PACKET )  # recv A packets of size Np/MAX_PACKET
#         data_p += s.recv( Np % MAX_PACKET ) # recv leftover data
#     else:
#         data_p = s.recv(Np)
#
#     # Convert back to numpy
#     data_l = pickle.loads(data_p)
#     data = np.asarray(data_l)
#
#     ttl_time = time.time() - t0
#
#     print("recv: pack_size = {}, raw data len = {}, pickld len = {}, ttl_time = {}, elem_1 = {}").format(MAX_PACKET, len(data),len(data_p),ttl_time,data[0])
#     s.close
#     return data




# TCP CODE
# '''
# $ cat /proc/sys/net/ipv4/tcp_rmem # ubuntu 14.04lts 64x
# 4096	87380	6291456
# $ cat /proc/sys/net/ipv4/tcp_wmem # ubuntu 14.04lts 64x
# 4096	16384	4194304
# min      def      max    memory size values in byte for buffers sizes
#
# Maximum size of (N) for floating point 16380
# Maximum size of (N) for int is 10k????
# '''
# import socket
# import os
# import sys
# import cPickle as pickle
# import numpy as np
#
# MAX_PACKET = 16384
#
# def socket_serv(port_name, data):
#     """
#     Uses cPickle to send data to connected client port at port_name
#     """
#     # Investigate AF_UNIX
#     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     # prevents socket blocking on next connection
#     s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#     host = socket.gethostname()
#     s.bind((host,port_name))
#     s.listen(1) # One maximum connection at a time
#     c, addr = s.accept()
#
#     # Send pickled Array size, convert to list
#     data_l = data.tolist()
#     data_p = pickle.dumps(data_l)
#     Np = str(len(data_p))
#     Np = Np.rjust(10,'0') # pad str(N) to be 6 char
#     c.send(str(Np))
#     print("serv: pack_size = {}, raw data len = {}, pickld len = {}").format(MAX_PACKET, len(data),len(data_p))
#
#     #### TEST data
#     with open("input.txt","w") as text_file:
#         text_file.write(data_p)
#
#     # OK! Find out how to send in chunks of 10k or less
#     # if N <= 10k no problem just send!
#     # if N > 10k send in groups of A...
#     # A = N/10k; send A packets then one packet of N%10k
#     if int(Np) > MAX_PACKET:
#         A = int(Np)/MAX_PACKET
#         for i in range(0,A):
#             c.send(data_p[i*MAX_PACKET:i*MAX_PACKET+MAX_PACKET])
#         c.send(data_p[-(int(Np) % MAX_PACKET):]) # send leftover data
#     else:
#         c.send(data_p)
#     c.close()
#     s.close()
#     return
#
# def socket_recv(port_name):
#     """
#     Uses cPickle to unpickle the data received from server port @ port_name
#     returns the data set (numpy or otherwise)
#     """
#     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     host = socket.gethostname()
#     s.connect((host,port_name))
#
#     Np = int(s.recv(10)) # INITAL PICKLE SIZE
#     data_p = ''
#     if Np > MAX_PACKET:
#         A = Np/MAX_PACKET
#         for i in range(0,A):
#             data_p += s.recv( MAX_PACKET )  # recv A packets of size Np/MAX_PACKET
#         data_p += s.recv( Np % MAX_PACKET ) # recv leftover data
#     else:
#         data_p = s.recv(Np)
#
#     with open("output.txt","w") as text_file:
#         text_file.write(data_p)
#
#     # Convert back to numpy
#     data_l = pickle.loads(data_p)
#     data = np.asarray(data_l)
#
#     print("recv: pack_size = {}, raw data len = {}, pickld len = {}").format(MAX_PACKET, len(data),len(data_p))
#     s.close
#     return data

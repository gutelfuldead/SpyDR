#!/usr/bin/python2.7

# Sockets Test Code
from sockets_functions import socket_serv, open_socket_serv
import numpy as np

N = 1000000
addr = './uds_socket'
s = open_socket_serv(addr)

# a = np.random.random(N)
# socket_serv(s, a)

for i in range(N/2, N):
    a = np.random.random(i)
    socket_serv(s,a)
    # sleep(0.05)

s.close()

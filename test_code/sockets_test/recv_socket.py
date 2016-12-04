#!/usr/bin/python2.7

# Client Test
from sockets_functions import socket_recv
import numpy as np

N = 1000000
# socket = 12333
addr = './uds_socket'
# data_in = socket_recv(socket)

while(1):
    data_in = socket_recv(addr)

s.close

#!/usr/bin/python2.7

import numpy as np
from socket_funcs import *
####################
# Add some AWGN    #
# and burst errors #
####################

# Using np float now

var = 0.3
mean = 0.7
burstErrors = 0

sock_in = './tx4_send.uds'
sock_out= './channel_send.uds'

# Open Server Socket
s = open_socket_serv(sock_out)

while(1):
    qpskMod = socket_recv(sock_in)
    noise = np.random.normal(mean,var,len(qpskMod))
    # channel = noise + qpskMod
    channel = qpskMod
    # generate burst errors
    # for i in range(len(qpskMod)/2, len(qpskMod)/2+burstErrors):
    #     channel[i] = 0
    socket_serv(s, channel)

s.close()

#!/usr/bin/python2.7
"""
This block reads an input binary file and converts the message to a sequence of
binary files saved as a numpy int8 array and passed to a FIFO pipe

Runs until broken

##################    #####################    ############
# Input bin file # -> # tx_2_read_data.py # -> # tx1.fifo #
##################    #####################    ############
"""
import numpy as np
import os
import time
from socket_funcs import socket_serv, open_socket_serv

INPUT_NAME = "input_data.bin"
# INPUT_NAME = 'raven_input.txt'
socket_out = './tx2_send.uds'

# Open Server Socket
s = open_socket_serv(socket_out)

path = os.getcwd()
path = path + '/' + INPUT_NAME

# while(1):
#
# 	fifo = open(path, "r")
# 	for i in fifo:
# 			data = i
# 	fifo.close()
# 	# print data
#
# 	tx = np.fromstring(data,dtype=np.int8)
# 	# print tx
# 	socket_serv(s, tx)
# s.close()


while(1):

	fifo = open(path, "r")
	data = ''
	for i in fifo:
			data += i
	fifo.close()

	send_size = 512 # bytes
	A = len(data)/send_size
	pad = send_size - len(data)%send_size

	int_data = np.empty(len(data)+pad,dtype=np.int8)
	for i in range(0,len(int_data)):
		if i < len(data):
			int_data[i] = ord(data[i])
		else:
			int_data[i] = ord('.')

	# for i in range(0,len(data)):
	# 	if (chr(int_data[i]) != data[i]):
	# 		print "ERROR ERROR"

	for i in range(0,A):
		socket_serv(s,int_data[i*send_size:i*send_size+send_size])

s.close()

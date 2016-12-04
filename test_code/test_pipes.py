#########################################################
# named pipes; os.mkfifo not avaiable on Windows 95/98;
# no reason to fork here, since fifo file pipes are
# external to processes--shared fds are irrelevent;
#########################################################

import os, time, sys
import numpy as np
fifoname = './pipefifo'                       # must open same name

def child():
    a = np.zeros(100,dtype=np.int)
    for i in range(0,len(a)):
        if (np.random.randint(0,100) >= 50):
            a[i] = 1
    print(a)
    pipeout = os.open(fifoname, 'wb')     # open fifo pipe file as fd
    for i in range (0,len(a)):
        os.write(pipeout, a[i])
    os.close(pipeout)

def parent():
    pipein = open(fifoname, 'rb')                 # open fifo as stdio object
    while 1:
        line = pipein.readline(  )[:-1]            # blocks until data sent
        print(line)

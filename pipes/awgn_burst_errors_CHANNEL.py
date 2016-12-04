import numpy as np
from fifo_ops import *

####################
# Add some AWGN    #
# and burst errors #
####################

# Using np float now

INPUT_NAME = "tx3.fifo"
OUTPUT_NAME = "channel.fifo"
var = 0.3
mean = 0.7
burstErrors = 0

qpskMod = read_pipe(INPUT_NAME)
noise = np.random.normal(mean,var,len(qpskMod))
channel = noise + qpskMod
# generate burst errors
for i in range(len(qpskMod)/2, len(qpskMod)/2+burstErrors):
    channel[i] = 0
write_pipe(channel,OUTPUT_NAME)

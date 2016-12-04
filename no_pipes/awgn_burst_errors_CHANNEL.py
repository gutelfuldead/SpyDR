import numpy as np

####################
# Add some AWGN    #
# and burst errors #
####################

qpskMod = np.load("tx3.npy")

var = 0.3
mean = 0.7
noise = np.random.normal(mean,var,len(qpskMod))
channel = noise + qpskMod

burstErrors = 0
for i in range(len(qpskMod)/2, len(qpskMod)/2+burstErrors):
    channel[i] = 0

np.save("channel.npy",channel)

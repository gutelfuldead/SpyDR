import numpy as np
import random

N = 100
message0 = np.zeros(N,dtype=np.int)
message1 = np.zeros(N,dtype=np.int)
message2 = np.zeros(N,dtype=np.int)

for i in range(0,N):
	if(random.randint(0,999) > 500):
		message0[i] = 1
	if(random.randint(0,999)>500):
		message1[i] = 1
	if(random.randint(0,999)>500):
		message2[i] = 1

PN0 = [1,0,1,1,1,0,0]
PN0s = PN0
PN1 = [1,0,0,1,0,1,1]
PN2 = [0,1,1,1,0,0,1]

PN0message0 = np.zeros(N*len(PN0), dtype=np.int)
PN1message1 = np.zeros(N*len(PN0), dtype=np.int)
PN2message2 = np.zeros(N*len(PN0), dtype=np.int)
channel_message = np.zeros(N*len(PN0), dtype=np.int)
for i in range(0,len(message0)):
	for j in range(0,len(PN0)):
		PN0message0[i*len(PN0)+j] = message0[i]^PN0[j]
		PN1message1[i*len(PN0)+j] = message1[i]^PN1[j]
		PN2message2[i*len(PN0)+j] = message2[i]^PN2[j]

channel_message = PN0message0 + PN1message1 + PN2message2

# Find auto-correlation values
atocor = np.zeros(len(PN0),dtype=np.int) # holds auto correlation values
for i in range(0,len(PN0)):
	for j in range(0,len(PN0)):
		# if(PN0[j] == 0):
		# 	PN0[j] = -1
		# elif PN0s[j] == -1:
		# 	PN0s[j] = -1
		atocor[i] = atocor[i] + PN0[j]*PN0s[j]
	print("PN0s i={}: {}: auto-correlation = {}").format(i,PN0s,atocor[i])
	PN0s = np.roll(PN0s,1)

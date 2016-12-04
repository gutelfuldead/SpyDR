n = 3 

# initalize registers with arbitrary values (except all zero vector)
r0 = 0 # reg 0
r1 = 0 # reg 1
r2 = 1 # reg 2
mseq1 = []
mseq2 = []
gold  = []

# generate m-sequence 1, x^3+x^2+1
for i in range(0,2**n): # loop for 2^n - 1 times
	r0_n = r2 ^ r1
	r1_n = r0
	r2_n = r1
	# print("mseq1 state: ",i)
	# print(r0_n, r1_n, r2_n)
	r0 = r0_n
	r1 = r1_n
	r2 = r2_n
	tmp_lst=[r0,r1,r2]
	mseq1 = mseq1 + tmp_lst
print("mseq1:     ",mseq1)

r0 = 1
r1 = 1
r2 = 0
# generate m-sequence 2, x^3+x+1
for i in range(0,2**n):
	r0_n = r2 ^ r0
	r1_n = r0
	r2_n = r1
	# print("mseq2 state: ",i)
	# print(r0_n, r1_n, r2_n)
	r0 = r0_n
	r1 = r1_n
	r2 = r2_n
	tmp_lst=[r0,r1,r2]
	mseq2 = mseq2 + tmp_lst
print("mseq2:     ",mseq2)

# generate gold code
for i in range(0,len(mseq1)):	gold.append(mseq1[i]^mseq2[i])
print("gold code: ",gold)

<!-- # **SpyDR** -->
SpyDR
=====

Software (python) Defined Radio

Written for 2016 Summer Internship at Nasa Goddard Flight Center. 

Demo Forward Error Correction and QPSK Mod/Demod on dataset.

Example SDR workflow in Python using Unix Domain Sockets (UDS) to connect all modules. 

To Use
------
`./python/RUNALL_SDR.sh` to autostart all the python modules. Ctrl+C will end all of the running modules and clean up data.

`./python/verifyData.sh` will compare the input and output binaries via md5sum. Needs to be fixed since when killing the RUNALL_SDR script data may be in the process of being written to the binary causing a mismatch. 

Sequence of events
------------------

1. `tx_1_create_data.py` create test data, random integers

2. `tx_2_read_data.py` takes input data and generates packets of 512 bytes

3. `tx_3_FEC.py` performs rate 1/2, k = 3 convolutional encoding on the packets

4. `tx_4_qpsk_mod.py` performs NRZ encoding of data then performs qpsk modulation generating I and Q data

5. `awgn_burst_errors_CHANNEL.py` adds awgn and burst errors to the data (burst currently disabled)

6. `rx_1_qpsk_demod.py` demodulates data based on hard decisions

7. `rx_2_decode.py` (slow) implementation of Viterbi algorithm

8. `rx_3_reconstruct.py` reconstructs integers from bitstream and writes to output.bin

Socket Ports
------------

| file name | read in socket | write out socket|
|-----------|---------------|-----------------|
|tx_1_create_data.py | n/a | n/a |
|tx_2_read_data.py | n/a | tx2_send |
|tx_3_FEC.py | tx2_send | tx3_send |
|tx_4_qpsk_mod.py | tx3_send | tx4_send |
|awgn_burst_errors_CHANNEL.py | tx4_send | channel_send |
|rx_1_qpsk_demod.py | channel_send | rx1_send |
|rx_2_decode.py | rx1_send | rx2_send |
|rx_3_reconstruct.py | rx2_send | n/a |


VHDL
----

Convolutional Encoder core was generated in vhdl but never tested in implementation.


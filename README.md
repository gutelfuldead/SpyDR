<!-- # **SpyDR** -->

## production notes

* Don't worry about interleaving :white_check_mark:

* use sockets or shared memory pipe between modules

* <del> modularize all of the tx / rx components and create a single script to prevent the necessity of using pipes or other data sharing means (keep all the data in a single script)

* Could use a shared memory mailbox sort of approach

* Keep a buffer between each module to keep data always ready for transmission (FIFO BLOCK)

* USRP takes as an input baseband complex qpsk I and Q channels; it will do the upconversion to carrier and the I/Q combination

sdsoc xilinx

## App notes

### Socket Ports

| file name | readin socket | write out socket|
|-----------|---------------|-----------------|
|tx_1_create_data.py | n/a | n/a |
|tx_2_read_data.py | n/a | tx2_send |
|tx_3_FEC.py | tx2_send | tx3_send |
|tx_4_qpsk_mod.py | tx3_send | tx4_send |
|awgn_burst_errors_CHANNEL.py | tx4_send | channel_send |
|rx_1_qpsk_demod.py | channel_send | rx1_send |
|rx_2_decode.py | rx1_send | rx2_send |
|rx_3_reconstruct.py | rx2_send | n/a |

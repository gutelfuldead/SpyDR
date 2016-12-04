#!/bin/bash
# SpyDR (SOFTWARE  python2.7  DEFINED RADIO)
# Run the full TX/RX chain

mkfifo rx1.fifo rx2.fifo tx1.fifo tx2.fifo tx3.fifo channel.fifo

sleep 1

echo "running tx_1_create_data"
python2.7  tx_1_create_data.py
echo "running tx_2_read_data"
python2.7  tx_2_read_data.py &
echo "running tx_3_FEC"
python2.7  tx_3_FEC.py &
echo "running tx_4_qpsk_mod"
python2.7  tx_4_qpsk_mod.py &
echo "running awgn_burst_errors_CHANNEL"
python2.7  awgn_burst_errors_CHANNEL.py &
echo "running rx_1_qpsk_demod"
python2.7  rx_1_qpsk_demod.py &
echo "running rx_2_decode"
python2.7  rx_2_decode.py &
echo "running rx_3_reconstruct"
python2.7  rx_3_reconstruct.py &


# wait
#
# # Comparing input and output files
# echo "Comparing md5sum of input and output bins..."
# INPUTmd5=$(md5sum input_data.bin)
# INPUT=${INPUTmd5:0:32}
# OUTPUTmd5=$(md5sum output_data.bin)
# OUTPUT=${OUTPUTmd5:0:32}
# echo "Input: " $INPUT
# echo "Output: "$OUTPUT
#
# if [ "$INPUT" = "$OUTPUT" ]; then
#   echo "Output matches input"
# else
#   echo "Output does NOT match input"
# fi
#
# echo "--cleaning up--"
# rm *.bin *.fifo

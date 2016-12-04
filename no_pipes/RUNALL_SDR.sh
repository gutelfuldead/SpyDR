#!/bin/bash
# SpyDR (SOFTWARE python DEFINED RADIO)
# Run the full TX/RX chain

# TX Chain
echo "--Starting TX Chain--"
python tx_1_create_data.py
startTX=$(($(date +%s%N)/1000000))
python tx_2_read_data.py
python tx_3_FEC.py
python tx_4_qpsk_mod.py
endTX=$(($(date +%s%N)/1000000))
durationTX=`expr $endTX - $startTX`
echo "Tx took $durationTX ms"
echo "======================"

# Add channel noise/burst
echo "--Adding noise--"
python awgn_burst_errors_CHANNEL.py
echo "============"

# RX Chain
echo "--Starting RX chain--"
startRX=$(($(date +%s%N)/1000000))
python rx_1_qpsk_demod.py
python rx_2_decode.py
endRX=$(($(date +%s%N)/1000000))
python rx_3_reconstruct.py
durationRX=`expr $endRX - $startRX`
echo "Rx took $durationRX ms"

echo "===================="
ttl=`expr $durationRX + $durationTX`
echo "Total time $ttl ms"
echo "===================="

# Comparing input and output files
echo "Comparing md5sum of input and output bins..."
INPUTmd5=$(md5sum raven_input.txt)
INPUT=${INPUTmd5:0:32}
OUTPUTmd5=$(md5sum output_data.bin)
OUTPUT=${OUTPUTmd5:0:32}
echo "Input: " $INPUT
echo "Output: "$OUTPUT

if [ "$INPUT" = "$OUTPUT" ]; then
  echo "Output matches input"
else
  echo "Output does NOT match input"
fi

cat output_data.bin

echo "--cleaning up--"
rm *.npy *.bin

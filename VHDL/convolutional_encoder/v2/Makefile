GHDL=ghdl
GHDLFLAGS=
MODULES=\
		conv_encoder_top.o \
		conv_encoder.o \
		d_ff.o \
		tb_conv_encoder \

test: $(MODULES)
				./tb_conv_encoder --vcd=wave_output.vcd
# Binary depends on the object file
%: %.o
				$(GHDL) -e $(GHDLFLAGS) $@

# Object file depends on source
%.o: %.vhd
				$(GHDL) -a $(GHDLFLAGS) $<

all:

clean:
				echo "Cleaning up..."
				rm -f *.o *_testbench work*.cf e*.lst conv_encoder_top conv_encoder d_ff fsm tb_conv_encoder *vcd

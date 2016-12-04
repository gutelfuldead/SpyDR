#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: SpyDR_TCPSOURCE
# Generated: Wed Aug  3 15:45:08 2016
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from grc_gnuradio import blks2 as grc_blks2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import wx


class SpyDR_TCPSOURCE(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="SpyDR_TCPSOURCE")
        _icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
        self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 200e3

        ##################################################
        # Blocks
        ##################################################
        self.nb = self.nb = wx.Notebook(self.GetWin(), style=wx.NB_TOP)
        self.nb.AddPage(grc_wxgui.Panel(self.nb), "waveform")
        self.nb.AddPage(grc_wxgui.Panel(self.nb), "fft")
        self.nb.AddPage(grc_wxgui.Panel(self.nb), "waterfall")
        self.nb.AddPage(grc_wxgui.Panel(self.nb), "histogram")
        self.Add(self.nb)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_float*1, "/home/afx/SDR/SpyDR/no_pipes/gnuradio/rx_gen/rx_in.bin", False)
        self.blocks_file_sink_0.set_unbuffered(False)
        self.blks2_tcp_source_0 = grc_blks2.tcp_source(
        	itemsize=gr.sizeof_float*1,
        	addr="192.168.56.101",
        	port=12345,
        	server=True,
        )

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blks2_tcp_source_0, 0), (self.blocks_file_sink_0, 0))    

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate


def main(top_block_cls=SpyDR_TCPSOURCE, options=None):

    tb = top_block_cls()
    tb.Start(True)
    tb.Wait()


if __name__ == '__main__':
    main()

#!/usr/bin/env python
########### VIDEO_STREAMER 

import gobject, pygst
pygst.require("0.10")
import gst
import gobject
import sys
import os
import readline

REMOTE_HOST = '192.168.33.153'
WRITE_VIDEO_CAPS = 'video.caps'

mainloop = gobject.MainLoop()
pipeline = gst.Pipeline('server')
bus = pipeline.get_bus()

dv1394src = gst.element_factory_make("dv1394src", "dv1394src")
dvdemux = gst.element_factory_make("dvdemux", "dvdemux")
q1 = gst.element_factory_make("queue", "q1")
q2 = gst.element_factory_make("queue", "q2")
dvdec = gst.element_factory_make("dvdec", "dvdec")
videoscale = gst.element_factory_make('videoscale')
ffmpegcs = gst.element_factory_make("ffmpegcolorspace", "ffmpegcs")
capsfilter = gst.element_factory_make('capsfilter')
capsfilter.set_property('caps', gst.caps_from_string('video/x-raw-yuv, width=320, height=240'))
tcpsrc = gst.element_factory_make("tcpserversrc", "source")
x264enc = gst.element_factory_make("x264enc", "x264enc")
x264enc.set_property('qp-min', 18)
rtph264pay = gst.element_factory_make("rtph264pay", "rtph264pay")
udpsink_rtpout = gst.element_factory_make("udpsink", "udpsink0")
udpsink_rtpout.set_property('host', REMOTE_HOST)
udpsink_rtpout.set_property('port', 10000)
udpsink_rtcpout = gst.element_factory_make("udpsink", "udpsink1")
udpsink_rtcpout.set_property('host', REMOTE_HOST)
udpsink_rtcpout.set_property('port', 10001)
udpsrc_rtcpin = gst.element_factory_make("udpsrc", "udpsrc0")
udpsrc_rtcpin.set_property('port', 10002)

rtpbin = gst.element_factory_make('gstrtpbin', 'gstrtpbin')

# Add elements
pipeline.add(dv1394src, dvdemux, q1, dvdec, videoscale, ffmpegcs, capsfilter, x264enc, rtph264pay, rtpbin, udpsink_rtpout, udpsink_rtcpout, udpsrc_rtcpin)

# Link them
dv1394src.link(dvdemux)
def dvdemux_padded(dbin, pad):
    print "dvdemux got pad %s" % pad.get_name()
    if pad.get_name() == 'video':
        print "Linking dvdemux to queue1"
        dvdemux.link(q1)

# Create links
dvdemux.connect('pad-added', dvdemux_padded)

gst.element_link_many(q1, dvdec, videoscale, capsfilter, ffmpegcs, x264enc, rtph264pay)

rtph264pay.link_pads('src', rtpbin, 'send_rtp_sink_0')
rtpbin.link_pads('send_rtp_src_0', udpsink_rtpout, 'sink')
rtpbin.link_pads('send_rtcp_src_0', udpsink_rtcpout, 'sink')
udpsrc_rtcpin.link_pads('src', rtpbin, 'recv_rtcp_sink_0')

def go():
    print "Setting locked state for udpsink"
    print udpsink_rtcpout.set_locked_state(gst.STATE_PLAYING)
    print "Setting pipeline to PLAYING"
    print pipeline.set_state(gst.STATE_PLAYING)
    print "Waiting pipeline to settle"
    print pipeline.get_state()
    print "Final caps written to", WRITE_VIDEO_CAPS
    open(WRITE_VIDEO_CAPS, 'w').write(str(udpsink_rtpout.get_pad('sink').get_property('caps')))
    mainloop.run()

go()

#!/usr/bin/env python

import sys
import gobject, pygst
pygst.require("0.10")
import gst
import gobject
import sys
import os
import readline

AUDIO_DEV = 'hw:0,0'
VIDEO_DEV = '/dev/video0'
REMOTE_HOST = '192.168.1.4'
REMOTE_PORT = 9000
# WRITE_VIDEO_CAPS = 'video.caps'

mainloop = gobject.MainLoop()
pipeline = gst.Pipeline('server')
bus = pipeline.get_bus()

audiosrc = gst.element_factory_make("alsasrc", "alsasrc")
audiosrc.set_property('device',AUDIO_DEV)
videosrc = gst.element_factory_make("v4l2src", "v4l2src")
videosrc.set_property('device',VIDEO_DEV)
tcpsink = gst.element_factory_make("tcpserversink", "tcpserversink")
tcpsink.set_property("host",REMOTE_HOST)
tcpsink.set_property("port",REMOTE_PORT)
tcpsink.set_property("qos",True)
q1 = gst.element_factory_make("queue", "q1")
q2 = gst.element_factory_make("queue", "q2")
x264enc = gst.element_factory_make("x264enc", "x264enc")
x264enc.set_property('quantizer', 50)
x264enc.set_property('qp-min', 18)
rtph264pay = gst.element_factory_make("rtph264pay", "rtph264pay")

rtpbin = gst.element_factory_make('gstrtpbin', 'gstrtpbin')

pipeline.add(audiosrc, videosrc, q1, q2, x264enc, rtph264pay, rtpbin, tcpsink)
audiosrc.link(q1)
videosrc.link(q2)
gst.element_link_many(q2, x264enc, rtph264pay)

rtph264pay.link_pads('src', rtpbin, 'send_rtp_sink_0')
rtpbin.link_pads('send_rtp_src_0', tcpsink, 'sink')
# udpsrc_rtcpin.link_pads('src', rtpbin, 'recv_rtcp_sink_0')

def go():
    print "Setting locked state for udpsink"
    print tcpsink.set_locked_state(gst.STATE_PLAYING)
    print "Setting pipeline to PLAYING"
    print pipeline.set_state(gst.STATE_PLAYING)
    print "Waiting pipeline to settle"
    print pipeline.get_state()
    # print "Final caps written to", WRITE_VIDEO_CAPS
    # open(WRITE_VIDEO_CAPS, 'w').write(str(udpsink_rtpout.get_pad('sink').get_property('caps')))
    mainloop.run()

go()

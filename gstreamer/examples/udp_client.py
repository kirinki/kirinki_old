#!/usr/bin/env python

import gobject, pygst
pygst.require("0.10")
import gst
import sys
import os
import readline

# oggmux name=mux ! filesink location=test0.ogg
# v4l2src device=/dev/video0 ! video/x-raw-yuv,width=640,height=480 ! ffmpegcolorspace ! theoraenc ! queue ! mux.
# alsasrc device=hw:0,0 ! audio/x-raw-int,channels=2,depth=16 ! audioconvert ! queue ! vorbisenc ! mux.

REMOTE_HOST = '192.168.1.2'
REMOTE_PORT = 9000
WRITE_VIDEO_CAPS = 'video.caps'

mainloop = gobject.MainLoop()
pipeline = gst.Pipeline('client')

v4l2src = gst.element_factory_make("v4l2src", "src1")
v4l2src.set_property('device','/dev/video0')

capsfilter_video = gst.element_factory_make('capsfilter')
capsfilter_video.set_property('caps', gst.caps_from_string('video/x-raw-yuv, width=640, height=480'))

q1 = gst.element_factory_make("queue", "q1")

videoscale = gst.element_factory_make('videoscale')
ffmpegcs = gst.element_factory_make("ffmpegcolorspace", "ffmpegcs")
theoraenc = gst.element_factory_make("theoraenc", "theoraenc")
rtptheorapay = gst.element_factory_make("rtptheorapay", "rtptheorapay")
udpsink_rtpout = gst.element_factory_make("udpsink", "udpsink0")
udpsink_rtpout.set_property('host', REMOTE_HOST)
udpsink_rtpout.set_property('port', REMOTE_PORT)
udpsink_rtpout.set_property('sync', True)
udpsink_rtcpout = gst.element_factory_make("udpsink", "udpsink1")
udpsink_rtcpout.set_property('host', REMOTE_HOST)
udpsink_rtcpout.set_property('port', REMOTE_PORT+1)
udpsink_rtcpout.set_property('sync', True)
udpsrc_rtcpin = gst.element_factory_make("udpsrc", "udpsrc0")
udpsrc_rtcpin.set_property('port', REMOTE_PORT+2)

rtpbin = gst.element_factory_make('gstrtpbin', 'gstrtpbin')


# Add elements
pipeline.add(v4l2src, q1, videoscale, ffmpegcs, capsfilter_video, theoraenc, rtptheorapay, rtpbin, udpsink_rtpout, udpsink_rtcpout, udpsrc_rtcpin)

gst.element_link_many(v4l2src, q1, videoscale, capsfilter_video, ffmpegcs, theoraenc, rtptheorapay)

rtptheorapay.link_pads('src', rtpbin, 'send_rtp_sink_0')
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

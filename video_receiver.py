#!/usr/bin/env python
# -=- encoding: utf-8 -=-
################ VIDEO RECEIVER

import gobject, pygst
pygst.require("0.10")
import gst


# TODO: detect from the RTPSource element inside the GstRtpBin
REMOTE_HOST = '192.168.34.150'
READ_VIDEO_CAPS = 'video.caps'

pipeline = gst.Pipeline('server')

caps = open(READ_VIDEO_CAPS).read().replace('\\', '')
rtpbin = gst.element_factory_make('gstrtpbin', 'rtpbin')
rtpbin.set_property('latency', 400)
udpsrc_rtpin = gst.element_factory_make('udpsrc', 'udpsrc0')
udpsrc_rtpin.set_property('port', 10000)
udpsrc_caps = gst.caps_from_string(caps)
udpsrc_rtpin.set_property('caps', udpsrc_caps)
udpsrc_rtcpin = gst.element_factory_make('udpsrc', 'udpsrc1')
udpsrc_rtcpin.set_property('port', 10001)
udpsink_rtcpout = gst.element_factory_make('udpsink', 'udpsink0')
udpsink_rtcpout.set_property('host', REMOTE_HOST)
udpsink_rtcpout.set_property('port', 10002)

rtph264depay = gst.element_factory_make('rtph264depay', 'rtpdepay')
q1 = gst.element_factory_make("queue", "q1")
q2 = gst.element_factory_make("queue", "q2")
avimux = gst.element_factory_make('avimux', 'avimux')
filesink = gst.element_factory_make('filesink', 'filesink')
filesink.set_property('location', '/tmp/go.avi')

ffmpegcs = gst.element_factory_make("ffmpegcolorspace", "ffmpegcs")
ffdec264 = gst.element_factory_make('ffdec_h264', 'ffdec264')
autovideosink = gst.element_factory_make('autovideosink')

pipeline.add(rtpbin, udpsrc_rtpin, udpsrc_rtcpin, udpsink_rtcpout,
             rtph264depay, q1, avimux, ffdec264, autovideosink)

# Receive the RTP and RTCP streams
udpsrc_rtpin.link_pads('src', rtpbin, 'recv_rtp_sink_0')
udpsrc_rtcpin.link_pads('src', rtpbin, 'recv_rtcp_sink_0')
# reply with RTCP stream
rtpbin.link_pads('send_rtcp_src_0', udpsink_rtcpout, 'sink')
# Plus the RTP into the rest of the pipe...
def rtpbin_pad_added(obj, pad):
    print "PAD ADDED"
    print "  obj", obj
    print "  pad", pad
    rtpbin.link(rtph264depay)
rtpbin.connect('pad-added', rtpbin_pad_added)
gst.element_link_many(rtph264depay, q1, ffdec264, autovideosink)

def start():
    pipeline.set_state(gst.STATE_PLAYING)
    udpsink_rtcpout.set_locked_state(gst.STATE_PLAYING)
    print "Started..."

def loop():
    print "Running..."
    gobject.MainLoop().run()

if __name__ == '__main__':
    start()
    loop()

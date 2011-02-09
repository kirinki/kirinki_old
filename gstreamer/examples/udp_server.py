#!/usr/bin/env python

import gobject, pygst
pygst.require("0.10")
import gst

# Stream to:
LOCAL_HOST = '192.168.1.2'
LOCAL_PORT = 9000
READ_VIDEO_CAPS = 'video.caps'

pipeline = gst.Pipeline('server')

caps = open(READ_VIDEO_CAPS).read().replace('\\', '')
rtpbin = gst.element_factory_make('gstrtpbin', 'rtpbin')
rtpbin.set_property('latency', 400)
udpsrc_rtpin = gst.element_factory_make('udpsrc', 'udpsrc0')
udpsrc_rtpin.set_property('port', LOCAL_PORT)
udpsrc_caps = gst.caps_from_string(caps)
udpsrc_rtpin.set_property('caps', udpsrc_caps)
udpsrc_rtcpin = gst.element_factory_make('udpsrc', 'udpsrc1')
udpsrc_rtcpin.set_property('port', LOCAL_PORT+1)
udpsink_rtcpout = gst.element_factory_make('udpsink', 'udpsink0')
udpsink_rtcpout.set_property('host', LOCAL_HOST)
udpsink_rtcpout.set_property('port', LOCAL_PORT+2)
udpsink_rtcpout.set_property('sync', True)

rtptheoradepay = gst.element_factory_make('rtptheoradepay', 'rtpdepay')

q1 = gst.element_factory_make("queue", "q1")

caps0 = gst.element_factory_make("capsfilter", "caps0")
caps0.set_property('caps',gst.caps_from_string('audio/x-raw-int, endianness=(int)1234, signed=(boolean)true, width=(int)16, depth=(int)16, rate=(int)44100, channels=(int)2'))
caps1 = gst.element_factory_make("capsfilter", "caps1")
caps1.set_property('caps', gst.caps_from_string('video/x-raw-yuv, width=640, height=480'))
caps2 = gst.element_factory_make("capsfilter", "caps2")
caps2.set_property('caps', gst.caps_from_string('audio/x-raw-int, endianness=(int)1234, signed=(boolean)true, width=(int)16, depth=(int)16, rate=(int)44100, channels=(int)2'))

audioconvert = gst.element_factory_make("audioconvert")
vorbisdec = gst.element_factory_make('vorbisdec')
theoradec = gst.element_factory_make('theoradec', 'theoradec0')
vorbisenc = gst.element_factory_make('vorbisenc')
theoraenc = gst.element_factory_make('theoraenc', 'theoraenc0')

oggdemux = gst.element_factory_make('oggdemux', 'oggdemux')
oggmux = gst.element_factory_make('oggmux', 'oggmux')
filesink = gst.element_factory_make('filesink', 'filesink')
filesink.set_property('location', 'video.ogg')

audiosink = gst.element_factory_make('alsasink', 'sink0')
videosink = gst.element_factory_make('xvimagesink', 'sink1')

pipeline.add(rtpbin, udpsrc_rtpin, udpsrc_rtcpin, udpsink_rtcpout, rtptheoradepay, q1, oggdemux, theoradec, vorbisdec, audioconvert, audiosink, videosink)
# gst.element_link_many(tcpserversrc_audio, caps2, q1, audioconvert, caps0, audiosink)
# gst.element_link_many(tcpserversrc_video, q3, caps1, videosink)

# pipeline.add(tcpserversrc_video, q3, theoradec, ffmpegcs, theoraenc, q4, tcpserversrc_audio, q1, vorbisdec, audioconvert, q2, vorbisenc, oggmux, filesink)
# gst.element_link_many(tcpserversrc_audio, q1, vorbisdec, audioconvert, q2, vorbisenc, oggmux)
# gst.element_link_many(tcpserversrc_video, q3, theoradec, ffmpegcs, theoraenc, q4, oggmux)
# oggmux.link(filesink)

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
    rtpbin.link(rtptheoradepay)
rtpbin.connect('pad-added', rtpbin_pad_added)
gst.element_link_many(rtptheoradepay, q1, theoradec, videosink)


def start():
    pipeline.set_state(gst.STATE_PLAYING)
    udpsink_rtcpout.set_locked_state(gst.STATE_PLAYING)
    print "Started..."
    print pipeline.get_state()

def loop():
    print "Running..."
    gobject.MainLoop().run()

if __name__ == '__main__':
    start()
    loop()

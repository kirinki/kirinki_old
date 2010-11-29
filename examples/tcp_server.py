#!/usr/bin/env python

import gobject, pygst
pygst.require("0.10")
import gst

# Stream to:
LOCAL_HOST = '192.168.1.2'
LOCAL_PORT = 9000

pipeline = gst.Pipeline('server')

tcpserversrc_audio = gst.element_factory_make('tcpserversrc', 'src0')
tcpserversrc_audio.set_property('host', LOCAL_HOST)
tcpserversrc_audio.set_property('port', LOCAL_PORT)
tcpserversrc_audio.set_property('protocol', 1)

tcpserversrc_video = gst.element_factory_make('tcpserversrc', 'src1')
tcpserversrc_video.set_property('host', LOCAL_HOST)
tcpserversrc_video.set_property('port', LOCAL_PORT+1)
tcpserversrc_video.set_property('protocol', 1)

q1 = gst.element_factory_make("queue", "q1")
q2 = gst.element_factory_make("queue", "q2")
q3 = gst.element_factory_make("queue", "q3")
q4 = gst.element_factory_make("queue", "q4")

caps0 = gst.element_factory_make("capsfilter", "caps0")
caps0.set_property('caps',gst.caps_from_string('audio/x-raw-int, endianness=(int)1234, signed=(boolean)true, width=(int)16, depth=(int)16, rate=(int)44100, channels=(int)2'))
caps1 = gst.element_factory_make("capsfilter", "caps1")
caps1.set_property('caps', gst.caps_from_string('video/x-raw-yuv, width=640, height=480'))
caps2 = gst.element_factory_make("capsfilter", "caps2")
caps2.set_property('caps', gst.caps_from_string('audio/x-raw-int, endianness=(int)1234, signed=(boolean)true, width=(int)16, depth=(int)16, rate=(int)44100, channels=(int)2'))

audioconvert = gst.element_factory_make("audioconvert")
ffmpegcs = gst.element_factory_make("ffmpegcolorspace", "ffmpegcs")
# vorbisdec = gst.element_factory_make('vorbisdec')
# theoradec = gst.element_factory_make('theoradec', 'theoradec0')
vorbisenc = gst.element_factory_make('vorbisenc')
theoraenc = gst.element_factory_make('theoraenc', 'theoraenc0')

# oggmux = gst.element_factory_make('oggmux', 'oggmux')
# filesink = gst.element_factory_make('filesink', 'filesink')
# filesink.set_property('location', 'video.ogg')

audiosink = gst.element_factory_make('alsasink', 'sink0')
videosink = gst.element_factory_make('xvimagesink', 'sink1')

pipeline.add(tcpserversrc_video, caps1, q3, ffmpegcs, theoraenc, q4, tcpserversrc_audio, caps2, q1, audioconvert, caps0, q2, vorbisenc, audiosink, videosink)
gst.element_link_many(tcpserversrc_audio, caps2, q1, audioconvert, caps0, q2, audiosink)
gst.element_link_many(tcpserversrc_video, q3, ffmpegcs, caps1, q4, videosink)

# pipeline.add(tcpserversrc_video, q3, theoradec, ffmpegcs, theoraenc, q4, tcpserversrc_audio, q1, vorbisdec, audioconvert, q2, vorbisenc, oggmux, filesink)
# gst.element_link_many(tcpserversrc_audio, q1, vorbisdec, audioconvert, q2, vorbisenc, oggmux)
# gst.element_link_many(tcpserversrc_video, q3, theoradec, ffmpegcs, theoraenc, q4, oggmux)
# oggmux.link(filesink)

def start():
    print "Started..."
    pipeline.set_state(gst.STATE_PLAYING)
    print "Waiting pipeline to settle"
    print pipeline.get_state()

def loop():
    print "Running..."
    gobject.MainLoop().run()

if __name__ == '__main__':
    start()
    loop()

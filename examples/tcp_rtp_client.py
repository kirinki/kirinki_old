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

mainloop = gobject.MainLoop()
pipeline = gst.Pipeline('client')

alsasrc = gst.element_factory_make("alsasrc", "src0")
alsasrc.set_property('device','hw:0,0')
pipeline.add(alsasrc)

capsfilter_audio = gst.element_factory_make("capsfilter", "caps0")
capsfilter_audio.set_property('caps',gst.caps_from_string('audio/x-raw-int, depth=(int)16, channels=(int)2'))
pipeline.add(capsfilter_audio)

q1 = gst.element_factory_make("queue", "q1")
pipeline.add(q1)

audioconvert = gst.element_factory_make("audioconvert")
# vorbisenc = gst.element_factory_make("vorbisenc")
pipeline.add(audioconvert)

client_audio = gst.element_factory_make("tcpclientsink", "client0")
client_audio.set_property("host", REMOTE_HOST)
client_audio.set_property("port", REMOTE_PORT)
client_audio.set_property("protocol", 1)
pipeline.add(client_audio)

gst.element_link_many(alsasrc, capsfilter_audio, q1, audioconvert, client_audio)

v4l2src = gst.element_factory_make("v4l2src", "src1")
v4l2src.set_property('device','/dev/video0')
pipeline.add(v4l2src)

capsfilter_video = gst.element_factory_make('capsfilter')
capsfilter_video.set_property('caps', gst.caps_from_string('video/x-raw-yuv, width=640, height=480'))
pipeline.add(capsfilter_video)

q2 = gst.element_factory_make("queue", "q2")
pipeline.add(q2)

videoscale = gst.element_factory_make('videoscale')
ffmpegcs = gst.element_factory_make("ffmpegcolorspace", "ffmpegcs")
# theoraenc = gst.element_factory_make("theoraenc", "theoraenc")
pipeline.add(videoscale, ffmpegcs)

client_video = gst.element_factory_make("tcpclientsink", "client1")
client_video.set_property("host", REMOTE_HOST)
client_video.set_property("port", REMOTE_PORT+1)
client_video.set_property("protocol", 1)
pipeline.add(client_video)

gst.element_link_many(v4l2src, capsfilter_video, q2, videoscale, ffmpegcs, client_video)

def go():
    print "Setting pipeline to PLAYING"
    print pipeline.set_state(gst.STATE_PLAYING)
    print "Waiting pipeline to settle"
    print pipeline.get_state()
    mainloop.run()

go()

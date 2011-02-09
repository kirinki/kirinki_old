#!/usr/bin/env python
import pygst
pygst.require("0.10")
import gst
import pygtk
import gtk
 
# oggmux name=mux ! filesink location=test0.ogg
# v4l2src device=/dev/video0 ! video/x-raw-yuv,width=640,height=480 ! ffmpegcolorspace ! theoraenc ! queue ! mux.
# alsasrc device=hw:0,0 ! audio/x-raw-int,channels=2,depth=16 ! audioconvert ! queue ! vorbisenc ! mux.

AUDIO_DEV = 'hw:0,0'
VIDEO_DEV = '/dev/video0'
REMOTE_HOST = '192.168.1.2' 
REMOTE_PORT = 9000

class Main:
    def __init__(self):
        self.setupSimpleGTKWindow()
        self.createPipelineElements()
        self.setupPipeline()
        self.window.show_all()
 
    def setupSimpleGTKWindow(self):
        self.window = gtk.Window()
        self.vbox = gtk.VBox()
        self.da = gtk.DrawingArea()
        self.bb = gtk.HButtonBox()
        self.da.set_size_request(300,150)
        self.playButton = gtk.Button(stock='gtk-media-play')
        self.playButton.connect("clicked", self.OnPlay)
        self.stopButton = gtk.Button(stock='gtk-media-stop')
        self.stopButton.connect("clicked", self.OnStop)
        self.quitButton = gtk.Button(stock='gtk-quit')
        self.quitButton.connect("clicked", self.OnQuit)
        self.vbox.pack_start(self.da)
        self.bb.add(self.playButton)
        self.bb.add(self.stopButton)
        self.bb.add(self.quitButton)
        self.vbox.pack_start(self.bb)
        self.window.add(self.vbox)
 
    def createPipelineElements(self):
        # mainloop = gobject.MainLoop()
        self.pipeline = gst.Pipeline('client')

        self.alsasrc = gst.element_factory_make("alsasrc", "src0")
        self.alsasrc.set_property('device',AUDIO_DEV)

        self.capsfilter_audio = gst.element_factory_make("capsfilter", "caps0")
        self.capsfilter_audio.set_property('caps',gst.caps_from_string('audio/x-raw-int, depth=(int)16, channels=(int)2'))

        self.q1 = gst.element_factory_make("queue", "q1")

        self.audioconvert = gst.element_factory_make("audioconvert")
        # vorbisenc = gst.element_factory_make("vorbisenc")

        self.client_audio = gst.element_factory_make("tcpclientsink", "client0")
        self.client_audio.set_property("host", REMOTE_HOST)
        self.client_audio.set_property("port", REMOTE_PORT)
        self.client_audio.set_property("protocol", 1)

        self.v4l2src = gst.element_factory_make("v4l2src", "src1")
        self.v4l2src.set_property('device',VIDEO_DEV)

        self.capsfilter_video = gst.element_factory_make('capsfilter')
        self.capsfilter_video.set_property('caps', gst.caps_from_string('video/x-raw-yuv, width=640, height=480'))

        self.q2 = gst.element_factory_make("queue", "q2")

        self.videoscale = gst.element_factory_make('videoscale')
        self.ffmpegcs = gst.element_factory_make("ffmpegcolorspace", "ffmpegcs")
        # self.theoraenc = gst.element_factory_make("theoraenc", "theoraenc")

        self.client_video = gst.element_factory_make("tcpclientsink", "client1")
        self.client_video.set_property("host", REMOTE_HOST)
        self.client_video.set_property("port", REMOTE_PORT+1)
        self.client_video.set_property("protocol", 1)

    def setupPipeline(self):
        self.pipeline.add(self.alsasrc)
        self.pipeline.add(self.capsfilter_audio)
        self.pipeline.add(self.q1)
        self.pipeline.add(self.audioconvert)
        self.pipeline.add(self.client_audio)

        self.pipeline.add(self.v4l2src)
        self.pipeline.add(self.capsfilter_video)
        self.pipeline.add(self.q2)
        self.pipeline.add(self.videoscale, self.ffmpegcs)
        self.pipeline.add(self.client_video)

        gst.element_link_many(self.alsasrc, self.capsfilter_audio, self.q1, self.audioconvert, self.client_audio)
        gst.element_link_many(self.v4l2src, self.capsfilter_video, self.q2, self.videoscale, self.ffmpegcs, self.client_video)
 
    def OnPlay(self, widget):
        print "Play"
        # self.vsink.set_xwindow_id(self.da.window.xid)
        self.pipeline.set_state(gst.STATE_PLAYING)
 
    def OnStop(self, widget):
        print "Stop"
        # We have to pause only src. If we pause whole pipeline, there will
        # be delay added to video
        self.pipeline.set_state(gst.STATE_PAUSED)
 
    def OnQuit(self, widget):
        gtk.main_quit()
 
    def decode_audio_pad(dbin, pad, islast):
        pad.link(convert.get_pad("asink"))

    def decode_video_pad(dbin, pad, islast):
        pad.link(convert.get_pad("vsink"))

    def on_pad_added(self, element, src_pad):
        print "pad added"
        # When rtpdemux creates dynamic pad, we can link it to filter
        # self.rtpdemux.link(self.filter)
 
start=Main()
gtk.main()

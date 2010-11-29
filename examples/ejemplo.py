#!/usr/bin/env python
import pygst
pygst.require("0.10")
import gst
import pygtk
import gtk
 
AUDIO_DEV = 'hw:0,0'
VIDEO_DEV = '/dev/video0'
LOCAL_HOST = '192.168.1.2' 
LOCAL_PORT = 9000
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
        # Create the pipeline
        self.pipelineClient = gst.Pipeline("client")
        self.pipelineServer = gst.Pipeline("server")
 
        # We use "udpsrc" on port 5000 for video source 
        self.audiosrc = gst.element_factory_make("alsasrc", "asrc")
	self.audiosrc.set_property('device',AUDIO_DEV)
        self.videosrc = gst.element_factory_make("v4l2src", "vsrc")
	self.videosrc.set_property('device',VIDEO_DEV)

        # We need some queues
        self.queue1 = gst.element_factory_make("queue","que1")
        self.queue2 = gst.element_factory_make("queue","que2")
        self.queue3 = gst.element_factory_make("queue","que3")
        self.queue4 = gst.element_factory_make("queue","que4")
 
        # We use "xvimagesink" to display video on x-window
        self.asink = gst.element_factory_make("alsasink", "asink")
        self.vsink = gst.element_factory_make("xvimagesink", "vsink")

        self.tcpvclientsink = gst.element_factory_make("tcpclientsink", "tcpclientsink0")
	self.tcpvclientsink.set_property('host', REMOTE_HOST)
	self.tcpvclientsink.set_property('port', REMOTE_PORT)
 
        self.tcpaclientsink = gst.element_factory_make("tcpclientsink", "tcpclientsink1")
	self.tcpaclientsink.set_property('host', REMOTE_HOST)
	self.tcpaclientsink.set_property('port', REMOTE_PORT+1)

        self.tcpvserversrc = gst.element_factory_make("tcpserversrc", "tcpserversrc0")
	self.tcpvserversrc.set_property('host', LOCAL_HOST)
	self.tcpvserversrc.set_property('port', LOCAL_PORT)
 
        self.tcpaserversrc = gst.element_factory_make("tcpserversrc", "tcpserversrc1")
	self.tcpaserversrc.set_property('host', LOCAL_HOST)
	self.tcpaserversrc.set_property('port', LOCAL_PORT+1)

	self.adecode = gst.element_factory_make("decodebin2", "decode0")
	self.adecode.connect("new-decoded-pad", self.decode_audio_pad)

	self.vdecode = gst.element_factory_make("decodebin", "decode1")
	self.vdecode.connect("new-decoded-pad", self.decode_video_pad)

	self.aconvert = gst.element_factory_make("audioconvert", "aconvert")
	self.vconvert = gst.element_factory_make("colorconvert", "vconvert")

	# self.mux = gst.element_factory_make("", "mux0")
	# self.demux = gst.element_factory_make("", "demux0")

    def setupPipeline(self):
        # Add elements to pipeline
        self.pipelineClient.add(self.videosrc)
        self.pipelineClient.add(self.queue1)
        self.pipelineClient.add(self.audiosrc)
        self.pipelineClient.add(self.queue2)
        self.pipelineClient.add(self.tcpvclientsink)
        self.pipelineClient.add(self.tcpaclientsink)
 
        self.pipelineServer.add(self.tcpvserversrc)
        self.pipelineServer.add(self.vconvert)
        self.pipelineServer.add(self.queue3)
        self.pipelineServer.add(self.vdecode)
        self.pipelineServer.add(self.vsink)
        self.pipelineServer.add(self.tcpaserversrc)
        self.pipelineServer.add(self.aconvert)
        self.pipelineServer.add(self.queue4)
        self.pipelineServer.add(self.adecode)
        self.pipelineServer.add(self.asink)
 
        gst.element_link_many(self.videosrc, self.queue1, self.tcpvclientsink) 
        gst.element_link_many(self.audiosrc, self.queue2, self.tcpaclientsink) 
 
	self.tcpaserversrc.link(self.adecode)
	self.aconvert.link(self.asink)
	self.tcpvserversrc.link(self.vdecode)
	self.vconvert.link(self.vsink)
        # gst.element_link_many(self.tcpvserversrc, self.queue3, self.vsink) 
        # gst.element_link_many(self.tcpaserversrc, self.decode, self.queue4, self.convert, self.asink) 
 
    def OnPlay(self, widget):
        print "Play"
        self.vsink.set_xwindow_id(self.da.window.xid)
        self.pipelineServer.set_state(gst.STATE_PLAYING)
        self.pipelineClient.set_state(gst.STATE_PLAYING)
 
    def OnStop(self, widget):
        print "Stop"
        # We have to pause only src. If we pause whole pipeline, there will
        # be delay added to video
        self.audiosrc.set_state(gst.STATE_PAUSED)
        self.videosrc.set_state(gst.STATE_PAUSED)
 
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

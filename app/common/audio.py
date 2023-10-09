import pyaudio
import wave
import wx
from assets import resource_path
from threading import * 

class ManageAudioRecord:
    def __init__(self, notify_window):
        self.audio = None
        self.EVT_RESULT_ID = wx.NewId()
        self._notify_window = notify_window

    def prepare(self):
        self.audio = AudioRecord(self)
        self.audio.icon = self._notify_window.\
            ctrls['btns']['circle']['e']

    def bind(self, func):
        """Define Result Event."""
        self._notify_window.\
            Connect(-1, -1, self.EVT_RESULT_ID, func)

    def onStop(self, _stream, _pyaudio):
        # stop and close stream
        _stream.stop_stream()
        _stream.close()
        # terminate pyaudio object
        _pyaudio.terminate()

        wx.PostEvent(self._notify_window, 
            ManageAudioResultEvent(
                self.EVT_RESULT_ID, 
                self.audio.stream))

    def record(self):
        self.audio.record()

    def stop(self):
        self.audio.stop()
    def save(self):
        self.audio.save()

class ManageAudioResultEvent(wx.PyEvent):
    """Simple event to carry arbitrary result data."""
    def __init__(self, _event_id, _stream):
        """Init Result Event."""
        wx.PyEvent.__init__(self)
        self.SetEventType(_event_id)
        self.stream = _stream;

class AudioRecord(Thread):
    def __init__(self, manager):
        Thread.__init__(self)
        # self.EVT_RESULT_ID = wx.NewId()
        self.manager = manager
        # the file name output you want to record into
        self.filename = "./recorded.wav"
        self.icon = None
        self.statusIcon = False

    def defaults(self):
        # set the chunk size of 1024 samples
        self.chunk = 1024
        # sample format
        self.FORMAT = pyaudio.paInt16
        # mono, change to 2 if you want stereo
        self.channels = 1
        # 44100 samples per second
        self.sample_rate = 44100
        self.record_seconds = 5    
        self.o = None
        self.stream = None
        self.frames = None
        self.flag = False
        self.counter = 0

    def record(self):
        self.defaults()
        self.flag = True
        self.start()
    def run(self):

        # initialize PyAudio object
        self.o = pyaudio.PyAudio()
        # open stream object as input & output
        self.stream = self.o.open(format=self.FORMAT,
                channels=self.channels,
                rate=self.sample_rate,
                input=True,
                output=True,
                frames_per_buffer=self.chunk)
        self.frames = []
        print("Recording...")
        # for i in range(int(44100 / self.chunk * self.record_seconds)):
        # iconoff = wx.Bitmap(resource_path("assets/recording.png"), 
        #     wx.BITMAP_TYPE_ANY)
        # iconon = wx.Bitmap(resource_path("assets/recording-1.png"), 
        #     wx.BITMAP_TYPE_ANY)

        while self.flag:
            self.playIcon()
            data = self.stream.read(self.chunk)
            # if you want to hear your voice while recording
            # stream.write(data)
            self.frames.append(data)

        self.manager.onStop(self.stream, self.o)
        # wx.PostEvent(self._notify_window, 
        #     AudioResultEvent(self.EVT_RESULT_ID, 
        #         self.stream, 
        #         self.o))
        print("Finished recording.")

    def playIcon(self):
        return
        if (self.counter % 20 == 0):
            if self.statusIcon:
                print("on")
                self.icon.SetBitmapSelected(iconoff)
                self.statusIcon = False
            else:
                print("off")
                self.icon.SetBitmapSelected(iconon)
                self.statusIcon = True
        self.counter += 1        

    def stop(self):
        # print("EY STOP")
        self.flag = False


    def save(self):
        # save audio file
        # open the file in 'write bytes' mode
        wf = wave.open(self.filename, "wb")
        # set the channels
        wf.setnchannels(self.channels)
        # set the sample format
        wf.setsampwidth(self.o.get_sample_size(self.FORMAT))
        # set the sample rate
        wf.setframerate(self.sample_rate)
        # write the frames as bytes
        wf.writeframes(b"".join(self.frames))
        # close the file
        wf.close()        
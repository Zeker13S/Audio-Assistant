from settings import WIT_TOKEN
from wit import Wit
import wx
from threading import * 

class ManageListenerEvent(wx.PyEvent):
    """Simple event to carry arbitrary result data."""
    def __init__(self, _event_id, response):
        """Init Result Event."""
        wx.PyEvent.__init__(self)
        self.SetEventType(_event_id)
        self.response = response

class ManageListener:
    def __init__(self, notify_window):
        self.client = None
        self.token = WIT_TOKEN
        self.EVT_RESULT_ID = wx.NewId()
        self._notify_window = notify_window

    def prepare(self):
        self.client = ClientWit(self, 
            self.token)
    def set_stream_audio(self, wav_audio):
        self.client.stream_audio = wav_audio

    def bind(self, func):
        """Define Result Event."""
        self._notify_window.\
            Connect(-1, -1, self.EVT_RESULT_ID, func)

    def onStop(self, response):
        wx.PostEvent(self._notify_window, 
            ManageListenerEvent(self.EVT_RESULT_ID, response))

    def analyze(self):
        self.client.analyze()

class ClientWit(Thread):
    def __init__(self, manager, _token):
        Thread.__init__(self)
        self.token = _token
        self.o = Wit(self.token)
        self.manager = manager
        self.stream_audio = None
        # the file name output you want to record into
        # self.filename = "./recorded.wav"

    def defaults(self):
        pass

    def analyze(self):
        self.start()

    def run(self):
        print("WIT is running...")
        with open('./recorded.wav', 'rb') as f:
            resp = self.o.speech(f, {
                'Content-Type': 'audio/wav'
            })
        print('Yay, got Wit.ai response: ' + str(resp))
        self.manager.onStop(resp)
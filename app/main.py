import wx
import pyaudio
import wave
import sys
import os
import logging
sys.\
    path.\
    append(os.path.join(os.path.dirname(__file__), 'common'))

from wit import Wit
from wx.lib.agw.shapedbutton import SButton, \
    SBitmapButton
from wx.lib.agw.shapedbutton import SBitmapToggleButton, \
    SBitmapTextToggleButton
from images import scale_bitmap
from audio import ManageAudioRecord
from listener import ManageListener
from assets import resource_path
from actions import traits

logging.basicConfig(filename='./tmp/app.log',
    level=logging.NOTSET,
    format='%(name)s - %(levelname)s - %(message)s')

class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        super().__init__(parent=None, title='Oreja')
        self.panel_1 = wx.Panel(self, wx.ID_ANY)
        self.panel_2 = wx.Panel(self.panel_1, wx.ID_ANY)

        self.sizer_1 = wx.BoxSizer(wx.VERTICAL)
        self.sizer_2 = wx.BoxSizer(wx.VERTICAL)

        self.ctrls = {
            'btns': {
                'circle': {
                    'e': self.getRoundedButton(self.panel_2),
                    'selected': False
                }
            },
            'texts': {
                'status': wx.StaticText(self.panel_2, wx.ID_ANY, "...")
            },
            'tmp': {
                'audio': None,
                'wit': None
            }
        }
        
        self.prepareToRecord()

        self.ctrls['btns']['circle']['e'].\
            Bind(wx.EVT_BUTTON, self.onRecord)

        self.sizer_2.Add(self.ctrls['btns']['circle']['e'], 
            0, wx.ALL | wx.CENTER, 5)
        self.sizer_2.Add(self.ctrls['texts']['status'], 
            0, wx.ALL | wx.CENTER, 5)

        self.panel_2.SetSizer(self.sizer_2)

        self.sizer_1.Add(self.panel_2, 1, wx.EXPAND, 0)

        self.panel_1.SetSizer(self.sizer_1)
        self.Layout()
        
        self.__set_properties()
        self.__do_layout()

    def __set_properties(self):
        pass
    def __do_layout(self):
        pass

    def getRoundedButton(self, _panel):
        bmpStop = wx.Bitmap(resource_path("assets/stop.png"), 
            wx.BITMAP_TYPE_ANY)

        bmpRecording = wx.Bitmap(resource_path("assets/recording.png"), 
            wx.BITMAP_TYPE_ANY)

        size = (75,75)
        
        bmpToggleBtn = SBitmapToggleButton(_panel, 
            wx.ID_ANY, bitmap=bmpStop, size = size)

        bmpToggleBtn.SetBitmapSelected(bmpRecording)
        bmpToggleBtn.Bind(wx.EVT_BUTTON, self.onRecord)
        return bmpToggleBtn

    def prepareToRecord(self):
        self.ctrls['tmp']['audio'] = ManageAudioRecord(self)
        self.ctrls['tmp']['audio'].bind(self.onAudioStop)
        self.ctrls['tmp']['wit'] = ManageListener(self)
        self.ctrls['tmp']['wit'].bind(self.onWitResponse)
    def onAudioStop(self, e):
        self.ctrls['texts']['status'].SetLabel("Analyzing...")
        self.ctrls['tmp']['audio'].save()
        self.ctrls['tmp']['wit'].prepare()
        self.ctrls['tmp']['wit'].analyze()
        

    def onWitResponse(self, e):
        action = traits(e.response)
        self.ctrls['texts']['status'].SetLabel(action)
        logging.info('Wit response: %s', e.response)
        logging.info('-'*10)
        if action == 'abrir navegador':
            abrir_navegador()
        elif action == 'cerrar navegador':
            cerrar_navegador()


    def onRecord(self, e):
        if ( self.ctrls['btns']['circle']['selected'] ):
            self.ctrls['tmp']['audio'].stop()
            self.ctrls['texts']['status'].SetLabel("Stopping...")
            self.ctrls['btns']['circle']['selected'] = False
        else:
            self.ctrls['tmp']['audio'].prepare()
            self.ctrls['tmp']['audio'].record()
            self.ctrls['texts']['status'].SetLabel("Grabando...")
            self.ctrls['btns']['circle']['selected'] = True

    def checkAudio(self):
        resp = None
        with open('test.wav', 'rb') as f:
          resp = client.speech(f, {'Content-Type': 'audio/wav'})
        print('Yay, got Wit.ai response: ' + str(resp))        

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, wx.ID_ANY, "")
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True

# end of class MyApp

if __name__ == "__main__":
    app = MyApp(0)
    app.MainLoop()

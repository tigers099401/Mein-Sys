# wx.lib.analogclockでアナログ時計を表示させるサンプルコード

import wx
import wx.lib.analogclock as ac

class MyFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(MyFrame, self).__init__(*args, **kw)

        self.IntUI()

    def IntUI(self):

        panel = wx.Panel(self)
        box = wx.BoxSizer(wx.VERTICAL)

        clock = ac.AnalogClockWindow(panel)

        box.Add(clock, proportion=1, flag=wx.ALL|wx.EXPAND)
        panel.SetSizer(box)

        self.SetSize((300, 300))
        self.SetTitle('Simple Analog Clock')

def main():
    app = wx.App()
    frame = MyFrame(None)
    frame.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()
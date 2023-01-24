import wx

class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, "My Frame")

        text_ctrl = wx.TextCtrl(self)
        current_size = text_ctrl.GetSize()
        text_ctrl.SetSizeHints(current_size, wx.Size(current_size.x * 2, current_size.y * 2))
    def on_size(self, event):
        textctrl = event.GetEventObject()
        size = textctrl.GetBestSize()
        textctrl.SetSize(size)

if __name__ == "__main__":
    app = wx.App()
    frame = MyFrame()
    frame.Show()
    app.MainLoop()
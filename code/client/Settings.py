import json
import webbrowser

import cv2
import requests
import wx
import wx.xrc

from tcp_by_size import recv_by_size
from tcp_by_size import send_with_size


class SettingsFrame(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"Mood Music", pos=wx.DefaultPosition,
                          size=wx.Size(560, 550), style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
        self.ModeColors = {'Black': {'Button': wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DDKSHADOW),
                                     'Background1': wx.Colour(20, 17, 21),
                                     'Background2': wx.Colour(53, 53, 53),
                                     'Text': wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNHIGHLIGHT),
                                     'TextCtrl': wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DDKSHADOW)},

                           'White': {'Button': wx.Colour(236, 239, 244),
                                     'Background1': wx.Colour(223, 223, 227, 255),
                                     'Background2': wx.Colour(255, 253, 255, 255),
                                     'Text': wx.SystemSettings.GetColour(wx.SYS_COLOUR_CAPTIONTEXT),
                                     'TextCtrl': wx.Colour(223, 223, 227, 255)}
                           }
        self.statusMode = 'Black'
        self.parent = parent
        self.client = parent.client
        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetIcon(wx.Icon("images/black logo2.ico"))
        font = wx.Font(16, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Poppins")
        bSizer_main = wx.BoxSizer(wx.VERTICAL)

        bSizer_panel1 = wx.BoxSizer(wx.VERTICAL)

        self.panel_background1 = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.panel_background1.SetBackgroundColour(wx.Colour(20, 17, 21))

        bSizer_panel2 = wx.BoxSizer(wx.VERTICAL)

        self.m_panel9 = wx.Panel(self.panel_background1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_panel9.SetFont(
            wx.Font(22, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Poppins"))
        self.m_panel9.SetBackgroundColour(wx.Colour(53, 53, 53))

        panel_background2 = wx.BoxSizer(wx.VERTICAL)

        gbSizer_allitems = wx.GridBagSizer(0, 0)
        gbSizer_allitems.SetFlexibleDirection(wx.BOTH)
        gbSizer_allitems.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        Sizer_settings = wx.BoxSizer(wx.VERTICAL)

        self.settings_text = wx.StaticText(self.m_panel9, wx.ID_ANY, u"Settings", wx.DefaultPosition, wx.DefaultSize, 0)
        self.settings_text.Wrap(-1)

        self.settings_text.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNHIGHLIGHT))

        Sizer_settings.Add(self.settings_text, 0, wx.ALIGN_CENTER | wx.TOP, 10)

        gbSizer_allitems.Add(Sizer_settings, wx.GBPosition(0, 1), wx.GBSpan(1, 1), wx.ALIGN_CENTER, 5)

        Sizer_userdev = wx.BoxSizer(wx.HORIZONTAL)

        Sizer_user = wx.BoxSizer(wx.VERTICAL)

        self.image_logo = wx.StaticBitmap(self.m_panel9, wx.ID_ANY,
                                          wx.Bitmap(u"images/black logo(main).png", wx.BITMAP_TYPE_ANY),
                                          wx.DefaultPosition, wx.DefaultSize, 0)
        Sizer_user.Add(self.image_logo, 0, wx.BOTTOM, 5)

        Sizer_userdev.Add(Sizer_user, 0, wx.ALIGN_CENTER, 0)

        gbSizer_allitems.Add(Sizer_userdev, wx.GBPosition(2, 1), wx.GBSpan(1, 1), wx.ALIGN_CENTER | wx.EXPAND, 5)

        bSizer70 = wx.BoxSizer(wx.VERTICAL)

        Sizer_info = wx.BoxSizer(wx.HORIZONTAL)

        self.name_text = wx.StaticText(self.m_panel9, wx.ID_ANY, u"", wx.DefaultPosition, wx.DefaultSize, 0)
        self.name_text.Wrap(-1)

        self.name_text.SetFont(font)
        self.name_text.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNHIGHLIGHT))

        Sizer_info.Add(self.name_text, 1, wx.ALIGN_CENTER | wx.ALL | wx.SHAPED, 5)

        bSizer70.Add(Sizer_info, 0, wx.ALIGN_CENTER, 5)

        Sizer_info1 = wx.BoxSizer(wx.HORIZONTAL)

        self.spotname_text = wx.StaticText(self.m_panel9, wx.ID_ANY, u"No Spotify linked", wx.DefaultPosition,
                                           wx.DefaultSize, 0)
        self.spotname_text.Wrap(-1)

        self.spotname_text.SetFont(font)
        self.spotname_text.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNHIGHLIGHT))

        Sizer_info1.Add(self.spotname_text, 1, wx.ALIGN_CENTER | wx.ALL, 5)

        bSizer70.Add(Sizer_info1, 1, 0, 5)

        gbSizer_allitems.Add(bSizer70, wx.GBPosition(3, 1), wx.GBSpan(1, 1), wx.EXPAND, 5)

        Sizer_changespot = wx.BoxSizer(wx.HORIZONTAL)

        self.button_changespot = wx.Button(self.m_panel9, wx.ID_ANY, u"change spotify acoount", wx.DefaultPosition,
                                           wx.DefaultSize, 0)
        self.button_changespot.SetFont(font)
        self.button_changespot.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DDKSHADOW))

        Sizer_changespot.Add(self.button_changespot, 0, wx.ALL, 5)

        gbSizer_allitems.Add(Sizer_changespot, wx.GBPosition(4, 1), wx.GBSpan(1, 3), 0, 5)

        Sizer_mode = wx.BoxSizer(wx.HORIZONTAL)

        self.Button_mode = wx.Button(self.m_panel9, wx.ID_ANY, u"NightMode night", wx.DefaultPosition, wx.DefaultSize,
                                     0)
        self.Button_mode.SetLabelMarkup(u"White Mode")
        self.Button_mode.SetFont(font)
        self.Button_mode.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DDKSHADOW))

        Sizer_mode.Add(self.Button_mode, 0, wx.ALL, 5)

        gbSizer_allitems.Add(Sizer_mode, wx.GBPosition(5, 1), wx.GBSpan(1, 1), wx.ALIGN_CENTER | wx.EXPAND, 5)

        Sizer_back = wx.BoxSizer(wx.VERTICAL)

        self.Button_back = wx.BitmapButton(self.m_panel9, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize,
                                           wx.BU_AUTODRAW | 0 | wx.BORDER_NONE)

        self.Button_back.SetBitmap(wx.Bitmap(u"images/back icon big.png", wx.BITMAP_TYPE_ANY))
        self.Button_back.SetBackgroundColour(wx.Colour(53, 53, 53))

        Sizer_back.Add(self.Button_back, 0, wx.ALL, 5)

        gbSizer_allitems.Add(Sizer_back, wx.GBPosition(4, 0), wx.GBSpan(3, 1), wx.EXPAND, 5)

        panel_background2.Add(gbSizer_allitems, 1, wx.ALIGN_CENTER, 5)

        self.m_panel9.SetSizer(panel_background2)
        self.m_panel9.Layout()
        panel_background2.Fit(self.m_panel9)
        bSizer_panel2.Add(self.m_panel9, 1, wx.ALL | wx.EXPAND, 60)

        self.panel_background1.SetSizer(bSizer_panel2)
        self.panel_background1.Layout()
        bSizer_panel2.Fit(self.panel_background1)
        bSizer_panel1.Add(self.panel_background1, 1, wx.EXPAND | wx.ALL, 0)

        bSizer_main.Add(bSizer_panel1, 1, wx.EXPAND, 5)

        self.SetSizer(bSizer_main)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.button_changespot.Bind(wx.EVT_BUTTON, self.ChangeSpotAcc)
        self.Button_mode.Bind(wx.EVT_BUTTON, self.ChangeMode)
        self.Button_back.Bind(wx.EVT_BUTTON, self.GoBack)

    def ChangeMode(self, event):
        if self.statusMode == 'Black':
            self.statusMode = 'White'
        else:
            self.statusMode = 'Black'
        for frame in wx.GetTopLevelWindows():
            print(type(frame))
            if type(frame).__name__ == "SettingsFrame":
                frame.panel_background1.SetBackgroundColour(self.ModeColors[self.statusMode]['Background1'])
                frame.m_panel9.SetBackgroundColour(self.ModeColors[self.statusMode]['Background2'])
                self.panel_background1.SetBackgroundColour(self.ModeColors[self.statusMode]['Background1'])
                self.m_panel9.SetBackgroundColour(self.ModeColors[self.statusMode]['Background2'])
                for button in (frame.button_changespot, frame.Button_mode):
                    button.SetBackgroundColour(self.ModeColors[self.statusMode]['Button'])
                for text in (frame.settings_text, frame.name_text, frame.spotname_text):
                    text.SetForegroundColour(self.ModeColors[self.statusMode]['Text'])
                frame.Button_back.SetBackgroundColour(self.ModeColors[self.statusMode]['Background2'])
                if self.statusMode == 'White':
                    frame.Button_mode.SetLabel('Black Mode')
                else:
                    frame.Button_mode.SetLabel('White Mode')
                self.Refresh()
            if type(frame).__name__ == "LoginFrame":

                frame.panel_background1.SetBackgroundColour(self.ModeColors[self.statusMode]['Background1'])
                frame.panel_background2.SetBackgroundColour(self.ModeColors[self.statusMode]['Background2'])
                for button in (frame.Button_signup, frame.Button_login, frame.Button_password):
                    button.SetBackgroundColour(self.ModeColors[self.statusMode]['Button'])
                for text in (
                        frame.staticText_noAcc, frame.staticText_dev, frame.staticText_user, frame.staticText_accType):
                    text.SetForegroundColour(self.ModeColors[self.statusMode]['Text'])
                for textctrl in (frame.textCtrl_Email, frame.textCtrl_password):
                    textctrl.SetBackgroundColour(self.ModeColors[self.statusMode]['TextCtrl'])
                frame.Button_settings.SetBackgroundColour(self.ModeColors[self.statusMode]['Background2'])
            if type(frame).__name__ == "RegisterFrame":
                frame.panel_background1.SetBackgroundColour(self.ModeColors[self.statusMode]['Background1'])
                frame.m_panel9.SetBackgroundColour(self.ModeColors[self.statusMode]['Background2'])
                for button in (frame.Button_user, frame.Button_login):
                    button.SetBackgroundColour(self.ModeColors[self.statusMode]['Button'])
                for text in (
                        frame.staticText_accType, frame.staticText_user, frame.staticText_dev,
                        frame.staticText_accType):
                    text.SetForegroundColour(self.ModeColors[self.statusMode]['Text'])
                for textctrl in (frame.textCtrl_name, frame.textCtrl_Email, frame.textCtrl_password):
                    textctrl.SetBackgroundColour(self.ModeColors[self.statusMode]['TextCtrl'])
                frame.Button_settings.SetBackgroundColour(self.ModeColors[self.statusMode]['Background2'])
                frame.Button_back.SetBackgroundColour(self.ModeColors[self.statusMode]['Background2'])
            if type(frame).__name__ == "ForgotFrame":
                frame.panel_background1.SetBackgroundColour(self.ModeColors[self.statusMode]['Background1'])
                frame.m_panel9.SetBackgroundColour(self.ModeColors[self.statusMode]['Background2'])
                frame.Button_login.SetBackgroundColour(self.ModeColors[self.statusMode]['Button'])
                for text in (frame.header_text, frame.status_text):
                    text.SetForegroundColour(self.ModeColors[self.statusMode]['Text'])
                for textctrl in (frame.textCtrl_first, frame.textCtrl_second):
                    textctrl.SetBackgroundColour(self.ModeColors[self.statusMode]['TextCtrl'])
                frame.Button_settings.SetBackgroundColour(self.ModeColors[self.statusMode]['Background2'])
                frame.Button_back.SetBackgroundColour(self.ModeColors[self.statusMode]['Background2'])
            if type(frame).__name__ == "MainFrame":
                frame.panel_background1.SetBackgroundColour(self.ModeColors[self.statusMode]['Background1'])
                frame.m_panel9.SetBackgroundColour(self.ModeColors[self.statusMode]['Background2'])
                for button in (frame.Button_on, frame.Button_off, frame.button_Create, frame.button_Created):
                    button.SetBackgroundColour(self.ModeColors[self.statusMode]['Button'])
                for text in (frame.error_box_text, frame.text_camera, frame.username_text):
                    text.SetBackgroundColour(self.ModeColors[self.statusMode]['Background2'])
                    text.SetForegroundColour(self.ModeColors[self.statusMode]['Text'])
                frame.Button_settings.SetBackgroundColour(self.ModeColors[self.statusMode]['Background2'])
                frame.Button_back.SetBackgroundColour(self.ModeColors[self.statusMode]['Background2'])
                if self.statusMode == 'White':
                    frame.image = cv2.imread('images/nocamwhite.jpg')
                    frame.image = cv2.cvtColor(frame.image, cv2.COLOR_BGR2RGB)
                    frame.bmp = wx.Bitmap.FromBuffer(400, 320, frame.image)
                    frame.userCam.SetBitmap(frame.bmp)

                else:
                    frame.image = cv2.imread('images/nocamblack.jpg')
                    frame.image = cv2.cvtColor(frame.image, cv2.COLOR_BGR2RGB)
                    frame.bmp = wx.Bitmap.FromBuffer(400, 320, frame.image)
                    frame.userCam.SetBitmap(wx.Bitmap.FromBuffer(400, 320, frame.image))
                frame.Refresh()

    def GoBack(self, event):
        self.Hide()  # hide the register frame
        self.parent.Show()  # show the login frame
        if self.parent == 'MainFrame object':
            dict = {
                'Func': 'CheckUrl',
                'Email': self.parent.Email
            }
            data_send = json.dumps(dict)
            send_with_size(self.client, data_send)
            msg = recv_by_size(self.client)
            if msg == '1':
                self.parent.button_Created.Enable()
                self.parent.button_Create.Enable()
            else:
                self.parent.button_Created.Disable()
                self.parent.button_Create.Disable()

    def ChangeSpotAcc(self, event):
        dict = {
            'Func': 'SpotAuth',
            'Name': self.parent.name,
            'Email': self.parent.Email
        }
        data_send = json.dumps(dict)
        send_with_size(self.client, data_send)
        msg = recv_by_size(self.client)
        webbrowser.open("http://127.0.0.1:5000")

        data = {'Email': self.parent.Email}
        response = requests.post('http://127.0.0.1:5000/getEmail', data=data)
        print(msg)

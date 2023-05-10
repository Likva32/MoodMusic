import hashlib
import json

import wx
import wx.xrc
from loguru import logger
from validators import email

from Settings import SettingsFrame


class ForgotFrame(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"Mood Music", pos=wx.DefaultPosition,
                          size=wx.Size(500, 500), style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
        self.parent = parent
        self.client = parent.client
        self.Email = ''
        self.Code = ''
        self.SettingsFrame = SettingsFrame(self)
        self.SetIcon(wx.Icon("images/black logo2.ico"))
        font = wx.Font(15, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Garamond")

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        bSizer58 = wx.BoxSizer(wx.VERTICAL)

        bSizer_panel1 = wx.BoxSizer(wx.VERTICAL)

        self.panel_background1 = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.panel_background1.SetBackgroundColour(wx.Colour(20, 17, 21))

        bSizer_panel2 = wx.BoxSizer(wx.VERTICAL)

        self.m_panel9 = wx.Panel(self.panel_background1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_panel9.SetFont(font)
        self.m_panel9.SetBackgroundColour(wx.Colour(53, 53, 53))

        panel_background2 = wx.BoxSizer(wx.VERTICAL)

        gbSizer_allitems = wx.GridBagSizer(0, 0)
        gbSizer_allitems.SetFlexibleDirection(wx.BOTH)
        gbSizer_allitems.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        header_sizer = wx.BoxSizer(wx.VERTICAL)

        self.header_text = wx.StaticText(self.m_panel9, wx.ID_ANY, u"Forgot your password?", wx.DefaultPosition,
                                         wx.DefaultSize, 0)
        self.header_text.Wrap(-1)

        self.header_text.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNHIGHLIGHT))
        self.header_text.SetFont(
            wx.Font(20, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Garamond"))

        header_sizer.Add(self.header_text, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        gbSizer_allitems.Add(header_sizer, wx.GBPosition(0, 0), wx.GBSpan(1, 2), wx.ALIGN_CENTER | wx.LEFT, 50)

        image_sizer = wx.BoxSizer(wx.VERTICAL)

        self.image = wx.StaticBitmap(self.m_panel9, wx.ID_ANY,
                                     wx.Bitmap(u"images/Forgot Password.png", wx.BITMAP_TYPE_ANY), wx.DefaultPosition,
                                     wx.DefaultSize, 0)
        image_sizer.Add(self.image, 0, wx.ALL, 5)

        gbSizer_allitems.Add(image_sizer, wx.GBPosition(1, 1), wx.GBSpan(1, 1), wx.ALIGN_CENTER, 5)

        first_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.textCtrl_first = wx.TextCtrl(self.m_panel9, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                          wx.TE_CENTER | wx.BORDER_STATIC)
        self.textCtrl_first.SetFont(font)
        self.textCtrl_first.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOWTEXT))
        self.textCtrl_first.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DDKSHADOW))

        first_sizer.Add(self.textCtrl_first, 1, wx.EXPAND | wx.BOTTOM | wx.TOP, 5)

        gbSizer_allitems.Add(first_sizer, wx.GBPosition(3, 1), wx.GBSpan(1, 1), wx.EXPAND, 5)

        second_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.textCtrl_second = wx.TextCtrl(self.m_panel9, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                           wx.TE_CENTER | wx.BORDER_STATIC)
        self.textCtrl_second.SetFont(font)
        self.textCtrl_second.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOWTEXT))
        self.textCtrl_second.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DDKSHADOW))

        second_sizer.Add(self.textCtrl_second, 1, wx.EXPAND | wx.ALL, 5)

        gbSizer_allitems.Add(second_sizer, wx.GBPosition(4, 1), wx.GBSpan(1, 1), wx.EXPAND, 5)

        status_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.status_text = wx.StaticText(self.m_panel9, wx.ID_ANY, "", wx.DefaultPosition,
                                         wx.DefaultSize, 0)
        self.status_text.Wrap(-1)
        self.status_text.SetFont(
            wx.Font(18, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Garamond"))
        status_sizer.Add(self.status_text, 1, wx.ALIGN_CENTER | wx.RIGHT, 70)
        gbSizer_allitems.Add(status_sizer, wx.GBPosition(6, 1), wx.GBSpan(1, 1), wx.ALIGN_CENTER, 5)

        Sizer_login = wx.BoxSizer(wx.HORIZONTAL)

        self.Button_login = wx.Button(self.m_panel9, wx.ID_ANY, u"Send", wx.DefaultPosition, wx.DefaultSize, 0)
        self.Button_login.SetLabelMarkup(u"Send")
        self.Button_login.SetFont(font)
        self.Button_login.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DDKSHADOW))

        Sizer_login.Add(self.Button_login, 0, wx.ALL, 5)

        gbSizer_allitems.Add(Sizer_login, wx.GBPosition(7, 1), wx.GBSpan(1, 1), wx.ALIGN_CENTER | wx.EXPAND, 5)

        Sizer_back = wx.BoxSizer(wx.VERTICAL)

        self.Button_back = wx.BitmapButton(self.m_panel9, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize,
                                           wx.BU_AUTODRAW | 0 | wx.BORDER_NONE)

        self.Button_back.SetBitmap(wx.Bitmap(u"images/back icon big.png", wx.BITMAP_TYPE_ANY))
        self.Button_back.SetBackgroundColour(wx.Colour(53, 53, 53))

        Sizer_back.Add(self.Button_back, 0, wx.ALL, 5)

        gbSizer_allitems.Add(Sizer_back, wx.GBPosition(3, 0), wx.GBSpan(6, 1), wx.EXPAND, 5)

        settings_sizer = wx.BoxSizer(wx.VERTICAL)

        self.Button_settings = wx.BitmapButton(self.m_panel9, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition,
                                               wx.DefaultSize, wx.BU_AUTODRAW | 0 | wx.BORDER_NONE)

        self.Button_settings.SetBitmap(wx.Bitmap(u"images/setting icon resized.png", wx.BITMAP_TYPE_ANY))
        self.Button_settings.SetBackgroundColour(wx.Colour(53, 53, 53))

        settings_sizer.Add(self.Button_settings, 0, wx.ALL, 5)

        gbSizer_allitems.Add(settings_sizer, wx.GBPosition(0, 2), wx.GBSpan(1, 1), wx.ALIGN_CENTER | wx.EXPAND, 5)

        panel_background2.Add(gbSizer_allitems, 0, wx.ALIGN_CENTER, 5)

        self.m_panel9.SetSizer(panel_background2)
        self.m_panel9.Layout()
        panel_background2.Fit(self.m_panel9)
        bSizer_panel2.Add(self.m_panel9, 1, wx.ALL | wx.EXPAND, 60)

        self.panel_background1.SetSizer(bSizer_panel2)
        self.panel_background1.Layout()
        bSizer_panel2.Fit(self.panel_background1)
        bSizer_panel1.Add(self.panel_background1, 1, wx.EXPAND | wx.ALL, 0)

        bSizer58.Add(bSizer_panel1, 1, wx.EXPAND, 5)

        self.SetSizer(bSizer58)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.Button_login.Bind(wx.EVT_BUTTON, self.SendEmail)
        self.Button_back.Bind(wx.EVT_BUTTON, self.GoBack)
        self.Button_settings.Bind(wx.EVT_BUTTON, self.GoToSettings)
        self.Bind(wx.EVT_CLOSE, self.on_close)

        self.EmailScreen()

    def on_close(self, event):
        try:
            self.parent.on_close(event)
        except AttributeError:
            pass
        self.Destroy()

    def EmailScreen(self):
        self.Button_login.Bind(wx.EVT_BUTTON, self.SendEmail)
        self.textCtrl_second.Hide()
        self.textCtrl_first.SetHint('Email')

    def SendEmail(self, event):
        self.status_text.SetLabelText('')
        # bla bla send
        self.Email = self.textCtrl_first.GetValue()
        dict = {
            'Func': 'Sendmail',
            'Email': self.Email,
        }
        data_send = json.dumps(dict)
        if email(self.Email):
            self.parent.send_with_size(self.parent.client, data_send)
            data_from_server = self.parent.recv_by_size(self.parent.client)
            if data_from_server == 'Code Sended':
                self.CodeScreen()
            else:
                self.status_text.SetLabelText(data_from_server)
                self.status_text.SetForegroundColour(colour='red')
                logger.error("error")
        else:
            self.status_text.SetForegroundColour(colour='red')
            self.status_text.SetLabelText('invalid Email')

    def CodeScreen(self):
        self.status_text.SetLabelText('')
        self.textCtrl_first.SetValue('')
        self.textCtrl_first.SetHint('Code')
        self.Button_login.Bind(wx.EVT_BUTTON, self.SendCode)

    def SendCode(self, event):
        self.Code = self.textCtrl_first.GetValue()
        dict = {
            'Func': 'Sendcode',
            'Email': self.Email,
            'Code': self.Code,
        }
        data_send = json.dumps(dict)
        self.parent.send_with_size(self.parent.client, data_send)
        data_from_server = self.parent.recv_by_size(self.parent.client)
        if data_from_server == 'Code verified':
            self.PasswordScreen()
        else:
            self.status_text.SetLabelText(data_from_server)
            self.status_text.SetForegroundColour(colour='red')
            logger.error("error")

    def PasswordScreen(self):
        self.textCtrl_first.SetWindowStyle(style=wx.TE_PASSWORD)
        self.textCtrl_second.SetWindowStyle(style=wx.TE_PASSWORD)
        self.status_text.SetLabelText('')
        self.textCtrl_first.SetValue('')
        self.textCtrl_second.SetValue('')
        self.textCtrl_second.Show()
        self.textCtrl_first.Show()

        self.textCtrl_first.SetHint('Password')
        self.textCtrl_second.SetHint('Confirm Password')
        self.Button_login.Bind(wx.EVT_BUTTON, self.SendPassword)

    def SendPassword(self, event):
        # send pass

        Password1 = self.textCtrl_first.GetValue()
        Password2 = self.textCtrl_second.GetValue()
        salt = 'MoodMusic'
        hashed_pass = hashlib.md5(salt.encode('utf-8') + Password1.encode('utf-8')).hexdigest()
        dict = {
            'Func': 'Sendpass',
            'Email': self.Email,
            'Password': hashed_pass,
        }
        data_send = json.dumps(dict)
        if Password1 == Password2:
            self.parent.send_with_size(self.parent.client, data_send)
            data_from_server = self.parent.recv_by_size(self.parent.client)
            if data_from_server == 'Password Changed':
                self.status_text.SetLabelText(data_from_server)
                self.status_text.SetForegroundColour(colour='green')
            else:
                self.status_text.SetLabelText(data_from_server)
                self.status_text.SetForegroundColour(colour='red')
        else:
            self.status_text.SetLabelText("pass1 not equal to pass2")
            self.status_text.SetForegroundColour(colour='red')
            logger.warning("pass1 not equal to pass2")

    def GoBack(self, event):

        self.Hide()  # hide the register frame
        self.EmailScreen()
        self.parent.Show()  # show the login frame

    def GoToSettings(self, event):
        self.Hide()
        self.SettingsFrame.button_changespot.Hide()
        self.SettingsFrame.Centre()
        self.SettingsFrame.Show()

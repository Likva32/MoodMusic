import wx
import wx.xrc
from tcp_by_size import recv_by_size
from tcp_by_size import send_with_size


class RegisterFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"Mood Music", pos=wx.DefaultPosition,
                          size=wx.Size(620, 635), style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER | wx.TAB_TRAVERSAL)
        self.parent = parent
        self.SetIcon(wx.Icon("images/black logo2.ico"))
        font = wx.Font(15, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Garamond")

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        bSizer_main = wx.BoxSizer(wx.VERTICAL)

        bSizer_panel1 = wx.BoxSizer(wx.VERTICAL)

        self.panel_background1 = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.panel_background1.SetBackgroundColour(wx.Colour(20, 17, 21))

        bSizer_panel2 = wx.BoxSizer(wx.VERTICAL)

        self.m_panel9 = wx.Panel(self.panel_background1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_panel9.SetFont(
            wx.Font(20, wx.FONTFAMILY_SCRIPT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Viner Hand ITC"))
        self.m_panel9.SetBackgroundColour(wx.Colour(53, 53, 53))

        panel_background2 = wx.BoxSizer(wx.VERTICAL)

        gbSizer_allitems = wx.GridBagSizer(0, 0)
        gbSizer_allitems.SetFlexibleDirection(wx.BOTH)
        gbSizer_allitems.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        bSizer_accType1 = wx.BoxSizer(wx.VERTICAL)

        self.staticText_accType1 = wx.StaticText(self.m_panel9, wx.ID_ANY, u"Register Menu", wx.DefaultPosition,
                                                 wx.DefaultSize, 0)
        self.staticText_accType1.Wrap(-1)

        self.staticText_accType1.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNHIGHLIGHT))

        bSizer_accType1.Add(self.staticText_accType1, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        gbSizer_allitems.Add(bSizer_accType1, wx.GBPosition(0, 1), wx.GBSpan(1, 1), wx.EXPAND, 5)

        bSizer_accType = wx.BoxSizer(wx.VERTICAL)

        self.staticText_accType = wx.StaticText(self.m_panel9, wx.ID_ANY, u"Choose Account Type", wx.DefaultPosition,
                                                wx.DefaultSize, 0)
        self.staticText_accType.Wrap(-1)

        self.staticText_accType.SetFont(
            wx.Font(18, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString))
        self.staticText_accType.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNHIGHLIGHT))

        bSizer_accType.Add(self.staticText_accType, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        gbSizer_allitems.Add(bSizer_accType, wx.GBPosition(1, 1), wx.GBSpan(1, 1), wx.ALIGN_CENTER, 5)

        Sizer_userdev = wx.BoxSizer(wx.HORIZONTAL)

        Sizer_user = wx.BoxSizer(wx.VERTICAL)

        self.staticText_user = wx.StaticText(self.m_panel9, wx.ID_ANY, u"User", wx.DefaultPosition, wx.DefaultSize, 0)
        self.staticText_user.Wrap(-1)

        self.staticText_user.SetFont(
            wx.Font(18, wx.FONTFAMILY_SCRIPT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Viner Hand ITC"))
        self.staticText_user.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNHIGHLIGHT))

        Sizer_user.Add(self.staticText_user, 0, wx.ALIGN_CENTER, 5)

        self.Button_user = wx.BitmapButton(self.m_panel9, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize,
                                           wx.BU_AUTODRAW | wx.BU_TOP)

        self.Button_user.SetBitmap(wx.Bitmap(u"images/user resized.jpg", wx.BITMAP_TYPE_ANY))
        Sizer_user.Add(self.Button_user, 0, wx.ALL, 5)

        Sizer_userdev.Add(Sizer_user, 0, wx.ALIGN_CENTER, 5)

        Sizer_dev = wx.BoxSizer(wx.VERTICAL)

        self.staticText_dev = wx.StaticText(self.m_panel9, wx.ID_ANY, u"Developer", wx.DefaultPosition, wx.DefaultSize,
                                            0)
        self.staticText_dev.Wrap(-1)

        self.staticText_dev.SetFont(
            wx.Font(18, wx.FONTFAMILY_SCRIPT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Viner Hand ITC"))
        self.staticText_dev.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNHIGHLIGHT))

        Sizer_dev.Add(self.staticText_dev, 0, wx.ALIGN_CENTER, 0)

        self.Button_dev = wx.BitmapButton(self.m_panel9, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize,
                                          wx.BU_AUTODRAW | 0)

        self.Button_dev.SetBitmap(wx.Bitmap(u"images/dev resized.jpg", wx.BITMAP_TYPE_ANY))
        Sizer_dev.Add(self.Button_dev, 0, wx.ALL, 5)

        Sizer_userdev.Add(Sizer_dev, 0, wx.ALIGN_CENTER, 5)

        gbSizer_allitems.Add(Sizer_userdev, wx.GBPosition(2, 1), wx.GBSpan(1, 1), wx.ALIGN_CENTER | wx.EXPAND, 5)

        Sizer_username = wx.BoxSizer(wx.HORIZONTAL)

        self.textCtrl_name = wx.TextCtrl(self.m_panel9, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                         wx.DefaultSize, wx.TE_CENTER | wx.BORDER_STATIC)
        self.textCtrl_name.SetFont(font)
        self.textCtrl_name.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOWTEXT))
        self.textCtrl_name.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DDKSHADOW))
        self.textCtrl_name.SetHint('Name')

        Sizer_username.Add(self.textCtrl_name, 1, wx.ALIGN_CENTER | wx.ALL, 5)

        gbSizer_allitems.Add(Sizer_username, wx.GBPosition(3, 1), wx.GBSpan(1, 1), wx.ALIGN_CENTER | wx.EXPAND, 5)

        Sizer_password = wx.BoxSizer(wx.HORIZONTAL)

        self.textCtrl_password = wx.TextCtrl(self.m_panel9, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                             wx.DefaultSize, wx.TE_CENTER | wx.TE_PASSWORD | wx.BORDER_STATIC)
        self.textCtrl_password.SetFont(font)
        self.textCtrl_password.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOWTEXT))
        self.textCtrl_password.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DDKSHADOW))
        self.textCtrl_password.SetHint('Password')

        Sizer_password.Add(self.textCtrl_password, 0, wx.BOTTOM | wx.TOP, 5)

        gbSizer_allitems.Add(Sizer_password, wx.GBPosition(5, 1), wx.GBSpan(1, 1), wx.ALIGN_CENTER | wx.EXPAND, 5)

        Sizer_username1 = wx.BoxSizer(wx.HORIZONTAL)

        self.textCtrl_username = wx.TextCtrl(self.m_panel9, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                             wx.DefaultSize, wx.TE_CENTER | wx.BORDER_STATIC)
        self.textCtrl_username.SetFont(font)
        self.textCtrl_username.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOWTEXT))
        self.textCtrl_username.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DDKSHADOW))
        self.textCtrl_username.SetHint('Username')

        Sizer_username1.Add(self.textCtrl_username, 1, wx.ALIGN_CENTER | wx.ALL, 5)

        gbSizer_allitems.Add(Sizer_username1, wx.GBPosition(4, 1), wx.GBSpan(1, 1), wx.ALIGN_CENTER | wx.EXPAND, 5)

        status_box = wx.BoxSizer(wx.HORIZONTAL)

        self.status_text = wx.StaticText(self.m_panel9, wx.ID_ANY, '', wx.DefaultPosition, wx.DefaultSize, 0)
        self.status_text.Wrap(-1)
        self.status_text.SetFont(font)


        status_box.Add(self.status_text, 0,  wx.ALIGN_CENTER, 0)

        gbSizer_allitems.Add(status_box, wx.GBPosition(6, 1), wx.GBSpan(1, 1), wx.ALIGN_CENTER_HORIZONTAL | wx.RIGHT, 75)

        Sizer_login = wx.BoxSizer(wx.HORIZONTAL)

        self.Button_login = wx.Button(self.m_panel9, wx.ID_ANY, u"Register", wx.DefaultPosition, wx.DefaultSize, 0)
        self.Button_login.SetLabelMarkup(u"Register")
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

        gbSizer_allitems.Add(Sizer_back, wx.GBPosition(5, 0), wx.GBSpan(3, 1), wx.EXPAND, 5)

        bSizer185 = wx.BoxSizer(wx.VERTICAL)

        self.m_bpButton33 = wx.BitmapButton(self.m_panel9, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize,
                                            wx.BU_AUTODRAW | 0 | wx.BORDER_NONE)

        self.m_bpButton33.SetBitmap(wx.Bitmap(u"images/setting icon resized.png", wx.BITMAP_TYPE_ANY))
        self.m_bpButton33.SetBackgroundColour(wx.Colour(53, 53, 53))

        bSizer185.Add(self.m_bpButton33, 0, wx.ALL, 5)

        gbSizer_allitems.Add(bSizer185, wx.GBPosition(0, 3), wx.GBSpan(1, 1), wx.ALIGN_CENTER | wx.EXPAND, 5)

        panel_background2.Add(gbSizer_allitems, 0, wx.EXPAND, 5)

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
        self.Button_user.Bind(wx.EVT_BUTTON, self.typeUser)
        self.Button_dev.Bind(wx.EVT_BUTTON, self.typeDev)
        self.Button_login.Bind(wx.EVT_BUTTON, self.Register)
        self.Button_back.Bind(wx.EVT_BUTTON, self.GoBack)
        self.m_bpButton33.Bind(wx.EVT_BUTTON, self.GoToSettings)

    def __del__(self):
        pass

    # Virtual event handlers, override them in your derived class
    def typeUser(self, event):
        send_with_size(self.parent.client, 'CatUser')
        event.Skip()

    def typeDev(self, event):
        send_with_size(self.parent.client, 'CatDev')
        event.Skip()

    def Register(self, event):
        name = self.textCtrl_name.GetValue()
        username = self.textCtrl_username.GetValue()
        password = self.textCtrl_password.GetValue()
        data_send = f'register@{name}@{username}@{password}'
        if username and password != '':
            send_with_size(self.parent.client, data_send)
            msg = recv_by_size(self.parent.client)
            if msg == 'user inserted success':
                self.status_text.SetForegroundColour(colour='green')
            self.status_text.SetLabelText(msg)
            print(msg)
        elif username == '' and password == '':
            self.status_text.SetLabelText('write username and password')
            self.status_text.SetForegroundColour(colour='red')
        elif username == '':
            self.status_text.SetLabelText('write username')
            self.status_text.SetForegroundColour(colour='red')
        elif password == '':
            self.status_text.SetLabelText('write password')
            self.status_text.SetForegroundColour(colour='red')

    def GoBack(self, event):
        self.Hide()  # hide the register frame
        self.parent.Show()  # show the login frame

    def GoToSettings(self, event):
        event.Skip()

# app = wx.App()
# frame = RegisterFrame(None)
# frame.Show()
#
# frame.Centre()
# app.MainLoop()

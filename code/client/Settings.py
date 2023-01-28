import wx
import wx.xrc


class SettingsFrame(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"Mood Music", pos=wx.DefaultPosition,
                          size=wx.Size(560, 550), style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
        self.parent = parent
        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetIcon(wx.Icon("images/black logo2.ico"))
        font = wx.Font(16, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Poppins")
        bSizer_main = wx.BoxSizer(wx.VERTICAL)

        bSizer_panel1 = wx.BoxSizer(wx.VERTICAL)

        self.panel_background1 = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.panel_background1.SetBackgroundColour(wx.Colour(20, 17, 21))

        bSizer_panel2 = wx.BoxSizer(wx.VERTICAL)

        self.m_panel9 = wx.Panel(self.panel_background1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_panel9.SetFont(wx.Font(22, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Poppins"))
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

        self.name_text = wx.StaticText(self.m_panel9, wx.ID_ANY, u"Artur", wx.DefaultPosition, wx.DefaultSize, 0)
        self.name_text.Wrap(-1)

        self.name_text.SetFont(font)
        self.name_text.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNHIGHLIGHT))

        Sizer_info.Add(self.name_text, 1, wx.ALIGN_CENTER | wx.ALL | wx.SHAPED, 5)

        bSizer70.Add(Sizer_info, 0, wx.ALIGN_CENTER, 5)

        Sizer_info1 = wx.BoxSizer(wx.HORIZONTAL)

        self.spotname_text = wx.StaticText(self.m_panel9, wx.ID_ANY, u"Likva32(spotify)", wx.DefaultPosition,
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

        self.Button_mde = wx.Button(self.m_panel9, wx.ID_ANY, u"NightMode night", wx.DefaultPosition, wx.DefaultSize, 0)
        self.Button_mde.SetLabelMarkup(u"NightMode night")
        self.Button_mde.SetFont(font)
        self.Button_mde.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DDKSHADOW))

        Sizer_mode.Add(self.Button_mde, 0, wx.ALL, 5)

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
        self.Button_mde.Bind(wx.EVT_BUTTON, self.ChangeMode)
        self.Button_back.Bind(wx.EVT_BUTTON, self.GoBack)

    def __del__(self):
        pass

    # Virtual event handlers, override them in your derived class
    def ChangeSpotAcc(self, event):
        event.Skip()

    def ChangeMode(self, event):
        event.Skip()

    def GoBack(self, event):
        self.Hide()  # hide the register frame
        self.parent.Show()  # show the login frame

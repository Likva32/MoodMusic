import wx
import wx.xrc
from tcp_by_size import recv_by_size
from tcp_by_size import send_with_size


class MainFrame(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"Mood Music", pos=wx.DefaultPosition,
                          size=wx.Size(840, 660), style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
        self.parent = parent
        self.SetIcon(wx.Icon("images/black logo2.ico"))
        font = wx.Font(20, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Garamond")

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        bSizer32 = wx.BoxSizer(wx.VERTICAL)

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

        Sizer_logo = wx.BoxSizer(wx.VERTICAL)

        self.logo_image = wx.StaticBitmap(self.m_panel9, wx.ID_ANY,
                                          wx.Bitmap(u"images/black logo(main).png", wx.BITMAP_TYPE_ANY),
                                          wx.DefaultPosition, wx.DefaultSize, 0)
        Sizer_logo.Add(self.logo_image, 0, wx.ALL, 5)

        gbSizer_allitems.Add(Sizer_logo, wx.GBPosition(0, 0), wx.GBSpan(2, 1), 0, 5)

        Sizer_Create = wx.BoxSizer(wx.VERTICAL)

        self.button_Create = wx.Button(self.m_panel9, wx.ID_ANY, u"Create Playlist", wx.DefaultPosition, wx.DefaultSize,
                                       0)
        self.button_Create.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DDKSHADOW))

        Sizer_Create.Add(self.button_Create, 0, wx.ALL, 5)

        gbSizer_allitems.Add(Sizer_Create, wx.GBPosition(2, 0), wx.GBSpan(1, 1), wx.ALIGN_CENTER, 5)

        bSizer_accType = wx.BoxSizer(wx.VERTICAL)

        self.button_Create1 = wx.Button(self.m_panel9, wx.ID_ANY, u"Created Playlist", wx.DefaultPosition,
                                        wx.DefaultSize, 0)
        self.button_Create1.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DDKSHADOW))

        bSizer_accType.Add(self.button_Create1, 0, wx.ALL, 5)

        gbSizer_allitems.Add(bSizer_accType, wx.GBPosition(5, 0), wx.GBSpan(1, 1), wx.ALIGN_CENTER, 5)

        Sizer_userdev = wx.BoxSizer(wx.HORIZONTAL)

        self.Button_dev = wx.BitmapButton(self.m_panel9, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize,
                                          wx.BU_AUTODRAW | 0)

        self.Button_dev.SetBitmap(wx.Bitmap(u"images/face2.png", wx.BITMAP_TYPE_ANY))
        Sizer_userdev.Add(self.Button_dev, 0, wx.ALL, 5)

        gbSizer_allitems.Add(Sizer_userdev, wx.GBPosition(1, 3), wx.GBSpan(5, 7), wx.ALIGN_CENTER | wx.EXPAND, 5)

        xd_box = wx.BoxSizer(wx.HORIZONTAL)

        self.username_text = wx.StaticText(self.m_panel9, wx.ID_ANY, u"Username", wx.DefaultPosition, wx.DefaultSize, 0)
        self.username_text.Wrap(-1)

        self.username_text.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DDKSHADOW))

        xd_box.Add(self.username_text, 0, wx.EXPAND, 5)

        gbSizer_allitems.Add(xd_box, wx.GBPosition(0, 5), wx.GBSpan(1, 2), wx.ALIGN_CENTER, 5)

        xd_box1 = wx.BoxSizer(wx.HORIZONTAL)

        self.username_text1 = wx.StaticText(self.m_panel9, wx.ID_ANY, u"Camera", wx.DefaultPosition, wx.DefaultSize, 0)
        self.username_text1.Wrap(-1)

        self.username_text1.SetBackgroundColour(wx.Colour(53, 53, 53))

        xd_box1.Add(self.username_text1, 0, wx.EXPAND, 5)

        gbSizer_allitems.Add(xd_box1, wx.GBPosition(6, 5), wx.GBSpan(1, 3), wx.ALIGN_CENTER, 5)

        Sizer_login = wx.BoxSizer(wx.HORIZONTAL)

        self.Button_login = wx.Button(self.m_panel9, wx.ID_ANY, u"On", wx.DefaultPosition, wx.DefaultSize, 0)
        self.Button_login.SetLabelMarkup(u"On")
        self.Button_login.SetFont(font)
        self.Button_login.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DDKSHADOW))

        Sizer_login.Add(self.Button_login, 0, wx.ALL, 5)

        gbSizer_allitems.Add(Sizer_login, wx.GBPosition(7, 5), wx.GBSpan(1, 1), wx.ALIGN_CENTER, 5)

        Sizer_login1 = wx.BoxSizer(wx.HORIZONTAL)

        self.Button_login1 = wx.Button(self.m_panel9, wx.ID_ANY, u"Off", wx.DefaultPosition, wx.DefaultSize, 0)
        self.Button_login1.SetLabelMarkup(u"Off")
        self.Button_login1.SetFont(font)
        self.Button_login1.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DDKSHADOW))

        Sizer_login1.Add(self.Button_login1, 0, wx.ALL, 5)

        gbSizer_allitems.Add(Sizer_login1, wx.GBPosition(7, 7), wx.GBSpan(1, 1), wx.EXPAND, 5)

        Sizer_back = wx.BoxSizer(wx.VERTICAL)

        self.Button_back = wx.BitmapButton(self.m_panel9, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize,
                                           wx.BU_AUTODRAW | 0 | wx.BORDER_NONE)

        self.Button_back.SetBitmap(wx.Bitmap(u"images/back icon big.png", wx.BITMAP_TYPE_ANY))
        self.Button_back.SetBackgroundColour(wx.Colour(53, 53, 53))

        Sizer_back.Add(self.Button_back, 0, wx.ALL, 5)

        gbSizer_allitems.Add(Sizer_back, wx.GBPosition(6, 0), wx.GBSpan(4, 1), 0, 5)

        bSizer185 = wx.BoxSizer(wx.VERTICAL)

        self.m_bpButton33 = wx.BitmapButton(self.m_panel9, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize,
                                            wx.BU_AUTODRAW | 0 | wx.BORDER_NONE)

        self.m_bpButton33.SetBitmap(wx.Bitmap(u"images/setting icon resized.png", wx.BITMAP_TYPE_ANY))
        self.m_bpButton33.SetBackgroundColour(wx.Colour(53, 53, 53))

        bSizer185.Add(self.m_bpButton33, 0, wx.ALL, 5)

        gbSizer_allitems.Add(bSizer185, wx.GBPosition(0, 9), wx.GBSpan(1, 1), wx.ALIGN_CENTER , 5)

        panel_background2.Add(gbSizer_allitems, 0, wx.ALIGN_CENTER , 5)

        self.m_panel9.SetSizer(panel_background2)
        self.m_panel9.Layout()
        panel_background2.Fit(self.m_panel9)
        bSizer_panel2.Add(self.m_panel9, 1, wx.ALL | wx.EXPAND, 60)

        self.panel_background1.SetSizer(bSizer_panel2)
        self.panel_background1.Layout()
        bSizer_panel2.Fit(self.panel_background1)
        bSizer_panel1.Add(self.panel_background1, 1, wx.EXPAND | wx.ALL, 0)

        bSizer32.Add(bSizer_panel1, 1, wx.EXPAND, 5)

        self.SetSizer(bSizer32)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.button_Create.Bind(wx.EVT_BUTTON, self.Go_To_CreatePlaylist)
        self.button_Create1.Bind(wx.EVT_BUTTON, self.Go_To_CreatedPlaylist)
        self.Button_dev.Bind(wx.EVT_BUTTON, self.CAMERA)
        self.Button_login.Bind(wx.EVT_BUTTON, self.OnCamera)
        self.Button_login1.Bind(wx.EVT_BUTTON, self.OffCamera)
        self.Button_back.Bind(wx.EVT_BUTTON, self.GoBack)
        self.m_bpButton33.Bind(wx.EVT_BUTTON, self.GoToSettings)

    def __del__(self):
        pass

    # Virtual event handlers, override them in your derived class
    def Go_To_CreatePlaylist(self, event):
        event.Skip()

    def Go_To_CreatedPlaylist(self, event):
        event.Skip()

    def CAMERA(self, event):
        event.Skip()

    def OnCamera(self, event):
        event.Skip()

    def OffCamera(self, event):
        event.Skip()

    def GoBack(self, event):
        self.Hide()  # hide the register frame
        self.parent.Show()  # show the login frame

    def GoToSettings(self, event):
        event.Skip()
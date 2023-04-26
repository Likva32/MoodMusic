import wx
import wx.xrc

from Settings import SettingsFrame


class CreatePlaylistFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"Mood Music", pos=wx.DefaultPosition,
                          size=wx.Size(840, 660), style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
        self.parent = parent
        self.mood = ''
        self.name = ''
        self.Email = None
        self.client = parent.client
        self.SettingsFrame = SettingsFrame(self)
        self.SetIcon(wx.Icon("images/black logo2.ico"))
        font = wx.Font(20, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Poppins")

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        bSizer32 = wx.BoxSizer(wx.VERTICAL)

        bSizer_panel1 = wx.BoxSizer(wx.VERTICAL)

        self.panel_background1 = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.panel_background1.SetBackgroundColour(wx.Colour(20, 17, 21))

        bSizer_panel2 = wx.BoxSizer(wx.VERTICAL)

        self.m_panel9 = wx.Panel(self.panel_background1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_panel9.SetFont(
            wx.Font(20, wx.FONTFAMILY_SCRIPT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Viner Hand ITC"))
        self.m_panel9.SetBackgroundColour(wx.Colour(53, 53, 53))

        panel_background2 = wx.BoxSizer(wx.VERTICAL)

        self.m_bpButton33 = wx.BitmapButton(self.m_panel9, wx.ID_ANY, wx.NullBitmap, wx.Point(453, 34), wx.DefaultSize,
                                            wx.BU_AUTODRAW | 0 | wx.BORDER_NONE)

        self.m_bpButton33.SetBitmap(wx.Bitmap(u"images/setting icon resized.png", wx.BITMAP_TYPE_ANY))
        self.m_bpButton33.SetBackgroundColour(wx.Colour(53, 53, 53))

        panel_background2.Add(self.m_bpButton33, 0, wx.ALL, 5)

        self.Button_back = wx.BitmapButton(self.m_panel9, wx.ID_ANY, wx.NullBitmap, wx.Point(345, -1), wx.DefaultSize,
                                           wx.BU_AUTODRAW | 0 | wx.BORDER_NONE)

        self.Button_back.SetBitmap(wx.Bitmap(u"images/back icon big.png", wx.BITMAP_TYPE_ANY))
        self.Button_back.SetBackgroundColour(wx.Colour(53, 53, 53))

        panel_background2.Add(self.Button_back, 0, wx.ALL, 5)

        self.Button_login1 = wx.Button(self.m_panel9, wx.ID_ANY, u"Off", wx.Point(-1, 24), wx.DefaultSize, 0)
        self.Button_login1.SetLabelMarkup(u"Off")
        self.Button_login1.SetFont(
            wx.Font(wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL,
                    False, wx.EmptyString))
        self.Button_login1.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DDKSHADOW))

        panel_background2.Add(self.Button_login1, 0, wx.ALL, 5)

        self.Button_login = wx.Button(self.m_panel9, wx.ID_ANY, u"On", wx.Point(235, -1), wx.DefaultSize, 0)
        self.Button_login.SetLabelMarkup(u"On")
        self.Button_login.SetFont(
            wx.Font(wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL,
                    False, wx.EmptyString))
        self.Button_login.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DDKSHADOW))

        panel_background2.Add(self.Button_login, 0, wx.ALL, 5)

        self.username_text1 = wx.StaticText(self.m_panel9, label=u"34534534", pos=(400, 600))
        self.username_text1.Wrap(-1)

        self.username_text1.SetBackgroundColour(wx.Colour(53, 53, 53))

        panel_background2.Add(self.username_text1, 0, wx.EXPAND, 5)

        self.error_box_text = wx.StaticText(self.m_panel9, wx.ID_ANY, u"Camera", wx.Point(600, 500), wx.DefaultSize, 0)
        self.error_box_text.Wrap(-1)

        self.error_box_text.SetBackgroundColour(wx.Colour(53, 53, 53))

        panel_background2.Add(self.error_box_text, 1, wx.ALIGN_CENTER, 5)

        self.logo_image = wx.StaticBitmap(self.m_panel9, wx.ID_ANY,
                                          wx.Bitmap(u"images/black logo(main).png", wx.BITMAP_TYPE_ANY), wx.Point(4, 3),
                                          wx.DefaultSize, 0)
        panel_background2.Add(self.logo_image, 0, wx.ALL, 5)

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

        self.Button_back.Bind(wx.EVT_BUTTON, self.GoBack)
        # self.Button_settings.Bind(wx.EVT_BUTTON, self.GoToSettings)
        self.Bind(wx.EVT_CLOSE, self.on_close)

    def on_close(self, event):
        try:
            self.parent.on_close(event)
        except AttributeError:
            pass
        self.Destroy()

    def GoBack(self, event):
        self.Hide()  # hide the register frame
        self.parent.Show()  # show the login frame

    def GoToSettings(self, event):
        self.SettingsFrame.name_text.SetLabel(self.name)
        self.Hide()
        self.SettingsFrame.Centre()
        self.SettingsFrame.Show()

    def __str__(self):
        return "MainFrame object"

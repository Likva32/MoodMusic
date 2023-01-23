import wx
import wx.xrc
import socket
from Register import RegisterFrame


class LoginFrame(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"Mood Music", pos=wx.DefaultPosition,
                          size=wx.Size(620, 635), style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.register_frame = RegisterFrame(self)
        self.SetIcon(wx.Icon("images/black logo2.ico"))
        font = wx.Font(15, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Garamond")
        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetFont(
            wx.Font(14, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_SEMIBOLD, False, "Bookman Old Style"))

        bSizer_main = wx.BoxSizer(wx.VERTICAL)

        bSizer_panel1 = wx.BoxSizer(wx.VERTICAL)

        self.panel_background1 = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.panel_background1.SetBackgroundColour(wx.Colour(20, 17, 21))

        bSizer_panel2 = wx.BoxSizer(wx.VERTICAL)

        self.panel_background2 = wx.Panel(self.panel_background1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)
        self.panel_background2.SetFont(
            wx.Font(20, wx.FONTFAMILY_SCRIPT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Viner Hand ITC"))
        self.panel_background2.SetBackgroundColour(wx.Colour(53, 53, 53))

        bSizer_gridbag = wx.BoxSizer(wx.VERTICAL)

        gbSizer_allitems = wx.GridBagSizer(0, 0)
        gbSizer_allitems.SetFlexibleDirection(wx.BOTH)
        gbSizer_allitems.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        bSizer_accType1 = wx.BoxSizer(wx.VERTICAL)

        self.staticText_accType1 = wx.StaticText(self.panel_background2, wx.ID_ANY, u"Login", wx.DefaultPosition,
                                                 wx.DefaultSize, 0)
        self.staticText_accType1.Wrap(-1)

        self.staticText_accType1.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNHIGHLIGHT))

        bSizer_accType1.Add(self.staticText_accType1, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        gbSizer_allitems.Add(bSizer_accType1, wx.GBPosition(0, 1), wx.GBSpan(1, 1), wx.ALIGN_CENTER, 5)

        bSizer_accType = wx.BoxSizer(wx.VERTICAL)

        self.staticText_accType = wx.StaticText(self.panel_background2, wx.ID_ANY, u"Choose Account Type",
                                                wx.DefaultPosition, wx.DefaultSize, 0)
        self.staticText_accType.Wrap(-1)

        self.staticText_accType.SetFont(
            wx.Font(18, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString))
        self.staticText_accType.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNHIGHLIGHT))

        bSizer_accType.Add(self.staticText_accType, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        gbSizer_allitems.Add(bSizer_accType, wx.GBPosition(1, 1), wx.GBSpan(1, 1), wx.ALIGN_CENTER, 5)

        Sizer_userdev = wx.BoxSizer(wx.HORIZONTAL)

        Sizer_user = wx.BoxSizer(wx.VERTICAL)

        self.staticText_user = wx.StaticText(self.panel_background2, wx.ID_ANY, u"User", wx.DefaultPosition,
                                             wx.DefaultSize, 0)
        self.staticText_user.Wrap(-1)

        self.staticText_user.SetFont(
            wx.Font(18, wx.FONTFAMILY_SCRIPT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Viner Hand ITC"))
        self.staticText_user.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNHIGHLIGHT))

        Sizer_user.Add(self.staticText_user, 0, wx.ALIGN_CENTER, 5)

        self.Button_user = wx.BitmapButton(self.panel_background2, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition,
                                           wx.DefaultSize, wx.BU_AUTODRAW | wx.BU_TOP)

        self.Button_user.SetBitmap(wx.Bitmap(u"images/user resized.jpg", wx.BITMAP_TYPE_ANY))
        Sizer_user.Add(self.Button_user, 0, wx.ALL, 5)

        Sizer_userdev.Add(Sizer_user, 0, wx.ALIGN_CENTER, 5)

        Sizer_dev = wx.BoxSizer(wx.VERTICAL)

        self.staticText_dev = wx.StaticText(self.panel_background2, wx.ID_ANY, u"Developer", wx.DefaultPosition,
                                            wx.DefaultSize, 0)
        self.staticText_dev.Wrap(-1)

        self.staticText_dev.SetFont(
            wx.Font(18, wx.FONTFAMILY_SCRIPT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Viner Hand ITC"))
        self.staticText_dev.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNHIGHLIGHT))

        Sizer_dev.Add(self.staticText_dev, 0, wx.ALIGN_CENTER, 0)

        self.Button_dev = wx.BitmapButton(self.panel_background2, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition,
                                          wx.DefaultSize, wx.BU_AUTODRAW | 0)

        self.Button_dev.SetBitmap(wx.Bitmap(u"images/dev resized.jpg", wx.BITMAP_TYPE_ANY))
        Sizer_dev.Add(self.Button_dev, 0, wx.ALL, 5)

        Sizer_userdev.Add(Sizer_dev, 0, wx.ALIGN_CENTER, 5)

        gbSizer_allitems.Add(Sizer_userdev, wx.GBPosition(2, 1), wx.GBSpan(1, 1), wx.ALIGN_CENTER | wx.EXPAND, 5)

        Sizer_username = wx.BoxSizer(wx.HORIZONTAL)

        self.textCtrl_username = wx.TextCtrl(self.panel_background2, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                             wx.DefaultSize, wx.TE_CENTER | wx.BORDER_STATIC)
        self.textCtrl_username.SetFont(font)
        self.textCtrl_username.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOWTEXT))
        self.textCtrl_username.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DDKSHADOW))
        self.textCtrl_username.SetHint('Username')

        Sizer_username.Add(self.textCtrl_username, 1, wx.ALIGN_CENTER | wx.ALL, 10)

        gbSizer_allitems.Add(Sizer_username, wx.GBPosition(3, 1), wx.GBSpan(1, 1), wx.ALIGN_CENTER | wx.EXPAND, 5)

        Sizer_password = wx.BoxSizer(wx.HORIZONTAL)

        self.textCtrl_password = wx.TextCtrl(self.panel_background2, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                             wx.DefaultSize, wx.TE_CENTER | wx.TE_PASSWORD | wx.BORDER_STATIC)
        self.textCtrl_password.SetFont(font)
        self.textCtrl_password.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOWTEXT))
        self.textCtrl_password.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DDKSHADOW))
        self.textCtrl_password.SetHint('Password')

        Sizer_password.Add(self.textCtrl_password, 0, wx.LEFT, 42)

        self.Button_password = wx.Button(self.panel_background2, wx.ID_ANY, u"Forgot?", wx.DefaultPosition,
                                         wx.DefaultSize, 0 | wx.BORDER_RAISED | wx.BORDER_SIMPLE)
        self.Button_password.SetFont(font)
        self.Button_password.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_CAPTIONTEXT))
        self.Button_password.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DDKSHADOW))

        Sizer_password.Add(self.Button_password, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 5)

        gbSizer_allitems.Add(Sizer_password, wx.GBPosition(4, 1), wx.GBSpan(1, 3), wx.ALIGN_CENTER | wx.EXPAND, 5)

        Sizer_login = wx.BoxSizer(wx.HORIZONTAL)

        self.Button_login = wx.Button(self.panel_background2, wx.ID_ANY, u"Login", wx.DefaultPosition, wx.DefaultSize,
                                      0)
        self.Button_login.SetLabelMarkup(u"Login")
        self.Button_login.SetFont(font)
        self.Button_login.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DDKSHADOW))

        Sizer_login.Add(self.Button_login, 0, wx.ALL, 10)

        gbSizer_allitems.Add(Sizer_login, wx.GBPosition(5, 1), wx.GBSpan(1, 1), wx.ALIGN_CENTER | wx.EXPAND, 5)

        Sizer_noAcc = wx.BoxSizer(wx.HORIZONTAL)

        self.staticText_noAcc = wx.StaticText(self.panel_background2, wx.ID_ANY, u"No account?", wx.DefaultPosition,
                                              wx.DefaultSize, 0)
        self.staticText_noAcc.Wrap(-1)

        self.staticText_noAcc.SetFont(font)
        self.staticText_noAcc.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNHIGHLIGHT))

        Sizer_noAcc.Add(self.staticText_noAcc, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.Button_signup = wx.Button(self.panel_background2, wx.ID_ANY, u"SignUp", wx.DefaultPosition, wx.DefaultSize,
                                       0)
        self.Button_signup.SetLabelMarkup(u"SignUp")
        self.Button_signup.SetFont(font)
        self.Button_signup.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOWTEXT))
        self.Button_signup.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_GRAYTEXT))

        Sizer_noAcc.Add(self.Button_signup, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        gbSizer_allitems.Add(Sizer_noAcc, wx.GBPosition(6, 1), wx.GBSpan(1, 1), wx.ALIGN_CENTER | wx.EXPAND, 5)

        Sizer_back = wx.BoxSizer(wx.VERTICAL)

        gbSizer_allitems.Add(Sizer_back, wx.GBPosition(5, 0), wx.GBSpan(4, 1), wx.ALIGN_CENTER | wx.EXPAND, 5)

        bSizer185 = wx.BoxSizer(wx.VERTICAL)

        self.m_bpButton33 = wx.BitmapButton(self.panel_background2, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition,
                                            wx.DefaultSize, wx.BU_AUTODRAW | 0 | wx.BORDER_NONE)

        self.m_bpButton33.SetBitmap(wx.Bitmap(u"images/setting icon resized.png", wx.BITMAP_TYPE_ANY))
        self.m_bpButton33.SetBackgroundColour(wx.Colour(53, 53, 53))

        bSizer185.Add(self.m_bpButton33, 0, wx.ALL, 5)

        gbSizer_allitems.Add(bSizer185, wx.GBPosition(0, 2), wx.GBSpan(1, 1), wx.ALIGN_CENTER | wx.EXPAND, 5)

        bSizer_gridbag.Add(gbSizer_allitems, 0, wx.ALIGN_CENTER | wx.LEFT, 53)

        self.panel_background2.SetSizer(bSizer_gridbag)
        self.panel_background2.Layout()
        bSizer_gridbag.Fit(self.panel_background2)
        bSizer_panel2.Add(self.panel_background2, 1, wx.ALL | wx.EXPAND, 60)

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
        self.Button_password.Bind(wx.EVT_BUTTON, self.GoToForgot)
        self.Button_login.Bind(wx.EVT_BUTTON, self.Login)
        self.Button_signup.Bind(wx.EVT_BUTTON, self.GoToSignup)
        self.m_bpButton33.Bind(wx.EVT_BUTTON, self.GoToSettings)
        self.connect()

    def connect(self):

        my_ip = socket.gethostbyname(socket.gethostname())
        PORT = 5052
        ADDR = (my_ip, PORT)
        try:
            self.client.connect(ADDR)
            print('good')
        except:
            print('fail')

    # Virtual event handlers, override them in your derived class
    def typeUser(self, event):
        event.Skip()

    def typeDev(self, event):
        event.Skip()

    def GoToForgot(self, event):
        event.Skip()

    def Login(self, event):
        event.Skip()

    def GoToSignup(self, event):
        self.Hide()  # hide the login frame
        self.register_frame.Centre()
        self.register_frame.Show()  # show the register frame

    def GoToSettings(self, event):
        event.Skip()


# Virtual event handlers, override them in your derived class

if __name__ == '__main__':
    app = wx.App()
    frame = LoginFrame(None)
    frame.Show()

    frame.Centre()
    app.MainLoop()

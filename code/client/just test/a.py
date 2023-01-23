import wx


class LoginFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, title="Login")
        self.register_frame = RegisterFrame(self)
        self.panel = wx.Panel(self)

        self.username_label = wx.StaticText(self.panel, label="Username:")
        self.username_txt = wx.TextCtrl(self.panel)

        self.password_label = wx.StaticText(self.panel, label="Password:")
        self.password_txt = wx.TextCtrl(self.panel, style=wx.TE_PASSWORD)

        self.login_button = wx.Button(self.panel, label="Login")
        self.login_button.Bind(wx.EVT_BUTTON, self.on_login)

        self.register_button = wx.Button(self.panel, label="Register")
        self.register_button.Bind(wx.EVT_BUTTON, self.on_register)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.username_label, 0, wx.ALL, 5)
        self.sizer.Add(self.username_txt, 0, wx.ALL, 5)
        self.sizer.Add(self.password_label, 0, wx.ALL, 5)
        self.sizer.Add(self.password_txt, 0, wx.ALL, 5)
        self.sizer.Add(self.login_button, 0, wx.ALL, 5)
        self.sizer.Add(self.register_button, 0, wx.ALL, 5)
        self.panel.SetSizer(self.sizer)

    def on_login(self, event):
        # Perform login action here
        pass

    def on_register(self, event):
        self.Hide()  # hide the login frame
        self.register_frame.Show()  # show the register frame


class RegisterFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, title="Register")
        self.panel = wx.Panel(self)
        self.parent = parent

        # Add labels, text fields, and buttons for registration here
        self.register_button = wx.Button(self.panel, label="back")
        self.register_button.Bind(wx.EVT_BUTTON, self.on_cancel)

    def on_submit(self, event):
        # Perform registration action here
        pass

    def on_cancel(self, event):
        self.Hide()  # hide the register frame
        self.parent.Show()  # show the login frame


class MainFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, title="Main")
        self.panel = wx.Panel(self)

        # Add widgets for the main screen here


class MyApp(wx.App):
    def OnInit(self):
        self.login_frame = LoginFrame(None)

        self.login_frame.Show()
        return True


if __name__ == '__main__':
    app = MyApp()
    app.MainLoop()

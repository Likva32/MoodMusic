"""
    Module Name: ForgotPassword

    Description: This module contains the implementation of the ForgotFrame class, which represents a frame for password recovery functionality in the Mood Music application.

    Dependencies:
        - hashlib: A module providing various hashing algorithms.
        - json: A module for working with JSON data.
        - wx: A GUI toolkit for Python.
        - loguru: A library for logging.
        - validators: A library for data validation.
        - Settings: A module containing the SettingsFrame class.

    Classes:
        - ForgotFrame: Represents a frame for password recovery functionality.

    Author: Artur Tkach (Likva32 in GitHub)
"""

import hashlib
import json

import wx
import wx.xrc
from loguru import logger
from validators import email

from Settings import SettingsFrame


class ForgotFrame(wx.Frame):
    """
       Represents a frame for password recovery functionality in the Mood Music application.

       Attributes:
           - parent (wx.Window): The parent window that contains the frame.
           - client: The client object used for communication.
           - Email (str): The email address entered by the user.
           - Code (str): The code entered by the user.
           - SettingsFrame (SettingsFrame): An instance of the SettingsFrame class.
           - panel_background1 (wx.Panel): The main panel of the frame.
           - header_text (wx.StaticText): The static text widget for the header.
           - image (wx.StaticBitmap): The static bitmap widget for the image.
           - textCtrl_first (wx.TextCtrl): The text control widget for entering the email or code.
           - textCtrl_second (wx.TextCtrl): The text control widget for entering the password or confirmation password.
           - status_text (wx.StaticText): The static text widget for displaying status messages.
           - Button_login (wx.Button): The button widget for sending the email, code, or password.
           - Button_back (wx.BitmapButton): The button widget for going back to the previous screen.
           - Button_settings (wx.BitmapButton): The button widget for opening the settings frame.

       Methods:
           - __init__(parent): Initializes the ForgotFrame object.
           - on_close(event): Event handler for the close event of the frame.
           - EmailScreen(): Sets up the initial screen for entering the email address.
           - SendEmail(event): Event handler for sending the email.
           - CodeScreen(): Sets up the screen for entering the code.
           - SendCode(event): Event handler for sending the code.
           - PasswordScreen(): Sets up the screen for entering the new password.
           - SendPassword(event): Event handler for sending the new password.
           - GoBack(event): Event handler for going back to the previous screen.
           - GoToSettings(event): Event handler for opening the settings frame.

       """
    def __init__(self, parent):
        """
                Initializes the ForgotFrame object.
                Args:
                    - parent (wx.Window): The parent window that contains the frame.
        """
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
        """
            Handles the close event of the window.
            Calls the 'on_close' method of the parent window (if available) and destroys the current window.
        """
        try:
            self.parent.on_close(event)
        except AttributeError:
            pass
        self.Destroy()

    def EmailScreen(self):
        """
            Sets up the email screen UI.
            Binds the 'SendEmail' method to the login button's 'EVT_BUTTON' event.
            Hides 'textCtrl_second' control.
            Sets the hint for 'textCtrl_first' to 'Email'.
        """
        self.Button_login.Bind(wx.EVT_BUTTON, self.SendEmail)
        self.textCtrl_second.Hide()
        self.textCtrl_first.SetHint('Email')

    def SendEmail(self, event):
        """
            Sends the email to the server for verification.
            Retrieves the email from 'textCtrl_first'.
            Serializes the email into JSON format and sends it to the server.
            If the email is valid, proceeds to the code screen.
            Displays error messages for invalid email or server response.
        """
        self.status_text.SetLabelText('')
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
        """
            Sets up the code screen UI.
            Clears 'textCtrl_first'.
            Sets the hint for 'textCtrl_first' to 'Code'.
            Binds the 'SendCode' method to the login button's 'EVT_BUTTON' event.
        """
        self.status_text.SetLabelText('')
        self.textCtrl_first.SetValue('')
        self.textCtrl_first.SetHint('Code')
        self.Button_login.Bind(wx.EVT_BUTTON, self.SendCode)

    def SendCode(self, event):
        """
           Sends the verification code to the server.
           Retrieves the code from 'textCtrl_first'.
           Serializes the code and email into JSON format and sends it to the server.
           If the code is verified, proceeds to the password screen.
           Displays error messages for incorrect code or server response.
        """
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
        """
            Sets up the password screen UI.
            Sets 'textCtrl_first' and 'textCtrl_second' to password style.
            Clears the values of 'textCtrl_first' and 'textCtrl_second'.
            Shows 'textCtrl_second' control.
            Set hints for password and confirm password fields.
            Binds the 'SendPassword' method to the login button's 'EVT_BUTTON' event.
        """
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
        """
            Sends the password to the server for account registration.
            Retrieves the passwords from 'textCtrl_first' and 'textCtrl_second'.
            Generates an MD5 hash of the password.
            Serializes the email, hashed password, and function identifier into JSON format and sends it to the server.
            If the passwords match, displays a success message.
            Displays error messages for password mismatch or server response.
        """
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
        """
            Handles the 'Go Back' action.
            Hides the current window, sets up the email screen UI, and shows the parent window.
        """
        self.Hide()
        self.EmailScreen()
        self.parent.Show()

    def GoToSettings(self, event):
        """
            Handles the 'Go To Settings' action.
            Hides the current window, hides 'button_changespot' control of the 'SettingsFrame',
            centers the 'SettingsFrame', and shows it.
        """
        self.Hide()
        self.SettingsFrame.button_changespot.Hide()
        self.SettingsFrame.Centre()
        self.SettingsFrame.Show()

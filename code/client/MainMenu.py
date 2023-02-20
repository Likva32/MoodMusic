import json
import threading

import cv2
import wx
import wx.xrc
from wx.lib import statbmp

from Settings import SettingsFrame
from tcp_by_size import recv_by_size
from tcp_by_size import send_with_size


class MainFrame(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"Mood Music", pos=wx.DefaultPosition,
                          size=wx.Size(840, 660), style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
        self.parent = parent
        self.name = ''
        self.Email = None
        self.client = parent.client
        self.camStatus = False
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

        self.button_Created = wx.Button(self.m_panel9, wx.ID_ANY, u"Created Playlist", wx.DefaultPosition,
                                        wx.DefaultSize, 0)
        self.button_Created.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DDKSHADOW))

        bSizer_accType.Add(self.button_Created, 0, wx.ALL, 5)

        gbSizer_allitems.Add(bSizer_accType, wx.GBPosition(5, 0), wx.GBSpan(1, 1), wx.ALIGN_CENTER, 5)

        #################################

        # self.capture = cv2.VideoCapture(0)
        self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

        # ret, frame = self.capture.read()
        # frame = cv2.resize(frame, (400, 320))
        # height, width = frame.shape[:2]

        self.image = cv2.imread('images/nocamblack.jpg')
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        self.bmp = wx.Bitmap.FromBuffer(400, 320, self.image)
        # print(f"{width} + {height}")
        self.timer = wx.Timer(self)
        self.fps = 60
        # self.timer.Start(int(self.timer.Start(int())))
        self.userCam = statbmp.GenStaticBitmap(self.m_panel9, wx.ID_ANY, self.bmp)

        # self.Button_Cam = wx.BitmapButton(self.m_panel9, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize,
        #                                   wx.BU_AUTODRAW | 0)
        #
        # self.Button_Cam.SetBitmap(wx.Bitmap(u"images/face2.png", wx.BITMAP_TYPE_ANY))
        # Sizer_userCam.Add(self.Button_Cam, 0, wx.ALL, 5)
        gbSizer_allitems.Add(self.userCam, wx.GBPosition(1, 3), wx.GBSpan(5, 7), wx.ALIGN_CENTER, 5)

        error_box_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.error_box_text = wx.StaticText(self.m_panel9, wx.ID_ANY, u"", wx.DefaultPosition, wx.DefaultSize, 0)
        self.error_box_text.Wrap(-1)

        error_box_sizer.Add(self.error_box_text, 1, wx.ALIGN_CENTER, 5)

        gbSizer_allitems.Add(error_box_sizer, wx.GBPosition(6, 5), wx.GBSpan(1, 1), wx.ALIGN_CENTER, 5)

        xd_box = wx.BoxSizer(wx.HORIZONTAL)

        self.username_text = wx.StaticText(self.m_panel9, wx.ID_ANY, self.name, wx.DefaultPosition, wx.DefaultSize, 0)
        self.username_text.Wrap(-1)
        self.username_text.SetFont(
            wx.Font(28, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Poppins"))

        xd_box.Add(self.username_text, 0, wx.EXPAND, 5)

        gbSizer_allitems.Add(xd_box, wx.GBPosition(0, 5), wx.GBSpan(1, 2), wx.ALIGN_CENTER, 5)

        xd_box1 = wx.BoxSizer(wx.HORIZONTAL)

        self.text_camera = wx.StaticText(self.m_panel9, wx.ID_ANY, u"Camera", wx.DefaultPosition, wx.DefaultSize, 0)
        self.text_camera.Wrap(-1)

        self.text_camera.SetBackgroundColour(wx.Colour(53, 53, 53))

        xd_box1.Add(self.text_camera, 0, wx.EXPAND, 5)

        gbSizer_allitems.Add(xd_box1, wx.GBPosition(7, 5), wx.GBSpan(1, 3), wx.ALIGN_CENTER, 5)

        Sizer_login = wx.BoxSizer(wx.HORIZONTAL)

        self.Button_on = wx.Button(self.m_panel9, wx.ID_ANY, u"On", wx.DefaultPosition, wx.DefaultSize, 0)
        self.Button_on.SetLabelMarkup(u"On")
        self.Button_on.SetFont(font)
        self.Button_on.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DDKSHADOW))

        Sizer_login.Add(self.Button_on, 0, wx.ALL, 5)

        gbSizer_allitems.Add(Sizer_login, wx.GBPosition(8, 5), wx.GBSpan(1, 1), wx.ALIGN_CENTER, 5)

        Sizer_login1 = wx.BoxSizer(wx.HORIZONTAL)

        self.Button_off = wx.Button(self.m_panel9, wx.ID_ANY, u"Off", wx.DefaultPosition, wx.DefaultSize, 0)
        self.Button_off.SetLabelMarkup(u"Off")
        self.Button_off.SetFont(font)
        self.Button_off.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DDKSHADOW))

        Sizer_login1.Add(self.Button_off, 0, wx.ALL, 5)

        gbSizer_allitems.Add(Sizer_login1, wx.GBPosition(8, 7), wx.GBSpan(1, 1), wx.EXPAND, 5)

        Sizer_back = wx.BoxSizer(wx.VERTICAL)

        self.Button_back = wx.BitmapButton(self.m_panel9, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize,
                                           wx.BU_AUTODRAW | 0 | wx.BORDER_NONE)

        self.Button_back.SetBitmap(wx.Bitmap(u"images/back icon big.png", wx.BITMAP_TYPE_ANY))
        self.Button_back.SetBackgroundColour(wx.Colour(53, 53, 53))

        Sizer_back.Add(self.Button_back, 0, wx.ALL, 5)

        gbSizer_allitems.Add(Sizer_back, wx.GBPosition(6, 0), wx.GBSpan(4, 1), 0, 5)

        bSizer185 = wx.BoxSizer(wx.VERTICAL)

        self.Button_settings = wx.BitmapButton(self.m_panel9, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition,
                                               wx.DefaultSize,
                                               wx.BU_AUTODRAW | 0 | wx.BORDER_NONE)

        self.Button_settings.SetBitmap(wx.Bitmap(u"images/setting icon resized.png", wx.BITMAP_TYPE_ANY))
        self.Button_settings.SetBackgroundColour(wx.Colour(53, 53, 53))

        bSizer185.Add(self.Button_settings, 0, wx.ALL, 5)

        gbSizer_allitems.Add(bSizer185, wx.GBPosition(0, 9), wx.GBSpan(1, 1), wx.ALIGN_CENTER, 5)

        panel_background2.Add(gbSizer_allitems, 0, wx.ALIGN_CENTER, 5)

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
        self.button_Created.Bind(wx.EVT_BUTTON, self.Go_To_CreatedPlaylist)
        self.Button_on.Bind(wx.EVT_BUTTON, self.camera_on_thread)
        self.Button_off.Bind(wx.EVT_BUTTON, self.OffCamera)
        self.Button_back.Bind(wx.EVT_BUTTON, self.GoBack)
        self.Button_settings.Bind(wx.EVT_BUTTON, self.GoToSettings)
        self.Bind(wx.EVT_TIMER, self.NextFrame)

    def NextFrame(self, event):
        try:
            ret, frame = self.capture.read()
            frame = cv2.resize(frame, (400, 320))
            if ret:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                self.bmp.CopyFromBuffer(frame)
                self.userCam.SetBitmap(self.bmp)
        except Exception as e:
            self.error_box_text.SetLabelText("cant grab image from cam")
            self.error_box_text.SetForegroundColour(colour='red')
            self.timer.Stop()
            print(e)

    def Go_To_CreatePlaylist(self, event):
        dict = {
            'Func': 'GetAllTracks',
            'Email': self.Email,
        }
        data_send = json.dumps(dict)
        send_with_size(self.client, data_send)
        msg = recv_by_size(self.client)
        print(msg)

    def Go_To_CreatedPlaylist(self, event):
        dict = {
            'Func': 'GetUser',
            'Email': self.Email,
        }
        data_send = json.dumps(dict)
        send_with_size(self.client, data_send)
        msg = recv_by_size(self.client)
        print(msg)

    def camera_on_thread(self, event):
        thread = threading.Thread(target=self.OnCamera)
        thread.start()

    def OnCamera(self):
        try:
            self.capture = cv2.VideoCapture(0)
            wx.CallAfter(self.timer.Start)
            # self.timer.Start()
            self.error_box_text.SetLabelText('Camera On')
            self.error_box_text.SetForegroundColour(colour='green')
        except Exception as e:
            self.error_box_text.SetLabelText("cant grab image from cam")
            self.error_box_text.SetForegroundColour(colour='red')
            self.timer.Stop()
            print(e)

    def OffCamera(self, event):
        try:
            self.capture.release()
            self.timer.Stop()
            self.userCam.SetBitmap(wx.Bitmap.FromBuffer(400, 320, self.image))
            self.error_box_text.SetLabelText('Camera Off')
            self.error_box_text.SetForegroundColour(colour='Black')
        except:
            pass

    def GoBack(self, event):
        self.Hide()  # hide the register frame
        self.parent.Show()  # show the login frame

    def GoToSettings(self, event):
        self.SettingsFrame.name_text.SetLabel(self.name)
        self.Hide()
        self.SettingsFrame.Centre()
        self.SettingsFrame.Show()

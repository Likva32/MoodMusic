import socket
import wx
from tcp_by_size import send_with_size
from Login import LoginFrame


class client:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        my_ip = socket.gethostbyname(socket.gethostname())
        self.IP = my_ip  # '127.0.0.1'
        self.PORT = 5051
        self.ADDR = (self.IP, self.PORT)
        self.FORMAT = 'utf-8'
        self.running = True
        try:
            #self.client.connect(self.ADDR)
            self.gui()
        except Exception as e:
            print(e)

    def gui(self):
        app = wx.App()
        frame = LoginFrame(None)
        frame.Show()

        frame.Centre()
        app.MainLoop()


if __name__ == '__main__':
    client()

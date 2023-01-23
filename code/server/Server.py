import socket
import threading
from tcp_by_size import recv_by_size
from tcp_by_size import send_with_size
from DataBase.Users import Users
import smtplib
import ssl
from email.message import EmailMessage


class server:
    def __init__(self):
        print(socket.gethostbyname(socket.gethostname()))
        self.UsersDb = Users()
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.running = True
        self.IP = socket.gethostbyname(socket.gethostname())
        self.PORT = 5056
        self.ADDR = (self.IP, self.PORT)
        self.FORMAT = 'utf-8'
        self.server.bind(self.ADDR)
        self.server.listen()
        self.FORMAT = 'utf-8'
        print(f"[LISTENING] Server is listening on {self.server}")
        self.main()

    def main(self):
        while self.running:
            try:
                conn, addr = self.server.accept()
                print(f"[CONNECTION] user connected successfully, addr: {addr}")
                thread = threading.Thread(target=self.case, args=(conn, addr))
                thread.daemon = True
                thread.start()
            except:
                self.running = False
                self.server.close()

    def case(self, conn, addr):
        while True:
            data = recv_by_size(conn)
            print(data)
            if len(data) == 0:
                print('disconnect')
                break
            arr = data.split('@')
            func = arr[0]
            if func == 'register':
                if not self.UsersDb.is_exist(arr[2]):
                    try:
                        self.UsersDb.insert_user(arr[1], arr[2], arr[3])
                        send_with_size(conn, 'user inserted success')
                        print('user inserted success')
                    except:
                        send_with_size(conn, 'user inserted NOT success')
                        print('user inserted NOT success')
                else:
                    send_with_size(conn, 'user exist')
                    print('user exist')
            if func == 'login':
                if self.UsersDb.Login(arr[1], arr[2]):
                    send_with_size(conn, 'Login success')
                    print('Login success')
                else:
                    send_with_size(conn, 'Login NOT success')
                    print('Login NOT success')
            if func == 'sendmail':
                pass
                pass


if __name__ == '__main__':
    server()

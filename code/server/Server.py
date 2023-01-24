import socket
import threading
from tcp_by_size import recv_by_size
from tcp_by_size import send_with_size
from DataBase.Users import Users
import smtplib
import ssl
import uuid
from SendMail import SendVerificationCode
from validators import email


class server:
    def __init__(self):
        print(socket.gethostbyname(socket.gethostname()))
        self.UsersDb = Users()
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.running = True
        self.IP = socket.gethostbyname(socket.gethostname())
        self.PORT = 5061
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
            arr = data.split('*')
            func = arr[0]
            print(arr)
            if func == 'register':
                if not self.UsersDb.is_exist(arr[2]):
                    if email(arr[2]):
                        flag = self.UsersDb.insert_user(arr[1], arr[2], arr[3])
                        if flag:
                            send_with_size(conn, 'Email inserted success')
                            print('Email inserted success')
                        else:
                            send_with_size(conn, 'user inserted NOT success')
                            print('Email inserted NOT success')
                    else:
                        send_with_size(conn, 'invalid email')
                        print('invalid email')
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
                if self.UsersDb.is_exist(arr[1]):
                    sendmail = SendVerificationCode(arr[1])
                    sendmail.SendMail()
                    code = sendmail.security_code
                    self.UsersDb.update_code(arr[1], code)
                    send_with_size(conn, 'Code Sended')
                    print('Code Sended')
                else:
                    send_with_size(conn, 'user NOT exist')
                    print('user NOT exist')
            if func == 'sendcode':
                if self.UsersDb.verify_code(arr[1], arr[2]):
                    send_with_size(conn, 'Code verified')
                    print('Code verified')
                else:
                    send_with_size(conn, 'Code NOT verified')
                    print('Code NOT verified')
            if func == 'sendpass':
                flag = self.UsersDb.update_password(arr[1], arr[2])
                if flag:
                    send_with_size(conn, 'Password Changed')
                    print('Password Changed')
                else:
                    send_with_size(conn, 'Password NOT Changed')
                    print('Password NOT Changed')
            if func == '':
                pass


if __name__ == '__main__':
    server()

import json
import socket
import threading

from validators import email

from DataBase.Users import Users
from Spotifyfunc import MySpotifyFunc
from lib.SendMail import SendVerificationCode
from lib.secretsId import email_sender, email_password
from lib.tcp_by_size import recv_by_size
from lib.tcp_by_size import send_with_size
from workedFlask import MyFlaskApp


class server:
    def __init__(self):
        print(socket.gethostbyname(socket.gethostname()))
        self.UsersDb = Users()
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.running = True
        self.IP = socket.gethostbyname(socket.gethostname())
        self.PORT = 5059
        self.ADDR = (self.IP, self.PORT)
        self.FORMAT = 'utf-8'
        self.server.bind(self.ADDR)
        self.server.listen()
        self.FORMAT = 'utf-8'
        thread = threading.Thread(target=self.create_flask)
        thread.start()
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
            data_recv = recv_by_size(conn)
            data_recv = json.loads(data_recv)
            print(data_recv)
            if len(data_recv) == 0:
                print('disconnect')
                break
            if data_recv['Func'] == 'Register':
                if not self.UsersDb.is_exist(data_recv['Email']):
                    if email(data_recv['Email']):
                        flag = self.UsersDb.insert_user(data_recv['Name'], data_recv['Email'], data_recv['Password'])
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
            if data_recv['Func'] == 'Login':
                if self.UsersDb.Login(data_recv['Email'], data_recv['Password']):
                    send_with_size(conn, 'Login success')
                    print('Login success')
                else:
                    send_with_size(conn, 'Login NOT success')
                    print('Login NOT success')
            if data_recv['Func'] == 'Sendmail':
                print(data_recv['Email'])
                if self.UsersDb.is_exist(data_recv['Email']):
                    sendmail = SendVerificationCode(email_sender, email_password, data_recv['Email'])
                    sendmail.SendMail()
                    code = sendmail.security_code
                    self.UsersDb.update_code(data_recv['Email'], code)
                    send_with_size(conn, 'Code Sended')
                    print('Code Sended')
                else:
                    send_with_size(conn, 'user NOT exist')
                    print('user NOT exist')
            if data_recv['Func'] == 'Sendcode':
                if self.UsersDb.verify_code(data_recv['Email'], data_recv['Code']):
                    send_with_size(conn, 'Code verified')
                    print('Code verified')
                else:
                    send_with_size(conn, 'Code NOT verified')
                    print('Code NOT verified')
            if data_recv['Func'] == 'Sendpass':
                flag = self.UsersDb.update_password(data_recv['Email'], data_recv['Password'])
                if flag:
                    send_with_size(conn, 'Password Changed')
                    print('Password Changed')
                else:
                    send_with_size(conn, 'Password NOT Changed')
                    print('Password NOT Changed')
            if data_recv['Func'] == 'GetName':
                data_send = self.UsersDb.name_by_email(data_recv['Email'])
                send_with_size(conn, data_send)

            if data_recv['Func'] == 'SpotAuth':
                send_with_size(conn, "enter the site")
            if data_recv['Func'] == 'GetAllTracks':
                sp = MySpotifyFunc(data_recv['Email'])
                x = sp.get_all_tracks()
                send_with_size(conn, x)
            if data_recv['Func'] == 'GetUser':
                sp = MySpotifyFunc(data_recv['Email'])
                x = sp.get_current_user()
                send_with_size(conn, x)
            if data_recv['Func'] == 'CheckUrl':
                x = self.UsersDb.check_url(data_recv['Email'])
                print(x)
                send_with_size(conn, x)
            if data_recv['Func'] == '':
                pass

    def create_flask(self):
        app = MyFlaskApp('Mood Music')
        app.run()


if __name__ == '__main__':
    server()

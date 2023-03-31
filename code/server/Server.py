import json
import socket
import threading

import cv2
import numpy as np
from keras.models import load_model
from validators import email

from DataBase.Users import Users
from Spotifyfunc import MySpotifyFunc
from lib.SendMail import SendVerificationCode
from lib.secret import email_sender, email_password
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
        self.model = load_model('model\MAYBE_FINAL\model3.h5')
        thread = threading.Thread(target=self.create_flask)
        thread.start()
        print(f"[LISTENING] Server is listening on {self.server}")
        self.emotion_labels = {
            0: 'Angry',  # +
            1: 'Disgust',  #
            2: 'Fear',  #
            3: 'Happy',  # +
            4: 'Sad',  # +
            5: 'Surprise',  # -
            6: 'Neutral'  # -
        }
        self.faceCascade = cv2.CascadeClassifier('model\MAYBE_FINAL\haarcascade_frontalface_default.xml')
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
            if len(data_recv) == 0:
                print(f"client {addr} DISCONNECTED")
                break
            data_recv = json.loads(data_recv)
            print(data_recv)

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
            if data_recv['Func'] == 'CreatePlaylist':
                sp = MySpotifyFunc(data_recv['Email'])
                x = sp.create_playlist(data_recv['Mood'])
                send_with_size(conn, x)
            if data_recv['Func'] == 'GetUser':
                sp = MySpotifyFunc(data_recv['Email'])
                x = sp.get_current_user()
                send_with_size(conn, x)
            if data_recv['Func'] == 'CheckUrl':
                x = self.UsersDb.check_url(data_recv['Email'])
                print(x)
                send_with_size(conn, x)
            if data_recv['Func'] == 'Predict':
                frame = data_recv['Frame']
                frame = np.array(frame)
                frame = frame.astype(np.uint8)
                result = self.Predict(frame)
                if type(result) == type((0, 0)):
                    mood = result[1]
                    new_frame = result[0]
                else:
                    mood = "Neutral"
                    new_frame = result
                mood = 'Angry'
                dict = {
                    'Frame': new_frame.tolist(),
                    'Mood': mood
                }
                data_send = json.dumps(dict)
                send_with_size(conn, data_send)
            if data_recv['Func'] == '':
                pass

    def Predict2(self, frame):
        return frame

    def Predict(self, frame):

        font_scale = 1.5
        font = cv2.FONT_HERSHEY_PLAIN

        rectangle_bgr = (255, 0, 0)
        img = np.zeros((400, 320))

        text = 'some text'
        (text_width, text_hieght) = cv2.getTextSize(text, font, font_scale, thickness=1)[0]
        text_offset_x = 10
        text_offset_y = img.shape[0] - 25

        box_coords = ((text_offset_x, text_offset_y), (text_offset_x + text_width + 2, text_offset_y - text_hieght - 2))
        cv2.rectangle(img, box_coords[0], box_coords[1], rectangle_bgr, cv2.FILLED)
        cv2.putText(img, text, (text_offset_x, text_offset_y), font, fontScale=font_scale, color=(0, 0, 0), thickness=1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.faceCascade.detectMultiScale(gray, 1.1, 4)

        face_roi_gray = None
        x, y, w, h = 0, 0, 0, 0
        for x1, y1, w1, h1 in faces:
            x, y, w, h = x1, y1, w1, h1
            roi_gray = gray[y1:y1 + h1, x:x1 + w1]
            cv2.rectangle(frame, (x1, y1), (x1 + w1, y1 + h1), (255, 0, 0), 2)
            faces = self.faceCascade.detectMultiScale(roi_gray)
            face_roi_gray = roi_gray
            if len(faces) == 0:

                frame2 = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                return frame2
            else:
                for (ex, ey, ew, eh) in faces:
                    face_roi_gray = roi_gray[ey:ey + eh, ex:ex + ew]
        if face_roi_gray is None:
            return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        final_image = cv2.resize(face_roi_gray, (48, 48))
        final_image = np.expand_dims(final_image, axis=0)
        final_image = final_image.reshape(1, 48, 48, 1)
        final_image = final_image / 255.0

        Predict = self.model.predict(final_image)
        predicted_label = np.argmax(Predict)

        status = self.emotion_labels[int(predicted_label)]

        x1, y1, w1, h1 = 0, 0, 175, 50
        cv2.rectangle(frame, (x1, y1), (x1 + w1, y1 + h1), (0, 0, 0), -1)
        cv2.putText(frame, status, (x1 + int(w1 / 10), y1 + int(h1 / 2)), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                    (0, 0, 255), 2)

        cv2.putText(frame, status, (x, y - 10), font, 3, (0, 0, 255), 2, cv2.LINE_4)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255))
        frame2 = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        print(status)
        if not status:
            status = 'Neutral'
        return frame2, status

    def create_flask(self):
        app = MyFlaskApp('Mood Music')
        app.run()


if __name__ == '__main__':
    server()

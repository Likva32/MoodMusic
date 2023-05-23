"""
    Module Name: Server
    Description: This module provides functionality for a server that handles user registration, login, email verification, Spotify integration, emotion prediction, and more.
    Dependencies:
        - json
        - socket
        - sys
        - threading
        - cv2
        - numpy
        - keras.models
        - loguru.logger
        - validators.email
        - rsa
        - DataBase.SpotifyPlaylist.SpotifyStat
        - DataBase.Users.Users
        - Spotifyfunc.MySpotifyFunc
        - lib.SendMail.SendVerificationCode
        - lib.secret.email_sender
        - lib.secret.email_password
        - lib.tcp_by_size.recv_by_size
        - lib.tcp_by_size.send_with_size
        - workedFlask.MyFlaskApp

    Classes:
        - server: A class representing the server for handling user requests and managing connections.

    Author: Artur Tkach (Likva32 on GitHub)
"""
import json
import socket
import sys
import threading

# import downloaded libs
import cv2
import numpy as np
from keras.models import load_model
from loguru import logger
from validators import email
import rsa

# import libs that I wrote by myself
from DataBase.SpotifyPlaylist import SpotifyStat
from DataBase.Users import Users
from Spotifyfunc import MySpotifyFunc
from lib.SendMail import SendVerificationCode
from lib.secret import email_sender, email_password
from lib.tcp_by_size import recv_by_size
from lib.tcp_by_size import send_with_size
from workedFlask import MyFlaskApp


class server:
    """
        A class representing the server for handling user requests and managing connections.

        Attributes:
            UsersDb (DataBase.Users.Users): An instance of the Users class for user database operations.
            SpotifyStatDB (DataBase.SpotifyPlaylist.SpotifyStat): An instance of the SpotifyStat class for Spotify playlist statistics.
            server (socket.socket): The server socket object for accepting client connections.
            running (bool): Flag indicating whether the server is running.
            IP (str): The IP address of the server.
            PORT (int): The port number of the server.
            ADDR (tuple): The address tuple consisting of IP and PORT.
            FORMAT (str): The encoding format used for communication.
            model (keras.models.Model): The pre-trained emotion prediction model.
            faceCascade (cv2.CascadeClassifier): The classifier for detecting faces in frames.

        Methods:
            __init__(): Initializes the server and sets up the necessary configurations.
            main(): Main loop that listens for client connections and handles them.
            case(conn, addr): Handles the client requests and performs the corresponding actions.
            Predict(frame): Predicts the emotion from a given frame using a pre-trained model.
            create_flask(): Creates and runs a Flask application for additional functionality.
    """
    def __init__(self):
        """
            Initializes the server and sets up the necessary configurations.
        """
        logger.info("IP: " + socket.gethostbyname(socket.gethostname()))
        self.UsersDb = Users()
        self.SpotifyStatDB = SpotifyStat()

        self.SpotifyStatDB.insert_first_stat()
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.running = True

        try:
            if sys.argv[1] == "Local" or sys.argv[1] == "local":
                self.IP = socket.gethostbyname(socket.gethostname())
            else:
                self.IP = sys.argv[1]
            self.PORT = int(sys.argv[2])
        except:
            self.IP = socket.gethostbyname(socket.gethostname())
            self.PORT = 5005

        self.ADDR = (self.IP, self.PORT)
        self.FORMAT = 'utf-8'
        public_key, private_key = rsa.newkeys(1024)
        self.server.bind(self.ADDR)
        self.server.listen()
        self.model = load_model('model\\MAYBE_FINAL\\model3.h5')
        thread = threading.Thread(target=self.create_flask)
        thread.start()
        logger.info(f"[LISTENING] Server is listening on {self.server}")
        self.emotion_labels = {
            0: 'Angry',  # + Heavy Metal, Hardcore, Punk, Rap, Industrial
            1: 'Disgust',  # Experimental, Noise, Grindcore, Death Metal
            2: 'Fear',  # Dark Ambient, Horrorcore, Industrial, Darkwave, Drone
            3: 'Happy',  # +  Pop, Dance, Electronic, Indie Pop, Reggae
            4: 'Sad',  # +  Blues, Jazz, Folk, Indie, Ambient
            5: 'Surprise',  # -  Classical, Jazz, World, Experimental
            6: 'Neutral'  # - Classical, Ambient, New Age, Instrumental, Soundtrack
        }
        self.faceCascade = cv2.CascadeClassifier('model\\MAYBE_FINAL\\haarcascade_frontalface_default.xml')

        self.main()

    def main(self):
        """
            Main loop that listens for client connections and handles them.
        """
        while self.running:
            try:
                conn, addr = self.server.accept()
                logger.success(f"[CONNECTION] user connected successfully, addr: {addr}")
                thread = threading.Thread(target=self.case, args=(conn, addr))
                thread.daemon = True
                thread.start()
            except:
                self.running = False
                self.server.close()

    def case(self, conn, addr):
        """
                Handles the client requests and performs the corresponding actions.

                Parameters:
                    conn (socket.socket): The connection socket object.
                    addr (str): The address of the client.
        """
        try:
            while self.running:
                data_recv = recv_by_size(conn)
                if len(data_recv) == 0 or data_recv is None:
                    logger.info(f"client {addr} DISCONNECTED")
                    break
                data_recv = json.loads(data_recv)
                if data_recv['Func'] == 'Register':
                    # Handle user registration
                    msg = ''
                    if not self.UsersDb.is_exist(data_recv['Email']):
                        if email(data_recv['Email']):
                            flag = self.UsersDb.insert_user(data_recv['Name'], data_recv['Email'],
                                                            data_recv['Password'])
                            if flag:
                                msg = 'Email inserted success'
                                logger.success('Email inserted success')
                            else:
                                msg = 'user inserted NOT success'
                                logger.error('Email inserted NOT success')
                        else:
                            msg = 'invalid email'
                            logger.error('invalid email')
                    else:
                        msg = 'user exist'
                        logger.info('user exist')
                    send_with_size(conn, msg)
                if data_recv['Func'] == 'Login':
                    # Handle user login
                    if self.UsersDb.Login(data_recv['Email'], data_recv['Password']):
                        send_with_size(conn, 'Login success')
                        logger.success('Login success')
                    else:
                        send_with_size(conn, 'Login NOT success')
                        logger.error('Login NOT success')
                if data_recv['Func'] == 'Sendmail':
                    # Handle sending verification code via email
                    if self.UsersDb.is_exist(data_recv['Email']):
                        sendmail = SendVerificationCode(email_sender, email_password, data_recv['Email'])
                        sendmail.SendMail()
                        code = sendmail.security_code
                        self.UsersDb.update_code(data_recv['Email'], code)
                        send_with_size(conn, 'Code Sended')
                        logger.success('Code Sended')
                    else:
                        send_with_size(conn, 'user NOT exist')
                        logger.error('user NOT exist')
                if data_recv['Func'] == 'Sendcode':

                    if self.UsersDb.verify_code(data_recv['Email'], data_recv['Code']):
                        send_with_size(conn, 'Code verified')
                        logger.success('Code verified')
                    else:
                        send_with_size(conn, 'Code NOT verified')
                        logger.error('Code NOT verified')
                if data_recv['Func'] == 'Sendpass':
                    flag = self.UsersDb.update_password(data_recv['Email'], data_recv['Password'])
                    if flag:
                        send_with_size(conn, 'Password Changed')
                        logger.success('Password Changed')
                    else:
                        send_with_size(conn, 'Password NOT Changed')
                        logger.error('Password NOT Changed')
                if data_recv['Func'] == 'GetName':
                    data_send = self.UsersDb.name_by_email(data_recv['Email'])
                    send_with_size(conn, data_send)

                if data_recv['Func'] == 'SpotAuth':
                    send_with_size(conn, self.IP)

                if data_recv['Func'] == 'CreatePlaylist':
                    sp = MySpotifyFunc(data_recv['Email'])
                    x = sp.create_playlist(data_recv['Mood'])
                    self.SpotifyStatDB.update_stat(data_recv['Mood'])
                    send_with_size(conn, x)
                if data_recv['Func'] == 'GetUser':
                    try:
                        sp = MySpotifyFunc(data_recv['Email'])
                        x = sp.get_current_user()
                    except:
                        x = 'No Spotify linked'
                    send_with_size(conn, x)
                if data_recv['Func'] == 'CheckUrl':
                    x = self.UsersDb.check_url(data_recv['Email'])
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
                    msg = {
                        'Frame': new_frame.tolist(),
                        'Mood': mood
                    }
                    data_send = json.dumps(msg)
                    send_with_size(conn, data_send)
                if data_recv['Func'] == '':
                    pass
        except ConnectionResetError:
            conn.close()
            logger.error("The remote host forcibly terminated the existing connection")
        except:
            conn.close()
            logger.error("ERROR - Disconnect Client")

    def Predict(self, frame):
        """
                Predicts the emotion from a given frame using a pre-trained model.

                Parameters:
                    frame (numpy.ndarray): The input frame.
                Returns: tuple or numpy.ndarray: If emotion prediction is successful, it returns a tuple containing the processed frame and the predicted emotion.
                         Otherwise, it returns the original frame.
        """

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
        logger.info(status)
        if not status:
            status = 'Neutral'
        return frame2, status

    def create_flask(self):
        """
            Creates and runs a Flask application for additional functionality.
        """
        app = MyFlaskApp('Mood Music')
        app.run(self.IP)


if __name__ == '__main__':
    server()

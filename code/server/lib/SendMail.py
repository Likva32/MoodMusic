"""
    Module Name: SendMail
    Description: This module provides a class for sending a verification code via email.

    Dependencies:
        - smtplib: Required for sending emails using the SMTP protocol.
        - ssl: Required for creating a secure SSL/TLS connection.
        - uuid: Required for generating a unique security code.
        - email.message.EmailMessage: Required for creating an email message.

    Classes:
        SendVerificationCode: A class for sending a verification code via email.

    Author: Artur Tkach (Likva32 on GitHub)
"""
import smtplib
import ssl
import uuid
from email.message import EmailMessage


class SendVerificationCode:
    """
        A class for sending a verification code via email.

        Attributes:
            email_sender (str): The email address of the sender.
            email_password (str): The password for the sender's email account.
            email_receiver (str): The email address of the receiver.
            security_code (str): The generated security code for verification.

        Methods:
            SendMail(): Sends an email with the verification code.
    """
    def __init__(self, email_sender, email_password, email_receiver):
        """
            Initialize the SendVerificationCode object.

            Args:
                email_sender (str): The email address of the sender.
                email_password (str): The password for the sender's email account.
                email_receiver (str): The email address of the receiver.
        """
        self.email_sender = email_sender
        self.email_password = email_password
        self.email_receiver = email_receiver
        self.security_code = str(uuid.uuid4())
        half_length = len(self.security_code) // 2
        self.security_code = self.security_code[:half_length]

    def SendMail(self):
        """
            Sends an email with the verification code.

            The email contains a temporary security code for the MoodMusic Account,
            which can only be used once within the next 5 minutes before it expires.

            Returns:
                None
        """
        subject = 'Artur Security Code'
        body = f"""


        Hi,



        Here is a temporary security code for your MoodMusic Account. It can only be used once within the next 5 minutes, after which it will expire:

        {self.security_code}



        Did you receive this email without having an active request from MoodMusic to enter a verification code? If so, the security of your MoodMusic account may be compromised. Please change your password as soon as possible.



        Sincerely,

        Your dear ARTUR
        """
        em = EmailMessage()
        em['From'] = self.email_sender
        em['To'] = self.email_receiver
        em['Subject'] = subject
        em.set_content(body)

        # Add SSL (layer of security)
        context = ssl.create_default_context()

        # Log in and send the email

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(self.email_sender, self.email_password)
            smtp.sendmail(self.email_sender, self.email_receiver, em.as_string())

import smtplib
import ssl
import uuid
from email.message import EmailMessage
from validators import email


class SendVerificationCode:
    def __init__(self, email_receiver):
        # Define email sender and receiver
        self.email_sender = 'companymoodmusic@gmail.com'
        self.email_password = 'sosdxdenkxkfgvmg'
        self.email_receiver = email_receiver
        self.security_code = str(uuid.uuid4())
        half_length = len(self.security_code) // 2
        self.security_code = self.security_code[:half_length]

    def SendMail(self):
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


email2 = "example@domain.com"

if email(email2):
    print("valid email")
else:
    print("invalid email")


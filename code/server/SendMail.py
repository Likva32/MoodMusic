import smtplib
import ssl
import uuid
from email.message import EmailMessage

# Define email sender and receiver
email_sender = 'companymoodmusic@gmail.com'
email_password = 'sosdxdenkxkfgvmg'
email_receiver = 'sushko.ariel@gmail.com'
security_code = str(uuid.uuid4())
half_length = len(security_code) // 2
security_code = security_code[:half_length]


# Set the subject and body of the email
subject = 'Artur Security Code'
body = f"""


Hi,

 

Here is a temporary security code for your MoodMusic Account. It can only be used once within the next 5 minutes, after which it will expire:

{security_code}

 

Did you receive this email without having an active request from MoodMusic to enter a verification code? If so, the security of your MoodMusic account may be compromised. Please change your password as soon as possible.

 

Sincerely,

Your dear ARTUR
"""

em = EmailMessage()
em['From'] = email_sender
em['To'] = email_receiver
em['Subject'] = subject
em.set_content(body)

# Add SSL (layer of security)
context = ssl.create_default_context()

# Log in and send the email

with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
    smtp.login(email_sender, email_password)
    smtp.sendmail(email_sender, email_receiver, em.as_string())
# x =uuid.uuid1()
# print(x)
# print(uuid.uuid3(x, 'name'))
# print(uuid.uuid4())
# print(uuid.uuid5())
import smtplib
import ssl
from email.message import EmailMessage

from decouple import config

# Email configuration
msg = EmailMessage()

sender_email = config('EMAIL_SENDER', cast=str)
message = "There has been a new email has been uploaded to the provided playlist."

msg['Subject'] = 'A new video has been added to the playlist'
msg['From'] = sender_email
msg['To'] = sender_email
msg.set_content(message)


class EmailSender:
    def __init__(self):
        self.smtp_server = config('SERVER', cast=str)
        self.password = config('PASSWORD', cast=str)
        self.port = config('PORT', cast=int)

    def send_email(self):
        try:
            # Create a secure smtp server connection
            smtp_server = smtplib.SMTP_SSL(self.smtp_server, self.port)
            smtp_server.ehlo()

            smtp_server.login(sender_email, config('PASSWORD', cast=str))
            smtp_server.send_message(msg)
            smtp_server.close()
        except Exception as ex:
            print("Something went wrong….", ex)

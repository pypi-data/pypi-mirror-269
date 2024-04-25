import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class AlertOnException:
    def __init__(self, receiver_email, subject=None, message=None):
        self.receiver_email = receiver_email
        self.subject = subject
        self.message = message

        msg = MIMEMultipart()
        sender_email = "exceptionotifier@gmail.com"
        pwd = "risi brcr jhuo clql"

        msg["From"] = sender_email
        msg["To"] = self.receiver_email
        msg["Subject"] = self.subject
        msg.attach(MIMEText(self.message, "plain"))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        try:
            server.starttls()
            server.login(sender_email, pwd)
            text = msg.as_string()
            server.sendmail(sender_email, self.receiver_email, text)
        finally:
            server.quit()

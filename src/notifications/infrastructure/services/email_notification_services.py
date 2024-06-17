import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

class EmailService:
    def __init__(self):
        self.host = os.getenv('EMAIL_HOST')
        self.port = os.getenv('EMAIL_PORT')
        self.user = os.getenv('EMAIL_USER')
        self.password = os.getenv('EMAIL_PASS')

    def send_email(self, to, subject, body):
        try:
            msg = MIMEMultipart()
            msg['From'] = self.user
            msg['To'] = to
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))

            server = smtplib.SMTP(self.host, self.port)
            server.starttls()
            server.login(self.user, self.password)
            text = msg.as_string()
            server.sendmail(self.user, to, text)
            server.quit()
        except smtplib.SMTPConnectError as e:
            print(f'Error while connecting to SMTP server: {str(e)}')
        except Exception as e:
            print(f'Error while sending email: {str(e)}')
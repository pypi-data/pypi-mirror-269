from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import smtplib
import json
import os


class Email:

    def __init__(self, from_address, host, port, username, password, recipients, subject=None, error_recipients=None):
        self.from_address = from_address
        self.recipients = json.loads(recipients)
        self.error_recipients = error_recipients
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.subject = subject

    def send_email(self, message, filename=None, filedir=None, warning=None, subject=None):
        try:
            if warning:
                recipients = self.error_recipients
            else:
                recipients = self.recipients

            subject = subject or self.subject
            msg = MIMEMultipart()
            msg['From'] = self.from_address
            msg['Subject'] = "{}".format(subject)
            body = MIMEText('<p>{}</p>'.format(message), 'html', 'utf-8')
            msg.attach(body)
            if filename:
                for file in filename:
                    dir_path = os.path.join(filedir, 'spreadsheets')
                    file_path = os.path.join(dir_path, file)
                    attachment = MIMEApplication(open(file_path, "rb").read(), _subtype="txt")
                    attachment.add_header('Content-Disposition', 'attachment', filename=file)
                    msg.attach(attachment)
            server = smtplib.SMTP(self.host, self.port)
            print(self.host, self.port)
            print(self.username, self.password)
            server.login(self.username, self.password)
            text = msg.as_string()

            server.sendmail(self.from_address, recipients, text)
            server.quit()
            return True, recipients
        except Exception as e:
            return False, e

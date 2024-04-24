from notificationmethods.notificacion import Notificacion
import requests
import ssl
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader

class Email(Notificacion):
    def __init__(self, sender, api_key, host,mode = 'test', psw = None, port = None
                ):
        self.sender = sender
        self.host = host
        self.api_key = api_key
        self.mode = mode
        self.psw = psw
        self.port = port

    def send(self, to, subject, reply_to, bcc, attachments=None,
             body='<p>--Emtpy--</p>'):
        try:
            files = []
            if self.mode == 'prod':
                for attachment in attachments:
                    file_opened = open(attachment,'rb')
                    files.append(('attachment',file_opened))
                    
                response = requests.post(
                    f"https://api.mailgun.net/v3/{self.host}/messages",
                    auth=("api", self.api_key),
                    data={
                        "from": self.sender,
                        "to": to,
                        "subject": subject,
                        "html": body,
                        'h:Reply_to':reply_to,
                        'bcc':bcc,
                    },
                    files = files
                )
                return response
            else:
                context = ssl.create_default_context()
                server = smtplib.SMTP(self.host, self.port)
                server.ehlo(name=self.host)
                server.starttls(context=context)
                server.ehlo(name=self.host)
                server.login(self.sender, self.psw)
                if isinstance(to, str):
                    to = [i.strip() for i in to.split(',') if i.strip()]
                msg = MIMEMultipart()
                msg.attach(MIMEText(body, 'html'))
                msg['Subject'] = subject
                msg['From'] = self.sender
                msg['To'] = ', '.join(to)
                msg['reply-to'] = reply_to
                to += bcc
                if attachments:
                    for attachment in attachments:
                        part = MIMEBase('application', 'octet-stream')
                        with open(attachment, 'rb') as f:
                            part.set_payload(f.read())
                        encoders.encode_base64(part)
                        part.add_header('Content-Disposition', 'attachment',
                                        filename=attachment.split('/')[-1])
                        msg.attach(part)
                response = server.sendmail(self.sender, to, msg.as_string())
                return response
        except Exception as error:
            print(error)
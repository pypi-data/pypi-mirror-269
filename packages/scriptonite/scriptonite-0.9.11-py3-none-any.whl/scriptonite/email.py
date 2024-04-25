from curses.ascii import EM
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import logging

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class EmailMessage:
    """
    An email message.

    Attributes are:
    - **sender**: the From field of the email
    - **recipient**: the To field of the email
    - **subject**: well, the subject of the email
    - **body**: the text part of the message
    - **cclist**: a list of email addresses that will receive a copy of the email
    """

    def __init__(self, sender: str,
                 recipient: str,
                 subject: str,
                 body: str,
                 cclist: list = []):

        message = MIMEMultipart()
        message['From'] = sender
        message['To'] = recipient
        if cclist:
            message['Cc'] = ','.join(cclist)
        message['Subject'] = subject

        # Attach body
        message.attach(MIMEText(body, 'plain'))

        self.payload = message

    def attach_file(self,
                    attachment: str) -> None:
        """
        Attach a file to the email

        Parameters:
        - **attachment**: full path to the file to be attached
        """
        with open(attachment, 'rb') as fd:
            self.payload.attach_data(fd.read(),
                                     filename=attachment)

    def attach_data(self, data: bytes,
                    filename: str) -> None:
        """
        Attach a bytes object to the message, useful if you built a file in the
        script and need to send it without having to save it in a
        temporary file

        Parameters:
        - **data**: the bytes stream that we want to attach
        - **filename**: the name of the attachment
        """
        part = MIMEBase("application", "octet-stream")
        part.set_payload(data)
        encoders.encode_base64(part)
        part.add_header("Content-Disposition",
                        f"attachment; filename={filename}")
        self.payload.attach(part)


class EmailSender:
    """
    A connector to an SMTP server

    Parameters:
    - **server**: the server name
    - **port**: the server port, defaults to 587 (submission)
    - **username**: the username used to authenticate
    - **password**: the password used to authenticate
    - **starttls**: if we want to use STARTTLS

    If username and password are empty authentication will be disabled
    """

    def __init__(self, server: str,
                 username: str = "",
                 password: str = "",
                 starttls: bool = True,
                 port: int = 587) -> None:
        self.server = server
        self.port = port
        self.username = username
        self.password = password
        self.auth = bool(self.username and self.password)
        self.starttls = starttls

    def send(self, message: EmailMessage) -> None:
        """
        Send an EmailMessage object, built with the above class
        Errors are not trapped and exception will be raised, it is up to the
        calling script to trap them

        Parameters:
        - **message**: an EmailMessage object
        """
        with smtplib.SMTP(self.server, self.port) as server:
            if self.starttls:
                server.starttls()  # Enable secure connection
            if self.auth:
                server.login(self.username, self.password)
            server.send_message(message.payload)
            log.info('Email sent successfully.')

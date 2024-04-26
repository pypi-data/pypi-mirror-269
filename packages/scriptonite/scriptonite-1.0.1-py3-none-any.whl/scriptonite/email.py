from dataclasses import dataclass
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


class EmailMessage:
    """
    An email message.

    """

    def __init__(self, sender: str,
                 recipients: list,
                 subject: str,
                 body: str,
                 cclist: list = []):
        """
        :param sender: the From field of the email
        :param recipients: the To field of the email, is a list
        :param subject: well, the subject of the email
        :param body: the text part of the message
        :param cclist: a list of email addresses that will receive
                       a copy of the email

        To send an email to a single address use
        `recipient=["recipient@domain"]`

        """
        message = MIMEMultipart()
        message['From'] = sender
        message['To'] = ",".join(recipients)
        if cclist:
            message['Cc'] = ','.join(cclist)
        message['Subject'] = subject

        # Attach body
        message.attach(MIMEText(body, 'plain'))

        self._payload = message

    def attach_file(self,
                    attachment: str) -> None:
        """
        Attach a file to the email

        :param attachment: full path to the file to be attached
        """
        with open(attachment, 'rb') as fd:
            self._payload.attach_data(fd.read(),
                                      filename=attachment)

    def attach_data(self, stream: bytes,
                    filename: str) -> None:
        """
        Attach a bytes object to the message, useful if you built a file in the
        script and need to send it without having to save it in a
        temporary file

        :param stream: the bytes stream that we want to attach
        :param filename: the name of the attachment
        """
        part = MIMEBase("application", "octet-stream")
        part.set_payload(stream)
        encoders.encode_base64(part)
        part.add_header("Content-Disposition",
                        f"attachment; filename={filename}")
        self._payload.attach(part)


@dataclass
class EmailSender:
    """
    A connector to an SMTP server
    """

    def __init__(self, server: str,
                 username: str = "",
                 password: str = "",
                 starttls: bool = True,
                 port: int = 587) -> None:
        """
        :param server: the server name
        :param port: the server port, defaults to 587 (submission)
        :param username: the username used to authenticate
        :param password: the password used to authenticate
        :param starttls: if we want to use STARTTLS
        :type server: str

        If `username` and `password` are empty authentication will be disabled
        """

        self.server = server
        self.port = port
        self.username = username
        self.password = password
        self._auth = bool(self.username and self.password)
        self.starttls = starttls

    def send(self, message: EmailMessage) -> None:
        """
        Send an EmailMessage object, built with the above class
        Errors are not trapped and exception will be raised, it is up to the
        calling script to trap them

        :param message: an EmailMessage object
        """
        with smtplib.SMTP(self.server, self.port) as server:
            if self.starttls:
                server.starttls()  # Enable secure connection
            if self._auth:
                server.login(self.username, self.password)
            server.send_message(message._payload)

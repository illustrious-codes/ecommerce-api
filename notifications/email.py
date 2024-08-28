
from django.core import mail
from django.template.loader import render_to_string
import threading

class EmailThread(threading.Thread):
    def __init__(self, plain_message, subject, html_message, from_email, receiver):
        threading.Thread.__init__(self)
        self.subject = subject
        self.plain_message = plain_message
        self.from_email = from_email
        self.receiver = receiver
        self.html_message = html_message

    def run(self):
        mail.send_mail(
            subject=self.subject,
            message=str(self.plain_message),
            from_email=self.from_email,
            recipient_list=[self.receiver],
            html_message=self.html_message
        )

class Email:
    def __init__(
        self, 
        subject: str = "Ecommerce",
        receiver: str = "",
        plain_message: str = "",
        template: str = "",
        data = {},
    ) -> None:
        self.subject = subject
        self.receiver = receiver
        self.from_email = "From <no_reply@ecommerce.com>"
        self.plain_message = plain_message
        self.template = template
        self.data = data

    def send(self):
        try: 
            html_message = render_to_string(f"{self.template}", self.data)
            EmailThread(
                self.subject,
                self.receiver,
                self.plain_message,
                html_message,
                self.template,
            ).start()
        except Exception as e:
                print(f"Send Email: {e}")
                
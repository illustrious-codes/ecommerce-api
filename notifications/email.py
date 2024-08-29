
from django.core import mail
from django.template.loader import render_to_string
import threading

class EmailThread(threading.Thread):
    def __init__(self, subject, from_email, receiver, plain_message,  html_message):
        threading.Thread.__init__(self)
        self.subject = subject
        self.from_email = from_email
        self.receiver = receiver
        self.plain_message = plain_message
        self.html_message = html_message

    def run(self):
        mail.send_mail(
            subject=self.subject,
            from_email=self.from_email,
            recipient_list=[self.receiver],
            message=str(self.plain_message),
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
        self.from_email = "From <onatayodavid105@gmail.com>"
        self.plain_message = plain_message
        self.template = template
        self.data = data

    def send(self):
        try: 
            html_message = render_to_string(f"{self.template}", self.data)
            EmailThread(
                self.subject,
                self.from_email,
                self.receiver,
                self.plain_message,
                html_message,
            ).start()
        except Exception as e:
                print(f"Send Email: {e}")
                
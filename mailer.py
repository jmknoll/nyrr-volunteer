import requests
import json

from util import Status
from config import MAIL_API_KEY


class Mailer:
    def __init__(self):
        self.url = "https://api.postmarkapp.com/email"
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-Postmark-Server-Token": MAIL_API_KEY,
        }

    def send(self, from_email, to_email, subject, html_body, message_stream):
        data = {
            "From": from_email,
            "To": to_email,
            "Subject": subject,
            "HtmlBody": html_body,
            "MessageStream": message_stream,
        }
        res = requests.post(self.url, headers=self.headers, data=json.dumps(data))

        data = res.json()
        return data

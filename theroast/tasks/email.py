from theroast.extensions import celery
import time
from textwrap import dedent
from flask_mail import Message
from ..extensions import mail
from ..app import create_app
import json
from ..theroast.lib.utils import construct_newsletter_html

@celery.task
def send_email(app = None, data: dict = None, html: str = None):
    app = app or create_app()
    with app.app_context():
        msg = Message('Hello', sender = 'fishtuna908@gmail.com', recipients = ['fishtuna908@gmail.com'])
        msg.html = html if html else construct_newsletter_html(data)
        mail.send(msg)
    return "Sent"
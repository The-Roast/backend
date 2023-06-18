from app import Message
from app import mail
from time import time
import json
msg = Message(subject='Test Email', sender='bearseascape@gmail.com', recipients=['tanushchop@gmail.com'])
msg.body = 'This is a scheduled test email.'
msg.extra_headers = {'X-SMTPAPI': json.dumps({'send_at': time() + 120})}
mail.send(msg)

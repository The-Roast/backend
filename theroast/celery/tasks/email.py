from typing import Any, Dict
import emails
from emails.template import JinjaTemplate
from celery.result import AsyncResult
import json

from theroast.config import server_config
from theroast.celery.worker import celery_app, logger

# @celery_app.task(name="send_email")
def send_email(
    email_to: str,
    subject_template: str = "",
    html_template: str = "",
    environment: Dict[str, Any] = {},
) -> None:
    # logger.info(f"Here")
    assert server_config.EMAILS_ENABLED, "Emailing is not enabled."
    message = emails.Message(
        subject=JinjaTemplate(subject_template),
        html=JinjaTemplate(html_template),
        mail_from=(server_config.EMAILS_FROM_NAME, server_config.EMAILS_FROM_EMAIL),
    )
    # logger.info(f"Message: {message.as_string()}")
    smtp_options = {"host": server_config.SMTP_HOST, "port": server_config.SMTP_PORT}
    if server_config.SMTP_TLS:
        smtp_options["tls"] = True
    if server_config.SMTP_USER:
        smtp_options["user"] = server_config.SMTP_USER
    if server_config.SMTP_PASSWORD:
        smtp_options["password"] = server_config.SMTP_PASSWORD
    # logger.info("Header: " + json.dumps(smtp_options))
    response = message.send(to=email_to, render=environment, smtp=smtp_options)
    # logger.info(f"Response: {response}")
    return None
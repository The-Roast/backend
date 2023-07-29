from typing import Any, Dict, Optional
from pathlib import Path
import emails
from emails.template import JinjaTemplate

from theroast.config import server_config


def send_email(
    email_to: str,
    subject_template: str = "",
    html_template: str = "",
    environment: Dict[str, Any] = {},
) -> None:
    assert server_config.EMAILS_ENABLED, "no provided configuration for email variables"
    message = emails.Message(
        subject=JinjaTemplate(subject_template),
        html=JinjaTemplate(html_template),
        mail_from=(server_config.EMAILS_FROM_NAME, server_config.EMAILS_FROM_EMAIL),
    )
    smtp_options = {"host": server_config.SMTP_HOST, "port": server_config.SMTP_PORT}
    if server_config.SMTP_TLS:
        smtp_options["tls"] = True
    if server_config.SMTP_USER:
        smtp_options["user"] = server_config.SMTP_USER
    if server_config.SMTP_PASSWORD:
        smtp_options["password"] = server_config.SMTP_PASSWORD
    response = message.send(to=email_to, render=environment, smtp=smtp_options)

def send_reset_password_email(email_to: str, email: str, token: str) -> None:
    project_name = server_config.PROJECT_NAME
    subject = f"{project_name} - Password recovery for user {email}"
    with open(Path(server_config.EMAIL_TEMPLATES_DIR) / "reset_password.html") as f:
        template_str = f.read()
    server_host = server_config.SERVER_HOST
    link = f"{server_host}/reset-password?token={token}"
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={
            "project_name": server_config.PROJECT_NAME,
            "username": email,
            "email": email_to,
            "valid_hours": server_config.EMAIL_RESET_TOKEN_EXPIRE_HOURS,
            "link": link,
        },
    )

def send_new_account_email(email_to: str, username: str, password: str) -> None:
    project_name = server_config.PROJECT_NAME
    subject = f"{project_name} - New account for user {username}"
    with open(Path(server_config.EMAIL_TEMPLATES_DIR) / "new_account.html") as f:
        template_str = f.read()
    link = server_config.SERVER_HOST
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={
            "project_name": server_config.PROJECT_NAME,
            "username": username,
            "password": password,
            "email": email_to,
            "link": link,
        },
    )
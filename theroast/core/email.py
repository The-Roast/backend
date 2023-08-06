from pathlib import Path

from theroast.config import server_config
from theroast.celery.tasks.email import send_email


def send_reset_password_email(email_to: str, email: str, token: str) -> None:
    project_name = server_config.PROJECT_NAME
    subject = f"{project_name} - Password recovery for user {email}"
    with open(Path(server_config.EMAIL_TEMPLATES_DIR) / "reset_password.html") as f:
        template_str = f.read()
    server_host = server_config.SERVER_HOST
    link = f"{server_host}/reset-password?token={token}"
    send_email.delay(
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

def send_new_account_email(email_to: str, first_name: str, username: str, password: str) -> None:
    project_name = server_config.PROJECT_NAME
    subject = f"{project_name} - New account for user {first_name}"
    with open(Path(server_config.EMAIL_TEMPLATES_DIR) / "create_account.html") as f:
        template_str = f.read()
    link = server_config.SERVER_HOST
    send_email.delay(
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

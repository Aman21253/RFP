import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_email_sendgrid(subject: str, message: str, to_email: str):
    api_key = os.environ.get("SENDGRID_API_KEY")
    from_email = os.environ.get("DEFAULT_FROM_EMAIL")
    if not api_key:
        raise Exception("SENDGRID_API_KEY missing")
    if not from_email:
        raise Exception("DEFAULT_FROM_EMAIL missing")

    mail = Mail(
        from_email=from_email,
        to_emails=to_email,
        subject=subject,
        plain_text_content=message,
    )
    sg = SendGridAPIClient(api_key)
    sg.send(mail)
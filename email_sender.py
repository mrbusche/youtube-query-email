import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from config import EMAIL_PASSWORD, SENDER_EMAIL


def send_email(recipient_emails, subject, body):
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()

        server.login(SENDER_EMAIL, EMAIL_PASSWORD)

        if isinstance(recipient_emails, str):
            recipient_emails = [recipient_emails]

        for recipient in recipient_emails:
            msg = MIMEMultipart()
            msg["From"] = SENDER_EMAIL
            msg["To"] = recipient
            msg["Subject"] = subject

            msg.attach(MIMEText(body, "plain"))

            server.send_message(msg)
            print(f"Email sent successfully to {recipient}")

        server.quit()

    except Exception as e:
        print(f"Failed to send email: {str(e)}")

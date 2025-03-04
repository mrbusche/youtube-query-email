from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from config import DAYS_BACK, EMAIL_PASSWORD, SENDER_EMAIL
from youtube_api import get_video_stats


def format_results(search_term, results):
    email_body = (
        f"Here are the most viewed videos for '{search_term}' in the last {DAYS_BACK} days\n"
    )
    email_body += "=" * 75 + "\n\n"

    for i, video in enumerate(results, 1):
        video_url = f"https://www.youtube.com/watch?v={video['video_id']}"

        # Convert the published_at time to a more readable format
        published_date = datetime.strptime(video["published_at"], "%Y-%m-%dT%H:%M:%SZ")
        formatted_date = published_date.strftime("%Y-%m-%d %I:%M %p")

        email_body += f"{i}. Title: {video['title']}\n"
        email_body += f"Watch at: {video_url}\n"
        email_body += f"Channel: {video['channel']}\n"
        email_body += f"Published: {formatted_date}\n"

        # Add comment status
        if video["already_commented"]:
            email_body += "Status: Already commented on this video\n"
        elif not video["already_commented"]:
            email_body += "Status: No comment yet\n"
        else:
            email_body += "Status: Unable to check comment status\n"

        # Get and add video statistics
        stats = get_video_stats(video["video_id"])
        if stats:
            email_body += f"Views: {stats['views']}\n"
            email_body += f"Likes: {stats['likes']}\n"
            email_body += f"Comments: {stats['comments']}\n"

        email_body += "-" * 75 + "\n\n"

    return email_body


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

from datetime import datetime

import pytz

from config import DAYS_BACK, RECIPIENT_EMAILS, SEARCH_TERMS
from email_sender import send_email
from youtube_api import get_video_stats, youtube_search


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
        if video["already_commented"] is True:
            email_body += "Status: Already commented on this video\n"
        elif video["already_commented"] is False:
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


def main():
    print("Starting YouTube search...")
    all_results = ""

    for search_term in SEARCH_TERMS:
        print(f"Searching for: {search_term}")
        results = youtube_search(search_term)

        if results:
            print(f"Found {len(results)} results")
            all_results += format_results(search_term, results)
        else:
            print(f"No results found for {search_term}")

    if all_results:
        central = pytz.timezone("America/Chicago")
        current_datetime = datetime.now(central).strftime("%B %d, %Y at %I %p")
        subject = f"YouTube Videos to watch for {current_datetime}"
        print("RECIPIENT_EMAILS: ", RECIPIENT_EMAILS)
        print("DAYS_BACK: ", DAYS_BACK)
        print("subject: ", subject)
        print("all_results: ", all_results)
        send_email(RECIPIENT_EMAILS, subject, all_results)
        print("Search complete and results emailed!")
    else:
        print("No results found for any search terms.")


if __name__ == "__main__":
    main()

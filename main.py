from datetime import datetime

import pytz

from config import DAYS_BACK, RECIPIENT_EMAILS, SEARCH_TERMS
from emails import send_email
from transcription import get_transcript
from youtube_api import youtube_search


def main():
    print("Starting YouTube search...")
    all_results = []

    for search_term in SEARCH_TERMS:
        print(f"Searching for: {search_term}")
        results = youtube_search(search_term)
        all_results += results

    if all_results:
        central = pytz.timezone("America/Chicago")
        current_datetime = datetime.now(central).strftime("%B %d, %Y at %I %p")
        subject = f"YouTube Videos to watch for {current_datetime}"
        print(f"RECIPIENT_EMAILS: {RECIPIENT_EMAILS}")
        print(f"DAYS_BACK: {DAYS_BACK}")
        print(f"subject: {subject}")
        for result in all_results:
            result["transcription"] = get_transcript(result["video_id"])
        send_email(RECIPIENT_EMAILS, subject, all_results)
        print("Search complete and results emailed!")
    else:
        print("No results found for any search terms.")


if __name__ == "__main__":
    main()

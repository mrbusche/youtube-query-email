from datetime import datetime
import pytz

from config import DAYS_BACK, RECIPIENT_EMAILS, SEARCH_TERMS
from emails import format_results, send_email
from youtube_api import get_video_stats, youtube_search


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
        print(f"RECIPIENT_EMAILS: {RECIPIENT_EMAILS}")
        print(f"DAYS_BACK: {DAYS_BACK}")
        print(f"subject: {subject}")
        print(f"all_results: {all_results}")
        send_email(RECIPIENT_EMAILS, subject, all_results)
        print("Search complete and results emailed!")
    else:
        print("No results found for any search terms.")


if __name__ == "__main__":
    main()

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime, timedelta, timezone
from config import API_KEY, MAX_RESULTS, SORT_ORDER, DAYS_BACK, YOUTUBE_USERNAME

def check_if_commented(youtube, video_id):
    try:
        # Get all comments for the video
        comments = youtube.commentThreads().list(
            part='snippet',
            videoId=video_id,
            maxResults=100,
            textFormat='plainText'
        ).execute()

        # Check if any comments are from our channel
        for item in comments.get('items', []):
            comment = item['snippet']['topLevelComment']['snippet']
            author_name = comment['authorDisplayName']

            # Check for your channel name (both with and without @)
            if author_name in [f'@{YOUTUBE_USERNAME}', YOUTUBE_USERNAME]:
                print(f"Found existing comment on video {video_id}")
                return True

        print(f"No existing comment found on video {video_id}")
        return False

    except HttpError as e:
        if e.resp.status == 403:  # Comments might be disabled
            print(f"Unable to check comments for video {video_id} - Comments might be disabled")
        else:
            print(f"Error checking comments: {e}")
        return None

def youtube_search(query):
    try:
        # Create YouTube API client
        youtube = build('youtube', 'v3', developerKey=API_KEY)

        # Calculate date based on DAYS_BACK config
        days_ago = (datetime.now(timezone.utc) - timedelta(days=DAYS_BACK)).strftime('%Y-%m-%dT%H:%M:%SZ')

        # Call the search.list method with parameters from config
        search_response = youtube.search().list(
            q=query,
            part='id,snippet',
            maxResults=MAX_RESULTS,
            order=SORT_ORDER,
            publishedAfter=days_ago,
            type='video'
        ).execute()

        # Process the results
        videos = []
        for search_result in search_response.get('items', []):
            if search_result['id']['kind'] == 'youtube#video':
                video_id = search_result['id']['videoId']

                # Check if we've already commented
                already_commented = check_if_commented(youtube, video_id)

                videos.append({
                    'title': search_result['snippet']['title'],
                    'video_id': video_id,
                    'channel': search_result['snippet']['channelTitle'],
                    'description': search_result['snippet']['description'],
                    'published_at': search_result['snippet']['publishedAt'],
                    'url': f"https://www.youtube.com/watch?v={video_id}",
                    'already_commented': already_commented
                })

        return videos

    except HttpError as e:
        print(f'An HTTP error {e.resp.status} occurred: {e.content}')
        return None

def get_video_stats(video_id):
    try:
        youtube = build('youtube', 'v3', developerKey=API_KEY)

        # Call the videos.list method for statistics
        video_response = youtube.videos().list(
            part='statistics,snippet',
            id=video_id
        ).execute()

        if video_response['items']:
            stats = video_response['items'][0]['statistics']
            return {
                'views': stats.get('viewCount', 'N/A'),
                'likes': stats.get('likeCount', 'N/A'),
                'comments': stats.get('commentCount', 'N/A')
            }
        return None

    except HttpError as e:
        print(f'An HTTP error {e.resp.status} occurred: {e.content}')
        return None

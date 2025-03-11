import os

import whisper
import yt_dlp


def download_audio_from_youtube(video_url, output_path="audio.mp3"):
    """
    Downloads the audio from the provided YouTube video URL
    and saves it as an MP3 file.
    """
    if os.path.exists(output_path):
        print(f"File already exists: {output_path}")
        return output_path

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_path.replace(".mp3", ""),
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
        "quiet": False,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])
    return output_path


def transcribe_audio(audio_path, model_size="base"):
    """
    Transcribes the given audio file using OpenAI's Whisper.
    You can choose different model sizes such as "tiny", "base", "small", "medium", "large".
    """
    # Load the Whisper model (this may take a moment)
    model = whisper.load_model(model_size)
    result = model.transcribe(audio_path)
    return result["text"]


def get_transcript(video_id):
    # Download audio from the video
    print("Downloading audio from YouTube...")
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    audio_file = download_audio_from_youtube(video_url, video_id + ".mp3")

    # Transcribe the audio using Whisper
    print("Transcribing audio...")
    transcription = transcribe_audio(audio_file)

    return transcription

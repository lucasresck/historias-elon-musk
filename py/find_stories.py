import scrapetube
from pathlib import Path
from tqdm.auto import tqdm
from youtube_transcript_api import YouTubeTranscriptApi

def my_print(text, file, end="\n"):
    print(text, end=end)
    print(text, file=file, end=end)

def print_transcription(transcriptions, transcription, i, video_id, file_path):
    f = open(file_path, 'a')
    for j in range(max([i - 3, 0]), min([i + 3, len(transcriptions)])):
        if j == i:
            my_print(">> ", f, end="")
        my_print(transcriptions[j]['text'], f)
    my_print("", f)

    my_print(f"Time: {int(transcription['start']//60):02}:{int(transcription['start']%60):02}", f)
    my_print(f"Duration: {int(transcription['duration'])} seconds", f)
    my_print(f"Link: https://www.youtube.com/watch?v={video_id}&t={int(transcription['start'])}", f)
    my_print("", f)
    my_print("", f)
    f.close()

def check_historia(text):
    """Check if a text is a story.

    Search for keywords in the text in order to determine if it is a story.

    Args:
        text (str): Text to check.

    Returns:
        bool: True if it is a story, False otherwise.
    """
    text = text.lower()

    # It is not possible to simply search for "Elon Musk", "Elon", and "Musk"
    # in a text because automatically generated Portuguese transcriptions
    # usually don't recognize these words.
    strings = ["história", "historia", "choradeira", "joelho", "teve uma vez"]

    for string in strings:
        if string in text:
            return True
    return False

def find_stories_on_video(video_id, data_path="../data/video_transcriptions"):
    """Find Elon Musk miraculous stories on a video.

    Args:
        video_id (str): YouTube video id.
        data_path (str): Path to save the data.
    """
    data_path = Path(data_path)
    data_path.mkdir(parents=True, exist_ok=True)
    file_path = data_path / f"{video_id}.txt"
    if file_path.exists():
        file_path.unlink()

    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
    transcript_list = [transcript for transcript in transcript_list if transcript.language_code == 'pt']
    if len(transcript_list) == 0:
        print(f"No transcript found for video {video_id}")
        return
    assert len(transcript_list) == 1, "More than one transcript found for video"

    transcriptions = transcript_list[0].fetch()
    for i, transcription in enumerate(transcriptions):
        if check_historia(transcription['text']):
            print_transcription(transcriptions, transcription, i, video_id, file_path)

def find_stories_on_channel(channel_url, data_path="../data/video_transcriptions"):
    """Find Elon Musk miraculous stories on a channel.

    Args:
        channel_url (str): YouTube channel url.
        data_path (str): Path to save the data.
    """
    videos = scrapetube.get_channel(channel_url=channel_url)
    video_ids = [video['videoId'] for video in tqdm(videos, desc="Getting channel videos...")]
    for video_id in tqdm(video_ids, desc="Finding stories..."):
        find_stories_on_video(video_id, data_path)

from pathlib import Path
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

    my_print(f"Time: {int(transcription['start']//60)}:{int(transcription['start']%60)}", f)
    my_print(f"Duration: {int(transcription['duration'])} seconds", f)
    my_print(f"Link: https://www.youtube.com/watch?v={video_id}&t={int(transcription['start'])}", f)
    my_print("", f)
    my_print("", f)
    f.close()

def check_historia(text):
    text = text.lower()
    strings = ["história", "historia", "choradeira", "joelho", "teve uma vez"]
    for string in strings:
        if string in text:
            return True

def find_stories_on_video(video_id, data_path="../data/video_transcriptions"):
    """Find Elon Musk miraculous stories on a video.

    Args:
        video_id (str): YouTube video id.
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

from youtube_transcript_api import YouTubeTranscriptApi

def print_transcription(transcriptions, transcription, i, video_id):
    for j in range(max([i - 3, 0]), min([i + 3, len(transcriptions)])):
        if j == i:
            print(">> ", end="")
        print(transcriptions[j]["text"])
    print()

    print(f"Time: {int(transcription['start']//60)}:{int(transcription['start']%60)}")
    print(f"Duration: {int(transcription['duration'])} seconds")
    print(f"Link: https://www.youtube.com/watch?v={video_id}&t={int(transcription['start'])}")
    print()
    print()

def find_stories_on_video(video_id):
    """Find Elon Musk miraculous stories on a video.

    Args:
        video_id (str): YouTube video id.
    """
    transcriptions = YouTubeTranscriptApi.get_transcript(video_id, languages=['pt'])
    for i, transcription in enumerate(transcriptions):
        if "história" in transcription["text"].lower():
            print_transcription(transcriptions, transcription, i, video_id)

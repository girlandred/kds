import cv2
from moviepy.editor import VideoFileClip


def read_audio_from_video(video_path):
    video = cv2.VideoCapture(video_path)

    if not video.isOpened():
        print("Error: Could not open the video file")
        return None

    try:
        clip = VideoFileClip(video_path)
        audio = clip.audio
    except AttributeError:
        print("Error: Video does not contain audio")
        audio = None

    video.release()

    return audio


video_path = '20230610_124605.mp4'
audio = read_audio_from_video(video_path)

if audio:
    audio.write_audiofile('output_audio.mp3', codec='mp3')
else:
    print("No audio found in the video.")

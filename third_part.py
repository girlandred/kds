import cv2
import numpy as np
from pydub import AudioSegment


def overlay_sound(input_video, input_sound, output_video):
    video = cv2.VideoCapture(input_video)
    sound = AudioSegment.from_wav(input_sound)
    fps = int(video.get(cv2.CAP_PROP_FPS))
    out = cv2.VideoWriter(output_video, cv2.VideoWriter_fourcc(*'mp4v'), fps, (int(video.get(3)), int(video.get(4))))

    frame_num = 0

    while True:
        ret, frame = video.read()
        if not ret:
            break

        # Ensure the audio position is within the audio file's duration
        audio_position = int(frame_num * 1000 / fps)
        if audio_position <= len(sound):
            sound_segment = sound[audio_position:audio_position + len(frame) * 1000 // fps]
            combined = cv2.addWeighted(frame, 1, np.zeros(frame.shape, frame.dtype), 0, 0)
            out.write(combined)
        else:
            print("Sound overlay finished with error.")
            break

        frame_num += 1

    video.release()
    out.release()

    print("Sound overlay finished.")


if __name__ == "__main__":
    overlay_sound("output_video_part1.mp4", "custom_audio.wav", "video_with_sound_part1.mp4")

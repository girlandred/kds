import cv2
import sounddevice as sd
import wave


def record_audio(output_file, duration=5, sample_rate=44100):
    print("Recording audio...")
    audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
    sd.wait()

    print("Saving audio to", output_file)
    with wave.open(output_file, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(audio_data.tobytes())

    print("Recording complete.")


def record_video(output_file, audio_file):
    video = cv2.VideoCapture(0)

    if not video.isOpened():
        print("Error: Could not open video capture device")
        return

    frame_width = int(video.get(3))
    frame_height = int(video.get(4))

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    result = cv2.VideoWriter(output_file, fourcc, 20.0, (frame_width, frame_height))

    # Record audio while capturing video
    record_audio(audio_file)

    while True:
        ret, frame = video.read()

        if ret:
            result.write(frame)
            cv2.imshow('Frame', frame)

            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        else:
            break

    video.release()
    result.release()
    cv2.destroyAllWindows()


output_video_file = 'output_video.avi'
output_audio_file = 'output_audio.wav'

record_video(output_video_file, output_audio_file)

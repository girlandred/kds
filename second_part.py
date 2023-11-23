import sounddevice as sd
import wave
import numpy as np


def record_audio(output_file, duration=70, sample_rate=44100):
    print("Recording audio. Speak into the microphone...")
    audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=2, dtype=np.int16)
    sd.wait()
    with wave.open(output_file, 'wb') as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(audio_data.tobytes())
    print(f"Audio recording finished. Saved to {output_file}")


if __name__ == "__main__":
    record_audio("custom_audio.wav", duration=60)

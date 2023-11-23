import subprocess
from pydub import AudioSegment


def add_music(input_sound, input_music, output_sound):
    print(f"Checking file: {input_sound}")

    subprocess.run(['ffmpeg', '-i', input_sound, '-vn', '-acodec', 'pcm_s16le', '-ar', '44100', '-ac', '2', '-f', 'wav', 'extracted_audio.wav'])
    sound = AudioSegment.from_wav('extracted_audio.wav')

    music = AudioSegment.from_file(input_music, format="mp3")
    music_segment = music[:len(sound)]

    combined = sound.overlay(music_segment)
    combined.export(output_sound, format="mp3")

    print("Music addition finished.")


if __name__ == "__main__":
    add_music("custom_audio.wav", "output_audio_1.mp3", "output_audio_with_music.mp3")

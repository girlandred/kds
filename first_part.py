import cv2
from moviepy.audio.fx.all import audio_fadein as afx_fadein, audio_fadeout as afx_fadeout
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.editor import VideoFileClip, concatenate_videoclips, TextClip


def save_video_part(clip, start_time, end_time, output_path):
    part = clip.subclip(start_time, end_time)
    part.write_videofile(output_path)


def main():
    video_path = 'vid.mp4'
    clip = VideoFileClip(video_path)

    # Save video parts
    save_video_part(clip, 0, 60, 'part1.mp4')
    save_video_part(clip, 60, 120, 'part2.mp4')

    # Load video parts
    part1 = VideoFileClip('part1.mp4')
    part2 = VideoFileClip('part2.mp4')

    audio = AudioFileClip('your_audio.wav')

    # Add audio to video parts
    part1 = part1.set_audio(audio)
    part2 = part2.set_audio(audio)

    # Apply fade-in and fade-out to audio
    audio_faded = afx_fadein(audio, 3).fx(afx_fadeout, 3)

    # Concatenate video parts with crossfade
    final_clip = concatenate_videoclips([part1.crossfadeout(3), part2.crossfadein(3)])

    # Set final audio
    final_clip = final_clip.set_audio(audio_faded)

    # Write the final video with crossfade
    final_clip.write_videofile('final_video.mp4', codec='libx264', audio_codec='aac')

    # Create video with music
    video_with_music = part1.set_audio(audio_faded)
    video_with_music.write_videofile('video_with_music.mp4')

    # Save start frame
    start_frame = clip.get_frame(0)
    cv2.imwrite('start_frame.jpg', cv2.cvtColor(start_frame, cv2.COLOR_RGB2BGR))

    # Create end frame with text
    txt_clip = TextClip("The End", fontsize=70, color='white')
    end_frame = txt_clip.set_pos('center').set_duration(clip.duration)
    end_frame.write_videofile('end_frame.mp4', audio=False)


if __name__ == "__main__":
    main()

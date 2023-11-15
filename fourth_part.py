from __future__ import print_function, division
import cv2
import pyaudio
import wave
import threading
import time
import subprocess
import os


# VideoRecorder class for recording video from a camera
class VideoRecorder:
    def __init__(self, name="temp_video.avi", fourcc="MJPG", size_x=640, size_y=480, cam_index=0, fps=30):
        # Initialize video recording parameters
        self.open = True
        self.device_index = cam_index
        self.fps = fps
        self.fourcc = fourcc
        self.frameSize = (size_x, size_y)
        self.video_filename = name
        self.video_cap = cv2.VideoCapture(self.device_index)
        self.video_writer = cv2.VideoWriter_fourcc(*self.fourcc)
        self.video_out = cv2.VideoWriter(self.video_filename, self.video_writer, self.fps, self.frameSize)
        self.frame_counts = 1
        self.start_time = time.time()

    # Method to record video frames
    def record(self):
        while self.open:
            ret, video_frame = self.video_cap.read()
            if ret:
                self.video_out.write(video_frame)
                self.frame_counts += 1
                time.sleep(1 / self.fps)
            else:
                break

    # Method to stop video recording
    def stop(self):
        if self.open:
            self.open = False
            self.video_out.release()
            self.video_cap.release()
            cv2.destroyAllWindows()

    # Method to start video recording in a separate thread
    def start(self):
        video_thread = threading.Thread(target=self.record)
        video_thread.start()


# AudioRecorder class for recording audio from a microphone
class AudioRecorder:
    def __init__(self, filename="temp_audio.wav", rate=44100, fpb=2 ** 12, channels=1, audio_index=0):
        # Initialize audio recording parameters
        self.open = True
        self.rate = rate
        self.frames_per_buffer = fpb
        self.channels = channels
        self.format = pyaudio.paInt16
        self.audio_filename = filename
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=self.format,
                                      channels=self.channels,
                                      rate=self.rate,
                                      input=True,
                                      input_device_index=audio_index,
                                      frames_per_buffer=self.frames_per_buffer)
        self.audio_frames = []

    # Method to record audio frames
    def record(self):
        self.stream.start_stream()
        t_start = time.time_ns()
        while self.open:
            try:
                data = self.stream.read(self.frames_per_buffer)
                self.audio_frames.append(data)
            except Exception as e:
                print('\n' + '*' * 80)
                print('PyAudio read exception at %.1fms\n' % ((time.time_ns() - t_start) / 10 ** 6))
                print(e)
                print('*' * 80 + '\n')
            time.sleep(0.01)
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
        # Save recorded audio to a WAV file
        wave_file = wave.open(self.audio_filename, 'wb')
        wave_file.setnchannels(self.channels)
        wave_file.setsampwidth(self.audio.get_sample_size(self.format))
        wave_file.setframerate(self.rate)
        wave_file.writeframes(b''.join(self.audio_frames))
        wave_file.close()

    # Method to stop audio recording
    def stop(self):
        if self.open:
            self.open = False

    # Method to start audio recording in a separate thread
    def start(self):
        audio_thread = threading.Thread(target=self.record)
        audio_thread.start()


# Function to start audio and video recording
def start_av_recording(filename="test", audio_index=0, sample_rate=44100):
    global video_thread
    global audio_thread
    video_thread = VideoRecorder()
    audio_thread = AudioRecorder(audio_index=audio_index, rate=sample_rate)
    audio_thread.start()
    video_thread.start()
    return filename


# Function to start video recording
def start_video_recording(filename="test"):
    global video_thread
    video_thread = VideoRecorder()
    video_thread.start()
    return filename


# Function to start audio recording
def start_audio_recording(filename, audio_index=0, sample_rate=44100):
    global audio_thread
    audio_thread = AudioRecorder(audio_index=audio_index, rate=sample_rate)
    audio_thread.start()
    return filename


# Function to stop audio and video recording, and perform post-processing
def stop_av_recording(filename):
    audio_thread.stop()
    frame_counts = video_thread.frame_counts
    elapsed_time = time.time() - video_thread.start_time
    recorded_fps = frame_counts / elapsed_time
    print("total frames " + str(frame_counts))
    print("elapsed time " + str(elapsed_time))
    print("recorded fps " + str(recorded_fps))
    video_thread.stop()

    # Wait for all threads to finish
    while threading.active_count() > 1:
        time.sleep(1)

    # Check if re-encoding is required based on recorded fps
    if abs(recorded_fps - 6) >= 0.01:
        print("Re-encoding")
        cmd = "ffmpeg -r " + str(recorded_fps) + " -i temp_video.avi -pix_fmt yuv420p -r 6 temp_video2.avi"
        subprocess.call(cmd, shell=True)
        print("multiplexing")
        cmd = "ffmpeg -y -ac 2 -channel_layout stereo -i temp_audio.wav -i temp_video2.avi -pix_fmt yuv420p " + \
              filename + ".avi"
        subprocess.call(cmd, shell=True)
    else:
        print("Normal recording\nmultiplexing")
        cmd = "ffmpeg -y -ac 2 -channel_layout stereo -i temp_audio.wav -i temp_video.avi -pix_fmt yuv420p " + \
              filename + ".avi"
        subprocess.call(cmd, shell=True)
        print("..")


# Function to clean up temporary files
def file_manager():
    local_path = os.getcwd()
    if os.path.exists(str(local_path) + "/temp_audio.wav"):
        os.remove(str(local_path) + "/temp_audio.wav")
    if os.path.exists(str(local_path) + "/temp_video.avi"):
        os.remove(str(local_path) + "/temp_video.avi")
    if os.path.exists(str(local_path) + "/temp_video2.avi"):
        os.remove(str(local_path) + "/temp_video2.avi")


# Function to list audio devices with optional name filtering
def list_audio_devices(name_filter=None):
    pa = pyaudio.PyAudio()
    device_index = None
    sample_rate = None
    for x in range(pa.get_device_count()):
        info = pa.get_device_info_by_index(x)
        print(pa.get_device_info_by_index(x))
        if name_filter is not None and name_filter in info['name']:
            device_index = info['index']
            sample_rate = int(info['defaultSampleRate'])
            break
    return device_index, sample_rate


if __name__ == '__main__':
    # Example usage: Start recording, wait for 10 seconds, stop recording, and clean up
    start_av_recording()
    time.sleep(10)
    stop_av_recording("test")
    file_manager()

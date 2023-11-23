import cv2
import os


def add_initial_end_frames(input_video, initial_frame_path, end_frame_path, output_video):
    video = cv2.VideoCapture(input_video)
    fps = int(video.get(cv2.CAP_PROP_FPS))
    out = cv2.VideoWriter(output_video, cv2.VideoWriter_fourcc(*'mp4v'), fps, (int(video.get(3)), int(video.get(4))))

    initial_frame = cv2.imread(initial_frame_path)
    end_frame = cv2.imread(end_frame_path)

    for _ in range(int(fps)):
        out.write(initial_frame)

    while True:
        ret, frame = video.read()
        if not ret:
            break
        out.write(frame)

    for _ in range(int(fps)):
        out.write(end_frame)

    video.release()
    out.release()

    print("Initial and end frames addition finished.")


if __name__ == "__main__":
    add_initial_end_frames("video_with_sound.mp4", "initial_frame.png", "end_frame.png", "output_video.mp4")

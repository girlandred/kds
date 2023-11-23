import cv2
import os


def extract_initial_end_frames(input_video, output_directory):
    video = cv2.VideoCapture(input_video)
    fps = int(video.get(cv2.CAP_PROP_FPS))

    os.makedirs(output_directory, exist_ok=True)
    frame_num = 0
    initial_frame, last_frame = None, None

    while True:
        ret, frame = video.read()
        if not ret:
            break

        frame_path = os.path.join(output_directory, f"frame_{frame_num:04d}.png")

        if frame_num == 0:
            initial_frame = frame.copy()

        # Keep updating the last frame with the latest frame
        last_frame = frame.copy()

        # Save each frame as a PNG file
        cv2.imwrite(frame_path, frame)

        frame_num += 1

    video.release()
    print(f"Initial and last frames extracted from {input_video}.")

    return initial_frame, last_frame


if __name__ == "__main__":
    initial_frame, last_frame = extract_initial_end_frames("vid.mp4", "frames_output_folder")

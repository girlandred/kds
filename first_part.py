import cv2


def divide_video(input_video, output_video1, output_video2, duration=60):
    cap = cv2.VideoCapture(input_video)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    start_frame_part1, end_frame_part1 = 0, duration * fps
    start_frame_part2, end_frame_part2 = end_frame_part1, min(total_frames, start_frame_part1 + duration * fps)

    out1 = cv2.VideoWriter(output_video1, cv2.VideoWriter_fourcc(*'mp4v'), fps, (int(cap.get(3)), int(cap.get(4))))
    out2 = cv2.VideoWriter(output_video2, cv2.VideoWriter_fourcc(*'mp4v'), fps, (int(cap.get(3)), int(cap.get(4))))

    for frame_num in range(start_frame_part1, end_frame_part1):
        ret, frame = cap.read()
        if not ret:
            break
        out1.write(frame)

    for frame_num in range(start_frame_part2, end_frame_part2):
        ret, frame = cap.read()
        if not ret:
            break
        out2.write(frame)

    out1.release()
    out2.release()
    cap.release()

    print("Video division finished.")


if __name__ == "__main__":
    divide_video("vid.mp4", "output_video_part1.mp4", "output_video_part2.mp4")

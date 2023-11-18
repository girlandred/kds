import cv2


def record_video(output_file):
    video = cv2.VideoCapture(0)

    if not video.isOpened():
        print("Error: Could not open video capture device")
        return

    frame_width = int(video.get(3))
    frame_height = int(video.get(4))

    fourcc = cv2.VideoWriter_fourcc(*'H264')
    result = cv2.VideoWriter(output_file, fourcc, 20.0, (frame_width, frame_height))

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


record_video('vid.mp4')

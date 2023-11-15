import cv2


def record_video(output_file):
    video = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    if not video.isOpened():
        print("Error")
        return

    fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    result = cv2.VideoWriter(output_file, fourcc, 20.0, (720, 480))

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


record_video('video.mp4')

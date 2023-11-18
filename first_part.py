import cv2
import numpy as np


class ObjectObserver:
    def __init__(self):
        self.background_subtractor = cv2.createBackgroundSubtractorMOG2()
        self.objects = []

    def observe(self, frame):
        fg_mask = self.background_subtractor.apply(frame)

        kernel = np.ones((5, 5), np.uint8)
        fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, kernel)
        fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_CLOSE, kernel)

        contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        self.objects = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            area = cv2.contourArea(contour)

            if area > 500:
                self.objects.append((x, y, x + w, y + h))

        for obj in self.objects:
            cv2.rectangle(frame, (obj[0], obj[1]), (obj[2], obj[3]), (0, 255, 0), 2)

        return frame


if __name__ == "__main__":
    video_capture = cv2.VideoCapture(0)
    observer = ObjectObserver()

    while True:
        ret, frame = video_capture.read()

        if not ret:
            print("Error: Could not read frame")
            break

        observed_frame = observer.observe(frame)

        cv2.imshow('Observer', observed_frame)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()

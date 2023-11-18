import cv2
import numpy as np

video_path = 'vid.mp4'
cap = cv2.VideoCapture(video_path)

# Check if the video is opened successfully
if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

while True:
    # Display menu
    print("Choose an operation:")
    print("1. Convert video to grayscale")
    print("2. Convert video to red palette (RGB)")
    print("3. Basic Image Operations (Blurring)")
    print("4. Image Analysis (Morphology, Contour Detection, Histograms)")
    print("5. Mirror Picture")
    print("6. Rotate Picture")
    print("Press 'q' to exit")

    choice = input("Enter your choice (1/2/3/4/5/6/q): ")

    if choice == '1':
        while True:
            ret, frame = cap.read()

            # Check if frame is read successfully
            if not ret:
                print("Error: Could not read frame from video.")
                break

            # Convert to grayscale
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            cv2.imshow('Gray Video', gray_frame)

            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

    elif choice == '2':
        while True:
            ret, frame = cap.read()

            # Check if frame is read successfully
            if not ret:
                print("Error: Could not read frame from video.")
                break

            # Convert to red palette (RGB)
            red_frame = np.zeros_like(frame)
            red_frame[:, :, 2] = frame[:, :, 2]  # Keep the red channel, set others to zero

            cv2.imshow('Red Video (RGB)', red_frame)

            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

    elif choice == '3':
        while True:
            ret, frame = cap.read()

            # Check if frame is read successfully
            if not ret:
                print("Error: Could not read frame from video.")
                break

            # Check if the frame is empty before applying operations
            if not frame.size:
                print("Error: Empty frame.")
                break

            # Basic Image Operations
            # Blurring
            blurred_frame = cv2.GaussianBlur(frame, (5, 5), 0)

            cv2.imshow('Blurred Video', blurred_frame)

            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

    elif choice == '4':
        while True:
            ret, frame = cap.read()

            # Check if frame is read successfully
            if not ret:
                print("Error: Could not read frame from video.")
                break

            # Check if the frame is empty before applying operations
            if not frame.size:
                print("Error: Empty frame.")
                break

            # Image Analysis
            # Morphology
            kernel = np.ones((5, 5), np.uint8)
            dilated_frame = cv2.dilate(frame, kernel, iterations=1)
            eroded_frame = cv2.erode(frame, kernel, iterations=1)

            # Contour Detection
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(gray_frame, 127, 255, cv2.THRESH_BINARY)
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Check if contours are found before drawing
            if contours:
                cv2.drawContours(frame, contours, -1, (0, 255, 0), 2)

            # Histogram
            histogram = cv2.calcHist([gray_frame], [0], None, [256], [0, 256])
            histogram_frame = np.zeros((256, 256, 3), dtype=np.uint8)
            cv2.normalize(histogram, histogram, 0, 255, cv2.NORM_MINMAX)
            for i in range(1, 256):
                cv2.line(histogram_frame, (i - 1, int(histogram[i - 1][0])), (i, int(histogram[i][0])), (255, 0, 0), 2)

            cv2.imshow('Dilated Video', dilated_frame)
            cv2.imshow('Eroded Video', eroded_frame)
            cv2.imshow('Contours Video', frame)  # Display the original frame with contours
            cv2.imshow('Histogram', histogram_frame)

            if cv2.waitKey(0) & 0xFF == ord('q'):
                break

    elif choice == '5':
        while True:
            ret, frame = cap.read()

            # Check if frame is read successfully
            if not ret:
                print("Error: Could not read frame from video.")
                break

            # Mirror Picture
            mirrored_frame = cv2.flip(frame, 1)  # 1 for horizontal flip, 0 for vertical flip

            cv2.imshow('Mirrored Video', mirrored_frame)

            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

    elif choice == '6':
        while True:
            ret, frame = cap.read()

            # Check if frame is read successfully
            if not ret:
                print("Error: Could not read frame from video.")
                break

            # Rotate Picture
            rotated_frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

            cv2.imshow('Rotated Video', rotated_frame)

            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

    elif choice.lower() == 'q':
        break

# Release resources
cap.release()
cv2.destroyAllWindows()

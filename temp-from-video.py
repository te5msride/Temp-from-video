import cv2
import pytesseract
import csv
import time

# Function for selecting ROI
roi_selected = False
roi_start_point = None
roi_end_point = None


def select_roi(event, x, y, flags, param):
    global roi_selected, roi_start_point, roi_end_point
    if event == cv2.EVENT_LBUTTONDOWN:
        roi_start_point = (x, y)
    elif event == cv2.EVENT_LBUTTONUP:
        # Ensure top-left and bottom-right are correctly ordered
        x1, x2 = sorted([roi_start_point[0], x])
        y1, y2 = sorted([roi_start_point[1], y])
        roi_start_point, roi_end_point = (x1, y1), (x2, y2)

        roi_selected = True
        vis_image = cv2.cvtColor(gray.copy(), cv2.COLOR_GRAY2BGR)
        cv2.rectangle(vis_image, roi_start_point, roi_end_point, (255, 0, 0), 2)
        cv2.imshow("video", vis_image)


# Load the video
video_path = "video.mp4"
cap = cv2.VideoCapture(video_path)

# Check if video opened successfully
if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

# Extract the first frame
ret, frame = cap.read()

if not ret:
    print("Error: Could not read frame from video.")
    cap.release()
    exit()

# Convert the frame to grayscale
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

# Display the frame and select ROI
cv2.namedWindow("video")
cv2.setMouseCallback("video", select_roi)
cv2.imshow("video", gray)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Initialize CSV file
csv_file = "output.csv"
with open(csv_file, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Time", "Temperature"])

# FPS of the video
fps = int(cap.get(cv2.CAP_PROP_FPS))

# Interval for extraction in seconds
interval = 0.5  # change this as required

# Calculate frames to skip
skip_frames = int(fps * interval)

current_time = 0
while ret:
    # Extract number from ROI
    roi = gray[
        roi_start_point[1] : roi_end_point[1], roi_start_point[0] : roi_end_point[0]
    ]
    text = pytesseract.image_to_string(roi, config="--psm 6")
    numbers = [num for num in text.split() if num.replace(".", "").isdigit()]

    # Assuming you're looking for the first number (or change logic accordingly)
    temp = numbers[0] if numbers else "N/A"

    # Write time and temperature to CSV
    with open(csv_file, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([current_time, temp])

    # Skip frames and update current_time
    cap.set(1, cap.get(1) + skip_frames)
    current_time += interval

    # Read the next frame
    ret, frame = cap.read()
    if ret:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

# Release video capture object
cap.release()

print(f"Data written to {csv_file}")

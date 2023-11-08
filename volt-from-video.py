import cv2
import pytesseract
import csv
import time
import os
from PIL import Image
import re

# Function for selecting ROI
roi_selected = False
roi_start_point = None
roi_end_point = None

# Create a directory to save the frames
output_dir = 'frames'
os.makedirs(output_dir, exist_ok=True)

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
# video_path = "HeatCameraText.mp4"
video_path = "volt_test.mp4"
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
# half resolution
#scale_percent = 90
scale_percent = 50
width = int(gray.shape[1] * scale_percent / 100)
height = int(gray.shape[0] * scale_percent / 100)
dim = (width, height)
gray = cv2.resize(gray, dim, interpolation=cv2.INTER_AREA)

# border_width = 100  # Adjust as needed
# border_color = (0, 0, 0)  # Black color
# gray = cv2.copyMakeBorder(gray, border_width, border_width, border_width, border_width, cv2.BORDER_CONSTANT, value=border_color)


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
#fps = int(cap.get(cv2.CAP_PROP_FPS))
fps = 30 

# Interval for extraction in seconds
interval = 2  # change this as required

# Calculate frames to skip
skip_frames = int(fps * interval)

current_time = 0
previous_number = 0 
number = 0 

while ret:
    # Extract number from ROI

    #roi = gray 
    roi = gray[
        roi_start_point[1] : roi_end_point[1], roi_start_point[0] : roi_end_point[0]
    ]
    # thr = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
    #                         cv2.THRESH_BINARY, 21, 23)

    # resize
    #roi = cv2.resize(roi, dim, interpolation=cv2.INTER_AREA)
    border_width = 100  # Adjust as needed
    border_color = (0, 0, 0)  # Black color
    roi = cv2.copyMakeBorder(roi, border_width, border_width, border_width, border_width, cv2.BORDER_CONSTANT, value=border_color)


    # threshold
    #ret, roi = cv2.threshold(roi, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # smoothing
    #roi = cv2.medianBlur(roi, 3)

    # show for debugging
    cv2.imshow("roi", roi)
    frame_filename = os.path.join(output_dir, 'f.jpg')
    cv2.imwrite(frame_filename, roi)
    cv2.waitKey(1)

    text = pytesseract.image_to_string(roi, config="--psm 6")
    numbers = re.findall(r'\d+\.\d+|\d+', text)

    # numbers = [num for num in text.split() if num.replace(".", "").isinteger()]

    # Assuming you're looking for the first number (or change logic accordingly)
    # temp = numbers[0] if numbers else "N/A"
    if(numbers):
        number = float(numbers[1]) if len(numbers) > 1 else float(numbers[0])
        
    print(previous_number)
    print(number)
    print(type(number))
    print(type(previous_number))
    # Write time and temperature to CSV
    with open(csv_file, "a", newline="") as file:
        writer = csv.writer(file)
        if abs(number - previous_number) < 50: 
            writer.writerow([current_time, number])
            previous_number = number
            
            # if (previous_number):
            #     previous_number = previous_number[0]

    # Skip frames and update current_time
    cap.set(1, cap.get(1) + skip_frames)
    current_time += interval

    # Read the next frame
    ret, frame = cap.read()
    if ret:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.resize(gray, dim, interpolation=cv2.INTER_AREA)

# Release video capture object
cap.release()

print(f"Data written to {csv_file}")

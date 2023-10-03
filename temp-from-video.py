import cv2
import pytesseract
import csv
from datetime import datetime

# Path to tesseract executable (modify if necessary)
pytesseract.pytesseract.tesseract_cmd = r"/usr/bin/tesseract"


def extract_temperatures(frame):
    # Convert frame to grayscale for better OCR accuracy
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Extract text from frame
    text = pytesseract.image_to_string(gray)

    # Extract temperature values from text (assuming they're in a recognizable format e.g., "23.4°C")
    temps = [t.replace("°C", "").strip() for t in text.split() if "°C" in t]

    return temps


def main():
    # Open the video
    cap = cv2.VideoCapture("path_to_your_video.mp4")

    # Open a CSV file for writing
    with open("temperature_data.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Time", "Temperature1", "Temperature2", "Temperature3"])

        while cap.isOpened():
            ret, frame = cap.read()

            if not ret:
                break

            temperatures = extract_temperatures(frame)

            if len(temperatures) == 3:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                writer.writerow([timestamp] + temperatures)

    cap.release()


if __name__ == "__main__":
    main()

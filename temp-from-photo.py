import cv2
import pytesseract

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
        cv2.imshow("image", vis_image)


# Load the image
image_path = "frames/f.jpg"
image = cv2.imread(image_path)

if image is None:
    #print(f"Failed to load image: {image_path}")
    exit()

# Scale image 50%
scale_percent = 50
width = int(image.shape[1] * scale_percent / 100)
height = int(image.shape[0] * scale_percent / 100)
dim = (width, height)
image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Display the image and select ROI
cv2.namedWindow("image")
cv2.setMouseCallback("image", select_roi)
cv2.imshow("image", gray)
cv2.waitKey(0)

# Check if ROI has been selected
if roi_selected:
    roi = gray[
        roi_start_point[1] : roi_end_point[1], roi_start_point[0] : roi_end_point[0]
    ]
else:
    print("ROI not selected!")
    roi = gray

# Expected number
expected_number = "29.3"

# Use pytesseract to extract text
text = pytesseract.image_to_string(roi, config="--psm 6")
print(text)

# Split the text into individual numbers
numbers = [num for num in text.split() if num.replace(".", "").isdigit()]

if expected_number in numbers:
    print("Found the number {expected_number}!")
else:
    print ("Did not find the number {expected_number}.")

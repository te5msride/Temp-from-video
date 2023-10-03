import cv2
import pytesseract

# Load the image
image = cv2.imread("image.png")

# scale image 50%
scale_percent = 50
width = int(image.shape[1] * scale_percent / 100)
height = int(image.shape[0] * scale_percent / 100)
dim = (width, height)
image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Expected numbers
expected_numbers = ["29.3", "32.8", "24.5"]

# Experiment with kernel sizes, shapes, and iterations
shapes = [cv2.MORPH_RECT, cv2.MORPH_ELLIPSE, cv2.MORPH_CROSS]
found_optimal = False

for shape in shapes:
    for width in range(2, 6):  # Adjust as needed
        for iterations in range(1, 4):  # Adjust as needed
            kernel = cv2.getStructuringElement(shape, (width, 2))
            dilated = cv2.dilate(gray, kernel, iterations=iterations)

            # Threshold the image
            _, threshed = cv2.threshold(
                dilated, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
            )

            # Use pytesseract to extract text
            text = pytesseract.image_to_string(threshed, config="--psm 6")

            # Split the text into individual numbers
            numbers = [num for num in text.split() if num.replace(".", "").isdigit()]

            print(
                f"Shape: {shape}, Width: {width}, Iterations: {iterations}, Numbers: {numbers}"
            )

            # Check if at least 2 out of 3 extracted numbers match the expected numbers
            common_numbers = set(numbers).intersection(set(expected_numbers))
            if len(common_numbers) >= 2:
                print("Found optimal (or near-optimal) settings!")
                found_optimal = True
                break

        if found_optimal:
            break

    if found_optimal:
        break
# show optimal thresholded image
cv2.imshow("threshed", threshed)
cv2.waitKey(0)

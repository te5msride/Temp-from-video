import cv2
import pytesseract

# Open the video file
cap = cv2.VideoCapture('volt_test.mp4')
cap.set(cv2.CAP_PROP_POS_FRAMES, 70)

while cap.isOpened():
    
    ret, frame = cap.read()
    if not ret:
        break  # Break the loop at the end of the video

    cv2.imshow("frame", frame)
<<<<<<< Updated upstream
    cv2.waitKey(int(3000 / 30))
    # Process the frame with Tesseract
    text = pytesseract.image_to_string(frame, config="--psm 6")
=======
    cv2.waitKey(100)
    # Process the frame with Tesseract
    text = pytesseract.image_to_string(frame, config="--psm 6")
    #--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789.
>>>>>>> Stashed changes

    # Do something with the extracted text
    print("extracted: ")
    print(text)

cap.release()
cv2.destroyAllWindows()
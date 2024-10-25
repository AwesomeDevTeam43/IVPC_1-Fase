import cv2
import numpy as np

# OpenCV settings for color segmentation
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Check if the webcam is opened correctly
if not cap.isOpened():
    print("Failed to open the webcam.")
    exit()

# Define color ranges
lower_red = np.array([170, 100, 100])  # Lower bound for red
upper_red = np.array([180, 255, 255])  # Upper bound for red
lower_blue = np.array([100, 150, 0])  # Lower bound for blue
upper_blue = np.array([140, 255, 255])  # Upper bound for blue


def cv_update():
    if cap is None or not cap.isOpened():
        print("Webcam is not initialized or failed to open.")
        return

    ret, frame = cap.read()
    if not ret or frame is None:
        print("Failed to capture the image.")
        return

    # Convert to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # Create masks for red and blue
    mask_red = cv2.inRange(hsv, lower_red, upper_red)
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)

    # Combine the masks
    mask_combined = cv2.bitwise_or(mask_red, mask_blue)

    # Apply the mask to get the segmented result
    result = cv2.bitwise_and(frame, frame, mask=mask_combined)

    # Find contours
    contours_red, _ = cv2.findContours(mask_red, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours_blue, _ = cv2.findContours(mask_blue, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Minimum area for contours
    min_area = 1000  # Adjust as necessary

    red_y_coords = []  # List to store y-coordinates of detected red areas
    blue_y_coords = []  # List to store y-coordinates of detected blue areas

    # Process red contours
    if contours_red:
        large_contours_red = [contour for contour in contours_red if cv2.contourArea(contour) > min_area]
        for contour in large_contours_red:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Draw rectangle around detected red area
            red_y_coords.append(y)  # Store the y-coordinate
            print(f"Detected red at y: {y}")  # Print the detected position

    # Process blue contours
    if contours_blue:
        large_contours_blue = [contour for contour in contours_blue if cv2.contourArea(contour) > min_area]
        for contour in large_contours_blue:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Draw rectangle around detected blue area
            blue_y_coords.append(y)  # Store the y-coordinate
            print(f"Detected blue at y: {y}")  # Print the detected position

    # Display the original image and the masks
    cv2.imshow("Original Frame", frame)
    cv2.imshow("Red Mask", mask_red)
    cv2.imshow("Blue Mask", mask_blue)
    cv2.imshow("Combined Mask", mask_combined)
    cv2.imshow("Segmented Result", result)

    # Handle the exit condition
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv_cleanup()

def cv_cleanup():
    global cap
    if cap is not None and cap.isOpened():
        cap.release()
    cv2.destroyAllWindows()


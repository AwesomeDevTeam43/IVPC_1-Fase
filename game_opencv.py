import cv2
import numpy as np

cap = None  # Variável global para captura de vídeo

def cv_setup():
    # Configurações do OpenCV para segmentação de cores
    cap = cv2.VideoCapture(0)  # Abre a webcam

    # Define color ranges
    lower_red = np.array([170, 100, 100]) # Lower bound for red
    upper_red = np.array([180, 255, 255])  # Upper bound for red
    lower_blue = np.array([100, 150, 0])  # Lower bound for blue
    upper_blue = np.array([140, 255, 255])  # Upper bound for blue

def cv_update():
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Falha ao capturar a imagem.")
            break

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # Convert to HSV
        mask_red = cv2.inRange(hsv, lower_red, upper_red)  # Create mask for red
        mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)  # Create mask for blue

        # Combine masks
        mask_combined = cv2.bitwise_or(mask_red, mask_blue)

        result = cv2.bitwise_and(frame, frame, mask=mask_combined)

        # Encontrar contornos
        contours_red, _ = cv2.findContours(mask_red, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours_blue, _ = cv2.findContours(mask_blue, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Definir uma área mínima para os contornos
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

        # Exibir a imagem original e a máscara
        cv2.imshow("Original Frame", frame)
        cv2.imshow("Red Mask", mask_red)
        cv2.imshow("Blue Mask", mask_blue)
        cv2.imshow("Combined Mask", mask_combined)
        cv2.imshow("Segmented Result", result)

        # Pressione 'q' para sair do loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Liberar a captura e fechar janelas
    cap.release()
    cv2.destroyAllWindows()

    # Return the y-coordinates after closing the camera
    return red_y_coords, blue_y_coords

# Chame a função de configuração
red_y, blue_y = cv_setup()
print("Final Red Y Coordinates:", red_y)
print("Final Blue Y Coordinates:", blue_y)

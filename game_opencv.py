import cv2
import numpy as np

def cv_setup():
    # Configurações do OpenCV para segmentação de cores
    cap = cv2.VideoCapture(0)  # Abre a webcam
    # Intervalo para tons de pele
    lower_skin = np.array([0, 20, 70])  # Limite inferior para tons de pele
    upper_skin = np.array([20, 255, 255])  # Limite superior para tons de pele

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Falha ao capturar a imagem.")
            break

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        # Converter para o espaço de cores HSV

        # Criar a máscara para detectar a cor de pele
        mask = cv2.inRange(hsv, lower_skin, upper_skin)

        # Encontrar contornos
        #contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Definir uma área mínima para os contornos
        min_area = 1000  # Ajusta este valor conforme necessário

        #if contours:
            # Filtrar contornos com base na área
         #   large_contours = [contour for contour in contours if cv2.contourArea(contour) > min_area]

          #  if large_contours:
          #      # Obter o maior contorno dos grandes
          #      largest_contour = max(large_contours, key=cv2.contourArea)
          #      x, y, w, h = cv2.boundingRect(largest_contour)
           #     cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Desenhar retângulo ao redor do maior contorno
          #      print(f"Detected at y: {y}")  # Print the detected position

        # Exibir a imagem original e a máscara
        cv2.imshow("Original Frame", frame)
        cv2.imshow("Skin Mask", mask)

        # Pressione 'q' para sair do loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Liberar a captura e fechar janelas
    cap.release()
    cv2.destroyAllWindows()

# Chame a função de configuração
cv_setup()

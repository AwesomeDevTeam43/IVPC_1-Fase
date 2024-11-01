import cv2
import numpy as np
from cv2 import resizeWindow

# Inicialização da câmara
cap = cv2.VideoCapture(0)

# Verifica se a câmara foi aberta corretamente
if not cap.isOpened():
    print("Erro ao abrir a câmara.")
    exit()

# Função para atualizar as *trackbars*
def nothing(x):
    pass

# Criação de *trackbars* na janela "Configurações" para ajuste das cores azul e verde
cv2.namedWindow("Settings", cv2.WINDOW_GUI_EXPANDED)

# Trackbars para o objeto azul
cv2.createTrackbar("Azul H Min", "Settings", 90, 179, nothing)
cv2.createTrackbar("Azul H Max", "Settings", 130, 179, nothing)
cv2.createTrackbar("Azul S Min", "Settings", 50, 255, nothing)
cv2.createTrackbar("Azul S Max", "Settings", 255, 255, nothing)
cv2.createTrackbar("Azul V Min", "Settings", 50, 255, nothing)
cv2.createTrackbar("Azul V Max", "Settings", 255, 255, nothing)

# Trackbars para o objeto verde
cv2.createTrackbar("Verde H Min", "Settings", 35, 179, nothing)
cv2.createTrackbar("Verde H Max", "Settings", 85, 179, nothing)
cv2.createTrackbar("Verde S Min", "Settings", 50, 255, nothing)
cv2.createTrackbar("Verde S Max", "Settings", 255, 255, nothing)
cv2.createTrackbar("Verde V Min", "Settings", 50, 255, nothing)
cv2.createTrackbar("Verde V Max", "Settings", 255, 255, nothing)

green_y_coords = []
blue_y_coords = []

#def calcbndrec(height, y):
#    my = height / 2
#    hf = 480
#    hi = hf - height

#    coord = (y + my) * (hf / hi) - 60
#    return coord

def calcbndrec(h, y):
    s_height = 480   # Altura total da janela (ou altura do quadro)
    p_height = 50    # Altura do paddle
    hj_height = 480  # Altura do jogo
    hc_height = 480  # Altura da câmera

    # Calcula a nova posição do canto superior esquerdo
    coord = (y) * (hj_height - p_height) / (hc_height - h)
    # Limita a coordenada para que o paddle não ultrapasse os limites da janela
    coord = max(0, min(coord, s_height - p_height))
    return coord

# Função principal de processamento de vídeo
def cv_update():
    global cap, green_y_coords, blue_y_coords

    min_area = 1000  # Área mínima para contornos
    ret, frame = cap.read()
    if not ret or frame is None:
        print("Erro ao capturar a imagem.")
        return
    print(frame.shape)

    # Conversão do quadro para HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Obtenção dos valores das *trackbars* para a cor azul
    blue_h_min = cv2.getTrackbarPos("Azul H Min", "Settings")
    blue_h_max = cv2.getTrackbarPos("Azul H Max", "Settings")
    blue_s_min = cv2.getTrackbarPos("Azul S Min", "Settings")
    blue_s_max = cv2.getTrackbarPos("Azul S Max", "Settings")
    blue_v_min = cv2.getTrackbarPos("Azul V Min", "Settings")
    blue_v_max = cv2.getTrackbarPos("Azul V Max", "Settings")

    # Criação dos limites para o azul
    lower_blue = np.array([blue_h_min, blue_s_min, blue_v_min])
    upper_blue = np.array([blue_h_max, blue_s_max, blue_v_max])

    # Obtenção dos valores das *trackbars* para a cor verde
    green_h_min = cv2.getTrackbarPos("Verde H Min", "Settings")
    green_h_max = cv2.getTrackbarPos("Verde H Max", "Settings")
    green_s_min = cv2.getTrackbarPos("Verde S Min", "Settings")
    green_s_max = cv2.getTrackbarPos("Verde S Max", "Settings")
    green_v_min = cv2.getTrackbarPos("Verde V Min", "Settings")
    green_v_max = cv2.getTrackbarPos("Verde V Max", "Settings")

    # Criação dos limites para o verde
    lower_green = np.array([green_h_min, green_s_min, green_v_min])
    upper_green = np.array([green_h_max, green_s_max, green_v_max])

    # Criação das máscaras para azul e verde
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
    mask_green = cv2.inRange(hsv, lower_green, upper_green)

    # Combinação das máscaras
    mask_combined = cv2.bitwise_or(mask_blue, mask_green)

    # Aplicação da máscara para obter o resultado segmentado
    result = cv2.bitwise_and(frame, frame, mask=mask_combined)

    # Encontrar contornos para azul
    contours_blue, _ = cv2.findContours(mask_blue, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    blue_y_coords = []

    if contours_blue:
        large_contours_blue = [contour for contour in contours_blue if cv2.contourArea(contour) > min_area]
        for contour in large_contours_blue:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)  # Retângulo azul
            if h > 0:  # Garante que h não seja zero
                blue_y_coords = calcbndrec(h, y)
                print(f"Detectado azul em y: {blue_y_coords}")

    # Encontrar contornos para verde (igual lógica)
    contours_green, _ = cv2.findContours(mask_green, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    green_y_coords = []

    if contours_green:
        large_contours_green = [contour for contour in contours_green if cv2.contourArea(contour) > min_area]
        for contour in large_contours_green:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Retângulo verde
            if h > 0:  # Garante que h não seja zero
                green_y_coords = calcbndrec(h, y)
                print(f"Detectado verde em y: {green_y_coords}")

    # Exibir o frame original e os resultados da segmentação
    cv2.imshow("Camara", frame)
    cv2.imshow("Mascara Azul", mask_blue)
    cv2.imshow("Mascara Verde", mask_green)
    cv2.imshow("Mascara Combinada", mask_combined)
    cv2.imshow("Resultado Segmentado", result)

    # Pressionar 'q' para sair
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv_cleanup()

# Função para fechar a câmara e encerrar as janelas
def cv_cleanup():
    global cap
    if cap is not None and cap.isOpened():
        cap.release()
    cv2.destroyAllWindows()

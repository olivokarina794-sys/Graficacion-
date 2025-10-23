import cv2
import mediapipe as mp
import numpy as np

# Inicializar MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7, max_num_hands=2)

# Variables 
punto_inicio = None
punto_final = None
dibujando = False

# función para determinar la letra según la posición de los dedos
def reconocer_letra(hand_landmarks, frame):
    # Obtener coordenadas de los puntos clave de la mano
    dedos = [hand_landmarks.landmark[i] for i in range(21)]
    
    
    pulgar = dedos[4]   # Punta del pulgar
    indice = dedos[8]   # Punta del índice
    medio = dedos[12]   # Punta del medio
    anular = dedos[16]  # Punta del anular
    meñique = dedos[20] # Punta del meñique

    # Distancias entre puntos 
    distancia_pulgar_indice = np.linalg.norm([pulgar.x - indice.x, pulgar.y - indice.y])
    distancia_indice_medio = np.linalg.norm([indice.x - medio.x, indice.y - medio.y])
    

    if distancia_pulgar_indice < 0.05 and distancia_indice_medio > 0.1:
        return "A"  # Seña de la letra A (puño cerrado con pulgar al lado)
    elif indice.y < medio.y and medio.y < anular.y and anular.y < meñique.y:
        return "B"  # Seña de la letra B (todos los dedos estirados, pulgar en la palma)
    elif distancia_pulgar_indice > 0.1 and distancia_indice_medio > 0.1:
        return "C"  # Seña de la letra C (mano en forma de "C")
    
    return "Desconocido"

# Función para obtener las coordenadas de los dedos índices
def obtener_indices(results, frame_shape):
    indices = []
    
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Obtener la punta del dedo índice (landmark 8)
            dedo_indice = hand_landmarks.landmark[8]
            
            # Convertir coordenadas normalizadas a píxeles
            h, w, _ = frame_shape
            x = int(dedo_indice.x * w)
            y = int(dedo_indice.y * h)
            
            indices.append((x, y))
    
    return indices

# Captura de video en tiempo real
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Crear una copia del frame para dibujar el rectángulo
    frame_con_rectangulo = frame.copy()

    # Convertir a RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Procesar la imagen con MediaPipe
    results = hands.process(frame_rgb)

    # Obtener posiciones de los dedos índices
    indices = obtener_indices(results, frame.shape)
    
    # Dibujar puntos de la mano y reconocer letras
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame_con_rectangulo, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            # Identificar la letra
            letra_detectada = reconocer_letra(hand_landmarks, frame)

            # Mostrar la letra en pantalla
            cv2.putText(frame_con_rectangulo, f"Letra: {letra_detectada}", (50, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    # Dibujar rectángulo si hay dos dedos índices detectados
    if len(indices) == 2:
        # Dibujar círculos en los dedos índices
        for punto in indices:
            cv2.circle(frame_con_rectangulo, punto, 10, (255, 0, 0), -1)
        
        # Dibujar línea entre los dedos índices
        cv2.line(frame_con_rectangulo, indices[0], indices[1], (0, 255, 255), 2)
        
        # Calcular el rectángulo
        x1, y1 = indices[0]
        x2, y2 = indices[1]
        
        # Asegurar que las coordenadas sean correctas para el rectángulo
        x_min = min(x1, x2)
        y_min = min(y1, y2)
        x_max = max(x1, x2)
        y_max = max(y1, y2)
        
        # Dibujar el rectángulo
        cv2.rectangle(frame_con_rectangulo, (x_min, y_min), (x_max, y_max), (0, 0, 255), 2)
        
        # Mostrar información del rectángulo
        cv2.putText(frame_con_rectangulo, f"Rectangulo: ({x_min},{y_min})-({x_max},{y_max})", 
                    (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2, cv2.LINE_AA)

    # Mostrar el video
    cv2.imshow("Reconocimiento de Letras con Rectangulo", frame_con_rectangulo)

    # Salir con la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar recursos
cap.release()
cv2.destroyAllWindows()
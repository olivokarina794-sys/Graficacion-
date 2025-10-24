import cv2
import mediapipe as mp
import numpy as np

# Inicializar MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=2, 
                                  min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Captura de video
cap = cv2.VideoCapture(0)

# Puntos específicos para emociones
puntos_seleccionados = [33, 133, 362, 263, 61, 291, 4, 36, 0, 13, 14, 78, 308]  # Ojos, boca y nariz

def distancia(p1, p2):
    """Calcula la distancia euclidiana entre dos puntos."""
    return np.linalg.norm(np.array(p1) - np.array(p2))

def detectar_emocion_simple(puntos):
    """Detecta emociones basadas en distancias faciales simples"""
    
    # Distancia entre esquinas de la boca (sonrisa)
    if 78 in puntos and 308 in puntos:
        ancho_boca = distancia(puntos[78], puntos[308])
    else:
        ancho_boca = 0
    
    # Apertura de boca
    if 13 in puntos and 14 in puntos:
        apertura_boca = distancia(puntos[13], puntos[14])
    else:
        apertura_boca = 0
    
    # Distancia entre ojos (para cejas)
    if 33 in puntos and 133 in puntos:
        distancia_ojos = distancia(puntos[33], puntos[133])
    else:
        distancia_ojos = 0
    
    # Detectar emoción basada en patrones simples
    if ancho_boca > 60 and apertura_boca < 15:  # Boca ancha pero no abierta
        return "😊 FELIZ - Sonriendo"
    elif apertura_boca > 20:  # Boca muy abierta
        return "😮 SORPRENDIDO/A"
    elif ancho_boca < 45 and apertura_boca < 10:  # Boca cerrada y estrecha
        return "😠 ENOJADO/A"
    elif distancia_ojos > 100:  # Ojos muy separados (sorpresa)
        return "😲 ASOMBRADO/A"
    else:
        return "😐 NEUTRO"

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)  # Espejo para mayor naturalidad
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)

    emocion = "🤔 Detectando..."

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            puntos = {}
            
            for idx in puntos_seleccionados:
                x = int(face_landmarks.landmark[idx].x * frame.shape[1])
                y = int(face_landmarks.landmark[idx].y * frame.shape[0])
                puntos[idx] = (x, y)
                cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)  # Dibuja el punto en verde
            
            # Detectar emoción
            emocion = detectar_emocion_simple(puntos)
            
            # Mostrar coordenadas del punto 61 (como en tu código original)
            if 61 in puntos:
                cv2.putText(frame, f" {int(puntos[61][0]-20), int(puntos[61][1]-20) }", 
                           (puntos[61][0], puntos[61][1] - 10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    # Mostrar emoción en pantalla
    cv2.putText(frame, emocion, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    
    cv2.imshow('Deteccion de Emociones', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
import cv2
import mediapipe as mp
import numpy as np

# Inicializar MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Variables para la calculadora
numero_seleccionado = 0
operacion_seleccionada = None
primer_numero = 0
resultado = 0

# Configuración de la malla de números
filas, columnas = 3, 3
numeros_malla = [
    [1, 2, 3],
    [4, 5, 6], 
    [7, 8, 9]
]

# Configuración de operaciones - CORREGIDO: usar '*' en lugar de '×'
operaciones = ['+', '-', '*', 'C', '=']

def dibujar_malla_numeros(frame):
    h, w, _ = frame.shape
    
    # Panel principal ultra compacto
    panel_x, panel_y = 20, 60
    ancho_panel, alto_panel = 180, 180  # Más pequeño
    
    # Fondo del panel
    cv2.rectangle(frame, (panel_x, panel_y), (panel_x + ancho_panel, panel_y + alto_panel), (40, 40, 40), -1)
    cv2.rectangle(frame, (panel_x, panel_y), (panel_x + ancho_panel, panel_y + alto_panel), (200, 200, 200), 1)
    
    # Dibujar malla de números
    celda_ancho = ancho_panel // columnas
    celda_alto = alto_panel // filas
    
    for fila in range(filas):
        for columna in range(columnas):
            x1 = panel_x + columna * celda_ancho
            y1 = panel_y + fila * celda_alto
            x2 = x1 + celda_ancho
            y2 = y1 + celda_alto
            
            numero = numeros_malla[fila][columna]
            
            # Color de la celda
            color_celda = (60, 60, 60) if numero != numero_seleccionado else (0, 80, 160)
            
            # Dibujar celda
            cv2.rectangle(frame, (x1, y1), (x2, y2), color_celda, -1)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (200, 200, 200), 1)
            
            # Dibujar número (más pequeño)
            texto = str(numero)
            cv2.putText(frame, texto, (x1 + 20, y1 + 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
    
    return panel_x, panel_y, celda_ancho, celda_alto

def dibujar_panel_operaciones(frame):
    h, w, _ = frame.shape
    
    # Panel de operaciones ultra compacto
    panel_x, panel_y = 210, 60
    ancho_panel, alto_panel = 80, 180
    
    # Fondo del panel
    cv2.rectangle(frame, (panel_x, panel_y), (panel_x + ancho_panel, panel_y + alto_panel), (40, 40, 40), -1)
    cv2.rectangle(frame, (panel_x, panel_y), (panel_x + ancho_panel, panel_y + alto_panel), (200, 200, 200), 1)
    
    # Dibujar botones de operaciones
    celda_alto = alto_panel // len(operaciones)
    
    for i, operacion in enumerate(operaciones):
        y1 = panel_y + i * celda_alto
        y2 = y1 + celda_alto
        x1 = panel_x
        x2 = panel_x + ancho_panel
        
        # Color del botón
        if operacion == operacion_seleccionada:
            color_boton = (0, 120, 0)  # Verde seleccionado
        elif operacion == 'C':
            color_boton = (0, 0, 120)  # Rojo Clear
        elif operacion == '=':
            color_boton = (120, 120, 0)  # Amarillo igual
        else:
            color_boton = (70, 70, 70)  # Gris normal
        
        # Dibujar botón
        cv2.rectangle(frame, (x1, y1), (x2, y2), color_boton, -1)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (200, 200, 200), 1)
        
        # Dibujar texto de operación (más pequeño)
        texto_x = x1 + 25
        texto_y = y1 + 25
        
        cv2.putText(frame, operacion, (texto_x, texto_y), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
    
    return panel_x, panel_y, ancho_panel, celda_alto

def dibujar_display(frame):
    h, w, _ = frame.shape
    
    # Display superior ultra compacto
    display_x, display_y = 20, 30
    ancho_display, alto_display = 270, 25
    
    # Fondo del display
    cv2.rectangle(frame, (display_x, display_y), (display_x + ancho_display, display_y + alto_display), (0, 0, 0), -1)
    cv2.rectangle(frame, (display_x, display_y), (display_x + ancho_display, display_y + alto_display), (255, 255, 255), 1)
    
    # Texto del display (más pequeño)
    if operacion_seleccionada:
        texto_display = f"{primer_numero} {operacion_seleccionada} {numero_seleccionado if numero_seleccionado else ''}"
    else:
        texto_display = f"{numero_seleccionado}" if numero_seleccionado else "0"
    
    if resultado != 0:
        texto_display += f" = {resultado}"
    
    cv2.putText(frame, texto_display, (display_x + 5, display_y + 17), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

def detectar_seleccion(dedo_x, dedo_y, panel_x, panel_y, celda_ancho, celda_alto, op_panel_x, op_panel_y, op_ancho, op_celda_alto):
    global numero_seleccionado, operacion_seleccionada, primer_numero, resultado
    
    # Verificar selección en malla de números
    for fila in range(filas):
        for columna in range(columnas):
            x1 = panel_x + columna * celda_ancho
            y1 = panel_y + fila * celda_alto
            x2 = x1 + celda_ancho
            y2 = y1 + celda_alto
            
            if x1 <= dedo_x <= x2 and y1 <= dedo_y <= y2:
                numero_seleccionado = numeros_malla[fila][columna]
                return
    
    # Verificar selección en operaciones
    for i, operacion in enumerate(operaciones):
        y1 = op_panel_y + i * op_celda_alto
        y2 = y1 + op_celda_alto
        x1 = op_panel_x
        x2 = op_panel_x + op_ancho
        
        if x1 <= dedo_x <= x2 and y1 <= dedo_y <= y2:
            if operacion == 'C':  # Clear
                numero_seleccionado = 0
                operacion_seleccionada = None
                primer_numero = 0
                resultado = 0
            elif operacion == '=' and operacion_seleccionada and primer_numero != 0 and numero_seleccionado != 0:
                # Calcular resultado - CORREGIDO: usar '*'
                if operacion_seleccionada == '+':
                    resultado = primer_numero + numero_seleccionado
                elif operacion_seleccionada == '-':
                    resultado = primer_numero - numero_seleccionado
                elif operacion_seleccionada == '*':  # CORREGIDO
                    resultado = primer_numero * numero_seleccionado
                
                numero_seleccionado = resultado
                primer_numero = 0
                operacion_seleccionada = None
            elif operacion in ['+', '-', '*']:  # CORREGIDO
                if numero_seleccionado != 0:
                    primer_numero = numero_seleccionado
                    operacion_seleccionada = operacion
                    numero_seleccionado = 0

def obtener_posicion_dedo_index(hand_landmarks, frame):
    h, w, _ = frame.shape
    landmarks = hand_landmarks.landmark
    
    # Obtener posición del dedo índice (landmark 8)
    dedo_x = int(landmarks[8].x * w)
    dedo_y = int(landmarks[8].y * h)
    
    return dedo_x, dedo_y

# Captura de video
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Voltear frame horizontalmente para efecto espejo
    frame = cv2.flip(frame, 1)
    
    # Convertir a RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Procesar con MediaPipe
    results = hands.process(frame_rgb)
    
    # Dibujar interfaz ultra compacta
    panel_x, panel_y, celda_ancho, celda_alto = dibujar_malla_numeros(frame)
    op_panel_x, op_panel_y, op_ancho, op_celda_alto = dibujar_panel_operaciones(frame)
    dibujar_display(frame)
    
    # Detectar manos y selección
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            # Obtener posición del dedo índice
            dedo_x, dedo_y = obtener_posicion_dedo_index(hand_landmarks, frame)
            
            # Dibujar círculo en el dedo índice (pequeño)
            cv2.circle(frame, (dedo_x, dedo_y), 6, (0, 255, 0), -1)
            
            # Detectar selección
            detectar_seleccion(dedo_x, dedo_y, panel_x, panel_y, celda_ancho, celda_alto, 
                             op_panel_x, op_panel_y, op_ancho, op_celda_alto)
    
    # Instrucciones pequeñas
    cv2.putText(frame, "Toca con el dedo indice", (20, 250), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 0), 1)

    # Mostrar el video
    cv2.imshow("Calculadora Mini", frame)

    # Salir con 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar recursos
cap.release()
cv2.destroyAllWindows()
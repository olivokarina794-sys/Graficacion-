import cv2 as cv
import numpy as np

cap = cv.VideoCapture(0)

# Crear una imagen en negro para dibujar la trayectoria
trayectoria = None

# Guardamos el último centro detectado
ultimo_centro = None

while True:
    ret, img = cap.read()
    if not ret:
        break

    if trayectoria is None:
        trayectoria = np.zeros_like(img)

    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

    # Rango de color a detectar (ajústalo según el objeto)
    uba = (90, 255, 255)   # HSV alto
    ubb = (40, 40, 40)     # HSV bajo

    mask = cv.inRange(hsv, ubb, uba)
    res = cv.bitwise_and(img, img, mask=mask)

    # Buscar contornos
    contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    if contours:
        # Tomamos el contorno más grande
        c = max(contours, key=cv.contourArea)
        M = cv.moments(c)
        if M["m00"] > 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])

            # Dibujar punto en el centro
            cv.circle(img, (cx, cy), 5, (0, 0, 255), -1)

            # Dibujar línea desde el último centro al actual
            if ultimo_centro is not None:
                cv.line(trayectoria, ultimo_centro, (cx, cy), (0, 255, 0), 2)

            ultimo_centro = (cx, cy)

    # Combinar video + trayectoria
    salida = cv.add(img, trayectoria)

    cv.imshow('video', salida)
    cv.imshow('mask', mask)
    cv.imshow('res', res)

    k = cv.waitKey(1) & 0xFF
    if k == 27:  # ESC para salir
        break

cap.release()
cv.destroyAllWindows()

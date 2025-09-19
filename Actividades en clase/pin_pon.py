import cv2 as cv
import numpy as np

# Crear lienzo
width, height = 500, 500
radius = 20

# Posición inicial
x, y = 100, 100
# Velocidad inicial
vx, vy = 9,6

while True:
    # Fondo blanco
    img = np.ones((height, width, 3), dtype=np.uint8) * 255
    
    # Dibujar círculo
    cv.circle(img, (x, y), radius, (0, 234, 21), -1)
    
    # Mostrar imagen
    cv.imshow("Pin Pon", img)
    
    # Actualizar posición
    x += vx
    y += vy
    
    # Rebotar en los bordes
    if x - radius <= 0 or x + radius >= width:
        vx = -vx
    if y - radius <= 0 or y + radius >= height:
        vy = -vy
    
    # Control de velocidad de animación
    if cv.waitKey(20) & 0xFF == 27:  # ESC para salir
        break

cv.destroyAllWindows()

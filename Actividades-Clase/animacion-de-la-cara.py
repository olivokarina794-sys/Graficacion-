import cv2 as cv 
import numpy as np
#03-10-25
# Cargar el clasificador de rostros
rostro = cv.CascadeClassifier('haarcascade_frontalface_alt.xml')
cap = cv.VideoCapture(0)

while True:
    ret, img = cap.read()
    if not ret:
        break
        
    gris = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    rostros = rostro.detectMultiScale(gris, 1.3, 5)
    
    for(x, y, w, h) in rostros:
        # Dibujar rectángulo alrededor del rostro
        img = cv.rectangle(img, (x, y), (x+w, y+h), (234, 23, 23), 5)
        
        # Dibujar rectángulo para la boca
        img = cv.rectangle(img, (x, int(y+h/2)), (x+w, y+h), (0, 255, 0), 5)
        
        # Ojos 
        img = cv.circle(img, (x + int(w*0.3), y + int(h*0.4)), 21, (0, 0, 0), 2)
        img = cv.circle(img, (x + int(w*0.7), y + int(h*0.4)), 21, (0, 0, 0), 2)
        img = cv.circle(img, (x + int(w*0.3), y + int(h*0.4)), 20, (255, 255, 255), -1)
        img = cv.circle(img, (x + int(w*0.7), y + int(h*0.4)), 20, (255, 255, 255), -1)
        img = cv.circle(img, (x + int(w*0.3), y + int(h*0.4)), 5, (0, 0, 255), -1)
        img = cv.circle(img, (x + int(w*0.7), y + int(h*0.4)), 5, (0, 0, 255), -1)
        
        # NARIZ - Triángulo proporcional
        nose_width = int(w * 0.15)
        nose_height = int(h * 0.1)
        nose_top = (x + w//2, y + int(h*0.5))
        nose_left = (x + w//2 - nose_width//2, y + int(h*0.5) + nose_height)
        nose_right = (x + w//2 + nose_width//2, y + int(h*0.5) + nose_height)
        
        # Dibujar triángulo de la nariz
        triangle_cnt = np.array([nose_top, nose_left, nose_right])
        img = cv.drawContours(img, [triangle_cnt], 0, (0, 100, 200), -1)
        img = cv.drawContours(img, [triangle_cnt], 0, (0, 0, 0), 2)
        
        # OREJAS - Elipses proporcionales
        ear_width = int(w * 0.15)
        ear_height = int(h * 0.25)
        
        # Oreja izquierda
        left_ear_center = (x - ear_width//2, y + int(h*0.4))
        img = cv.ellipse(img, left_ear_center, (ear_width//2, ear_height//2), 0, 0, 360, (200, 150, 100), -1)
        img = cv.ellipse(img, left_ear_center, (ear_width//2, ear_height//2), 0, 0, 360, (0, 0, 0), 2)
        
        # Oreja derecha
        right_ear_center = (x + w + ear_width//2, y + int(h*0.4))
        img = cv.ellipse(img, right_ear_center, (ear_width//2, ear_height//2), 0, 0, 360, (200, 150, 100), -1)
        img = cv.ellipse(img, right_ear_center, (ear_width//2, ear_height//2), 0, 0, 360, (0, 0, 0), 2)
        
        # BOCA - Arco proporcional
        mouth_width = int(w * 0.4)
        mouth_height = int(h * 0.1)
        mouth_center = (x + w//2, y + int(h*0.7))
        
        # Dibujar boca como una elipse
        img = cv.ellipse(img, mouth_center, (mouth_width//2, mouth_height//2), 0, 0, 180, (0, 0, 255), -1)
        img = cv.ellipse(img, mouth_center, (mouth_width//2, mouth_height//2), 0, 0, 180, (0, 0, 0), 2)
        
      

    cv.imshow('img', img)
    if cv.waitKey(1) == ord('q'):
        break
    
cap.release()
cv.destroyAllWindows()
import cv2 as cv
import numpy as np
import math


img = cv.imread('pa.png', 0)
x, y = img.shape
print(f"Tamaño original: {x}x{y}")


print("Trasladando imagen al contrario...")
dx, dy = -50, -30 
translated_img = np.zeros((x, y), dtype=np.uint8)

for i in range(x):
    for j in range(y):
        
        orig_x = j - dx
        orig_y = i - dy
        
        if 0 <= orig_x < y-1 and 0 <= orig_y < x-1:
            x0 = int(orig_x)
            y0 = int(orig_y)
            x1 = min(x0 + 1, y - 1)
            y1 = min(y0 + 1, x - 1)
            
        
            wx = orig_x - x0
            wy = orig_y - y0
            
          
            p00 = img[y0, x0]
            p01 = img[y0, x1]
            p10 = img[y1, x0]
            p11 = img[y1, x1]
            
            value = (1 - wx) * (1 - wy) * p00 + \
                    wx * (1 - wy) * p01 + \
                    (1 - wx) * wy * p10 + \
                    wx * wy * p11
            
            translated_img[i, j] = np.clip(value, 0, 255)

print(f"Tamaño trasladado: {translated_img.shape}")


angle = 90
theta = math.radians(angle)


cos_ang = abs(math.cos(theta))
sin_ang = abs(math.sin(theta))
rot_x = int(x * cos_ang + y * sin_ang)
rot_y = int(x * sin_ang + y * cos_ang)

rotated_img = np.zeros((rot_x, rot_y), dtype=np.uint8)
print(f"Tamaño rotado: {rot_x}x{rot_y}")


cx, cy = x // 2, y // 2
rot_cx, rot_cy = rot_x // 2, rot_y // 2

print("Rotando 90° con filtro bilineal...")
for i in range(rot_x):
    for j in range(rot_y):
        
        rel_x = j - rot_cy
        rel_y = i - rot_cx
        
        
        orig_x = rel_x * math.cos(theta) + rel_y * math.sin(theta) + cy
        orig_y = -rel_x * math.sin(theta) + rel_y * math.cos(theta) + cx
        
        
        if 0 <= orig_x < y-1 and 0 <= orig_y < x-1:
            x0 = int(orig_x)
            y0 = int(orig_y)
            x1 = min(x0 + 1, y - 1)
            y1 = min(y0 + 1, x - 1)
            
          
            wx = orig_x - x0
            wy = orig_y - y0
            
        
            p00 = translated_img[y0, x0]
            p01 = translated_img[y0, x1]
            p10 = translated_img[y1, x0]
            p11 = translated_img[y1, x1]
            
            value = (1 - wx) * (1 - wy) * p00 + \
                    wx * (1 - wy) * p01 + \
                    (1 - wx) * wy * p10 + \
                    wx * wy * p11
            
            rotated_img[i, j] = np.clip(value, 0, 255)

scale_factor = 2
final_x, final_y = int(rot_x * scale_factor), int(rot_y * scale_factor)
final_img = np.zeros((final_x, final_y), dtype=np.uint8)

print("Escalando imagen 2x con vecino más cercano...")
print(f"Tamaño final: {final_x}x{final_y}")
for i in range(final_x):
    for j in range(final_y):
    
        orig_i = min(int(i / scale_factor), rot_x-1)
        orig_j = min(int(j / scale_factor), rot_y-1)
        final_img[i, j] = rotated_img[orig_i, orig_j]


cv.imshow('1. Imagen Original', img)
cv.imshow('2. Imagen Trasladada (Bilineal)', translated_img)
cv.imshow('3. Imagen Rotada 90° (Bilineal)', rotated_img)
cv.imshow('4. Imagen Final Escalada 2x (Vecino Cercano)', final_img)

print("Presiona cualquier tecla para cerrar las ventanas...")
cv.waitKey(0)
cv.destroyAllWindows()
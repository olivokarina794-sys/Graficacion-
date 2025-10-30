import glfw
from OpenGL.GL import glClearColor, glEnable, glClear, glLoadIdentity, glTranslatef, glRotatef, glMatrixMode
from OpenGL.GL import glBegin, glColor3f, glVertex3f, glEnd, glFlush, glViewport
from OpenGL.GL import GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT, GL_DEPTH_TEST, GL_TRIANGLES, GL_PROJECTION, GL_MODELVIEW
from OpenGL.GLU import gluPerspective
import sys
import time

# Variables globales que voy a usar en todo el programa
window = None  # Esta va a ser mi ventana
angle = 0      # Este ángulo lo uso para hacer girar la pirámide
last_time = 0  # Variable para controlar el tiempo

def init():
    # Aquí configuro cómo se va a ver el fondo y las cosas en 3D
    glClearColor(0.0, 0.0, 0.0, 1.0)  # Pongo el fondo negro (rojo=0, verde=0, azul=0)
    glEnable(GL_DEPTH_TEST)  # Activo la profundidad para que se vea bien en 3D

    # Configuro cómo se proyecta la imagen en la pantalla (la "cámara")
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1.0, 0.1, 50.0)  # Angulo de vista, relación de aspecto, cerca y lejos

    # Cambio para dibujar los objetos
    glMatrixMode(GL_MODELVIEW)

def draw_pyramid():
    global angle, last_time
    
    # Limpio la pantalla y el buffer de profundidad en cada frame
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Preparo la escena para dibujar
    glLoadIdentity()
    glTranslatef(0.0, 0.0, -5)  # Muevo la pirámide hacia atrás para verla bien
    glRotatef(angle, 0, 1, 0)   # La hago girar alrededor del eje Y (el vertical)

    # Empiezo a dibujar TODAS las caras triangulares de la pirámide
    glBegin(GL_TRIANGLES)

    # Cara frontal - Rojo
    glColor3f(1.0, 0.0, 0.0)    # Pongo color rojo
    glVertex3f( 0.0, 1.0, 0.0)  # Punta de la pirámide
    glVertex3f(-1.0, -1.0, 0.0) # Base izquierda
    glVertex3f( 0.0, -1.0, 1.0) # Base frontal

    # Cara derecha - Verde
    glColor3f(0.0, 1.0, 0.0)    # Pongo color verde
    glVertex3f(0.0, 1.0, 0.0)   # Punta
    glVertex3f(0.0, -1.0, 1.0)  # Base frontal
    glVertex3f(1.0, -1.0, 0.0)  # Base derecha

    # Cara izquierda - Azul
    glColor3f(0.0, 0.0, 1.0)    # Pongo color azul
    glVertex3f(0.0, 1.0, 0.0)   # Punta
    glVertex3f(1.0, -1.0, 0.0)  # Base derecha
    glVertex3f(-1.0, -1.0, 0.0) # Base izquierda

    # Base - Amarillo (también es un triángulo)
    glColor3f(1.0, 1.0, 0.0)    # Pongo color amarillo
    glVertex3f(-1.0, -1.0, 0.0) # Esquina izquierda de la base
    glVertex3f( 0.0, -1.0, 1.0) # Esquina frontal de la base
    glVertex3f( 1.0, -1.0, 0.0) # Esquina derecha de la base

    glEnd()  # Termino de dibujar todos los triángulos

    glFlush()  # Aseguro que todo se dibuje

    # Cambio los buffers para que la animación sea suave
    glfw.swap_buffers(window)
    
    # Control de velocidad
    current_time = time.time()
    if current_time - last_time > 0.03:  # Solo actualizo cada 0.03 segundos (30 FPS)
        angle += 0.6  # Control de velocidad de rotación
        last_time = current_time

def main():
    global window, last_time

    # Primero inicializo GLFW
    if not glfw.init():
        sys.exit()

    # Creo la ventana de 500x500 píxeles
    width, height = 500, 500
    window = glfw.create_window(width, height, "Pirámide Triangular 3D Girando", None, None)
    if not window:
        glfw.terminate()
        sys.exit()

    # Hago que esta ventana sea la actual para OpenGL
    glfw.make_context_current(window)

    # Configuro el área de dibujo y inicializo OpenGL
    glViewport(0, 0, width, height)
    init()
    
    last_time = time.time()  # Inicia el tiempo

    # Este es el loop principal del programa - se ejecuta constantemente
    while not glfw.window_should_close(window):
        draw_pyramid()  # Dibujo la pirámide en cada frame
        glfw.poll_events()  # Reviso si hay eventos (como cerrar la ventana)

    # Cuando salgo del loop, cierro todo
    glfw.terminate()

if __name__ == "__main__":
    main()

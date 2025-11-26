import glfw
from OpenGL.GL import *
from OpenGL.GLU import gluPerspective, gluLookAt
import sys

def init():
    """Configuración inicial de OpenGL"""
    glClearColor(0.5, 0.8, 1.0, 1.0)  # Fondo azul cielo
    glEnable(GL_DEPTH_TEST)           # Activar prueba de profundidad

    # Configuración de la perspectiva
    glMatrixMode(GL_PROJECTION)
    gluPerspective(60, 1, 1, 100.0)
    glMatrixMode(GL_MODELVIEW)

def draw_cube():
    """Dibuja el cubo (base de la casa)"""
    glBegin(GL_QUADS)
    glColor3f(0.8, 0.5, 0.2)  # Marrón para todas las caras

    # Frente
    glVertex3f(-1, 0, 1)
    glVertex3f(1, 0, 1)
    glVertex3f(1, 5, 1)
    glVertex3f(-1, 5, 1)

    # Atrás
    glVertex3f(-1, 0, -1)
    glVertex3f(1, 0, -1)
    glVertex3f(1, 5, -1)
    glVertex3f(-1, 5, -1)

    # Izquierda
    glVertex3f(-1, 0, -1)
    glVertex3f(-1, 0, 1)
    glVertex3f(-1, 5, 1)
    glVertex3f(-1, 5, -1)

    # Derecha
    glVertex3f(1, 0, -1)
    glVertex3f(1, 0, 1)
    glVertex3f(1, 5, 1)
    glVertex3f(1, 5, -1)

    # Arriba
    glColor3f(0.9, 0.6, 0.3)
    glVertex3f(-1, 5, -1)
    glVertex3f(1, 5, -1)
    glVertex3f(1, 5, 1)
    glVertex3f(-1, 5, 1)

    # Abajo
    glColor3f(0.6, 0.4, 0.2)
    glVertex3f(-1, 0, -1)
    glVertex3f(1, 0, -1)
    glVertex3f(1, 0, 1)
    glVertex3f(-1, 0, 1)
    glEnd()

def draw_roof():
    """Dibuja el techo (pirámide)"""
    glBegin(GL_TRIANGLES)
    glColor3f(0.9, 0.1, 0.1)  # Rojo brillante

    # Frente
    glVertex3f(-1, 5, 1)
    glVertex3f(1, 5, 1)
    glVertex3f(0, 9, 0)

    # Atrás
    glVertex3f(-1, 5, -1)
    glVertex3f(1, 5, -1)
    glVertex3f(0, 9, 0)

    # Izquierda
    glVertex3f(-1, 5, -1)
    glVertex3f(-1, 5, 1)
    glVertex3f(0, 9, 0)

    # Derecha
    glVertex3f(1, 5, -1)
    glVertex3f(1, 5, 1)
    glVertex3f(0, 9, 0)
    glEnd()

def draw_ground():
    """Dibuja un plano para representar el suelo o calle"""
    glBegin(GL_QUADS)
    glColor3f(0.3, 0.3, 0.3)  # Gris oscuro para la calle

    # Coordenadas del plano
    glVertex3f(-20, 0, 20)
    glVertex3f(20, 0, 20)
    glVertex3f(20, 0, -20)
    glVertex3f(-20, 0, -20)
    glEnd()

def draw_house():
    """Dibuja una casa (base + techo)"""
    draw_cube()
    draw_roof()

def draw_scene():
    """Dibuja toda la escena con vista desde automóvil"""
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # *** MI DESAFÍO - VISTA DESDE AUTOMÓVIL ***
    gluLookAt(0, 1, 18,    # POSICIÓN: Como desde un auto lejano (bajo y atrás)
              0, 1, 0,     # ENFOQUE: Mirando al centro de la calle
              0.5, 1, 0)   # ORIENTACIÓN: Inclinado lateralmente (efecto dinámico)

    # Dibujar el suelo
    draw_ground()

    # Dibujar las casas en diferentes posiciones
    positions = [
        (-5, 0, -5),  # Casa 1
        (5, 0, -5),   # Casa 2
        (-5, 0, 5),   # Casa 3
        (5, 0, 5),    # Casa 4
        (0, 0, 0),    # Casa central
    ]
    
    for pos in positions:
        glPushMatrix()
        glTranslatef(*pos)
        draw_house()
        glPopMatrix()

    glfw.swap_buffers(window)

def main():
    global window

    # Inicializar GLFW
    if not glfw.init():
        sys.exit()
    
    # Crear ventana de GLFW
    width, height = 800, 600
    window = glfw.create_window(width, height, "VISTA DESDE AUTOMÓVIL - Desafío", None, None)
    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)
    glViewport(0, 0, width, height)
    init()

    # Bucle principal
    while not glfw.window_should_close(window):
        draw_scene()
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()
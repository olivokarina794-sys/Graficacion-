import sys
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)  # Establecer color de fondo negro
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1.0, 0.1, 50.0)  # Configuración de perspectiva
    glMatrixMode(GL_MODELVIEW)

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Limpiar buffers
    glLoadIdentity()
    glTranslatef(0.0, 0.0, -5)  # Mover la cámara hacia atrás

    # Dibujar un triángulo invertido con los mismos colores del cuadrado
    glBegin(GL_TRIANGLES)
    
    # Vértice superior izquierdo - Rojo
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-0.5, 0.5, 0.0)
    
    # Vértice inferior - Verde
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, -0.5, 0.0)
    
    # Vértice superior derecho - Azul
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.5, 0.5, 0.0)
    
    glEnd()

    glutSwapBuffers()  # Intercambiar buffers

def main():
    # Inicializar GLUT
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutCreateWindow(b"Triangulo Invertido - GLUT y Python")

    init()
    glutDisplayFunc(display)
    glutMainLoop()

if __name__ == "__main__":
    main()
import glfw
from OpenGL.GL import *
from OpenGL.GLU import *

def draw_christmas_tree():
    """
    FUNCIÓN QUE DIBUJA UN ÁRBOL DE NAVIDAD
    Combino tres tipos de primitivas diferentes:
    - GL_QUADS para el tronco (cuadrado)
    - GL_TRIANGLES para las capas del pino 
    - GL_POINTS para la estrella y decoraciones
    """
    
    # DIBUJO EL TRONCO DEL ÁRBOL - Uso GL_QUADS para hacer un rectángulo
    glBegin(GL_QUADS)  # Inicio la primitiva de cuadriláteros
    glColor3f(0.55, 0.27, 0.07)  # Pongo color marrón para el tronco
    # Defino los 4 vértices del tronco (x, y):
    glVertex2f(-0.05, -0.8)  # Esquina inferior izquierda
    glVertex2f(0.05, -0.8)   # Esquina inferior derecha  
    glVertex2f(0.05, -0.6)   # Esquina superior derecha
    glVertex2f(-0.05, -0.6)  # Esquina superior izquierda
    glEnd()  # Termino de dibujar el tronco
    
    # DIBUJO LAS CAPAS DEL PINO - Uso GL_TRIANGLES para hacer triángulos
    glBegin(GL_TRIANGLES)  # Inicio la primitiva de triángulos
    
    # Primera capa (la de abajo, más grande)
    glColor3f(0.0, 0.5, 0.0)  # Verde oscuro
    glVertex2f(-0.3, -0.6)    # Vértice izquierdo
    glVertex2f(0.3, -0.6)     # Vértice derecho  
    glVertex2f(0.0, -0.3)     # Vértice superior (punta)
    
    # Segunda capa (mediana)
    glColor3f(0.0, 0.7, 0.0)  # Verde medio
    glVertex2f(-0.25, -0.3)   # Vértice izquierdo
    glVertex2f(0.25, -0.3)    # Vértice derecho
    glVertex2f(0.0, 0.0)      # Vértice superior (punta)
    
    # Tercera capa (la de arriba, más pequeña)
    glColor3f(0.0, 0.9, 0.0)  # Verde claro
    glVertex2f(-0.2, 0.0)     # Vértice izquierdo
    glVertex2f(0.2, 0.0)      # Vértice derecho
    glVertex2f(0.0, 0.3)      # Vértice superior (punta)
    glEnd()  # Termino de dibujar las capas del árbol
    
    # DIBUJO LA ESTRELLA EN LA PUNTA - Uso GL_POINTS
    glPointSize(8.0)  # Hago el punto más grande para la estrella
    glBegin(GL_POINTS)  # Inicio la primitiva de puntos
    glColor3f(1.0, 1.0, 0.0)  # Color amarillo para la estrella
    glVertex2f(0.0, 0.35)     # Posición de la estrella (arriba del todo)
    glEnd()  # Termino de dibujar la estrella
    
    # DIBUJO LAS BOLAS DECORATIVAS - También uso GL_POINTS
    glPointSize(10.0)  # Puntos más grandes para las bolas
    glBegin(GL_POINTS)  # Inicio otra primitiva de puntos
    
    # Bolas rojas - glColor3f(1.0, 0.0, 0.0) es rojo
    glColor3f(1.0, 0.0, 0.0)
    glVertex2f(-0.15, -0.45)  # Bola roja izquierda
    glVertex2f(0.1, -0.15)    # Bola roja derecha
    glVertex2f(-0.08, 0.15)   # Bola roja superior
    
    # Bolas azules - glColor3f(0.0, 0.0, 1.0) es azul  
    glColor3f(0.0, 0.0, 1.0)
    glVertex2f(0.12, -0.45)   # Bola azul derecha
    glVertex2f(-0.18, -0.2)   # Bola azul izquierda
    glVertex2f(0.05, 0.1)     # Bola azul superior
    
    # Bolas doradas - glColor3f(1.0, 0.84, 0.0) es dorado
    glColor3f(1.0, 0.84, 0.0)
    glVertex2f(0.0, -0.5)     # Bola dorada central abajo
    glVertex2f(-0.1, -0.1)    # Bola dorada izquierda
    glVertex2f(0.15, 0.05)    # Bola dorada derecha
    glEnd()  # Termino de dibujar las decoraciones

def main():
    """
    FUNCIÓN PRINCIPAL DEL PROGRAMA
    Aquí configuro la ventana y el bucle principal
    """
    # Primero inicializo GLFW (la biblioteca de ventanas)
    if not glfw.init():
        return

    # Creo una ventana de 800x800 píxeles
    window = glfw.create_window(800, 800, "Mi Árbol de Navidad con OpenGL", None, None)
    if not window:
        glfw.terminate()
        return

    # Hago que OpenGL use esta ventana
    glfw.make_context_current(window)

    # Pongo el color de fondo azul oscuro (como cielo nocturno)
    glClearColor(0.0, 0.1, 0.2, 1.0)

    # BUCLE PRINCIPAL - se ejecuta mientras la ventana esté abierta
    while not glfw.window_should_close(window):
        # Limpio la pantalla con el color de fondo
        glClear(GL_COLOR_BUFFER_BIT)

        # Configuro cómo se ve la escena (coordenadas de -1 a 1 en X e Y)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-1.0, 1.0, -1.0, 1.0, -1.0, 1.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        # ¡LLAMO A MI FUNCIÓN PARA DIBUJAR EL ÁRBOL!
        draw_christmas_tree()

        # Actualizo la ventana y reviso eventos (teclado, mouse, etc.)
        glfw.swap_buffers(window)
        glfw.poll_events()

    # Cuando cierro la ventana, finalizo GLFW
    glfw.terminate()

# Esto hace que el programa se ejecute cuando lo corro
if __name__ == "__main__":
    main()
import pygame
import random

# Inicializar Pygame
pygame.init()

# --- Constantes y Configuración ---

# Colores (R, G, B)
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
GRIS = (128, 128, 128)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
CIAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
AMARILLO = (255, 255, 0)

# Dimensiones de la pantalla
ANCHO_PANTALLA = 800
ALTO_PANTALLA = 600

# Dimensiones del área de juego
ANCHO_JUEGO = 15
ALTO_JUEGO = 25
TAMANO_BLOQUE = 20
SUPERIOR_IZQUIERDA_X = (ANCHO_PANTALLA - ANCHO_JUEGO * TAMANO_BLOQUE) // 2
SUPERIOR_IZQUIERDA_Y = ALTO_PANTALLA - ALTO_JUEGO * TAMANO_BLOQUE - 25

# Formas de los Tetriminos
# Cada forma es una lista de sus posibles rotaciones
# Cada rotación es una lista de coordenadas (fila, columna)
S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0.',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0.',
      '.00.',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

# Lista de todas las formas y sus colores correspondientes
FORMAS = [S, Z, I, O, J, L, T]
COLORES_FORMAS = [VERDE, ROJO, CIAN, AMARILLO, AZUL, MAGENTA, (128, 0, 128)]

# --- Clases ---

class Pieza:
    """
    Representa una pieza de Tetris (Tetrimino).
    """
    def __init__(self, columna, fila, forma):
        self.x = columna
        self.y = fila
        self.forma = forma
        self.color = COLORES_FORMAS[FORMAS.index(forma)]
        self.rotacion = 0

def crear_cuadricula(bloqueos_pos={}):
    """
    Crea la estructura de la cuadrícula del juego.
    """
    cuadricula = [[NEGRO for _ in range(ANCHO_JUEGO)] for _ in range(ALTO_JUEGO)]

    for i in range(len(cuadricula)):
        for j in range(len(cuadricula[i])):
            if (j, i) in bloqueos_pos:
                color = bloqueos_pos[(j, i)]
                cuadricula[i][j] = color
    return cuadricula

def convertir_formato_forma(pieza):
    """
    Convierte el formato de la forma de la pieza en una lista de posiciones en la cuadrícula.
    """
    posiciones = []
    formato = pieza.forma[pieza.rotacion % len(pieza.forma)]

    for i, linea in enumerate(formato):
        fila = list(linea)
        for j, columna in enumerate(fila):
            if columna == '0':
                posiciones.append((pieza.x + j, pieza.y + i))

    for i, pos in enumerate(posiciones):
        posiciones[i] = (pos[0] - 2, pos[1] - 4)

    return posiciones

def espacio_valido(pieza, cuadricula):
    """
    Verifica si la pieza se encuentra en una posición válida en la cuadrícula.
    """
    pos_aceptadas = [[(j, i) for j in range(ANCHO_JUEGO) if cuadricula[i][j] == NEGRO] for i in range(ALTO_JUEGO)]
    pos_aceptadas = [j for sub in pos_aceptadas for j in sub]
    formato = convertir_formato_forma(pieza)

    for pos in formato:
        if pos not in pos_aceptadas:
            if pos[1] > -1:
                return False
    return True

def verificar_derrota(posiciones):
    """
    Verifica si alguna pieza ha alcanzado la parte superior de la cuadrícula.
    """
    for pos in posiciones:
        x, y = pos
        if y < 1:
            return True
    return False

def obtener_forma():
    """
    Devuelve una nueva pieza de Tetris aleatoria.
    """
    return Pieza(5, 0, random.choice(FORMAS))

def dibujar_texto_medio(texto, tamano, color, superficie):
    """
    Dibuja texto en el centro de la pantalla.
    """
    fuente = pygame.font.SysFont('comicsans', tamano, bold=True)
    etiqueta = fuente.render(texto, 1, color)
    superficie.blit(etiqueta, (SUPERIOR_IZQUIERDA_X + ANCHO_JUEGO * TAMANO_BLOQUE / 2 - (etiqueta.get_width() / 2),
                              SUPERIOR_IZQUIERDA_Y + ALTO_JUEGO * TAMANO_BLOQUE / 2 - etiqueta.get_height() / 2))

def dibujar_cuadricula(superficie, cuadricula):
    """
    Dibuja las líneas de la cuadrícula del juego.
    """
    sx = SUPERIOR_IZQUIERDA_X
    sy = SUPERIOR_IZQUIERDA_Y

    for i in range(len(cuadricula)):
        pygame.draw.line(superficie, GRIS, (sx, sy + i * TAMANO_BLOQUE), (sx + ANCHO_JUEGO * TAMANO_BLOQUE, sy + i * TAMANO_BLOQUE))
        for j in range(len(cuadricula[i])):
            pygame.draw.line(superficie, GRIS, (sx + j * TAMANO_BLOQUE, sy), (sx + j * TAMANO_BLOQUE, sy + ALTO_JUEGO * TAMANO_BLOQUE))

def limpiar_filas(cuadricula, bloqueos):
    """
    Limpia las filas completas y actualiza la puntuación.
    """
    incremento = 0
    for i in range(len(cuadricula) - 1, -1, -1):
        fila = cuadricula[i]
        if NEGRO not in fila:
            incremento += 1
            ind = i
            for j in range(len(fila)):
                try:
                    del bloqueos[(j, i)]
                except:
                    continue

    if incremento > 0:
        for key in sorted(list(bloqueos), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                nueva_llave = (x, y + incremento)
                bloqueos[nueva_llave] = bloqueos.pop(key)
    return incremento

def dibujar_siguiente_forma(forma, superficie):
    """
    Dibuja la siguiente pieza que aparecerá en el juego.
    """
    fuente = pygame.font.SysFont('comicsans', 30)
    etiqueta = fuente.render('Siguiente', 1, BLANCO)

    sx = SUPERIOR_IZQUIERDA_X + ANCHO_JUEGO * TAMANO_BLOQUE + 50
    sy = SUPERIOR_IZQUIERDA_Y + ALTO_JUEGO * TAMANO_BLOQUE / 2 - 100
    formato = forma.forma[forma.rotacion % len(forma.forma)]

    for i, linea in enumerate(formato):
        fila = list(linea)
        for j, columna in enumerate(fila):
            if columna == '0':
                pygame.draw.rect(superficie, forma.color, (sx + j * TAMANO_BLOQUE, sy + i * TAMANO_BLOQUE, TAMANO_BLOQUE, TAMANO_BLOQUE), 0)

    superficie.blit(etiqueta, (sx + 10, sy - 30))

def dibujar_ventana(superficie, cuadricula, puntuacion=0):
    """
    Dibuja todos los elementos en la ventana del juego. 
    """
    superficie.fill(NEGRO)

    fuente = pygame.font.SysFont('Arial Black', 45)
    etiqueta = fuente.render('TETRIS', 1, BLANCO)

    superficie.blit(etiqueta, (SUPERIOR_IZQUIERDA_X + ANCHO_JUEGO * TAMANO_BLOQUE / 2 - (etiqueta.get_width() / 2), 20))

    # Puntuación
    fuente = pygame.font.SysFont('Algherian', 50)
    etiqueta = fuente.render('Puntuación: ' + str(puntuacion), 1, BLANCO)
    sx = SUPERIOR_IZQUIERDA_X + ANCHO_JUEGO * TAMANO_BLOQUE + 30
    sy = SUPERIOR_IZQUIERDA_Y + ALTO_JUEGO * TAMANO_BLOQUE / 2 - 100
    superficie.blit(etiqueta, (sx + 20, sy + 160))

    for i in range(len(cuadricula)):
        for j in range(len(cuadricula[i])):
            pygame.draw.rect(superficie, cuadricula[i][j], (SUPERIOR_IZQUIERDA_X + j * TAMANO_BLOQUE, SUPERIOR_IZQUIERDA_Y + i * TAMANO_BLOQUE, TAMANO_BLOQUE, TAMANO_BLOQUE), 0)

    dibujar_cuadricula(superficie, cuadricula)
    pygame.draw.rect(superficie, ROJO, (SUPERIOR_IZQUIERDA_X, SUPERIOR_IZQUIERDA_Y, ANCHO_JUEGO * TAMANO_BLOQUE, ALTO_JUEGO * TAMANO_BLOQUE), 5)

# --- Bucle Principal del Juego ---

def main():
    """
    Función principal que ejecuta el juego de Tetris.
    """
    bloqueos_pos = {}
    cuadricula = crear_cuadricula(bloqueos_pos)

    cambiar_pieza = False
    run = True
    pieza_actual = obtener_forma()
    siguiente_pieza = obtener_forma()
    reloj = pygame.time.Clock()
    tiempo_caida = 0
    puntuacion = 0

    while run:
        cuadricula = crear_cuadricula(bloqueos_pos)
        tiempo_caida += reloj.get_rawtime()
        reloj.tick()

        # Caída de la pieza
        if tiempo_caida / 1000 >= 0.27:
            tiempo_caida = 0
            pieza_actual.y += 1
            if not (espacio_valido(pieza_actual, cuadricula)) and pieza_actual.y > 0:
                pieza_actual.y -= 1
                cambiar_pieza = True

        # Manejo de eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT:
                    pieza_actual.x -= 1
                    if not espacio_valido(pieza_actual, cuadricula):
                        pieza_actual.x += 1
                elif evento.key == pygame.K_RIGHT:
                    pieza_actual.x += 1
                    if not espacio_valido(pieza_actual, cuadricula):
                        pieza_actual.x -= 1
                elif evento.key == pygame.K_DOWN:
                    pieza_actual.y += 1
                    if not espacio_valido(pieza_actual, cuadricula):
                        pieza_actual.y -= 1
                elif evento.key == pygame.K_UP:
                    pieza_actual.rotacion = pieza_actual.rotacion + 1 % len(pieza_actual.forma)
                    if not espacio_valido(pieza_actual, cuadricula):
                        pieza_actual.rotacion = pieza_actual.rotacion - 1 % len(pieza_actual.forma)

        forma_pos = convertir_formato_forma(pieza_actual)

        # Colorear la pieza en la cuadrícula
        for i in range(len(forma_pos)):
            x, y = forma_pos[i]
            if y > -1:
                cuadricula[y][x] = pieza_actual.color

        # Si la pieza toca el fondo o otra pieza
        if cambiar_pieza:
            for pos in forma_pos:
                p = (pos[0], pos[1])
                bloqueos_pos[p] = pieza_actual.color
            pieza_actual = siguiente_pieza
            siguiente_pieza = obtener_forma()
            cambiar_pieza = False
            puntuacion += limpiar_filas(cuadricula, bloqueos_pos) * 10

        dibujar_ventana(pantalla, cuadricula, puntuacion)
        dibujar_siguiente_forma(siguiente_pieza, pantalla)
        pygame.display.update()

        # Comprobar si se ha perdido
        if verificar_derrota(bloqueos_pos):
            run = False

    dibujar_texto_medio("¡Has perdido!", 60, BLANCO, pantalla)
    pygame.display.update()
    pygame.time.delay(2000)

def menu_principal():
    """
    Muestra el menú principal del juego.
    """
    run = True
    while run:
        pantalla.fill(NEGRO)
        dibujar_texto_medio('Presiona cualquier tecla para jugar', 40, BLANCO, pantalla)
        pygame.display.update()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                run = False
            if evento.type == pygame.KEYDOWN:
                main()
    pygame.quit()


# Configuración inicial de la pantalla y ejecución del menú
pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
pygame.display.set_caption('Tetris')

menu_principal()
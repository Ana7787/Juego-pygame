import pygame

pygame.init()

COLOR_NEGRO = (0, 0, 0)
COLOR_BOTONES = (255, 0, 255)
COLOR_BLANCO = (255, 255, 255)
COLOR_AZUL = (173, 216, 230)

global velocidad_juego, nivel_actual, puntos, muertes, fuente, puntajes, progreso

pantalla_alto = 600
pantalla_ancho = 1100
pantalla = pygame.display.set_mode((pantalla_ancho, pantalla_alto))

velocidad_juego = 20
x_pos_FD = 0
y_pos_FD = 380
nivel_actual = 1
puntos = 0
fuente = pygame.font.Font('freesansbold.ttf', 20)
musica = pygame.mixer.Sound('Archivos/Sonidos/tema.mp3')
salto = pygame.mixer.Sound('Archivos/Sonidos/wi.mp3')
final_sonido = pygame.mixer.Sound('Archivos/Sonidos/game_over.mp3')

progreso = {}
puntajes = {}
obstaculos = []
muertes = 0

correr = [pygame.image.load("Archivos/Dino/Dinocorriendo1.png"),
          pygame.image.load("Archivos/Dino/Dinocorriendo2.png")]
saltando = pygame.image.load("Archivos/Dino/Dinosaltando.png")
agachado = [pygame.image.load("Archivos/Dino/Dinoagachado1.png"),
            pygame.image.load("Archivos/Dino/Dinoagachado2.png")]
morido = [pygame.image.load("Archivos/Dino/Dinomuerto.png")]

cactus_chiquito = [pygame.image.load("Archivos/Cactus/cactus_chiquito1.png"),
                   pygame.image.load("Archivos/Cactus/cactus_chiquito2.png"),
                   pygame.image.load("Archivos/Cactus/cactus_chiquito3.png")]
cactus_grande = [pygame.image.load("Archivos/Cactus/cactus_grande1.png"),
                 pygame.image.load("Archivos/Cactus/cactus_grande2.png"),
                 pygame.image.load("Archivos/Cactus/cactus_grande3.png")]

pajarito = [pygame.image.load("Archivos/pajarito/pajarito1.png"),
            pygame.image.load("Archivos/pajarito/pajarito2.png")]

nube = pygame.image.load("Archivos/Other/nube.png")

FD = pygame.image.load("Archivos/Other/Fondo.png")

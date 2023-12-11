import random
from constantes import *

class Dinosaurio:
    X_POS = 80
    Y_POS = 310
    Y_POS_agachado = 340
    saltando_VEL = 8.5

    def __init__(self):
        
        self.img_agachado = agachado
        self.img_corriendo = correr
        self.img_saltando = saltando
        self.img_morido = morido

        self.dino_agachado = False
        self.dino_corriendo = True
        self.dino_saltando = False
        self.dino_morido = False

        self.paso_index = 0
        self.saltando_vel = self.saltando_VEL
        self.image = self.img_corriendo[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS

    def carga(self, BotonPresionado, muertes):
        if self.dino_agachado:
            self.agachado()
        if self.dino_corriendo:
            self.corriendo()
        if self.dino_saltando:
            self.saltando()
        if self.dino_morido:
            self.morido()

        if self.paso_index >= 10:
            self.paso_index = 0

        if (BotonPresionado[pygame.K_UP] or BotonPresionado[pygame.K_SPACE]) and not self.dino_saltando:
            self.dino_agachado = False
            self.dino_corriendo = False
            self.dino_saltando = True
            self.dino_morido = False
        elif BotonPresionado[pygame.K_DOWN] and not self.dino_saltando:
            self.dino_agachado = True
            self.dino_corriendo = False
            self.dino_saltando = False
            self.dino_morido = False
        elif not (self.dino_saltando or BotonPresionado[pygame.K_DOWN]):
            self.dino_agachado = False
            self.dino_corriendo = True
            self.dino_saltando = False
            self.dino_morido = False
        elif muertes > 0:
            self.dino_agachado = False
            self.dino_corriendo = False
            self.dino_saltando = False
            self.dino_morido = True

    def agachado(self):
        self.image = self.img_agachado[self.paso_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_agachado
        self.paso_index += 1

    def corriendo(self):
        self.image = self.img_corriendo[self.paso_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.paso_index += 1

    def saltando(self):
        self.image = self.img_saltando
        if self.dino_saltando:
            self.dino_rect.y -= self.saltando_vel * 4
            self.saltando_vel -= 0.8

        if self.saltando_vel < - self.saltando_VEL:
            self.dino_saltando = False
            self.saltando_vel = self.saltando_VEL

    def morido(self):
        self.image = self.img_morido
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        


    def dibujar(self, pantalla):
        pantalla.blit(self.image, (self.dino_rect.x, self.dino_rect.y))


class Nube:
    def __init__(self):
        self.x = pantalla_ancho + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = nube
        self.ancho = self.image.get_width()

    def carga(self):
        self.x -= velocidad_juego
        if self.x < -self.ancho:
            self.x = pantalla_ancho + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def dibujar(self, pantalla):
        pantalla.blit(self.image, (self.x, self.y))



class Obstaculos:
    def __init__(self, image, type):
        self.image = image
        self.tipo = type
        self.rect = self.image[self.tipo].get_rect()
        self.rect.x = pantalla_ancho

    def carga(self):
        self.rect.x -= velocidad_juego

        if self.rect.x < -self.rect.width and obstaculos:
            obstaculos.pop()


    def dibujar(self, pantalla):
        pantalla.blit(self.image[self.tipo], self.rect)


class Cactus_chiquito(Obstaculos):
    def __init__(self, image):
        self.tipo = random.randint(0, 2)
        super().__init__(image, self.tipo)
        self.rect.y = 325


class Cactus_grande(Obstaculos):
    def __init__(self, image):
        self.tipo = random.randint(0, 2)
        super().__init__(image, self.tipo)
        self.rect.y = 300


class Pajarito(Obstaculos):
    def __init__(self, image):
        self.tipo = 0
        super().__init__(image, self.tipo)
        self.rect.y = 250
        self.index = 0

    def dibujar(self, pantalla):
        if self.index >= 9:
            self.index = 0
        pantalla.blit(self.image[self.index//5], self.rect)
        self.index += 1

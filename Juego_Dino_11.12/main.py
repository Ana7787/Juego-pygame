import pygame
import random
from constantes import *
from plataforma import *
from personajes import *
import sqlite3

pygame.init()

musica.play()

with sqlite3.connect('base_puntajes.db') as conexion:
    try:
        sentencia = '''create table puntos
        (
        id integer primary key autoincrement, nombre text, puntaje int    
        )
        '''
        conexion.execute(sentencia)
        print('Se creo la tabla de puntos')

    except sqlite3.OperationalError:
        print('La tabla de puntos existe!!')

    def cerrar_conexion(conexion):
        if conexion:
            conexion.close()

conexion = sqlite3.connect('base_puntajes.db')

def guardar_datos(nombre_usuario:str, puntos:int):
        try:
            conexion.execute('INSERT into puntos(nombre,puntaje) values (?,?)', (nombre_usuario, puntos))
            conexion.commit()
            print("guardo datos en base")
        except:
            print('error')
    
def obtener_datos():
        cursor = conexion.execute("SELECT * FROM PUNTOS order by puntaje desc LIMIT 3")
        datos = [{'nombre': fila[1], 'puntos': fila[2]} for fila in cursor]

        return datos
    
def mostrar_datos():
        corriendo = True

        while corriendo:
            pantalla.fill((255, 255, 255))

            text = fuente.render("Presione ESC para volver al menú", True, (0, 0, 0))
            textRect = text.get_rect()
            textRect.center = (550, 100)
            pantalla.blit(text, textRect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    corriendo = False
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        corriendo = False
                        menu()

            puntajes = obtener_datos()
            for i, puntaje in enumerate(puntajes):
                texto_puntaje = fuente.render(f"{i + 1}. Nombre: {puntaje['nombre']}, Puntos: {puntaje['puntos']}", True, (0, 0, 0))

                pantalla.blit(texto_puntaje, (pantalla_ancho // 2 - 150, pantalla_alto // 2 - 100 + i * 100))

            pygame.display.update()

        pygame.quit()

def score():
    texto = fuente.render("puntos: " + str(puntos), True, (0, 0, 0))
    textoRect = texto.get_rect()
    textoRect.center = (1000, 40)
    pantalla.blit(texto, textoRect)

def ganaste():
    corriendo = True
    guardar_datos(nombre_usuario, puntos)

    while corriendo:

        pantalla.fill((255, 255, 255))

        texto_ganaste = fuente.render('Ganaste! Presiona ESC para volver al menú', True, (0, 0, 0))
        score = fuente.render("Tu Puntaje: " + str(puntos), True, (0, 0, 0))
        scoreRect = score.get_rect()
        scoreRect.center = (pantalla_ancho // 2, pantalla_alto // 2 + 50)
        pantalla.blit(score, scoreRect)
        ganasteRect = texto_ganaste.get_rect()
        ganasteRect.center = (pantalla_ancho // 2, pantalla_alto // 2 + 50)
        ganasteRect = texto_ganaste.get_rect()
        ganasteRect.center = (pantalla_ancho // 2, pantalla_alto // 2)
        pantalla.blit(texto_ganaste, ganasteRect)
        pantalla.blit(correr[0], (pantalla_ancho // 2 - 20, pantalla_alto // 2 - 140))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                corriendo = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu()

        pygame.display.update()

def ingresar_usuario():
    global nombre_usuario
    corriendo = True
    nombre_usuario = ""

    while corriendo:
        pantalla.fill((255, 255, 255))

        texto_ingreso = fuente.render("Ingresa tu nombre de usuario:", True, (0, 0, 0))
        pantalla.blit(texto_ingreso, (pantalla_ancho // 2 -150, pantalla_alto // 2))
        input_rect = pygame.Rect(pantalla_ancho // 2 - 100, pantalla_alto // 2 + 30, 200, 30)
        pygame.draw.rect(pantalla, (0, 0, 0), input_rect, 2)
        texto_input = fuente.render(nombre_usuario, True, (0, 0, 0))
        pantalla.blit(texto_input, (input_rect.x + 5, input_rect.y + 5))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                corriendo = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    corriendo = False
                    menu()

                elif event.key == pygame.K_RETURN:
                    if nombre_usuario:
                        corriendo = False
                        nivel_1()
                        return nombre_usuario
                elif event.key == pygame.K_BACKSPACE:
                    nombre_usuario = nombre_usuario[:-1]
                else:
                    nombre_usuario += event.unicode
        
        pygame.display.update()
    
    pygame.quit()       

def pasar_nivel():
    global corriendo, nivel_actual
    
    corriendo = True
    
    while corriendo:
        pantalla.fill((255, 255, 255))

        texto_ganaste = fuente.render('Pasaste al siguiente nivel! Presiona Enter para continuar o ESC para volver al menú', True, (0, 0, 0))
        ganasteRect = texto_ganaste.get_rect()
        ganasteRect.center = (pantalla_ancho // 2, pantalla_alto // 2 + 50)
        ganasteRect = texto_ganaste.get_rect()
        ganasteRect.center = (pantalla_ancho // 2, pantalla_alto // 2)
        pantalla.blit(texto_ganaste, ganasteRect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                corriendo = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if nivel_actual == 1:
                        nivel_2(muertes)
                    elif nivel_actual == 2:
                        nivel_3(muertes)
                elif event.key == pygame.K_ESCAPE:
                    menu()

        pygame.display.update()
    pygame.quit()

def mostrar_gameover():
    corriendo_go = True
    juego_iniciado = False
    guardar_datos(nombre_usuario, puntos)

    while corriendo_go:
        pantalla.fill((255, 255, 255))

        estado = morido
        text = fuente.render("Game Over. Presiona ESC para volver al menú ", True, (0, 0, 0))
        score = fuente.render("Tu Puntaje: " + str(puntos), True, (0, 0, 0))
        scoreRect = score.get_rect()
        scoreRect.center = (pantalla_ancho // 2, pantalla_alto // 2 + 50)
        pantalla.blit(score, scoreRect)
        textRect = text.get_rect()
        textRect.center = (pantalla_ancho // 2, pantalla_alto // 2)
        pantalla.blit(text, textRect)
        pantalla.blit(estado[0], (pantalla_ancho // 2 - 20, pantalla_alto // 2 - 140))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                corriendo_go = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    corriendo_go = False
                    reiniciar_juego()

        pygame.display.update()
        
    pygame.quit()

def reiniciar_juego():
    global puntos, muertes
    puntos = 0
    muertes = 0
    menu()

def nivel_3(muertes):
    global velocidad_juego, x_pos_FD, y_pos_FD, puntos, obstaculos, nivel_actual
    nivel_actual = 3
    velocidad_juego = 100
    corriendo = True
    clock = pygame.time.Clock()
    player = Dinosaurio()
    nube = Nube()
    corriendo = True

    while corriendo:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                corriendo = False

        pantalla.fill((255, 165, 230))
        BotonPresionado = pygame.key.get_pressed()
        fondo()

        nube.dibujar(pantalla)
        nube.carga()

        player.dibujar(pantalla)
        player.carga(BotonPresionado, muertes)

        if len(obstaculos) == 0:
            if random.randint(0, 2) == 0:
                obstaculos.append(Cactus_chiquito(cactus_chiquito))
            elif random.randint(0, 2) == 1:
                obstaculos.append(Cactus_grande(cactus_grande))
            elif random.randint(0, 2) == 2:
                obstaculos.append(Pajarito(pajarito))

        for obstaculo in obstaculos:
            obstaculo.dibujar(pantalla)
            obstaculo.carga()
            if player.dino_rect.colliderect(obstaculo.rect):
                final_sonido.play()
                pygame.time.delay(500)
                muertes += 1
                mostrar_gameover()
                corriendo = False
            elif (player.dino_rect.x > obstaculo.rect.x and player.dino_rect.x > obstaculo.rect.x + obstaculo.rect.width):       
                salto.play()
                puntos += 4
                if puntos > 455:
                    ganaste()
                    corriendo = False

        score()

        clock.tick(30)
        pygame.display.update()
    pygame.quit()

def nivel_2(muertes):
    global velocidad_juego, x_pos_FD, y_pos_FD, puntos, obstaculos, nivel_actual
    nivel_actual = 2
    velocidad_juego = 55

    corriendo = True
    clock = pygame.time.Clock()
    player = Dinosaurio()
    nube = Nube()
    corriendo = True

    while corriendo:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                corriendo = False

        pantalla.fill((75, 75, 75))
        BotonPresionado = pygame.key.get_pressed()
        fondo()

        nube.dibujar(pantalla)
        nube.carga()

        player.dibujar(pantalla)
        player.carga(BotonPresionado, muertes)

        if len(obstaculos) == 0:
            if random.randint(0, 2) == 0:
                obstaculos.append(Cactus_chiquito(cactus_chiquito))
            elif random.randint(0, 2) == 1:
                obstaculos.append(Cactus_grande(cactus_grande))

        for obstaculo in obstaculos:
            obstaculo.dibujar(pantalla)
            obstaculo.carga()
            if player.dino_rect.colliderect(obstaculo.rect):
                #pygame.time.delay(500)
                final_sonido.play()
                pygame.time.delay(500)
                muertes += 1
                mostrar_gameover()
            elif (player.dino_rect.x > obstaculo.rect.x and player.dino_rect.x > obstaculo.rect.x + obstaculo.rect.width):       
                salto.play()
                puntos += 2
                if puntos == 155:
                    pasar_nivel()

        score()

        clock.tick(30)
        pygame.display.update()
    pygame.quit()

def nivel_1():
    global velocidad_juego, x_pos_FD, y_pos_FD, puntos, obstaculos, muertes, nivel_actual, nombre_usuario
    nivel_actual = 1
    corriendo1 = True
    clock = pygame.time.Clock()
    player = Dinosaurio()
    nube = Nube()

    while corriendo1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                corriendo1 = False

        pantalla.fill((173, 216, 230))
        BotonPresionado = pygame.key.get_pressed()
        fondo()

        nube.dibujar(pantalla)
        nube.carga()

        player.dibujar(pantalla)
        player.carga(BotonPresionado, muertes)

        if len(obstaculos) == 0:
            if random.randint(0, 2) == 0:
                obstaculos.append(Cactus_chiquito(cactus_chiquito))

        for obstaculo in obstaculos:
            obstaculo.dibujar(pantalla)
            obstaculo.carga()
            if player.dino_rect.colliderect(obstaculo.rect):
                final_sonido.play()
                pygame.time.delay(500)
                muertes += 1
                mostrar_gameover()
                corriendo1 = False
            elif (player.dino_rect.x > obstaculo.rect.x and player.dino_rect.x > obstaculo.rect.x + obstaculo.rect.width):       
                puntos += 1
                salto.play()
                if puntos == 25:
                    pasar_nivel()
                    corriendo1 = False

        score()

        clock.tick(30)
        pygame.display.update()
        
    pygame.quit()
    return muertes

def menu():
    global puntos, muertes
    corriendo = True
    puntos = 0
    boton_inicio = pygame.Rect(pantalla_ancho // 2 - 50, pantalla_alto // 2 - 25, 100, 50)
    boton_salir = pygame.Rect(pantalla_ancho // 2 - 50, pantalla_alto // 2 + 50, 100, 50)
    boton_puntajes = pygame.Rect(pantalla_ancho // 2 - 50, pantalla_alto // 2 + 125, 100, 50)

    while corriendo:
        pantalla.fill((255, 255, 255))

        text = fuente.render("DINOSAAAWWR", True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (550, 100)
        pantalla.blit(text, textRect)
        pantalla.blit(correr[0], (pantalla_ancho // 2 - 40, pantalla_alto // 2 - 140))


        pygame.draw.rect(pantalla, (0, 0, 0), boton_inicio)
        pygame.draw.rect(pantalla, (0, 0, 0), boton_salir)
        pygame.draw.rect(pantalla, (0, 0, 0), boton_puntajes)

        fuente_boton = pygame.font.Font('freesansbold.ttf', 20)
        texto_inicio = fuente_boton.render("Inicio", True, (255, 255, 255))
        texto_salir = fuente_boton.render("Salir", True, (255, 255, 255))
        texto_puntajes = fuente_boton.render("Puntajes", True, (255, 255, 255))


        pantalla.blit(texto_inicio, (boton_inicio.x + 25, boton_inicio.y + 15))
        pantalla.blit(texto_salir, (boton_salir.x + 30, boton_salir.y + 15))
        pantalla.blit(texto_puntajes, (boton_puntajes.x + 8, boton_puntajes.y + 15))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                corriendo = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    corriendo = False
                    pygame.quit()  # Cierra Pygame correctamente
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if boton_inicio.collidepoint(event.pos):
                        #guardar_puntaje()
                        ingresar_usuario()
                    elif boton_salir.collidepoint(event.pos):
                        corriendo = False
                    elif boton_puntajes.collidepoint(event.pos):
                        #cargar_puntajes()
                        #obtener_datos()
                        print(obtener_datos())
                        mostrar_datos()
        pygame.display.flip()

    pygame.quit()

menu()
cerrar_conexion(conexion)


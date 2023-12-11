from constantes import *

def fondo():
    global x_pos_FD, y_pos_FD
    imagen_alto = FD.get_height()
    pantalla.blit(FD, (x_pos_FD, y_pos_FD))
    pantalla.blit(FD, (imagen_alto + x_pos_FD, y_pos_FD))
    if x_pos_FD <= -imagen_alto:
        pantalla.blit(FD, (imagen_alto + x_pos_FD, y_pos_FD))
        x_pos_FD = 0
        y_pos_FD = 380
    x_pos_FD -= velocidad_juego

import pygame.image
from pygame.math import Vector2 as vec

#PANTALLA
ANCHO, ALTO = 912,966
BORDE = 70
ANCHO_JUEGO,ALTO_JUEGO = ANCHO - BORDE, ALTO - BORDE
FPS = 60

#FUENTE (TAMAÑO Y COLOR)
TAMAÑO_TEXTO_INI = 25
FUENTE_INI = 'arial black'

#COLORES
Negro = (0,0,0)
Blanco = (255,255,255)
Gris = (127,127,127)
Naranja = (170,132,68)
Cian = (44,167,190)
Morado = (163, 73, 164)

#PERSONAJE

POS_INI_X = (BORDE//2 + ANCHO_JUEGO/19 * 1.2)
POS_INI_Y = (BORDE//2 + ALTO_JUEGO/21 * 1.05)

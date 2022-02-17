import os.path
import sys
import pygame
from personaje import *
from Configuracion import *


# INICIO
pygame.init()
vec = pygame.math.Vector2


class Aplicacion:

    def __init__(self):
        self.screen = pygame.display.set_mode((ANCHO, ALTO))
        self.clock = pygame.time.Clock()
        self.running = True
        self.estado = 'intro'
        self.ancho_celda = (ANCHO_JUEGO // 19)
        self.alto_celda = (ALTO_JUEGO // 21)
        self.personaje = Personaje(self,vec(1,1))
        self.muros = []
        self.cargar()

    def run(self):
        while self.running:
            if self.estado == 'intro':
                self.inicio_eventos()
                self.inicio_actualizar()
                self.inicio_graficos()
            if self.estado == 'jugando':
                self.jugando_eventos()
                self.jugando_actualizar()
                self.jugando_graficos()
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()
    ######################################FUNCIONES AUXILIARES###################################

    def dibujar_texto(self, texto, screen, posicion, tamaño, color, nombre_fuente, centrado = False):
        fuente = pygame.font.SysFont(nombre_fuente, tamaño)
        mensaje = fuente.render(texto, False, color)
        tamaño_mensaje = mensaje.get_size()
        if (centrado):
            posicion[0] = posicion[0] - tamaño_mensaje[0]//2
            posicion[1] = posicion[1] - tamaño_mensaje[1]//2
        screen.blit(mensaje, posicion)

    def cargar(self):
        self.fondo = pygame.image.load('imgs/maze-optimizada.png')
        self.fondo = pygame.transform.scale(self.fondo,(ANCHO_JUEGO,ALTO_JUEGO))

        with open("muros.txt",'r') as file:
            for ywall, line in enumerate(file):
                for xwall, char in enumerate(line):
                    if char == "1":
                        self.muros.append(vec(xwall,ywall))
        print(self.muros)

    def dibujarMatriz(self):
        #Comprobacion de que las casillas están bien situadas
        for x in range(ANCHO_JUEGO // 19):
            pygame.draw.line(self.fondo, Gris,(x*ANCHO_JUEGO//19,0),(x*ANCHO_JUEGO//19,ALTO))
        for y in range(ALTO_JUEGO // 21):
            pygame.draw.line(self.fondo, Gris, (0,y * ALTO_JUEGO//21),(ANCHO,y * ALTO_JUEGO//21))
    def dibujarMuros(self):
        #Comprobación de que los muros están bien definidos
        for muro in self.muros:
            pygame.draw.rect(self.fondo, Morado, (muro.x*ANCHO_JUEGO//19, muro.y*ALTO_JUEGO//21, self.ancho_celda, self.alto_celda))

    ######################################FUNCIONES DE PANTALLA INICIAL######################################

    def inicio_eventos(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.estado = 'jugando'

    def inicio_actualizar(self):
        pass

    def inicio_graficos(self):
        self.screen.fill(Negro)
        self.dibujar_texto('PULSA ESPACIO PARA EMPEZAR', self.screen, [ANCHO//2, ALTO//2], TAMAÑO_TEXTO_INI, Naranja, FUENTE_INI,centrado=True)
        self.dibujar_texto('1 SOLO JUGADOR', self.screen, [ANCHO // 2, ALTO // 2 + 100], TAMAÑO_TEXTO_INI, Cian,
                           FUENTE_INI,centrado=True)
        self.dibujar_texto('HIGH SCORE', self.screen, [10,0], TAMAÑO_TEXTO_INI, Blanco,
                           FUENTE_INI)
        pygame.display.update()

    ################################################FUNCIONES DE JUEGO EJECUTANDOSE#################################################

    def jugando_eventos(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.personaje.moverse(vec(-1,0))
                if event.key == pygame.K_RIGHT:
                    self.personaje.moverse(vec(1,0))
                if event.key == pygame.K_UP:
                    self.personaje.moverse(vec(0,-1))
                if event.key == pygame.K_DOWN:
                    self.personaje.moverse(vec(0,1))

    def jugando_actualizar(self):
        self.personaje.actualizar()

    def jugando_graficos(self):
        self.screen.fill(Negro)
        self.screen.blit(self.fondo, (BORDE//2,BORDE//2))
        self.dibujarMatriz()
        # self.dibujarMuros()
        self.personaje.dibujarPerson(self.screen)
        pygame.display.update()

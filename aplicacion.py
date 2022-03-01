import os.path
import sys
import pygame
from personaje import *
from Configuracion import *
from Enemigo import *


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
        self.llaves = []
        self.enemigos=[]
        self.pos_enemigo = []
        self.cargar()
        self.cargar_enemigo()
        self.sumador_puntuacion = pygame.USEREVENT+1

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
            if self.estado == 'GAME OVER':
                self.gameover_eventos()
                self.gameover_actualizar()
                self.gameover_graficos()
                pass
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

        with open("mapa_de_juego.txt", 'r') as file:
            for ywall, line in enumerate(file):
                for xwall, char in enumerate(line):
                    if char == "1":
                        self.muros.append(vec(xwall,ywall))
                    elif char == "L":
                        self.llaves.append(vec(xwall,ywall))
                    elif char in ["2","3","4","5"]:
                        self.pos_enemigo.append(vec(xwall,ywall))
                    elif char == "P":
                        pygame.draw.rect(self.fondo,Negro,(xwall*self.ancho_celda,ywall*self.alto_celda,self.ancho_celda,self.alto_celda))

    def cargar_enemigo(self):
        for indice,pos in enumerate(self.pos_enemigo):
            self.enemigos.append(Enemigo(self,vec(pos),indice))


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

    def dibujarLLaves(self):
        dibujo = pygame.image.load("imgs/llave_final.png")
        dibujo = pygame.transform.scale(dibujo, (self.ancho_celda-20, self.alto_celda-13))
        for llave in self.llaves:
            self.screen.blit(dibujo,(int(llave.x*ANCHO_JUEGO//19)+14+35, int(llave.y*ALTO_JUEGO//21)+7+35))

    def reset(self):
        self.personaje.vidas = 3
        self.personaje.puntuacion = 0
        self.personaje.pos_matriz = vec(1,1)
        self.personaje.pix_pos = self.personaje.getPixPos()
        self.personaje.direction = vec(1,0)
        for enemigo in self.enemigos:
            enemigo.pos_matriz = vec(enemigo.pos_inicial)
            enemigo.pos_pix = enemigo.getPixpos()
            enemigo.direction *= 0

        self.coins = []
        with open("walls.txt", 'r') as file:
            for yidx, line in enumerate(file):
                for xidx, char in enumerate(line):
                    if char == 'C':
                        self.coins.append(vec(xidx, yidx))
        self.state = "playing"

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
        self.screen.fill(Cian)
        img_inicio = pygame.image.load("imgs/press-space.png")
        self.screen.blit(img_inicio,[-25, ALTO//2])
        self.dibujar_texto('1 SOLO JUGADOR', self.screen, [ANCHO // 2, ALTO // 2 + 200], TAMAÑO_TEXTO_INI, Naranja,
                           FUENTE_INI,centrado=True)
        self.dibujar_texto('MÁXIMA PUNTUACIÓN', self.screen, [10,0], TAMAÑO_TEXTO_INI, Blanco,FUENTE_INI)
        pygame.display.update()

    ################################################FUNCIONES DE JUEGO EJECUTANDOSE#################################################

    def jugando_eventos(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.personaje.moverse(vec(-1,0))
                    self.personaje.img_actual = self.personaje.img_izq
                if event.key == pygame.K_RIGHT:
                    self.personaje.moverse(vec(1,0))
                    self.personaje.img_actual = self.personaje.img_dcha
                if event.key == pygame.K_UP:
                    self.personaje.moverse(vec(0,-1))
                    self.personaje.img_actual = self.personaje.img_espaldas
                if event.key == pygame.K_DOWN:
                    self.personaje.moverse(vec(0,1))
                    self.personaje.img_actual = self.personaje.img_frontal

    def jugando_actualizar(self):
        self.personaje.actualizar()
        for enemigo in self.enemigos:
            enemigo.actualizar()

        for enemigo in self.enemigos:
            if enemigo.pos_matriz == self.personaje.pos_matriz:
                self.pierde_vida()

    def jugando_graficos(self):
        self.screen.fill(Negro)
        self.screen.blit(self.fondo, (BORDE//2,BORDE//2))
        self.dibujarLLaves()
        self.dibujar_texto('MÁXIMA PUNTUACIÓN', self.screen, [ANCHO_JUEGO//2+200, 0], 18, Blanco,FUENTE_INI)
        self.dibujar_texto('PUNTUACIÓN: {}'.format(self.personaje.puntuacion),self.screen, [60, 0], 18, Blanco, FUENTE_INI)
        self.personaje.dibujarPerson(self.personaje.img_actual)
        self.personaje.dibujarVidas()
        for enemigo in self.enemigos:
            enemigo.dibujar_enemigo()
        pygame.display.update()

    def pierde_vida(self):
        self.personaje.vidas -= 1
        if self.personaje.vidas == 0:
            self.estado = "GAME OVER"
        else:
            self.personaje.pos_matriz = vec(1,1)
            self.personaje.pos_pix = self.personaje.getPixPos()
            self.personaje.direccion = vec(1,0)
            for enemigo in self.enemigos:
                enemigo.pos_matriz = vec(enemigo.pos_inicial)
                enemigo.pos_pix = enemigo.getPixpos()
                enemigo.direccion = vec(0,0)

    ################################################FUNCIONES DE GAME OVER#################################################

    def gameover_eventos(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.reset()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False

    def gameover_actualizar(self):
        pass

    def gameover_graficos(self):
        self.screen.fill(Cian)
        pygame.display.update()

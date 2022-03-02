import os.path
import sys
import pygame

import conexion
from personaje import *
from conexion import *
from Configuracion import *
from Enemigo import *
from datetime import datetime


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
        self.pos_inicial = None
        self.muros = []
        self.llaves = []
        self.enemigos=[]
        self.pos_enemigo = []
        self.cargar()
        self.personaje = Personaje(self, vec(self.pos_inicial))
        self.cargar_enemigo()
        self.puntuacion_maxima = 0
        self.restador_puntuacion = pygame.USEREVENT+1
        pygame.time.set_timer(self.restador_puntuacion,2000)

    def run(self):
        conexion.Conexion.crearBD(DBFILE)
        conexion.Conexion.conectarBD(DBFILE)
        self.cargar_puntuacion()
        while self.running:
            if self.estado == 'intro':
                self.inicio_eventos()
                self.inicio_actualizar()
                self.inicio_graficos()
            if self.estado == 'jugando':
                self.jugando_eventos()
                self.jugando_actualizar()
                self.jugando_graficos()
                if pygame.event.get(self.restador_puntuacion):
                    self.personaje.puntuacion -= 1
            if self.estado == 'GAME OVER':
                self.gameover_eventos()
                self.gameover_actualizar()
                self.gameover_graficos()
            if self.estado == 'ganar':
                self.ganar_eventos()
                self.ganar_actualizar()
                self.ganar_graficos()
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
                    elif char == "A":
                        self.pos_inicial = [xwall,ywall]
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
        self.personaje.vidas = 2
        self.personaje.puntuacion = 0
        self.personaje.pos_matriz = vec(self.personaje.pos_inicial)
        self.personaje.pos_pix = self.personaje.getPixPos()
        self.personaje.direccion = vec(0,0)
        for enemigo in self.enemigos:
            enemigo.pos_matriz = vec(enemigo.pos_inicial)
            enemigo.pos_pix = enemigo.getPixpos()
            enemigo.direccion *= 0

        self.llaves = []
        with open("mapa_de_juego.txt", 'r') as file:
            for yidx, line in enumerate(file):
                for xidx, char in enumerate(line):
                    if char == 'L':
                        self.llaves.append(vec(xidx, yidx))
        self.estado = "jugando"

    def reset_sin_iniciar(self):
        self.personaje.vidas = 2
        self.personaje.puntuacion = 0
        self.personaje.pos_matriz = vec(self.personaje.pos_inicial)
        self.personaje.pos_pix = self.personaje.getPixPos()
        self.personaje.direccion = vec(0,0)
        for enemigo in self.enemigos:
            enemigo.pos_matriz = vec(enemigo.pos_inicial)
            enemigo.pos_pix = enemigo.getPixpos()
            enemigo.direccion *= 0

        self.llaves = []
        with open("mapa_de_juego.txt", 'r') as file:
            for yidx, line in enumerate(file):
                for xidx, char in enumerate(line):
                    if char == 'L':
                        self.llaves.append(vec(xidx, yidx))

    def cargar_puntuacion(self):
        query = QtSql.QSqlQuery()
        query.prepare('SELECT max_puntos FROM puntuacion DESC')
        if query.exec():
            while query.next():
                self.puntuacion_maxima = query.value(0)
        else:
            print('fallo al sacar la puntuacion')


    ######################################FUNCIONES DE PANTALLA INICIAL######################################

    def inicio_eventos(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.estado = 'jugando'

    def inicio_actualizar(self):
        self.cargar_puntuacion()

    def inicio_graficos(self):
        self.screen.fill(Cian)
        img_inicio = pygame.image.load("imgs/press-space.png")
        self.screen.blit(img_inicio,[-25, ALTO//2])
        self.dibujar_texto('1 SOLO JUGADOR', self.screen, [ANCHO // 2, ALTO // 2 + 200], TAMAÑO_TEXTO_INI, Naranja,
                           FUENTE_INI,centrado=True)
        self.dibujar_texto('MÁXIMA PUNTUACIÓN: '+str(self.puntuacion_maxima), self.screen, [10,0], TAMAÑO_TEXTO_INI, Blanco,FUENTE_INI)
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
        self.dibujar_texto('MÁXIMA PUNTUACIÓN '+str(self.puntuacion_maxima), self.screen, [ANCHO_JUEGO//2+200, 0], 18, Blanco,FUENTE_INI)
        if len(self.llaves) == 5:
            self.dibujar_texto('0/5 ', self.screen, [ANCHO_JUEGO//2+120, 0], 18, Blanco,FUENTE_INI)
        if len(self.llaves) == 4:
            self.dibujar_texto('1/5 ', self.screen, [ANCHO_JUEGO//2+120, 0], 18, Blanco,FUENTE_INI)
        if len(self.llaves) == 3:
            self.dibujar_texto('2/5 ', self.screen, [ANCHO_JUEGO//2+120, 0], 18, Blanco,FUENTE_INI)
        if len(self.llaves) == 2:
            self.dibujar_texto('3/5 ', self.screen, [ANCHO_JUEGO//2+120, 0], 18, Blanco,FUENTE_INI)
        if len(self.llaves) == 1:
            self.dibujar_texto('4/5 ', self.screen, [ANCHO_JUEGO//2+120, 0], 18, Blanco,FUENTE_INI)
        # imagen_llave = pygame.image.load("imgs/llave_final.png")
        # imagen_llave = pygame.transform.scale(imagen_llave, (self.ancho_celda-26, self.alto_celda-17))
        # self.screen.blit(imagen_llave,([ANCHO_JUEGO//2+150,0]))
        self.dibujar_texto('PUNTUACIÓN: {}'.format(self.personaje.puntuacion),self.screen, [60, 0], 18, Blanco, FUENTE_INI)
        self.personaje.dibujarPerson(self.personaje.img_actual)
        self.personaje.dibujarVidas()
        for enemigo in self.enemigos:
            enemigo.dibujar_enemigo()
        pygame.display.update()

    def pierde_vida(self):
        self.personaje.vidas -= 1
        self.personaje.puntuacion -= 50
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
        img_inicio = pygame.image.load("imgs/restart.png")
        self.screen.blit(img_inicio, [-70, ALTO // 2])
        self.dibujar_texto("Press ESC to Exit", self.screen, [
            ANCHO // 2, ALTO // 1.5], 36, (190, 190, 190), FUENTE_INI)
        pygame.display.update()


    ###########################################FUNCIONES GANAR#####################################

    def ganar_eventos(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.cargar_puntuacion()
                self.reset_sin_iniciar()
                self.estado = 'intro'

    def ganar_actualizar(self):
        if self.personaje.puntuacion > self.puntuacion_maxima:
            self.puntuacion_maxima = self.personaje.puntuacion
            conexion.Conexion.conectarBD(DBFILE)
            info = []
            fecha = datetime.now()
            fecha_formateada = fecha.strftime("%d/%m/%Y")
            info.append(self.puntuacion_maxima)
            info.append(fecha_formateada)
            conexion.Conexion.guardar_puntuacion(info)


    def ganar_graficos(self):
        self.screen.fill(Negro)
        img_ganar = pygame.image.load("imgs/ganar.jpg")
        self.screen.blit(img_ganar, [250,ALTO//2-250])
        self.dibujar_texto("Tu puntuación ha sido de: "+str(self.personaje.puntuacion), self.screen, [178, ALTO // 1.5], 36, (Blanco), FUENTE_INI)
        pygame.display.update()




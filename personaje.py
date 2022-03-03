import aplicacion
from Configuracion import *
import pygame
from aplicacion import *
vec = pygame.math.Vector2


class Personaje:

    def __init__(self, app, pos):
        self.app = app
        self.pos_matriz = pos
        self.pos_inicial = [pos.x,pos.y]
        self.pos_pix = self.getPixPos()
        self.img_actual = "imgs/pj2-frente.png"
        self.img_frontal = "imgs/pj2-frente.png"
        self.img_izq = "imgs/pj2-izq.png"
        self.img_dcha = "imgs/pj2-dcha.png"
        self.img_espaldas = "imgs/pj2-espaldas.png"
        self.puntuacion = 0
        self.direccion = vec(0,0)
        self.direccion_almacenada = None
        self.puede_moverse = True
        self.velocidad = 1
        self.vidas = 1

    def actualizar(self):
        if self.puede_moverse:
            self.pos_pix += self.direccion*self.velocidad
        if self.momento_moverse():
            if self.direccion_almacenada != None:
                self.direccion = self.direccion_almacenada
            self.puede_moverse = self.PuedeMoverse()

        self.pos_matriz.x = (self.pos_pix.x-35)//self.app.ancho_celda
        self.pos_matriz.y = (self.pos_pix.y-35)//self.app.alto_celda

        if self.sobre_llave():
            self.coger_llave()

    def sobre_llave(self):
        if self.pos_matriz in self.app.llaves:
            return True
        return False

    def coger_llave(self):
        self.app.llaves.remove(self.pos_matriz)
        self.puntuacion += 100
        if not self.app.llaves:
            self.app.estado = "ganar"


    def moverse(self, direccion):
        self.direccion_almacenada = direccion

    def getPixPos(self):
        return vec((self.pos_matriz.x*self.app.ancho_celda) + (BORDE//2)+(self.app.ancho_celda//2)-12,
                   (self.pos_matriz.y*self.app.alto_celda)+(BORDE//2)+(self.app.alto_celda//2)-13)


    def dibujarPerson(self,img_inicio):
        imagen = pygame.image.load(img_inicio).convert()
        imagen = pygame.transform.scale(imagen, (23, 34))
        posicion = (int(self.pos_pix.x), int(self.pos_pix.y))
        #pygame.draw.rect(self.app.fondo, Rojo, (self.pos_matriz.x*self.app.ancho_celda,self.pos_matriz.y*self.app.alto_celda,self.app.ancho_celda,self.app.alto_celda),1)
        self.app.screen.blit(imagen, posicion)


    def dibujarVidas(self):
        for x in range(self.vidas):
            imagen_vida = pygame.image.load("imgs/corazon.png").convert()
            imagen_vida = pygame.transform.scale(imagen_vida, (33, 28))
            posicion_cora = (30 + 30*x,ALTO-33)
            self.app.screen.blit(imagen_vida,posicion_cora)

    def momento_moverse(self):
        if self.pos_pix.x % self.app.ancho_celda == 0:
            if self.direccion == vec(1,0) or self.direccion == vec(-1,0) or self.direccion == vec(0,0):
                return True

        if self.pos_pix.y % self.app.alto_celda == 0:
            if self.direccion == vec(0,1) or self.direccion == vec(0,-1) or self.direccion == vec(0,0):
                return True

    def PuedeMoverse(self):
        for muro in self.app.muros:
            if vec(self.pos_matriz+self.direccion) == muro:
                return False
        return True
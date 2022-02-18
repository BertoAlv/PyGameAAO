import aplicacion
from Configuracion import *
import pygame
from aplicacion import *
vec = pygame.math.Vector2


class Personaje:

    def __init__(self, app, pos):
        self.app = app
        self.pos_matriz = pos
        self.pos_pix = self.getPixPos()
        self.direccion = vec(1,0)
        self.direccion_almacenada = None
        self.puede_moverse = True

    def actualizar(self):
        if self.puede_moverse:
            self.pos_pix += self.direccion
        if self.momento_movimiento():
            if self.direccion_almacenada != None:
                self.direccion = self.direccion_almacenada
            self.puede_moverse = self.PuedeMoverse()

        self.pos_matriz.x = (self.pos_pix.x-35)//self.app.ancho_celda
        self.pos_matriz.y = (self.pos_pix.y-35)//self.app.alto_celda


    def moverse(self, direccion):
        self.direccion_almacenada = direccion;

    def getPixPos(self):
        return vec((self.pos_matriz.x*self.app.ancho_celda) + (BORDE//2)+(self.app.ancho_celda//2)-14,
                   (self.pos_matriz.y*self.app.alto_celda)+(BORDE//2)+(self.app.alto_celda//2)-14)


    def dibujarPerson(self,screen):
        imagen = pygame.image.load("imgs/pj2-frente.png")
        imagen = pygame.transform.scale(imagen, (25, 34))
        posicion = (int(self.pos_pix.x), int(self.pos_pix.y))
        pygame.draw.rect(self.app.fondo, Rojo, (self.pos_matriz.x*self.app.ancho_celda,self.pos_matriz.y*self.app.alto_celda,self.app.ancho_celda,self.app.alto_celda),1)
        screen.blit(imagen, posicion)

    def momento_movimiento(self):
        if self.pos_pix.x % self.app.ancho_celda == 0:
            if self.direccion == vec(1,0) or self.direccion == vec(-1,0):
                return True

        if self.pos_pix.y % self.app.alto_celda == 0:
            if self.direccion == vec(0,1) or self.direccion == vec(0,-1):
                return True

    def PuedeMoverse(self):
        for muro in self.app.muros:
            if vec(self.pos_matriz+self.direccion) == muro:
                return False
        return True
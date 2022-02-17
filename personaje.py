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
        self.direccion = vec(0,0)
        self.direccion_almacenada = None

    def actualizar(self):
        self.pos_pix += self.direccion
        if self.pos_pix.x % self.app.ancho_celda == 0:
            if self.direccion == vec(1,0) or self.direccion == vec(-1,0):
                if self.direccion_almacenada != None:
                    self.direccion = self.direccion_almacenada

        if self.pos_pix.y % self.app.alto_celda == 0:
            if self.direccion == vec(0,1) or self.direccion == vec(0,-1):
                if self.direccion_almacenada != None:
                    self.direccion = self.direccion_almacenada

        self.pos_matriz.x = (self.pos_pix.x-BORDE//2)//(ANCHO_JUEGO//19)-13
        self.pos_matriz.y = (self.pos_pix.y-BORDE//2)//(ALTO_JUEGO//21)-19


    def moverse(self, direccion):
        self.direccion_almacenada = direccion;

    def getPixPos(self):
        return vec((self.pos_matriz.x*ANCHO_JUEGO//19) + (BORDE//2)+((ANCHO_JUEGO//19)//2)-13,
                   (self.pos_matriz.y*ALTO_JUEGO//21)+(BORDE//2)+((ALTO_JUEGO//19)//2)-19)


    def dibujarPerson(self,screen):
        imagen = pygame.image.load("imgs/pj2-frente.png")
        imagen = pygame.transform.scale(imagen, (25, 34))
        posicion = (int(self.pos_pix.x), int(self.pos_pix.y))
        pygame.draw.rect(self.app.fondo, Rojo, (self.pos_matriz.x*(ANCHO_JUEGO//19),self.pos_matriz.y*(ALTO_JUEGO//21),ANCHO_JUEGO//19,ALTO_JUEGO//21),1)
        screen.blit(imagen, posicion)

    def PuedeMoverse(self):
        for muro in self.app.muros:
            if vec(self.pos_matriz+self.direccion) == muro:
                return False
        return True
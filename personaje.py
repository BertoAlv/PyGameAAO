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
        self.puede_moverse = True
        self.direccion = vec(1,0)

    def moverse(self, direccion):
        self.pos_matriz += direccion;

    def getPixPos(self):
        return vec((self.pos_matriz.x*self.app.ancho_celda) + BORDE, (self.pos_matriz.y*self.app.alto_celda)+BORDE)
        print(self.pos_matriz,self.pos_pix)

    def dibujarPerson(self,screen):
        imagen = pygame.image.load("imgs/pj2-frente.png")
        imagen = pygame.transform.scale(imagen, (29, 39))
        posicion = self.pos_matriz
        screen.blit(imagen, posicion)

    def PuedeMoverse(self):
        for muro in self.app.muros:
            if vec(self.pos_matriz+self.direccion) == muro:
                return False
        return True
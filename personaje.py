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

    def mover(self, direccion):
        self.direccion = direccion

    def getPixPos(self):
        return vec((self.pos_matriz.x*self.app.ancho_celda) + BORDE, (self.pos_matriz.y*self.app.alto_celda)+BORDE)
        print(self.pos_matriz,self.pos_pix)

    @staticmethod
    def dibujarPerson(self, url, screen, posicion):
        imagen = pygame.image.load(url)
        imagen = pygame.transform.scale(imagen, (29, 39))
        screen.blit(imagen, posicion)

    def PuedeMoverse(self):
        for muro in self.app.muros:
            if vec(self.pos_matriz+self.direccion) == muro:
                return False
        return True
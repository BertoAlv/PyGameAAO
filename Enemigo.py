import pygame
import random
from Configuracion import *
vec = pygame.math.Vector2

class Enemigo:
    def __init__(self,app,pos, indice):
        self.app = app
        self.pos_matriz = pos
        self.pos_inicial = [pos.x,pos.y]
        self.pos_pix = self.getPixpos()
        self.indice = indice
        self.direccion = vec(0,0)
        self.actuacion = self.set_actuacion()
        self.objetivo = None


    def actualizar(self):
        self.objetivo = self.set_objetivo()
        if self.objetivo != self.pos_matriz:
            self.pos_pix += self.direccion
            if self.momento_moverse():
                self.moverse()

        self.pos_matriz.x = (self.pos_pix.x - 35) // self.app.ancho_celda
        self.pos_matriz.y = (self.pos_pix.y - 35) // self.app.alto_celda

    def dibujar_enemigo(self):
        imagen = pygame.image.load("imgs/snake-final.png").convert()
        imagen = pygame.transform.scale(imagen, (25, 34))
        posicion = (int(self.pos_pix.x), int(self.pos_pix.y))
        #pygame.draw.rect(self.app.fondo, Rojo, (self.pos_matriz.x * self.app.ancho_celda, self.pos_matriz.y * self.app.alto_celda, self.app.ancho_celda,self.app.alto_celda), 1)
        self.app.screen.blit(imagen, posicion)

    def getPixpos(self):
        return vec((self.pos_matriz.x * self.app.ancho_celda) + (BORDE // 2) + (self.app.ancho_celda // 2)-12,
                   (self.pos_matriz.y * self.app.alto_celda) + (BORDE // 2) + (self.app.alto_celda // 2)-13)


    def momento_moverse(self):
        if self.pos_pix.x % self.app.ancho_celda == 0:
            if self.direccion == vec(1,0) or self.direccion == vec(-1,0) or self.direccion == (0,0):
                return True

        if self.pos_pix.y % self.app.alto_celda == 0:
            if self.direccion == vec(0,1) or self.direccion == vec(0,-1) or self.direccion == (0,0):
                return True
        return False

    def set_actuacion(self):
        if self.indice == 0:
            return "aleatoria2"
        if self.indice == 1:
            return "aleatoria"
        if self.indice == 2:
            return "buscadora"
        if self.indice == 3:
            return "buscadora2"


    def moverse(self):
        if self.actuacion == "aleatoria":
            self.direccion = self.get_random_direction()
        if self.actuacion == "aleatoria2":
            self.direccion = self.get_random_direction()
        if self.actuacion == "buscadora":
            self.direccion = self.encontrar_camino(self.objetivo)
        if self.actuacion == "buscadora2":
            self.direccion = self.encontrar_camino(self.objetivo)


    def encontrar_camino(self,objetivo):
        celda_siguiente = self.encontrar_celda_siguiente(objetivo)
        xdir = celda_siguiente[0] - self.pos_matriz[0]
        ydir = celda_siguiente[1] - self.pos_matriz[1]
        return vec(xdir, ydir)

    def encontrar_celda_siguiente(self,objetivo):
        path = self.BFS([int(self.pos_matriz.x), int(self.pos_matriz.y)], [int(objetivo[0]), int(objetivo[1])])
        return path[1]

    def BFS(self, inicio, objetivo):
        matriz = [[0 for x in range(19)] for x in range(21)]
        for cell in self.app.muros:
            if cell.x < 19 and cell.y < 21:
                matriz[int(cell.y)][int(cell.x)] = 1
        queue = [inicio]
        path = []
        visited = []
        while queue:
            current = queue[0]
            queue.remove(queue[0])
            visited.append(current)
            if current == objetivo:
                break
            else:
                neighbours = [[0, -1], [1, 0], [0, 1], [-1, 0]]
                for neighbour in neighbours:
                    if neighbour[0] + current[0] >= 0 and neighbour[0] + current[0] < len(matriz[0]):
                        if neighbour[1] + current[1] >= 0 and neighbour[1] + current[1] < len(matriz):
                            next_cell = [neighbour[0] + current[0], neighbour[1] + current[1]]
                            if next_cell not in visited:
                                if matriz[next_cell[1]][next_cell[0]] != 1:
                                    queue.append(next_cell)
                                    path.append({"Current": current, "Next": next_cell})
        shortest = [objetivo]
        while objetivo != inicio:
            for step in path:
                if step["Next"] == objetivo:
                    objetivo = step["Current"]
                    shortest.insert(0, step["Current"])
        return shortest

    def get_random_direction(self):
        while True:
            numero = random.randint(-2,1)
            if numero == -2:
                xdir,ydir = 1,0
            elif numero == -1:
                xdir,ydir = 0,1
            elif numero == 1:
                xdir,ydir = -1,0
            else:
                xdir,ydir = 0,-1
            pos_siguiente = vec(self.pos_matriz.x + xdir, self.pos_matriz.y + ydir)
            if pos_siguiente not in self.app.muros:
                break
        return vec(xdir,ydir)

    def set_objetivo(self):
        if self.actuacion == "buscadora" or self.actuacion == "buscadora2":
            return self.app.personaje.pos_matriz
        else:
            if self.app.personaje.pos_matriz[0] > COLUMNAS // 2 and self.app.personaje.pos_matriz[1] > FILAS // 2:
                return vec(1, 1)
            if self.app.personaje.pos_matriz[0] > COLUMNAS // 2 and self.app.personaje.pos_matriz[1] < FILAS // 2:
                return vec(1, FILAS - 2)
            if self.app.personaje.pos_matriz[0] < COLUMNAS // 2 and self.app.personaje.pos_matriz[1] > FILAS // 2:
                return vec(COLUMNAS - 2, 1)
            else:
                return vec(COLUMNAS - 2, FILAS - 2)


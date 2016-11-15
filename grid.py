import pygame
import math


GRASS = 0
WATER = 1
ROCKS = 2

IMGS = ["imgs/hex_tile_grass.png"
       ,"imgs/hex_tile_water.png"
       ,"imgs/hex_tile_rocks.png"]

SelIMG = "imgs/hex_tile_sel.png"

class Tile:
    def __init__(self, t=GRASS):
        self.type = t

class Grid:
    def rectToHex(self, i, j):
        y = int(j*4/self.size/3)
        x = int((i-self.size*(y%2)/2)/self.size)
        return (x, y)

    def hexToRect(self, i, j):
        i -= math.floor(j / 2)
        x = i*self.size + j*self.size/2
        y = j*self.size*3/4
        return (x, y)

    def hexDistance(self, ai, aj, bi, bj):
        ati = ai - math.floor(aj/2)
        bti = bi - math.floor(bj/2)
        return ( abs(ati - bti) 
               + abs(ati + aj - bti - bj)
               + abs(aj - bj)) / 2
        


    def __init__(self, width = 10, height = 10, size = 32):
        self.width  = width
        self.height = height
        self.size   = size
        self.tiles  = [[Tile(GRASS) for x in range(0, width)] for y in range(0, height)]
        self._imgs  = {}
        for i in range(0, len(IMGS)):
            self._imgs[i] = pygame.image.load(IMGS[i])
            self._imgs[i] = pygame.transform.scale(self._imgs[i], (size, size))
        self._rect = self._imgs[0].get_rect()
        self.selectedX = []
        self.selectedY = []
        self._simg = pygame.image.load(SelIMG)
        self._simg = pygame.transform.scale(self._simg, (size, size))

    def draw(self, screen, vx, vy):
        if vx < 0: vx = 0
        if vy < 0: vy = 0
        xi, yi = self.rectToHex(vx, vy)
        xo, yo = self.rectToHex(screen.get_width(),screen.get_height())
        for i in range(-2, xo+2):
            for j in range(-2, yo+2):
                if not self.inRange(i + xi, j + yi): continue
                tile = self.tiles[i + xi][j + yi]
                img  = self._imgs[tile.type]
                self._rect.x, self._rect.y = self.hexToRect(i + xi, j + yi)
                self._rect.x -= vx
                self._rect.y -= vy
                screen.blit(img, self._rect)
                if (i + xi) in self.selectedX and (j + yi) in self.selectedY:
                    screen.blit(self._simg, self._rect)

    def inRange(self, i, j):
        return (i >= 0 and i < self.width and j >= 0 and j < self.height)

    def setTile(self, i, j, k):
        self.tiles[i][j].type = k

    def getBetween(self, i, j, n, f):
        return [(x, y)
                for x in range(0, self.width)
                for y in range(0, self.height)
                if n <= self.hexDistance(i, j, x, y) <= f]

    def select(self, i, j):
        self.selectedX.append(i)
        self.selectedY.append(j)

    def clearSelection(self):
        self.selectedX = []
        self.selectedY = []

    def getAdjacent(self, i, j):
        return self.getBetween(i, j, 1, 1)

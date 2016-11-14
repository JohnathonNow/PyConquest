from collections import namedtuple
import pygame
import math

Tile = namedtuple("Tile", ["x", "y"])

GRASS = 0
WATER = 1
ROCKS = 2

IMGS = ["imgs/hex_tile_grass.png"
       ,"imgs/hex_tile_water.png"
       ,"imgs/hex_tile_rocks.png"]

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
        self.tiles  = {}
        for x in range(0, width):
            for y in range(0, height):
                self.tiles[Tile(x, y)] = GRASS

        self._imgs        = {}
        self._rect        = {}
        for i in range(0, len(IMGS)):
            self._imgs[i] = pygame.image.load(IMGS[i])
            self._imgs[i] = pygame.transform.scale(self._imgs[i], (size, size))
            self._rect[i] = self._imgs[i].get_rect()

    def draw(self, screen, vx, vy):
        if vx < 0: vx = 0
        if vy < 0: vy = 0
        xi, yi = self.rectToHex(vx, vy)
        xo, yo = self.rectToHex(screen.get_width(),screen.get_height())
        for i in range(-2, xo+2):
            for j in range(-2, yo+2):
                if not self.inRange(i + xi, j + yi): continue
                tile = self.tiles[Tile(i + xi, j + yi)]
                img  = self._imgs[tile]
                rct  = self._rect[tile]
                rct.x, rct.y = self.hexToRect(i + xi, j + yi)
                rct.x -= vx
                rct.y -= vy
                screen.blit(img, rct)

    def inRange(self, i, j):
        return (i >= 0 and i < self.width and j >= 0 and j < self.height)

    def setTile(self, i, j, k):
        self.tiles[Tile(i, j)] = k

    def getBetween(self, i, j, n, f):
        return [(x, y)
                for x in range(0, self.width)
                for y in range(0, self.height)
                if n <= self.hexDistance(i, j, x, y) <= f]

    def getAdjacent(self, i, j):
        return self.getBetween(i, j, 1, 1)

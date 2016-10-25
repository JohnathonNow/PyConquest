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

ADJACENTS   = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, -1), (1, 1)]

class Grid:
    def rectToHex(self, i, j):
        y = math.floor(j*4/self.size/3)
        x = math.floor((i-self.size*(y%2)/2)/self.size)
        return (x, y)

    def hexToRect(self, i, j):
        i -= math.floor(j / 2)
        x = i*self.size + j*self.size/2
        y = j*self.size*3/4
        return (x, y)

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

    def draw(self, screen):
        for i in range(0, self.width):
            for j in range(0, self.height):
                tile = self.tiles[Tile(i, j)]
                img  = self._imgs[tile]
                rct  = self._rect[tile]
                rct.x, rct.y = self.hexToRect(i, j)
                screen.blit(img, rct)

    def inRange(self, i, j):
        return (i >= 0 and i < self.width and j >= 0 and j < self.height)

    def setTile(self, i, j, k):
        self.tiles[Tile(i, j)] = k

    def getAdjacent(self, i, j):
        if j%2 == 0:
            return [(x + i - (y + j)%2, y + j) 
                    for (x, y) in ADJACENTS
                    if self.inRange(x + i - (y + j)%2, y + j)]
        else:
            return [(x + i, y + j) 
                    for (x, y) in ADJACENTS
                    if self.inRange(x + i, y + j)]
            

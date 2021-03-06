import pygame
import math
import random
import queue

GRASS = 0
WATER = 1
ROCKS = 2
CITY = 3

PASSABLE = [GRASS, CITY]

IMGS = ["imgs/hex_tile_grass.png"
       ,"imgs/hex_tile_water.png"
       ,"imgs/hex_tile_rocks.png"
       ,"imgs/hex_tile_city.png"]

IMGS2 = ["imgs/hex_tile_grass_far.png"
       ,"imgs/hex_tile_water_far.png"
       ,"imgs/hex_tile_rocks_far.png"
       ,"imgs/hex_tile_city_far.png"]

SelIMG = "imgs/hex_tile_sel.png"
UnseenIMG = "imgs/hex_tile_unknown.png"

ADJACENTS   = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, -1), (1, 1)]

class Tile:
    def __init__(self, t=GRASS, s="n/a"):
        self.type = t
        self.units = 0
        self.known = False
        self.city = s
        self.visible = False

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
        self.tiles  = [[Tile(GRASS, "n/a") for x in range(0, width)] for y in range(0, height)]
        y = 0
        with open("map.txt", "r") as mp:
            for line in mp:
                for x in range(0,width):
                    if line[x] == "R":
                        self.tiles[x][y] = Tile(ROCKS, "n/a")
                    elif line[x] == "G":
                        self.tiles[x][y] = Tile(GRASS, "n/a")
                    elif line[x] == "B":
                        self.tiles[x][y] = Tile(WATER, "n/a")
                y += 1
        self._imgs  = {}
        self._imgs2 = {}
        for i in range(0, len(IMGS)):
            self._imgs[i] = pygame.image.load(IMGS[i])
            self._imgs[i] = pygame.transform.scale(self._imgs[i], (size, size)).convert_alpha()
            self._imgs2[i] = pygame.image.load(IMGS2[i])
            self._imgs2[i] = pygame.transform.scale(self._imgs2[i], (size, size)).convert_alpha()
        self._rect = self._imgs[0].get_rect()
        self.selected = []
        self._simg = pygame.image.load(SelIMG)
        self._simg = pygame.transform.scale(self._simg, (size, size)).convert_alpha()
        self._uimg = pygame.image.load(UnseenIMG)
        self._uimg = pygame.transform.scale(self._uimg, (size, size)).convert_alpha()

    def draw(self, screen, vx, vy):
        if vx < 0: vx = 0
        if vy < 0: vy = 0
        xi, yi = self.rectToHex(vx, vy)
        xo, yo = self.rectToHex(screen.get_width(),screen.get_height())
        for i in range(-2, xo+2):
            for j in range(-2, yo+2):
                if not self.inRange(i + xi, j + yi): continue
                tile = self.tiles[i + xi][j + yi]
                if tile.known:
                    if tile.visible == True:
                        img  = self._imgs[tile.type]
                    else:
                        img = self._imgs2[tile.type]
                else:
                    img = self._uimg
                self._rect.x, self._rect.y = self.hexToRect(i + xi, j + yi)
                self._rect.x -= vx
                self._rect.y -= vy
                screen.blit(img, self._rect)
                if tile in self.selected:
                    screen.blit(self._simg, self._rect)

    def inRange(self, i, j):
        return (i >= 0 and i < self.width and j >= 0 and j < self.height)

    def getTile(self, i, j):
        return self.tiles[i][j]

    def setTile(self, i, j, k, l):
        self.tiles[i][j].type = k
        self.tiles[i][j].city = l

    def setVisible(self):
        for i in range(0, self.width):
            for j in range(0, self.height):
                self.getTile(i,j).visible = False

    def getBetween(self, i, j, n, f):
        return [(x, y)
                for x in range(i-n-f-f, i+n+f+f)
                for y in range(j-n-f-f, j+n+f+f)
                if self.inRange(x, y) and
                n <= self.hexDistance(i, j, x, y) <= f]

    def select(self, i, j):
        #if self.tiles[i][j].known:
        self.selected.append(self.tiles[i][j])
        return True
        #return False

    def clearSelection(self):
        self.selected = []

    def getAdjacent(self, i, j):
        #return self.getBetween(i, j, 1, 1)
        if j%2 == 0:
            return [(x + i - (y + j)%2, y + j) 
                    for (x, y) in ADJACENTS
                    if self.inRange(x + i - (y + j)%2, y + j)]
        else:
            return [(x + i, y + j) 
                    for (x, y) in ADJACENTS                                                       if self.inRange(x + i, y + j)]

    #use A* to find the shortest path
    #between (sx, sy) and (ex, ey)
    #returns a set of visited tiles
    def shortestPath(self, sx, sy, ex, ey):
        marked = {}
        q = queue.PriorityQueue()
        #we cannot go to a non-grass tile,
        #so random walk until we get to one
        while self.getTile(ex, ey).type not in PASSABLE:
            ex, ey = random.choice(self.getAdjacent(ex, ey))
        #start A*
        q.put((0, ((ex, ey), (ex, ey))))
        while not q.empty():
            v = q.get()
            if v[1][0] in marked: continue #we've been here, so leave
            marked[v[1][0]] = v[1][1] #mark the current entry
            if v[1][0] == (sx, sy): break #stop when we find our destination
            for u in self.getAdjacent(v[1][0][0], v[1][0][1]): #add neighbors
                h = self.hexDistance(u[0], u[1], sx, sy) #calculate heuristic
                if self.getTile(u[0], u[1]).type in PASSABLE: #only visit valids
                    #"best" path is the least tiles + prefer tiles closer
                    #to our destination
                    q.put((1 + v[0] + h, (u, v[1][0])))
        path = set()
        v = (sx, sy)
        #add the path to the set
        while not v == (ex, ey):
            path.add(v)
            v = marked[v]
        return path

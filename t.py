#!/usr/bin/python2
import sys, pygame, math, grid

pygame.init()

size = width, height = 656, int(656)
black = 0, 0, 0
Vx, Vy = 0, 0
dvx, dvy = 0, 0
gWidth = 600
gSize = 64
sleep_time = 16
menu_y = 0.624*height
menu_text_x = 56
menu_text_y = menu_y + 40
gTileW = gWidth*gSize - width + gSize
screen = pygame.display.set_mode(size)
g   = grid.Grid(gWidth, gWidth, gSize)
X, Y = (5, 5)
menu = pygame.image.load("imgs/menu.png")
menu = pygame.transform.scale(menu, size).convert_alpha()
menu_rect = menu.get_rect()
menu_font = pygame.font.SysFont("monospace", 15)

g.setTile(X, Y, grid.WATER)
for (i, j) in g.getBetween(X, Y, 2, 5):
    g.setTile(i, j, grid.ROCKS)

for (i, j) in g.getBetween(0, 0, 0, 5):
    g.getTile(i, j).known = True

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            if my < menu_y:
                xx, yy = g.rectToHex(mx + Vx, my + Vy)
                g.clearSelection()
                g.select(xx, yy)
                if g.selected:
                    for (i, j) in g.getBetween(xx, yy, 0, 1):
                        g.getTile(i, j).known = True
        if event.type == pygame.KEYUP:
            if event.key == 276:
                dvx = 0
            elif event.key == 274:
                dvy = 0
            elif event.key == 275:
                dvx = 0
            elif event.key == 273:
                dvy = 0
        if event.type == pygame.KEYDOWN:
            if event.key == 276:
                dvx = -1
            elif event.key == 274:
                dvy = 1
            elif event.key == 275:
                dvx = 1
            elif event.key == 273:
                dvy = -1
                
    Vx += dvx*32
    Vy += dvy*32
    if Vx < 0: Vx = 0
    if Vy < 0: Vy = 0
    if Vx > gTileW: Vx = gTileW
    if Vy > gTileW: Vy = gTileW
    screen.fill(black)
    g.draw(screen, Vx, Vy)
    screen.blit(menu, menu_rect)

    label_string = ["", "", "", "", ""]
    
    if g.selected:
        label_string[0] = "There are {} troops here.".format(g.selected[0].units)
        label_string[1] = "It is {} here.".format({grid.GRASS: "grassy", grid.WATER: "watery", grid.ROCKS: "rocky"}[g.selected[0].type])
    else:
        label_string[0] = "You gotta select something."
    
    for i in xrange(0,len(label_string)):
        label = menu_font.render(label_string[i], 1, (0,0,0))
        screen.blit(label, (menu_text_x, menu_text_y + 16*i))
    
    pygame.display.flip()
    pygame.time.wait(sleep_time)

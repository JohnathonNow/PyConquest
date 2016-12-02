#!/usr/bin/python2
import sys
import pygame
import math
import grid
import core
import inputbox

pygame.init()

size = width, height = 656, int(656)  #size of game window
gWidth = 600                          #number of tiles per row
gSize = 64                            #size of grid tiles, in pixels
startX, startY = 520, 300             #starting coordinates, in tiles
dvx, dvy = 0, 0                       #starting viewpoint velocity
sleep_time = 16                       #number of milliseconds to sleep for
menu_y = 0.624*height                 #lower boundary of visible tile area
menu_text_x = 56                      #where to draw text
menu_text_y = menu_y + 40             #where to draw text
gTileW = gWidth*gSize - width + gSize #viewpoint extreme location
screen = pygame.display.set_mode(size)#set screen
g = grid.Grid(gWidth, gWidth, gSize)  #define grid
xx, yy = 0, 0                         #last clicked tile coordinates

#load menu image
menu = pygame.image.load("imgs/menu.png")
menu = pygame.transform.scale(menu, size).convert_alpha()
menu_rect = menu.get_rect()
#load menu font
menu_font = pygame.font.SysFont("monospace", 15)
#get game instance, for core processing
game = core.Game(g, screen)
game.moveCortez(startX, startY)

#calculate starting viewpoint
Vx, Vy = startX*gSize - width/2, startY*gSize*3/4 - height/2
#unhide the starting area
for (i, j) in g.getBetween(startX, startY, 0, 10):
    g.getTile(i, j).known = True

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit() #handle quitting
        if event.type == pygame.MOUSEBUTTONDOWN: #handle clicking
            mx, my = event.pos
            if my < menu_y:
                xxt, yyt = g.rectToHex(mx + Vx, my + Vy)
                g.clearSelection()
                if g.select(xxt, yyt): 
                    xx, yy = xxt, yyt
        if event.type == pygame.KEYUP:          #handle key releases
            k = pygame.key.name(event.key)
            if k == 'left' or k == 'right': 
                dvx = 0
            elif k == 'down' or k == 'up':
                dvy = 0
            elif k == 'space':  #move cortez
                if g.selected and g.selected[0].known:
                    game.moveCortez(xx, yy)
            elif k == 'c':      #send troops
                if g.selected:
                    c = inputbox.ask(screen, 'How many men?')
                    game.sendMen(xx, yy, c)
            elif k == 'z':      #recenter camera
                Vx, Vy = game.cortez_x*gSize - width/2, game.cortez_y*gSize*3/4 - height/2
        if event.type == pygame.KEYDOWN:        #handle key presses
            k = pygame.key.name(event.key)
            if k == 'left':
                dvx = -1
            elif k == 'down':
                dvy = 1
            elif k == 'right':
                dvx = 1
            elif k == 'up':
                dvy = -1
    #move view                
    Vx += dvx*32
    Vy += dvy*32
    #prevent view from going too far
    if Vx < 0: Vx = 0
    if Vy < 0: Vy = 0
    if Vx > gTileW: Vx = gTileW
    if Vy > gTileW: Vy = gTileW
    #clear screen
    screen.fill((0, 0, 0))
    #draw grid
    g.draw(screen, Vx, Vy)
    #draw menu
    screen.blit(menu, menu_rect)
    #process main logic
    game.run(xx, yy)
    #draw text labels
    for i in range(0,len(game.label_string)):
        label = menu_font.render(game.label_string[i], 1, (0,0,0))
        screen.blit(label, (menu_text_x, menu_text_y + 16*i))
    #flop
    pygame.display.flip()
    pygame.time.wait(sleep_time)

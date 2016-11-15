import sys, pygame, math, grid


pygame.init()

size = width, height = 656, int(656)
black = 0, 0, 0
Vx, Vy = 0, 0
dvx, dvy = 0, 0
gWidth = 600
gSize = 64
sleep_time = 16
gTileW = gWidth*gSize - width + gSize
screen = pygame.display.set_mode(size)
g   = grid.Grid(gWidth, gWidth, gSize)
X, Y = (5, 5)
menu = pygame.image.load("imgs/menu.png")
menu = pygame.transform.scale(menu, size).convert_alpha()
menu_rect = menu.get_rect()
g.setTile(X, Y, grid.WATER)
for (i, j) in g.getBetween(X, Y, 2, 5):
    g.setTile(i, j, grid.ROCKS)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            if my < 0.624*height:
                xx, yy = g.rectToHex(mx + Vx, my + Vy)
                g.clearSelection()
                g.select(xx, yy)
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
    pygame.display.flip()
    pygame.time.wait(sleep_time)

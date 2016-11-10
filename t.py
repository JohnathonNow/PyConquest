import sys, pygame, math, grid


pygame.init()

size = width, height = 656, int(656*3/4)
black = 0, 0, 0
Vx, Vy = 0, 0
dvx, dvy = 0, 0

screen = pygame.display.set_mode(size)
g   = grid.Grid(600,600,64)
X, Y = (5, 5)

g.setTile(X, Y, grid.WATER)
for (i, j) in g.getBetween(X, Y, 2, 5):
    g.setTile(i, j, grid.ROCKS)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            xx, yy = g.rectToHex(mx + Vx, my + Vy)
            g.setTile(xx, yy, grid.WATER)
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
                
    Vx += dvx
    Vy += dvy
    print Vx, Vy
    screen.fill(black)
    g.draw(screen, Vx, Vy)
    pygame.display.flip()

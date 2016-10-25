import sys, pygame, math, hexgrid.grid


pygame.init()

size = width, height = 336, math.ceil(336*3/4)
black = 0, 0, 0

screen = pygame.display.set_mode(size)
grid   = hexgrid.grid.Grid()
X, Y = (5, 5)

grid.setTile(X, Y, hexgrid.grid.WATER)
for (i, j) in grid.getAdjacent(X, Y):
    grid.setTile(i, j, hexgrid.grid.ROCKS)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                xx, yy = grid.rectToHex(mx, my)
                grid.setTile(xx, yy, hexgrid.grid.WATER)

    screen.fill(black)
    grid.draw(screen)
    pygame.display.flip()

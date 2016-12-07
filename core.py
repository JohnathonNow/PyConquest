import grid
import inputbox
class Game:
    def __init__(self, g, s):
        self.xt = 0
        self.yt = 0
        self.cityData = {}
        #define cities
        self.cityData["Tenochtitlan"] = {"Population" : 1000000,
                                         "Troops" : 2000,
                                         "Resources" : 300,
                                         "Smallpox" : "No",
                                         "Starvation" : "No",
                                        }
        self.label_string = ["", "", "", "", "", "", "", "", ""]
        self.cortez_x, self.cortez_y = 520, 300                     #cortez starting location
        self.grid = g
        self.screen = s
        self.troops = {'spanish': 500}
        self.dispatched = []
        self.time = 0
        self.mode = 'select'

    def run(self):
        xx = self.xt
        yy = self.yt
        self.time += 1 #increment time
        #handle displaying useful information
        if self.grid.selected:
            self.label_string[0] = "There are {} troops here.".format(self.grid.selected[0].units)
            if (self.grid.selected[0].type != grid.CITY):
                self.label_string[1] = "It is {} here.".format(
                    {grid.GRASS: "grassy", grid.WATER: "watery", grid.ROCKS: "rocky"}[self.grid.selected[0].type])
            else:
                ct = self.grid.selected[0].city
                self.label_string[1] = ct
                self.label_string[2] = "Population: " + str(cityData[ct]["Population"])
                self.label_string[3] = "Troops: " + str(cityData[ct]["Troops"])
                self.label_string[4] = "Resources: " + str(cityData[ct]["Resources"])
                self.label_string[5] = "Smallpox?: " + str(cityData[ct]["Smallpox"])
                self.label_string[6] = "Starvation?: " + str(cityData[ct]["Starvation"])
        else:
            self.label_string[0] = "You gotta select something."

        #move dispatched troops
        if self.time % 10 == 0:
            for group in self.dispatched:
                if (self.cortez_x == group[1] and 
                    self.cortez_y == group[2] and
                    self.time     >= group[5]):
                    self.label_string[7] = "Your dispatched troups have returned"
                    for (i, j) in self.grid.getBetween(group[3], group[4], 0, 3):
                        self.grid.getTile(i, j).known = True
                    for n in group[6]:
                        self.grid.getTile(n[0], n[1]).known = True
                    #recover troops
                    self.troops['spanish'] += group[0]
                    self.dispatched.remove(group)
          
        self.label_string[8] = 'Men: ' + ', '.join(['{} {}'.format(self.troops[x], x) for x in self.troops])
                
            
    def moveCortez(self, xx, yy):
        if self.grid.getTile(xx, yy).type != grid.GRASS: return     #can only move on grass
        #hide old tiles
        for (i, j) in self.grid.getBetween(self.cortez_x, self.cortez_y, 0, 1):
            self.grid.getTile(i, j).visible = False
        #make area visible
        for (i, j) in self.grid.getBetween(xx, yy, 0, 1):
            self.grid.getTile(i, j).known = True
            self.grid.getTile(i, j).visible = True
        self.cortez_x = xx
        self.cortez_y = yy

    def sendMen(self, xx, yy, count):
        try:
            count = int(count)
            if count <= self.troops['spanish'] and count > 0:
                self.troops['spanish'] -= count
                p = self.grid.shortestPath(self.cortez_x, self.cortez_y, xx, yy)
                self.dispatched.append( (count, self.cortez_x, self.cortez_y, xx, yy, len(p) + self.time, p) )
        except:
            return
        
    def handleKeyDown(self, k):
        pass

    def handleKeyUp(self, k):
        if k == 'space':  #move cortez
            if self.grid.selected and self.grid.selected[0].known:
                self.moveCortez(self.xt, self.yt)
        elif k == 'c':    #send troops
            if self.grid.selected:
                c = inputbox.ask(self.screen, 'How many men?')
                self.sendMen(self.xt, self.yt, c)

    def handleClick(self, xxt, yyt):
        self.grid.clearSelection()
        if self.grid.select(xxt, yyt): 
            self.xt = xxt
            self.yt = yyt
            if self.mode == 'move' and self.grid.selected[0].known:
                self.moveCortez(self.xt, self.yt)
            elif self.mode == 'dispatch':
                c = inputbox.ask(self.screen, 'How many men?')
                self.sendMen(self.xt, self.yt, c)

    def handleMenu(self, mx, my):
        if my > 605 and my < 650:
            chosex = int((mx - 31) / 101)
            if chosex < 5:
                self.mode = ['move', 'dispatch', self.mode, self.mode, 'select'][chosex]
        

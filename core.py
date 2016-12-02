import grid
class Game:
    def __init__(self, g, s):
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
    def run(self, xx, yy):
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
                px = group[1]
                py = group[2]
                t = self.grid.getTile(px, py)
                #keep track of where we've been
                group[8].append(t)
                #make us win
                if group[1] > group[3]: group[1] -= 1
                if group[2] > group[4]: group[2] -= 1
                if group[1] < group[3]: group[1] += 1
                if group[2] < group[4]: group[2] += 1
                #make us in grass
                if t.type != grid.GRASS:
                    group[1] = px + 1
                    group[2] = py
                #when we reach our destination, turn around
                #bright eyes
                if group[1] == group[3] and group[2] == group[4]:
                    if group[5]:
                        group[5] = False
                        group[3] = group[6] #set new destination to origin
                        group[4] = group[7] #set new destination to origin
                        group[6] = group[1] #set new origin to old destination
                        group[7] = group[2] #set new origin to old destination
                    elif self.cortez_x == group[1] and self.cortez_y == group[2]:
                        self.label_string[7] = "Your dispatched troups have returned"
                        for (i, j) in self.grid.getBetween(group[6], group[7], 0, 3):
                            self.grid.getTile(i, j).known = True
                        for n in group[8]:
                            n.known = True
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
            if count <= self.troops['spanish']:
                self.troops['spanish'] -= count
                self.dispatched.append( [count, self.cortez_x, self.cortez_y, xx, yy, True, self.cortez_x, self.cortez_y, [], self.time] )
        except:
            return
        

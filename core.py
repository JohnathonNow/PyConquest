import grid
import inputbox
import random

MOVE_INTERVAL  = 10 #number of ticks per tile it takes units to move
LOSS_INTERVAL  = 50 #number of ticks it takes for someone to die of disease
TLOS_INTERVAL  = LOSS_INTERVAL*5 #number of ticks for a troop to die
SPRD_INTERVAL  = 80 #number of ticks it takes to roll for disease spreading

SPRD_CHANCE    = 6  #1 in SPRD_CHANCE chances a disease spreads

ATCK_DICE      = 12 #1 die per ATCK_DICE troops
ATCK_DIE_SIDES = 5  #attack dice has sides 0-ATCK_DIE_SIDES

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
                                         "Tributers" : [],
                                        }
        #set up our text box text
        self.label_string = ["", "", "", "", "", "", "", "", "", ""]
        self.cortez_x, self.cortez_y = 520, 300 #cortez starting location
        #grab the grid and screen from top.py
        self.grid = g
        self.screen = s
        #define our starting troops
        self.troops = {'spanish': 500}
        #set up our list of dispatched units
        self.dispatched = []
        self.time = 0        #number of gameticks that have passed
        self.gold = 0        #cortez's amount of gold found
        self.food = 300      #cortez's food supply
        self.mode = 'select' #our current selection mode

        #define cities
        g.getTile(520, 301).city = "Tenochtitlan"
        g.getTile(520, 301).type = grid.CITY

    def run(self):
        xx = self.xt
        yy = self.yt
        self.time += 1 #increment time
        #handle displaying useful information
        if self.grid.selected:
            #this label below is probably deprecated, consider changing
            self.label_string[0] = "There are {} troops here.".format(self.grid.selected[0].units)
            #if we selected something other than a city
            if (self.grid.selected[0].type != grid.CITY):
                #tell us what it is
                self.label_string[1] = "It is {} here.".format(
                    {grid.GRASS: "grassy",
                     grid.WATER: "watery",
                     grid.ROCKS: "rocky"}[self.grid.selected[0].type])
            else:
                #otherwise, tell us about the city
                ct = self.grid.selected[0].city
                cd = self.cityData[ct]
                self.label_string[1] = ct
                self.label_string[2] = "Population: " + str(cd["Population"])
                self.label_string[3] = "Troops: " + str(cd["Troops"])
                self.label_string[4] = "Resources: " + str(cd["Resources"])
                self.label_string[5] = "Smallpox?: " + str(cd["Smallpox"])
                self.label_string[6] = "Starvation?: " + str(cd["Starvation"])
        else:
            self.label_string[0] = "You gotta select something."

        #"move" dispatched troops
        if self.time % MOVE_INTERVAL == 0:
            for group in self.dispatched:
                #check if they're back yet
                if (self.cortez_x == group[1] and 
                    self.cortez_y == group[2] and
                    self.time     >= group[5]):
                    #if so, tell us
                    self.label_string[7] = "Your dispatched men have returned"
                    #highlight their destination
                    for i, j in self.grid.getBetween(group[3], group[4], 0, 3):
                        self.grid.getTile(i, j).known = True
                    #reveal their path
                    for n in group[6]:
                        self.grid.getTile(n[0], n[1]).known = True
                    #recover troops
                    self.troops['spanish'] += group[0]
                    self.dispatched.remove(group)
        #if we're in a city, maybe spread disease
        if self.time % SPRD_INTERVAL == 0:
            tile = self.grid.getTile(self.cortez_x, self.cortez_y)
            if tile.type == grid.CITY:
                city = self.cityData[tile.city]
                if random.randint(0, SPRD_CHANCE) == 0:
                    city["Smallpox"] = "Yes"
        #lower the populations of cities if they're sick or starving
        if self.time % LOSS_INTERVAL == 0:
            for cityName in self.cityData:
                city = self.cityData[cityName]
                if city["Starvation"] != "No": 
                    city["Population"] -= 1
                    #can troops starve?
                    #if self.time % TLOS_INTERVAL == 0:
                    #    city["Troops"] -= 1
                if city["Smallpox"]   != "No": 
                    city["Population"] -= 1
                    #have troops die less often from disease
                    if self.time % TLOS_INTERVAL == 0:
                        city["Troops"] -= 1
        #troops label
        self.label_string[8] = 'Men: ' + ', '.join(['{} {}'.format(self.troops[x], x) for x in self.troops])

        #gold label
        self.label_string[9] = 'Gold: {}'.format(self.gold)
                
            
    def moveCortez(self, xx, yy):
        if self.grid.getTile(xx, yy).type not in grid.PASSABLE: return
        #we can only move on grass/city, so return if we can't go
        #hide old tiles
        for (i, j) in self.grid.getBetween(self.cortez_x, self.cortez_y, 0, 1):
            self.grid.getTile(i, j).visible = False
        #make area visible
        for (i, j) in self.grid.getBetween(xx, yy, 0, 1):
            self.grid.getTile(i, j).known = True
            self.grid.getTile(i, j).visible = True
        #perform the move
        self.cortez_x = xx
        self.cortez_y = yy

    def sendMen(self, xx, yy, count):
        try:
            #convert to number, may fail, so catch the exception
            count = int(count)
            #check that we have enough men
            if count <= self.troops['spanish'] and count > 0:
                #set the notification
                self.label_string[7] = "You dispatched {} men.".format(count)
                #lose the troops
                self.troops['spanish'] -= count
                #find a path for the men
                p = self.grid.shortestPath(self.cortez_x, self.cortez_y, xx, yy)
                #add the men to our queue
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
                if chosex == 3: #fight
                    self.fight()
                elif chosex == 2: #talk
                    self.talk()

    def fight(self):
        tile = self.grid.getTile(self.cortez_x, self.cortez_y)
        if tile.type == grid.CITY:
            city = self.cityData[tile.city]
            city_dice = int(city["Troops"] / ATCK_DICE)
            cort_dice = 0
            for i in self.troops.values():
                cort_dice += i
            cort_dice = int(cort_dice / ATCK_DICE)
            for i in range(cort_dice):
                city["Troops"] -= random.randint(0, ATCK_DIE_SIDES)
            for i in range(city_dice):
                self.troops["spanish"] -= random.randint(0, ATCK_DIE_SIDES)
        else:
            #set the notification
            self.label_string[7] = "Who are you fighting?"

    def talk(self):
        pass

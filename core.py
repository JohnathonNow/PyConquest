import grid
import inputbox
import random
import time

MOVE_INTERVAL  = 10 #number of ticks per tile it takes units to move
LOSS_INTERVAL  = 50 #number of ticks it takes for someone to die of disease
TLOS_INTERVAL  = LOSS_INTERVAL*5 #number of ticks for a troop to die
SPRD_INTERVAL  = 80 #number of ticks it takes to roll for disease spreading
WEEK_INTERVAL  = 350 #number of ticks for a "week" to pass by
DIED_FROM_JOURNEY = 10 #1 in DIED_FROM_JOURNEY deaths per space for dispatched men

SPRD_CHANCE    = 6  #1 in SPRD_CHANCE chances a disease spreads

ATCK_DICE      = 12 #1 die per ATCK_DICE troops
GOLD_DIE_SIDES = 1000 #gold dice has sides 0-GOLD_DIE_SIDES
ATCK_DIE_SIDES = 5  #attack dice has sides 0-ATCK_DIE_SIDES

class Game:
    def __init__(self, g, s):
        self.xt = 0
        self.yt = 0
        self.wait = 0
        self.DonaMaria = 0
        self.cityData = {}
        #define cities
        for (i, j) in g.getBetween(118, 298, 0, 1):
            g.getTile(i, j).type = grid.WATER
        g.getTile(118, 296).city = "Tenochtitlan"
        g.getTile(118, 296).type = grid.CITY
        self.cityData["Tenochtitlan"] = {"Population" : 1000000,
                                         "Troops" : 6000,
                                         "Resources" : 300,
                                         "Gold" : 420000,
                                         "Smallpox" : "No",
                                         "Starvation" : "No",
                                         "Tributers" : ["Tlatelolco", "Cholula"],
                                         "Trust" : 0,
                                        }
        g.getTile(118, 295).city = "Tlatelolco"
        g.getTile(118, 295).type = grid.CITY
        self.cityData["Tlatelolco"] = {"Population" : 30000,
                                         "Troops" : 200,
                                         "Resources" : 3000,
                                         "Gold" : 30000,
                                         "Smallpox" : "No",
                                         "Starvation" : "No",
                                         "Tributers" : [],
                                         "Trust" : 0,
                                        }
        g.getTile(102, 297).city = "Cholula"
        g.getTile(102, 297).type = grid.CITY
        self.cityData["Cholula"] = {"Population" : 100000,
                                         "Troops" : 120,
                                         "Resources" : 3000,
                                         "Gold" : 9000,
                                         "Smallpox" : "No",
                                         "Starvation" : "No",
                                         "Tributers" : [],
                                         "Trust" : 0,
                                         "Initial" : "You enter the massive square of Cholula where you are met by a seemingly friendly group of warriors and noblemen. Your translator tells you that they plan to attack on your way out of the city.",
                                         "IA" : 0,
                                         "Reject" : "You massacre the warriors and noblemen and burn down the city. Maybe this will send a message to Tenochtitlan.",
                                         "RA" : 5,
                                         "RK" : True
                                        }
        g.getTile(148, 300).city = "Tlaxcala"
        g.getTile(148, 300).type = grid.CITY
        self.cityData["Tlaxcala"] = {"Population" : 300000,
                                         "Troops" : 6000,
                                         "Resources" : 30000,
                                         "Gold" : 30000,
                                         "Smallpox" : "No",
                                         "Starvation" : "No",
                                         "Tributers" : [],
                                         "Trust" : 0,
                                         "Initial" : "Tlaxcala is currently engaged in a perpetual war against Tenochtitlan and the rest of the Triple Alliance. The Tlaxcalteca initially attack your party. You would have lost the battle had their war chief not been persuaded to stop fighting in favor of a strategic alliance with you.",
                                         "IA" : 100,
                                         "Reject" : "Since you rejected the alliance, the Tlaxcalteca continue to attack and completely massacre you.",
                                         "RA" : 30000,
                                         "RK" : False
                                        }
        g.getTile(153, 272).city = "Texcoco"
        g.getTile(153, 272).type = grid.CITY
        self.cityData["Texcoco"] = {"Population" : 25000,
                                        "Troops" : 2000,
                                        "Resources" : 300,
                                        "Gold" : 50000,
                                        "Smallpox" : "No",
                                        "Starvation" : "No",
                                        "Tributers" : [],
                                        "Trust" : 0,
                                        "Initial" : "Texcoco is one of the largest and most powerful cities in Acolhua with plenty of resources. It seems as though their alliance with Tenochtitlan is suffering due to Montezuma's arrogance and attempts to diminish their power. It could be a strategic location for a base of operations.",
                                        "IA" : 0,
                                        "Reject" : "Fearing you've sided with Tenochtitlan, Texcoco attacks you as you try to retreat, killing several of your men.",
                                        "RA" : 200,
                                        "RK" : False
                                        }
        g.getTile(518, 305).city = "Potonchan"
        g.getTile(518, 305).type = grid.CITY
        self.cityData["Potonchan"] = {"Population" : 200,
                                        "Troops" : 50,
                                        "Resources" : 300,
                                        "Gold" : 10000,
                                        "Smallpox" : "No",
                                        "Starvation" : "No",
                                        "Tributers" : [],
                                        "Trust" : 0
                                        }
        g.getTile(470, 291).city = "Xalapa"
        g.getTile(470, 291).type = grid.CITY
        self.cityData["Xalapa"] = {"Population" : 100,
                                        "Troops" : 50,
                                        "Resources" : 300,
                                        "Gold" : 10000,
                                        "Smallpox" : "No",
                                        "Starvation" : "No",
                                        "Tributers" : [],
                                        "Trust" : 0,
                                        "Initial" : "Xalapa has a very low population and seems very friendly towards your party. They also seem very receptive towards Christianity.",
                                        "IA" : 0,
                                        "Reject" : "You burn the small town of Xalapa to the ground. You gain nothing.",
                                        "RA" : 5,
                                        "RK" : True,
                                        "Intel" : "They tell you that you might find the city of Texcoco important in your conquest. It is located at (153, 272)."
                                        }
        g.getTile(500, 283).city = "Zempoala"
        g.getTile(500, 283).type = grid.CITY
        self.cityData["Zempoala"] = {"Population" : 25000,
                                        "Troops" : 3000,
                                        "Resources" : 5000,
                                        "Gold" : 10000,
                                        "Smallpox" : "No",
                                        "Starvation" : "No",
                                        "Tributers" : [],
                                        "Trust" : 0,
                                        "Initial" : "20 Zempoala noblemen greet you with various gifts, including gold, as you enter the city. The complain that they have been dominated by the Aztec armies for years and would like to form an alliance to take them down.",
                                        "IA" : 0,
                                        "Reject" : "By rejecting their offer for an alliance, you have given the Zempoala the impression that you are alligned with the Aztecs. They slaughter your small group of men.",
                                        "RA" : 1000,
                                        "RK" : False,
                                        "Intel" : "There is a small town called Xalapa at coordinates (470, 291). They urge you to take their finest warriors with you."
                                        }
        #set up our text box text
        self.label_string = [""] * 10
        self.cortez_x, self.cortez_y = 520, 300 #cortez starting location
        #grab the grid and screen from top.py
        self.grid = g
        self.screen = s
        #define our starting troops
        self.troops = {'spanish': 500, 'nahua' : 0}
        self.time = 0        #number of gameticks that have passed
        self.week = 1        #number of weeks that have gone by
        self.gold = 0        #cortez's amount of gold found
        self.food = 300      #cortez's food supply
        self.mode = 'select' #our current selection mode

    def run(self):
        xx = self.xt
        yy = self.yt
        inputbox.coordinates(self.screen, self.xt, self.yt)
        self.time += 1 #increment time
        #handle displaying useful information
        #show current week
        self.label_string[0] = "Week {}".format(int(self.week))
        if self.grid.selected:
            #if we selected something other than a city
            if (self.grid.selected[0].type != grid.CITY):
                #tell us what it is
                self.label_string = [""] * 10
                self.label_string[0] = "Week {}".format(int(self.week))
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
                self.label_string[4] = "Resources: " + str(cd["Resources"]) + " Gold: " + str(cd["Gold"])
                self.label_string[5] = "Smallpox?: " + str(cd["Smallpox"])
                self.label_string[6] = "Starvation?: " + str(cd["Starvation"])

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
                    if city["Population"] > 0: 
                        city["Population"] -= 1
                    #have troops die less often from disease
                    if self.time % TLOS_INTERVAL == 0:
                        if city["Troops"] > 0:
                            city["Troops"] -= 1
        #troops label
        self.label_string[8] = 'Men: ' + ', '.join(['{} {}'.format(self.troops[x], x) for x in self.troops])

        #gold label
        self.label_string[9] = 'Gold: {}'.format(self.gold)
                
            
    def moveCortez(self, xx, yy):
        #self.label_string = []
        if self.grid.getTile(xx, yy).type not in grid.PASSABLE: return
        #we can only move on grass/city, so return if we can't go
        #hide old tiles
        for (i, j) in self.grid.getBetween(self.cortez_x, self.cortez_y, 0, 1):
            self.grid.getTile(i, j).visible = False
        #make area visible
        for (i, j) in self.grid.getBetween(xx, yy, 0, 1):
            self.grid.getTile(i, j).known = True
            self.grid.getTile(i, j).visible = True
        #calculate the elapsed time
        dt = self.grid.hexDistance(xx, yy, self.cortez_x, self.cortez_y)*MOVE_INTERVAL/WEEK_INTERVAL
        self.week += dt
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
                #calculate the elapsed time
                dt = len(p)*MOVE_INTERVAL/WEEK_INTERVAL
                self.week += dt
                #calculate how many men died
                death = int(len(p)*random.random()/DIED_FROM_JOURNEY)
                if death < count:
                    self.label_string[7] = "After {} days, {} dispatched men return.".format(int(7*dt), int(count - death))
                    #highlight their destination
                    for i, j in self.grid.getBetween(xx, yy, 0, 3):
                        self.grid.getTile(i, j).known = True
                    #reveal their path
                    for n in p:
                        self.grid.getTile(n[0], n[1]).known = True
                    #recover troops
                    self.troops['spanish'] += int(count - death)
                else:
                    self.label_string[7] = "You wait for {} days, but no men returned.".format(int(7*dt))
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
            print((xxt, yyt))
            #inputbox.coordinates(screen, xxt, yyt)
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
                #roll for attack
                city["Troops"] -= random.randint(0, ATCK_DIE_SIDES)
                if city["Troops"] <= 0:
                    city["Troops"] = 0
                    city["Population"] -= random.randint(0, ATCK_DIE_SIDES*1000)
                    if city["Population"] < 0:
                        city["Population"] = 0
                        if tile.city == "Potonchan":
                            if self.DonaMaria == 0:
                                self.DonaMaria = 1
                                #print("hi")
                                inputbox.message_box(self.screen, "In victory you acquired 20 slaves. One of these slaves seems as though she can translate for you. You can now use her as a translator to communicate with cities. If you trust her, that is.")
                #roll for stolen gold
                stolen = random.randint(0, GOLD_DIE_SIDES)
                #can't steal more than they have
                if city["Gold"] < stolen: stolen = city["Gold"]
                #take it!
                city["Gold"] -= stolen
                self.gold += stolen
            for i in range(city_dice):
                #roll for getting attacked
                self.troops["spanish"] -= random.randint(0, ATCK_DIE_SIDES)
                if self.troops["spanish"] < 0:
                    self.troops["spanish"] = 0 #GAME OVER
        else:
            #set the notification
            self.label_string[7] = "Who are you fighting?"

    def talk(self):
        tile = self.grid.getTile(self.cortez_x, self.cortez_y)
        if tile.type == grid.CITY:
            city = self.cityData[tile.city]
            if self.DonaMaria == 1:
                if city["Trust"] == 0:
                    inputbox.message_box(self.screen, city["Initial"])
                    if self.troops["nahua"] > 0:
                        self.troops["nahua"] -= city["IA"]
                        if self.troops["nahua"] < 0:
                            self.troops["spanish"] += self.troops["nahua"]
                            self.troops["nahua"] = 0
                    else:
                        self.troops["spanish"] -= city["IA"]
                    self.week += 15/7
                    c = "~"
                    while c[0] not in "yn":
                        c = inputbox.ask(self.screen, 'Ally with ' + tile.city + '? (yes or no)')
                        if c[0] in "y":
                            self.troops["nahua"] = self.troops['nahua'] + city["Troops"]
                            city["Troops"] = 0
                            city["Trust"] = 1
                            self.label_string[7] = tile.city + " agrees to an alliance with you."
                        else:
                            city["Trust"] = -1
                            inputbox.message_box(self.screen, city["Reject"])
                            if self.troops["nahua"] > 0:
                                self.troops["nahua"] -= city["IA"]
                                if self.troops["nahua"] < 0:
                                    self.troops["spanish"] += self.troops["nahua"]
                                    self.troops["nahua"] = 0
                            else:
                                self.troops["spanish"] -= city["IA"]
                            if city["RK"]:
                                city["Troops"] = 0
                                city["Population"] = 0
                    #city["Trust"] = 1
                elif city["Trust"] > 0:
                    if "Intel" in city.keys():
                        input.message_box(self.screen, city["Intel"])
                elif city["Trust"] < 0:
                    self.fight()
            else:
                inputbox.message_box(self.screen, "You cannot effectively communicate with cites because you do not know the language. Perhaps a translator would help...")
        else:
            #set the notification
            self.label_string[7] = "Talking to yourself will get you nowhere."

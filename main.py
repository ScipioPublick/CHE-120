#Matthew D Jessup

#Imports pygame and the exit command. The Pygame module is required for almost all functions used and the exit will allow me to stop the script.
import pygame
from sys import exit

#Initiates pygame to be used.
pygame.init()

#Import assets- this section is just for importing assets (png picture files), to be later put on the display screen. They contain the backdrops, player sprites and currency symbols

#Doctor sprites

doctor1 = pygame.image.load('sprites/doctor1.png')
doctor2 = pygame.image.load('sprites/doctor2.png')

#UI sprites

pulse_symbol = pygame.image.load('sprites/pulse_big.png')
upgrade_tray = pygame.image.load('sprites/Backdrops/upgrade_tray.png')
equipment_clipboard = pygame.image.load('sprites/Backdrops/equipment_clipboard.png')
backdrop = pygame.image.load('sprites/Backdrops/backdrop.png')
dialog_box = pygame.image.load('sprites/dialog_box.png')

cpr_button = pygame.image.load('sprites/Buttons/cpr_button.png')
adrenaline_button = pygame.image.load('sprites/Buttons/adrenaline_button.png')
defibrillator_button = pygame.image.load('sprites/Buttons/defibrillator_button.png')
crystal_button = pygame.image.load('sprites/Buttons/crystal_button.png')
necro_button = pygame.image.load('sprites/Buttons/necro_button.png')

#Dialog box images

cpr_manual = pygame.image.load('sprites/Equipment/cpr_manual.png')
adrenaline = pygame.image.load('sprites/Equipment/adrenaline.png')
defibrillator = pygame.image.load('sprites/Equipment/defibrillator.png')
crystal = pygame.image.load('sprites/Equipment/crystal.png')
necronomicon = pygame.image.load('sprites/Equipment/necronomicon.png')
prescription = pygame.image.load('sprites/upgrades/prescription.png')

#Upgrade sprites

tongue_depressors = pygame.image.load('sprites/upgrades/tongue_depressors.png')
golden_stethescope = pygame.image.load('sprites/upgrades/golden_stethescope.png') 
longer_needles = pygame.image.load('sprites/upgrades/longer_needles.png')
midichlorians = pygame.image.load('sprites/upgrades/midichlorians.png')
car_battery = pygame.image.load('sprites/upgrades/car_battery.png')
lightning_rod = pygame.image.load('sprites/upgrades/lightning_rod.png')
goat_yoga = pygame.image.load('sprites/upgrades/goat_yoga.png')
bleach_therapy = pygame.image.load('sprites/upgrades/bleach_therapy.png')
ouija_board = pygame.image.load('sprites/upgrades/ouija_board.png')
demon_goat = pygame.image.load('sprites/upgrades/demon_goat.png')

#this section is to define classes. I found trying to make this game without classes was a nightmare making sure certain functions or images initiated in the proper order. 
#Classes cleaned this up quite a bit. I probably overused classes here.

#This class is for the doctor (player), it defines his x and y coordinate (def_init_), the size of the sprite and an animation state so his hands move when you click him. 
#If the animation state is greater than 0 (is clicked, adds a 1 to animation state), his sprite changes for a brief second and the animation state is reduced back to 0.
#Finally, this class also has the collideppoint, that is defining where you can click to trigger the doctors effects.

class Doctor:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.length = 268
        self.height = 496
        
        self.animation_state = 0
    def draw(self):
        if self.animation_state > 0:
            window.blit(doctor2, (doctor2.get_rect(center = (int(self.x + self.length/2), int(self.y + self.height/2))  )))
            self.animation_state -= 1
        else:
            window.blit(doctor1, (doctor1.get_rect(center = (int(self.x + self.length/2), int(self.y + self.height/2))  )))
    def collidepoint(self, point):
        return pygame.Rect(self.x, self.y, self.length, self.height).collidepoint(point)

#This is a silly class I made at the very beginning, it just defines a pulse symbol's size and then places it on the display screen. Could have easily just been placed on the display screen 
#without a class. I Kept it to remind me classes need a purpose that makes the code better.

class Pulse:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.length = 64
        self.height = 64
    def draw(self):
        window.blit(pulse_symbol, (pulse_symbol.get_rect(center = (int(self.x + self.length/2), int(self.y + self.height/2))  )))
 
#This class is for displaying the players score. It defines the the specific font to use, renders the font, defines what the font should say 
#(in this instance {} is used to change what is written dynamically with the format call) Finally it places the text on the display screen.

class Player_Score:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.length = 100
        self.height = 100
        self.score = 0
                
    def draw(self, score, user_pps):
        font = pygame.font.Font('Font/8bit.otf', 32)
        small_font = pygame.font.Font('Font/8bit.otf', 24)
        
        text = font.render('{} pulses'.format(str( score_format(score) )), True, WHITE)
        pps = small_font.render('per second: {}'.format(str( score_format(user_pps))), True, WHITE)
        window.blit( text, (  text.get_rect(center=(int(self.x + self.length / 2), int(self.y + self.height / 2)))  ) )
        window.blit( pps, (  pps.get_rect(center=(int(self.x + self.length / 2), int(self.y + self.height / 2) + 24))  ) )

#this class is quite a bit larger and would be used a lot more with other functions so I made sure all inputs were defined easily to be used later without hassle. It is used for the equipment the doctor 
#uses to save a patient is is an important element of the game.the __init__ defines the x, y, length and height per usual. It also defines the name, image, icon, how many have been purchased (quantity)
# and pulses per minute (pps). Then it defines the collidepoint, a function called cost_next that determines the cost of the next equipment, then draws the equipment purchase buttons. I also made the 
#buttons transparent when you cannot afford one using set_alpha. Finally it has some synamic text that is placed on top of the button to show the cost to buy and how many have been purchased. 
# Now for the dialog box, the dialog box it there to give extra information about the equipment and is activated when the mouse collides with the collidepoint. A dialog boy is drawn above the buttons 
#and more dynamic text is layered on top. Finally, it defines the add_upgrades function that generates upgrades if enough equipment have been purchased. It says if you have a certain number of each 
#equipment, to make a certain upgrade for that number. the numbers are 25 and 50, but queries for 24 and 49 because it updates when you purchase your 25th and 5th.

class Equipment:
    def __init__(self, name, x, y, image, png, base_cost, cost_coefficient, pps):
        self.x = x
        self.y = y
        self.length = 384
        self.height = 86
        self.name = name
        self.image = image
        self.png = png
        self.quantity = 0
        self.base_cost = base_cost
        self.cost_coefficient = cost_coefficient
        self.pps = pps

    def collidepoint(self, point):
        return pygame.Rect(self.x, self.y, self.length, self.height).collidepoint(point)
    def Cost_Next(self):
        return int(self.base_cost * self.cost_coefficient**(self.quantity))
    
    def draw(self, solid=True):
        
        equipment_cost_font = pygame.font.Font('Font/8bit.otf', 20)
        equipment_amount_font = pygame.font.Font('Font/8bit.otf', 42)
        
        png = self.image
        cost = equipment_cost_font.render('{}'.format( score_format(self.Cost_Next()) ), True, BLACK)
        quantity = equipment_amount_font.render('{}'.format(self.quantity), True, BLACK)
        if solid == False:    
            png.set_alpha(100)
        else:
            png.set_alpha(255)
        window.blit(png, (self.x , self.y))
        window.blit(cost, (self.x + 117, self.y + self.height - 35))
        window.blit(quantity, (self.x + self.length - 55, self.y + 36))

    def Draw_Dialogue_Box(self):
        equipment_font = pygame.font.Font('Font/8bit.otf', 36)
        equipment_name = equipment_font.render('{}'.format(self.name), True, BLACK)
        
        description_font = pygame.font.Font('Font/8bit.otf', 17)
        production = description_font.render('Each {} generates {:.1f} pulses per second'.format(self.name, self.pps), True, BLACK)
        quantity = description_font.render('You have {} {}s generating {:.1f} pulses per second'.format(self.quantity, self.name, self.pps * self.quantity), True, BLACK)
        
        x_pos = 577
        y_pos = 77
        
        window.blit(dialog_box, (x_pos, y_pos))
        window.blit(self.png, (x_pos + 4, y_pos + 4))
        window.blit(equipment_name, (x_pos + 69, y_pos + 3))
        
        '''Description'''
        line_spacing = 20
        window.blit(production, (x_pos + 8, y_pos + 70))
        window.blit(quantity, (x_pos + 8, y_pos + 70 + line_spacing*1))
        
    def Add_Upgrades(self):
        stage_1 = 24
        stage_2 = 49
        if self.name == 'CPR Manual':
            if self.quantity == stage_1:
                list_of_upgrades.append(Upgrade('Tongue Depressors', cost=self.Cost_Next()*100, upgrade=self.name))
            elif self.quantity == stage_2:
                list_of_upgrades.append(Upgrade('Golden Stethescope', cost=self.Cost_Next()*1000, upgrade=self.name))
        elif self.name == 'Adrenaline':
            if self.quantity == stage_1:
                list_of_upgrades.append(Upgrade('Midichlorians', cost=self.Cost_Next()*100, upgrade=self.name))
            elif self.quantity == stage_2:
                list_of_upgrades.append(Upgrade('Longer Needles', cost=self.Cost_Next()*2000, upgrade=self.name))               
        elif self.name == 'Defibrillator':
            if self.quantity == stage_1:
                list_of_upgrades.append(Upgrade('Car Battery', cost=self.Cost_Next()*100, upgrade=self.name))
            elif self.quantity == stage_2:
                list_of_upgrades.append(Upgrade('Lightning Rod', cost=self.Cost_Next()*1000, upgrade=self.name))
        elif self.name == 'Healing Crystal':
            if self.quantity == stage_1:
                list_of_upgrades.append(Upgrade('Goat Yoga', cost=self.Cost_Next()*100, upgrade=self.name))
            elif self.quantity == stage_2:
                list_of_upgrades.append(Upgrade('Bleach Therapy', cost=self.Cost_Next()*1000, upgrade=self.name))
        elif self.name == 'Necronomicon':
            if self.quantity == stage_1:
                list_of_upgrades.append(Upgrade('Demon Goat', cost=self.Cost_Next()*100, upgrade=self.name))
            elif self.quantity == stage_2:
                list_of_upgrades.append(Upgrade('Ouija Board', cost=self.Cost_Next()*1000, upgrade=self.name))

#This is the upgrade class. When you buy enough equipment, there are two upgrades for each equipment type. we start by defining the function __init__ that gives values to upgrade name, cost, 
#the png size and where it will be placed on the display screen. It then checks how many of each equipment you have to make sure the proper image is joined with the upgrade name 
#(level 1 upgrades are at 24, then it switches to the 2nd tier upgrade). Then we define the collidepoint so you cxan hover over the upgrade and click on them to purchase.
#The next function is draw and it draws the upgrades in the display screen. First it needs to layer the upgrade on a prescription pad. Then theres a fucntion that creates a dialog box that 
#pops up when you hover over an upgrade for some more info, very similar to the equipment dialog box. The last function sets the multiplier the upgrade increases the equipments pps for. 
#Just an if statement with following elifs for each equipment type.
                
class Upgrade:
    def __init__(self, name, cost, upgrade):
        self.name = name
        self.cost = cost
        self.x = 700
        self.y = 16
        self.length = 72
        self.height = 72
        self.upgrade = upgrade
        
        if upgrade == 'CPR Manual':
            if equipment.quantity == 24:
                self.image = tongue_depressors
            else:
                self.image = golden_stethescope
        elif upgrade == 'Adrenaline':
            if equipment.quantity == 24:
                self.image = longer_needles
            else:
                self.image = midichlorians
        elif upgrade == 'Defibrillator':
            if equipment.quantity == 24:
                self.image = car_battery
            else:
                self.image = lightning_rod
        elif upgrade == 'Healing Crystal':
            if equipment.quantity == 24:
                self.image = goat_yoga
            else:
                self.image = bleach_therapy
        elif upgrade == 'Necronomicon':
            if equipment.quantity == 24:
                self.image = ouija_board
            else:
                self.image = demon_goat
            
    def collidepoint(self, point):
        return pygame.Rect(self.x, self.y, self.length, self.height).collidepoint(point)
    
    def draw(self, solid=True):
        png = self.image
        frame = prescription
        if solid == False:    
            png.set_alpha(100)
            frame.set_alpha(100)
        else:
            png.set_alpha(255)
            frame.set_alpha(255)
        window.blit(frame, (self.x, self.y))
        window.blit(png, (png.get_rect(center=(int(self.x + self.length / 2), int(self.y + self.height / 2 + 4)))))
    
    def Draw_Dialogue_Box(self):
        upgrade_font = pygame.font.Font('Font/8bit.otf', 36)
        upgrade_title = upgrade_font.render('{}'.format(self.name), True, BLACK)
        
        cost_font = pygame.font.Font('Font/8bit.otf', 17)
        cost = cost_font.render('Pulse Required: {}'.format( score_format(self.cost) ), True, BLACK)
        
        description_font = pygame.font.Font('Font/8bit.otf', 17)
        description = description_font.render('{}s are much more effective.'.format(self.upgrade), True, BLACK)
        
        x_pos = 80
        y_pos = 375
        
        window.blit(dialog_box, (x_pos, y_pos))
        window.blit(self.image, (x_pos + 4, y_pos + 4))
        window.blit(upgrade_title, (x_pos + 69, y_pos + 3))
        window.blit(cost, (x_pos + 8, y_pos + 70))
        line_spacing = 20
        window.blit(description, (x_pos + 8, y_pos + 70 + line_spacing))
        
    def Equipment_Multiplier(self, equipment_list):
        if self.upgrade == 'CPR Manual':
            cpr_manual.pps *= 2.5
        elif self.upgrade == 'Adrenaline':
            adrenaline.pps *= 7.5
        elif self.upgrade == 'Defibrillator':
            defibrillator.pps *= 6
        elif self.upgrade == 'Healing Crystal':
            healing_crystal.pps *= 2
        elif self.upgrade == 'Necronomicon':
            necronomicon.pps *= 1.75

#This class is for everything relates to the users score and was the first class I created. It defines the score and the total pps. It then defines how to calculate the total pps which is 
#a linear function using the total pps + equipment pps * equipment quantity.
            
class Player:
    def __init__(self):
        self.score = 0
        self.total_pps = 0
    def PPS_Calc(self, equipment_list):
        self.total_pps = 0
        for equipment in equipment_list:
            self.total_pps += equipment.pps * equipment.quantity

#Formats the score so if you have millions or billions the number is more legible.
       
def score_format(n):
    if int(n) <= 1000000:
        n = str(round(n,2))
    elif int(n) >= 1000000000:
        if (n / 1000000000 )% 1 == 0:
            n = '{:.2f} bil'.format(n / 1000000000)
        else:
            n = '{:.2f} bil'.format(n / 1000000000)
    elif n >= 1000000:
        if (n / 1000000) % 1 == 0:
            n = '{:.2f} mil'.format(n / 1000000) 
        else:
            n = '{:.2f} mil'.format(n / 1000000)
    return n


#Defines what should be drawn and where as well as if what is drown should be transparent or not. The part at the end is a method I found from a youtube to blit images next to one another and 
#in a square pattern. Finally it also draws the dialog boxes if there is a collision with the corresponding button.
def draw():
    window.blit(backdrop, (0, 0))
    window.blit(equipment_clipboard, (550, 0))
    pulse.draw()
    pulse_score.draw(user.score, user.total_pps)
    pulse_obj.draw()
    window.blit(upgrade_tray, (0, 500))
    
    for equipment in equipment_list:
        if user.score >= equipment.Cost_Next():
            equipment.draw(solid=True)
        else:
            equipment.draw(solid=False)
        user.score += 4.52 * equipment.quantity * equipment.pps * .01
        if equipment.collidepoint(pygame.mouse.get_pos()):
            equipment.Draw_Dialogue_Box()

    for i in range(0, len(list_of_upgrades)):
        upgrade = list_of_upgrades[i]
        upgrade.x = upgrades_x + (i % 6) *72
        upgrade.y = upgrades_y + (i // 6) * 72
        if user.score >= upgrade.cost:
            upgrade.draw(solid=True)
        else:
            upgrade.draw(solid=False)
        if upgrade.collidepoint(pygame.mouse.get_pos()):
            upgrade.Draw_Dialogue_Box()

#This section is for initiating aspects of the classes and gamestates before the while loop.

#First we define the clock name to be used later to keep the framerate stable. This will keep the score from increasing too fast or slow on different machines.
#Then we rename the doctor class to an easier name to reference (I removed the bit that required this). Most class and some functions I would rename as they seemed to read better and work better with 
#the ."function" methods. It also gave a good time to define x and y coords. We redefine and set the coords for the score board and the pulse symbol above the score. We define the x and y coords for  
#where the upgrades get drawn and update the list of upgrades. As upgrades are purchased they are removed from the list and the list is updated so they are not drawn (so you can't buy them twice). 
#The equipment needs a y coord set. I set it here so I could change it to make it look good without having to mess about with the class. At first I didn't want to mess with my class's once I had them working.
clock = pygame.time.Clock() 
pulse = Doctor(163, 4)
pulse_score = Player_Score(230, 6)
pulse_obj = Pulse(243,-8)
upgrades_x = 50
upgrades_y = 540
list_of_upgrades = []
equipment_y = 212

#This defined exactly what each equipment type was. Gave it a reference name, and defined the string name, x coord, the y coord (each had to be placed below the other by 100 pixels), 
#their png image to draw, their symbol for the dialog box, base pulse cost, and the cost for the next equipment's coeeficient. At the end of each we have the pps each equipment gives the player.
cpr_manual = Equipment('CPR Manual', 585, equipment_y, cpr_button, cpr_manual, base_cost = 3.75, cost_coefficient = 1.07, pps=100)
adrenaline = Equipment('Adrenaline', 585, equipment_y + 100*1, adrenaline_button, adrenaline, base_cost=60, cost_coefficient=1.15, pps=20)
defibrillator = Equipment('Defibrillator', 585, equipment_y + 100*2, defibrillator_button, defibrillator, base_cost=720, cost_coefficient=1.14, pps=90)
healing_crystal = Equipment('Healing Crystal', 585, equipment_y + 100*3, crystal_button, crystal, base_cost=8640, cost_coefficient=1.13, pps=360)
necronomicon = Equipment('Necronomicon', 585, equipment_y + 100*4, necro_button, necronomicon, base_cost=103680, cost_coefficient=1.12, pps=2160)


#We need to have an equipment list so we can draw all the equipment files, define upgrades for types of equipment and to allow collisions.
equipment_list = [cpr_manual, adrenaline, defibrillator, healing_crystal, necronomicon]

#Redefine the player() class to work better with ."functions"
user = Player()

#Gives the display screen the name of the game to print at the top.
pygame.display.set_caption("Spaghetti Code Blue")


#Defines the size of the display screen
window_length = 1000
window_height = 800

#Gives values for colours so its less work defining font colours.
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#Defines the display screen as a window for more readability and defines the size for easier testing and fitting the sprites.
window = pygame.display.set_mode((window_length, window_height))

#These two statements and the while loop actually run the game. Everything that happens in the game are within this while loop. After a game cycle happens things are redefined and run within the 
#while loop. The game would simply not run without this as there would be no iterative changes.

main = True
while main == True:
    
#Going to be honest, I'm not entirely sure why pygame.time.delay(10) is actually doing. I added it hoping to delay the animation state changes so they weren't so rapid. It didn't work, 
#however it really helped with the score increases matching real time. Without this the score increases much faster than it should, or maybe not, I just kind of eyeballed it. That's why 
#I put a coefficient in the score increase calculation and used a stop watch to determine a good coefficient. All of that was after I put the delay so I just left it as it looks like it slows it 
#down a bit.

    pygame.time.delay(10)
    
#Literally means whenever an event that pygame recognizes happens (do this). This is a setup to allow buttons to be pressed without having to have pygame constantly searching for events. Instead the 
#event informs the game a new action has to be taken.

    for event in pygame.event.get():
        
        #pygame.mixer.music.load('sounds\8-bit.wav') fix this or remove
        #pygame.mixer.music.play(0)

#pygame has a method for allowing the user to close the display screen. I made the mistake of running a display screen without pygame.quit() in the code and led to a control - alt -delete moment.
#this says that if the event pygame.quit occurs (pressing the x on the display screen), to then define main as false and that ends the while loop, allowing the final pygame.quit() call to occur.

        if event.type == pygame.QUIT:
            main = False
#this says if you click a mousebutton down, the mouse position will be recorded for collidepoints to go off. This allows the next three events to occur through user inputs.
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos

# This lets you click on the doctor and increase your pulses by 1 and changes the animationstate from 0 to 1 to trigger an animation change. Its fun, try it!

            if pulse.collidepoint(mouse_pos):
                user.score += 1
                pulse.animation_state = 1
                
# This allows the user to buy equipment if the mouse is colidding with the equipment button rectangle and the user has enough pulses. It then updates the upgrades if you bought enough equipment 
#to unlock them, removes the buolding cost from your score and updates your pps so your score increses by the appropriate amount.

            for equipment in equipment_list:
                if equipment.collidepoint(mouse_pos) and user.score >= equipment.Cost_Next():
                    equipment.Add_Upgrades()
                    user.score -= equipment.Cost_Next()
                    equipment.quantity += 1
                    user.PPS_Calc(equipment_list)
                    
#These are similar for the equipment points above. It checks if your mouse is coliding from a rectangle of an upgrade in the list of upgrades and checks if you have enough pulses to buy them. 
#If you do, it removes the cost from your score, removes the upgrade from the list of upgrades (so you can't buy it twice), improves the pps of the equipment related to the upgrade and updates total pps.  
            for upgrade in list_of_upgrades:
                if upgrade.collidepoint(mouse_pos) and user.score >= upgrade.cost:
                    user.score -= upgrade.cost
                    upgrade.Equipment_Multiplier(equipment_list)
                    list_of_upgrades.remove(upgrade)
                    user.PPS_Calc(equipment_list)
#This sets the clocks tickrate at 60 fps as stated earlier.
    clock.tick(60)

#when the while loop is running this draws all the window.blit images into the display screen. There's also a display update to refresh everything. TBH I'm not 100% clear, but a few people from youtube 
#said is was necessary.edit: Just hashed it out and, yep, it leads to a black screen, I take it it actually makes the images appear on the display screen, whereas draw just initiates the drawing of 
#the rectangles/surfaces.
    draw()
    pygame.display.update()

#closes down display screen and pygame module.
pygame.quit()

#initializes python system exit command to shut down the script.
exit()

# Bibliography/Credits:
# https://www.youtube.com/channel/UCznj32AM2r98hZfTxrRo9bQ : channel Clear Code has pygame tutorial. This was my main source of learning how to code in pygame, specifically his video "The Ultimate Introduction to Pygame" and "Creating a Mario Style Platformer in Python with Pygame (with Pirates)"
# https://www.youtube.com/channel/UCBOFnvulaF5hQnosSPJvKVg : channel Sup Man has pygame tutorials. I watched pretty much his entire channel and picked up how to use classes and his syntax rules/function formatting. He also has a "Coding Cookie Clicker in Python in 6 Minutes".
# Cookie Clicker: the basis of this game is a style of games called clicker games, popularized by cookie clicker. Much was inspired by this game. It is a terrific game to try to create as its very UI based but simple. A good beginning to interfaces for a language.
# Adventure Capitalist: Another clicker game that I have played more so than cookie clicker. It's pretty much the same deal but I borrowed from their design philosophy for clicker/exponential games.
# "SH Pinscher Font Free by Design Sayshu" was the font I used, found at: https://www.fontsquirrel.com/fonts/sh-pinscher
# All assets were created by me using Asprite. The doctor was influenced by works found at "https://www.artstation.com/pixelbradii"
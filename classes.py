# Define necessary classes and functions, plus some useful constants
# Also initiate pygame, screen and suchlike

# ====
# Import libraries
# ====

import pygame
from numpy import random


# ====
# Define necessary classes
# ====

# Tardis class
# Only really useful for one thing at the moment, but will need to be fiddled
# with when other Tardises are needed.
class Tardis(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(im_dir+"tardis2010a.bmp")
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (tile*12, tile*10)
        self.base = pygame.Rect(self.rect.left, self.rect.bottom-(tile*2), tile*2, tile*2)
        self.sound = pygame.mixer.Sound(sound_dir+"Tardis.wav")
        self.sound.set_volume(0.2)
        self.menu = Menu()
        self.menu.add_option("TARDIS workshop")
        self.menu.add_option("Pallet Town")
    # Function to open the door when the Doctor stands on the threshold
    def open_door(self):
        self.image = pygame.image.load(im_dir+"tardis2010b.bmp")
        pos = self.rect.bottomleft
        self.rect = self.image.get_rect()
        self.rect.bottomleft = pos
    # Function to close the door
    def close_door(self):
        self.image = pygame.image.load(im_dir+"tardis2010a.bmp")
        pos = self.rect.bottomleft
        self.rect = self.image.get_rect()
        self.rect.bottomleft = pos
    # Function to move self.rect and self.base to a new position
    def move(self, new_position):
        self.rect = self.rect.move(new_position)
        self.base = self.base.move(new_position)

# Character class
# Again, will probably need fleshing out when I want more than one character
class Character(pygame.sprite.Sprite):
    def __init__(self, name, char_im, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.im_base = char_im
        self.face_direction("down", x, y)
        self.base = pygame.Rect(self.rect.left, self.rect.bottom-tile, tile, tile)
        self.health = [0, 0]
        self.conviction = 0
        self.attributes = {"Strength": 0, "Defense": 0,
                           "Agility": 0, "Accuracy": 0}
        self.skills = {"Intellect": 0, "Counter-argument": 0,
                       "Stubbornness": 0, "Charisma": 0}
    # Function for turning character to face new direction. Loads new image and 
    # redefines rectangle.
    def face_direction(self, direction, x=None, y=None):
        if x == None and y ==None:
            corner=self.rect.bottomleft
            x, y = corner[0], corner[1]
        self.image = pygame.image.load(im_dir+self.im_base+direction+".bmp")
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x, y)
    # Function to move self.rect and self.base to a new position
    def move(self, new_position):
        self.rect = self.rect.move(new_position)
        self.base = self.base.move(new_position)
    # Function for drawing health bar to screen during fights.
    def draw_health_bar(self):
        self.bar = pygame.Surface((tile, tile/4))
        red = (255, 0, 0)
        green = (0, 255, 0)
        health_left = (self.health[0]/self.health[1])*tile
        self.bar.fill(red)
        self.bar.fill(green, (0, 0, health_left, tile/4))
        self.bar_rect = self.bar.get_rect()
        self.bar_rect.left = self.rect.left
        self.bar_rect.bottom = self.rect.top - (tile/2)
        screen.blit(self.bar, self.bar_rect)
        pygame.display.update(self.bar_rect)

# Background class
# Defines the background map to be used - shouldn't need much changing
class Background(pygame.Surface):
    def __init__(self, image):
        self.image = pygame.image.load(im_dir+image)
        self.rect = self.image.get_rect()
        self.background = pygame.Surface(self.rect.size)
        self.background.blit(self.image, self.rect)
        self.objects = []
    # Function to move to a new position
    def move(self, new_position):
        self.rect = self.rect.move(new_position)

# Menu class
# Should be ok but might need to be tweaked for sub-menus
class Menu(pygame.Surface):
    def __init__(self):
        self.surf = pygame.Surface((tile*8, tile*7))
        self.rect = self.surf.fill((0, 0, 255))
        self.rect.center = screen.get_rect().center
        self.options = []
        self.opt_rects = []
        self.option_texts = []
        self.max_opts = 0
        self.type = "normal menu"
    def add_option(self,optiontext):
        self.max_opts += 1
        self.option_texts.append(optiontext)
        font = pygame.font.Font(None, 24)
        option = font.render(optiontext, 1, (255, 255, 255))
        self.options.append(option)
        self.rect = self.surf.fill((0, 0, 255))
        self.rect.center = screen.get_rect().center
        for o, opt in enumerate(self.options):
            optpos = opt.get_rect(centerx=self.surf.get_width()/2, centery=(self.surf.get_height()/(self.max_opts+1.5))*(o+1))
        self.opt_rects.append(optpos)
        for o, opt in enumerate(self.options):
            self.surf.blit(opt, self.opt_rects[o])

# FightMenu class
# Defines the menu shown at the bottom of the screen during fights
class FightMenu(pygame.Surface):
    def __init__(self):
        self.surf = pygame.Surface((tile*10, tile*2))
        self.rect = self.surf.fill((0, 0, 255))
        self.rect.bottomleft = screen.get_rect().bottomleft
        self.options = []
        self.opt_rects = []
        self.option_texts = []
        self.max_opts = 0
        self.type = "fight menu"
    def add_option(self,optiontext):
        self.max_opts += 1
        self.option_texts.append(optiontext)
        font = pygame.font.Font(None, 14)
        option = font.render(optiontext, 1, (255, 255, 255))
        self.options.append(option)
        self.rect = self.surf.fill((0, 0, 255))
        self.rect.bottomleft = screen.get_rect().bottomleft
        for o, opt in enumerate(self.options):
            optpos = opt.get_rect(left=self.surf.get_rect().left+(tile*1.5), bottom=(o+1)*(tile/2))
        self.opt_rects.append(optpos)
        for o, opt in enumerate(self.options):
            self.surf.blit(opt, self.opt_rects[o])


# ====
# Define useful functions
# ====

# Transport function
# Called on entering the Tardis. Gives the player the option to travel elsewhere
def transport():
    tardis.sound.play()
    pygame.time.delay(400)
    m, selection = show_menu(tardis.menu)
    if m == -1:
        return m
    destination = places[m]
    backgr_map = Background(destination)
    backgr_map.objects.append(tardis)
    if destination == "pallet.bmp":
        backgr_map.rect.x, backgr_map.rect.y = -tile*7, tile*2
        dalek1 = init_dalek("drone", -3*tile, 11*tile)
        dalek1.face_direction("right")
        bloke = init_bloke(3*tile, 18*tile)
        backgr_map.objects.append(dalek1)
        backgr_map.objects.append(bloke)
    elif destination == "floor.bmp":
        from numpy import array
        bg_size = array(backgr_map.rect.size)
        bg_size[0] *= -1
        bg_size[1] *= -1
        location = []
        location.append(random.randint((bg_size[0]/tile)+6, 3)*tile)
        location.append(random.randint((bg_size[1]/tile)+5, 3)*tile)
        backgr_map.rect.x, backgr_map.rect.y = location
    tardis.rect.bottomright = doctor.base.topright
    tardis.base.bottomright = doctor.base.topright
    doctor.face_direction("down")
    return backgr_map

# Show menu function
# Presents the player with appropriate (pre-set) options and returns their choice
def show_menu(menu, doctor=None, opponent=None, fight=None):
    icon = pygame.image.load(im_dir+"tardis2010small.bmp")
    icon_r = icon.get_rect()
    selected = 0
    while 2:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return selected, menu.option_texts[selected]
                elif event.key == pygame.K_DOWN:
                    selected += 1
                elif event.key == pygame.K_UP:
                    selected -= 1
                elif event.key == pygame.K_BACKSPACE:
                    return -1, None
        if selected > menu.max_opts-1:
            selected = 0
        elif selected < 0:
            selected = menu.max_opts-1
        if menu.type == "normal menu":
            icon_r.centery = menu.opt_rects[selected].centery+tile
            icon_r.left = menu.opt_rects[selected].left
        else:
            icon_r.centery = menu.opt_rects[selected].centery+tile*7
            icon_r.left = menu.opt_rects[selected].left-tile
        if opponent != None:
            if fight == "fight":
                doctor.draw_health_bar()
                opponent.draw_health_bar()
            else:
                draw_conviction_bar(doctor, opponent)
        screen.blit(menu.surf, menu.rect)
        screen.blit(icon, icon_r)
        pygame.display.update(menu.rect)

# Update screen function
def update_screen(backgr, doctor):
    black = 0, 0, 0
    # Sort all objects into those above the Doctor and everything else
    above, below = [], []
    for obj in backgr.objects:
        if obj.rect.bottom < doctor.rect.bottom:
            above.append(obj)
        else:
            below.append(obj)
    screen.fill(black)
    screen.blit(backgr.image, backgr.rect)
    # Blit the objects above the Doctor first so that he appears to be behind
    # them
    for obj in above:
        screen.blit(obj.image, obj.rect)
    screen.blit(doctor.image, doctor.rect)
    for obj in below:
        screen.blit(obj.image, obj.rect)
    pygame.display.flip()
    
# Move map function
# Moves the map when the player moves and produces the illusion of walking.
def move_map(backgr_map, doctor, newpos, dir):
    move_increment = [newpos[0]/2, newpos[1]/2]
    temp_pos = [0, 0]
    ab = "_b"
    while temp_pos[0] != newpos[0] or temp_pos[1] != newpos[1]:
        if dir == "down" or dir == "up":
            if ab == "_b":
                ab = "_a"
            else:
                ab = "_b"
            doctor.image = pygame.image.load(im_dir+"doctor"+doc_num+dir+ab+".bmp")
        temp_pos[0] += move_increment[0]
        temp_pos[1] += move_increment[1]
        backgr_map.move(move_increment)
        for obj in backgr_map.objects:
            obj.move(move_increment)
        if doctor.base.topright == tardis.rect.bottomright:
            tardis.open_door()
        else:
            tardis.close_door()
        update_screen(backgr_map, doctor)
        pygame.time.wait(80)

# Fight loop function
# Defines the loop for having a fight with some opponent. Should be fairly easy
# to adapt to arguments
def fight(doctor, opponent, fight="fight"):
    menu1 = FightMenu()
    menu1.add_option("Fight")
    menu1.add_option("Items")
    menu1.add_option("Run")
    if opponent.name == "DALEK":
        sound = pygame.mixer.Sound(sound_dir+"Some Tea.wav")
        sound.set_volume(0.2)
        sound.play()
        gunsound = pygame.mixer.Sound(sound_dir+"dalek gun.wav")
        gunsound.set_volume(0.1)
    fight_map = Background("floor.bmp")
    fight_map.objects.append(opponent)
    doctor.rect.bottomleft = (tile, tile*5)
    opponent.rect.bottomleft = (tile*8, tile*5)
    doctor.face_direction("down")
    opponent.face_direction("left")
    update_screen(fight_map, doctor)
    attack_menu = FightMenu()
    for attack in doctor.attacks:
        attack_menu.add_option(attack)
    while 1:
        m, selection = show_menu(menu1, doctor, opponent, fight)
        # If player chooses to attack:
        if m == 0:
            # Choose which attack to use
            m2, attack = show_menu(attack_menu, doctor, opponent, fight)
            print_fight(doctor.name+" uses "+attack)
            hit = hit_or_miss(doctor, opponent)
            if hit == True:
                strength = doctor.attributes["Strength"]
                defense = opponent.attributes["Defense"]
                multiplier = strength/defense
                damage = int(doctor.attacks[attack]*multiplier)
                opponent.health[0] -= damage
                opponent.draw_health_bar()
                print_fight(attack+" did "+str(damage)+" damage to "+opponent.name)
            else:
                print_fight(doctor.name+"'s attack missed!")
            pygame.time.wait(1000)
            # Dalek attacks if not dead:
            if opponent.health[0] <= 0:
                return True
            a = random.randint(0, len(opponent.attacks.keys()))
            attack = opponent.attacks.keys()[a]
            print_fight(opponent.name+" uses "+attack)
            hit = hit_or_miss(opponent, doctor)
            if hit == True:
                if attack == "Dalek Gun":
                    gunsound.play()
                strength = opponent.attributes["Strength"]
                defense = doctor.attributes["Defense"]
                multiplier = strength/defense
                damage = int(opponent.attacks[attack]*multiplier)
                doctor.health[0] -= damage
                doctor.draw_health_bar()
                print_fight(attack+" did "+str(damage)+" damage to "
                            +doctor.name)
                pygame.time.wait(1000)
                if doctor.health[0] <= 0:
                    return False
            else:
                print_fight(opponent.name+"'s attack missed!")
        # If player chooses to run away:
        elif m == 2:
            return None

# Argument loop function.
# Pretty much the same as the fight loop but I found I was dealing with too many
# pointless if loops, so I separated it into two functions
def argue(doctor, opponent, doc_conv=0, opp_conv=0, fight="argument"):
    menu1 = FightMenu()
    doctor.conviction = doc_conv
    opponent.conviction = opp_conv
    menu1.add_option("Argue")
    menu1.add_option("Items")
    menu1.add_option("Run")
    fight_map = Background("floor.bmp")
    fight_map.objects.append(opponent)
    doctor.rect.bottomleft = (tile, tile*5)
    opponent.rect.bottomleft = (tile*8, tile*5)
    doctor.face_direction("down")
    update_screen(fight_map, doctor)
    attack_menu = FightMenu()
    for attack in doctor.arguments:
        attack_menu.add_option(attack)
    while 1:
        m, selection = show_menu(menu1, doctor, opponent, fight)
        # If player chooses to attack:
        if m == 0:
            # Choose which attack to use
            m2, attack = show_menu(attack_menu, doctor, opponent, fight)
            print_fight(doctor.name+" says: "+attack)
            hit = hit_or_miss(doctor, opponent)
            if hit == True:
                strength = doctor.skills["Intellect"]
                defense = opponent.skills["Counter-argument"]
                multiplier = strength/defense
                damage = int(doctor.arguments[attack]*multiplier)
                opponent.conviction -= damage
                doctor.conviction += damage
                draw_conviction_bar(doctor, opponent)
                print_fight(doctor.name+" did "+str(damage)+" damage to "
                            +opponent.name+"'s argument")
            else:
                print_fight(doctor.name+"'s argument fell on deaf ears!")
            pygame.time.wait(1000)
            # Opponent argues back if not convinced:
            if opponent.conviction <= 0:
                return True
            a = random.randint(0, len(opponent.arguments.keys()))
            attack = opponent.arguments.keys()[a]
            print_fight(opponent.name+" says: "+attack)
            hit = hit_or_miss(opponent, doctor, "argument")
            if hit == True:
                strength = opponent.skills["Intellect"]
                defense = doctor.skills["Counter-argument"]
                multiplier = strength/defense
                damage = int(opponent.arguments[attack]*multiplier)
                doctor.conviction -= damage
                opponent.conviction += damage
                draw_conviction_bar(doctor, opponent)
                print_fight(opponent.name+" did "+str(damage)+" damage to "
                            +doctor.name+"'s argument")
                pygame.time.wait(1000)
                if doctor.conviction <= 0:
                    return False
            else:
                print_fight(opponent.name+"'s argument fell on deaf ears!")
        # If player chooses to run away:
        elif m == 2:
            return None

# hit_or_miss function.
# Defines whether or not a character's attack hits the opponent.
def hit_or_miss(attacker, defender, fight="fight"):
    if fight == "fight":
        accuracy = attacker.attributes["Accuracy"]
        agility = defender.attributes["Agility"]
    else:
        accuracy = attacker.skills["Charisma"]
        agility = defender.skills["Stubbornness"]
    roll = random.randint(0, accuracy+agility)
    if roll > agility:
        return True
    else:
        return False

# print_fight function.
# Function to output text to the screen during a confrontation.
def print_fight(text):
    surf = pygame.Surface((tile*10, tile*2))
    rect = surf.fill((0, 0, 255))
    rect.bottomleft = screen.get_rect().bottomleft
    font = pygame.font.Font(None, 14)
    output = font.render(text, 1, (255, 255, 255))
    text_rect = output.get_rect(left=surf.get_rect().left+(tile/2), bottom=(tile/2))
    # Need a few lines here to put text on multiple lines if neccessary.
    surf.blit(output, text_rect)
    screen.blit(surf, rect)
    pygame.display.update(rect)
    pygame.time.delay(1000)
    
# Conviction bar function.
# Draws a bar in arguments to show who's winning. Very similar to
# Character.draw_health_bar.
def draw_conviction_bar(doctor, opponent):
    bar = pygame.Surface((tile*8, tile/2))
    red = (255, 0, 0)
    green = (0, 255, 0)
    total = doctor.conviction+opponent.conviction
    doctor_winning = (doctor.conviction/total)*tile*8
    bar.fill(red)
    bar.fill(green, (0, 0, doctor_winning, tile/2))
    bar_rect = bar.get_rect()
    bar_rect.left = doctor.rect.left
    bar_rect.bottom = doctor.rect.top - (tile)
    screen.blit(bar, bar_rect)
    pygame.display.update(bar_rect)

# Game over function.
# Prints game over message to the screen
def game_over():
    image = pygame.image.load(im_dir+"tardis2010a.bmp")
    rect = image.get_rect(center=screen.get_rect().center)
    font = pygame.font.Font(None, 28)
    text1 = font.render("Game", 1, (255, 255, 255))
    textrect1 = text1.get_rect(right=rect.left-(tile/2),centery=rect.centery)
    text2 = font.render("Over", 1, (255, 255, 255))
    textrect2 = text2.get_rect(left=rect.right+(tile/2),centery=rect.centery)
    screen.fill((0, 0, 0))
    screen.blit(image, rect)
    screen.blit(text1, textrect1)
    screen.blit(text2, textrect2)
    pygame.display.flip()
    pygame.time.wait(5000)
    pygame.display.quit()

# Initiate Doctor function
# Sets up the image and attributes of the Doctor
def init_doctor(doc_num):
    doctor = Character("DOCTOR", "doctor"+doc_num, tile*4, tile*5)
    # Define Doctor's current and maximum health.
    doctor.health = [10.0, 10.0]
    # Define Doctor's fighting attributes.
    doctor.attributes["Strength"] = 5.0
    doctor.attributes["Defense"] = 2.0
    doctor.attributes["Agility"] = 15.0
    doctor.attributes["Accuracy"] = 15.0
    # Define attacks Doctor can use.
    doctor.attacks = {"Punch": 3}
    # Define Doctor's arguing attributes.
    doctor.skills["Intellect"] = 15.0
    doctor.skills["Counter-argument"] = 10.0
    doctor.skills["Stubbornness"] = 6.0
    doctor.skills["Charisma"] = 10.0
    doctor.arguments = {"'Daleks are bad.'": 5}
    return doctor

# Initiate Dalek function
# Sets up a dalek Character
def init_dalek(dalek_type, x, y):
    dalek = Character("DALEK", "dalek"+dalek_type, x, y)
    dalek.health = [5.0, 15.0]
    dalek.attributes["Strength"] = 10.0
    dalek.attributes["Defense"] = 15.0
    dalek.attributes["Agility"] = 2.0
    dalek.attributes["Accuracy"] = 15.0
    dalek.attacks = {"Dalek Gun": 5, "Plunger": 2}
    return dalek

# Initiate bloke function.
# Defines a generic Character for the purposes of testing how well the arguments
# work
def init_bloke(x, y):
    bloke = Character("MR. SMITH", "bloke", x, y)
    bloke.skills["Intellect"] = 5.0
    bloke.skills["Counter-argument"] = 5.0
    bloke.skills["Stubbornness"] = 10.0
    bloke.skills["Charisma"] = 8.0
    bloke.arguments = {"'They've never done me any harm.'": 2}
    return bloke


# ====
# Define constants to be referred to later (many times)
# ====

tile = 32 # Width of squares (in pixels) used as unit for moving images around
places = ["floor.bmp", "pallet.bmp"] # List of places available to travel to. Will obviously need to be extended and will probably need several versions.
im_dir = "./images/" # Directory for graphics
sound_dir = "./sounds/" # Directory for sounds and music


# ====
# Initiate actual game
# ====

pygame.init()
size = width, height = tile*10, tile*9
pygame.key.set_repeat(50, 120)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Doctor Who")


# ====
# Initiate important objects
# ====

# There is now a choice of Doctor: Patrick Troughton or Matt Smith
doc_num = "2"
#doc_num = "11"
doctor = init_doctor(doc_num)
tardis = Tardis()

# Set up main menu
menu1 = Menu()
menu1.add_option("Return to game")
menu1.add_option("Quit")

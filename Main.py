import pygame, sys, math, Asteroid_Data, Menu, random
from pygame.locals import *


# draws information to the game screen
def draw_hud(surface, q_asteroids, php, round_num):
    if not (php <= 0):
        acount = pygame.font.SysFont("comicsansms", 24).render('Asteroids: ' + str(q_asteroids), True, yellow)
        hp = pygame.font.SysFont("comicsansms", 48).render('HP: ' + str(php) + '%', True, red)
        rndnum = pygame.font.SysFont("comicsansms", 24).render('Current Round: ' + str(round_num), True, yellow)
        surface.blit(rndnum, (790, 10))
        surface.blit(hp, (10, 700))
        surface.blit(acount, (10, 10))

    #   Rotate Functions


def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    return rot_image


def rot_center2(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image


# get asteroid info
E_Asteroids, M_Asteroids, H_Asteroids = Asteroid_Data.getA_Info()

##################  Tuples     ###############
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()

# Sound vars
pygame.mixer.music.load('sounds/soundtrack.mp3')
pygame.mixer.music.play(-1, 0.0)
shoot = pygame.mixer.Sound('sounds/fire.wav')
explode = pygame.mixer.Sound('sounds/bangsmall.wav')
banglarge = pygame.mixer.Sound('sounds/banglarge.wav')

FPS = 60
fpsClock = pygame.time.Clock()

surface = pygame.display.set_mode((1024, 768), 0, 32)  # define surface
# color tuples
yellow = (255, 255, 0)
red = (255, 0, 0)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
white = (255, 255, 255)
# predefine bullets list
bullets = []
speed = 6  # spaceship speed
bspeed = 10  # bullet speed
# inital asteroid speeds
espeed = 1
mspeed = 0.5
hspeed = 0.2
mousedown = False
# load the images
explosion = pygame.image.load('Images/explosion.png')
fireball = pygame.image.load('Images/fireball.png')
back1 = pygame.image.load('Images/background.png')
back2 = pygame.image.load('Images/gameback.png')
backg1 = back1.convert()
backg2 = back2.convert()
# random background for game play
backg = random.choice([backg2, backg1])

# define spaceship information
spaceshiplist = [pygame.image.load('Images/spaceship_engineoff.png'),
                 pygame.image.load('Images/spaceship_engineon.png'), False, 500, 500, 100]
ship = spaceshiplist[0].get_rect()

round_num = 1
# define initial movement vars
moveright = False
moveleft = False
moveup = False
movedown = False
# cheat mode toggle
toggle_C = 1
cheatmode = False
# gamemode bools
easymode = False
medmode = False
hardmode = False
# start bools
start = False
runmenu = True
lose = False  # this bool checks for lossing
# seconds make sure float
seconds = 0.0
wait = 3  # countdown time
proceed = False  # starts countdown clock

#   Main Game Loop
while True:
    # caption
    pygame.display.set_caption('Roid Rage - Jake Hessian FPS: ' + str(fpsClock.get_fps()))
    # for the timer
    seconds = (fpsClock.tick(FPS)) / 1000.0
    if runmenu == True:
        Menu.main(surface, runmenu)
        # get list info
        easymode, medmode, hardmode, start, runmenu = Menu.playmenu(surface, easymode, medmode, hardmode)
    if start == True:
        surface.blit(backg, (0, 0))
        # countdown before next round
        if proceed == False:
            text = pygame.font.SysFont("comicsansms", 48).render('Round starts in: ' + str((wait)), True, yellow)
            surface.blit(text, (100, 100))
            wait -= seconds
            if (wait) <= 0:
                proceed = True
        # gamemodes
        if proceed == True:
            # easymode
            if easymode == True:
                if lose == False:
                    # if player destroys all asteroids on screen
                    if len(E_Asteroids) == 0:
                        # reset vars
                        E_Asteroids, M_Asteroids, H_Asteroids = Asteroid_Data.getA_Info()
                        espeed += 0.2
                        round_num += 1
                        spaceshiplist[3] = 512 + 50
                        spaceshiplist[4] = 384 - 50
                        proceed = False
                        wait = 3
                        bullets = []  # delete bullets off screen
                    # go throught each asteroid
                    for asteroid in E_Asteroids:
                        # HP bar above asteroids
                        tr = (asteroid[3] / asteroid[4]) * 47
                        pygame.draw.line(surface, red, (asteroid[1], asteroid[2] - 10),
                                         (asteroid[1] + 47, asteroid[2] - 10), 2)
                        pygame.draw.line(surface, green, (asteroid[1], asteroid[2] - 10),
                                         (asteroid[1] + tr, asteroid[2] - 10), 2)
                        # attraction for asteroids -> asteroid movement
                        if spaceshiplist[3] + 50 > asteroid[1]:
                            asteroid[1] += espeed
                        if spaceshiplist[3] + 50 < asteroid[1]:
                            asteroid[1] -= espeed
                        if spaceshiplist[4] + 50 > asteroid[2]:
                            asteroid[2] += espeed
                        if spaceshiplist[4] + 50 < asteroid[2]:
                            asteroid[2] -= espeed
                        surface.blit(asteroid[0], (int(asteroid[1]), int(asteroid[2])))  # blit asteroid
                        # collision
                        if (spaceshiplist[3] < asteroid[1] < spaceshiplist[3] + 100) and (
                                spaceshiplist[4] < asteroid[2] < spaceshiplist[4] + 100):
                            banglarge.play()
                            spaceshiplist[5] -= random.randint(7, 12)
                            E_Asteroids.remove(asteroid)
                            surface.blit(explosion, (spaceshiplist[3] + 25, spaceshiplist[4] + 25))
                            if spaceshiplist[5] <= 0:
                                # make explosions around spaceship
                                surface.blit(explosion, (spaceshiplist[3] + 10, spaceshiplist[4] + 10))
                                surface.blit(explosion, (spaceshiplist[3] + 5, spaceshiplist[4] + 5))
                                surface.blit(explosion, (spaceshiplist[3] - 10, spaceshiplist[4] - 10))
                                surface.blit(explosion, (spaceshiplist[3] + 40, spaceshiplist[4] + 40))
                                surface.blit(explosion, (spaceshiplist[3] - 25, spaceshiplist[4] - 25))
                                lose = True
                    # go through every bullet
                    for bullet in bullets:
                        surface.blit(bullet[6], (bullet[0], bullet[1]))
                        bullet[1] += bullet[5]
                        bullet[0] += bullet[4]
                        # if the bullet goes off screen then remove it
                        if bullet[1] < 10 or bullet[0] < 10 or bullet[0] > 1014:
                            bullets.remove(bullet)
                        # go through each asteroid
                        for asteroid in E_Asteroids:
                            # detect collision between bullet and asteroid then inflict damage
                            if (asteroid[1] < bullet[0] < asteroid[1] + 47) and (
                                        asteroid[2] - 10 < bullet[1] < asteroid[2] + 43):
                                asteroid[3] -= 12
                                explode.play()
                                # this prevented an annoying error
                                try:
                                    if not (cheatmode == True):
                                        bullets.remove(bullet)
                                except:
                                    pass
                                surface.blit(explosion, (asteroid[1] - 10, asteroid[2] - 10))
                            if asteroid[3] < 0:
                                E_Asteroids.remove(asteroid)
                    # draw info to the screen
                    draw_hud(surface, len(E_Asteroids), spaceshiplist[5], round_num)
                # display the lose screen
                else:
                    lose = pygame.font.SysFont("comicsansms", 48).render('You Lose! ... Press backspace to countinue',
                                                                         True, yellow)
                    surface.blit(lose, (512 - lose.get_width() // 2, 384 - lose.get_height() // 2))
                    # medium mode
            if medmode == True:
                if lose == False:
                    # check to see if user destroyed all the asteroids
                    if len(M_Asteroids) == 0:
                        # reset the vars
                        E_Asteroids, M_Asteroids, H_Asteroids = Asteroid_Data.getA_Info()
                        espeed += 0.2
                        mspeed += 0.2
                        round_num += 1
                        spaceshiplist[3] = 512 + 50
                        spaceshiplist[4] = 384 - 50
                        proceed = False
                        wait = 3
                        bullets = []
                    # go through each asteroid
                    for asteroid in M_Asteroids:
                        # HP bar above asteroids
                        tr = (asteroid[3] / asteroid[4]) * 47
                        pygame.draw.line(surface, red, (asteroid[1], asteroid[2] - 10),
                                         (asteroid[1] + 47, asteroid[2] - 10), 2)
                        pygame.draw.line(surface, green, (asteroid[1], asteroid[2] - 10),
                                         (asteroid[1] + tr, asteroid[2] - 10), 2)
                        # detect collision with spaceship
                        if (spaceshiplist[3] < asteroid[1] < spaceshiplist[3] + 100) and (
                                spaceshiplist[4] < asteroid[2] < spaceshiplist[4] + 100):
                            banglarge.play()
                            M_Asteroids.remove(asteroid)  # remove asteroid
                            surface.blit(explosion, (spaceshiplist[3] + 25, spaceshiplist[4] + 25))
                        if (spaceshiplist[3] < asteroid[1] < spaceshiplist[3] + 100) and (
                                spaceshiplist[4] < asteroid[2] < spaceshiplist[4] + 100):
                            banglarge.play()
                            try:
                                M_Asteroids.remove(asteroid)
                            except:
                                pass
                            if asteroid[5] == "easy":
                                spaceshiplist[5] -= random.randint(5, 12)
                            else:
                                spaceshiplist[5] -= random.randint(15, 22)
                            surface.blit(explosion, (spaceshiplist[3] + 25, spaceshiplist[4] + 25))
                            if spaceshiplist[5] <= 0:
                                surface.blit(explosion, (spaceshiplist[3] + 10, spaceshiplist[4] + 10))
                                surface.blit(explosion, (spaceshiplist[3] + 5, spaceshiplist[4] + 5))
                                surface.blit(explosion, (spaceshiplist[3] - 10, spaceshiplist[4] - 10))
                                surface.blit(explosion, (spaceshiplist[3] + 40, spaceshiplist[4] + 40))
                                surface.blit(explosion, (spaceshiplist[3] - 25, spaceshiplist[4] - 25))
                                lose = True  # initiate lose screen

                                # attraction for asteroids -> asteroid movement
                                # Medium asteroids
                        if asteroid[5] == "med":
                            if spaceshiplist[3] + 50 > asteroid[1]:
                                asteroid[1] += mspeed
                            if spaceshiplist[3] + 50 < asteroid[1]:
                                asteroid[1] -= mspeed
                            if spaceshiplist[4] + 50 > asteroid[2]:
                                asteroid[2] += mspeed
                            if spaceshiplist[4] + 50 < asteroid[2]:
                                asteroid[2] -= mspeed
                        else:  # this hangled the easy asteroids
                            if spaceshiplist[3] + 50 > asteroid[1]:
                                asteroid[1] += espeed
                            if spaceshiplist[3] + 50 < asteroid[1]:
                                asteroid[1] -= espeed
                            if spaceshiplist[4] + 50 > asteroid[2]:
                                asteroid[2] += espeed
                            if spaceshiplist[4] + 50 < asteroid[2]:
                                asteroid[2] -= espeed
                        surface.blit(asteroid[0], (int(asteroid[1]), int(asteroid[2])))
                        # go throught the bullets
                    for bullet in bullets:
                        # update bullet
                        surface.blit(bullet[6], (bullet[0], bullet[1]))
                        bullet[1] += bullet[5]
                        bullet[0] += bullet[4]
                        if bullet[1] < 10 or bullet[0] < 10 or bullet[0] > 1014:
                            bullets.remove(bullet)
                        for asteroid in M_Asteroids:
                            # check for bullet asteroid collision
                            if asteroid[5] == 'easy':  # easy asteroids
                                if (asteroid[1] < bullet[0] < asteroid[1] + 47) and (
                                            asteroid[2] - 10 < bullet[1] < asteroid[2] + 43):
                                    try:
                                        if not (cheatmode == True):
                                            bullets.remove(bullet)
                                    except:
                                        pass
                                    asteroid[3] -= 12
                                    explode.play()
                                    surface.blit(explosion, (asteroid[1] - 10, asteroid[2] - 10))  # blit
                            else:  # medium asteroids
                                if (asteroid[1] < bullet[0] < asteroid[1] + 60) and (
                                            asteroid[2] - 10 < bullet[1] < asteroid[2] + 60):
                                    try:
                                        if not (cheatmode == True):
                                            bullets.remove(bullet)
                                    except:
                                        pass
                                    asteroid[3] -= 12
                                    explode.play()
                                    surface.blit(explosion, (asteroid[1] - 10, asteroid[2] - 10))

                            if asteroid[3] < 0:
                                M_Asteroids.remove(asteroid)
                    draw_hud(surface, len(M_Asteroids), spaceshiplist[5], round_num)  # draw hud
                else:
                    # lose screen
                    lose = pygame.font.SysFont("comicsansms", 48).render('You Lose! ... Press backspace to countinue',
                                                                         True, yellow)
                    surface.blit(lose, (512 - lose.get_width() // 2, 384 - lose.get_height() // 2))
            # hardmode
            if hardmode == True:
                if lose == False:
                    # check to see if the user destroyed all the asteroids
                    if len(H_Asteroids) == 0:
                        # reset the vars
                        E_Asteroids, M_Asteroids, H_Asteroids = Asteroid_Data.getA_Info()
                        espeed += 0.5
                        mspeed += 0.2
                        hspeed += 0.2
                        round_num += 1
                        spaceshiplist[3] = 512 + 50
                        spaceshiplist[4] = 384 - 50
                        proceed = False
                        wait = 3
                        bullets = []
                    # go through each asteroid
                    for asteroid in H_Asteroids:
                        # HP bar above asteroids
                        # attraction for asteroids -> asteroid movement
                        # handle medium asteroid movement
                        if asteroid[5] == "med":
                            if spaceshiplist[3] + 50 > asteroid[1]:
                                asteroid[1] += mspeed
                            if spaceshiplist[3] + 50 < asteroid[1]:
                                asteroid[1] -= mspeed
                            if spaceshiplist[4] + 50 > asteroid[2]:
                                asteroid[2] += mspeed
                            if spaceshiplist[4] + 50 < asteroid[2]:
                                asteroid[2] -= mspeed
                            # DISPLAY health bar
                            tr = (asteroid[3] / asteroid[4]) * 60
                            pygame.draw.line(surface, red, (asteroid[1], asteroid[2] - 10),
                                             (asteroid[1] + 60, asteroid[2] - 10), 2)
                            pygame.draw.line(surface, green, (asteroid[1], asteroid[2] - 10),
                                             (asteroid[1] + tr, asteroid[2] - 10), 2)
                        # hangdle easy asteroids
                        if asteroid[5] == "easy":
                            if spaceshiplist[3] + 50 > asteroid[1]:
                                asteroid[1] += espeed
                            if spaceshiplist[3] + 50 < asteroid[1]:
                                asteroid[1] -= espeed
                            if spaceshiplist[4] + 50 > asteroid[2]:
                                asteroid[2] += espeed
                            if spaceshiplist[4] + 50 < asteroid[2]:
                                asteroid[2] -= espeed
                            # display healthbar
                            tr = (asteroid[3] / asteroid[4]) * 47
                            pygame.draw.line(surface, red, (asteroid[1], asteroid[2] - 10),
                                             (asteroid[1] + 47, asteroid[2] - 10), 2)
                            pygame.draw.line(surface, green, (asteroid[1], asteroid[2] - 10),
                                             (asteroid[1] + tr, asteroid[2] - 10), 2)
                        # handle hard asteroids
                        if asteroid[5] == 'hard':
                            if spaceshiplist[3] + 50 > asteroid[1]:
                                asteroid[1] += hspeed
                            if spaceshiplist[3] + 50 < asteroid[1]:
                                asteroid[1] -= hspeed
                            if spaceshiplist[4] + 50 > asteroid[2]:
                                asteroid[2] += hspeed
                            if spaceshiplist[4] + 50 < asteroid[2]:
                                asteroid[2] -= hspeed
                            # display healthbar
                            tr = (asteroid[3] / asteroid[4]) * 75
                            pygame.draw.line(surface, red, (asteroid[1], asteroid[2] - 10),
                                             (asteroid[1] + 75, asteroid[2] - 10), 2)
                            pygame.draw.line(surface, green, (asteroid[1], asteroid[2] - 10),
                                             (asteroid[1] + tr, asteroid[2] - 10), 2)

                        surface.blit(asteroid[0], (int(asteroid[1]), int(asteroid[2])))
                        # spaceship asteroid collision
                        if (spaceshiplist[3] < asteroid[1] < spaceshiplist[3] + 100) and (
                                spaceshiplist[4] < asteroid[2] < spaceshiplist[4] + 100):
                            banglarge.play()
                            try:
                                H_Asteroids.remove(asteroid)
                            except:
                                pass
                            surface.blit(explosion, (spaceshiplist[3] + 25, spaceshiplist[4] + 25))  # blit
                            # inflict damage based on the asteroid difficulty
                            if asteroid[5] == "easy":
                                spaceshiplist[5] -= random.randint(5, 12)
                            if asteroid[5] == "med":
                                spaceshiplist[5] -= random.randint(15, 22)
                            if asteroid[5] == "hard":
                                spaceshiplist[5] -= random.randint(22, 55)
                            surface.blit(explosion, (spaceshiplist[3] + 25, spaceshiplist[4] + 25))
                            if spaceshiplist[5] <= 0:
                                surface.blit(explosion, (spaceshiplist[3] + 10, spaceshiplist[4] + 10))
                                surface.blit(explosion, (spaceshiplist[3] + 5, spaceshiplist[4] + 5))
                                surface.blit(explosion, (spaceshiplist[3] - 10, spaceshiplist[4] - 10))
                                surface.blit(explosion, (spaceshiplist[3] + 40, spaceshiplist[4] + 40))
                                surface.blit(explosion, (spaceshiplist[3] - 25, spaceshiplist[4] - 25))
                                lose = True
                    # go through each bullet
                    for bullet in bullets:
                        surface.blit(bullet[6], (bullet[0], bullet[1]))
                        bullet[1] += bullet[5]
                        bullet[0] += bullet[4]
                        if bullet[1] < 10 or bullet[0] < 10 or bullet[0] > 1014:
                            bullets.remove(bullet)
                        # go through each asteroid
                        for asteroid in H_Asteroids:
                            # check easy asteroid collision with bullet
                            if asteroid[5] == 'easy':
                                if (asteroid[1] < bullet[0] < asteroid[1] + 47) and (
                                            asteroid[2] - 10 < bullet[1] < asteroid[2] + 43):
                                    try:
                                        if not (cheatmode == True):
                                            bullets.remove(bullet)
                                    except:
                                        pass
                                    asteroid[3] -= 12
                                    explode.play()
                                    surface.blit(explosion, (asteroid[1] - 10, asteroid[2] - 10))
                            # check medium collision with bullet
                            if asteroid[5] == "med":
                                if (asteroid[1] < bullet[0] < asteroid[1] + 60) and (
                                            asteroid[2] - 10 < bullet[1] < asteroid[2] + 60):
                                    try:
                                        if not (cheatmode == True):
                                            bullets.remove(bullet)
                                    except:
                                        pass
                                    asteroid[3] -= 12
                                    explode.play()
                                    surface.blit(explosion, (asteroid[1] - 10, asteroid[2] - 10))
                            # check hard collision with bullet
                            if asteroid[5] == 'hard':
                                if (asteroid[1] < bullet[0] < asteroid[1] + 75) and (
                                            asteroid[2] - 10 < bullet[1] < asteroid[2] + 75):
                                    try:
                                        if not (cheatmode == True):
                                            bullets.remove(bullet)
                                    except:
                                        pass
                                    asteroid[3] -= 12
                                    explode.play()
                                    surface.blit(explosion, (asteroid[1] - 10, asteroid[2] - 10))

                            if asteroid[3] < 0:  # if asteroi'ds health is below zero remove it
                                H_Asteroids.remove(asteroid)
                    draw_hud(surface, len(H_Asteroids), spaceshiplist[5], round_num)
                else:
                    lose = pygame.font.SysFont("comicsansms", 48).render('You Lose! ... Press backspace to countinue',
                                                                         True, yellow)
                    surface.blit(lose, (512 - lose.get_width() // 2, 384 - lose.get_height() // 2))
        if lose == False:
            # constant getting angle to rotate the image
            pos2 = pygame.mouse.get_pos()

            x12 = (pos2[0] - 100) - (spaceshiplist[3] - 100)
            y12 = (pos2[1] - 100) - (spaceshiplist[4] - 100)
            angle = (math.degrees(math.atan2(y12, x12)) / -1) - 90

            if spaceshiplist[2] == False:
                sprite = rot_center2(spaceshiplist[0], angle)
                surface.blit(sprite, (spaceshiplist[3], spaceshiplist[4]))
            else:
                sprite = rot_center2(spaceshiplist[1], angle)
                surface.blit(sprite, (spaceshiplist[3], spaceshiplist[4]))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            # this sets the movement vars to false
            if event.type == KEYUP:
                if event.key == K_w:
                    spaceshiplist[2] = False
                    moveup = False
                if event.key == K_s:
                    spaceshiplist[2] = False
                    movedown = False
                if event.key == K_d:
                    spaceshiplist[2] = False
                    moveright = False
                if event.key == K_a:
                    spaceshiplist[2] = False
                    moveleft = False
            if event.type == KEYDOWN:
                # toggle cheatmode
                if event.key == K_c:
                    toggle_C += 1
                    if toggle_C % 2 == 0:
                        print "Cheat mode ENABLED"
                        cheatmode = True
                    else:
                        print "Cheat mode DISABLED"
                        cheatmode = False
                        # go back and reset vars
                if event.key == K_BACKSPACE:
                    bspeed = 10
                    espeed = 1
                    mspeed = 0.5
                    hspeed = 0.2
                    runmenu = True
                    lose = False
                    spaceshiplist[2] = False
                    spaceshiplist[3] = 500
                    spaceshiplist[4] = 500
                    spaceshiplist[5] = 100
                    round_num = 1
                    proceed = False
                    wait = 3
                    backg = random.choice([backg2, backg1])
                    easymode = False
                    medmode = False
                    hardmode = False
                    E_Asteroids, M_Asteroids, H_Asteroids = Asteroid_Data.getA_Info()
                    # enables movement variables
                if event.key == K_w:
                    moveup = True
                if event.key == K_s:
                    movedown = True
                if event.key == K_d:
                    moveright = True
                if event.key == K_a:
                    moveleft = True
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if lose == False:
                # create a bullet
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if proceed == True:
                            shoot.play()
                            # this gets the bullets angle based on the mouseclick and the spaceship
                            pos = pygame.mouse.get_pos()
                            x1 = int(pos[0]) - int(spaceshiplist[3] + 50)
                            y1 = int(pos[1]) - int(spaceshiplist[4] + 50)
                            angle = math.atan2(y1,
                                               x1)  # (y/x),      (tan = opposite/adjacent) of a right triangle. (atan or cot = adja/opp)
                            dx = bspeed * math.cos(angle)
                            dy = bspeed * math.sin(angle)
                            print dx, dy
                            angle = (math.degrees(angle))
                            sprite = rot_center(fireball, angle)
                            ship = spaceshiplist[0].get_rect()
                            # add to bullet list
                            bullets.append(
                                    [spaceshiplist[3] + 50, spaceshiplist[4] + 50, pos[0], pos[1], dx, dy, sprite])
                    if event.button == 3:
                        spaceshiplist[2] = True
                if event.type == MOUSEBUTTONUP:
                    if event.button == 3:
                        spaceshiplist[2] = False
                        #
        if lose == False:  # this disabled movement on the lost screen
            # movement vars
            if moveup == True:
                spaceshiplist[2] = True
                spaceshiplist[4] -= speed
            if movedown == True:
                spaceshiplist[2] = True
                spaceshiplist[4] += speed
            if moveleft == True:
                spaceshiplist[2] = True
                spaceshiplist[3] -= speed
            if moveright == True:
                spaceshiplist[2] = True
                spaceshiplist[3] += speed
            if spaceshiplist[4] < 0:
                spaceshiplist[4] = 0
                # so the spaceship doesn't go off screen (my brother was cheating)
            if spaceshiplist[4] + 100 > 768:
                spaceshiplist[4] = 668
            if spaceshiplist[3] + 100 > 1024:
                spaceshiplist[3] = 1024 - 100
            if spaceshiplist[3] < 0:
                spaceshiplist[3] = 0

        pygame.display.update()  # update screen

    pygame.display.update()
    fpsClock.tick(FPS)

import pygame, sys, math, Asteroid_Data
from pygame.locals import *

#define picture tuples
back = pygame.image.load('Images/menu/background.png')
play_menu = pygame.image.load('Images/menu/playmenu.png')
controls_pic = pygame.image.load('images/menu/controlsmenu.png')
help_menu = pygame.image.load('images/menu/helpmenu.png')

pygame.init()
FPS = 60#FPS cap
yellow = (255,255,0)#color tuple for underline selection
fpsClock = pygame.time.Clock()
#this handles the mainmenu    must input surface and runmenu to run certain components of function
def main(surface,runmenu):
    #booleans to display certain items
    showcontrols = False
    showhelp = False
    main = True
    #main menu run
    while runmenu == True:
        #blit the controls picture if it is slected
        if showcontrols == True:
            surface.blit(controls_pic,(0,0))
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_BACKSPACE:#returns to main menu
                        showcontrols = False
                        main = True
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
        #if slected show help picture
        if showhelp == True:
            surface.blit(help_menu,(0,0))
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_BACKSPACE:
                        showhelp = False
                        main = True
                if event.type==QUIT:
                    pygame.quit()
                    sys.exit()
        #main menu that handles most user input
        if main == True:
            surface.blit(back,(0,0))
            mousex, mousey = pygame.mouse.get_pos()
            #this detects mousemotion over top of a button
            if (330 < mousex < 708) and (240 < mousey < 340):
                pygame.draw.line(surface,yellow,(388,309),(645,309),5)
            if (330 < mousex < 708) and (380 < mousey < 480):
                pygame.draw.line(surface,yellow,(388,456),(645,456),5)
            if (330 < mousex < 708) and (520 < mousey < 622):
                pygame.draw.line(surface,yellow,(388,597),(645,597),5)
            #user input
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_BACKSPACE:
                        pygame.quit()
                        sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        #see where the user clicked and what button the user clicked
                        mousex, mousey = pygame.mouse.get_pos()
                        if (330 < mousex < 708) and (240 < mousey < 340):
                            #playmenu enabled
                            runmenu = False
                        if (330 < mousex < 708) and (380 < mousey < 480):
                            #show controls
                            showcontrols = True
                            main = False
                        if (330 < mousex < 708) and (520 < mousey < 622):
                            #show help
                            showhelp = True
                            main = False
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
        pygame.display.update()
        fpsClock.tick(FPS)
#input surface and the booleans for the gamemodes
def playmenu(surface,easymode,medmode,hardmode):
   # print "Play menu selected"
   #display while the user has not made achoice
    while easymode == False and medmode == False and hardmode == False:
        surface.blit(play_menu,(0,0))
        mousex,mousey = pygame.mouse.get_pos()
        if (333 < mousex < 708) and (261 < mousey < 358):
            pygame.draw.line(surface,yellow,(377,335),(665,335),5)
        if (333 < mousex < 708) and (389 < mousey < 490):
            pygame.draw.line(surface,yellow,(377,466),(665,466),5)
        if (333 < mousex < 708) and (527 < mousey < 626):
            pygame.draw.line(surface,yellow,(377,605),(665,605),5)
            
            
        #see where the user clicked accordingly
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_BACKSPACE:
                    main(surface,runmenu=True)
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    mousex,mousey = pygame.mouse.get_pos()
                    if (333 < mousex < 708) and (261 < mousey < 358):
                        
                        easymode = True
                    if (333 < mousex < 708) and (389 < mousey < 490):
                        medmode = True
                        
                    if (333 < mousex < 708) and (527 < mousey < 626):
                        hardmode = True
                        
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
        fpsClock.tick(FPS)
    #runemenu = false start = True initilizes game
    runmenu = False
    start = True
    #return the gamemode booleans
    return easymode,medmode,hardmode,start,runmenu

    

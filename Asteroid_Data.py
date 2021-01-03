import pygame, sys, math,random
from pygame.locals import *
#this function reads data from the textfile "Asteroids.txt" then assigns it to a list then returns the lists.
def getA_Info():
    #define the images
    surface = pygame.display.set_mode((1024,768),0,32)
    image = pygame.image.load('Images/roids/roid.png')#small roid
    image2 = pygame.image.load('Images/roids/roid2.png')#med roid
    image3 = pygame.image.load('Images/roids/roid3.png')#large roid
    #see if the speeds up the fps
    image.convert()
    image2.convert()
    image3.convert()
    #easy asteroid list
    E_Asteroids = []
    te = "" #Temporary variable
    infile = open("Asteroids.txt","r")
    line = infile.readline().rstrip("\n")
    while line != '&':
        te = line.split(" ")
        te[0] = image
        #make sure to add this to the list as integer data
        te[1] = int(te[1])
        te[2] = int(te[2])
        te[3] = float(te[3])
        te[4] = float(te[4])
        E_Asteroids.append(te)
        line = infile.readline().rstrip("\n")
    #Medium asteroid list
    M_Asteroids = []
    line = infile.readline().rstrip('\n')
    te = ""
    while line != '$':
        te = line.split(" ")
        te[0] = image
        #must be int data
        te[1] = int(te[1])
        te[2] = int(te[2])
        te[3] = float(te[3])
        te[4] = float(te[4])
        #this assigns the proper image to the asteroid based on health
        if te[4] >= 33:
            te[0] = image2
        M_Asteroids.append(te)
        line = infile.readline().rstrip('\n')
    #hard asteroids list
    H_Asteroids = []
    line = infile.readline().rstrip('\n')
    te = ""
    while line != '#':
        te = line.split(" ")
        #add as integer data
        te[1] = int(te[1])
        te[2] = int(te[2])
        te[3] = float(te[3])
        te[4] = float(te[4])
        #assign proper image to the asteroid based on the asteroid's hp
        if te[5] == 'easy':
            te[0] = image
        if te[5] == 'med':
            te[0] = image2
        if te[5] == 'hard':
            te[0] = image3
        H_Asteroids.append(te)
        line = infile.readline().strip('\n')
    #return the lists
    return E_Asteroids, M_Asteroids, H_Asteroids





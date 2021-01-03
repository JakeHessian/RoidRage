import random
import pygame
from pygame.locals import *
#open textfile for writing
infile = open('Asteroids.txt',"w")

#define inital vars
line = ""
te = 0

#Define the easy asteroids
for i in range(0,30):
    hp = random.randint(1,33)
    x = random.randint(-40,1024)
    #so the asteroid doesn't spawn in the middle of the screen
    if x > 100 and x < 900:
        te = random.randint(1,2)
        if te == 1:
            y = random.randint(-40,50)
        else:
            y = random.randint(650,780)
    else:
        y = random.randint(10,750)
    #write lines to the textfile
    if i == 0:
        line = 'easy'+ ' ' + str(x) + ' ' + str(y) + ' ' + str(hp)+ ' ' +str(hp)
        infile.write(line)
    else:
        line = '\neasy'+ ' ' + str(x) + ' ' + str(y) + ' ' + str(hp)+ ' ' +str(hp)
        infile.write(line)
#stop at "&" for the reader
infile.write('\n&')


#Generate Medium asteroids
for i in range(0,25):
    #every other asteroid is an easy asteroid
    #medium asteroids
    if x%2 == 0:
        hp = random.randint(33,66)
        x = random.randint(-40,1024)
        if x > 100 and x < 900:
            te = random.randint(1,2)
            if te == 1:
                y = random.randint(1,50)
            else:
                y = random.randint(700,750)
        else:
            y = random.randint(10,750)
        line = '\nmed'+ ' ' + str(x) + ' ' + str(y) + ' ' + str(hp)+ ' ' +str(hp)+ ' med'
        infile.write(line)
    #easy asteroids
    else:
        hp = random.randint(1,33)
        x = random.randint(-40,1024)
        if x > 100 and x < 900:
            #te can either make the asteroid spawn on the top or the bottom
            te = random.randint(1,2)
            if te == 1:
                y = random.randint(1,50)
            else:
                y = random.randint(700,750)
        else:
            y = random.randint(10,750)
        #write items to text file
        line = '\neasy'+ ' ' + str(x) + ' ' + str(y) + ' ' + str(hp)+ ' ' +str(hp)+ ' easy'
        infile.write(line)
#so the asteroid data reader knows where to end this list
infile.write('\n$')


#hard mode asteroid data
#Hard asteroids
for i in range(0,28):
    hp = random.randint(66,99)
    x = random.randint(-40,1024)
    if x > 100 and x < 900:
        te = random.randint(1,2)
        if te == 1:
            y = random.randint(1,50)
        else:
            y = random.randint(700,750)
    else:
        y = random.randint(10,750)
    line = '\nhard'+ ' ' + str(x) + ' ' + str(y) + ' ' + str(hp)+ ' ' +str(hp)+ ' hard'
    infile.write(line)
#medium asteroids
for i in range(0,12):
    hp = random.randint(33,66)
    x = random.randint(-40,1024)
    if x > 100 and x < 900:
        te = random.randint(1,2)
        if te == 1:
            y = random.randint(1,50)
        else:
            y = random.randint(700,750)
    else:
        y = random.randint(10,750)
    line = '\nmed'+ ' ' + str(x) + ' ' + str(y) + ' ' + str(hp)+ ' ' +str(hp)+ ' med'
    infile.write(line)
#easy asteroids
for i in range(0,8):
    hp = random.randint(1,33)
    x = random.randint(-40,1024)
    if x > 100 and x < 900:
        te = random.randint(1,2)
        if te == 1:
            y = random.randint(1,50)
        else:
            y = random.randint(700,750)
    else:
        y = random.randint(10,750)
    if i == 0:
        line = '\neasy'+ ' ' + str(x) + ' ' + str(y) + ' ' + str(hp)+ ' ' +str(hp) + ' easy'
        infile.write(line)
    else:
        line = '\neasy'+ ' ' + str(x) + ' ' + str(y) + ' ' + str(hp)+ ' ' +str(hp) + ' easy'
        infile.write(line)
infile.write('\n#')
#close the file to avoid corruption
infile.close()

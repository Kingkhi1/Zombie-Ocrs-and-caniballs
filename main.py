#import sys
 
import pygame
import math
from pygame.locals import *
from pygame import mixer
from enum import Enum


DEBUG = False

#Useful Colors 
GREEN = (0, 255, 0) 
BLUE = (0, 0, 128) 
BLACK = (0, 0, 0)

#D11A. GameState Enum
class GameState(Enum):
    MAINMENU = 1
    GAMEPLAY = 2
    GAMEOVER = 3

# Collision Detection #####################################
def CollisionDetected(rectangleA, rectangleB):
    collided = False
    if ((rectangleA.top < rectangleB.bottom) and
    (rectangleA.bottom > rectangleB.top) and
    (rectangleA.right > rectangleB.left) and
    (rectangleA.left < rectangleB.right)):
        collided = True
    return collided

# Main Program ############################################

pygame.init()
#Screen Size 
width = 1024
height = 1024
pygame.display.set_caption ("Game Name")
screen = pygame.display.set_mode((width, height))
#Setting FPS
fps = 60
fpsClock = pygame.time.Clock()
 
#pygame.mixer.init() #sound not supported in repl.it

font = pygame.font.Font('freesansbold.ttf', 30)
text = font.render("START", True, GREEN, BLUE)
textRect = text.get_rect()
textRect.center = (width//2, height- 100)

debugfont = pygame.font.Font('freesansbold.ttf', 10)
debugtext = debugfont.render("", True, GREEN, BLUE)
debugRect = debugtext.get_rect()
debugRect.center = (width//2, 20)

#Predefine variables
keys = pygame.key.get_pressed()

#D11B. Starting GameState
gamestate = GameState.MAINMENU


#background Variables
bgPic = pygame.image.load("island.png")
bgPic = pygame.transform.scale(bgPic, (4096, 4096))
bgRect = bgPic.get_rect()
bgRect.center = (width//2,height//2)

#Bullet Variables
showBullet = False
colliding = False
rockPic = pygame.image.load("rock.png")
rockPic = pygame.transform.scale(rockPic, (50, 50))
rocks = []

#Ship Lives Variables
smallPic = pygame.image.load("zombie2.png")
smallPic =  pygame.transform.scale(smallPic, (30, 40))
small1Rect = smallPic.get_rect() 
small2Rect = smallPic.get_rect() 
small1Rect.center = (width//12,height//12)
small2Rect.center = (width//12+50,height//12)

#Player Ship Variables
ericpic = pygame.image.load("eric.png")
ericpic = pygame.transform.scale(ericpic, (75, 75))
playerrect = ericpic.get_rect() 
playerrect.center = (width//2,height//2)
  
#UFO Ship Variables
canabalPic = pygame.image.load("canabal.png")
canabalPic = pygame.transform.scale(canabalPic, (90, 90))
canabalRect = canabalPic.get_rect() 
canabalRect.center = (-100,-100)
direction = "RIGHT"

#UFO BIG ENDING
endPic = pygame.image.load("canabal.png")
startRect = endPic.get_rect() 
startRect.center = (120,100)
endRect = endPic.get_rect() 
endRect.center = (width//2,height//2)

#Sound Effect Variables (sound not supported in repl.it)
laserSound = pygame.mixer.Sound('laser.wav') 

# Game loop ##############################################
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False

    screen.fill(BLACK)

    #DEBUG MESSAGES
    if DEBUG:
        debugtext = debugfont.render("(DEBUG) " + gamestate.name + " " + str(gamestate.value) + " Colliding: " + str (colliding), True, (0,0,0), (255,255,255))
        debugRect = debugtext.get_rect()
        debugRect.center = (400, 20)
      
    ##### Update Section #####
    #Detecting inputs
    keys = pygame.key.get_pressed()
    mouseXY = pygame.mouse.get_pos()
    #gamepad = pygame.joystick.Joystick(0)
    #Read left mouse button
    mouseClick = pygame.mouse.get_pressed()[0] 
    #Read all 3 mouse buttons
    mouseMCR = pygame.mouse.get_pressed()


    if gamestate == GameState.MAINMENU:
        if keys[pygame.K_RETURN]:
            gamestate = GameState.GAMEPLAY
        if mouseClick and textRect.collidepoint(mouseXY):
            gamestate = GameState.GAMEPLAY
            canabalRect.center = (-250,-650)
            playerrect.center = (width//2,height//2)
            bgRect.center = (width//2,height//2)

    elif gamestate == GameState.GAMEPLAY:
        #move canabal
        dist = math.sqrt((playerrect.centerx-canabalRect.centerx)**2 + (playerrect.centery-canabalRect.centery)**2)
        if dist < 550:
            oldRect = pygame.Rect(canabalRect.x, canabalRect.y, canabalRect.width, canabalRect.height)
            print(oldRect)
            print(canabalRect)
            if canabalRect.centerx > playerrect.centerx:
                canabalRect.move_ip(-3,0)
            if canabalRect.centerx < playerrect.centerx:
                canabalRect.move_ip(3,0)
            for rock in rocks:
                if CollisionDetected(canabalRect, rock):
                    canabalRect = oldRect
                    break
        if canabalRect.centery > playerrect.centery:
            canabalRect.move_ip(0,-3)
        if canabalRect.centery < playerrect.centery:
            canabalRect.move_ip(0,3)

        for rock in rocks:
          if CollisionDetected(canabalRect, rock):
            canabalRect = oldRect
            break
        #Example of moving a rocket sprite left and right with keyboard
        if keys[pygame.K_LEFT]:
            bgRect.move_ip(10,0)
            canabalRect.move_ip(10,0)
            for rock in rocks: rock.move_ip(10,0)
 
        if keys [pygame.K_RIGHT]:
            bgRect.move_ip(-10,0)
            for rock in rocks: rock.move_ip(-10,0)
            canabalRect.move_ip(-10,0)
        if keys[pygame.K_UP]:
            bgRect.move_ip(0,10)
            for rock in rocks: rock.move_ip(0,10)
            canabalRect.move_ip(0,10)
        if keys [pygame.K_DOWN]:
            bgRect.move_ip(0,-10)
            for rock in rocks: rock.move_ip(0,-10)
            canabalRect.move_ip(0,-10)
            
        #Example of moving a rocket sprite left and right with DPAD
        #[x1, y1] = gamepad.get_hat(0)
        #rocketRect.move_ip(x1*10,-y1*10)
      
        #Example of moving a rocket sprite left and right with Analog Stick
        #x2 = gamepad.get_axis(0)
        #y2 = gamepad.get_axis(1)
        #rocketRect.move_ip(x2*10,y2*10)

        #Example of firing bullet with keyboard
        if keys [pygame.K_SPACE]:
            rockRect = rockPic.get_rect()
            rockRect.center = (playerrect.centerx,playerrect.centery)
            rocks.append(rockRect)

        #Example of firing bullet with controller
        #if gamepad.get_button(0):
        #  laserSound.play()
        #  showBullet = True
        #  bulletRect = bulletPic.get_rect()
        #  bulletRect.center = (rocketRect.centerx,height - 100)

      
        #check if ufo and bullet collide
        colliding = CollisionDetected(canabalRect,playerrect) 
        if colliding:
            gamestate = GameState.GAMEOVER
    
    elif gamestate == GameState.GAMEOVER:
        text = font.render("Press SPACE", True, GREEN, BLACK)
        textRect = text.get_rect()
        textRect.center = (width//2, height- 100)
        if keys[pygame.K_SPACE]:
            gamestate = GameState.MAINMENU
            showBullet = False
            rockRect.center = (0,height - 100)
            colliding = False
            text = font.render("START", True, GREEN, BLUE)
            textRect = text.get_rect()
            textRect.center = (width//2, height- 100)




    ##### Draw Section #####
    if gamestate == GameState.MAINMENU:
        screen.blit(bgPic,bgRect)
        screen.blit(text, textRect)
        screen.blit(endPic,startRect)

    elif gamestate == GameState.GAMEPLAY:
        screen.blit(bgPic,bgRect)
        screen.blit(ericpic,playerrect)
        screen.blit(smallPic,small1Rect)
        screen.blit(smallPic,small2Rect)
        screen.blit(canabalPic,canabalRect)
        for rock in rocks:
            screen.blit(rockPic,rock)
    
    elif gamestate == GameState.GAMEOVER:
        endPic = pygame.transform.rotate (endPic, 180)
        screen.blit(endPic,endRect)
        endPic = pygame.transform.rotate (endPic, 180)
        screen.blit(text, textRect) 
    
    if DEBUG:
        screen.blit(debugtext, debugRect)

    pygame.display.flip()
    fpsClock.tick(fps)

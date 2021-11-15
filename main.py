import pygame
import math
from pygame.locals import *
from pygame import mixer
pygame.init()

GREEN = (0, 255, 0) 
BLUE = (0, 0, 128) 
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class GameState():
    MAINMENU = 1
    GAMEPLAY = 2
    GAMEOVER = 3

gamestate = GameState.MAINMENU

# Collision Detection #####################################
def CollisionDetected(rectangleA, rectangleB):
    collided = False
    if ((rectangleA.top < rectangleB.bottom) and
    (rectangleA.bottom > rectangleB.top) and
    (rectangleA.right > rectangleB.left) and
    (rectangleA.left < rectangleB.right)):
        collided = True
    return collided

#Screen Size 
class GameWindow:
    def __init__(self):
        self.width = 1024
        self.height = 1024
        pygame.display.set_caption("Game")
        self.display = pygame.display.set_mode((self.width, self.height)) #is it called display?
gameWindow = GameWindow()

class TextSprite():
    def __init__(self, text, fontFamily, fontSize, foreColor, backColor, x, y):
        self.font = pygame.font.Font(fontFamily, fontSize)
        self.text = self.font.render(text, True, foreColor, backColor)
        self.rect = self.text.get_rect()
        self.rect.center = (x, y)
    def draw(self):
        gameWindow.display.blit(self.text, self.rect)
texts = {
    'start': TextSprite('START', 'freesansbold.ttf', 30, GREEN, BLUE, gameWindow.width//2, gameWindow.height-100), 
    'gameover': TextSprite('Press SPACE', 'freesansbold.ttf', 30, GREEN, BLACK, gameWindow.width//2, gameWindow.width-100)
}

class ImageSprite():
    def __init__(self, image, width, height, realX, realY):
        self.image = pygame.transform.scale(pygame.image.load(image), (width, height))
        self.rect = self.image.get_rect()
        self.rect.center = (realX, realY)
        self.drawable = True
    def draw(self):
        if self.drawable:
            gameWindow.display.blit(self.image, self.rect)

#Player movement from 0,0
camera_pos = (0, 0)
background = ImageSprite("media/background.png", 4096, 4096, 0, 0)

class Player(ImageSprite):
    def __init__(self, image, width, height, realX, realY):
        extClass = super()
        extClass.__init__(image, width, height, realX, realY)
        self.health = 6
player = Player('media/player.png', 75, 75, gameWindow.width//2,gameWindow.height//2)

class Entity(ImageSprite):
    def __init__(self, image, width, height, realX, realY, type=None):
        extClass = super()
        extClass.__init__(image, width, height, realX, realY)
        self.type = type
entities = [
    Entity('media/cannibal.png', 90, 90, -100, -100)
]

class Rock(ImageSprite):
    def __init__(self, image, width, height, realX, realY):
        extClass = super()
        extClass.__init__(image, width, height, realX, realY)
        self.health = 100
rocks = []

heartImageSize = 9 * 5
heartsSpacing = 60
hearts = [
    [ImageSprite('media/heart.png', heartImageSize, heartImageSize, 50, 50), ImageSprite('media/half_heart.png', heartImageSize, heartImageSize, 50, 50)], 
    [ImageSprite('media/heart.png', heartImageSize, heartImageSize, 50+heartsSpacing, 50), ImageSprite('media/half_heart.png', heartImageSize, heartImageSize, 50+heartsSpacing, 50)], 
    [ImageSprite('media/heart.png', heartImageSize, heartImageSize, 50+heartsSpacing+heartsSpacing, 50), ImageSprite('media/half_heart.png', heartImageSize, heartImageSize, 50+heartsSpacing+heartsSpacing, 50)]
]

#UFO BIG ENDING
endPic = pygame.image.load("media/cannibal.png")
startRect = endPic.get_rect() 
startRect.center = (120,100)
endRect = endPic.get_rect() 
endRect.center = (gameWindow.width//2,gameWindow.height//2)

#Sound Effect Variables (sound not supported in repl.it)
laserSound = pygame.mixer.Sound('media/laser.wav') 

def drawAll():
    if gamestate == GameState.MAINMENU:
        background.draw()
        texts['start'].draw()
        gameWindow.display.blit(endPic,startRect)

    elif gamestate == GameState.GAMEPLAY:
        background.draw()
        player.draw()
        for heart in hearts:
            heart[0].draw()
        for entity in entities:
            entity.draw()
        for rock in rocks:
            rock.draw()
    
    elif gamestate == GameState.GAMEOVER:
        endPic2 = pygame.transform.rotate(endPic, 180)
        gameWindow.display.blit(endPic2,endRect)
        texts['gameover'].draw()


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == K_SPACE:
                print('hi')
        if event.type == pygame.QUIT:
            running = False
    gameWindow.display.fill(BLACK)
    keys = pygame.key.get_pressed()
    mouseXY = pygame.mouse.get_pos()
    #Read left mouse button
    mouseClick = pygame.mouse.get_pressed()[0] 
    #Read all 3 mouse buttons
    mouseMCR = pygame.mouse.get_pressed()


    if gamestate == GameState.MAINMENU:
        if keys[pygame.K_RETURN]:
            gamestate = GameState.GAMEPLAY
        if mouseClick and texts['start'].rect.collidepoint(mouseXY):
            gamestate = GameState.GAMEPLAY
            entities[0].rect.center = (-250,-650)
            player.rect.center = (gameWindow.width//2,gameWindow.height//2)
            background.rect.center = (gameWindow.width//2,gameWindow.height//2)

    elif gamestate == GameState.GAMEPLAY:
        #move canabal
        dist = math.sqrt((player.rect.centerx-entities[0].rect.centerx)**2 + (player.rect.centery-entities[0].rect.centery)**2)
        if dist < 550:
            oldRect = pygame.Rect(entities[0].rect.x, entities[0].rect.y, entities[0].rect.width, entities[0].rect.height)
            if entities[0].rect.centerx > player.rect.centerx:
                entities[0].rect.move_ip(-3,0)
            if entities[0].rect.centerx < player.rect.centerx:
                entities[0].rect.move_ip(3,0)
            for rock in rocks:
                if CollisionDetected(entities[0].rect, rock.rect):
                    entities[0].rect = oldRect
                    break
        if entities[0].rect.centery > player.rect.centery:
            entities[0].rect.move_ip(0,-3)
        if entities[0].rect.centery < player.rect.centery:
            entities[0].rect.move_ip(0,3)

        for rock in rocks:
          if CollisionDetected(entities[0].rect, rock.rect):
            entities[0].rect = oldRect
            break
        #Example of moving a rocket sprite left and right with keyboard
        if keys[pygame.K_LEFT]:
            camera_pos[1] -= 1
            background.rect.move_ip(10,0)
            entities[0].rect.move_ip(10,0)
            for rock in rocks:
                rock.rect.move_ip(10,0)
 
        if keys [pygame.K_RIGHT]:
            camera_pos[1] += 1
            background.rect.move_ip(-10,0)
            for rock in rocks:
                rock.rect.move_ip(-10,0)
            entities[0].rect.move_ip(-10,0)
        if keys[pygame.K_UP]:
            camera_pos[0] -= 1
            background.rect.move_ip(0,10)
            for rock in rocks:
                rock.rect.move_ip(0,10)
            entities[0].rect.move_ip(0,10)
        if keys [pygame.K_DOWN]:
            camera_pos[0] += 1
            background.rect.move_ip(0,-10)
            for rock in rocks:
                rock.rect.move_ip(0,-10)
            entities[0].rect.move_ip(0,-10)
            
        if keys [pygame.K_SPACE]:
            rocks.append(Rock('rock.png', 826//10, 662//10, player.rect.centerx, player.rect.centery))

        colliding = CollisionDetected(entities[0].rect, player.rect) 
        if colliding:
            gamestate = GameState.GAMEOVER
    
    elif gamestate == GameState.GAMEOVER:
        if keys[pygame.K_SPACE]:
            gamestate = GameState.MAINMENU


    drawAll()

    pygame.display.flip()

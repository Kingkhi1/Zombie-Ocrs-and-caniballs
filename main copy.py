import pygame
import math
from pygame.locals import *
from pygame import mixer
pygame.init()

GREEN = (0, 255, 0) 
BLUE = (0, 0, 128) 
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
water = (33, 150, 243)

class GameState():
    MAINMENU = 1
    GAMEPLAY = 2
    GAMEOVER = 3

class Items:
    AIR = 0
    ROCK = 1
    PICKAXE = 2
    AXE = 3

tools = [Items.ROCK, Items.AIR, Items.ROCK, Items.AIR, Items.AIR, Items.AIR, Items.AIR, Items.AIR]
hotbarSelection = 0
airPic = pygame.transform.scale(pygame.image.load('media/empty.png'), (80, 80))
rockPic = pygame.transform.scale(pygame.image.load('media/rock.png'), (80, 80))
selectionPic = pygame.transform.scale(pygame.image.load('media/selection.png'), (80, 80))

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
            gameWindow.display.blit(self.image, pygame.Rect(self.rect.x-camera_pos[0], self.rect.y-camera_pos[1], self.rect.width, self.rect.height))
    def drawUI(self):
        if self.drawable:
            gameWindow.display.blit(self.image, pygame.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height))

#Player movement from 0,0
camera_pos = [2048, 2048]
background = ImageSprite("media/background.png", 4096, 4096, 2048, 2048)
print(background.rect)

class Player(ImageSprite):
    def __init__(self, image, width, height, realX, realY, speed):
        extClass = super()
        extClass.__init__(image, width, height, realX, realY)
        self.health = 6
        self.speed = speed
player = Player('media/player.png', 75, 75, 2048+gameWindow.width//2,2048+gameWindow.height//2, 10)

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
            heart[0].drawUI()
        for entity in entities:
            entity.draw()
        for rock in rocks:
            rock.draw()
        for x in range(len(tools)):
            if tools[x] == Items.AIR:
                aTool = airPic
            elif tools[x] == Items.ROCK:
                aTool = rockPic
            gameWindow.display.blit(aTool, pygame.Rect((80*x)+192, gameWindow.height-100, 80, 80))
        gameWindow.display.blit(selectionPic, pygame.Rect((80*hotbarSelection)+192, gameWindow.height-100, 80, 80))
        
    
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
            entities[0].rect.center = (1000,1000)
            #player.rect.center = (gameWindow.width//2,gameWindow.height//2)
            #background.rect.center = (gameWindow.width//2,gameWindow.height//2)

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
        speed = player.speed
        print(background.image.get_at((camera_pos[0]+gameWindow.width//2, camera_pos[1]+gameWindow.height//2))[2], water[2])
        if background.image.get_at((camera_pos[0]+gameWindow.width//2, camera_pos[1]+gameWindow.height//2))[0]==water[0] and background.image.get_at((camera_pos[0]+gameWindow.width//2, camera_pos[1]+gameWindow.height//2))[1]==water[1] and background.image.get_at((camera_pos[0]+gameWindow.width//2, camera_pos[1]+gameWindow.height//2))[2]==water[2]:
            print("True")
            speed=speed//2
        if keys[pygame.K_LEFT]:
            camera_pos[0] -= 10
            player.rect.move_ip(-speed,0)
 
        if keys [pygame.K_RIGHT]:
            camera_pos[0] += 10
            player.rect.move_ip(speed,0)
        if keys[pygame.K_UP]:
            camera_pos[1] -= 10
            player.rect.move_ip(0,-speed)
        if keys [pygame.K_DOWN]:
            camera_pos[1] += 10
            player.rect.move_ip(0,speed)
            
        if keys [pygame.K_SPACE]:
            if tools[hotbarSelection] == Items.ROCK:
                rocks.append(Rock('media/rock.png', 826//10, 662//10, player.rect.centerx, player.rect.centery))
                tools[hotbarSelection] = Items.AIR

        if keys [pygame.K_1]:
            hotbarSelection = 0
        if keys [pygame.K_2]:
            hotbarSelection = 1
        if keys [pygame.K_3]:
            hotbarSelection = 2
        if keys [pygame.K_4]:
            hotbarSelection = 3
        if keys [pygame.K_5]:
            hotbarSelection = 4
        if keys [pygame.K_6]:
            hotbarSelection = 5
        if keys [pygame.K_7]:
            hotbarSelection = 6
        if keys [pygame.K_8]:
            hotbarSelection = 7

        colliding = CollisionDetected(entities[0].rect, player.rect) 
        if colliding:
            gamestate = GameState.GAMEOVER
    
    elif gamestate == GameState.GAMEOVER:
        if keys[pygame.K_SPACE]:
            gamestate = GameState.MAINMENU


    drawAll()

    pygame.display.flip()

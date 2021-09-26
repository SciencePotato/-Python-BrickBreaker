import pygame
import random
import sys

#### #### #### STATIC VARIABLE #### #### ####
DISPLAY = [1040, 720]
BRICK_SIZE = [80, 40]
SPACING = 5
POWER_UP = ["Speed", "MoreBalls", "BiggerPaddle"]

#### #### #### VARIABLE #### #### #### ####
brickList = []
ballList = []
BrickNum = 0



#### #### #### CLASSES #### #### #### ####
class Player:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)
        self.color = (250, 120, 60)
        self.rect = pygame.Rect(self.x, self.y, 130, 25)
        self.press_left = False
        self.press_right = False
        self.speed = 4
        self.velocityX = 0

    def drawplayer(self):
        pygame.draw.rect(screen, self.color, self.rect)

    def update(self):
        self.velocityX = 0
        if self.press_left and not self.press_right:
            self.velocityX = -self.speed
        
        if self.press_right and not self.press_left:
            self.velocityX = self.speed
    
        if self.x <= 0: 
            self.x = 1

        if self.x >= 1040 - 130:
            self.x = 1040 - 129

        self.x += self.velocityX

        self.rect = pygame.Rect(int(self.x), int(self.y), 130, 25)


class Ball:
    def __init__(self):
        self.x = 520
        self.y = 360
        self.sX = random.randint(-3,3)
        self.sY = 4
        self.rect = pygame.Rect(self.x, self.y, 20, 20)

        
    def render(self):
        pygame.draw.rect(screen, (0, 255, 0), self.rect)
    
    def update(self):
        self.rect = pygame.Rect(int(self.x), int(self.y), 20, 20)

    def checkPlayer(self):
        return player.rect.colliderect(self.rect)
        
    def checkBrick():
        #for loop
        #colliderect
        print("hello")

    def checkBound(self):
        if self.x <= 0 or self.x >= 1040 - 20:
            self.sX = -self.sX 

        if self.y <= 0: 
            self.sY = -self.sY
        
        if self.y >= 720:
            pygame.quit()

    def update(self):
        self.x += self.sX
        self.y += self.sY
        self.rect = pygame.Rect(int(self.x), int(self.y), 20, 20)

    def bounce_A(self):
        if (ball.y > 576):
            self.sY = -3
            self.sX = -self.sX
        self.sX = random.randint(-3, 3)
        self.sY = -self.sY

    def bounce_B(self):
        self.sY = -self.sY
 


class brick:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.touched = False
        self.rect = pygame.Rect(x, y , BRICK_SIZE[0], BRICK_SIZE[1]) 
    """
    def getXLoc(self):
        return self.x

    def getYLoc(self):
        return self.y
    """
    def getTouch(self):
        return self.touched

    def setTouch(self):
        self.touched = True

    def checkBrick(self):
        return ball.rect.colliderect(self.rect)

    def render(self):
        pygame.draw.rect(screen, (255, 0, 0), self.rect)
        pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, BRICK_SIZE[0], BRICK_SIZE[1]), width=1)
        


#### #### #### FUNCTIONS #### #### #### ####

def createBricks():
    for yLoc in range(2, (int)((DISPLAY[1] / 3) / BRICK_SIZE[1])):
        for xLoc in range(1, (int)(DISPLAY[0] / (BRICK_SIZE[0]) - 1)):
            brickList.append(brick(xLoc * BRICK_SIZE[0], yLoc * BRICK_SIZE[1]))
        

def drawBricks():
    for i in brickList:
        if not i.getTouch():
            i.render()


"""
def drawSingleBrick(x, y, color):
    pygame.draw.rect(screen, color, pygame.Rect(x, y, BRICK_SIZE[0], BRICK_SIZE[1]), width=0)
    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(x, y, BRICK_SIZE[0], BRICK_SIZE[1]), width=2)


def drawBricks():
    for y in range(1, (int) ((DISPLAY[1]/3)/ BRICK_SIZE[1])):
        for x in range(1,(int)(DISPLAY[0]/(BRICK_SIZE[0]))-1):
            drawSingleBrick(x*BRICK_SIZE[0], y*BRICK_SIZE[1], (255, 0, 0))

def drawSingleBrick(x, y, color):
    pygame.draw.rect(screen, color, pygame.Rect(x, y, BRICK_SIZE[0], BRICK_SIZE[1]), width=0)
    pygame.draw.rect(screen, (0,0,0), pygame.Rect(x, y, BRICK_SIZE[0], BRICK_SIZE[1]), width=2)

 """   


#### #### #### Main Loop #### #### ####
if __name__ == "__main__":
    pygame.init()    

    pygame.mixer.music.load('acoustic-guitars-ambient-uplifting-background-music-for-videos-5642.wav')
    pygame.mixer.music.play(-1)
    hitNormal = pygame.mixer.Sound('drum-hitnormal.wav')


    screen = pygame.display.set_mode(DISPLAY)
    clock = pygame.time.Clock()
    pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])
    pygame.display.set_caption("Brick Thing")

    player = Player(DISPLAY[0]/2.25, DISPLAY[1]/1.25)
    ball = Ball()
    createBricks()
    BrickNum = len(brickList)

    running = True
    while running:

        #boundary to prevent the paddle from going out of the screen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    player.press_left = True
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    player.press_right = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    player.press_left = False
                if event.key == pygame.K_RIGHT or event.key == ord('d'): 
                    player.press_right = False

        screen.fill((255, 255, 255))

        drawBricks()

        ball.render()
        if ball.checkPlayer():
            ball.bounce_A()
            pygame.mixer.Sound.play(hitNormal)

        for i in brickList:
            if i.checkBrick() and not i.getTouch():
                ball.bounce_B()
                pygame.mixer.Sound.play(hitNormal)
                BrickNum -= 1
                i.setTouch()
                break

        if BrickNum == 0:
            pygame.quit()

        ball.checkBound()

        ball.update()
        
        player.drawplayer()
        player.update()
        
        clock.tick(60)
        
        pygame.display.update()
        # pygame.display.flip()

    pygame.quit()
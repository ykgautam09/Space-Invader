import pygame,math
import random
import sys

pygame.init()
pygame.display.set_caption('Space Explorer')
pygame.display.set_icon(pygame.image.load('./images/rocket.png'))

screen_x = 700
screen_y = 467
screen = pygame.display.set_mode((screen_x, screen_y))

playerImg = pygame.image.load("./images/space.png")
positionP_dx = 0
positionP_dy = 0
positionP_x = int((screen_x/2)-32)
positionP_y = screen_y-100


def player():
    screen.blit(playerImg, (positionP_x, positionP_y))


positionB_dx = 0
positionB_dy = 0.6
positionB_x = positionP_x + 32
positionB_y = 0
bulletState = 'ready'
bulletImg = pygame.image.load('./images/bullet.png')


def shoot(x, y):
    global positionB_dy, bulletState, positionB_y, positionB_x
    positionB_x = x
    bulletState = 'fired'
    positionB_y = y
    positionB_y -= positionB_dy
    screen.blit(bulletImg, (x+16, positionB_y))


positionE_dx = 0.6
positionE_dy = 0
positionE_x = random.randint(0, screen_x-64)
positionE_y = random.randint(20, 100)


def updateE():
    global enemyImg
    path = './images/'+str(random.randint(1, 3))+'.png'
    enemyImg = pygame.image.load(path)


def enemy():
    global positionE_x, positionE_dx
    positionE_x += positionE_dx
    screen.blit(enemyImg, (positionE_x, positionE_y))


def isCollision(ex,ey,bx,by):
    if math.sqrt((ex-bx)**2+(ey-by)**2)<=32:
        return True
    else:
        False

updateE()

backImg = pygame.image.load('./images/back1.jpg')
while True:
    # paint background
    screen.fill((0, 0, 50))
    screen.blit(backImg, (0, 0))

    #reload and quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        # detect key for player movement and bullet
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                positionP_dx = -0.8
            if event.key == pygame.K_RIGHT:
                positionP_dx = 0.8
            if event.key == pygame.K_UP:
                positionP_dy = -0.8
            if event.key == pygame.K_DOWN:
                positionP_dy = 0.8
            if event.key == pygame.K_SPACE:
                shoot(positionP_x+16, positionP_y-30)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                positionP_dx = 0
            if event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                positionP_dy = 0

    # movement player
    positionP_x += positionP_dx
    positionP_y += positionP_dy
    if positionP_x <= 0:
        positionP_x = 0
    if positionP_x >= screen_x-64:
        positionP_x = screen_x-64
    if positionP_y <= 0:
        positionP_y = 0
    if positionP_y >= screen_y-64:
        positionP_y = screen_y-64

    # enemy movement
    if positionE_x <= 0:
        positionE_dx = 0.6
        positionE_dy = 40
        positionE_y += positionE_dy

    if positionE_x >= screen_x-64:
        positionE_dx = -0.5
        positionE_dy = 40
        positionE_y += positionE_dy

    # bullet movement
    if positionB_y<=0:
        bulletState='ready'
        positionB_y=positionP_y


    if bulletState == 'fired':
        positionB_y -= positionB_dy
        shoot(positionB_x, positionB_y)

    collide=isCollision(positionE_x+32,positionE_y+40,positionB_x+16,positionB_y)
    if collide==True:
        bulletState='ready'
        positionB_y=positionP_y-30
        positionB_x=positionP_x+16
        positionE_x=random.randint(0, screen_x-64)
        positionE_y=random.randint(20, 100)
    enemy()
    player()

    pygame.display.update()

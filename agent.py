import pygame

from configparser import ConfigParser

config = ConfigParser()
config.read('./.config')
SCREEN_WIDTH = int(config['DEFAULT']['SCREEN_WIDTH'])
SCREEN_HEIGHT = int(config['DEFAULT']['SCREEN_HEIGHT'])
ROCKET_SPEED = config['DEFAULT']['ROCKET_SPEED']
ROCKET_SIZE = config['DEFAULT']['ROCKET_SIZE']
SPACESHIP_IMAGE = config['DEFAULT']['SPACESHIP_IMAGE']


class Spaceship(pygame.sprite.Sprite):
    def __init__(self, x, y) -> None:
        super().__init__()
        # self.x = x
        # self.y = y
        self.image = pygame.image.load(SPACESHIP_IMAGE)
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self) -> None:
        speed = int(float(ROCKET_SPEED))

        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= speed
        if key[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += speed

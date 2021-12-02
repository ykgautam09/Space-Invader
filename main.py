import os
import random
import pygame
from configparser import ConfigParser

config = ConfigParser()
config.read('./.config')
SCREEN_WIDTH = int(config['DEFAULT']['SCREEN_WIDTH'])
SCREEN_HEIGHT = int(config['DEFAULT']['SCREEN_HEIGHT'])
WINDOW_CAPTION = config['DEFAULT']['WINDOW_CAPTION']
WINDOW_ICON_PATH = config['DEFAULT']['WINDOW_ICON_PATH']
BACKGROUND_IMAGE_PATH = config['DEFAULT']['BACKGROUND_IMAGE_PATH']
ROCKET_SPEED = config['DEFAULT']['SPACESHIP_SPEED']
SPACESHIP_IMAGE = config['DEFAULT']['SPACESHIP_IMAGE']
BULLET_IMAGE = config['DEFAULT']['BULLET_IMAGE']
BULLET_SPEED = config['DEFAULT']['BULLET_SPEED']
RELOAD_TIME = config['DEFAULT']['RELOAD_TIME']
ALIEN_FOLDER_PATH = config['DEFAULT']['ALIEN_FOLDER_PATH']
ALIEN_SPEED = config['DEFAULT']['ALIEN_SPEED']
ALIEN_BOMB_IMAGE = config['DEFAULT']['ALIEN_BOMB_IMAGE']

pygame.init()
# Audio configuration
pygame.mixer.init()


class Audio:
    def __init__(self, path) -> None:
        self.audio = pygame.mixer.Sound(path)
        self.audio.set_volume(0.2)


class Screen:
    game_over = 0  # not over:0,loss:-1,won:1

    def __init__(self):
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT
        self.screen = self.set_window()
        self.fps = 60
        self.cooldown = 3
        self.clock = pygame.time.Clock()
        self.time = pygame.time.get_ticks()
        self.image = pygame.image.load(BACKGROUND_IMAGE_PATH)
        self.font_bold = pygame.font.Font(
            'resources/fonts/Petrona-Bold.ttf', 60)
        self.font_light = pygame.font.Font(
            'resources/fonts/Petrona-Italic.ttf', 30)
        pygame.display.set_caption(WINDOW_CAPTION)
        pygame.display.set_icon(pygame.image.load(WINDOW_ICON_PATH))

    def set_window(self):
        return pygame.display.set_mode((self.width, self.height))

    def draw_background(self):
        self.screen.blit(self.image, (0, 0))

    def draw_text(self, text, font, pos):
        img = font.render(text, True, (255, 255, 255))
        self.screen.blit(img, pos)

    # def display_score(self):
    #     self.screen.blit(pygame.font.)
    # def status(self,message,size):

    @staticmethod
    def update_screen() -> None:
        pygame.display.update()


screen = Screen()


# agent classes
# Spaceship class
class Spaceship(pygame.sprite.Sprite):
    def __init__(self, x, y, health) -> None:
        super().__init__()
        self.mask = None
        self.image = pygame.transform.scale(
            pygame.image.load(SPACESHIP_IMAGE), (64, 50))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.health = health
        self.remaining_health = health
        self.last_shot = pygame.time.get_ticks()

    def update(self):
        screen.game_over = 0

        speed = int(ROCKET_SPEED)
        reload_time = int(RELOAD_TIME)  # in milliseconds default 500
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= speed
        if key[pygame.K_RIGHT] and self.rect.right < screen.width:
            self.rect.x += speed

        self.mask = pygame.mask.from_surface(self.image)

        current_time = pygame.time.get_ticks()
        # on space press create and shoot bullet
        if key[pygame.K_SPACE] and current_time - self.last_shot > reload_time:
            Audio('resources/Audio/bullet.mp3').audio.play()
            bullets_group.add(Bullets(self.rect.centerx, self.rect.top + 5))
            self.last_shot = current_time

        # create health bar
        pygame.draw.rect(screen.screen, (255, 0, 0),
                         (self.rect.x, self.rect.bottom + 10, self.rect.width, 8))
        if self.remaining_health:
            pygame.draw.rect(screen.screen, (0, 255, 0),
                             (self.rect.x, self.rect.bottom + 10,
                              int(self.rect.width * (self.remaining_health / self.health)), 8))
        if spaceship.remaining_health <= 0:
            explosion_group.add(
                Explosion(self.rect.centerx, self.rect.centery, 15))
            Audio('resources/Audio/explode.mp3').audio.play()
            spaceship.kill()
            screen.game_over = -1
        return screen.game_over


# Spaceship Bullets class
class Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y) -> None:
        super().__init__()
        self.image = pygame.transform.scale(
            pygame.image.load(BULLET_IMAGE), (25, 25))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        speed = int(BULLET_SPEED)
        self.rect.y -= speed
        if self.rect.bottom < 0:
            self.kill()

        if pygame.sprite.spritecollide(self, aliens_group, True):
            self.kill()
            Audio('resources/Audio/bullet_explosion.mp3').audio.play()

            explosion_group.add(
                Explosion(self.rect.centerx, self.rect.centery, 4))

        if pygame.sprite.spritecollide(self, aliens_bomb_group, True):
            self.kill()
            explosion_group.add(
                Explosion(self.rect.centerx, self.rect.centery, 1))
            screen.game_over = -1
        return screen.game_over


# Alien class
class Alien(pygame.sprite.Sprite):
    image_paths = os.listdir(ALIEN_FOLDER_PATH)

    def __init__(self, x, y) -> None:
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(os.path.join(
            ALIEN_FOLDER_PATH, random.choice(self.image_paths))), (40, 40))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.direction = 1
        self.counter = 0

    def update(self) -> None:
        self.rect.x += self.direction * int(ALIEN_SPEED)
        self.counter += 1
        if abs(self.counter) >= 50:
            self.direction *= -1
            self.counter *= self.direction

    @staticmethod
    def draw_aliens():
        rows = 5
        cols = 9
        for row in range(rows):
            for col in range(cols):
                aliens_group.add(Alien(80 + col * 80, 60 + row * 80))


# Alien Bullets class
class AlienBomb(pygame.sprite.Sprite):
    last_shot = pygame.time.get_ticks()
    cooldown = 800  # millisecond

    def __init__(self, x, y) -> None:
        super().__init__()
        self.image = pygame.transform.scale(
            pygame.image.load(ALIEN_BOMB_IMAGE), (10, 10))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self) -> None:
        speed = int(BULLET_SPEED)
        self.rect.y += speed // 2
        if self.rect.top > screen.height:
            self.kill()
        if pygame.sprite.spritecollide(self, spaceship_group, False, pygame.sprite.collide_mask):
            self.kill()
            Audio('resources/Audio/bomb_explosion.mp3').audio.play()
            spaceship.remaining_health -= 1
            explosion_group.add(
                Explosion(self.rect.centerx, self.rect.centery, 2))


# Explosion class
class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, scale) -> None:
        super().__init__()
        self.image_list = [pygame.transform.scale(pygame.image.load(os.path.join('./resources/image/Explosion',
                                                                                 path)), (10 * scale, 10 * scale)) for
                           path in os.listdir('./resources/image/Explosion/')]
        self.index = 0
        self.image = self.image_list[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.counter = 0  # len(image_list)

    def update(self) -> None:
        speed = 3
        self.counter += 1
        if self.counter >= speed and self.index < len(self.image_list) - 1:
            self.index += 1
            self.counter = 0
            self.image = self.image_list[self.index]
        if self.index >= len(self.image_list) - 1:
            self.kill()


# initialise spaceship
spaceship = Spaceship(screen.width // 2, screen.height - 100, 3)
spaceship_group = pygame.sprite.Group()
spaceship_group.add(spaceship)

# initialise bullets
bullet = Bullets(spaceship.rect.x, spaceship.rect.y - 10)
bullets_group = pygame.sprite.Group()

# initialise Aliens
aliens_group = pygame.sprite.Group()
Alien.draw_aliens()

aliens_bomb_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()

# game loop
run = True
while run:

    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_r and screen.game_over != 0:
                # replay game
                screen.game_over = 0
                # remove all objects
                spaceship_group.empty()
                bullets_group.empty()
                aliens_bomb_group.empty()
                aliens_group.empty()
                # reinitialise all object
                Alien.draw_aliens()
                spaceship_group.add(spaceship)
                spaceship.remaining_health = spaceship.health

    if screen.game_over == 0:
        # set fps control refresh rate
        screen.clock.tick(screen.fps)
        screen.draw_background()
        # no enemy remaining : player won

        current_time = pygame.time.get_ticks()
        if screen.cooldown <= 0:

            # randomly drop bomb from alien
            if current_time - AlienBomb.last_shot > AlienBomb.cooldown and len(aliens_bomb_group) < 8 and len(
                    aliens_group):
                attacking_alien = random.choice(aliens_group.sprites())
                aliens_bomb_group.add(
                    AlienBomb(attacking_alien.rect.centerx, attacking_alien.rect.bottom))
                AlienBomb.last_shot = current_time

            # update agents
            bullets_group.update()
            screen.game_over = spaceship.update()
            aliens_group.update()
            aliens_bomb_group.update()

        # draw agents
        bullets_group.draw(screen.screen)
        spaceship_group.draw(screen.screen)
        aliens_bomb_group.draw(screen.screen)
        aliens_group.draw(screen.screen)
        explosion_group.draw(screen.screen)

        if len(aliens_group) == 0:
            screen.game_over = 1

        if screen.cooldown > 0:
            screen.draw_text('GET READY!', screen.font_bold,
                             (screen.width // 2 - 150, screen.height // 2 - 100))
            screen.draw_text(str(screen.cooldown), screen.font_bold,
                             (screen.width // 2 - 30, screen.height // 2))
            if current_time - screen.time > 1000:
                screen.time = current_time
                screen.cooldown -= 1
    explosion_group.update()

    if screen.game_over == 1:
        screen.draw_text('YOU WON!', screen.font_bold,
                         (screen.width // 2 - 150, screen.height // 2 - 100))
        screen.draw_text('press R to replay', screen.font_light,
                         (screen.width // 2 - 100, screen.height // 2 - 50))
    if screen.game_over == -1:
        screen.draw_text('YOU LOSE!', screen.font_bold,
                         (screen.width // 2 - 150, screen.height // 2 - 100))

        screen.draw_text('press R to replay', screen.font_light,
                         (screen.width // 2 - 100, screen.height // 2 - 50))

    screen.update_screen()

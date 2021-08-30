import random
import pygame

pygame.init()

SCREEN_RECT = pygame.Rect(0, 0, 480, 700)
FPS = 60
CREAT_ENEMY_SPRITES = pygame.USEREVENT
FIRE_EVENT = pygame.USEREVENT + 1
SPEED_X, SPEED_Y = 2, 3
GAMEOVER_RECT = pygame.Rect(SCREEN_RECT.centerx - 150, 300, 300, 41)
pygame.font.init()
fontObj = pygame.font.SysFont("Microsoft Ya Hei.ttf", 40)


class GameSprite(pygame.sprite.Sprite):
    def __init__(self, image_name, speed_x=0, speed_y=1):
        super().__init__()
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.y += self.speed_y
        self.rect.x += self.speed_x


class Background(GameSprite):
    def __init__(self, is_alt=False):
        super().__init__("./images/background.png")
        if is_alt:
            self.rect.bottom = 0

    def update(self):
        super().update()
        if self.rect.y >= SCREEN_RECT.height:
            self.rect.bottom = 0


class Enemy(GameSprite):
    def __init__(self):
        self.modnum = 1
        self.imagename = "./images/enemy1.png"
        self.update_num = 0
        super().__init__(self.imagename)
        self.rect.bottom = 0
        self.rect.x = random.random() * (480 - 57)
        self.speed_y = random.random() * 2 + 1

    def update(self):
        super().update()
        self.update_num += 1
        if self.modnum == 1:
            self.image = pygame.image.load("./images/enemy1.png")
            self.update_num = 0
        elif self.modnum == 2:
            self.image = pygame.image.load("./images/enemy1_down1.png")
            if self.update_num == 3:
                self.modnum += 1
                self.update_num = 0
        elif self.modnum == 3:
            self.image = pygame.image.load("./images/enemy1_down2.png")
            if self.update_num == 3:
                self.modnum += 1
                self.update_num = 0
        elif self.modnum == 4:
            self.image = pygame.image.load("./images/enemy1_down3.png")
            if self.update_num == 3:
                self.modnum += 1
                self.update_num = 0
        elif self.modnum == 5:
            self.image = pygame.image.load("./images/enemy1_down4.png")
            if self.update_num == 3:
                self.modnum += 1
                self.update_num = 0
        else:
            self.kill()
        if self.rect.y >= SCREEN_RECT.height:
            self.kill()


class Hero(GameSprite):
    def __init__(self):
        super().__init__("./images/me1.png", 0)
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.bottom = SCREEN_RECT.height - 120
        self.bullets_num = 5
        self.image_num = 1.2
        self.num = 0
        self.bullets = pygame.sprite.Group()

    def update(self):
        self.image = pygame.image.load("./images/me%d.png" % (self.image_num // 1))
        if self.image_num <= 1.2:
            self.num = 0.1
        elif self.image_num >= 2.8:
            self.num = -0.1
        self.image_num += self.num
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.right > SCREEN_RECT.right:
            self.rect.right = SCREEN_RECT.right
        if self.rect.y < 0:
            self.rect.y = 0
        if self.rect.bottom > SCREEN_RECT.bottom:
            self.rect.bottom = SCREEN_RECT.bottom
        self.speed_x, self.speed_y = 0, 0

    def fire(self):
        if self.bullets_num > 0:
            bullet = Bullet()
            self.bullets.add(bullet)
            bullet.rect.centerx = self.rect.centerx
            bullet.rect.bottom = self.rect.y
            self.bullets_num -= 1
            return True
        else:
            return False


class Bullet(GameSprite):
    def __init__(self):
        super().__init__("./images/bullet1.png", 0, -2)

    def update(self):
        super().update()
        if self.rect.bottom < 0:
            self.kill()

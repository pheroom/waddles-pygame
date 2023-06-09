from math import pi, sin, cos
from pygame import *
from config import config
from util import transformImg
import pyganim
import monsters
import random

class Platform(sprite.Sprite):
    def __init__(self, x, y, img = None):
        sprite.Sprite.__init__(self)
        self.image = (img and transformImg(img))
        self.rect = Rect(x, y, config.PLATFORM_WIDTH, config.PLATFORM_HEIGHT)

class Rectangle(sprite.Sprite):
    def __init__(self, x, y, w, h):
        sprite.Sprite.__init__(self)
        self.image = Surface((w,h))
        self.rect = Rect(x, y, w, h)

    def update(self, x, y):
        self.rect.x = x
        self.rect.y = y

class Amount(sprite.Sprite):
    def __init__(self, x, y, amount, remove, color = '#ffffff'):
        sprite.Sprite.__init__(self)
        self.startX = x + random.randint(0, config.PLATFORM_WIDTH//3) * (-1 if random.randint(0,1) else 1)
        self.startY = y
        self.remove = remove
        self.image = font.Font('./emulogic.ttf', round(12 * config.PLATFORM_WIDTH/32)).render(str(amount), False, color)
        # self.image = font.Font('./emulogic.ttf', 12).render(str(amount), False, color)
        self.rect = Rect(self.startX, self.startY, config.PLATFORM_WIDTH, config.PLATFORM_HEIGHT)
        self.yvel = -4

    def update(self):
        self.rect.y += self.yvel
        if self.rect.y + 50 <= self.startY:
            self.remove(self)

class ActPlatform(Platform):
    def __init__(self, x, y, strength, needAction, img = None):
        Platform.__init__(self, x, y, img)
        self.needAction = needAction
        self.strength = strength
        self.end = False

    def act(self):
        if self.end:
            return

        if self.strength > 0:
            self.strength -= 1
            self.needAction(self.rect.x, self.rect.y)
        if self.strength <= 0:
            self.image = transformImg("./images/empty_coin_block.png")
            self.end = True


class Princess(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        boltAnim = []
        self.image = Surface((config.PLATFORM_WIDTH, config.PLATFORM_HEIGHT))
        self.image.fill(Color(config.COLOR))
        self.image.set_colorkey(Color(config.COLOR))
        for anim in config.ANIMATION_PRINCESS:
            boltAnim.append((transformImg(anim), config.ANIMATION_STAY_DELAY))
        self.boltAnim = pyganim.PygAnimation(boltAnim)
        self.boltAnim.play()

    def update(self):
        self.image.fill(Color(config.COLOR))
        self.boltAnim.blit(self.image, (0, 0))

class Heart(sprite.Sprite):
    def __init__(self, x, y, whenDead, removeDeepPlatform):
        sprite.Sprite.__init__(self)
        self.rect = Rect(x, y - config.PLATFORM_HEIGHT, config.PLATFORM_WIDTH, config.PLATFORM_HEIGHT)
        boltAnim = []
        self.image = Surface((config.PLATFORM_WIDTH, config.PLATFORM_HEIGHT))
        self.image.set_colorkey(Color(config.COLOR))
        for anim in config.ANIMATION_FLOWER:
            boltAnim.append((transformImg(anim), 0.1))
        self.boltAnim = pyganim.PygAnimation(boltAnim)
        self.boltAnim.play()
        self.removeDeepPlatform = removeDeepPlatform
        self.whenDead = whenDead
        self.id = random.random()

    def update(self):
        self.image.fill(Color(config.COLOR))
        self.boltAnim.blit(self.image, (0, 0))

    def die(self):
        self.removeDeepPlatform(self)
        self.whenDead(self)
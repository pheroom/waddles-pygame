from pygame import *
from config import config
from util import transformImg
import pyganim
import random

class Platform(sprite.Sprite):
    def __init__(self, x, y, img = None):
        sprite.Sprite.__init__(self)
        self.image = (img and transformImg(img)) or transformImg("images/brick.png")
        self.rect = Rect(x, y, config.PLATFORM_WIDTH, config.PLATFORM_HEIGHT)

class PlatformCoin(sprite.Sprite):
    def __init__(self, x, y, remove, img = None):
        sprite.Sprite.__init__(self)
        self.image = (img and transformImg(img)) or transformImg("images/coin.png")
        self.rect = Rect(x, y, config.PLATFORM_WIDTH, config.PLATFORM_HEIGHT)
        self.remove = remove

    def die(self):
        self.remove(self)

class Coin(sprite.Sprite):
    def __init__(self, x, y, remove):
        sprite.Sprite.__init__(self)
        self.startX = x
        self.startY = y
        self.remove = remove
        self.image = Surface((config.PLATFORM_WIDTH, config.PLATFORM_HEIGHT))
        self.image = transformImg("images/coin1.png")
        self.rect = Rect(x, y, config.PLATFORM_WIDTH, config.PLATFORM_HEIGHT)
        boltAnim = []
        for anim in config.ANIMATION_COIN:
            boltAnim.append((transformImg(anim), 0.2))
        self.boltAnim = pyganim.PygAnimation(boltAnim)
        self.boltAnim.play()
        self.yvel = -7

    def update(self):
        self.boltAnim.blit(self.image, (0, 0))
        self.rect.y += self.yvel
        if self.rect.y + 80 <= self.startY:
            self.yvel = -self.yvel
        if (self.startY < self.rect.y):
            self.remove(self)

class Bullet(sprite.Sprite):
    def __init__(self, x, y, owner, rightDirection, remove, img):
        sprite.Sprite.__init__(self)
        self.owner = owner
        self.startX = x
        self.remove = remove
        self.rightDirection = rightDirection
        self.image = Surface((config.PLATFORM_WIDTH, config.PLATFORM_HEIGHT))
        w, h = img.get_rect()[2], img.get_rect()[3]
        self.image = transform.scale(img, (13 * config.PLATFORM_WIDTH / 32 * w/h, 13 * config.PLATFORM_HEIGHT / 32))
        if not rightDirection:
            self.image = transform.rotate(self.image, 180)
        w, h = self.image.get_rect()[2], self.image.get_rect()[3]
        self.rect = Rect(x, y - h/2, w, h)
        self.xvel = 7

    def die(self):
        self.remove(self)

    def update(self):
        self.rect.x += self.xvel * (1 if self.rightDirection else -1)
        if abs(self.rect.x - self.startX) > 500:
            self.remove(self)

class Sword(sprite.Sprite):
    def __init__(self, x, y, orb):
        sprite.Sprite.__init__(self)
        # self.image = Surface((config.HERO_WIDTH + orb, config.HERO_HEIGHT))
        self.image = Surface((0, 0))
        self.rect = Rect(x, y, config.HERO_WIDTH + orb, config.HERO_HEIGHT)

    def update(self, x, y):
        self.rect.x = x
        self.rect.y = y

class Amount(sprite.Sprite):
    def __init__(self, x, y, amount, remove, color = '#ffffff'):
        sprite.Sprite.__init__(self)
        self.startX = x
        self.startY = y
        self.remove = remove
        self.image = font.Font('./emulogic.ttf', round(12 * config.PLATFORM_WIDTH/32)).render(str(amount), False, color)
        # self.image = font.Font('./emulogic.ttf', 12).render(str(amount), False, color)
        self.rect = Rect(x, y, config.PLATFORM_WIDTH, config.PLATFORM_HEIGHT)
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

class BlockTeleport(Platform):
    def __init__(self, x, y, goX, goY):
        Platform.__init__(self, x, y)
        self.goX = goX
        self.goY = goY
        boltAnim = []
        for anim in config.ANIMATION_BLOCKTELEPORT:
            boltAnim.append((transformImg(anim), 0.3))
        self.boltAnim = pyganim.PygAnimation(boltAnim)
        self.boltAnim.play()

    def update(self):
        self.image.fill(Color(config.PLATFORM_COLOR))
        self.boltAnim.blit(self.image, (0, 0))


class Princess(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x , y - (config.HERO_HEIGHT - 32))
        boltAnim = []
        self.image = Surface((config.HERO_WIDTH, config.HERO_HEIGHT))
        self.image.fill(Color(config.COLOR))
        self.image.set_colorkey(Color(config.COLOR))
        for anim in config.ANIMATION_PRINCESS:
            boltAnim.append((transformImg(anim), config.ANIMATION_STAY_DELAY))
        self.boltAnim = pyganim.PygAnimation(boltAnim)
        self.boltAnim.play()

    def update(self):
        self.image.fill(Color(config.COLOR))
        self.boltAnim.blit(self.image, (0, 0))

class Flower(sprite.Sprite):
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
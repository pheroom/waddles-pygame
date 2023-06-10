from math import pi, sin, cos
from pygame import *
from config import config
from util import transformImg, BULLET_HERO, BULLET_MUSHROOM
import blocks
import monsters
import random

class Bullet(sprite.Sprite):
    def __init__(self, x, y, owner, rightDirection, remove, img):
        sprite.Sprite.__init__(self)
        self.owner = owner
        self.startX = x
        self.remove = remove
        self.rightDirection = rightDirection
        # self.image = Surface((config.PLATFORM_WIDTH, config.PLATFORM_HEIGHT))
        w, h = img.get_rect()[2], img.get_rect()[3]
        self.image = transform.scale(img, (13 * config.PLATFORM_WIDTH / 32 * w/h, 13 * config.PLATFORM_HEIGHT / 32))
        if not rightDirection:
            self.image = transform.rotate(self.image, 180)
        w, h = self.image.get_rect()[2], self.image.get_rect()[3]
        self.rect = Rect(x, y - h/2, w, h)
        self.xvel = 10

    def changeDirection(self):
        self.rightDirection = not self.rightDirection

    def changeOwner(self, newOwner):
        self.owner = newOwner

    def die(self):
        self.remove(self)

    def update(self, platforms):
        self.rect.x += self.xvel * (1 if self.rightDirection else -1)
        for p in platforms:
            if sprite.collide_rect(self, p) and p != self and (isinstance(p, blocks.ActPlatform) or isinstance(p, blocks.Platform)):
                self.die()
        if abs(self.rect.x - self.startX) > 500:
            self.remove(self)

class Sword(sprite.Sprite):
    def __init__(self, x, y, orb):
        sprite.Sprite.__init__(self)
        # self.image = Surface((orb, config.HERO_HEIGHT))
        # self.image = Surface((0, 0))
        self.attackArea = blocks.Rectangle(x, y, orb, config.HERO_HEIGHT)
        self.img = transform.scale(image.load("images/weapon/rainbow-sword.png").convert_alpha(),
                                   (30 * 1.88 * config.PLATFORM_WIDTH/64, 30 * config.PLATFORM_HEIGHT/ 64))
        self.imgR = transform.rotate(self.img, 45)
        self.imgL = transform.rotate(self.img, 135)
        self.animationStage = 0
        self.image = self.imgR
        self.orb = orb
        self.w, self.h = orb, config.HERO_HEIGHT
        self.rect = Rect(x, y, self.w, self.h)
        self.animStep = pi/180
        self.r = config.PLATFORM_WIDTH*0.2

    def update(self, rect, rightDir):
        x = rect.right if rightDir else rect.x - self.orb
        y = rect.y
        self.attackArea.update(x, y)
        self.rect.x = x + (-15 if rightDir else 20) * config.PLATFORM_WIDTH/64
        self.rect.y = y
        if self.animationStage > 0:
            if rightDir:
                self.rect.x -= 5
                self.image = transform.rotate(self.img, self.animationStage)
            else:
                self.image = transform.rotate(self.img, 180 - self.animationStage)
                self.rect.x += self.w - self.image.get_width()
            self.rect.y += self.h - self.image.get_height()
            self.rect.x += cos(self.animStep * (self.animationStage)) * self.r * (1 if self.rightDirection else -1)
            self.rect.y -= sin(self.animStep * (self.animationStage)) * self.r
            self.animationStage -= 5
        else:
            self.image = self.imgR if rightDir else self.imgL

        self.rightDirection = rightDir

    def attack(self, platforms):
        if self.animationStage <= 0:
            self.animationStage = 90
        for p in platforms:
            if sprite.collide_rect(self.attackArea, p) and isinstance(p, monsters.Dwarf):
                p.hit(2)

class RainbowSword(sprite.Sprite):
    def __init__(self, x, y, orb):
        sprite.Sprite.__init__(self)
        # self.image = Surface((orb, config.HERO_HEIGHT))
        self.attackArea = blocks.Rectangle(x, y, orb, config.HERO_HEIGHT)
        self.img = transform.scale(image.load("images/weapon/ultimate-rainbow-sword.png").convert_alpha(),
                                   (30 * 1.88 * config.PLATFORM_WIDTH/64, 30 * config.PLATFORM_HEIGHT/ 64))
        self.imgR = transform.rotate(self.img, 45)
        self.imgL = transform.rotate(self.img, 135)
        self.animationStage = 0
        self.image = self.imgR
        self.orb = orb
        self.w, self.h = orb, config.HERO_HEIGHT
        self.rect = Rect(x, y, self.w, self.h)
        self.animStep = pi/180
        self.r = config.PLATFORM_WIDTH*0.2

    def update(self, rect, rightDir):
        x = rect.right if rightDir else rect.x - self.orb
        y = rect.y
        self.attackArea.update(x, y)
        self.rect.x = x + (-15 if rightDir else 20) * config.PLATFORM_WIDTH/64
        self.rect.y = y
        if self.animationStage > 0:
            if rightDir:
                self.rect.x -= 5
                self.image = transform.rotate(self.img, self.animationStage)
            else:
                self.image = transform.rotate(self.img, 180 - self.animationStage)
                self.rect.x += self.w - self.image.get_width()
            self.rect.y += self.h - self.image.get_height()
            self.rect.x += cos(self.animStep * (self.animationStage)) * self.r * (1 if self.rightDirection else -1)
            self.rect.y -= sin(self.animStep * (self.animationStage)) * self.r
            self.animationStage -= 5
        else:
            self.image = self.imgR if rightDir else self.imgL

        self.rightDirection = rightDir

    def attack(self, platforms):
        if self.animationStage <= 0:
            self.animationStage = 90
        for p in platforms:
            if sprite.collide_rect(self.attackArea, p):
                if isinstance(p, Bullet):
                    # p.die()
                    p.changeOwner('rainbowSword')
                    p.changeDirection()
                if isinstance(p, monsters.Dwarf):
                    p.hit(2)

class MushroomSword(sprite.Sprite):
    def __init__(self, x, y, orb, addObjective, removeObjective):
        sprite.Sprite.__init__(self)
        # self.image = Surface((orb, config.HERO_HEIGHT))
        self.removeObjective = removeObjective
        self.addObjective = addObjective
        self.attackArea = blocks.Rectangle(x, y, orb, config.HERO_HEIGHT)
        self.img = transform.scale(image.load("images/weapon/mushroom-sword.png").convert_alpha(),
                                   (30 * 1.88 * config.PLATFORM_WIDTH/64, 30 * config.PLATFORM_HEIGHT/ 64))
        self.imgR = transform.rotate(self.img, 45)
        self.imgL = transform.rotate(self.img, 135)
        self.animationStage = 0
        self.image = self.imgR
        self.orb = orb
        self.w, self.h = orb, config.HERO_HEIGHT
        self.rect = Rect(x, y, self.w, self.h)
        self.animStep = pi/180
        self.r = config.PLATFORM_WIDTH*0.2

    def shot(self):
        bullet = Bullet(self.rect.x, self.rect.y + config.HERO_HEIGHT / 2, 'player', self.rightDirection,
                        self.removeObjective, BULLET_MUSHROOM)
        self.addObjective(bullet)

    def update(self, rect, rightDir):
        x = rect.right if rightDir else rect.x - self.orb
        y = rect.y
        self.attackArea.update(x, y)
        self.rect.x = x + (-15 if rightDir else 20) * config.PLATFORM_WIDTH/64
        self.rect.y = y
        if self.animationStage > 0:
            if self.animationStage == 45 or self.animationStage == 5:
                self.shot()
            if rightDir:
                self.rect.x -= 5
                self.image = transform.rotate(self.img, self.animationStage)
            else:
                self.image = transform.rotate(self.img, 180 - self.animationStage)
                self.rect.x += self.w - self.image.get_width()
            self.rect.y += self.h - self.image.get_height()
            self.rect.x += cos(self.animStep * (self.animationStage)) * self.r * (1 if self.rightDirection else -1)
            self.rect.y -= sin(self.animStep * (self.animationStage)) * self.r
            self.animationStage -= 5
        else:
            self.image = self.imgR if rightDir else self.imgL

        self.rightDirection = rightDir

    def attack(self, platforms):
        if self.animationStage <= 0:
            self.animationStage = 90
        self.shot()
        for p in platforms:
            if sprite.collide_rect(self.attackArea, p) and isinstance(p, monsters.Dwarf):
                p.hit(2)

class Hook(sprite.Sprite):
    def __init__(self, x, y, addObjective, removeObjective):
        sprite.Sprite.__init__(self)
        self.removeObjective = removeObjective
        self.addObjective = addObjective
        # self.img = transform.scale(image.load("images/bullet/bullet_hook.png").convert_alpha(),
        #                            (30 * 1.285 * config.PLATFORM_WIDTH/64, 30 * config.PLATFORM_HEIGHT/ 64))
        self.img = transform.scale(image.load("images/weapon/hook.png").convert_alpha(),
                                   (30 * config.PLATFORM_WIDTH / 64, 30 * config.PLATFORM_HEIGHT / 64))
        self.imgR = self.img
        self.imgL = transform.flip(self.img, True, False)
        self.image = self.imgR
        self.rect = Rect(x, y, 30 * config.PLATFORM_WIDTH/64,30 * config.PLATFORM_HEIGHT/ 64)

    def update(self, rect, rightDir):
        x = rect.right if rightDir else rect.x
        y = rect.y
        self.rect.x = x + (-3 * config.PLATFORM_WIDTH/64 if rightDir else -self.img.get_width()+ 3* config.PLATFORM_WIDTH/64)
        self.rect.y = y + 15 * config.PLATFORM_HEIGHT/64
        self.image = self.imgR if rightDir else self.imgL
        self.rightDirection = rightDir

    def attack(self, platforms):
        bullet = Bullet(self.rect.x, self.rect.y + config.HERO_HEIGHT / 4, 'player', self.rightDirection,
                               self.removeObjective, BULLET_HERO)
        self.addObjective(bullet)
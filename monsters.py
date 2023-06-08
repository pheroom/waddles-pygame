from pygame import *
import util
import blocks
import pyganim
import random
from config import config


class Monster(sprite.Sprite):
    def __init__(self, x, y, left, maxLengthLeft, whenDead, removeSelf, addEntities, removeEntities, playAnimAmountWithRect):
        mixer.init()
        sprite.Sprite.__init__(self)
        self.image = Surface((config.MONSTER_WIDTH, config.MONSTER_HEIGHT))
        self.image.fill(Color(config.MONSTER_COLOR))
        self.image.set_colorkey(Color(config.MONSTER_COLOR))
        self.rect = Rect(x, y, config.MONSTER_WIDTH, config.MONSTER_HEIGHT)
        self.startX = x
        self.startY = y
        self.maxLengthLeft = maxLengthLeft
        self.xvel = left
        self.yvel = 0
        self.onGround = False
        self.dead = False
        self.indentImage = (0, 0)
        self.rightDirection = True

        self.health = config.MONSTER_HEALTH

        self.attackCooldown = 2000
        self.timeLastAttack = time.get_ticks()

        boltAnim = []
        for anim in config.ANIMATION_USUAL_DWARF_L:
            anim = self.transformImg(anim)
            boltAnim.append((anim, config.MONSTER_DELAY))
        self.boltAnim_left = pyganim.PygAnimation(boltAnim)
        self.boltAnim_left.play()
        boltAnim = []
        for anim in config.ANIMATION_USUAL_DWARF_R:
            anim = self.transformImg(anim)
            boltAnim.append((anim, config.MONSTER_DELAY))
        self.boltAnim_right = pyganim.PygAnimation(boltAnim)
        self.boltAnim_right.play()

        self.playAnimAmount = lambda amount, color: playAnimAmountWithRect(self.rect.x, self.rect.y, amount, color)
        self.addEntities = addEntities
        self.whenDead = whenDead
        self.removeSelf = removeSelf
        self.removeEntities = removeEntities

        self.s_damage = mixer.Sound('music/monster_damage.wav')
        self.s_damage.set_volume(0.5)

    def transformImg(self, img):
        if (isinstance(img, str)):
            return transform.scale(image.load(img), (config.MONSTER_WIDTH, config.MONSTER_HEIGHT))
        return transform.scale(img, (config.HERO_WIDTH, config.HERO_WIDTH))

    def die(self):
        self.image = transform.scale(self.image, (config.PLATFORM_WIDTH * 1.5, config.PLATFORM_HEIGHT / 2))
        self.rect.height -= config.PLATFORM_HEIGHT / 2
        self.xvel = 0
        self.whenDead(self)
        self.startDead = time.get_ticks()
        self.dead = True

    def hit(self, damage = 1):
        self.s_damage.play()
        self.playAnimAmount(damage, '#151515')
        self.health -= damage
        if self.health <= 0:
            self.die()

    def shot(self):
        self.timeLastAttack = time.get_ticks()
        bullet = blocks.Bullet(self.rect.x, self.rect.y + config.MONSTER_HEIGHT/2, 'monster',
                               self.rightDirection, self.removeEntities, util.BULLET_MONSTER)
        self.addEntities(bullet)

    def update(self, platforms):
        if self.dead:
            if self.startDead + 1000 < time.get_ticks():
                self.image = Surface((0, 0))
                self.removeSelf(self)
        else:
            if self.rightDirection:
                self.image.fill(Color(config.MONSTER_COLOR))
                self.boltAnim_right.blit(self.image, self.indentImage)
            else:
                self.image.fill(Color(config.MONSTER_COLOR))
                self.boltAnim_left.blit(self.image, self.indentImage)
            if random.randint(0,10) == 6 and time.get_ticks() - self.timeLastAttack >= self.attackCooldown:
                self.shot()
                # pass

        if not self.onGround:
            self.yvel += config.GRAVITY

        self.onGround = False
        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms)

        self.rect.x += self.xvel
        self.collide(self.xvel, 0, platforms)

        if (abs(self.startX - self.rect.x) > self.maxLengthLeft):
            self.xvel = -self.xvel
            # self.rightDirection = False if self.rightDirection else True
            self.rightDirection = not self.rightDirection

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p) and self != p and not isinstance(p, Mushroom) and (
                    not self.dead or not isinstance(p, Monster)):
                if isinstance(p, blocks.Bullet):
                    if p.owner != 'monster':
                        self.hit()
                        p.die()
                else:
                    if xvel > 0:
                        self.rect.right = p.rect.left
                        self.xvel = -self.xvel
                        self.rightDirection = False

                    if xvel < 0:
                        self.rect.left = p.rect.right
                        self.xvel = -self.xvel
                        self.rightDirection = True

                    if yvel > 0:
                        self.rect.bottom = p.rect.top
                        self.onGround = True
                        self.yvel = 0

                    if yvel < 0:
                        self.rect.top = p.rect.bottom
                        self.yvel = 0

class Mushroom(sprite.Sprite):
    def __init__(self, x, y, left, up, maxLengthLeft, maxLengthUp, whenDead, removeSelf):
        sprite.Sprite.__init__(self)
        self.id = random.random()
        self.whenDead = whenDead
        self.image = transform.scale(image.load("images/mushroom.png").convert_alpha(),
                                     (config.PLATFORM_WIDTH, config.PLATFORM_HEIGHT))
        self.rect = Rect(x, y, config.MONSTER_WIDTH, config.MONSTER_HEIGHT)
        self.startX = x
        self.startY = y
        self.maxLengthLeft = maxLengthLeft
        self.maxLengthUp = maxLengthUp
        self.xvel = left
        self.yvel = up
        self.onGround = False
        self.dead = False
        self.removeSelf = removeSelf

    def update(self, platforms):

        if not self.onGround:
            self.yvel += config.GRAVITY

        self.onGround = False
        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms)

        self.rect.x += self.xvel
        self.collide(self.xvel, 0, platforms)

        if (abs(self.startX - self.rect.x) > self.maxLengthLeft):
            self.xvel = -self.xvel

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p) and self != p and not isinstance(p, Monster):
                if xvel > 0:
                    self.rect.right = p.rect.left
                    self.xvel = -self.xvel

                if xvel < 0:
                    self.rect.left = p.rect.right
                    self.xvel = -self.xvel

                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.yvel = 0

                if yvel < 0:
                    self.rect.top = p.rect.bottom
                    self.yvel = 0

    def die(self):
        self.removeSelf(self)
        self.whenDead(self)

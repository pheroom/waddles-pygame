import math
from pygame import *
import util
import weapon
import blocks
import pyganim
import random
from config import config

mixer.init()
s_damage = mixer.Sound('music/monster_damage.wav')
s_damage.set_volume(0.5 + config.VOLUME_LEVEL)
s_shot = mixer.Sound('music/bullet.wav')
s_shot.set_volume(0.2 + config.VOLUME_LEVEL)

class Dwarf(sprite.Sprite):
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
        self.xvel = max(round(left * config.PLATFORM_WIDTH / 64), 1)
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

    def transformImg(self, img):
        if (isinstance(img, str)):
            return transform.scale(image.load(img), (config.MONSTER_WIDTH, config.MONSTER_HEIGHT))
        return transform.scale(img, (config.MONSTER_WIDTH, config.MONSTER_HEIGHT))

    def die(self):
        if self.dead:
            return
        self.image = transform.scale(self.image, (config.PLATFORM_WIDTH * 1.5, config.PLATFORM_HEIGHT / 2))
        self.rect.height -= config.PLATFORM_HEIGHT / 2
        self.xvel = 0
        self.whenDead(self)
        self.startDead = time.get_ticks()
        self.dead = True

    def hit(self, damage = 1):
        s_damage.play()
        self.playAnimAmount(damage, '#151515')
        self.health -= damage
        if self.health <= 0:
            self.die()

    def shot(self):
        self.timeLastAttack = time.get_ticks()
        bullet = weapon.Bullet(self.rect.x, self.rect.y + config.MONSTER_HEIGHT/2, 'monster',
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
            # if random.randint(0,10) == 6 and time.get_ticks() - self.timeLastAttack >= self.attackCooldown:
            #     self.shot()

        if not self.onGround:
            self.yvel += config.GRAVITY

        self.onGround = False
        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms)

        self.rect.x += self.xvel
        self.collide(self.xvel, 0, platforms)

        if (abs(self.startX - self.rect.x) > self.maxLengthLeft):
            self.xvel = -self.xvel
            self.rightDirection = not self.rightDirection

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p) and self != p and not isinstance(p, Mushroom) and (
                    not self.dead or (not isinstance(p, Dwarf) and not isinstance(p, DwarfLegless) and not isinstance(p, Gideon))):
                if isinstance(p, weapon.Bullet):
                    if p.owner != 'monster' and not self.dead:
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

class DwarfLegless(sprite.Sprite):
    def __init__(self, x, y, rightDirection, whenDead, removeSelf, addEntities, removeEntities, playAnimAmountWithRect):
        sprite.Sprite.__init__(self)
        self.image = Surface((config.MONSTER_WIDTH, config.MONSTER_HEIGHT))
        self.image.fill(Color(config.MONSTER_COLOR))
        self.image.set_colorkey(Color(config.MONSTER_COLOR))
        self.rect = Rect(x, y, config.MONSTER_WIDTH, config.MONSTER_HEIGHT)
        self.rightDirection = rightDirection
        self.dead = False
        self.indentImage = (0, 0)

        self.health = config.MONSTER_HEALTH

        self.attackCooldown = 2000
        self.timeLastAttack = time.get_ticks()

        anims = config.ANIMATION_PUKING_DWARF_r if rightDirection else config.ANIMATION_PUKING_DWARF_l
        self.boltAnim_attack = []
        for i in range(0, len(anims)):
            self.boltAnim_attack.append(pyganim.PygAnimation(self.transformAnim(anims[i])))
            self.boltAnim_attack[-1].play()

        self.boltAnim_stay = pyganim.PygAnimation([[self.transformImg(config.ANIMATION_PUKING_DWARF_STAY[0]), 100]])
        self.boltAnim_stay.play()

        self.lastAnimIndex = 0

        self.playAnimAmount = lambda amount, color: playAnimAmountWithRect(self.rect.x, self.rect.y, amount, color)
        self.addEntities = addEntities
        self.whenDead = whenDead
        self.removeSelf = removeSelf
        self.removeEntities = removeEntities

    def transformAnim(self, anim):
        return [(self.transformImg(anim), 100)]

    def transformImg(self, img):
        if (isinstance(img, str)):
            return transform.scale(image.load(img), (config.MONSTER_WIDTH, config.MONSTER_HEIGHT))
        return transform.scale(img, (config.MONSTER_WIDTH, config.MONSTER_HEIGHT))

    def die(self):
        if self.dead:
            return
        self.image.fill(Color(config.MONSTER_COLOR))
        self.boltAnim_stay.blit(self.image, self.indentImage)
        self.image = transform.scale(self.image, (config.PLATFORM_WIDTH * 1.5, config.PLATFORM_HEIGHT / 2))
        self.rect.y += config.PLATFORM_HEIGHT / 2
        self.rect.x -= config.PLATFORM_HEIGHT / 4
        self.xvel = 0
        self.whenDead(self)
        self.startDead = time.get_ticks()
        self.dead = True

    def hit(self, damage = 1):
        s_damage.play()
        self.playAnimAmount(damage, '#151515')
        self.health -= damage
        if self.health <= 0:
            self.die()

    def shot(self):
        self.timeLastAttack = time.get_ticks()
        bullet = weapon.Bullet(self.rect.x, self.rect.y + config.MONSTER_HEIGHT/2, 'monster',
                               self.rightDirection, self.removeEntities, util.BULLET_MONSTER)
        self.addEntities(bullet)

    def update(self, platforms):
        if self.dead:
            if self.startDead + 1000 < time.get_ticks():
                self.image = Surface((0, 0))
                self.removeSelf(self)
        else:
            self.image.fill(Color(config.MONSTER_COLOR))
            if random.randint(0,10) == 6 and time.get_ticks() - self.timeLastAttack >= self.attackCooldown:
                self.lastAnimIndex = random.randint(0,1)
                self.boltAnim_attack[self.lastAnimIndex].blit(self.image, self.indentImage)
                self.shot()
            else:
                if time.get_ticks() - self.timeLastAttack < 500:
                    self.boltAnim_attack[self.lastAnimIndex].blit(self.image, self.indentImage)
                else:
                    self.boltAnim_stay.blit(self.image, self.indentImage)

        for p in platforms:
            if sprite.collide_rect(self, p) and self != p:
                if isinstance(p, weapon.Bullet):
                    if p.owner != 'monster' and not self.dead:
                        self.hit()
                        p.die()

class Gideon(sprite.Sprite):
    def __init__(self, x, y, left, up, maxLengthLeft, maxLengthUp, whenDead, removeSelf, addEntities, removeEntities, playAnimAmountWithRect):
        mixer.init()
        sprite.Sprite.__init__(self)
        self.image = Surface((config.MONSTER_WIDTH, config.MONSTER_HEIGHT))
        self.image.fill(Color(config.MONSTER_COLOR))
        self.image.set_colorkey(Color(config.MONSTER_COLOR))
        self.rect = Rect(x, y, config.MONSTER_WIDTH, config.MONSTER_HEIGHT)
        self.startX = x
        self.startY = y
        self.maxLengthLeft = maxLengthLeft
        self.maxLengthUp = maxLengthUp
        self.xvel = max(round(left * config.PLATFORM_WIDTH / 64), 1)
        self.yvel = max(round(up * config.PLATFORM_WIDTH / 64), 1)
        print(maxLengthLeft, maxLengthUp, self.xvel, self.yvel)
        self.dead = False
        self.indentImage = (0, 0)
        self.rightDirection = True

        self.health = config.MONSTER_HEALTH

        self.attackCooldown = 2000
        self.timeLastAttack = time.get_ticks()

        boltAnim = []
        for anim in config.ANIMATION_GIDEON_L:
            anim = self.transformImg(anim)
            boltAnim.append((anim, config.GIDEON_DELAY))
        self.boltAnim_left = pyganim.PygAnimation(boltAnim)
        self.boltAnim_left.play()
        boltAnim = []
        for anim in config.ANIMATION_GIDEON_R:
            anim = self.transformImg(anim)
            boltAnim.append((anim, config.GIDEON_DELAY))
        self.boltAnim_right = pyganim.PygAnimation(boltAnim)
        self.boltAnim_right.play()

        self.playAnimAmount = lambda amount, color: playAnimAmountWithRect(self.rect.x, self.rect.y, amount, color)
        self.addEntities = addEntities
        self.whenDead = whenDead
        self.removeSelf = removeSelf
        self.removeEntities = removeEntities

    def transformImg(self, img):
        if (isinstance(img, str)):
            return transform.scale(image.load(img), (config.MONSTER_WIDTH, config.MONSTER_HEIGHT))
        return transform.scale(img, (config.MONSTER_WIDTH, config.MONSTER_HEIGHT))

    def die(self):
        if self.dead:
            return
        self.image = transform.scale(self.image, (config.PLATFORM_WIDTH * 1.5, config.PLATFORM_HEIGHT / 2))
        self.rect.height -= config.PLATFORM_HEIGHT / 2
        self.xvel = 0
        self.whenDead(self)
        self.startDead = time.get_ticks()
        self.dead = True

    def hit(self, damage = 1):
        s_damage.play()
        self.playAnimAmount(damage, '#151515')
        self.health -= damage
        if self.health <= 0:
            self.die()

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
            # if random.randint(0,10) == 6 and time.get_ticks() - self.timeLastAttack >= self.attackCooldown:
            #     self.shot()

        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms)

        self.rect.x += self.xvel
        self.collide(self.xvel, 0, platforms)

        if (abs(self.startX - self.rect.x) > self.maxLengthLeft):
            self.xvel = -self.xvel
            self.rightDirection = not self.rightDirection

        if (abs(self.startY - self.rect.y) > self.maxLengthUp):
            self.yvel = -self.yvel

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p) and self != p and not isinstance(p, Mushroom) and (
                    not self.dead or (not isinstance(p, Dwarf) and not isinstance(p, DwarfLegless) and not isinstance(p, Gideon))):
                if isinstance(p, weapon.Bullet):
                    if p.owner != 'monster'  and not self.dead:
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
                        self.yvel = - self.yvel


                    if yvel < 0:
                        self.rect.top = p.rect.bottom
                        self.yvel = - self.yvel


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
            if sprite.collide_rect(self, p) and self != p and not isinstance(p, Dwarf):
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

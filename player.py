from pygame import *
from config import config
import util
import pyganim
import blocks
import monsters
import weapon

class Player(sprite.Sprite):
    def __init__(self, x, y, playAnimAmountWithRect, maxX, maxY, afterDead, addEntities, removeEntities, addObjective, removeObjective):
        mixer.init()
        sprite.Sprite.__init__(self)
        self.startX = x
        self.startY = y
        self.maxX = maxX
        self.maxY = maxY
        self.xvel = 0
        self.yvel = 0
        self.onGround = False
        self.rect = Rect(x, y, config.HERO_PHYSICAL_WIDTH, config.HERO_PHYSICAL_HEIGHT)

        self.addEntities = addEntities
        self.removeEntities = removeEntities
        self.addObjective = addObjective
        self.removeObjective = removeObjective

        self.weaponIsKnife = True
        self.rightDirection = True

        self.attackOrb = config.PLATFORM_WIDTH
        sword = weapon.Sword(x, y, self.attackOrb)
        swordRainbow = weapon.RainbowSword(x, y, self.attackOrb)
        swordMushroom = weapon.MushroomSword(x, y, self.attackOrb, self.addObjective, self.removeObjective)
        hook = weapon.Hook(x, y, self.addObjective, self.removeObjective)
        self.weapons = [hook, swordMushroom, swordRainbow, sword]
        self.curWeaponIndex = 0
        addEntities(self.weapons[self.curWeaponIndex])
        self.attackCooldown = 500
        self.timeLastAttack = time.get_ticks()

        self.immunityStart = 0
        self.immunityValue = 1000
        self.afterDead = afterDead
        self.startDead = -1
        self.dead = False
        self.lives = 3
        self.health = config.HERO_HEALTH

        self.playAnimAmount = lambda amount,color: playAnimAmountWithRect(self.rect.x, self.rect.y, amount, color)
        self.points = 0
        self.coins = 0

        self.image = Surface((config.HERO_WIDTH, config.HERO_HEIGHT))
        self.image.fill(Color(config.COLOR))
        # self.indentImage = ((config.HERO_WIDTH - config.HERO_PHYSICAL_WIDTH)/2, (config.HERO_HEIGHT - config.HERO_PHYSICAL_HEIGHT)/2)
        self.indentImage = (0,0)
        self.image.set_colorkey(Color(config.COLOR))

        boltAnim = []
        boltAnimSuperSpeed = []
        for anim in config.ANIMATION_RIGHT:
            anim = self.transformImg(anim)
            boltAnim.append((anim, config.ANIMATION_DELAY))
            boltAnimSuperSpeed.append((anim, config.ANIMATION_SUPER_SPEED_DELAY))
        self.boltAnimRight = pyganim.PygAnimation(boltAnim)
        self.boltAnimRight.play()
        self.boltAnimRightSuperSpeed = pyganim.PygAnimation(boltAnimSuperSpeed)
        self.boltAnimRightSuperSpeed.play()
        boltAnim = []
        boltAnimSuperSpeed = []
        for anim in config.ANIMATION_LEFT:
            anim = self.transformImg(anim)
            boltAnim.append((anim, config.ANIMATION_DELAY))
            boltAnimSuperSpeed.append((anim, config.ANIMATION_SUPER_SPEED_DELAY))
        self.boltAnimLeft = pyganim.PygAnimation(boltAnim)
        self.boltAnimLeft.play()
        self.boltAnimLeftSuperSpeed = pyganim.PygAnimation(boltAnimSuperSpeed)
        self.boltAnimLeftSuperSpeed.play()
        boltAnim = []
        for anim in config.ANIMATION_STAY:
            anim = self.transformImg(anim)
            boltAnim.append((anim, config.ANIMATION_STAY_DELAY))
        self.boltAnimStay = pyganim.PygAnimation(boltAnim)
        self.boltAnimStay.play()
        self.boltAnimJumpLeft = pyganim.PygAnimation(self.transformAnim(config.ANIMATION_JUMP_LEFT))
        self.boltAnimJumpLeft.play()
        self.boltAnimJumpRight = pyganim.PygAnimation(self.transformAnim(config.ANIMATION_JUMP_RIGHT))
        self.boltAnimJumpRight.play()
        self.boltAnimJump = pyganim.PygAnimation(self.transformAnim(config.ANIMATION_JUMP))
        self.boltAnimJump.play()
        self.boltAnimHitRight = pyganim.PygAnimation(self.transformAnim(config.ANIMATION_HIT_RIGHT))
        self.boltAnimHitRight.play()
        self.boltAnimHitLeft = pyganim.PygAnimation(self.transformAnim(config.ANIMATION_HIT_LEFT))
        self.boltAnimHitLeft.play()

        self.s_jump = mixer.Sound('music/8bit_jump.wav')
        self.s_jump.set_volume(0.2 + config.VOLUME_LEVEL)
        self.s_hit = mixer.Sound('music/sword_whoosh.wav')
        self.s_hit.set_volume(0.2 + config.VOLUME_LEVEL)
        self.s_walk = mixer.Sound('music/walk.wav')
        self.s_walk.set_volume(0.4 + config.VOLUME_LEVEL)
        self.s_damage = mixer.Sound('music/hero_damage.wav')
        self.s_damage.set_volume(0.3 + config.VOLUME_LEVEL)
        self.s_die = mixer.Sound('music/die.wav')
        self.s_die.set_volume(0.2 + config.VOLUME_LEVEL)
        self.s_heal = mixer.Sound('music/heal.wav')
        self.s_heal.set_volume(0.3 + config.VOLUME_LEVEL)

        self.winner = False

    def transformAnim(self, anim):
        return [(self.transformImg(anim[0][0]), anim[0][1])]

    def transformImg(self, img):
        if(isinstance(img, str)):
            return transform.scale(image.load(img), (config.HERO_WIDTH, config.HERO_HEIGHT))
        return transform.scale(img, (config.HERO_WIDTH, config.HERO_HEIGHT))

    def die(self):
        self.s_die.play()
        if self.startDead + 500 > time.get_ticks():
            return
        self.dead = True
        self.lives -= 1
        self.startDead = time.get_ticks()
        self.image = transform.scale(image.load("images/waddles/waddles_dead.png").convert_alpha(), (config.PLATFORM_WIDTH, config.PLATFORM_HEIGHT) )
        self.yvel = -config.JUMP_POWER
        self.health = 0

    def getWeaponImg(self):
        return self.weapons[self.curWeaponIndex].getImg()

    def hit(self, damage = 1):
        if self.immunityStart + self.immunityValue < time.get_ticks():
            self.s_damage.play()
            self.playAnimAmount(damage, '#FF0000')
            self.health -= damage
            if self.health <= 0:
                self.die()

    def teleport(self, goX, goY):
        self.rect.x = goX
        self.rect.y = goY

    def addHealth(self, amount=1):
        self.playAnimAmount(amount, '#008000')
        self.s_heal.play()
        if(self.health < 20):
            self.health += min(amount, 20 - self.health)

    def addPoint(self, amount = 200):
        self.playAnimAmount(amount, '#ffffff')
        self.points += amount

    def addLive(self, amount = 1):
        self.playAnimAmount(amount, '#ffc0cb')
        self.lives += amount

    def addCoin(self):
        self.coins += 1

    def setImmunity(self, value = 1000):
        self.immunityStart = time.get_ticks()
        self.immunityValue = value

    def switchWeapon(self):
        self.removeEntities(self.weapons[self.curWeaponIndex])

        #whatafuck:
        # if self.weapons[self.curWeaponIndex] == self.weapons[0] or self.weapons[1]:
        #     self.s_hit = mixer.Sound('music/hook_whoosh.wav')
        #     self.s_hit.set_volume(0.2 + config.VOLUME_LEVEL)
        # else:
        #     self.s_hit = mixer.Sound('music/sword_whoosh.wav')
        #     self.s_hit.set_volume(0.2 + config.VOLUME_LEVEL)

        if self.curWeaponIndex + 1 < len(self.weapons):
            self.curWeaponIndex += 1
        else:
            self.curWeaponIndex = 0
        self.addEntities(self.weapons[self.curWeaponIndex])

    def addWeapon(self, newWeapon, needSwitching = True):
        self.weapons.append(newWeapon)
        if(needSwitching):
            self.curWeaponIndex = len(self.weapons)

    def update(self, left, right, up, space, running, slowly, platforms):
        if self.dead:
            if self.startDead + 1000 > time.get_ticks():
                self.rect.y += self.yvel
                self.yvel += config.GRAVITY
            else:
                self.health = config.HERO_HEALTH
                self.dead = False
                self.immunityStart = time.get_ticks()
                self.immunityValue = config.DEAD_SCREEN_TIME + 1500
                self.teleport(self.startX, self.startY)
                self.image = Surface((config.HERO_WIDTH, config.HERO_HEIGHT))
                self.image.fill(Color(config.COLOR))
                self.image.set_colorkey(Color(config.COLOR))
                self.afterDead()
            return

        if up:
            if self.onGround:
                self.s_jump.play()
                self.yvel = -config.JUMP_POWER
                if slowly:
                    self.yvel += config.JUMP_SLOW_POWER
                elif running and (left or right):
                    self.yvel -= config.JUMP_EXTRA_POWER
                self.image.fill(Color(config.COLOR))
                self.boltAnimJump.blit(self.image, self.indentImage)

        if left:
            self.rightDirection = False
            self.xvel = -config.MOVE_SPEED
            self.image.fill(Color(config.COLOR))
            if running:
                self.xvel -= config.MOVE_EXTRA_SPEED
                if not up:
                    self.boltAnimLeftSuperSpeed.blit(self.image, self.indentImage)
            else:
                if not up:
                    self.boltAnimLeft.blit(self.image, self.indentImage)
            if up:
                self.boltAnimJumpLeft.blit(self.image, self.indentImage)

        if right:
            self.rightDirection = True
            self.xvel = config.MOVE_SPEED
            self.image.fill(Color(config.COLOR))
            if running:
                self.xvel += config.MOVE_EXTRA_SPEED
                if not up:
                    self.boltAnimRightSuperSpeed.blit(self.image, self.indentImage)
            else:
                if not up:
                    self.boltAnimRight.blit(self.image, self.indentImage)
            if up:
                self.boltAnimJumpRight.blit(self.image, self.indentImage)

        if not (left or right):
            self.xvel = 0
            if not (up or space):
                self.image.fill(Color(config.COLOR))
                self.boltAnimStay.blit(self.image, self.indentImage)

        if not self.onGround:
            self.yvel += config.GRAVITY

        if slowly and (left or right):
            self.xvel = config.MOVE_SLOW_SPEED * (-1 if left else 1)

        self.onGround = False
        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms)

        self.rect.x += self.xvel
        self.collide(self.xvel, 0, platforms)

        if space and time.get_ticks() - self.timeLastAttack >= self.attackCooldown:
            self.s_hit.play()
            self.timeLastAttack = time.get_ticks()
            self.weapons[self.curWeaponIndex].attack(platforms)

        self.weapons[self.curWeaponIndex].update(self.rect, self.rightDirection)

        if self.rect.x + config.PLATFORM_WIDTH < 0 or self.rect.x - config.PLATFORM_WIDTH > self.maxX or self.rect.y - config.PLATFORM_HEIGHT*5 > self.maxY:
            self.die()

    def collide(self, xvel, yvel, platforms,):
        for p in platforms:
            if sprite.collide_rect(self, p):
                # if isinstance(p,monsters.Monster) and not p.dead:
                #     if self.immunityStart + self.immunityValue < time.get_ticks():
                #         if p.rect.y - config.HERO_HEIGHT / 2 < self.rect.y:
                #             p.die()
                #         else:
                #             self.die()
                if isinstance(p, monsters.Dwarf) and not p.dead:
                    self.hit(3)
                    self.setImmunity()
                elif isinstance(p, monsters.DwarfLegless) and not p.dead:
                    self.hit(1)
                    self.setImmunity()
                elif isinstance(p, monsters.Gideon) and not p.dead:
                    self.hit(2)
                    self.setImmunity()
                elif isinstance(p, weapon.Bullet):
                    if p.owner != 'player':
                        self.hit()
                        p.die()
                elif isinstance(p, blocks.BlockTeleport):
                    self.teleport(p.goX, p.goY)
                elif isinstance(p, blocks.Princess):
                    if not self.winner:
                        self.addPoint(10000)
                        self.winner = True
                elif isinstance(p, blocks.Flower):
                    self.addHealth(1)
                    p.die()
                elif isinstance(p, monsters.Mushroom):
                    self.addHealth(3)
                    # self.addPoint(800)
                    p.die()
                elif isinstance(p, blocks.PlatformCoin):
                    self.addCoin()
                    self.addPoint()
                    p.die()
                elif isinstance(p, weapon.Sword):
                    p.die()
                else:
                    if xvel > 0:
                        self.rect.right = p.rect.left

                    if xvel < 0:
                        self.rect.left = p.rect.right

                    if yvel > 0:
                        self.rect.bottom = p.rect.top
                        self.onGround = True
                        self.yvel = 0

                    if yvel < 0:
                        self.rect.top = p.rect.bottom
                        self.yvel = 0

                if isinstance(p, blocks.ActPlatform) and p.rect.y + config.HERO_HEIGHT == self.rect.y:
                    p.act()


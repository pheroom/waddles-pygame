from pygame import *
import time as pytime
from config import config, refreshConfig
from player import Player
from blocks import Platform, Princess, ActPlatform, Heart, Amount
from monsters import Dwarf, Mushroom, DwarfLegless, Gideon
import weapon
import pytmx

class Camera(object):
    def __init__(self, camera_func, width, height, floorY):
        self.camera_func = camera_func
        self.floorY = floorY
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect, self.floorY)


def camera_configure(camera, target_rect, y):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l + config.WIN_WIDTH / 2, -t + config.WIN_HEIGHT / 2
    l = min(0, l)
    l = max(-(camera.width - config.WIN_WIDTH), l)
    # t = max(-(camera.height - config.WIN_HEIGHT), t, -y+config.WIN_HEIGHT-config.PLATFORM_HEIGHT)
    t = max(-(camera.height - config.WIN_HEIGHT), t)
    t = min(0, t)

    return Rect(l, t, w, h)

def hexToColour( hash_colour ):
    red   = int( hash_colour[1:3], 16 )
    green = int( hash_colour[3:5], 16 )
    blue  = int( hash_colour[5:7], 16 )
    return ( red, green, blue )

LayerNamePlatforms = 'Platforms'
LayerNameActPlatforms = 'ActPlatforms'
LayerNameBackground = 'Background'
LayerNameBackgroundObject = 'BlocksBG'
LayerNamePlayer = 'Player'
LayerNameDwarf = 'Monsters'
LayerNameDwarfLegless = 'MonstersLegless'
LayerNameGideon = 'MonsterGideon'
LayerNamePrincess = 'Princess'
LayerNameEntity = 'Entity'

class Level:
    def __init__(self, surf, switchScreen, backToLastScreen, lvl, levelName):
        mixer.init()
        self.switchScreen = switchScreen
        self.surface = surf
        self.backToLastScreen = backToLastScreen
        self.levelName = levelName

        self.bg = Surface((config.WIN_WIDTH, config.WIN_HEIGHT))
        self.bg.fill(Color(config.BG_COLOR_SKY))

        self.space = self.left = self.right = self.up = False
        self.running = False
        self.slowly = False

        self.entities = sprite.Group()
        self.platforms = []
        self.animatedEntities = sprite.Group()
        self.monsters = sprite.Group()
        self.bullets = sprite.Group()
        self.backgrounds = sprite.Group()
        self.blocksBG = sprite.Group()
        self.actPlatforms = []

        self.startTime = time.get_ticks()

        self.levelName = levelName

        self.firstRenderMap(pytmx.load_pygame(lvl))
        self.ui = UI(self.surface, self.levelName)

        self.deadScreen = False
        self.startDead = 0

        self.winScreen = False
        self.startWin = 0
        self.canSkipWinScreen = False

        mixer.music.load('music/true_8_bit.mp3')
        mixer.music.set_volume(0.3 + config.VOLUME_LEVEL)
        mixer.music.play(loops=-1, start=0.0)

        self.s_winner = mixer.Sound('music/Winner_song.mp3')
        self.s_winner.set_volume(0.3 + config.VOLUME_LEVEL)
        self.bool_winner = True


    def createMushroom(self, x, y):
        mr = Mushroom(x, y - config.PLATFORM_HEIGHT, 3, 0,
                      150, 0, self.removePlatform, self.removeMonster)
        self.entities.add(mr)
        self.platforms.append(mr)
        self.monsters.add(mr)

    def createFlower(self, x, y):
        mr = Heart(x, y, self.removePlatform, self.removeMonster)
        self.entities.add(mr)
        self.animatedEntities.add(mr)
        self.platforms.append(mr)

    def addRainbowSword(self, x, y):
        swordRainbow = weapon.RainbowSword(x, y, self.hero.attackOrb)
        self.hero.addWeapon(swordRainbow)

    def addMushroomSword(self, x, y):
        swordMushroom = weapon.MushroomSword(x, y, self.hero.attackOrb, self.addObjective, self.removeObjective)
        self.hero.addWeapon(swordMushroom)

    def removeActPlatform(self, x, y):
        for pl in self.actPlatforms:
            if pl.rect.x == x and pl.rect.y == y:
                self.entities.remove(pl)
                self.platforms.remove(pl)
                self.actPlatforms.remove(pl)

    def removePlatform(self, obj):
        try:
            self.platforms.remove(obj)
        except:
            print(f'{obj} not in levels.platforms!')

    def removeMonster(self, obj):
        self.entities.remove(obj)
        self.monsters.remove(obj)

    def removePlatformAndEntity(self, obj):
        self.platforms.remove(obj)
        self.entities.remove(obj)

    def removeAnimatedEntity(self, obj):
        self.entities.remove(obj)
        self.animatedEntities.remove(obj)

    def addAnimatedEntity(self, obj):
        self.entities.add(obj)
        self.animatedEntities.add(obj)

    def removeObjective(self, obj):
        self.entities.remove(obj)
        # self.animatedEntities.remove(obj)
        self.bullets.remove(obj)
        self.removePlatform(obj)

    def addObjective(self, obj):
        self.entities.add(obj)
        # self.animatedEntities.add(obj)
        self.bullets.add(obj)
        self.platforms.append(obj)

    def playAnimAmount(self, x, y, amount, color):
        amount = Amount(x, y, amount, self.removeAnimatedEntity, color)
        self.entities.add(amount)
        self.animatedEntities.add(amount)

    def playDeadScreen(self):
        self.deadScreen = True
        self.startDead = time.get_ticks()

    def firstRenderMap(self, tmxMap):
        self.totalLevelWidth = config.PLATFORM_WIDTH * tmxMap.width
        self.totalLevelHeight = config.PLATFORM_HEIGHT * tmxMap.height
        # print(self.totalLevelWidth, tmxMap.width)
        self.floor = 0

        def getX(obj):
            return obj.x * config.PLATFORM_WIDTH/tmxMap.tilewidth
        def getY(obj):
            return obj.y * config.PLATFORM_HEIGHT/tmxMap.tileheight

        for layer in tmxMap.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile_bitmap = tmxMap.get_tile_image_by_gid(gid)
                    if tile_bitmap and layer.name.rstrip() == LayerNamePlatforms:
                        # pf = Platform(x * tmxMap.tilewidth, y * tmxMap.tileheight, img=tile_bitmap)
                        pf = Platform(x * config.PLATFORM_WIDTH, y * config.PLATFORM_HEIGHT, img=tile_bitmap)
                        self.floor = max(self.floor, y * config.PLATFORM_HEIGHT)
                        self.entities.add(pf)
                        self.platforms.append(pf)
                    if tile_bitmap and (layer.name.rstrip() == LayerNameBackground or layer.name.rstrip() == LayerNameBackgroundObject):
                        pf = Platform(x * config.PLATFORM_WIDTH, y * config.PLATFORM_HEIGHT, img=tile_bitmap)
                        self.entities.add(pf)
            elif isinstance(layer, pytmx.TiledObjectGroup):
                if layer.name.rstrip() == LayerNamePlayer:
                    self.hero = Player(getX(layer[0]), getY(layer[0]), self.playAnimAmount, self.totalLevelWidth, self.totalLevelHeight,
                                       self.playDeadScreen, self.entities.add, self.entities.remove, self.addObjective, self.removeObjective)
                    self.entities.add(self.hero)
                if layer.name.rstrip() == LayerNamePrincess:
                    pr = Princess(getX(layer[0]), getY(layer[0]))
                    self.platforms.append(pr)
                    self.entities.add(pr)
                    self.animatedEntities.add(pr)
                elif layer.name.rstrip() == LayerNameEntity:
                    for entity in layer:
                        if entity.name == 'flower':
                            self.createFlower(getX(entity), getY(entity) + config.PLATFORM_HEIGHT)
                elif layer.name.rstrip() == LayerNameActPlatforms:
                    for actPlatform in layer:
                        actObj = actPlatform.properties
                        if actObj.get('mushroom'):
                            pf = ActPlatform(getX(actPlatform), getY(actPlatform), 1, self.createMushroom,
                                             img=actPlatform.image)
                            self.entities.add(pf)
                            self.platforms.append(pf)
                            self.actPlatforms.append(pf)
                        elif actObj.get('break'):
                            pf = ActPlatform(getX(actPlatform), getY(actPlatform), actObj.get('break'), self.removeActPlatform,
                                             img=actPlatform.image)
                            self.entities.add(pf)
                            self.platforms.append(pf)
                            self.actPlatforms.append(pf)
                        elif actObj.get('flower'):
                            pf = ActPlatform(getX(actPlatform), getY(actPlatform), 1, self.createFlower,
                                             img=actPlatform.image)
                            self.entities.add(pf)
                            self.platforms.append(pf)
                            self.actPlatforms.append(pf)
                        elif actObj.get('weapon'):
                            pf = ActPlatform(getX(actPlatform), getY(actPlatform), 1,
                                             self.addRainbowSword if actObj.get('weapon') == 'rainbowSword' else self.addMushroomSword,
                                             img=actPlatform.image)
                            self.entities.add(pf)
                            self.platforms.append(pf)
                            self.actPlatforms.append(pf)
                elif layer.name.rstrip() == LayerNameDwarf:
                    for monster in layer:
                        mn = Dwarf(getX(monster), getY(monster), monster.left,
                                   monster.maxLeft * config.PLATFORM_WIDTH / tmxMap.tilewidth,
                                   self.removePlatform, self.removeMonster, self.addObjective, self.removeObjective,
                                   self.playAnimAmount)
                        self.entities.add(mn)
                        self.platforms.append(mn)
                        self.monsters.add(mn)
                elif layer.name.rstrip() == LayerNameDwarfLegless:
                    for monster in layer:
                        mn = DwarfLegless(getX(monster), getY(monster), monster.rightDirection,
                                   self.removePlatform, self.removeMonster, self.addObjective, self.removeObjective,
                                   self.playAnimAmount)
                        self.entities.add(mn)
                        self.platforms.append(mn)
                        self.monsters.add(mn)
                elif layer.name.rstrip() == LayerNameGideon:
                    for monster in layer:
                        mn = Gideon(getX(monster), getY(monster), monster.left, monster.up,
                                    monster.maxLeft * config.PLATFORM_WIDTH / tmxMap.tilewidth,
                                    monster.maxUp * config.PLATFORM_WIDTH / tmxMap.tilewidth,
                                   self.removePlatform, self.removeMonster, self.addObjective, self.removeObjective,
                                   self.playAnimAmount)
                        self.entities.add(mn)
                        self.platforms.append(mn)
                        self.monsters.add(mn)
        self.camera = Camera(camera_configure, self.totalLevelWidth, self.totalLevelHeight, self.floor)

    def run(self, events):
        if self.deadScreen:
            if self.canSkipWinScreen:
                self.s_winner.stop()
                self.backToLastScreen()
                return

            if self.startDead + config.DEAD_SCREEN_TIME > time.get_ticks():
                bg = Surface((config.WIN_WIDTH, config.WIN_HEIGHT))
                bg.fill(Color(config.BG_COLOR_DUNGEON))
                self.surface.blit(bg, (0, 0))
                deadImg = transform.scale(image.load('./images/waddles/waddles_dead.png').convert_alpha(), (64, 64))
                deadLabel = font.Font('./emulogic.ttf', 45).render('*' + str(self.hero.lives), False, '#ffffff')
                self.surface.blit(deadImg, (config.WIN_WIDTH // 2 - 100, config.WIN_HEIGHT // 2 - 15))
                self.surface.blit(deadLabel, (config.WIN_WIDTH // 2 - 32, config.WIN_HEIGHT // 2 - 15))
                time_diff = time.get_ticks() - self.startTime

                self.ui.draw(self.hero.points, self.hero.health, (time_diff - time_diff % 1000) // 1000, self.hero.getWeaponSet())

            else:
                if self.hero.lives == 0:
                    self.s_winner.stop()
                    self.backToLastScreen()
                self.deadScreen = False
            return

        needSwitchWeapon = False
        for e in events:
            if e.type == KEYDOWN and e.key == K_ESCAPE:
                self.s_winner.stop()
                self.backToLastScreen()
            if e.type == KEYDOWN and e.key == K_UP:
                self.up = True
            if e.type == KEYDOWN and e.key == K_LEFT:
                self.left = True
            if e.type == KEYDOWN and e.key == K_RIGHT:
                self.right = True
            if e.type == KEYDOWN and e.key == K_LSHIFT:
                self.running = True
            if e.type == KEYDOWN and e.key == K_LCTRL:
                self.slowly = True
            if e.type == KEYDOWN and e.key == K_SPACE:
                self.space = True

            if self.canSkipWinScreen and e.type == KEYDOWN and e.key == K_b:
                self.s_winner.stop()
                self.backToLastScreen()

            if e.type == KEYDOWN and e.key == K_c:
                needSwitchWeapon = True

            if e.type == KEYUP and e.key == K_UP:
                self.up = False
            if e.type == KEYUP and e.key == K_RIGHT:
                self.right = False
            if e.type == KEYUP and e.key == K_LEFT:
                self.left = False
            if e.type == KEYUP and e.key == K_LSHIFT:
                self.running = False
            if e.type == KEYUP and e.key == K_SPACE:
                self.space = False
            if e.type == KEYUP and e.key == K_LCTRL:
                self.slowly = False

        self.surface.blit(self.bg, (0, 0))
        self.bullets.update(self.platforms)
        self.monsters.update(self.platforms)
        self.animatedEntities.update()
        self.camera.update(self.hero)
        for e in self.entities:
            self.surface.blit(e.image, self.camera.apply(e))

        if needSwitchWeapon:
            self.hero.switchWeapon()

        self.hero.update(self.left, self.right, self.up, self.space, self.running,
                         self.slowly, self.platforms)

        time_diff = time.get_ticks() - self.startTime

        self.ui.draw(self.hero.points, self.hero.health, (time_diff - time_diff % 1000) // 1000, self.hero.getWeaponSet())

        if self.hero.winner:
            if not self.winScreen:
                self.winScreen = True
                self.startWin = time.get_ticks()
                mixer.music.stop()
                self.s_winner.play()
                if self.levelName not in config.END_LEVELS:
                    config.END_LEVELS.append(self.levelName)
                refreshConfig()

            if self.startWin + 600 < time.get_ticks():
                label = font.Font('./emulogic.ttf', 30).render('YOU RESCUED MABEL!', False, '#ffffff')
                self.surface.blit(label, (config.WIN_WIDTH // 2 - label.get_width()//2, config.WIN_HEIGHT // 2 - 200))
            if self.startWin + 1200 < time.get_ticks():
                label = font.Font('./emulogic.ttf', 30).render('YOUR QUEST IS OVER.', False, '#ffffff')
                self.surface.blit(label, (config.WIN_WIDTH // 2 - label.get_width()//2, config.WIN_HEIGHT // 2 - 120))
            if self.startWin + 1700 < time.get_ticks():
                label = font.Font('./emulogic.ttf', 30).render('WE PRESENT YOU A NEW QUEST.', False, '#ffffff')
                self.surface.blit(label, (config.WIN_WIDTH // 2 - label.get_width()//2, config.WIN_HEIGHT // 2 - 70))
            if self.startWin + 2500 < time.get_ticks():
                label = font.Font('./emulogic.ttf', 30).render('PUSH BUTTON B', False, '#ffffff')
                self.surface.blit(label, (config.WIN_WIDTH // 2 - label.get_width()//2, config.WIN_HEIGHT // 2 + 10))
            if self.startWin + 3200 < time.get_ticks():
                label = font.Font('./emulogic.ttf', 30).render('TO SELECT A NEW LEVEL', False, '#ffffff')
                self.surface.blit(label, (config.WIN_WIDTH // 2 - label.get_width()//2, config.WIN_HEIGHT // 2 + 60))

            if self.startWin + config.WIN_SCREEN_TIME < time.get_ticks():
                self.canSkipWinScreen = True

class UI:
    def __init__(self, surf, world):
        self.surface = surf
        self.world = world
        self.font = font.Font('./emulogic.ttf', 25)
        self.fontWeapon = font.Font('./emulogic.ttf', 10)
        self.fontTime = font.Font('./emulogic.ttf', 18)
        self.imgHeart = transform.scale(image.load("images/Heart/heart.png").convert_alpha(), (32, 32))
        self.imgTape = transform.scale(image.load("images/UI/tape.png").convert_alpha(), (160, 160))
        self.imgSweater = transform.scale(image.load("images/UI/sweater.png").convert_alpha(), (128, 128))
        self.memo = {}



    def renderFont(self, font ,text):
        return font.render(str(text), False, config.MENU_COLOR_WHITE)

    def util(self, num, cur = -1, pre = 1e6):
        if self.memo.get(num) != None:
            return self.memo.get(num)
        if pre == 0 and num == 0:
            return cur-1
        res = num % pre
        if res == num:
            return self.util(num, cur + 1, pre // 10)
        else:
            self.memo[num] = cur
            return cur

    def draw(self, point, health, time, weaponSet):
        padding_left = 100
        padding_right = 75
        smallPadding = 25

        all_surface = self.surface.get_size()[0]
        step = all_surface - 150
        weaponName = self.renderFont(self.fontWeapon, weaponSet[1])
        self.surface.blit(self.imgSweater, (step, 10))
        self.surface.blit(weaponSet[0], (step + 25, 43))
        self.surface.blit(weaponName, (all_surface - (self.imgSweater.get_width()/2 + weaponName.get_width()/2) - 20, 143))

        step -= self.imgSweater.get_width() + padding_right
        timeLabel = self.renderFont(self.fontTime, 'TIME')
        timeValue = self.renderFont(self.fontTime, time)
        self.surface.blit(timeLabel, (step - 10, 30))
        self.surface.blit(timeValue, (step + timeLabel.get_size()[0] - timeValue.get_size()[0] - 10, 50))
        self.surface.blit(self.imgTape, (step - 85, -25))

        x = 100
        pointLabel = self.renderFont(self.font, 'WADDLES')
        pointValue = self.renderFont(self.font, '0' * self.util(point) + str(point))
        self.surface.blit(pointLabel, (x, 32.5))
        # self.surface.blit(pointValue, (x, 45))
        x += pointValue.get_width() + padding_left

        health_value = self.renderFont(self.font, '*' + str(health))
        self.surface.blit(self.imgHeart, (x - 10, 32.5))
        self.surface.blit(health_value, (x + smallPadding, 32.5))

        x += self.imgHeart.get_width() + health_value.get_width() + padding_right
        worldLabel = self.renderFont(self.font, 'LEVEL')
        worldValue = self.renderFont(self.font, self.world)
        self.surface.blit(worldLabel, (x, 20))
        self.surface.blit(worldValue, (x + (worldLabel.get_size()[0] - worldValue.get_size()[0]) // 2, 45))


if __name__ == '__main__':
    init()
    size = (config.WIN_WIDTH, config.WIN_HEIGHT)
    screen = display.set_mode(size)
    clock = time.Clock()
    # lvl1 = Level(screen, lambda: print('switch'), lambda: print('back'), "levels/1-1.tmx", '1-1')
    lvl1 = Level(screen, lambda: print('switch'), lambda: print('back'), "levels/lvl3.tmx", '1-1')
    running = True
    while running:
        events = event.get()
        for e in events:
            if e.type == QUIT:
                quit()
        lvl1.run(events)
        display.update()
        # print(f"{clock.get_fps():2.0f} FPS")
        clock.tick(60)
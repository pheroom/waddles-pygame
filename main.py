from pygame import *
from config import config, saveConfigOnExit, refreshConfig
from menu import Menu
from level import Level

mixer.init()
s_menu = mixer.Sound('music/menu.wav')
s_menu.set_volume(0.15 + config.VOLUME_LEVEL)
class MainScreen():
    def __init__(self, surf, switchScreen):
        self.switchScreen = switchScreen
        self.surface = surf
        self.menu = Menu()
        self.bg = transform.scale(image.load('images/bg-dwarfs.jpg'), (config.WIN_WIDTH, config.WIN_HEIGHT))
        self.menu.append_option('Level Selection', lambda: self.switchScreen(lvlSelectionScreen), config.MENU_COLOR_WHITE)
        self.menu.append_option('Settings', lambda: self.switchScreen(settingsScreen), config.MENU_COLOR_WHITE)
        self.menu.append_option('Quit', lambda: self.switchScreen(None), config.MENU_COLOR_WHITE)
        self.menu.append_option('RESET PROGRESS', lambda: self.switchScreen(resetProgress), config.MENU_COLOR_RED)
        self.menu.append_option('FULL PROGRESS', lambda: self.switchScreen(fullProgress), config.MENU_COLOR_BLUE)

    def run(self, events):
        for e in events:
            if e.type == KEYDOWN:
                if e.key == K_UP:
                    s_menu.play()
                    self.menu.switch(-1)
                elif e.key == K_DOWN:
                    s_menu.play()
                    self.menu.switch(1)
                elif e.key == K_SPACE:
                    s_menu.play()
                    self.menu.select()

        self.surface.blit(self.bg, (0,0))
        self.menu.draw(self.surface, 100, 100, 75)

class LevelSelectionScreen():
    def __init__(self, surf, switchScreen):
        self.switchScreen = switchScreen
        self.surface = surf
        self.menu = Menu()
        self.bg = transform.scale(image.load('images/bg2.png'), (config.WIN_WIDTH, config.WIN_HEIGHT))
        self.menu.append_option('1-1', lambda: self.switchScreen(lvl1Screen), config.MENU_COLOR_WHITE)
        if config.LEVEL_2_AVAILABLE:
            self.menu.append_option('1-2', lambda: self.switchScreen(lvl2Screen), config.MENU_COLOR_WHITE)
        else:
            self.menu.append_option('1-2', lambda: self.switchScreen(lvlSelectionScreen), config.MENU_COLOR_GREY)
        if config.LEVEL_3_AVAILABLE:
            self.menu.append_option('1-3', lambda: self.switchScreen(lvl3Screen), config.MENU_COLOR_WHITE)
        else:
            self.menu.append_option('1-3', lambda: self.switchScreen(lvlSelectionScreen), config.MENU_COLOR_GREY)
        self.menu.append_option('Back to menu', lambda: self.switchScreen(MainScreen), config.MENU_COLOR_WHITE)

    def run(self, events):
        for e in events:
            if e.type == KEYDOWN:
                if e.key == K_UP:
                    s_menu.play()
                    self.menu.switch(-1)
                elif e.key == K_DOWN:
                    s_menu.play()
                    self.menu.switch(1)
                elif e.key == K_SPACE:
                    s_menu.play()
                    self.menu.select()

        self.surface.blit(self.bg, (0,0))
        self.menu.draw(self.surface, 700, 50, 75)



class SettingsScreen():
    def __init__(self, surf, switchScreen):
        self.switchScreen = switchScreen
        self.surface = surf
        self.menu = Menu()
        self.bg = transform.scale(image.load('images/bg-dwarfs.jpg'), (config.WIN_WIDTH, config.WIN_HEIGHT))
        # def switchScale(size):
        #     config.PLATFORM_WIDTH = size
        #     config.PLATFORM_HEIGHT = size
        #     refreshConfig()
        self.menu.append_option('Selection scale', lambda: self.switchScreen(selectScaleScreen), config.MENU_COLOR_WHITE)
        self.menu.append_option('Selection volume', lambda: self.switchScreen(selectVolumeScreen), config.MENU_COLOR_WHITE)
        self.menu.append_option('Back to menu', lambda: self.switchScreen(MainScreen), config.MENU_COLOR_WHITE)

    def run(self, events):
        for e in events:
            if e.type == KEYDOWN:
                if e.key == K_UP:
                    s_menu.play()
                    self.menu.switch(-1)
                elif e.key == K_DOWN:
                    s_menu.play()
                    self.menu.switch(1)
                elif e.key == K_SPACE:
                    s_menu.play()
                    self.menu.select()

        self.surface.blit(self.bg, (0,0))
        self.menu.draw(self.surface, 700, 50, 75)

class SelectScaleScreen():
    def __init__(self, surf, switchScreen):
        self.switchScreen = switchScreen
        self.surface = surf
        self.menu = Menu()
        self.bg = transform.scale(image.load('images/bg-dwarfs.jpg'), (config.WIN_WIDTH, config.WIN_HEIGHT))
        self.title = font.Font('./emulogic.ttf', 45).render('Select game scale', False, '#ffffff')
        def switchScale(size):
            config.PLATFORM_WIDTH = size
            config.PLATFORM_HEIGHT = size
            refreshConfig()
            self.switchScreen(settingsScreen)
        self.menu.append_option('Small', lambda: switchScale(32), config.PLATFORM_WIDTH == 32, config.MENU_COLOR_WHITE)
        self.menu.append_option('Medium', lambda: switchScale(48), config.PLATFORM_WIDTH == 48, config.MENU_COLOR_WHITE)
        self.menu.append_option('Large', lambda: switchScale(64), config.PLATFORM_WIDTH == 64, config.MENU_COLOR_WHITE)
        self.menu.append_option('Back to settings', lambda: self.switchScreen(settingsScreen), config.MENU_COLOR_WHITE)

    def run(self, events):
        for e in events:
            if e.type == KEYDOWN:
                if e.key == K_UP:
                    s_menu.play()
                    self.menu.switch(-1)
                elif e.key == K_DOWN:
                    s_menu.play()
                    self.menu.switch(1)
                elif e.key == K_SPACE:
                    s_menu.play()
                    self.menu.select()

        self.surface.blit(self.bg, (0,0))
        self.surface.blit(self.title, (100, 100))
        self.menu.draw(self.surface, 100, 200, 75)

class SelectVolumeScreen():
    def __init__(self, surf, switchScreen):
        self.switchScreen = switchScreen
        self.surface = surf
        self.menu = Menu()
        self.bg = transform.scale(image.load('images/bg-dwarfs.jpg'), (config.WIN_WIDTH, config.WIN_HEIGHT))
        self.title = font.Font('./emulogic.ttf', 45).render('Select game volume', False, '#ffffff')
        def switchVolume(level):
            config.VOLUME_LEVEL = level
            refreshConfig()
            self.switchScreen(settingsScreen)
        self.menu.append_option('Quiet', lambda: switchVolume(-0.1), config.VOLUME_LEVEL == -0.1, config.MENU_COLOR_WHITE)
        self.menu.append_option('Average', lambda: switchVolume(0), config.VOLUME_LEVEL == 0, config.MENU_COLOR_WHITE)
        self.menu.append_option('Loud', lambda: switchVolume(0.1), config.VOLUME_LEVEL == 0.1, config.MENU_COLOR_WHITE)
        self.menu.append_option('Back to settings', lambda: self.switchScreen(settingsScreen), config.MENU_COLOR_WHITE)

    def run(self, events):
        for e in events:
            if e.type == KEYDOWN:
                if e.key == K_UP:
                    s_menu.play()
                    self.menu.switch(-1)
                elif e.key == K_DOWN:
                    s_menu.play()
                    self.menu.switch(1)
                elif e.key == K_SPACE:
                    s_menu.play()
                    self.menu.select()

        self.surface.blit(self.bg, (0,0))
        self.surface.blit(self.title, (100, 100))
        self.menu.draw(self.surface, 100, 200, 75)


class Game():
    def __init__(self, surf):
        self.currentScreen = None
        self.surface = surf

    def switchScreen(self, Screen):
        s_menu.set_volume(0.15 + config.VOLUME_LEVEL)
        self.currentScreen = Screen and Screen(self.surface, self.switchScreen)

    def run(self, events):
        if(self.currentScreen):
            self.currentScreen.run(events)

init()
size = (config.WIN_WIDTH, config.WIN_HEIGHT)
screen = display.set_mode(size)
clock = time.Clock()
game = Game(screen)
display.set_caption("Waddles")
marioIcon = image.load('./images/coin_block.png')
display.set_icon(marioIcon)

def lvl1Screen(screen, switchScreen):
    return Level(screen, switchScreen, lambda: game.switchScreen(lvlSelectionScreen), "levels/lvl1.tmx", '1-1')

def lvl2Screen(screen, switchScreen):
    return Level(screen, switchScreen, lambda: game.switchScreen(lvlSelectionScreen), "levels/lvl2.tmx", '1-2')

def lvl3Screen(screen, switchScreen):
    return Level(screen, switchScreen, lambda: game.switchScreen(lvlSelectionScreen), "levels/lvl3.tmx", '1-3')

def lvlSelectionScreen(screen, switchScreen):
    mixer.music.stop()
    return LevelSelectionScreen(screen, switchScreen)

def resetProgress(screen, switchScreen):
    config.LEVEL_2_AVAILABLE = False
    config.LEVEL_3_AVAILABLE = False
    refreshConfig()
    return LevelSelectionScreen(screen, switchScreen)

def fullProgress(screen, switchScreen):
    config.LEVEL_2_AVAILABLE = True
    config.LEVEL_3_AVAILABLE = True
    refreshConfig()
    return LevelSelectionScreen(screen, switchScreen)

def settingsScreen(screen, switchScreen):
    return SettingsScreen(screen, switchScreen)

def selectScaleScreen(screen, switchScreen):
    return SelectScaleScreen(screen, switchScreen)

def selectVolumeScreen(screen, switchScreen):
    return SelectVolumeScreen(screen, switchScreen)

game.switchScreen(MainScreen)
while game.currentScreen is not None:
    events = event.get()
    for e in events:
        if e.type == QUIT:
            game.switchScreen(None)
    game.run(events)
    display.update()
    clock.tick(60)

saveConfigOnExit()
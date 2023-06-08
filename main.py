from pygame import *
from config import config, saveConfigOnExit, refreshConfig
from menu import Menu
from level import Level

class MainScreen():
    def __init__(self, surf, switchScreen):
        self.switchScreen = switchScreen
        self.surface = surf
        self.menu = Menu()
        self.bg = transform.scale(image.load('images/bg-dwarfs.jpg'), (config.WIN_WIDTH, config.WIN_HEIGHT))
        self.menu.append_option('Level Selection', lambda: self.switchScreen(lvlSelectionScreen))
        self.menu.append_option('Settings', lambda: self.switchScreen(settingsScreen))
        self.menu.append_option('Quit', lambda: self.switchScreen(None))

    def run(self, events):
        for e in events:
            if e.type == KEYDOWN:
                if e.key == K_UP:
                    self.menu.switch(-1)
                elif e.key == K_DOWN:
                    self.menu.switch(1)
                elif e.key == K_SPACE:
                    self.menu.select()

        self.surface.blit(self.bg, (0,0))
        self.menu.draw(self.surface, 100, 100, 75)

class LevelSelectionScreen():
    def __init__(self, surf, switchScreen):
        self.switchScreen = switchScreen
        self.surface = surf
        self.menu = Menu()
        self.bg = transform.scale(image.load('images/bg2.png'), (config.WIN_WIDTH, config.WIN_HEIGHT))
        self.menu.append_option('1-1', lambda: self.switchScreen(lvl1Screen))
        self.menu.append_option('2-1', lambda: self.switchScreen(lvl2Screen))
        self.menu.append_option('Back to menu', lambda: self.switchScreen(MainScreen))

    def run(self, events):
        for e in events:
            if e.type == KEYDOWN:
                if e.key == K_UP:
                    self.menu.switch(-1)
                elif e.key == K_DOWN:
                    self.menu.switch(1)
                elif e.key == K_SPACE:
                    self.menu.select()

        self.surface.blit(self.bg, (0,0))
        self.menu.draw(self.surface, 700, 50, 75)

class SettingsScreen():
    def __init__(self, surf, switchScreen):
        self.switchScreen = switchScreen
        self.surface = surf
        self.menu = Menu()
        self.bg = transform.scale(image.load('images/bg-dwarfs.jpg'), (config.WIN_WIDTH, config.WIN_HEIGHT))
        def switchScale(size):
            config.PLATFORM_WIDTH = size
            config.PLATFORM_HEIGHT = size
            refreshConfig()
        self.menu.append_option('Selection scale', lambda: self.switchScreen(selectScaleScreen))
        self.menu.append_option('Back to menu', lambda: self.switchScreen(MainScreen))

    def run(self, events):
        for e in events:
            if e.type == KEYDOWN:
                if e.key == K_UP:
                    self.menu.switch(-1)
                elif e.key == K_DOWN:
                    self.menu.switch(1)
                elif e.key == K_SPACE:
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
        self.menu.append_option('Small', lambda: switchScale(32), config.PLATFORM_WIDTH == 32)
        self.menu.append_option('Medium', lambda: switchScale(48), config.PLATFORM_WIDTH == 48)
        self.menu.append_option('Large', lambda: switchScale(64), config.PLATFORM_WIDTH == 64)
        self.menu.append_option('Back to settings', lambda: self.switchScreen(settingsScreen))

    def run(self, events):
        for e in events:
            if e.type == KEYDOWN:
                if e.key == K_UP:
                    self.menu.switch(-1)
                elif e.key == K_DOWN:
                    self.menu.switch(1)
                elif e.key == K_SPACE:
                    self.menu.select()

        self.surface.blit(self.bg, (0,0))
        self.surface.blit(self.title, (100, 100))
        self.menu.draw(self.surface, 100, 200, 75)

class Game():
    def __init__(self, surf):
        self.currentScreen = None
        self.surface = surf

    def switchScreen(self, Screen):
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
marioIcon = image.load('./images/logo-mabel.png')
display.set_icon(marioIcon)

def lvl1Screen(screen, switchScreen):
    return Level(screen, switchScreen, lambda: game.switchScreen(lvlSelectionScreen), "levels/1-1.tmx", '1-1')

def lvl2Screen(screen, switchScreen):
    return Level(screen, switchScreen, lambda: game.switchScreen(lvlSelectionScreen), "levels/lvl1.tmx", '2-1')

def lvlSelectionScreen(screen, switchScreen):
    return LevelSelectionScreen(screen, switchScreen)

def settingsScreen(screen, switchScreen):
    return SettingsScreen(screen, switchScreen)

def selectScaleScreen(screen, switchScreen):
    return SelectScaleScreen(screen, switchScreen)

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
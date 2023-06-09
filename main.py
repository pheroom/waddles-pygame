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
        if '1-1' in config.END_LEVELS:
            self.menu.append_option('1-2', lambda: self.switchScreen(lvl2Screen), config.MENU_COLOR_WHITE)
        else:
            self.menu.append_option('1-2', lambda: self.switchScreen(lvlSelectionScreen), config.MENU_COLOR_GREY)
        if '1-2' in config.END_LEVELS:
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
                elif e.key == K_ESCAPE:
                    s_menu.play()
                    self.switchScreen(MainScreen)

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
        self.menu.append_option('Controls', lambda: self.switchScreen(controlsScreen), config.MENU_COLOR_WHITE)
        self.menu.append_option('Selection scale', lambda: self.switchScreen(selectScaleScreen), config.MENU_COLOR_WHITE)
        self.menu.append_option('Selection volume', lambda: self.switchScreen(selectVolumeScreen), config.MENU_COLOR_WHITE)
        self.menu.append_option('Selection screen resolution', lambda: self.switchScreen(selectScreenResolution), config.MENU_COLOR_WHITE)
        self.menu.append_option('RESET PROGRESS', lambda: self.switchScreen(resetProgress), config.MENU_COLOR_RED)
        # self.menu.append_option('FULL PROGRESS', lambda: self.switchScreen(fullProgress), config.MENU_COLOR_BLUE)
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
                elif e.key == K_ESCAPE:
                    s_menu.play()
                    self.switchScreen(MainScreen)

        self.surface.blit(self.bg, (0,0))
        self.menu.draw(self.surface, 100, 50, 75)

class ControlsScreen():
    def __init__(self, surf, switchScreen):
        self.switchScreen = switchScreen
        self.surface = surf
        self.menu = Menu()
        self.bg = transform.scale(image.load('images/keyboard.png'), (config.WIN_WIDTH, config.WIN_HEIGHT))
        self.title = font.Font('./emulogic.ttf', 45).render('Controls', False, config.MENU_COLOR_WHITE)
        self.menu.append_option('Back to settings', lambda: self.switchScreen(settingsScreen), config.MENU_COLOR_WHITE)

    def run(self, events):
        for e in events:
            if e.type == KEYDOWN:
                if e.key == K_SPACE:
                    s_menu.play()
                    self.menu.select()
                elif e.key == K_ESCAPE:
                    s_menu.play()
                    self.switchScreen(settingsScreen)

        self.surface.blit(self.bg, (0,0))
        self.surface.blit(self.title, (config.WIN_WIDTH / 2 - self.title.get_width()/2 - 20, 20))
        self.menu.draw(self.surface, 80, config.WIN_HEIGHT - 60, 75)
class SelectScaleScreen():
    def __init__(self, surf, switchScreen):
        self.switchScreen = switchScreen
        self.surface = surf
        self.menu = Menu()
        self.bg = transform.scale(image.load('images/bg-dwarfs.jpg'), (config.WIN_WIDTH, config.WIN_HEIGHT))
        self.title = font.Font('./emulogic.ttf', 45).render('Select game scale', False, config.MENU_COLOR_WHITE)
        def switchScale(size):
            config.PLATFORM_WIDTH = size
            config.PLATFORM_HEIGHT = size
            refreshConfig()
            self.switchScreen(settingsScreen)
        self.menu.append_option('Small', lambda: switchScale(32), config.MENU_COLOR_WHITE, config.PLATFORM_WIDTH == 32)
        self.menu.append_option('Medium', lambda: switchScale(48), config.MENU_COLOR_WHITE, config.PLATFORM_WIDTH == 48)
        self.menu.append_option('Large', lambda: switchScale(64), config.MENU_COLOR_WHITE, config.PLATFORM_WIDTH == 64)
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
                elif e.key == K_ESCAPE:
                    s_menu.play()
                    self.switchScreen(settingsScreen)

        self.surface.blit(self.bg, (0,0))
        self.surface.blit(self.title, (100, 100))
        self.menu.draw(self.surface, 100, 200, 75)

class SelectVolumeScreen():
    def __init__(self, surf, switchScreen):
        self.switchScreen = switchScreen
        self.surface = surf
        self.menu = Menu()
        self.bg = transform.scale(image.load('images/bg-dwarfs.jpg'), (config.WIN_WIDTH, config.WIN_HEIGHT))
        self.title = font.Font('./emulogic.ttf', 45).render('Select game volume', False, config.MENU_COLOR_WHITE)
        def switchVolume(level):
            config.VOLUME_LEVEL = level
            refreshConfig()
            self.switchScreen(settingsScreen)
        self.menu.append_option('Quiet', lambda: switchVolume(-0.1), config.MENU_COLOR_WHITE, config.VOLUME_LEVEL == -0.1)
        self.menu.append_option('Average', lambda: switchVolume(0), config.MENU_COLOR_WHITE, config.VOLUME_LEVEL == 0)
        self.menu.append_option('Loud', lambda: switchVolume(0.1), config.MENU_COLOR_WHITE, config.VOLUME_LEVEL == 0.1)
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
                elif e.key == K_ESCAPE:
                    s_menu.play()
                    self.switchScreen(settingsScreen)

        self.surface.blit(self.bg, (0,0))
        self.surface.blit(self.title, (100, 100))
        self.menu.draw(self.surface, 100, 200, 75)

class SelectScreenResolutionScreen():
    def __init__(self, surf, switchScreen):
        self.switchScreen = switchScreen
        self.surface = surf
        self.menu = Menu()
        self.bg = transform.scale(image.load('images/bg-dwarfs.jpg'), (config.WIN_WIDTH, config.WIN_HEIGHT))
        self.title = font.Font('./emulogic.ttf', 45).render('Select game resolution', False, config.MENU_COLOR_WHITE)
        def switchResolution(width, height):
            config.WIN_WIDTH = width
            config.WIN_HEIGHT = height
            display.set_mode((width, height))
            refreshConfig()
            self.switchScreen(settingsScreen)
        def createOption(w, h):
            self.menu.append_option(f'{w}x{h}', lambda: switchResolution(w, h), config.MENU_COLOR_WHITE, config.WIN_WIDTH == w and config.WIN_HEIGHT == h)
        # createOption(800, 600)
        createOption(1280, 720)
        createOption(1600, 900)
        self.menu.append_option('Back to settings', lambda: self.switchScreen(settingsScreen), config.MENU_COLOR_WHITE)

    def run(self, events):
        for e in events:
            if e.type == KEYDOWN:
                s_menu.play()
                if e.key == K_UP:
                    self.menu.switch(-1)
                elif e.key == K_DOWN:
                    self.menu.switch(1)
                elif e.key == K_SPACE:
                    self.menu.select()
                elif e.key == K_ESCAPE:
                    s_menu.play()
                    self.switchScreen(settingsScreen)

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
    if '1-1' in config.END_LEVELS:
        config.END_LEVELS.remove('1-1')
    if '1-2' in config.END_LEVELS:
        config.END_LEVELS.remove('1-2')
    refreshConfig()
    return LevelSelectionScreen(screen, switchScreen)

# def fullProgress(screen, switchScreen):
#     if '1-1' not in config.END_LEVELS:
#         config.END_LEVELS.append('1-1')
#     if '1-2' not in config.END_LEVELS:
#         config.END_LEVELS.append('1-2')
#     refreshConfig()
#     return LevelSelectionScreen(screen, switchScreen)

def settingsScreen(screen, switchScreen):
    return SettingsScreen(screen, switchScreen)

def selectScaleScreen(screen, switchScreen):
    return SelectScaleScreen(screen, switchScreen)

def selectVolumeScreen(screen, switchScreen):
    return SelectVolumeScreen(screen, switchScreen)

def selectScreenResolution(screen, switchScreen):
    return SelectScreenResolutionScreen(screen, switchScreen)

def controlsScreen(screen, switchScreen):
    return ControlsScreen(screen, switchScreen)

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
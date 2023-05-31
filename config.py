import pickle

class Config:
    pass
config = Config()

with open("configfile.pickle", 'rb') as f:
    configData = pickle.load(f)
# config.__dict__ = configData

config.PLATFORM_WIDTH = configData['PLATFORM_WIDTH']
config.PLATFORM_HEIGHT = configData['PLATFORM_HEIGHT']

def refreshConfig():
    config.PLATFORM_COLOR = "#FF6262"

    config.WIN_SCREEN_TIME = 3000
    config.DEAD_SCREEN_TIME = 2000

    config.WIN_WIDTH = 1280
    config.WIN_HEIGHT = 720

    config.BG_COLOR_DUNGEON = '#000000'
    config.BG_COLOR_SKY = '#5C94FC'

    config.HERO_PHYSICAL_WIDTH = config.PLATFORM_WIDTH * 0.8
    config.HERO_PHYSICAL_HEIGHT = config.PLATFORM_HEIGHT
    config.HERO_WIDTH = config.PLATFORM_WIDTH
    config.HERO_HEIGHT = config.PLATFORM_HEIGHT
    config.MOVE_SPEED = 6 * config.HERO_WIDTH / 32
    config.COLOR = "#888888"
    config.JUMP_POWER = 12 * config.HERO_HEIGHT / 32
    config.GRAVITY = 0.5 * config.HERO_HEIGHT / 32

    config.JUMP_SLOW_POWER = 2 * config.HERO_HEIGHT / 32
    config.MOVE_SLOW_SPEED = 2 * config.HERO_WIDTH / 32

    config.MOVE_EXTRA_SPEED = 2.5 * config.HERO_WIDTH / 32
    config.JUMP_EXTRA_POWER = 1 / 5 * config.HERO_HEIGHT / 32
    config.ANIMATION_SUPER_SPEED_DELAY = 0.05

    config.ANIMATION_DELAY = 0.1
    config.ANIMATION_RIGHT = [('images/mario/r1.png'),
                              ('images/mario/r2.png'),
                              ('images/mario/r3.png'),
                              ('images/mario/r4.png'),
                              ('images/mario/r5.png')]
    config.ANIMATION_LEFT = [('images/mario/l1.png'),
                             ('images/mario/l2.png'),
                             ('images/mario/l3.png'),
                             ('images/mario/l4.png'),
                             ('images/mario/l5.png')]
    config.ANIMATION_JUMP_LEFT = [('images/mario/jl.png', 0.1)]
    config.ANIMATION_JUMP_RIGHT = [('images/mario/jr.png', 0.1)]
    config.ANIMATION_JUMP = [('images/mario/j.png', 0.1)]
    config.ANIMATION_STAY = [('images/mario/0.png', 0.1)]

    config.ANIMATION_BLOCKTELEPORT = [
        ('images/portal2.png'),
        ('images/portal1.png')]

    config.MONSTER_WIDTH = config.PLATFORM_WIDTH
    config.MONSTER_HEIGHT = config.PLATFORM_HEIGHT
    config.MONSTER_COLOR = "#2110FF"

    config.ANIMATION_MONSTERHORYSONTAL = [('images/goomba1.png'),
                                          ('images/goomba2.png')]

    config.ANIMATION_PRINCESS = [
        ('images/princess_l.png'),
        ('images/princess_r.png')]

    config.ANIMATION_COIN = [
        ('images/coin1.png'),
        ('images/coin2.png')]

    config.ANIMATION_FLOWER = [
        ('images/flower/flower1.png'),
        ('images/flower/flower2.png'),
        ('images/flower/flower3.png'),
        ('images/flower/flower4.png')]

refreshConfig()

def saveConfigOnExit():
    with open("configfile.pickle", "wb") as f:
        pickle.dump(config.__dict__, f)
import pickle

class Config:
    pass
config = Config()

with open("configfile.pickle", 'rb') as f:
    configData = pickle.load(f)
# config.__dict__ = configData

config.PLATFORM_WIDTH = configData['PLATFORM_WIDTH']
config.PLATFORM_HEIGHT = configData['PLATFORM_HEIGHT']
config.VOLUME_LEVEL = configData['VOLUME_LEVEL']

def refreshConfig():
    config.PLATFORM_COLOR = "#FF6262"

    config.WIN_SCREEN_TIME = 3000
    config.DEAD_SCREEN_TIME = 2000

    config.WIN_WIDTH = 1280
    config.WIN_HEIGHT = 720

    config.BG_COLOR_DUNGEON = '#000000'
    config.BG_COLOR_SKY = '#5C94FC'

    config.HERO_PHYSICAL_WIDTH = config.PLATFORM_WIDTH * 0.6875
    config.HERO_PHYSICAL_HEIGHT = config.PLATFORM_HEIGHT
    config.HERO_WIDTH = config.PLATFORM_WIDTH * 0.6875
    config.HERO_HEIGHT = config.PLATFORM_HEIGHT
    config.MOVE_SPEED = 4 * config.HERO_WIDTH / 32
    config.COLOR = "#888888"
    config.JUMP_POWER = 9 * config.HERO_HEIGHT / 32
    config.GRAVITY = 0.4 * config.HERO_HEIGHT / 32

    config.JUMP_SLOW_POWER = 2 * config.HERO_HEIGHT / 32
    config.MOVE_SLOW_SPEED = 2 * config.HERO_WIDTH / 32

    config.MOVE_EXTRA_SPEED = 2.5 * config.HERO_WIDTH / 32
    config.JUMP_EXTRA_POWER = 1 / 5 * config.HERO_HEIGHT / 32
    config.ANIMATION_SUPER_SPEED_DELAY = 0.05

    config.HERO_HEALTH = 10
    config.MONSTER_HEALTH = 3

    config.ANIMATION_DELAY = 0.12
    config.ANIMATION_STAY_DELAY = 0.8
    config.ANIMATION_HIT_DELAY = 0.5
    config.ANIMATION_RIGHT = ['images/waddles/waddles_run_r1.png',
                   'images/waddles/waddles_run_r2.png',
                   'images/waddles/waddles_run_r3.png',
                   'images/waddles/waddles_run_r4.png']
    config.ANIMATION_LEFT = ['images/waddles/waddles_run_l1.png',
                  'images/waddles/waddles_run_l2.png',
                  'images/waddles/waddles_run_l3.png',
                  'images/waddles/waddles_run_l4.png']
    config.ANIMATION_JUMP_LEFT = [('images/waddles/waddles_jump_l.png',  config.ANIMATION_DELAY)]
    config.ANIMATION_JUMP_RIGHT = [('images/waddles/waddles_jump_r.png',  config.ANIMATION_DELAY)]
    config.ANIMATION_JUMP = [('images/waddles/waddles_jump.png',  config.ANIMATION_DELAY)]
    config.ANIMATION_STAY = ['images/waddles/waddles_stay1.png',
                  'images/waddles/waddles_stay2.png']
    config.ANIMATION_HIT_RIGHT = [('images/waddles/waddles_hit_r.png', config.ANIMATION_HIT_DELAY)]
    config.ANIMATION_HIT_LEFT = [('images/waddles/waddles_hit_l.png', config.ANIMATION_HIT_DELAY)]


    config.ANIMATION_BLOCKTELEPORT = [
        ('images/portal2.png'),
        ('images/portal1.png')]
    
    config.MONSTER_DELAY = 0.1
    config.MONSTER_WIDTH = config.PLATFORM_WIDTH
    config.MONSTER_HEIGHT = config.PLATFORM_HEIGHT
    config.MONSTER_COLOR = "#2110FF"

    config.ANIMATION_DWARF_STAY = ['images/usual_dwarf/dwarf_stay.png']

    config.ANIMATION_USUAL_DWARF_L = ['images/usual_dwarf/usual_dwarf_run_l1.png',
                               'images/usual_dwarf/usual_dwarf_run_l2.png',
                               'images/usual_dwarf/usual_dwarf_run_l3.png',
                               'images/usual_dwarf/usual_dwarf_run_l4.png']
    config.ANIMATION_USUAL_DWARF_R = ['images/usual_dwarf/usual_dwarf_run_r1.png',
                               'images/usual_dwarf/usual_dwarf_run_r2.png',
                               'images/usual_dwarf/usual_dwarf_run_r3.png',
                               'images/usual_dwarf/usual_dwarf_run_r4.png']

    config.ANIMATION_PUKING_DWARF_l = ['images/puking_dwarf/puking_dwarf1.png',
                                            'images/puking_dwarf/puking_dwarf_r2.png',
                                            'images/puking_dwarf/puking_dwarf_r3.png']
    config.ANIMATION_PUKING_DWARF_r = ['images/puking_dwarf/puking_dwarf1.png',
                                     'images/puking_dwarf/puking_dwarf_l2.png',
                                     'images/puking_dwarf/puking_dwarf_l3.png']

    config.ANIMATION_GIDEON_L = ['images/gideon/gideon_l.png']
    config.ANIMATION_GIDEON_R = ['images/gideon/gideon_r.png']


    config.ANIMATION_PRINCESS = [
        'images/mabel/mabel_stay1.png',
        'images/mabel/mabel_stay2.png']

    config.ANIMATION_COIN = [
        ('images/coin1.png'),
        ('images/coin2.png')]

    config.ANIMATION_FLOWER = [
        ('images/Heart/heart1.png'),
    ('images/Heart/heart2.png'),
    ('images/Heart/heart3.png'),
    ('images/Heart/heart4.png'),
    ('images/Heart/heart3.png'),
    ('images/Heart/heart2.png')]


refreshConfig()

def saveConfigOnExit():
    with open("configfile.pickle", "wb") as f:
        pickle.dump(config.__dict__, f)

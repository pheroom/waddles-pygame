from pygame import *
PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32

PLATFORM_COLOR = "#FF6262"

WIN_SCREEN_TIME = 3000
DEAD_SCREEN_TIME = 2000

WIN_WIDTH = 1280
WIN_HEIGHT = 720

BG_COLOR_DUNGEON = '#000000'
BG_COLOR_SKY = '#5C94FC'

MOVE_SPEED = 5
HERO_PHYSICAL_WIDTH = 128
HERO_PHYSICAL_HEIGHT = 128
HERO_WIDTH = 128
HERO_HEIGHT = 128
COLOR = "#888888"
JUMP_POWER = 11
GRAVITY = 0.5

JUMP_SLOW_POWER = 2
MOVE_SLOW_SPEED = 3

MOVE_EXTRA_SPEED = 2.5
JUMP_EXTRA_POWER = 2
ANIMATION_SUPER_SPEED_DELAY = 0.05

ANIMATION_DELAY = 0.12
ANIMATION_STAY_DELAY = 0.8
ANIMATION_RIGHT = ['images/waddles/waddles_run_r1.png',
                   'images/waddles/waddles_run_r2.png',
                   'images/waddles/waddles_run_r3.png',
                   'images/waddles/waddles_run_r4.png']
ANIMATION_LEFT = ['images/waddles/waddles_run_l1.png',
                  'images/waddles/waddles_run_l2.png',
                  'images/waddles/waddles_run_l3.png',
                  'images/waddles/waddles_run_l4.png']
ANIMATION_STAY = ['images/waddles/waddles_stay1.png',
                  'images/waddles/waddles_stay2.png']
jump_l = transform.scale(image.load('images/waddles/waddles_jump_l.png'), (HERO_WIDTH, HERO_HEIGHT))
ANIMATION_JUMP_LEFT = [(jump_l, ANIMATION_DELAY)]
jump_r = transform.scale(image.load('images/waddles/waddles_jump_r.png'), (HERO_WIDTH, HERO_HEIGHT))
ANIMATION_JUMP_RIGHT = [(jump_r, ANIMATION_DELAY)]
jump = transform.scale(image.load('images/waddles/waddles_jump.png'), (HERO_WIDTH, HERO_HEIGHT))
ANIMATION_JUMP = [(jump, ANIMATION_DELAY)]


ANIMATION_BLOCKTELEPORT = [
            ('images/portal2.png'),
            ('images/portal1.png')]

MONSTER_DELAY = 0.1
MONSTER_WIDTH = 80
MONSTER_HEIGHT = 80
MONSTER_COLOR = "#2110FF"

ANIMATION_MONSTERHORYSONTAL_l = ['images/usual_dwarf/usual_dwarf_run_l1.png',
                               'images/usual_dwarf/usual_dwarf_run_l2.png',
                               'images/usual_dwarf/usual_dwarf_run_l3.png',
                               'images/usual_dwarf/usual_dwarf_run_l4.png']
ANIMATION_MONSTERHORYSONTAL_r = ['images/usual_dwarf/usual_dwarf_run_r1.png',
                               'images/usual_dwarf/usual_dwarf_run_r2.png',
                               'images/usual_dwarf/usual_dwarf_run_r3.png',
                               'images/usual_dwarf/usual_dwarf_run_r4.png']

ANIMATION_PRINCESS = [
    ('images/mabel/mabel_stay1.png'),
    ('images/mabel/mabel_stay2.png')]

ANIMATION_COIN = [
    ('images/coin1.png'),
    ('images/coin2.png')]

ANIMATION_FLOWER = [
    ('images/flower/flower1.png'),
    ('images/flower/flower2.png'),
    ('images/flower/flower3.png'),
    ('images/flower/flower4.png')]
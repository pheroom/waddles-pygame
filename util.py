from pygame import *
from config import *

def transformAnim(anim):
    return [(transformImg(anim[0][0]), anim[0][1])]

def transformImg(img, isPng = True):
    if (isinstance(img, str)):
        return transform.scale(image.load(img).convert_alpha() if isPng else image.load(img).convert(), (config.PLATFORM_WIDTH, config.PLATFORM_HEIGHT))
    return transform.scale(img.convert_alpha() if isPng else img.convert(), (config.PLATFORM_WIDTH, config.PLATFORM_HEIGHT))

BULLET_MONSTER = image.load('./images/bullet/bullet_rainbow.png')
BULLET_HERO = image.load('./images/bullet/bullet_hook.png')
BULLET_MUSHROOM = image.load('./images/bullet/mushroom.png')

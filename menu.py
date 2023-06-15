from pygame import *
class Menu:
    def __init__(self):
        self._option_surfaces = []
        self._callbacks = []
        self._current_option_index = 0
        self.ARIAL_50 = font.SysFont('arial', 50)
        self.font = font.Font('./emulogic.ttf', 30)
        # self.point = image.load('images/smallMushroom.png').convert_alpha()
        self.point = transform.scale(image.load('images/cap.png').convert_alpha(), (50,50))
        self.activePoint = transform.scale(image.load('images/star.png').convert_alpha(), (41,40))
        self.activeOption = []

    def append_option(self, option, callback, colour, isActive = False):
        self._option_surfaces.append(self.font.render(option, True, colour))
        self._callbacks.append(callback)
        if isActive:
            self.activeOption.append(len(self._option_surfaces) - 1)

    def switch(self, direction):
        self._current_option_index = max(0, min(self._current_option_index + direction,
                                                len(self._option_surfaces) - 1))

    def select(self):
        self._callbacks[self._current_option_index]()

    def draw(self, surf, x, y, option_y_padding):
        for i, option in enumerate(self._option_surfaces):
            option_rect = option.get_rect()
            option_rect.topleft = (x, y + i * option_y_padding)
            if i == self._current_option_index:
                # draw.rect(surf, (0, 50, 0), option_rect)
                surf.blit(self.point, (option_rect.x - 60, option_rect.y ))
            if i in self.activeOption:
                surf.blit(self.activePoint, (option_rect.right + 15, option_rect.y - 2))
            surf.blit(option, option_rect)
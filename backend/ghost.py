import parametros as p
from PyQt5.QtCore import (
    pyqtSignal, QRect
)
from PyQt5.QtGui import QPixmap
from backend.entity import Entity
from random import randint, random

class Ghost(Entity):

    def __init__(self, ghost_position: tuple[int, int], *args, **kwargs):
        velocidad = random() * (p.MAX_VELOCIDAD - p.MIN_VELOCIDAD) + p.MIN_VELOCIDAD
        super().__init__(
            entity_posititon=ghost_position,
            speed=velocidad/10,
            *args, **kwargs
        )
        self.x_direction = 0
        self.y_direction = 0

    def last_iteration(self):
        self._index = 0
        pass

    def get_next_img_src(self) -> str:
        self._index = self._index % 3
        direction = self.x_direction + self.y_direction
        img = self.sprites[direction][self._index]
        self._index += 1
        return img
    
    def start(self):
        self._timer_move.start()

    def stop(self):
        self._timer_move.stop()

    def dead(self):
        self.delete()

    def bounce(self):
        self.x_direction *= -1
        self.y_direction *= -1
        # super().bounce()
        self._pos.moveTo(
            self.x() + self.x_direction * self._steps[self._index],
            self.y() + self.y_direction * self._steps[self._index]
        )
        
class RedGhost(Ghost):
    def __init__(self, red_ghost_position: tuple[int, int], *arg, **kwargs):
        super().__init__(ghost_position=red_ghost_position, *arg, **kwargs)
        self.sprites = {
            -1: p.RED_GHOST_DOWN_SPRITES,
            1: p.RED_GHOST_UP_SPRITES,
        }
        self.y_direction = 1
        self.img = self.sprites[self.y_direction][0]

class WhiteGhost(Ghost):
    def __init__(self, white_ghost_position: tuple[int, int], *arg, **kwargs):
        super().__init__(ghost_position=white_ghost_position, *arg, **kwargs)
        self.sprites = {
            -1: p.WHITE_GHOST_LEFT_SPRITES,
            1: p.WHITE_GHOST_RIGTH_SPRITES,
        }
        self.x_direction = 1
        self.img = self.sprites[self.x_direction][0]

from PyQt5.QtCore import (
    pyqtSignal, QRect, QObject, QTimer,
)
from PyQt5.QtGui import QPixmap
from backend.entity import Entity
import parametros as p
""" 
"""


class Luigi(Entity):

    signal_lives = pyqtSignal(int)

    def __init__(self, luigi_position: tuple[int, int], *args, **kwargs):
        super().__init__(
            entity_posititon=luigi_position, 
            entity_main_img_src=p.LUIGI_SPRITE,
            # timer_interval=int(p.VELOCIDAD_LUIGI * 1000),
            speed=p.VELOCIDAD_LUIGI,
            *args, **kwargs
        )
        self.sprites = {
            p.LEFT: p.LUIGI_LEFT_SPRITES,
            p.RIGHT: p.LUIGI_RIGTH_SPRITES,
            p.UP: p.LUIGI_UP_SPRITES,
            p.DOWN: p.LUIGI_DOWN_SPRITES
        }
        # vidas restantes
        self.lives = p.CANTIDAD_VIDAS

    def get_next_img_src(self) -> str:
        direction = (self.x_direction, self.y_direction)
        if self._index == 3:
            self._index = 0
            self._timer_move.stop()
            img = self._main_img
        else:
            img = self.sprites[direction][self._index]
            self._index += 1
        return img
    
    def move_to(self, move_direction: tuple[int, int]):
        self.x_direction, self.y_direction = move_direction
        self._timer_move.start()

    def dead(self):
        self._timer_move.stop()
        self._pos.moveTo(p.CELL_SIZE, p.CELL_SIZE)
        self.img = self._main_img
        self._index = 0
        self.lives -= 1
        self._signal_update_img.emit(self.img, self._pos)
        self.signal_lives.emit(self.lives)
        
    def bounce(self):
        self._index = 0
        self._timer_move.stop()
        self._pos.moveTo(
            self.x() + self.x_direction * self.col(),
            self.y() + self.y_direction * self.row()
        )
        self.img = self._main_img
        self._signal_update_img.emit(self.img, self._pos)


from typing import Literal
import parametros as p
from PyQt5.QtCore import (
    pyqtSignal, QRect, QObject, QTimer,
)
from PyQt5.QtGui import QPixmap
from os.path import isfile

class Entity(QObject):

    _signal_update_img = pyqtSignal(QPixmap, QRect)
    _signal_delete_img = pyqtSignal()
    signal_current_pos = pyqtSignal(QObject)

    def __init__(self, 
            entity_posititon: tuple[int, int], 
            entity_main_img_src: str = None,
            speed: float = 0,
            *args, **kwargs
        ) -> None:
        super().__init__(*args, **kwargs)
        self._pos = QRect(
            entity_posititon[0]*p.CELL_SIZE, entity_posititon[1]*p.CELL_SIZE,
            p.CELL_SIZE-2, p.CELL_SIZE-2
        )
        self._sprites: dict[int | tuple[int, int], list[str]] = None
        if entity_main_img_src is not None and isfile(entity_main_img_src):
            self._main_img = entity_main_img_src
            self.img = self._main_img
        self._steps = [9, 8, 8, 9]
        self._timer_move = QTimer()
        if speed == 0:
            timer_interval = int(p.REFRESH_RATE * 1000)
        else:
            timer_interval = int(speed * 1000 / 4)
        self._timer_move.setInterval(timer_interval)
        self._timer_move.timeout.connect(self.move)
        self._index = 0
    
    def connect_signal(self, img: Literal['Image']):
        self._signal_update_img.connect(img.set_img)
        self._signal_update_img.emit(self._img, self._pos)
        self._signal_delete_img.connect(img.delete)

    def move(self) -> None:
        self.img = self.get_next_img_src()
        self._pos.moveTo(
            self.x() + self.x_direction * self._steps[self._index],
            self.y() + self.y_direction * self._steps[self._index]
        )
        self.signal_current_pos.emit(self)
        self._signal_update_img.emit(self._img, self._pos)

    def delete(self):
        self._signal_delete_img.emit()
        self.deleteLater()

    def collision(self, other: QRect):
        return self._pos.intersects(other)

    def __repr__(self) -> str:
        return f'{type(self).__name__}({self.x()}, {self.y()})'

    def get_next_img_src(self) -> str:
        raise NotImplementedError

    def x(self):
        return self._pos.x()
    
    def y(self):
        return self._pos.y()
        
    def col(self):
        return self.x()//p.CELL_SIZE
    
    def row(self):
        return self.y()//p.CELL_SIZE

    @property
    def img(self):
        return self._img
    
    @img.setter
    def img(self, img_src: str):
        if not isfile(img_src):
            raise FileNotFoundError(f'{img_src} not found')
        self._img = QPixmap(img_src)

    @property
    def sprites(self):
        return self._sprites
    
    @sprites.setter
    def sprites(self, sprite_dict: dict[int | tuple[int, int], list[str]]):
        for key, sprite_list in sprite_dict.items():
            for sprite in sprite_list:
                if not isfile(sprite):
                    raise FileNotFoundError(f'{sprite} not found')
        self._sprites = sprite_dict

    def __repr__(self) -> str:
        return f'{type(self).__name__}({self.x()}, {self.y()})'
    
    # def bounce(self):
    #     self._pos.moveTo(
    #         self.x() + self.x_direction * self._steps[self._index],
    #         self.y() + self.y_direction * self._steps[self._index]
    #     )


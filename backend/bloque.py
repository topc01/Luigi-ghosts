from PyQt5.QtCore import QObject, pyqtSignal, QRect
from PyQt5.QtGui import QPixmap
import parametros as p

class Bloque(QObject):

    _signal_set_img = pyqtSignal(QPixmap, QRect)

    def __init__(self, block_position: tuple[int, int], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._pos = QRect(
            block_position[0]*p.CELL_SIZE, block_position[1]*p.CELL_SIZE,
            p.CELL_SIZE, p.CELL_SIZE
        )
        self._img = None

    def connect_signal(self, img):
        self._signal_set_img.connect(img.set_img)
        self._signal_set_img.emit(self._img, self._pos)

    def x(self):
        return self._pos.x()
    
    def y(self):
        return self._pos.y()
    
    def col(self):
        return self.x()//p.CELL_SIZE
    
    def row(self):
        return self.y()//p.CELL_SIZE
    
    def __repr__(self) -> str:
        return f'{type(self).__name__}({self.x()}, {self.y()})'
class Wall(Bloque):
    def __init__(self, wall_position: tuple[int, int], *args, **kwargs):
        super().__init__(block_position=wall_position, *args, **kwargs)
        self._img = QPixmap(p.WALL_SPRITE)
    
class Fire(Bloque):
    def __init__(self, fire_position: tuple[int, int], *args, **kwargs):
        super().__init__(block_position=fire_position, *args, **kwargs)
        self._img = QPixmap(p.FIRE_SPRITE)

class Star(Bloque):
    def __init__(self, star_position: tuple[int, int], *args, **kwargs):
        super().__init__(block_position=star_position, *args, **kwargs)
        self._img = QPixmap(p.STAR_SPRITE)

class Rock(Bloque):
    def __init__(self, rock_position: tuple[int, int], *args, **kwargs):
        super().__init__(block_position=rock_position, *args, **kwargs)
        self._img = QPixmap(p.ROCK_SPRITE)

    def move(self, x, y):
        self._pos.moveTo(x*p.CELL_SIZE, y*p.CELL_SIZE)
        self._signal_set_img.emit(self._img, self._pos)
        #new_x = self.x() + x*p.CELL_SIZE
        #new_y = self.y() + y*p.CELL_SIZE
        #if p.CELL_SIZE <= new_x < p.CELL_SIZE*(p.ANCHO_GRILLA-1) and p.CELL_SIZE <= new_y < p.CELL_SIZE*(p.LARGO_GRILLA-1):
            #self._pos.moveTo(new_x, new_y)
            #self._signal_set_img.emit(self._img, self._pos)


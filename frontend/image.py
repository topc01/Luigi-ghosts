from PyQt5.QtWidgets import QLabel
from typing import Literal
import parametros as p

class Image(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def set_img(self, pixmap_img: Literal['QPixmap'], pos: Literal['QRect']) -> None:
        self.move(pos.x(), pos.y())
        self.setPixmap(pixmap_img)
        self.setScaledContents(True)
        self.setFixedSize(p.CELL_SIZE, p.CELL_SIZE)
        self.show()
    
    def delete(self):
        self.deleteLater()
        
    @property
    def x(self):
        return self.geometry().x()
    
    @property
    def y(self):
        return self.geometry().y()

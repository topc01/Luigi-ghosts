# if __name__ == '__main__':
#     import sys
#     from os.path import dirname, abspath
#     sys.path.append(dirname(dirname(abspath(__file__))))
from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QMimeData, pyqtSignal
from PyQt5.QtGui import QDrag, QMouseEvent, QPixmap
import parametros as p
from PyQt5.QtWidgets import QLabel, QFrame, QWidget, QApplication
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from os.path import join, isfile
# from utils import show_grab_cursor
# import utils

class Celda(QLabel):

    signal_send_type_pos = pyqtSignal(str, tuple)
    """clase Celda

    Attributes:
    -----------
    row : int
        fila de la celda
    col : int
        columna de la celda
    

    Methods:
    --------
    initUI_celda(row: int, col: int) -> None:
        inicializa la interfaz de la celda
    init() -> None:
        Método abstracto
        Las clases hijas la implementan para inicializar sus propios atributos
    """
    route_img = None # Ruta de la imagen de la celda

    def __init__(self, row, col, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.row = row
        self.col = col
        self.initUI_celda(row, col)
        self.init()
        self.show()
        self.blocked = False
        # self.texto = f'celda en {row}, {col}'

    def initUI_celda(self, row, col):
        self.setObjectName(f'{row}-{col}')
        self.setFixedSize(p.CELL_SIZE, p.CELL_SIZE)
        # self.setContentsMargins(1, 1, 1, 1)
        self.setLineWidth(1)
        self.setMidLineWidth(0)
        self.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.setStyleSheet(
            'background-color: rgb(45, 44, 44);'
            'border-color: rgb(15, 15, 15);'
        )
        if self.route_img is not None:
            self.setPixmap(QPixmap(self.route_img))
        self.setScaledContents(True)
    
    def init(self):
        self.setAcceptDrops(True)
    
    def dragEnterEvent(self, event) -> None:
        if self.blocked:
            return
        event.accept()
        widget: Item = event.source()
        img = QPixmap(widget.img_src)
        # img.setOpacity(0.5)
        # img.fill(Qt.WA_TranslucentBackground)
        self.setPixmap(img)
        
        # cambiar la opacidad de la imagen
        # self.setWindowOpacity(0.2)
        
    def dragLeaveEvent(self, event) -> None:
        event.accept()
        self.clear()

    def dropEvent(self, event) -> None:
        if self.blocked:
            return
        event.accept()
        widget: Item = event.source()
        self.setPixmap(QPixmap(widget.img_src))
        self.blocked = True
        self.signal_send_type_pos.emit(widget.type, (self.col, self.row))
        # QApplication.restoreOverrideCursor()
        # lo de la posicion
class Borde(Celda):
    route_img = join(p.PATH, 'sprites', 'Elementos', 'bordermap.png')
    def init(self):
        self.setLineWidth(0)
        self.setScaledContents(True)
        self.blocked = True
        self.type = 'Borde'

class Item(QLabel):
    def __init__(self, item_type: str, img_src: str = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = item_type
        if not isfile(img_src):
            raise FileNotFoundError(f'No se encontró la imagen {img_src}')
        self.img_src = img_src
        self.initUI()

    def initUI(self):
        self.img = QLabel(self)
        self.img.setFixedSize(32, 32)
        self.img.setPixmap(QPixmap(self.img_src))
        self.img.setScaledContents(True)
        self.img.setAlignment(Qt.AlignCenter)
        self.img.move(50, 0)
        self.setAlignment(Qt.AlignCenter)
        self.setFixedHeight(40)
        self.enable()
        # self.setFrameStyle(QFrame.Panel | QFrame.Raised)
        self.setStyleSheet("""
            background-color: rgb(45, 44, 44);
            border-color: rgb(15, 15, 15);
        """)
        self.setAlignment(Qt.AlignCenter)
    
    # @show_grab_cursor
    # def drag(self):
    #     drag = QDrag(self)
    #     mime = QMimeData()
    #     drag.setMimeData(mime)
    #     drag.exec(Qt.MoveAction)
    
    def mouseMoveEvent(self, ev: QMouseEvent) -> None:
        # QApplication.setOverrideCursor(Qt.ClosedHandCursor)
        if ev.buttons() == Qt.LeftButton:
            # QApplication.setOverrideCursor(Qt.ClosedHandCursor)
            drag = QDrag(self)
            mime = QMimeData()
            # drag.setDragCursor(QPixmap(self.img_src), Qt.MoveAction)
            drag.setMimeData(mime)
            drag.exec(Qt.MoveAction)
            

            # pixmap = QPixmap(self.size())
            # # pixmap = QPixmap(32, 32)
            # # pixmap = QPixmap(self.img_src)
            # self.render(pixmap)
            # drag.setPixmap(pixmap)
    
    def enable(self):
        self.setEnabled(True)
        self.setFrameStyle(QFrame.Panel | QFrame.Raised)

    def disable(self):
        self.setEnabled(False)
        self.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        
















# class Bloque(Celda):
#     def init(self):
#         self.setLineWidth(0)
#         self.setScaledContents(True)
#         self.blocked = True

# class Borde(Bloque):
#     route_img = join(p.PATH, 'sprites', 'Elementos', 'bordermap.png')

# class Wall(Bloque):
#     route_img = join(p.PATH, 'sprites', 'Elementos', 'wall.png')

# class Rock(Celda):
#     route_img = join(p.PATH, 'sprites', 'Elementos', 'rock.png')

#     def init(self):
#         self.blocked = True
#         self.movable = True

# class Fire(Celda):
#     route_img = join(p.PATH, 'sprites', 'Elementos', 'fire.png')

#     def init(self):
#         self.damage = True

# class Star(Celda):
#     route_img = join(p.PATH, 'sprites', 'Elementos', 'osstar.png')



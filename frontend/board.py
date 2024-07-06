from PyQt5.QtWidgets import QWidget, QGridLayout, QFrame
from frontend.elements import Celda, Borde
import parametros as p

class Board(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.rows = p.LARGO_GRILLA
        self.cols = p.ANCHO_GRILLA
       
        self.initUI()
    
    def initUI(self):
        self.setAcceptDrops(True)
        self.grid = QGridLayout()
        self.grid.setSpacing(0)
        self.grid.setContentsMargins(0, 0, 0, 0)

        for row in range(self.rows):
            for col in range(self.cols):
                if row == 0 or row == self.rows - 1 or col == 0 or col == self.cols - 1:
                    celda = Borde(row, col)
                else:
                    celda = Celda(row, col)
                    
                self.grid.addWidget(celda, row, col)
        inicial = Celda(1, 1)
        inicial.setStyleSheet(
            'background-color: rgb(0, 0, 0);'
        )
        inicial.setFrameStyle(QFrame.Panel | QFrame.Raised)
        old = self.grid.itemAtPosition(1, 1)
        self.grid.removeWidget(old.widget())
        self.grid.addWidget(inicial, 1, 1)
        self.setLayout(self.grid)
        self.setFixedSize(p.ANCHO_GRILLA*p.CELL_SIZE, p.LARGO_GRILLA*p.CELL_SIZE)
    


        

    
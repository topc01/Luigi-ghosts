from PyQt5.QtWidgets import (
    QMainWindow, QLabel, QWidget, QLineEdit, 
    QVBoxLayout, QComboBox, QPushButton
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSignal, Qt
import parametros as p
from os.path import join
from os import listdir

class StartUpWindow(QMainWindow):

    signal_validate_name = pyqtSignal(str)
    signal_game = pyqtSignal(str)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.route_logo = join(p.PATH, 'sprites', 'Elementos', 'logo.png')
        self.route_img = join(p.PATH, 'sprites', 'Fondos', 'fondo_inicio.png')

        self.initUI()
        self.show()

    def initUI(self):
        self.main = QWidget(parent=self)

        vbox = QVBoxLayout()

        image = QLabel(parent=self.main)
        image.setPixmap(QPixmap(self.route_img))
        image.setAlignment(Qt.AlignCenter)

        logo = QLabel(parent=image)
        logo.setPixmap(QPixmap(self.route_logo))
        logo.setAlignment(Qt.AlignCenter)

        mapas = list(filter(lambda x: x.endswith('.txt'), listdir(join(p.PATH, 'mapas'))))
        mapas = list(map(lambda x: x[:-4], mapas))
        self.maps_combo = QComboBox()
        self.maps_combo.addItem('Modo constructor')
        self.maps_combo.addItems(mapas)

        self.name_imput = QLineEdit('')
        self.name_imput.setPlaceholderText('Ingrese su nombre')

        play_button = QPushButton('Jugar')
        play_button.clicked.connect(self.validate_name)
        play_button.setDefault(True)

        exit_button = QPushButton('Salir')
        exit_button.clicked.connect(self.close)

        vbox.addWidget(image)
        vbox.addWidget(self.name_imput)
        vbox.addWidget(self.maps_combo)
        vbox.addWidget(play_button)
        vbox.addWidget(exit_button)

        
        self.main.setLayout(vbox)
        self.setCentralWidget(self.main)
        self.move(500, 100)
        self.setFixedSize(self.sizeHint())
    
    def keyPressEvent(self, event) -> None:
        if event.key() == Qt.Key_Return:
            self.validate_name()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def validate_name(self):
        self.signal_validate_name.emit(self.name_imput.text())

    def open_game_window(self):
        map_name = self.maps_combo.currentText()
        self.signal_game.emit(map_name)
        self.close()
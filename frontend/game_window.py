from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, 
    QVBoxLayout, QComboBox, QPushButton, QSpacerItem, 
    QSizePolicy, QLabel, QStackedLayout, QMessageBox,
    QShortcut
)
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import pyqtSignal, Qt, QUrl
from PyQt5.QtMultimedia import QSoundEffect
from frontend.board import Board
from frontend.image import Image
from frontend.elements import Item, Celda
import parametros as p

""" 
TODO: MODO CONSTRUCTOR
-> la cantidad de elementos
-> que no se pueda empezar sin luigi ni estrella

TODO: si se acaba el tiempo se bloquea el boton pero el shortcut sigue funcionando
-> hacer que se pare el juego globalmente
"""
class GameWindow(QMainWindow):

    signal_send_type = pyqtSignal(str, tuple)
    signal_direction = pyqtSignal(tuple)
    signal_send_image = pyqtSignal(Image)
    signal_switch_game_state = pyqtSignal()
    signal_delete_villains = pyqtSignal()
    signal_freeze = pyqtSignal()

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.remaining_time = p.TIEMPO_CUENTA_REGRESIVA
        self.initUI()
        # self._play_mode = False
        self.images = []
        self.create_shortcuts()
        self.create_sounds()
        self.connect_cell_signal()
        self.set_amounts()
        self.items_added: list[tuple[str, tuple[int, int]]] = []

        
    def initUI(self):
        
        self.main = QWidget(parent=self)

        hbox = QHBoxLayout(self.main)

        self.left_side = QWidget(parent=self.main)
        vbox = QVBoxLayout()
        
        self.stacked_layout = QStackedLayout()
        widget_construction_mode = self.create_widget_construction_mode()
        widget_game_mode = self.create_widget_game_mode()
        self.stacked_layout.addWidget(widget_construction_mode)
        self.stacked_layout.addWidget(widget_game_mode)
        vbox.addLayout(self.stacked_layout)
        
        spacer_item = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        vbox.addItem(spacer_item)

        buttons = self.create_widget_buttons()
        vbox.addLayout(buttons)

        self.left_side.setLayout(vbox)
        
        hbox.addWidget(self.left_side)
        hbox.addStretch(10)
        
        self.board = Board(parent=self.main)
        hbox.addWidget(self.board)

        self.main.setLayout(hbox)
        self.main.setMinimumSize(self.main.sizeHint())
        # self.left_side.setFixedHeight(self.main.height())
        self.setCentralWidget(self.main)

    def create_widget_construction_mode(self):
        modo_constructor = QWidget()
        constructor_vbox = QVBoxLayout()
        filter_combo = QComboBox()
        filter_combo.addItems([
            'Todos',
            'Bloques',
            'Entidades'
        ])
        self.items = {
            'L': Item(item_type='L', img_src=p.LUIGI_SPRITE),
            'S': Item(item_type='S', img_src=p.STAR_SPRITE),
            'P': Item(item_type='P', img_src=p.WALL_SPRITE),
            'F': Item(item_type='F', img_src=p.FIRE_SPRITE),
            'R': Item(item_type='R', img_src=p.ROCK_SPRITE),
            'V': Item(item_type='V', img_src=p.RED_GHOST_DOWN_SPRITES[0]),
            'H': Item(item_type='H', img_src=p.WHITE_GHOST_RIGTH_SPRITES[0])
        }
        constructor_vbox.addWidget(filter_combo)
        for item in self.items.values():
            constructor_vbox.addWidget(item)
        constructor_vbox.setSpacing(0)
        modo_constructor.setLayout(constructor_vbox)
        return modo_constructor

    def create_widget_game_mode(self):
        modo_juego = QWidget()
        juego_vbox = QVBoxLayout()

        tiempo_hbox = QHBoxLayout()
        tiempo = QLabel('Tiempo')
        self.tiempo_restante = QLabel(str(self.remaining_time))
        tiempo_hbox.addWidget(tiempo)
        tiempo_hbox.addWidget(self.tiempo_restante)

        vida_hbox = QHBoxLayout()
        vidas = QLabel('Vidas')
        self.vidas_restantes = QLabel(str(p.CANTIDAD_VIDAS))
        vida_hbox.addWidget(vidas)
        vida_hbox.addWidget(self.vidas_restantes)
        self.button = QPushButton('Pausar')
        self.button.clicked.connect(self.switch_game_state)
        juego_vbox.addLayout(tiempo_hbox)
        juego_vbox.addLayout(vida_hbox)
        juego_vbox.addWidget(self.button)
        juego_vbox.setSpacing(0)
        modo_juego.setLayout(juego_vbox)
        return modo_juego
    
    def create_widget_buttons(self):
        hbox_buttons = QHBoxLayout()
        self.clean = QPushButton('Limpiar')
        self.clean.clicked.connect(self.clear_items_added)
        self.play = QPushButton('Jugar')
        self.play.clicked.connect(self.play_mode)
        hbox_buttons.addWidget(self.clean)
        hbox_buttons.addWidget(self.play)
        return hbox_buttons
    
    def create_shortcuts(self):
        self.delete_villains = QShortcut(QKeySequence("K, I, L"), self)
        self.delete_villains.activated.connect(self.send)
        # self.delete_villains.activated.connect(self.signal_delete_villains.emit)
        self.freeze = QShortcut(QKeySequence("I, N, F"), self)
        self.freeze.activated.connect(self.signal_freeze.emit)
        self.switch_game_state_key = QShortcut("P", self)
        self.switch_game_state_key.activated.connect(self.switch_game_state)

    def create_sounds(self):
        self.sound_victory = QSoundEffect()
        self.sound_victory.setSource(QUrl.fromLocalFile(p.VICTORY_SOUND))
        self.sound_victory.setVolume(0.5)
        self.sound_game_over = QSoundEffect()
        self.sound_game_over.setSource(QUrl.fromLocalFile(p.GAME_OVER_SOUND))
        self.sound_game_over.setVolume(0.5)

    def send(self):
        # print('eliminando villanos desde el frontend')
        self.signal_delete_villains.emit()

    def play_mode(self):
        # self._play_mode = True
        self.send_items()
        self.clear_items_added()

        self.board.setAcceptDrops(False)
        self.stacked_layout.setCurrentIndex(1)
        self.clean.setEnabled(False)
        self.play.setEnabled(False)
        self.signal_switch_game_state.emit()

    def switch_game_state(self):
        self.signal_switch_game_state.emit()
        if self.button.text() == 'Continuar':
            self.button.setText('Pausar')
        else:
            self.button.setText('Continuar')

    def victory(self):
        self.sound_victory.play()
        self.signal_switch_game_state.emit()
        self.button.setEnabled(False)
        alert = QMessageBox()
        alert.setWindowTitle('Victoria')
        alert.setText('Ganaste!')
        alert.exec()
        self.close()

    def game_over(self):
        self.sound_game_over.play()
        self.signal_switch_game_state.emit()
        self.button.setEnabled(False)
        alert = QMessageBox()
        alert.setWindowTitle('Fin del juego')
        alert.setText('Juego terminado')
        alert.exec()
        self.close()
        
    def update_timer(self):
        self.remaining_time -= 1
        self.tiempo_restante.setText(str(self.remaining_time))
        if self.remaining_time == 0:
            self.game_over()

    def update_lives(self, lives):
        self.vidas_restantes.setText(str(lives))
        if lives == 0:
            self.game_over()

    def add_img(self):
        self.images.append(Image(self.board))
        self.signal_send_image.emit(self.images[-1])

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
        direction = p.DIRECTIONS.get(event.key())
        if direction is not None:
            self.signal_direction.emit(direction)

    def connect_cell_signal(self):
        for i in range(1, self.board.rows-1):
            for j in range(1, self.board.cols-1):
                cell: Celda = self.board.grid.itemAtPosition(i, j).widget()
                # print(cell.texto)
                cell.signal_send_type_pos.connect(self.recieve_item)
                # .signal_send_image.connect(self.signal_send_image.emit)

    def recieve_item(self, item_type: str, pos: tuple[int, int]):
        self.items_added.append((item_type, pos))
        self.amounts[item_type] -= 1
        if self.amounts[item_type] == 0:
            self.items[item_type].disable()
            pass

    def clear_items_added(self):
        self.items_added = []
        for i in range(1, self.board.rows-1):
            for j in range(1, self.board.cols-1):
                cell: Celda = self.board.grid.itemAtPosition(i, j).widget()
                cell.clear()
                cell.blocked = False
        for item in self.items.values():
            item.enable()
        self.set_amounts()

    def send_items(self):
        print('enviando items')
        for item_type, pos in self.items_added:
            print(item_type, pos)
            self.signal_send_type.emit(item_type, pos)

    def set_amounts(self):
        self.amounts = {
            'L': 1,
            'P': p.MAXIMO_PARED,
            'R': p.MAXIMO_ROCA,
            'F': p.MAXIMO_FUEGO,
            'V': p.MAXIMO_FANTASMAS_VERTICAL,
            'H': p.MAXIMO_FANTASMAS_HORIZONTAL,
            'S': 1
        }
        # self.luigis_left = 1
        # self.walls_left = p.MAXIMO_PARED
        # self.rocks_left = p.MAXIMO_ROCA
        # self.fires_left = p.MAXIMO_FUEGO
        # self.red_ghosts_left = p.MAXIMO_FANTASMAS_VERTICAL
        # self.white_ghosts_left = p.MAXIMO_FANTASMAS_HORIZONTAL
    # def clear_board(self):

        
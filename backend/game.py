from PyQt5.QtCore import QObject, pyqtSignal, QTimer
from backend.luigi import Luigi
from backend.ghost import RedGhost, WhiteGhost
from backend.bloque import Wall, Fire, Star, Rock
from typing import Literal
import parametros as p
import utils
""" 

TODO: verificar las posiciones
TODO: verificar que no se pueda mover a traves de los bloques
TODO: pausar la partida bien
"""
class Game(QObject):

    signal_open_window = pyqtSignal()
    signal_request_image = pyqtSignal()
    signal_update_timer = pyqtSignal()
    signal_update_lives = pyqtSignal(int)
    signal_victory = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.timer = QTimer()
        self.timer.timeout.connect(self.signal_update_timer.emit)
        self.cols = p.ANCHO_GRILLA
        self.rows = p.LARGO_GRILLA
        self._play = False
        self._img = None
        self._luigi = None
        self._star = None
        self.items = []
        # self._items = {}

    def move_luigi(self, direction: tuple[int, int]):
        if self.luigi is None:
            return
        if self.luigi._index != 0:
            return
        if direction == p.GET_STAR:
            if self.luigi._pos.intersects(self.star._pos):
                self.signal_victory.emit()
                return
        pos_x, pos_y = self.luigi.col(), self.luigi.row()
        new_x, new_y = pos_x + direction[0], pos_y + direction[1]
        item_pos = self.get_item_at_pos(new_x, new_y)
        if isinstance(item_pos, Wall) or new_x in (0, self.cols-1) or new_y in (0, self.rows-1):
            return
        if self.blocked_rock((pos_x, pos_y), direction):
            return
        self.luigi.move_to(move_direction=direction)
        if isinstance(item_pos, Fire):
            self.luigi.dead()

    def load_map(self, map_name: str):
        if map_name == 'Modo constructor':
            return
        map_ = utils.load_map(map_name)
        if map_ is None: # si el mapa no se encontro
            raise FileNotFoundError('Mapa no encontrado')
        for i, row in enumerate(map_):
            for j, element in enumerate(row):
                if element == '-':
                    continue
                pos = (j+1, i+1)
                self.add_item(element, pos)
                
    def add_item(self, item_type: str, pos: tuple[int, int]):
        print('adding items from backend')
        if item_type == 'L':
            self.luigi = Luigi(pos)
        elif item_type ==  'S':
            self.star = Star(pos)
        elif item_type == 'P':
            self.items.append(Wall(pos))
        elif item_type == 'F':
            self.items.append(Fire(pos))
        elif item_type == 'H':
            self.items.append(WhiteGhost(pos))
        elif item_type == 'V':
            self.items.append(RedGhost(pos))
        elif item_type == 'R':
            self.items.append(Rock(pos))
        else:
            raise ValueError(f'Elemento {item_type} no reconocido')
        self.connect_img()

    def init_game(self, map_name: str):
        print('>>>>>>>> iniciando juego')
        self.load_map(map_name)
        self.connect_img()
        self.signal_open_window.emit()
        self.print_items()
    
    def switch_game_state(self):
        self._play = not self._play
        if self._play:
            func = lambda ghost: ghost.start()
            self.timer.start(1000)
        else:
            func = lambda ghost: ghost.stop()
            self.timer.stop()
        for item in self.items:
            if isinstance(item, (RedGhost, WhiteGhost)):
                func(item)
       
    def accept_img(self, img: Literal['Image']):
        self._img = img

    def recieve_img(self):
        self.signal_request_image.emit()
        img = self._img
        if img is None:
            raise ValueError('No se ha recibido imagen')
        self._img = None
        return img

    def connect_img(self):
        # print('intentando conectar imagenes')
        for item in self.items:
            item: Wall | Fire | RedGhost | WhiteGhost | Rock | Star
            item_img = self.recieve_img()
            item.connect_signal(item_img)
            if isinstance(item, (RedGhost, WhiteGhost)):
                item.signal_current_pos.connect(self.check_pos)
                # item.signal_luigi_killed.connect(self.luigi_killed)

        if self.star is not None:
            # print('conectando estrella')
            star = self.recieve_img()
            self.star.connect_signal(star)

        if self.luigi is not None:
            # print('conectando luigi')
            luigi_img = self.recieve_img()
            self.luigi.connect_signal(luigi_img)
            self.luigi.signal_current_pos.connect(self.check_pos)

    def check_pos(self, entity: Luigi | RedGhost | WhiteGhost):
        # entity_position = entity._pos
        # positions = self._items.keys()
        # items = self._items.values()
        for item in self.items:
            # item = self._items.get(pos)
            if item is None:
                continue
            if entity.collision(item._pos):
                if isinstance(item, Fire):
                    entity.dead()
                elif isinstance(entity, (RedGhost, WhiteGhost)) and isinstance(item, (Wall, Rock)):
                    entity.bounce()
                elif isinstance(entity, Luigi) and isinstance(item, Rock):
                    item_x, item_y = item.col(), item.row()
                    new_x = item_x + entity.x_direction
                    new_y = item_y + entity.y_direction
                    if 1 <= new_x < p.ANCHO_GRILLA-2 and 1 <= new_y < p.LARGO_GRILLA:
                        item.move(new_x, new_y)
                        # self._items[(new_x, new_y)] = item
                        # self._items[pos] = None

        if not (1 <= entity.col() < self.cols-2) or not (1 <= entity.row() < self.rows-2):
            entity.bounce()
        if isinstance(entity, (RedGhost, WhiteGhost)) and entity.collision(self.luigi._pos) and not (self.luigi.col() == 1 and self.luigi.row() == 1):
            self.luigi.dead()

    def delete_villains(self):
        deleted = []
        for item in self.items:
            # item = self._items[key]
            if isinstance(item, (RedGhost, WhiteGhost)):
                try:
                    item.delete()
                except RuntimeError:
                    print('Fantasma ya eliminado')
                deleted.append(item)
        for item in deleted:
            del item

    def freeze(self):
        self.timer.stop()

    def manage_lives(self, lives: int):
        if lives == 0:
            self.freeze()
            self.delete_villains()
        self.signal_update_lives.emit(lives)

    @property
    def luigi(self):
        return self._luigi
    
    @luigi.setter
    def luigi(self, value):
        if not isinstance(value, Luigi):
            raise TypeError('luigi debe ser instancia de Luigi')
        value.signal_current_pos.connect(self.check_pos)
        value.signal_lives.connect(self.manage_lives)
        self._luigi = value    

    @property
    def star(self):
        return self._star
    
    @star.setter
    def star(self, value):
        if not isinstance(value, Star):
            raise TypeError('star debe ser instancia de Star')
        self._star = value
    
    def print_items(self):
        for item in self.items:
            print(item)
        print(self.luigi)
        print(self.star)
        
    def blocked_rock(self, item_pos, move_direction):
        new_x, new_y = item_pos[0] + move_direction[0], item_pos[0] + move_direction[0]
        next_item = self.get_item_at_pos(new_x, new_y)
        if next_item is None:
            return
        if not isinstance(next_item, Rock):
            return
        return not (1 <= new_x + move_direction[0] < self.cols-2 and 1 <= new_y + move_direction[1] < self.rows-2)
    
    def get_item_at_pos(self, x, y):
        for item in self.items:
            item: Wall | Fire | RedGhost | WhiteGhost | Rock | Star
            if item.col() == x and item.row() == y:
                return item
        return None
        
        
        
        
        
        
        
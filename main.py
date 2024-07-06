import sys
from PyQt5.QtWidgets import QApplication
from frontend.start_up_window import StartUpWindow
from frontend.game_window import GameWindow
from backend.start_up import StartUpBackend
from backend.game import Game

class App(QApplication):
    def __init__(self, argv: list[str]=[]) -> None:
        super().__init__(argv)

        def hook(type, value, traceback):
            print(type)
            print(traceback)
        sys.__excepthook__ = hook

        self.init_frontend()
        self.init_backend()
        self.connect()
    
    def init_frontend(self):
        self.start_up_window = StartUpWindow()
        self.window_game = GameWindow()
        
    def init_backend(self):
        self.start_up_backend = StartUpBackend()
        self.game = Game()

    def connect(self):

        # la ventana de inicio recibe un nombre y lo manda al backend para validarlo
        self.start_up_window.signal_validate_name.connect(self.start_up_backend.validate_name)

        # el backend manda una señal a la ventana de inicio para que abra la ventana de juego
        self.start_up_backend.signal_start_game.connect(self.start_up_window.open_game_window)

        self.window_game.signal_send_type.connect(self.game.add_item)
        # la ventana de inicio manda una señal con el nombre del mapa para iniciar el juego
        self.start_up_window.signal_game.connect(self.game.init_game)

        # el backend del juego le pide una nueva imagen al frontend
        self.game.signal_request_image.connect(self.window_game.add_img)

        # el frontend del juego manda una imagen al backend
        self.window_game.signal_send_image.connect(self.game.accept_img)

        # el backend manda una señal a la ventana de juego para que se muestre
        self.game.signal_open_window.connect(self.window_game.show)

        # la ventana de juego manda una señal con la tecla presionada para mover a luigi
        self.window_game.signal_direction.connect(self.game.move_luigi)

        # la ventana de juego manda una señal para pausar o reanudar el juego
        self.window_game.signal_switch_game_state.connect(self.game.switch_game_state)

        # el juego manda una señal para actualizar el timer
        self.game.signal_update_timer.connect(self.window_game.update_timer)

        self.game.signal_update_lives.connect(self.window_game.update_lives)
        # la ventana manda una señal para eliminar a los enemigos
        self.window_game.signal_delete_villains.connect(self.game.delete_villains)

        # la ventana manda una señal para congelar el tiempo
        self.window_game.signal_freeze.connect(self.game.freeze)

        self.game.signal_victory.connect(self.window_game.victory)
        
    def run(self):
        sys.exit(self.exec())

if __name__ == '__main__':
    app = App()
    app.run()
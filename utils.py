# utils.py
import parametros as p
from os.path import join, isfile
from decorator import decorator
from PyQt5.QtWidgets import QApplication as app
from PyQt5.QtCore import Qt

def inside(min_max: tuple[int, int], value: int) -> int:
    """Si el valor esta fuera del intervalo, devuelve el 
    maximo o el minimo, dependiendo el caso
    """
    return max(min(value, min_max[1]), min_max[0])

def load_map(map_name: str):
    route_file = join(p.PATH, 'mapas', map_name+'.txt')
    if not isfile(route_file):
        return None
    with open(route_file, 'r') as file:
        map_ = file.readlines()
    map_ = [list(line.strip()) for line in map_]
    return map_

@decorator
def show_grab_cursor(func, *args, **kwargs):
    app.setOverrideCursor(Qt.ClosedHandCursor)
    try:
        return func(*args, **kwargs)
    finally:
        app.restoreOverrideCursor()

def error_msg(name: str):
    if name == '':
        return 'El nombre no puede estar vacio.'
    elif len(name) < p.MIN_CARACTERES:
        return f'El nombre "{name}" tiene {len(name)} caracter{"es" if len(name) > 1 else ""}.\nDebe tener al menos {p.MIN_CARACTERES}.'
    elif len(name) > p.MAX_CARACTERES:
        return f'El nombre "{name}" tiene {len(name)} caracteres.\nDebe tener como maximo {p.MAX_CARACTERES}.'
    elif not name.isalnum():
        return f'El nombre "{name}" tiene caracteres no permitidos.\nDebe ser alfanumerico.'

        
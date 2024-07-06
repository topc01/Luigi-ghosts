# Tarea 2: DCCazafantasmas 👻🧱🔥


Un buen ```README.md``` puede marcar una gran diferencia en la facilidad con la que corregimos una tarea, y consecuentemente cómo funciona su programa, por lo en general, entre más ordenado y limpio sea éste, mejor será 

Para nuestra suerte, GitHub soporta el formato [MarkDown](https://es.wikipedia.org/wiki/Markdown), el cual permite utilizar una amplia variedad de estilos de texto, tanto para resaltar cosas importantes como para separar ideas o poner código de manera ordenada ([pueden ver casi todas las funcionalidades que incluye aquí](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet))

Un buen ```README.md``` no tiene por que ser muy extenso tampoco, hay que ser **concisos** (a menos que lo consideren necesario) pero **tampoco pueden** faltar cosas. Lo importante es que sea claro y limpio 

**Dejar claro lo que NO pudieron implementar y lo que no funciona a la perfección. Esto puede sonar innecesario pero permite que el ayudante se enfoque en lo que sí podría subir su puntaje.**

## Consideraciones generales :octocat:

<Descripción de lo que hace y que **_no_** hace la tarea que entregaron junto
con detalles de último minuto y consideraciones como por ejemplo cambiar algo
en cierta línea del código o comentar una función>

### Cosas implementadas y no implementadas :white_check_mark: :x:

Explicación: mantén el emoji correspondiente, de manera honesta, para cada item. Si quieres, también puedes agregarlos a los títulos:
- ❌ si **NO** completaste lo pedido
- ✅ si completaste **correctamente** lo pedido
- 🟠 si el item está **incompleto** o tiene algunos errores

**⚠️⚠️NO BASTA CON SOLO PONER EL COLOR DE LO IMPLEMENTADO**,
SINO QUE SE DEBERÁ EXPLICAR QUÉ SE REALIZO DETALLADAMENTE EN CADA ITEM.
⚠️⚠️

#### Ventanas: 27 pts (27%)
##### ✅ Ventana de Inicio
##### ✅ Ventana de Juego
#### Mecánicas de juego: 47 pts (47%)
##### ✅ Luigi
##### ✅ Fantasmas
##### ✅ Modo Constructor
##### ✅ Fin de ronda
#### Interacción con el usuario: 14 pts (14%)
##### ❌✅🟠 Clicks
##### ✅ Animaciones
#### Funcionalidades con el teclado: 8 pts (8%)
##### ❌✅🟠 Pausa
##### ✅ K + I + L
##### ❌✅🟠 I + N + F
#### Archivos: 4 pts (4%)
##### ✅ Sprites
##### ✅ Parametros.py
#### Bonus: 8 décimas máximo
##### ❌ Volver a Jugar
##### ❌ Follower Villain
##### ✅ Drag and Drop

## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```main.py```. Además se debe crear los siguientes archivos y directorios adicionales:
1. ```sounds``` con los sonidos
2. ```sprites``` con los archivos de sprites (se asume que son los mismos nombres)
3. ```mapas``` con los mapas predeterminados


## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```sys```: ```exit()```
2. ```typing```: ```Literal``` para los type hints
3. ```PyQt5.QWidgets```: ```QApplication```, ```QMainWindow```, ...
4. ```PyQt5.QtCore```: ```pyqtSignal```, ```Qt```, ```QUrl```
5. ```PyQt5.QtGui```: ```QPixmap```, ```QKeySequence```
6. ```PyQt5.QtMultimedia```: ```QSoundEffect```

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

Backend:
1. ```entity```: Contiene a ```Entity``` clase padre de fantasma y luigi
2. ```ghost```: Hecha para <insertar descripción **breve** de lo que hace o qué contiene>
3. ```luigi```:
4. ```bloque```:
5. ```game```:
6. ```start_up```:

Frontend:
1. ```board```:
2. ```elements```:
3. ```game_window```:
4. ```image```:
5. ```start_up_window```:

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. En la posicion inicial Luigi no puede morir

PD_1: Cuando se carga un mapa predeterminado, igual pasa al modo constructor (en caso de que se quieran agregar mas elementos)
PD_2: Cuando choca con la roca se pone raro. Se mueve pero algo le pasa a la posicion.


-------



**EXTRA:** si van a explicar qué hace específicamente un método, no lo coloquen en el README mismo. Pueden hacerlo directamente comentando el método en su archivo. Por ejemplo:

```python
class Corrector:

    def __init__(self):
          pass

    # Este método coloca un 6 en las tareas que recibe
    def corregir(self, tarea):
        tarea.nota  = 6
        return tarea
```

Si quieren ser más formales, pueden usar alguna convención de documentación. Google tiene la suya, Python tiene otra y hay muchas más. La de Python es la [PEP287, conocida como reST](https://www.python.org/dev/peps/pep-0287/). Lo más básico es documentar así:

```python
def funcion(argumento):
    """
    Mi función hace X con el argumento
    """
    return argumento_modificado
```
Lo importante es que expliquen qué hace la función y que si saben que alguna parte puede quedar complicada de entender o tienen alguna función mágica usen los comentarios/documentación para que el ayudante entienda sus intenciones.

## Referencias de código externo :book:

Para realizar mi tarea saqué código de:
1. \<link de código>: este hace \<lo que hace> y está implementado en el archivo <nombre.py> en las líneas <número de líneas> y hace <explicación breve de que hace>

## Descuentos
La guía de descuentos se encuentra [link](https://github.com/IIC2233/syllabus/blob/main/Tareas/Descuentos.md).

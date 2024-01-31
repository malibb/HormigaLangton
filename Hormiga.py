# Definición de constantes para las orientaciones de las hormigas.
NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3

class Hormiga:
    """
    Clase Hormiga representa una hormiga individual en el modelo de la Hormiga de Langton.
    
    Atributos:
        x (int): Posición en el eje X (horizontal) de la hormiga.
        y (int): Posición en el eje Y (vertical) de la hormiga.
        orientacion (int): Orientación actual de la hormiga (NORTH, EAST, SOUTH, WEST).
        vida_maxima (int): Vida máxima de la hormiga.
        vida_actual (int): Vida actual de la hormiga.
    """

    def __init__(self, x, y, orientacion, vida_maxima, vida_actual=0):
        """
        Constructor de la clase Hormiga.

        Parámetros:
            x (int): Posición inicial en el eje X de la hormiga.
            y (int): Posición inicial en el eje Y de la hormiga.
            orientacion (int): Orientación inicial de la hormiga.
            vida_maxima (int): Vida máxima asignada a la hormiga.
            vida_actual (int, opcional): Vida actual de la hormiga. Por defecto es 0.
        """
        self.x = x
        self.y = y
        self.orientacion = orientacion
        self.vida_maxima = vida_maxima
        self.vida_actual = vida_actual

    def procesar_paso(self, grid):
        """
        Procesa un paso de la hormiga, cambiando su posición y orientación según las reglas del autómata.

        Parámetros:
            grid (numpy.ndarray): El grid en el que la hormiga se mueve.

        Retorna:
            tuple: Un par de diccionarios con la nueva información del grid y la hormiga.
        """
        valor_grid = None
        alto, ancho, _ = grid.shape

        # Determinar el valor de la celda actual.
        valor_celda = sum(grid[self.x, self.y])

        # Calcular el nuevo valor de la celda y cambiar el color.
        if(valor_celda == 0):
            valor_grid = {'posicion': (self.x, self.y), 'valor': [255, 255, 255]}  # Celda se vuelve blanca
        else:
            valor_grid = {'posicion': (self.x, self.y), 'valor': [0, 0, 0]}  # Celda se vuelve negra

        # Actualizar la orientación y la posición de la hormiga según las reglas del autómata.
        self.orientacion = (self.orientacion + 1) % 4 if valor_celda else (self.orientacion - 1) % 4
        if self.orientacion == NORTH:
            self.x -= 1
        elif self.orientacion == EAST:
            self.y += 1
        elif self.orientacion == SOUTH:
            self.x += 1
        elif self.orientacion == WEST:
            self.y -= 1

        # Asegurar que la hormiga se mantenga dentro de los límites del grid.
        self.x = self.x % alto
        self.y = self.y % ancho

        informacion_hormiga = {'posicion': (self.x, self.y), 'orientacion': self.orientacion}
        return valor_grid, informacion_hormiga

    def __str__(self):
        """
        Representación en string de la hormiga.

        Retorna:
            str: Una cadena de texto que representa el estado actual de la hormiga.
        """
        return f'{self.x} {self.y} {self.orientacion} {self.vida_maxima} {self.vida_actual}'

class HormigaReina(Hormiga):
    """
    Clase HormigaReina, una especialización de la clase Hormiga que añade características de reproducción.

    Atributos heredados de Hormiga:
        x, y, orientacion, vida_maxima, vida_actual

    Atributos adicionales:
        edad_reproductiva_min (int): Edad mínima a la que la hormiga reina puede empezar a reproducirse.
        edad_reproductiva_max (int): Edad máxima a la que la hormiga reina puede reproducirse.
    """

    def __init__(self, x, y, orientacion, vida_maxima, edad_reproductiva_min, edad_reproductiva_max, vida_actual=0):
        """
        Constructor de la clase HormigaReina.

        Parámetros:
            x, y, orientacion, vida_maxima, vida_actual: Ver constructor de la clase Hormiga.
            edad_reproductiva_min (int): Edad mínima reproductiva de la hormiga reina.
            edad_reproductiva_max (int): Edad máxima reproductiva de la hormiga reina.
        """
        super().__init__(x, y, orientacion, vida_maxima, vida_actual)
        self.edad_reproductiva_min = edad_reproductiva_min
        self.edad_reproductiva_max = edad_reproductiva_max

    def procesar_paso(self, grid, lista_reproductoras):
        """
        Procesa un paso de la hormiga reina, incluyendo la posibilidad de reproducción.
        
        Este método extiende la funcionalidad de 'procesar_paso' de la clase Hormiga, añadiendo la lógica para la reproducción de hormigas.

        Parámetros:
            grid (numpy.ndarray): El grid en el que la hormiga se mueve, representando el espacio del autómata.
            lista_reproductoras (list): Lista de todas las hormigas reproductoras en el grid.

        Retorna:
            tuple: Un par de diccionarios con la nueva información del grid y la hormiga, y el número de nuevas hormigas generadas.
        """
        valor_grid = None
        alto, ancho, _ = grid.shape

        # Determina el valor de la celda en la que se encuentra la hormiga.
        valor_celda = sum(grid[self.x, self.y])

        # Actualiza el valor de la celda basado en el estado actual.
        # Si la celda está vacía (0), se convierte en una celda llena (255, 255, 255).
        # Si la celda está llena, se convierte en una celda vacía (0, 0, 0).
        if valor_celda == 0:
            valor_grid = {'posicion': (self.x, self.y), 'valor': [255, 255, 255]}
        else:
            valor_grid = {'posicion': (self.x, self.y), 'valor': [0, 0, 0]}

        # Actualiza la orientación de la hormiga según las reglas del autómata:
        # Gira a la derecha si la celda está llena, gira a la izquierda si está vacía.
        self.orientacion = (self.orientacion + 1) % 4 if valor_celda else (self.orientacion - 1) % 4

        # Avanza la hormiga hacia adelante en la dirección a la que ahora apunta.
        if self.orientacion == NORTH:
            self.x -= 1
        elif self.orientacion == EAST:
            self.y += 1
        elif self.orientacion == SOUTH:
            self.x += 1
        elif self.orientacion == WEST:
            self.y -= 1

        # Asegura que la hormiga permanezca dentro de los límites del grid.
        self.x = self.x % alto
        self.y = self.y % ancho

        # Información actualizada de la hormiga.
        informacion_hormiga = {
            'posicion': (self.x, self.y),
            'orientacion': self.orientacion,
            'vida_maxima': self.vida_maxima,
            'edad_reproductiva_min': self.edad_reproductiva_min,
            'edad_reproductiva_max': self.edad_reproductiva_max
        }

        # Calcula la reproducción basada en la interacción con hormigas reproductoras.
        nuevas_hormigas = 0
        for reproductora in lista_reproductoras:
            if self.x == reproductora.x and self.y == reproductora.y:
                nuevas_hormigas += 1
                print('Nueva hormiga')

        # Aumenta la edad de la hormiga reina en cada paso.
        self.vida_actual += 1

        return valor_grid, informacion_hormiga, nuevas_hormigas

    def __str__(self):
        """
        Representación en string de la hormiga reina.

        Retorna:
            str: Una cadena de texto que representa el estado actual de la hormiga reina.
        """
        return f'{self.x} {self.y} {self.orientacion} {self.vida_maxima} {self.edad_reproductiva_min} {self.edad_reproductiva_max} {self.vida_actual}'

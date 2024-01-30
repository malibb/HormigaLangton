# Definir las orientaciones de las hormigas
NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3

class Hormiga:
    def __init__(self, x, y, orientacion, vida_maxima, vida_actual=0):
        self.x = x
        self.y = y
        self.orientacion = orientacion
        self.vida_maxima = vida_maxima
        self.vida_actual = vida_actual

    def procesar_paso(self, grid):
        valor_grid = None
        alto, ancho, _ = grid.shape

        # Determinar el valor de la celda.
        valor_celda = sum(grid[self.x, self.y])

        # Calcular el nuevo valor de la celda.
        if(valor_celda == 0):
            valor_grid = {
                            'posicion': (self.x, self.y),
                            'valor': [255, 255, 255]
                        }
        else:
            valor_grid = {
                            'posicion': (self.x, self.y),
                            'valor': [0, 0, 0]
                        }

        # Actualiza la posicion y la orientación de la hormiga
        if valor_celda:
            self.orientacion = (self.orientacion + 1) % 4  # Girar a la derecha
        else:
            self.orientacion = (self.orientacion - 1) % 4  # Girar a la izquierda

        # Move the ant forward
        if(self.orientacion == NORTH):
            self.x -= 1
        elif(self.orientacion == EAST):
            self.y += 1
        elif(self.orientacion == SOUTH):
            self.x += 1
        elif(self.orientacion == WEST):
            self.y -= 1

        self.x = self.x % alto
        self.y = self.y % ancho

        informacion_hormiga = {
            'posicion': (self.x, self.y),
            'orientacion': self.orientacion
        }

        return valor_grid, informacion_hormiga

    def __str__(self):
        return f'{self.x} {self.y} {self.orientacion} {self.vida_maxima} {self.vida_actual}'

class HormigaReina(Hormiga):
    def __init__(self, x, y, orientacion, vida_maxima, edad_reproductiva_min, edad_reproductiva_max, vida_actual=0):
        super().__init__(x, y, orientacion, vida_maxima, vida_actual)
        self.edad_reproductiva_min = edad_reproductiva_min
        self.edad_reproductiva_max = edad_reproductiva_max

    def procesar_paso(self, grid, lista_reinas, lista_reproductoras):

        valor_grid = None
        alto, ancho, _ = grid.shape

        # Determinar el valor de la celda.
        valor_celda = sum(grid[self.x, self.y])

        # Calcular el nuevo valor de la celda.
        if(valor_celda == 0):
            valor_grid = {
                            'posicion': (self.x, self.y),
                            'valor': [255, 255, 255]
                        }
        else:
            valor_grid = {
                            'posicion': (self.x, self.y),
                            'valor': [0, 0, 0]
                        }

        # Actualiza la posicion y la orientación de la hormiga
        if valor_celda:
            self.orientacion = (self.orientacion + 1) % 4  # Girar a la derecha
        else:
            self.orientacion = (self.orientacion - 1) % 4  # Girar a la izquierda

        # Move the ant forward
        if(self.orientacion == NORTH):
            self.x -= 1
        elif(self.orientacion == EAST):
            self.y += 1
        elif(self.orientacion == SOUTH):
            self.x += 1
        elif(self.orientacion == WEST):
            self.y -= 1

        self.x = self.x % alto
        self.y = self.y % ancho

        informacion_hormiga = {
            'posicion': (self.x, self.y),
            'orientacion': self.orientacion,
            'vida_maxima': self.vida_maxima,
            'edad_reproductiva_min': self.edad_reproductiva_min,
            'edad_reproductiva_max': self.edad_reproductiva_max
        }

        nuevas_hormigas = 0
        for reproductora in lista_reproductoras:
            if(self.x == reproductora.x and self.y == reproductora.y):
                nuevas_hormigas += 1
                print('Nueva hormiga')

        self.vida_actual += 1
        return valor_grid, informacion_hormiga, nuevas_hormigas

    def __str__(self):
        return f'{self.x} {self.y} {self.orientacion} {self.vida_maxima} {self.edad_reproductiva_min} {self.edad_reproductiva_max} {self.vida_actual}'

import numpy as np

class ArchivoDTO:
    def __init__(self):
        self.numero_reinas = 0
        self.numero_trabajadoras = 0
        self.numero_soldados = 0
        self.numero_reproductoras = 0
        self.reinas = []
        self.trabajadoras = []
        self.soldados = []
        self.reproductoras = []
        self.ancho = 0
        self.alto = 0
        self.grid = None
        self.generacion = 0
        self.conteo_densidades = {
            'reina': np.zeros(100000),
            'trabajadora': np.zeros(100000),
            'soldado': np.zeros(100000),
            'reproductora': np.zeros(100000)
        }

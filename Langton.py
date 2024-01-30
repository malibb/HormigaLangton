#Bibliotecas gráficos.
import pygame
import pygame.freetype
import tkinter.filedialog
import tkinter as tk
import matplotlib
import matplotlib.pyplot as plt

#Bibliotecas procesamiento.
import numpy as np
import os
import sys
import time
import random
import re

#Módulos Python.
from ArchivoDTO import ArchivoDTO
from ManejadorArchivos import ManejadorArchivos
from Hormiga import Hormiga, HormigaReina

# Definir las orientaciones de las hormigas
NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3

class HormigaLangton(object):
    """Hormiga de Langton implementado en Pygame."""

    background_color = pygame.Color(224, 226, 219) #Posibles colores (24, 29, 29), (1, 22, 39), (61, 8, 20), (13, 19, 33), (25, 34, 51)
    celulas_vivas_color = pygame.Color(255, 255, 255) #Blanco.
    celulas_muertas_color = pygame.Color(64, 64, 64) #Blanco.
    color_boton = pygame.Color(25, 42, 81) #Posibles (26, 83, 92)
    sombra_boton = (15, 20, 51)
    color_boton_desactivado = pygame.Color(124, 11, 43) #194, 1, 20
    sombra_boton_desactivado = pygame.Color(74, 5, 25)
    

    FPS = 60
    FramePerSec = pygame.time.Clock()

    def __init__(self, celulas_por_lado):

        self.largo_grid = 800
        self.ancho_grid = 600
        self.tamanio_superficie_grid = 540
        self.tamanio_superficie_desplegable = 500
        self.tamanio_celula = 10
        self.celulas_por_lado = celulas_por_lado

        self.grid_t_0 = np.zeros((celulas_por_lado, celulas_por_lado, 3), np.int8)
        self.grid_t_1 = np.zeros((celulas_por_lado, celulas_por_lado, 3), np.int8)

        self.ants_queen_t_0 = []
        self.ants_soldier_t_0 = []
        self.ants_worker_t_0 = []
        self.ants_breeder_t_0 = []

        self.crear_hormigas_iniciales()

        self.zoom_val_desplegable = 1
        #Atributos para controlar la visualización de las células.
        self.zoom_val = 1 #1 = 1 pix por célula, 5 = 5 pix por célula, 10 = 10 pix por célula

        self.celulas_desplegadas = 500

        #    Atributos para control de scrollbar.
        self.posicion_scroll_vertical = 40
        self.posicion_scroll_horizontal = 40

        #   Atributos para control de zoom

        self.regla = "B3/S23"
        self.B = [3]
        self.S = [2, 3]
        self.generacion = 0

        self.pausa = True

        #Atributos de gráficas.
        self.densidad = True
        self.entropia =True

    def gray(self, im):
        im = 255 * (im / im.max())
        w, h = im.shape
        ret = np.empty((w, h, 3), dtype=np.uint8)
        ret[:, :, 2] = ret[:, :, 1] = ret[:, :, 0] = im
        return ret

    def cargar_archivo(self):
        if self.pausa:
            root = tk.Tk()
            root.filename = tkinter.filedialog.askopenfilename(initialdir = os.getcwdb(),title = "Selecciona el archivo .txt.",filetypes = (("Archivos de texto","*.txt"),("all files","*.*")))
            ruta_archivo = root.filename
            #print("Ruta: ", ruta_archivo)
            #if(ruta_archivo == ""):
            #    tk.Button(root, text="Ningún archivo seleccionado. Cerrar ventada", command=root.destroy).pack()
            #    return

            tk.Button(root, text="Cargar archivo .txt", command=root.destroy).pack()
            root.mainloop()

            if(ruta_archivo == ""):
                return

            manejador_archivos = ManejadorArchivos()
            archivoDTO = manejador_archivos.leer_archivo(ruta_archivo)
            nuevo_tamanio = archivoDTO.ancho

            if nuevo_tamanio < 1000:
                nuevo_tamanio = 1000

            self.celulas_por_lado = nuevo_tamanio

            #Se crea un nuevo tamaño en función del archivo leído.
            self.grid_t_0 = np.zeros((nuevo_tamanio, nuevo_tamanio, 3), np.int8)
            self.grid_t_1 = np.zeros((nuevo_tamanio, nuevo_tamanio, 3), np.int8)

            for i in range(archivoDTO.alto):
                for j in range(archivoDTO.ancho):
                    if(archivoDTO.grid[i, j] == 0):
                        self.grid_t_0[i, j] = np.array([0, 0, 0], np.int8)
                    else:
                        self.grid_t_0[i, j] = np.array([255, 255, 255], np.int8)

            self.generacion = archivoDTO.generacion

    def guardar_configuracion(self):
        root = tk.Tk()
        root.filename = tkinter.filedialog.asksaveasfile(initialdir = os.getcwdb(), defaultextension=".txt" , title = "Guardar archivo de configuración", filetypes = (("Archivos de texto","*.txt"),("all files","*.*")))
        ruta_guardar_archivo = root.filename
        tk.Button(root, text="Guardar configuración.", command=root.destroy).pack()
        root.mainloop()

        if(ruta_guardar_archivo == None):
            return
        
        manejador_archivos = ManejadorArchivos()
        archivoDTO = ArchivoDTO()
        archivoDTO.numero_reinas = len(self.ants_queen_t_0)
        archivoDTO.numero_trabajadoras = len(self.ants_worker_t_0)
        archivoDTO.numero_soldados = len(self.ants_soldier_t_0)
        archivoDTO.numero_reproductoras = len(self.ants_breeder_t_0)
        archivoDTO.reinas = self.ants_queen_t_0
        archivoDTO.trabajadoras = self.ants_worker_t_0
        archivoDTO.soldados = self.ants_soldier_t_0
        archivoDTO.reproductoras = self.ants_breeder_t_0
        archivoDTO.ancho = self.celulas_por_lado
        archivoDTO.alto = self.celulas_por_lado
        archivoDTO.grid = self.grid_t_0
        print(archivoDTO.grid)
        archivoDTO.generacion = self.generacion
        archivoDTO.conteo_densidades['reina'] = self.hormigas_x_generacion['soldado']
        archivoDTO.conteo_densidades['trabajadora'] = self.hormigas_x_generacion['trabajadora']
        archivoDTO.conteo_densidades['soldado'] = self.hormigas_x_generacion['soldado']
        archivoDTO.conteo_densidades['reproductora'] = self.hormigas_x_generacion['reproductora']
        manejador_archivos.guardar_archivo(archivoDTO, ruta_guardar_archivo.name)
        root.mainloop()

    def mostrar_graficas(self):        

        t = np.arange(1, self.generacion, 1)
        s_soldado = self.hormigas_x_generacion['soldado'][1:self.generacion]
        s_trabajadora = self.hormigas_x_generacion['trabajadora'][1:self.generacion]
        s_reproductora = self.hormigas_x_generacion['reproductora'][1:self.generacion]
        s_reina = self.hormigas_x_generacion['reina'][1:self.generacion]

        fig, ax = plt.subplots()
        ax.plot(t, s_soldado)
        ax.plot(t, s_trabajadora)
        ax.plot(t, s_reproductora)
        ax.plot(t, s_reina)

        ax.set(xlabel='Generación', ylabel='Células',
                title='Densidad de células')
        ax.grid()
        plt.show()        


    def scrollbar(self, scrollbar_selecionada, posicion_nueva):
        if scrollbar_selecionada:
            #print("Horizontal")
            if posicion_nueva > 540 - self.tamanio_grip:
                self.posicion_scroll_horizontal = 540 - self.tamanio_grip
            else:
                self.posicion_scroll_horizontal = posicion_nueva
        else:
            #print("Vertical")
            if posicion_nueva > 540 - self.tamanio_grip:
                self.posicion_scroll_vertical = 540 - self.tamanio_grip
            else:
                self.posicion_scroll_vertical = posicion_nueva

        self.inicio_x = int((self.posicion_scroll_horizontal - 40) * (self.celulas_por_lado) / 500)
        self.inicio_y = int((self.posicion_scroll_vertical - 40) * (self.celulas_por_lado) / 500)

    def zoom_in(self):
        
        if self.zoom_val < 10:

            if self.zoom_val == 1:
                self.zoom_val = 5
                self.inicio_x += 125
                self.inicio_y += 125       
                self.celulas_desplegadas = 250            

            elif self.zoom_val == 5:
                self.zoom_val = 10
                self.inicio_x += 100
                self.inicio_y += 100       
                self.celulas_desplegadas = 50

            if self.inicio_x + self.celulas_desplegadas > self.celulas_por_lado:
                self.inicio_x -= self_inicio_x - self.celulas_desplegadas - self.celulas_por_lado
            if self.inicio_y + self.celulas_desplegadas > self.celulas_por_lado:
                self.inicio_y -= self_inicio_y - self.celulas_desplegadas - self.celulas_por_lado
            
            #Se modifica el tamaño del grip del scrollbar para que se visualice correctamente.
            self.tamanio_grip = (self.celulas_desplegadas/self.celulas_por_lado)*self.tamanio_superficie_grid

    def zoom_out(self):
        
        if self.zoom_val > 1:

            if self.zoom_val == 10:
                self.zoom_val = 5
                self.inicio_x -= 100
                self.inicio_y -= 100       
                self.celulas_desplegadas = 250            

            elif self.zoom_val == 5:
                self.zoom_val = 1
                self.inicio_x -= 125
                self.inicio_y -= 125       
                self.celulas_desplegadas = 500

            if self.inicio_x < 0:
                self.inicio_x = 0
            if self.inicio_y < 0:
                self.inicio_y = 0
            
            #Se modifica el tamaño del grip del scrollbar para que se visualice correctamente.
            self.tamanio_grip = (self.celulas_desplegadas/self.celulas_por_lado)*self.tamanio_superficie_grid

    
    def activar_pausa(self):
        tamanio_borde = 7
        if self.pausa:
            self.pausa = False
            pygame.draw.rect(self.screen, self.sombra_boton, (self.pos_x_gui, self.pos_y_gui+5, self.tamanio_boton_x, self.tamanio_boton_y), border_radius = tamanio_borde)
            pygame.draw.rect(self.screen, self.color_boton, (self.pos_x_gui, self.pos_y_gui, self.tamanio_boton_x, self.tamanio_boton_y), border_radius = tamanio_borde)
            pausa_text_surface, pausa_text_rect = self.font.render('Pausa', (255, 255, 255))
            self.screen.blit(pausa_text_surface, (self.pos_x_gui+71, self.pos_relativa_y_letras))
        else:
            self.pausa = True
            pygame.draw.rect(self.screen, self.sombra_boton_desactivado, (self.pos_x_gui, self.pos_y_gui+5, self.tamanio_boton_x, self.tamanio_boton_y), border_radius = tamanio_borde)
            pygame.draw.rect(self.screen, self.color_boton_desactivado, (self.pos_x_gui, self.pos_y_gui, self.tamanio_boton_x, self.tamanio_boton_y), border_radius = tamanio_borde)
            pausa_text_surface, pausa_text_rect = self.font.render('Pausa', (255, 255, 255))
            self.screen.blit(pausa_text_surface, (self.pos_x_gui+71, self.pos_relativa_y_letras))
    
    def manejo_click(self):
        posicion_mouse = pygame.mouse.get_pos()
        #print("Click con el ratón en posición: ", posicion_mouse)
        #Vertical (17, 40, 18, 500)
        #Horizontal (40, 17, 500, 18)
        if(posicion_mouse[0] >= 17 and posicion_mouse[0] <= 17+18 and posicion_mouse[1] >= 40 and posicion_mouse[1] <= 40 + 500):
            #Control vertical.
            self.scrollbar(False, posicion_mouse[1])
                    #       Scroll vertical
            pygame.draw.rect(self.superficie_principal, self.sombra_boton, (17, 40, 18, 500))
            pygame.draw.rect(self.superficie_principal, self.color_boton, (19, self.posicion_scroll_vertical, 14, self.tamanio_grip), border_radius = 8)

        elif(posicion_mouse[0] >= 40 and posicion_mouse[0] <= 40 + 500 and posicion_mouse[1] >= 17 and posicion_mouse[1] <= 17 + 18):
            #Control horizontal
            self.scrollbar(True, posicion_mouse[0])
                                    #       Scroll horizontal
            pygame.draw.rect(self.superficie_principal, self.sombra_boton, (40, 17, 500, 18))
            pygame.draw.rect(self.superficie_principal, self.color_boton, (self.posicion_scroll_horizontal, 19, self.tamanio_grip, 14), border_radius = 8)
                    
        #Verificación de cambio de estado de célula.
        elif(posicion_mouse[0] >= 40 and posicion_mouse[0] <= 540 and posicion_mouse[0] >= 40 and posicion_mouse[0] <= 540):
            #print("Modificacion celula.")
            #self.modificar_valor_celula(posicion_mouse)
            pass

        #Se verifica si es una posición donde se encuentra algún botón.
        #self.distancia_entre_boton = 60
        #self.tamanio_boton_x = 190
        #self.tamanio_boton_y = 32
        #self.pos_x_gui = 570
        #self.pos_y_gui = 37

        if(posicion_mouse[0] > 540):
            #print("Posible presión de botón.")
            #Pausa.
            if(posicion_mouse[0] >= self.pos_x_gui and posicion_mouse[0] <= self.pos_x_gui + self.tamanio_boton_x and 
               posicion_mouse[1] >= self.pos_y_gui and posicion_mouse[1] <= self.pos_y_gui + self.tamanio_boton_y):
                #print("Boton pausa presionado.")
                self.activar_pausa()
            
            #Cambiar regla.
            elif(posicion_mouse[0] >= self.pos_x_gui and posicion_mouse[0] <= self.pos_x_gui + self.tamanio_boton_x and 
               posicion_mouse[1] >= self.pos_y_gui+self.distancia_entre_boton and posicion_mouse[1] <= self.pos_y_gui + self.tamanio_boton_y+self.distancia_entre_boton):
                #print("Boton cambio de regla presionado.")
                self.cambiar_regla()

            #Cargar archivo.
            elif(posicion_mouse[0] >= self.pos_x_gui and posicion_mouse[0] <= self.pos_x_gui + self.tamanio_boton_x and 
               posicion_mouse[1] >= self.pos_y_gui+2*self.distancia_entre_boton and posicion_mouse[1] <= self.pos_y_gui + self.tamanio_boton_y+2*self.distancia_entre_boton):
                #print("Boton cargar archivo presionado.")
                self.cargar_archivo()

            #Guardar archivo.
            elif(posicion_mouse[0] >= self.pos_x_gui and posicion_mouse[0] <= self.pos_x_gui + self.tamanio_boton_x and 
               posicion_mouse[1] >= self.pos_y_gui+3*self.distancia_entre_boton and posicion_mouse[1] <= self.pos_y_gui + self.tamanio_boton_y+3*self.distancia_entre_boton):
                #print("Boton guardar archivo presionado.")
                self.guardar_configuracion()

            #Activar densidad.
            elif(posicion_mouse[0] >= self.pos_x_gui and posicion_mouse[0] <= self.pos_x_gui + self.tamanio_boton_x and 
               posicion_mouse[1] >= self.pos_y_gui+4*self.distancia_entre_boton and posicion_mouse[1] <= self.pos_y_gui + self.tamanio_boton_y+4*self.distancia_entre_boton):
                #print("Boton generar densidad. presionado..")
                self.graficar_densidad()

            #Activar entropía.
            elif(posicion_mouse[0] >= self.pos_x_gui and posicion_mouse[0] <= self.pos_x_gui + self.tamanio_boton_x and 
               posicion_mouse[1] >= self.pos_y_gui+5*self.distancia_entre_boton and posicion_mouse[1] <= self.pos_y_gui + self.tamanio_boton_y+5*self.distancia_entre_boton):
                #print("Botón generar entropia presionado.")
                self.graficar_entropia()

            #Mostrar graficas.
            elif(posicion_mouse[0] >= self.pos_x_gui and posicion_mouse[0] <= self.pos_x_gui + self.tamanio_boton_x and 
               posicion_mouse[1] >= self.pos_y_gui+6*self.distancia_entre_boton and posicion_mouse[1] <= self.pos_y_gui + self.tamanio_boton_y+6*self.distancia_entre_boton):
                #print("Botón mostrar gráficas presionado.")
                self.mostrar_graficas()


    def crear_hormigas_iniciales(self):
        
        numero_hormigas = random.randint(1, 100)
        for i in range(numero_hormigas):
            x = random.randint(0, 20)
            y = random.randint(0, 20)
            orientacion = random.randint(0, 3)
            vida_maxima = random.randint(1, 100000)
            tipo_hormiga = random.choice([0, 1, 2, 3]) #Soldado, Trabajadora, Reproductora, Reina
            if(tipo_hormiga == 0):
                self.ants_soldier_t_0.append(Hormiga(x, y, orientacion, vida_maxima))
            elif(tipo_hormiga == 1):
                self.ants_worker_t_0.append(Hormiga(x, y, orientacion, vida_maxima))
            elif(tipo_hormiga == 2):
                self.ants_breeder_t_0.append(Hormiga(x, y, orientacion, vida_maxima))
            else:
                edad_reproductiva_min = random.randint(0, vida_maxima-1)
                edad_reproductiva_max = random.randint(edad_reproductiva_min, vida_maxima)
                self.ants_queen_t_0.append(HormigaReina(x, y, orientacion, vida_maxima, edad_reproductiva_min, edad_reproductiva_max))

    def crear_nuevas_hormigas(self, nuevas_hormigas):
        for i in range(nuevas_hormigas):
            x = random.randint(0, self.celulas_por_lado)
            y = random.randint(0, self.celulas_por_lado)
            orientacion = random.randint(0, 3)
            vida_maxima = random.randint(1, 10000)
            tipo_hormiga = random.choice([0, 1, 2, 3]) #Soldado, Trabajadora, Reproductora, Reina
            if(tipo_hormiga == 0):
                self.ants_soldier_t_0.append(Hormiga(x, y, orientacion, vida_maxima))
            elif(tipo_hormiga == 1):
                self.ants_worker_t_0.append(Hormiga(x, y, orientacion, vida_maxima))
            elif(tipo_hormiga == 2):
                self.ants_breeder_t_0.append(Hormiga(x, y, orientacion, vida_maxima))
            else:
                edad_reproductiva_min = random.randint(0, vida_maxima-1)
                edad_reproductiva_max = random.randint(edad_reproductiva_min, vida_maxima)
                self.ants_queen_t_0.append(HormigaReina(x, y, orientacion, vida_maxima, edad_reproductiva_min, edad_reproductiva_max))

    def iniciar(self):

        pygame.init()
        pygame.display.set_caption('Hormiga de Langton')
        self.font = pygame.freetype.Font('Roboto/Roboto-Light.ttf', 16)
        
        self.screen = pygame.display.set_mode((self.largo_grid, self.ancho_grid))
        #self.screen.set_alpha(128)
        self.screen.fill(self.background_color)

        #Datos para graficación de densidad.
        #self.celulas_x_generacion = np.zeros(100000)
        self.hormigas_x_generacion = {
            'reina': np.zeros(100000),
            'trabajadora': np.zeros(100000),
            'soldado': np.zeros(100000),
            'reproductora': np.zeros(100000)
        }

        #Datos para graficación de entropía.
        self.entropia_x_generacion = np.zeros(100000)

        #Posicion inicial de dibujado.

        self.inicio_x = 0
        self.inicio_y = 0

        #Texto y botones.

        tamanio_borde = 7
        self.distancia_entre_boton = 60
        self.tamanio_boton_x = 190
        self.tamanio_boton_y = 32

        self.pos_x_gui = 570
        self.pos_y_gui = 37

        self.pos_relativa_y_letras = 48

        #Pausa
        pygame.draw.rect(self.screen, self.sombra_boton_desactivado, (self.pos_x_gui, self.pos_y_gui+5, self.tamanio_boton_x, self.tamanio_boton_y), border_radius = tamanio_borde)
        pygame.draw.rect(self.screen, self.color_boton_desactivado, (self.pos_x_gui, self.pos_y_gui, self.tamanio_boton_x, self.tamanio_boton_y), border_radius = tamanio_borde)
        pausa_text_surface, pausa_text_rect = self.font.render('Pausa', (255, 255, 255))
        self.screen.blit(pausa_text_surface, (self.pos_x_gui+71, self.pos_relativa_y_letras))

        #Cargar archivo
        pygame.draw.rect(self.screen, self.sombra_boton, (self.pos_x_gui, self.pos_y_gui+5+2*self.distancia_entre_boton, self.tamanio_boton_x, self.tamanio_boton_y), border_radius = tamanio_borde)
        pygame.draw.rect(self.screen, self.color_boton, (self.pos_x_gui, self.pos_y_gui+2*self.distancia_entre_boton, self.tamanio_boton_x, self.tamanio_boton_y), border_radius = tamanio_borde)
        cargar_archivo_text_surface, cargar_archivo_text_rect = self.font.render('Cargar archivo', (255, 255, 255))
        self.screen.blit(cargar_archivo_text_surface, (self.pos_x_gui+43, self.pos_relativa_y_letras+2*self.distancia_entre_boton))

        #Guardar archivo
        pygame.draw.rect(self.screen, self.sombra_boton, (self.pos_x_gui, self.pos_y_gui+5+3*self.distancia_entre_boton, self.tamanio_boton_x, self.tamanio_boton_y), border_radius = tamanio_borde)
        pygame.draw.rect(self.screen, self.color_boton, (self.pos_x_gui, self.pos_y_gui+3*self.distancia_entre_boton, self.tamanio_boton_x, self.tamanio_boton_y), border_radius = tamanio_borde)
        guardar_archivo_text_surface, guardar_archivo_text_rect = self.font.render('Guardar archivo', (255, 255, 255))
        self.screen.blit(guardar_archivo_text_surface, (self.pos_x_gui+40, self.pos_relativa_y_letras+3*self.distancia_entre_boton))

        #Mostrar gráficas
        pygame.draw.rect(self.screen, self.sombra_boton, (self.pos_x_gui, self.pos_y_gui+5+6*self.distancia_entre_boton, self.tamanio_boton_x, self.tamanio_boton_y), border_radius = tamanio_borde)
        pygame.draw.rect(self.screen, self.color_boton, (self.pos_x_gui, self.pos_y_gui+6*self.distancia_entre_boton, self.tamanio_boton_x, self.tamanio_boton_y), border_radius = tamanio_borde)
        generar_atractores_text_surface, generar_atractores_text_rect = self.font.render('Mostrar gráficas', (255, 255, 255))
        self.screen.blit(generar_atractores_text_surface, (self.pos_x_gui+40, self.pos_relativa_y_letras+6*self.distancia_entre_boton))


        #Ayuda
        """pygame.draw.rect(self.screen, self.sombra_boton, (self.pos_x_gui, self.pos_y_gui+5+8*self.distancia_entre_boton, self.tamanio_boton_x, self.tamanio_boton_y), border_radius = tamanio_borde)
        pygame.draw.rect(self.screen, self.color_boton, (self.pos_x_gui, self.pos_y_gui+8*self.distancia_entre_boton, self.tamanio_boton_x, self.tamanio_boton_y), border_radius = tamanio_borde)
        generar_atractores_text_surface, generar_atractores_text_rect = self.font.render('Ayuda', (255, 255, 255))
        self.screen.blit(generar_atractores_text_surface, (self.pos_x_gui, self.pos_relativa_y_letras+8*self.distancia_entre_boton))
        """

        #Manejo de superficie de desplegado de autómata.
        self.superficie_principal = pygame.Surface((self.tamanio_superficie_grid, self.tamanio_superficie_grid))
        self.superficie_principal.fill(self.background_color)
        #   Scrollbar

        self.celulas_desplegadas = 500
        self.tamanio_grip = (self.celulas_desplegadas/self.celulas_por_lado)*self.tamanio_superficie_grid

        #       Scroll vertical
        pygame.draw.rect(self.superficie_principal, self.sombra_boton, (17, 40, 18, 500))
        pygame.draw.rect(self.superficie_principal, self.color_boton, (19, self.posicion_scroll_vertical, 14, self.tamanio_grip), border_radius = 8)

        #       Scroll horizontal
        pygame.draw.rect(self.superficie_principal, self.sombra_boton, (40, 17, 500, 18))
        pygame.draw.rect(self.superficie_principal, self.color_boton, (self.posicion_scroll_horizontal, 19, self.tamanio_grip, 14), border_radius = 8)

        while(True):

            #Captura de eventos.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    #print("Tecla presionada.")
                    if event.key == pygame.K_SPACE:
                        self.activar_pausa()

                    if event.key == pygame.K_z:
                        #print("Zoom in")
                        self.zoom_in()

                    if event.key == pygame.K_x:
                        #print("Zoom out")
                        self.zoom_out()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_presses = pygame.mouse.get_pressed()
                    if(mouse_presses[0]):
                        self.manejo_click()

            if not self.pausa:
                # print("Juego en movimiento.")
                # self.grid_t_1 = OptimizacionesC.evaluar(self.grid_t_0, 2, 3, 3, 3).astype(np.int)    
                # print("Celulas: ", np.sum(self.grid_t_0))          
                # resultados = OptimizacionesC.evaluar(self.grid_t_0, self.B, self.S)
                #self.grid_t_1 = self.evaluate_langton_step(self.grid_t_0)
                print('Generación: ' + str(self.generacion))

                self.grid_t_1 = self.grid_t_0.copy()
                ants_positions = []

                # Soldado
                self.ants_soldier_t_1 = []
                for hormiga in self.ants_soldier_t_0:
                    valor_grid, informacion_hormiga = hormiga.procesar_paso(self.grid_t_0)
                    self.ants_soldier_t_1.append(
                        Hormiga(
                            informacion_hormiga['posicion'][0], 
                            informacion_hormiga['posicion'][1],
                            informacion_hormiga['orientacion'], 
                            hormiga.vida_maxima
                        )
                    )
                    self.grid_t_1[valor_grid['posicion'][0], valor_grid['posicion'][1]] = valor_grid['valor']
                    ants_positions.append(
                        (
                            informacion_hormiga['posicion'][0], 
                            informacion_hormiga['posicion'][1], 
                            [255, 0, 0]
                        )
                    )
                self.ants_soldier_t_0 = self.ants_soldier_t_1

                # Trabajadoras
                self.ants_worker_t_1 = []
                for hormiga in self.ants_worker_t_0:
                    valor_grid, informacion_hormiga = hormiga.procesar_paso(self.grid_t_0)
                    self.ants_worker_t_1.append(
                        Hormiga(
                            informacion_hormiga['posicion'][0], 
                            informacion_hormiga['posicion'][1],
                            informacion_hormiga['orientacion'], 
                            hormiga.vida_maxima
                        )
                    )
                    self.grid_t_1[valor_grid['posicion'][0], valor_grid['posicion'][1]] = valor_grid['valor']
                    ants_positions.append(
                        (
                            informacion_hormiga['posicion'][0], 
                            informacion_hormiga['posicion'][1], 
                            [255, 0, 0]
                        )
                    )
                self.ants_worker_t_0 = self.ants_worker_t_1

                # Reproductoras
                self.ants_breeder_t_1 = []
                for hormiga in self.ants_breeder_t_0:
                    valor_grid, informacion_hormiga = hormiga.procesar_paso(self.grid_t_0)
                    self.ants_breeder_t_1.append(
                        Hormiga(
                            informacion_hormiga['posicion'][0], 
                            informacion_hormiga['posicion'][1],
                            informacion_hormiga['orientacion'], 
                            hormiga.vida_maxima
                        )
                    )
                    self.grid_t_1[valor_grid['posicion'][0], valor_grid['posicion'][1]] = valor_grid['valor']
                    ants_positions.append(
                        (
                            informacion_hormiga['posicion'][0], 
                            informacion_hormiga['posicion'][1], 
                            [255, 0, 0]
                        )
                    )
                self.ants_breeder_t_0 = self.ants_breeder_t_1

                # Reinas
                self.ants_queen_t_1 = []
                nuevas_hormigas = 0
                for hormiga in self.ants_queen_t_0:
                    valor_grid, informacion_hormiga, nuevas_hormigas = hormiga.procesar_paso(self.grid_t_0, self.ants_queen_t_0, self.ants_breeder_t_0)
                    self.ants_queen_t_1.append(
                        HormigaReina(
                            informacion_hormiga['posicion'][0], 
                            informacion_hormiga['posicion'][1],
                            informacion_hormiga['orientacion'], 
                            informacion_hormiga['vida_maxima'],
                            informacion_hormiga['edad_reproductiva_min'],
                            informacion_hormiga['edad_reproductiva_max']
                        )
                    )
                    self.grid_t_1[valor_grid['posicion'][0], valor_grid['posicion'][1]] = valor_grid['valor']
                    ants_positions.append(
                        (
                            informacion_hormiga['posicion'][0], 
                            informacion_hormiga['posicion'][1], 
                            [255, 0, 0]
                        )
                    )
                self.ants_queen_t_0 = self.ants_queen_t_1
                self.crear_nuevas_hormigas(nuevas_hormigas)

                #self.grid_t_1, self.ants_t_1 = self.evaluate_langton_step(self.grid_t_0, self.ants_t_0)
                #self.grid_t_1 = resultados[0].astype(int)
                #self.entropia = resultados[1]
                self.grid_t_0 = self.grid_t_1.copy()
                
                for ant_position in ants_positions:
                    self.grid_t_1[ant_position[0], ant_position[1]] = ant_position[2]

                self.numero_celulas = np.sum(self.grid_t_0)
                self.generacion += 1
                #self.celulas_x_generacion[self.generacion] = self.numero_celulas
                self.hormigas_x_generacion['soldado'][self.generacion] = len(self.ants_soldier_t_0)
                self.hormigas_x_generacion['trabajadora'][self.generacion] = len(self.ants_worker_t_0)
                self.hormigas_x_generacion['reproductora'][self.generacion] = len(self.ants_breeder_t_0)
                self.hormigas_x_generacion['reina'][self.generacion] = len(self.ants_queen_t_0)
                #self.entropia_x_generacion[self.generacion] = self.entropia
                #pygame.display.set_caption('Autómata celular. Generación: '+str(self.generacion)+" Número de células: "+str(self.numero_celulas) + " Zoom: "+str(self.zoom_val)+" "+self.regla)
                pygame.display.set_caption('Hormiga de Langton. Generación: '+str(self.generacion)+" Zoom: "+str(self.zoom_val)+" "+self.regla)

            self.screen.blit(self.superficie_principal, (0, 0))
            
            #Redibujado del nuevo estado.
            surf_celulas = pygame.surfarray.make_surface(self.grid_t_1[self.inicio_x:self.inicio_x + self.celulas_desplegadas, self.inicio_y:self.inicio_y+self.celulas_desplegadas])
            self.superficie_principal.blit(pygame.transform.scale(surf_celulas, (self.tamanio_superficie_desplegable, self.tamanio_superficie_desplegable)), (40, 40))


            pygame.display.update()
            self.FramePerSec.tick(self.FPS)

if __name__ == '__main__':
        
    print("El número de células por lado debe ser mínimo 1000 y máximo 5000, además debe ser múltiplo de 500.")        
    is_valido = False
    while(not is_valido):
        celulas_por_lado = int(input("Ingresa el número de células por lado: "))
        if celulas_por_lado >= 0 and celulas_por_lado <= 5000:
            is_valido = True
        else:
            print("Número de células por lado inválido. Por favor ingresa un número válido con las reglas mostradas al inicio.")

    hormiga_langton = HormigaLangton(celulas_por_lado)
    hormiga_langton.iniciar()

    #generador = GeneradorArboles("B3/S23")
    #generador.dibujar_arboles()
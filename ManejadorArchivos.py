import numpy as np

from ArchivoDTO import ArchivoDTO
from Hormiga import Hormiga, HormigaReina


class ManejadorArchivos:
    def __init__(self):
        pass

    def guardar_archivo(self, archivoDTO, nombre_archivo):
        with open(nombre_archivo,'w') as file:
            file.write(f'{archivoDTO.numero_reinas} {archivoDTO.numero_trabajadoras} {archivoDTO.numero_soldados} {archivoDTO.numero_reproductoras}\n')
            for hormiga in archivoDTO.reinas:
                file.write(f'{str(hormiga)}\n')
            for hormiga in archivoDTO.trabajadoras:
                file.write(f'{str(hormiga)}\n')
            for hormiga in archivoDTO.soldados:
                file.write(f'{str(hormiga)}\n')
            for hormiga in archivoDTO.reproductoras:
                file.write(f'{str(hormiga)}\n')
            file.write(f'{archivoDTO.ancho} {archivoDTO.alto}\n')
            for i in range(archivoDTO.alto):
                for j in range(archivoDTO.ancho):
                    if(sum(archivoDTO.grid[i, j]) == 0):
                        file.write(f'0 ')
                    else:
                        file.write(f'1 ')
                file.write('\n')
            file.write(f'{archivoDTO.generacion} _\n')
            for valor in archivoDTO.conteo_densidades['reina']:
                file.write(f'{int(valor)} ')
            file.write('\n')
            for valor in archivoDTO.conteo_densidades['trabajadora']:
                file.write(f'{int(valor)} ')
            file.write('\n')
            for valor in archivoDTO.conteo_densidades['soldado']:
                file.write(f'{int(valor)} ')
            file.write('\n')
            for valor in archivoDTO.conteo_densidades['reproductora']:
                file.write(f'{int(valor)} ')
            file.write('\n')

    def leer_archivo(self, nombre_archivo):
        archivoDTO = ArchivoDTO()
        with open(nombre_archivo, 'r') as file:
            cantidades_hormigas = file.readline().split()
            archivoDTO.numero_reinas = int(cantidades_hormigas[0])
            archivoDTO.numero_trabajadoras = int(cantidades_hormigas[1])
            archivoDTO.numero_soldados = int(cantidades_hormigas[2])
            archivoDTO.numero_reproductoras = int(cantidades_hormigas[3])
            
            if(archivoDTO.numero_reinas > 0):
                for i in range(archivoDTO.numero_reinas):
                    informacion_hormiga_reina = file.readline().split()
                    nueva_hormiga_reina = HormigaReina(
                        int(informacion_hormiga_reina[0]),
                        int(informacion_hormiga_reina[1]),
                        int(informacion_hormiga_reina[2]),
                        int(informacion_hormiga_reina[3]),
                        int(informacion_hormiga_reina[4]),
                        int(informacion_hormiga_reina[5]),
                        int(informacion_hormiga_reina[6]),
                    )
                    archivoDTO.reinas.append(nueva_hormiga_reina)

            if(archivoDTO.numero_trabajadoras > 0):
                for i in range(archivoDTO.numero_trabajadoras):
                    informacion_hormiga = file.readline().split()
                    nueva_hormiga = Hormiga(
                        int(informacion_hormiga[0]),
                        int(informacion_hormiga[1]),
                        int(informacion_hormiga[2]),
                        int(informacion_hormiga[3]),
                        int(informacion_hormiga[4]),
                    )
                    archivoDTO.trabajadoras.append(nueva_hormiga)

            if(archivoDTO.numero_soldados > 0):
                for i in range(archivoDTO.numero_soldados):
                    informacion_hormiga = file.readline().split()
                    nueva_hormiga = Hormiga(
                        int(informacion_hormiga[0]),
                        int(informacion_hormiga[1]),
                        int(informacion_hormiga[2]),
                        int(informacion_hormiga[3]),
                        int(informacion_hormiga[4]),
                    )
                    archivoDTO.soldados.append(nueva_hormiga)

            if(archivoDTO.numero_reproductoras > 0):
                for i in range(archivoDTO.numero_reproductoras):
                    informacion_hormiga = file.readline().split()
                    nueva_hormiga = Hormiga(
                        int(informacion_hormiga[0]),
                        int(informacion_hormiga[1]),
                        int(informacion_hormiga[2]),
                        int(informacion_hormiga[3]),
                        int(informacion_hormiga[4]),
                    )
                    archivoDTO.reproductoras.append(nueva_hormiga)
            
            ancho, alto = file.readline().split()
            archivoDTO.ancho = int(ancho)
            archivoDTO.alto = int(alto)
            archivoDTO.grid = np.zeros((archivoDTO.alto, archivoDTO.ancho), int)
            for i in range(archivoDTO.alto):
                valores = file.readline().split()
                for j, valor in enumerate(valores):
                    archivoDTO.grid[i, j] = int(valor)
            
            archivoDTO.generacion = int(file.readline().split()[0])
            valores_reina = file.readline().split()
            for i, valor in enumerate(valores_reina):
                archivoDTO.conteo_densidades['reina'][i] = int(valor)

            valores_trabajadora = file.readline().split()
            for i, valor in enumerate(valores_trabajadora):
                archivoDTO.conteo_densidades['trabajadora'][i] = int(valor)

            valores_soldado = file.readline().split()
            for i, valor in enumerate(valores_soldado):
                archivoDTO.conteo_densidades['soldado'][i] = int(valor)

            valores_reproductora = file.readline().split()
            for i, valor in enumerate(valores_reproductora):
                archivoDTO.conteo_densidades['reproductora'][i] = int(valor)
        
        return archivoDTO

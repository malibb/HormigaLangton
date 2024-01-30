# Hormiga de Langton

Este repositorio contiene la implementación del programa "La Hormiga de Langton", un modelo matemático para un sistema de autómatas celulares.

## Descripción

El proyecto implementa la versión original de "La Hormiga de Langton" junto con una variante que incluye cuatro tipos de hormigas: reina, soldado, obreras y reproductoras. El programa ofrece una interfaz gráfica para visualizar la evolución del sistema, mostrar estadísticas como la densidad de hormigas, media, varianza, y la entropía de Shannon.

## Requisitos

- Python 3.x
- Pygame
- Tkinter
- Matplotlib
- Numpy

## Configuración del Entorno Virtual

Para configurar y utilizar un entorno virtual en Python, sigue los siguientes pasos:

1. Clona el repositorio a tu máquina local:

   ```
   git clone https://github.com/AlfredoT11/HormigaLangton.git
   cd HormigaLangton
   ```

2. Crea un entorno virtual en la carpeta del proyecto:

   ```
   python -m venv venv
   ```

   En Windows, usa:

   ```
   python -m venv venv
   ```

3. Activa el entorno virtual:

   En macOS y Linux:

   ```
   source venv/bin/activate
   ```

   En Windows:

   ```
   .\venv\Scripts\activate
   ```

4. Una vez activado el entorno virtual, instala las dependencias:

   ```
   pip install -r requirements.txt
   ```

## Ejecución

Para ejecutar el programa, asegúrate de que el entorno virtual esté activado y ejecuta el archivo principal:

```
python Langton.py
```

## Contribución

Las contribuciones al proyecto son bienvenidas. Por favor, asegúrate de seguir las buenas prácticas de programación y documentar cualquier cambio o mejora.

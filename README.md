[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/tu-usuario/tu-repositorio/main)

# Automated_Dataset_Construction
La creación de datasets personalizados es esencial en aplicaciones de visión computarizada cuando los conjuntos de datos existentes no cumplen con los requisitos específicos de un problema. En este trabajo, presentamos un algoritmo automatizado para la construcción de un dataset enfocado en la detección de infracciones vehiculares en pasos peatonales durante el turno asignado a los peatones por las señales de control de tráfico.

El dataset se generó a partir de imágenes capturadas por la cámara 49 del sistema de CCTV público de Medellín, Colombia. Se implementó un algoritmo que realiza la descarga automática de imágenes cada dos minutos, evalúa su calidad mediante métricas de brillo y desenfoque, y almacena los resultados junto con metadatos relevantes como resolución, timestamp y estado de calidad.

El conjunto de datos final contiene 347 imágenes en formato JPG, con una resolución de 1280 x 720 píxeles. Las imágenes presentan una calidad uniforme (sin desenfoque) y un brillo promedio de 93.11 (escala de 0 a 255). Este dataset permite la detección clara de pasos peatonales y vehículos, proporcionando una base sólida para entrenar modelos de visión computarizada orientados a la detección de infracciones.
l trabajo demuestra que la construcción automatizada de datasets personalizados es una solución viable y eficiente para problemas específicos. Además, el algoritmo presentado puede adaptarse a otras aplicaciones que requieran generación continua de datos a partir de fuentes similares.

Descripción General:
Este código implementa un sistema automatizado para descargar y procesar imágenes de cámaras CCTV. El programa descarga imágenes de una URL específica cada 2 minutos, las almacena localmente, analiza sus características y mantiene un registro detallado de metadatos en un archivo CSV.


## 1. Importaciones y Configuración Inicial:

```python
import requests, os, schedule, time, logging, hashlib, cv2, numpy, pandas
```
- Se importan bibliotecas para manejo de HTTP, sistema de archivos, programación de tareas, procesamiento de imágenes y análisis de datos
  - requests: Para hacer peticiones HTTP a la cámara
  - cv2 (OpenCV): Para procesamiento de imágenes
  - pandas: Para manejo de datos estructurados
  - numpy: Para cálculos numéricos
  - Otras librerías de soporte (logging, hashlib, etc.)
- Se configura un sistema de logging básico que guardará los registros en 'cctv_dataset.log'

## 2. Clase CCTVDatasetGenerator:
Esta es la clase principal que maneja toda la funcionalidad. Analicemos sus métodos:

a) Método Constructor (__init__)

```python
def __init__(self, url, download_folder, metadata_file):
```
- Inicializa los parámetros básicos
- Crea la estructura de carpetas necesaria
- Prepara el entorno para el almacenamiento

b) Método de Descarga (download_image)
```python
def analyze_image(self, filepath):
```
- Configura headers HTTP para simular un navegador
- Descarga la imagen de la cámara
- Genera un nombre único usando timestamp + hash
- Guarda la imagen y registra los metadatos

c) Método de Análisis (analyze_image)
```python
def analyze_image(self, filepath):
```
- Extrae características de la imagen:
  - Dimensiones (ancho x alto)
  - Número de canales de color
  - Brillo promedio y su desviación estándar
  - Detección de imágenes borrosas
    
d) Método de Detección de Desenfoque (detect_blur)
```python
def detect_blur(self, image, threshold=100):
``` 
- Convierte la imagen a escala de grises
- Aplica el operador Laplaciano
- Calcula la varianza para detectar desenfoque

## 3. Sistema de Metadatos 
```python
def update_metadata(self, filename, metadata):
```
- Mantiene un registro CSV de todas las imágenes
- Guarda características técnicas
- Permite análisis posterior del dataset

## 4. Configuración y Ejecución
```python
url = 'https://www.medellin.gov.co/SIMM/camaras-cctv/imagen49.jpg'
schedule.every(2).minutes.do(capture_image)
```
- Define la fuente de datos (URL de la cámara)
- Programa la captura cada 2 minutos
- Implementa un bucle principal de ejecución

## 5. Sistema de Control de Errores
- Logging detallado de operaciones
- Manejo de excepciones en cada etapa
- Reintentos automáticos en caso de fallos

```Bash
Cámara CCTV → Descarga → Procesamiento → Almacenamiento
                ↓           ↓              ↓
              Imagen → Metadatos → CSV + Archivos JPG
```

Este algoritmo es particularmente útil para crear datasets de imágenes CCTV para análisis posterior o entrenamiento de modelos de machine learning. Tiene las siguientes funcionalidades:

- Recolección automática de datos
- Control de calidad de imágenes
- Trazabilidad completa
- Escalabilidad y mantenibilidad

# Automated_Dataset_Construction
La creación de datasets personalizados es esencial en aplicaciones de visión computarizada cuando los conjuntos de datos existentes no cumplen con los requisitos específicos de un problema. En este trabajo, presentamos un algoritmo automatizado para la construcción de un dataset enfocado en la detección de infracciones vehiculares en pasos peatonales durante el turno asignado a los peatones por las señales de control de tráfico.

El dataset se generó a partir de imágenes capturadas por la cámara 49 del sistema de CCTV público de Medellín, Colombia. Se implementó un algoritmo que realiza la descarga automática de imágenes cada dos minutos, evalúa su calidad mediante métricas de brillo y desenfoque, y almacena los resultados junto con metadatos relevantes como resolución, timestamp y estado de calidad.

El conjunto de datos final contiene 347 imágenes en formato JPG, con una resolución de 1280 x 720 píxeles. Las imágenes presentan una calidad uniforme (sin desenfoque) y un brillo promedio de 93.11 (escala de 0 a 255). Este dataset permite la detección clara de pasos peatonales y vehículos, proporcionando una base sólida para entrenar modelos de visión computarizada orientados a la detección de infracciones.
l trabajo demuestra que la construcción automatizada de datasets personalizados es una solución viable y eficiente para problemas específicos. Además, el algoritmo presentado puede adaptarse a otras aplicaciones que requieran generación continua de datos a partir de fuentes similares.
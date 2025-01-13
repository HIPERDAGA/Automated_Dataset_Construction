import requests
import os
import schedule
import time
from datetime import datetime
import logging
import hashlib
import cv2
import numpy as np
import pandas as pd

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s: %(message)s',
    filename='cctv_dataset.log'
)


class CCTVDatasetGenerator:
    def __init__(self, url, download_folder, metadata_file):
        self.url = url
        self.download_folder = download_folder
        self.metadata_file = metadata_file

        # Crear carpetas
        os.makedirs(download_folder, exist_ok=True)
        os.makedirs(os.path.join(download_folder, 'images'), exist_ok=True)
        os.makedirs(os.path.join(download_folder, 'metadata'), exist_ok=True)

    def download_image(self):
        try:
            # Configuraciones de conexión robustas
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
                'Accept': 'image/webp,*/*',
                'Connection': 'keep-alive'
            }

            response = requests.get(
                self.url,
                headers=headers,
                timeout=(10, 30),
                stream=True
            )

            if response.status_code == 200:
                # Generar nombre de archivo
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                raw_image = response.content

                # Calcular hash para detección de duplicados
                image_hash = hashlib.md5(raw_image).hexdigest()
                filename = f'{timestamp}_{image_hash}.jpg'
                filepath = os.path.join(self.download_folder, 'images', filename)

                # Guardar imagen
                with open(filepath, 'wb') as file:
                    file.write(raw_image)

                # Analizar imagen
                image_metadata = self.analyze_image(filepath)

                # Registrar metadata
                self.update_metadata(filename, image_metadata)

                logging.info(f'Imagen procesada: {filename}')
                return filepath, image_metadata

            else:
                logging.error(f'Error de descarga: {response.status_code}')
                return None, None

        except Exception as e:
            logging.error(f'Error en descarga: {e}')
            return None, None

    def analyze_image(self, filepath):
        try:
            # Leer imagen con OpenCV
            image = cv2.imread(filepath)

            # Metadatos de imagen
            metadata = {
                'filename': os.path.basename(filepath),
                'width': image.shape[1],
                'height': image.shape[0],
                'channels': image.shape[2],
                'mean_brightness': np.mean(image),
                'std_brightness': np.std(image),
                'is_blurry': self.detect_blur(image),
                'timestamp': datetime.now().isoformat()
            }

            return metadata

        except Exception as e:
            logging.error(f'Error analizando imagen: {e}')
            return {}

    def detect_blur(self, image, threshold=100):
        # Método de Varianza de Laplaciano para detectar desenfoque
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        variance = cv2.Laplacian(gray, cv2.CV_64F).var()
        return variance < threshold

    def update_metadata(self, filename, metadata):
        try:
            # Cargar o crear DataFrame de metadatos
            if os.path.exists(self.metadata_file):
                df = pd.read_csv(self.metadata_file)
            else:
                df = pd.DataFrame()

            # Añadir nueva entrada
            new_entry = pd.DataFrame([metadata])
            df = pd.concat([df, new_entry], ignore_index=True)

            # Guardar metadata actualizada
            df.to_csv(self.metadata_file, index=False)

        except Exception as e:
            logging.error(f'Error actualizando metadatos: {e}')


# Configuración de parámetros
url = 'https://www.medellin.gov.co/SIMM/camaras-cctv/imagen49.jpg'
download_folder = r'C:\Users\hiper\Desktop\cctv_dataset'
metadata_file = os.path.join(download_folder, 'metadata', 'image_metadata.csv')

# Crear generador de dataset
dataset_generator = CCTVDatasetGenerator(url, download_folder, metadata_file)


# Programar descarga
def capture_image():
    dataset_generator.download_image()


# Configurar schedule
schedule.every(2).minutes.do(capture_image)

# Iniciar proceso
print("Iniciando generación de dataset CCTV...")
logging.info("Iniciando generación de dataset CCTV...")

# Primera captura inmediata
capture_image()

# Bucle principal
while True:
    try:
        schedule.run_pending()
        time.sleep(1)
    except Exception as e:
        logging.error(f"Error en generación de dataset: {e}")
        time.sleep(10)
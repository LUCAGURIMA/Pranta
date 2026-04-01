"""Arquivo de configuração padrão - Pranta MVP.

Este arquivo concentra todas as constantes e configurações da aplicação.
Pode ser expandido para suportar loading de arquivo .env ou .ini.

Uso:
    from config import PROCESSING_CONFIG, DATA_DIR
    config = PROCESSING_CONFIG
    print(config.hue_min)
"""

from pathlib import Path
from app.processing.pipeline import ProcessingConfig

# Caminhos base
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
RESULTS_DIR = DATA_DIR / "results"
INDEX_DIR = RESULTS_DIR / "index"
LOGS_DIR = BASE_DIR / "logs"

# Configuração do Pipeline de Processamento
# Ajuste estes valores conforme necessário para seu ambiente
PROCESSING_CONFIG = ProcessingConfig(
    hue_min=25,                   # Hue mínimo (verde escuro)
    hue_max=90,                   # Hue máximo (verde claro)
    sat_min=20,                   # Saturação mínima (cor vibrante)
    val_min=40,                   # Valor (luminância) mínima
    morphology_kernel_size=5,     # Tamanho kernel para operações morfológicas
    min_contour_area=500,         # Área mínima de contorno (pixels²)
)

# Configuração de câmera (padrão)
CAMERA_CONFIG = {
    "width": 640,
    "height": 480,
    "fps": 30,
}

# Limites de câmeras
MAX_CAMERAS = 2
CAMERA_DETECTION_TIMEOUT = 5  # segundos

# Configuração de UI
UI_CONFIG = {
    "window_width": 1200,
    "window_height": 800,
    "default_tab": 0,  # 0=Preview, 1=Comparação, 2=ΔArea, 3=Saturação
}

# Logging
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Validação de entrada
VALIDATION_RULES = {
    "plant_name_min_length": 1,
    "plant_name_max_length": 100,
    "genotype_min_length": 1,
    "genotype_max_length": 100,
}

# Timeouts
PROCESSING_TIMEOUT = 30  # segundos para completar pipeline

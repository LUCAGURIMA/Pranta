"""Módulo de persistência de dados para armazenamento de imagens e resultados.

Responsável por:
- Salvar imagens capturadas
- Salvar output.json com métricas
- Atualizar consolidado results.csv
"""

import os
import json
import csv
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, Any
import numpy as np
import cv2

from app.processing.pipeline import PlantMetrics

logger = logging.getLogger(__name__)

# Diretórios base
BASE_DIR = Path(__file__).parent.parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
RESULTS_DIR = DATA_DIR / "results"
INDEX_DIR = RESULTS_DIR / "index"
CONSOLIDATED_CSV = INDEX_DIR / "results.csv"


class StorageManager:
    """Gerencia persistência de dados (imagens, JSON, CSV)."""

    def __init__(self):
        """Inicializa o gerenciador de armazenamento."""
        self._ensure_directories()
        self._initialize_consolidated_csv()

    def _ensure_directories(self) -> None:
        """Cria diretórios necessários se não existirem."""
        for dir_path in [RAW_DIR, PROCESSED_DIR, RESULTS_DIR, INDEX_DIR]:
            dir_path.mkdir(parents=True, exist_ok=True)
            logger.info(f"Diretório garantido: {dir_path}")

    def _initialize_consolidated_csv(self) -> None:
        """Inicializa CSV consolidado se não existir."""
        if CONSOLIDATED_CSV.exists():
            return

        headers = [
            "timestamp",
            "plant_name",
            "genotype",
            "camera_id",
            "image_path",
            "area_px",
            "perimeter_px",
            "solidity",
            "circularity",
            "aspect_ratio",
            "hue_mean",
            "hue_std",
            "sat_mean",
            "sat_std",
            "val_mean",
            "val_std",
        ]

        with open(CONSOLIDATED_CSV, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()

        logger.info(f"CSV consolidado inicializado: {CONSOLIDATED_CSV}")

    def create_plant_session(self, plant_name: str) -> Path:
        """Cria pasta de sessão para uma planta.

        Args:
            plant_name: Nome da planta.

        Returns:
            Caminho da pasta raw da planta.
        """
        plant_raw_dir = RAW_DIR / plant_name
        plant_raw_dir.mkdir(parents=True, exist_ok=True)

        plant_processed_dir = PROCESSED_DIR / plant_name
        plant_processed_dir.mkdir(parents=True, exist_ok=True)

        plant_results_dir = RESULTS_DIR / plant_name
        plant_results_dir.mkdir(parents=True, exist_ok=True)

        logger.info(f"Sessão de planta criada: {plant_name}")
        return plant_raw_dir

    def save_image(
        self,
        frame: np.ndarray,
        plant_name: str,
        camera_id: int,
        timestamp: Optional[datetime] = None,
    ) -> Path:
        """Salva imagem capturada com nome padrão.

        Args:
            frame: Frame capturado (numpy array BGR).
            plant_name: Nome da planta.
            camera_id: ID da câmera.
            timestamp: Timestamp (usa hora atual se não fornecido).

        Returns:
            Caminho do arquivo salvo.
        """
        if timestamp is None:
            timestamp = datetime.now()

        plant_raw_dir = RAW_DIR / plant_name
        timestamp_str = timestamp.strftime("%Y%m%d_%H%M%S")
        filename = f"{plant_name}_{timestamp_str}_cam{camera_id}.jpg"
        filepath = plant_raw_dir / filename

        cv2.imwrite(str(filepath), frame)
        logger.info(f"Imagem salva: {filepath}")
        return filepath

    def save_mask(
        self,
        mask: np.ndarray,
        plant_name: str,
        camera_id: int,
        timestamp: Optional[datetime] = None,
    ) -> Optional[Path]:
        """Salva máscara de segmentação (opcional).

        Args:
            mask: Máscara binária.
            plant_name: Nome da planta.
            camera_id: ID da câmera.
            timestamp: Timestamp.

        Returns:
            Caminho do arquivo salvo ou None se erro.
        """
        try:
            if timestamp is None:
                timestamp = datetime.now()

            plant_processed_dir = PROCESSED_DIR / plant_name
            timestamp_str = timestamp.strftime("%Y%m%d_%H%M%S")
            filename = f"{plant_name}_{timestamp_str}_cam{camera_id}_mask.png"
            filepath = plant_processed_dir / filename

            cv2.imwrite(str(filepath), mask)
            logger.info(f"Máscara salva: {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"Erro ao salvar máscara: {e}")
            return None

    def save_metrics_json(
        self,
        metrics: PlantMetrics,
        plant_name: str,
        genotype: str,
        camera_id: int,
        image_path: Path,
        timestamp: Optional[datetime] = None,
    ) -> Optional[Path]:
        """Salva métricas em JSON por sessão/imagem.

        Args:
            metrics: Objeto PlantMetrics com resultados.
            plant_name: Nome da planta.
            genotype: Genótipo.
            camera_id: ID da câmera.
            image_path: Caminho da imagem processada.
            timestamp: Timestamp.

        Returns:
            Caminho do arquivo salvo ou None se erro.
        """
        try:
            if timestamp is None:
                timestamp = datetime.now()

            plant_results_dir = RESULTS_DIR / plant_name
            timestamp_str = timestamp.strftime("%Y%m%d_%H%M%S")
            filename = f"output_{timestamp_str}_cam{camera_id}.json"
            filepath = plant_results_dir / filename

            data = {
                "plant_name": plant_name,
                "genotype": genotype,
                "camera_id": camera_id,
                "timestamp_iso": timestamp.isoformat(),
                "image_path": str(image_path),
                "area_px": metrics.area_px,
                "perimeter_px": metrics.perimeter_px,
                "solidity": metrics.solidity,
                "circularity": metrics.circularity,
                "aspect_ratio": metrics.aspect_ratio,
                "hue_mean": metrics.hue_mean,
                "hue_std": metrics.hue_std,
                "sat_mean": metrics.sat_mean,
                "sat_std": metrics.sat_std,
                "val_mean": metrics.val_mean,
                "val_std": metrics.val_std,
            }

            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            logger.info(f"JSON de métricas salvo: {filepath}")
            return filepath

        except Exception as e:
            logger.error(f"Erro ao salvar JSON de métricas: {e}")
            return None

    def append_to_consolidated_csv(
        self,
        metrics: PlantMetrics,
        plant_name: str,
        genotype: str,
        camera_id: int,
        image_path: Path,
        timestamp: Optional[datetime] = None,
    ) -> bool:
        """Adiciona entrada ao CSV consolidado.

        Args:
            metrics: Objeto PlantMetrics.
            plant_name: Nome da planta.
            genotype: Genótipo.
            camera_id: ID da câmera.
            image_path: Caminho da imagem.
            timestamp: Timestamp.

        Returns:
            True se sucesso, False caso contrário.
        """
        try:
            if timestamp is None:
                timestamp = datetime.now()

            row = {
                "timestamp": timestamp.isoformat(),
                "plant_name": plant_name,
                "genotype": genotype,
                "camera_id": camera_id,
                "image_path": str(image_path),
                "area_px": metrics.area_px,
                "perimeter_px": metrics.perimeter_px,
                "solidity": metrics.solidity,
                "circularity": metrics.circularity,
                "aspect_ratio": metrics.aspect_ratio,
                "hue_mean": metrics.hue_mean,
                "hue_std": metrics.hue_std,
                "sat_mean": metrics.sat_mean,
                "sat_std": metrics.sat_std,
                "val_mean": metrics.val_mean,
                "val_std": metrics.val_std,
            }

            with open(CONSOLIDATED_CSV, "a", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=row.keys())
                writer.writerow(row)

            logger.info(f"Entrada adicionada ao CSV consolidado: {plant_name}")
            return True

        except Exception as e:
            logger.error(f"Erro ao adicionar entrada ao CSV: {e}")
            return False

    def get_consolidated_csv_path(self) -> Path:
        """Retorna caminho do CSV consolidado.

        Returns:
            Path do arquivo CSV.
        """
        return CONSOLIDATED_CSV

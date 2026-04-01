"""Pipeline de processamento de imagens para fenotipagem de plantas.

Implementa:
- Conversão RGB/BGR para HSV
- Threshold HSV
- Segmentação com máscaras
- Morfologia (abertura/fechamento)
- Extração de contornos e métricas
"""

import cv2
import numpy as np
import logging
from typing import Dict, Optional, Tuple
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class ProcessingConfig:
    """Configuração de thresholds para processamento HSV."""

    hue_min: int = 25
    hue_max: int = 90
    sat_min: int = 20
    val_min: int = 40
    morphology_kernel_size: int = 5
    min_contour_area: float = 500


@dataclass
class PlantMetrics:
    """Métricas extraídas do objeto planta segmentado."""

    area_px: float
    perimeter_px: float
    solidity: float
    circularity: float
    aspect_ratio: float
    hue_mean: float
    hue_std: float
    sat_mean: float
    sat_std: float
    val_mean: float
    val_std: float


class RGBSimplePipeline:
    """Pipeline RGB Simples para processamento de imagens de plantas."""

    def __init__(self, config: Optional[ProcessingConfig] = None):
        """Inicializa o pipeline com configuração.

        Args:
            config: Objeto ProcessingConfig com thresholds. Se None, usa padrões.
        """
        self.config = config or ProcessingConfig()
        self.last_mask = None

    def process_image(self, image: np.ndarray) -> Tuple[Optional[PlantMetrics], np.ndarray]:
        """Processa uma imagem BGR completa e extrai métricas.

        Args:
            image: Imagem RGB/BGR da câmera.

        Returns:
            Tupla (PlantMetrics ou None, máscara binária).
            Se falhar na segmentação, retorna (None, máscara_vazia).
        """
        try:
            # Step 1: Converter para HSV
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

            # Step 2: Threshold HSV
            mask = self._threshold_hsv(hsv)

            # Step 3: Segmentação com morfologia
            mask = self._morphology_operations(mask)

            # Step 4: Encontrar contorno principal e extrair métricas
            metrics = self._extract_metrics(image, hsv, mask)

            self.last_mask = mask
            return metrics, mask

        except Exception as e:
            logger.error(f"Erro no processamento da imagem: {e}")
            return None, np.zeros_like(image[:, :, 0], dtype=np.uint8)

    def _threshold_hsv(self, hsv: np.ndarray) -> np.ndarray:
        """Aplica threshold HSV para destacar tecido vegetal.

        Args:
            hsv: Imagem em espaço HSV.

        Returns:
            Máscara binária com pixels que atendem aos critérios.
        """
        # Separar canais
        h, s, v = cv2.split(hsv)

        # Threshold para cada canal
        mask_hue = cv2.inRange(h, self.config.hue_min, self.config.hue_max)
        mask_sat = cv2.inRange(s, self.config.sat_min, 255)
        mask_val = cv2.inRange(v, self.config.val_min, 255)

        # Combinar máscaras
        mask = cv2.bitwise_and(mask_hue, cv2.bitwise_and(mask_sat, mask_val))

        return mask

    def _morphology_operations(self, mask: np.ndarray) -> np.ndarray:
        """Aplica operações morfológicas para cleanup.

        Args:
            mask: Máscara binária.

        Returns:
            Máscara limpa.
        """
        kernel = cv2.getStructuringElement(
            cv2.MORPH_ELLIPSE, (self.config.morphology_kernel_size,
                                self.config.morphology_kernel_size)
        )

        # Abertura: erode + dilate (remove ruído)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)

        # Fechamento: dilate + erode (preenche pequenos buracos)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=1)

        return mask

    def _extract_metrics(
        self, image: np.ndarray, hsv: np.ndarray, mask: np.ndarray
    ) -> Optional[PlantMetrics]:
        """Extrai métricas de forma e cor do objeto segmentado.

        Args:
            image: Imagem BGR original.
            hsv: Imagem HSV.
            mask: Máscara binária.

        Returns:
            PlantMetrics ou None se não detectar contorno válido.
        """
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        if not contours:
            logger.warning("Nenhum contorno detectado na imagem.")
            return None

        # Encontrar maior contorno
        largest_contour = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(largest_contour)

        if area < self.config.min_contour_area:
            logger.warning(f"Contorno detectado menor que área mínima ({area} < {self.config.min_contour_area}).")
            return None

        # Métricas de forma
        perimeter = cv2.arcLength(largest_contour, True)
        
        # Solidity
        hull = cv2.convexHull(largest_contour)
        hull_area = cv2.contourArea(hull)
        solidity = area / hull_area if hull_area > 0 else 0

        # Circularidade
        circularity = (4 * np.pi * area) / (perimeter ** 2) if perimeter > 0 else 0

        # Aspect Ratio
        x, y, w, h = cv2.boundingRect(largest_contour)
        aspect_ratio = float(w) / h if h > 0 else 0

        # Estatísticas de cor no objeto segmentado
        h_channel, s_channel, v_channel = cv2.split(hsv)
        object_pixels = mask > 0

        hue_mean = float(np.mean(h_channel[object_pixels]))
        hue_std = float(np.std(h_channel[object_pixels]))
        sat_mean = float(np.mean(s_channel[object_pixels]))
        sat_std = float(np.std(s_channel[object_pixels]))
        val_mean = float(np.mean(v_channel[object_pixels]))
        val_std = float(np.std(v_channel[object_pixels]))

        metrics = PlantMetrics(
            area_px=float(area),
            perimeter_px=float(perimeter),
            solidity=float(solidity),
            circularity=float(circularity),
            aspect_ratio=float(aspect_ratio),
            hue_mean=hue_mean,
            hue_std=hue_std,
            sat_mean=sat_mean,
            sat_std=sat_std,
            val_mean=val_mean,
            val_std=val_std,
        )

        return metrics

    def get_last_mask(self) -> Optional[np.ndarray]:
        """Retorna última máscara processada.

        Returns:
            Máscara binária ou None.
        """
        return self.last_mask

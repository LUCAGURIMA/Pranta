"""Gerenciador de câmeras para captura de imagens de plantas.

Responsável por:
- Descoberta de câmeras USB disponíveis
- Conexão e configuração de câmeras
- Captura de frames
- Liberação de recursos
"""

import cv2
import logging
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class CameraInfo:
    """Informações de uma câmera detectada."""

    camera_id: int
    width: int = 640
    height: int = 480
    fps: int = 30


class CameraManager:
    """Gerencia descoberta, conexão e captura de câmeras USB."""

    def __init__(self):
        """Inicializa o gerenciador de câmeras."""
        self.cameras: Dict[int, cv2.VideoCapture] = {}
        self.camera_info: Dict[int, CameraInfo] = {}

    def detect_cameras(self) -> List[int]:
        """Detecta câmeras USB disponíveis.

        Returns:
            Lista com IDs de câmeras disponíveis.
        """
        available_cameras = []

        # Tentar até 5 câmeras (índices 0-4)
        for i in range(5):
            cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
            if cap.isOpened():
                available_cameras.append(i)
                cap.release()
                logger.info(f"Câmera detectada: ID {i}")
            cap.release()

        return available_cameras

    def connect_camera(
        self, camera_id: int, width: int = 640, height: int = 480, fps: int = 30
    ) -> bool:
        """Conecta a uma câmera específica.

        Args:
            camera_id: ID da câmera.
            width: Largura da resolução desejada.
            height: Altura da resolução desejada.
            fps: Taxa de frames por segundo desejada.

        Returns:
            True se conectou com sucesso, False caso contrário.
        """
        if camera_id in self.cameras:
            logger.warning(f"Câmera {camera_id} já está conectada.")
            return True

        try:
            cap = cv2.VideoCapture(camera_id, cv2.CAP_DSHOW)
            if not cap.isOpened():
                logger.error(f"Falha ao abrir câmera {camera_id}")
                return False

            # Configurar resolução e FPS
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
            cap.set(cv2.CAP_PROP_FPS, fps)

            # Ajustes de buffer para garantir frame atual
            cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

            self.cameras[camera_id] = cap
            self.camera_info[camera_id] = CameraInfo(
                camera_id=camera_id, width=width, height=height, fps=fps
            )

            logger.info(f"Câmera {camera_id} conectada: {width}x{height} @ {fps} fps")
            return True

        except Exception as e:
            logger.error(f"Erro ao conectar câmera {camera_id}: {e}")
            return False

    def capture_frame(self, camera_id: int) -> Optional[Tuple[bool, object]]:
        """Captura um frame da câmera especificada.

        Args:
            camera_id: ID da câmera.

        Returns:
            Tupla (sucesso, frame) ou None se câmera não está conectada.
        """
        if camera_id not in self.cameras:
            logger.warning(f"Câmera {camera_id} não está conectada.")
            return None

        cap = self.cameras[camera_id]
        success, frame = cap.read()

        if not success:
            logger.warning(f"Falha ao capturar frame da câmera {camera_id}")
            return None

        return success, frame

    def get_connected_cameras(self) -> List[int]:
        """Retorna lista de IDs de câmeras conectadas.

        Returns:
            Lista com IDs das câmeras conectadas.
        """
        return list(self.cameras.keys())

    def disconnect_camera(self, camera_id: int) -> bool:
        """Desconecta uma câmera específica.

        Args:
            camera_id: ID da câmera.

        Returns:
            True se desconectou com sucesso.
        """
        if camera_id not in self.cameras:
            return False

        try:
            self.cameras[camera_id].release()
            del self.cameras[camera_id]
            del self.camera_info[camera_id]
            logger.info(f"Câmera {camera_id} desconectada.")
            return True
        except Exception as e:
            logger.error(f"Erro ao desconectar câmera {camera_id}: {e}")
            return False

    def disconnect_all(self) -> None:
        """Desconecta todas as câmeras."""
        for camera_id in list(self.cameras.keys()):
            try:
                self.cameras[camera_id].release()
            except Exception as e:
                logger.error(f"Erro ao liberar câmera {camera_id}: {e}")

        self.cameras.clear()
        self.camera_info.clear()
        logger.info("Todas as câmeras foram liberadas.")

    def __del__(self):
        """Garante liberação de câmeras ao destruir objeto."""
        self.disconnect_all()

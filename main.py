"""Ponto de entrada da aplicação Pranta.

Responsável por:
- Configurar logging
- Inicializar aplicação PyQt5
- Exibir janela principal
"""

import sys
import logging
from pathlib import Path
from PyQt5.QtWidgets import QApplication

from app.ui.main_window import PrantaMainWindow

# Configurar logging
LOG_DIR = Path(__file__).parent / "logs"
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "pranta.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger(__name__)


def main():
    """Função principal de entrada."""
    try:
        logger.info("=" * 60)
        logger.info("Iniciando aplicação Pranta")
        logger.info("=" * 60)

        # Criar aplicação PyQt5
        app = QApplication(sys.argv)

        # Criar janela principal
        window = PrantaMainWindow()
        window.show()

        logger.info("Janela principal exibida")

        # Executar loop de eventos
        sys.exit(app.exec_())

    except Exception as e:
        logger.error(f"Erro crítico na aplicação: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()

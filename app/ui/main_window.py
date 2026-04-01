"""Interface principal da aplicação em PyQt5.

Componentes:
- Janela principal
- Painel de configuração (nome planta, genótipo, câmeras)
- Botões "Iniciar Sessão" e "Capturar Agora"
- Abas com preview, tabela de comparação e gráficos
"""

import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Optional

import cv2
import numpy as np
from PyQt5.QtCore import (
    Qt, QThread, pyqtSignal, QSize, QTimer
)
from PyQt5.QtGui import QImage, QPixmap, QFont
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QComboBox, QCheckBox, QPushButton,
    QTabWidget, QTableWidget, QTableWidgetItem, QMessageBox,
    QScrollArea, QGroupBox
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from app.capture.camera_manager import CameraManager
from app.processing.pipeline import RGBSimplePipeline, ProcessingConfig
from app.data.storage import StorageManager
from app.analytics.metrics import MetricsAnalyzer

logger = logging.getLogger(__name__)


class CaptureWorker(QThread):
    """Worker thread para captura e processamento de imagens."""

    capture_finished = pyqtSignal(bool, str)  # sucesso, mensagem
    processing_started = pyqtSignal()
    processing_finished = pyqtSignal()

    def __init__(
        self,
        camera_manager: CameraManager,
        pipeline: RGBSimplePipeline,
        storage: StorageManager,
        plant_name: str,
        genotype: str,
        camera_ids: List[int],
    ):
        """Inicializa worker de captura.

        Args:
            camera_manager: Gerenciador de câmeras.
            pipeline: Pipeline de processamento.
            storage: Gerenciador de armazenamento.
            plant_name: Nome da planta.
            genotype: Genótipo.
            camera_ids: Lista de IDs de câmeras para capturar.
        """
        super().__init__()
        self.camera_manager = camera_manager
        self.pipeline = pipeline
        self.storage = storage
        self.plant_name = plant_name
        self.genotype = genotype
        self.camera_ids = camera_ids

    def run(self):
        """Executa captura e processamento."""
        try:
            self.processing_started.emit()
            timestamp = datetime.now()
            success_count = 0
            error_messages = []

            for camera_id in self.camera_ids:
                try:
                    # Capturar frame
                    result = self.camera_manager.capture_frame(camera_id)
                    if result is None or not result[0]:
                        error_messages.append(f"Falha ao capturar frame da câmera {camera_id}")
                        continue

                    success, frame = result

                    # Salvar imagem
                    image_path = self.storage.save_image(
                        frame, self.plant_name, camera_id, timestamp
                    )

                    # Processar pipeline
                    metrics, mask = self.pipeline.process_image(frame)

                    if metrics is None:
                        error_messages.append(f"Falha ao segmentar planta na câmera {camera_id}")
                        continue

                    # Salvar máscara (opcional)
                    self.storage.save_mask(mask, self.plant_name, camera_id, timestamp)

                    # Salvar JSON
                    self.storage.save_metrics_json(
                        metrics, self.plant_name, self.genotype, camera_id, image_path, timestamp
                    )

                    # Atualizar CSV consolidado
                    self.storage.append_to_consolidated_csv(
                        metrics, self.plant_name, self.genotype, camera_id, image_path, timestamp
                    )

                    success_count += 1
                    logger.info(f"Captura e processamento concluídos para câmera {camera_id}")

                except Exception as e:
                    logger.error(f"Erro ao processar câmera {camera_id}: {e}")
                    error_messages.append(f"Erro câmera {camera_id}: {str(e)}")

            # Preparar mensagem final
            msg = f"Processadas {success_count}/{len(self.camera_ids)} câmeras com sucesso."
            if error_messages:
                msg += "\n\n" + "\n".join(error_messages)

            self.processing_finished.emit()
            self.capture_finished.emit(success_count > 0, msg)

        except Exception as e:
            logger.error(f"Erro crítico no worker: {e}")
            self.processing_finished.emit()
            self.capture_finished.emit(False, f"Erro: {str(e)}")


class PrantaMainWindow(QMainWindow):
    """Janela principal da aplicação Pranta."""

    def __init__(self):
        """Inicializa a janela principal."""
        super().__init__()
        self.setWindowTitle("Pranta - Fenotipagem de Plantas")
        self.setGeometry(100, 100, 1200, 800)

        # Inicializar componentes
        self.camera_manager = CameraManager()
        self.pipeline = RGBSimplePipeline(ProcessingConfig())
        self.storage = StorageManager()
        self.metrics_analyzer = MetricsAnalyzer()

        self.capture_worker: Optional[CaptureWorker] = None
        self.session_started = False

        # Setup UI
        self._setup_ui()
        self._detect_cameras()

    def _setup_ui(self) -> None:
        """Configura interface de usuário."""
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # Painel left: Configuração
        left_panel = self._create_config_panel()
        main_layout.addWidget(left_panel, 1)

        # Painel right: Visualizações
        right_panel = self._create_visualization_panel()
        main_layout.addWidget(right_panel, 2)

    def _create_config_panel(self) -> QGroupBox:
        """Cria painel de configuração.

        Returns:
            GroupBox com controles de configuração.
        """
        group = QGroupBox("Configuração")
        layout = QVBoxLayout()

        # Nome da planta
        layout.addWidget(QLabel("Nome da Planta:"))
        self.plant_name_input = QLineEdit()
        self.plant_name_input.setPlaceholderText("Ex: Tomate_01")
        layout.addWidget(self.plant_name_input)

        # Genótipo
        layout.addWidget(QLabel("Genótipo:"))
        self.genotype_input = QLineEdit()
        self.genotype_input.setPlaceholderText("Ex: WT, mutante_A")
        layout.addWidget(self.genotype_input)

        # Seleção de câmeras
        layout.addWidget(QLabel("Câmeras Disponíveis:"))
        self.camera_checks = {}

        for cam_id in range(5):
            checkbox = QCheckBox(f"Câmera {cam_id}")
            checkbox.setEnabled(False)
            self.camera_checks[cam_id] = checkbox
            layout.addWidget(checkbox)

        # Botões
        layout.addSpacing(20)

        self.start_session_btn = QPushButton("Iniciar Sessão")
        self.start_session_btn.clicked.connect(self._start_session)
        layout.addWidget(self.start_session_btn)

        self.capture_btn = QPushButton("Capturar Agora")
        self.capture_btn.setEnabled(False)
        self.capture_btn.clicked.connect(self._capture_image)
        layout.addWidget(self.capture_btn)

        # Status
        layout.addSpacing(20)
        layout.addWidget(QLabel("Status:"))
        self.status_label = QLabel("Pronto")
        self.status_label.setStyleSheet("color: blue;")
        layout.addWidget(self.status_label)

        # Último arquivo salvo
        layout.addSpacing(10)
        self.last_file_label = QLabel("Nenhuma captura ainda")
        self.last_file_label.setWordWrap(True)
        self.last_file_label.setStyleSheet("font-size: 9px; color: gray;")
        layout.addWidget(self.last_file_label)

        layout.addStretch()

        group.setLayout(layout)
        return group

    def _create_visualization_panel(self) -> QTabWidget:
        """Cria painel com abas de visualização.

        Returns:
            TabWidget com abas de preview, tabela e gráficos.
        """
        tabs = QTabWidget()

        # Aba: Preview (placeholder)
        preview_widget = QLabel("Preview de câmera (em desenvolvimento)")
        preview_widget.setAlignment(Qt.AlignCenter)
        tabs.addTab(preview_widget, "Preview")

        # Aba: Comparação (Tabela)
        comparison_widget = self._create_comparison_table()
        tabs.addTab(comparison_widget, "Comparação")

        # Aba: Gráfico ΔArea/dia
        delta_area_widget = self._create_delta_area_chart()
        tabs.addTab(delta_area_widget, "ΔArea/dia")

        # Aba: Gráfico Saturação
        saturation_widget = self._create_saturation_chart()
        tabs.addTab(saturation_widget, "Saturação (Saúde)")

        return tabs

    def _create_comparison_table(self) -> QWidget:
        """Cria tabela de comparação de genótipos.

        Returns:
            Widget com tabela.
        """
        widget = QWidget()
        layout = QVBoxLayout(widget)

        self.comparison_table = QTableWidget()
        self.comparison_table.setColumnCount(7)
        self.comparison_table.setHorizontalHeaderLabels([
            "Genótipo", "Área Média", "Desvio Área",
            "N Observações", "Sat Média", "Desvio Sat", "Plantas"
        ])
        self.comparison_table.resizeColumnsToContents()

        layout.addWidget(self.comparison_table)

        # Botão para atualizar
        refresh_btn = QPushButton("Atualizar Tabela")
        refresh_btn.clicked.connect(self._update_comparison_table)
        layout.addWidget(refresh_btn)

        return widget

    def _create_delta_area_chart(self) -> QWidget:
        """Cria gráfico de ΔArea/dia.

        Returns:
            Widget com matplotlib figure.
        """
        widget = QWidget()
        layout = QVBoxLayout(widget)

        self.delta_area_figure = Figure(figsize=(6, 4))
        self.delta_area_canvas = FigureCanvas(self.delta_area_figure)
        layout.addWidget(self.delta_area_canvas)

        # Botão para atualizar
        refresh_btn = QPushButton("Atualizar Gráfico")
        refresh_btn.clicked.connect(self._update_delta_area_chart)
        layout.addWidget(refresh_btn)

        return widget

    def _create_saturation_chart(self) -> QWidget:
        """Cria gráfico de saturação por genótipo.

        Returns:
            Widget com matplotlib figure.
        """
        widget = QWidget()
        layout = QVBoxLayout(widget)

        self.saturation_figure = Figure(figsize=(6, 4))
        self.saturation_canvas = FigureCanvas(self.saturation_figure)
        layout.addWidget(self.saturation_canvas)

        # Botão para atualizar
        refresh_btn = QPushButton("Atualizar Gráfico")
        refresh_btn.clicked.connect(self._update_saturation_chart)
        layout.addWidget(refresh_btn)

        return widget

    def _detect_cameras(self) -> None:
        """Detecta câmeras USB disponíveis."""
        try:
            available_cameras = self.camera_manager.detect_cameras()
            logger.info(f"Câmeras detectadas: {available_cameras}")

            for cam_id, checkbox in self.camera_checks.items():
                if cam_id in available_cameras:
                    checkbox.setEnabled(True)
                    checkbox.setText(f"Câmera {cam_id} ✓")
                    checkbox.setChecked(True)

            if not available_cameras:
                QMessageBox.warning(self, "Aviso", "Nenhuma câmera USB detectada.")

        except Exception as e:
            logger.error(f"Erro ao detectar câmeras: {e}")
            QMessageBox.critical(self, "Erro", f"Erro ao detectar câmeras: {e}")

    def _start_session(self) -> None:
        """Inicia sessão de uma planta."""
        # Validação
        plant_name = self.plant_name_input.text().strip()
        genotype = self.genotype_input.text().strip()

        if not plant_name:
            QMessageBox.warning(self, "Validação", "Nome da planta não pode estar vazio.")
            return

        if not genotype:
            QMessageBox.warning(self, "Validação", "Genótipo não pode estar vazio.")
            return

        selected_cameras = [
            cam_id for cam_id, checkbox in self.camera_checks.items()
            if checkbox.isChecked()
        ]

        if not selected_cameras:
            QMessageBox.warning(self, "Validação", "Selecione ao menos 1 câmera.")
            return

        # Conectar câmeras
        try:
            for camera_id in selected_cameras:
                if not self.camera_manager.connect_camera(camera_id):
                    raise Exception(f"Falha ao conectar câmera {camera_id}")

            # Criar sessão
            self.storage.create_plant_session(plant_name)

            self.session_started = True
            self.capture_btn.setEnabled(True)
            self.start_session_btn.setEnabled(False)
            self.plant_name_input.setEnabled(False)
            self.genotype_input.setEnabled(False)

            for checkbox in self.camera_checks.values():
                checkbox.setEnabled(False)

            self.status_label.setText(f"Sessão iniciada: {plant_name} ({genotype})")
            self.status_label.setStyleSheet("color: green;")

            QMessageBox.information(self, "Sucesso", "Sessão iniciada com sucesso!")

            logger.info(f"Sessão iniciada: {plant_name}, {genotype}, câmeras {selected_cameras}")

        except Exception as e:
            logger.error(f"Erro ao iniciar sessão: {e}")
            QMessageBox.critical(self, "Erro", f"Erro ao iniciar sessão: {e}")

    def _capture_image(self) -> None:
        """Captura imagem(ns) da câmera(s) selecionada(s)."""
        if not self.session_started:
            QMessageBox.warning(self, "Aviso", "Inicie uma sessão primeiro.")
            return

        plant_name = self.plant_name_input.text().strip()
        genotype = self.genotype_input.text().strip()
        selected_cameras = [
            cam_id for cam_id, checkbox in self.camera_checks.items()
            if checkbox.isChecked()
        ]

        # Desabilitar botão durante processamento
        self.capture_btn.setEnabled(False)
        self.status_label.setText("Processando...")
        self.status_label.setStyleSheet("color: orange;")

        # Criar e executar worker
        self.capture_worker = CaptureWorker(
            self.camera_manager,
            self.pipeline,
            self.storage,
            plant_name,
            genotype,
            selected_cameras,
        )

        self.capture_worker.capture_finished.connect(self._on_capture_finished)
        self.capture_worker.processing_finished.connect(self._on_processing_finished)
        self.capture_worker.start()

    def _on_capture_finished(self, success: bool, message: str) -> None:
        """Callback quando captura termina.

        Args:
            success: Sucesso na captura.
            message: Mensagem de status.
        """
        self.capture_btn.setEnabled(True)

        if success:
            self.status_label.setText("Captura concluída")
            self.status_label.setStyleSheet("color: green;")
            self.last_file_label.setText(f"Última captura: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            QMessageBox.information(self, "Captura", message)
        else:
            self.status_label.setText("Erro na captura")
            self.status_label.setStyleSheet("color: red;")
            QMessageBox.warning(self, "Erro", message)

        # Atualizar visualizações
        self._update_comparison_table()
        self._update_delta_area_chart()
        self._update_saturation_chart()

    def _on_processing_finished(self) -> None:
        """Callback quando processamento termina."""
        pass

    def _update_comparison_table(self) -> None:
        """Atualiza tabela de comparação."""
        try:
            self.metrics_analyzer.load_data()
            data = self.metrics_analyzer.get_comparison_table_data()

            self.comparison_table.setRowCount(len(data))

            for row_idx, row_data in enumerate(data):
                self.comparison_table.setItem(row_idx, 0, QTableWidgetItem(row_data["genotype"]))
                self.comparison_table.setItem(row_idx, 1, QTableWidgetItem(f"{row_data['area_mean']:.2f}"))
                self.comparison_table.setItem(row_idx, 2, QTableWidgetItem(f"{row_data['area_std']:.2f}"))
                self.comparison_table.setItem(row_idx, 3, QTableWidgetItem(str(row_data["area_count"])))
                self.comparison_table.setItem(row_idx, 4, QTableWidgetItem(f"{row_data['sat_mean']:.2f}"))
                self.comparison_table.setItem(row_idx, 5, QTableWidgetItem(f"{row_data['sat_std']:.2f}"))
                self.comparison_table.setItem(row_idx, 6, QTableWidgetItem(str(row_data["plant_count"])))

            self.comparison_table.resizeColumnsToContents()

        except Exception as e:
            logger.error(f"Erro ao atualizar tabela: {e}")

    def _update_delta_area_chart(self) -> None:
        """Atualiza gráfico de ΔArea/dia."""
        try:
            self.metrics_analyzer.load_data()
            delta_data = self.metrics_analyzer.calculate_daily_area_variations()

            self.delta_area_figure.clear()
            ax = self.delta_area_figure.add_subplot(111)

            if not delta_data:
                ax.text(0.5, 0.5, "Sem dados para exibir", ha="center", va="center")
                self.delta_area_canvas.draw()
                return

            # Preparar dados para plot
            genotypes = list(delta_data.keys())
            x_pos = range(len(genotypes))

            # Calcular média de ΔArea para cada genótipo
            delta_means = []
            for genotype in genotypes:
                all_deltas = []
                for date_deltas in delta_data[genotype].values():
                    all_deltas.extend(date_deltas)
                delta_means.append(np.mean(all_deltas) if all_deltas else 0)

            ax.bar(x_pos, delta_means, color="steelblue")
            ax.set_xlabel("Genótipo")
            ax.set_ylabel("ΔArea/dia (pixels²)")
            ax.set_title("Variação de Área por Dia vs Genótipo")
            ax.set_xticks(x_pos)
            ax.set_xticklabels(genotypes, rotation=45)
            ax.grid(axis="y", alpha=0.3)

            self.delta_area_figure.tight_layout()
            self.delta_area_canvas.draw()

        except Exception as e:
            logger.error(f"Erro ao atualizar gráfico ΔArea: {e}")

    def _update_saturation_chart(self) -> None:
        """Atualiza gráfico de saturação por genótipo."""
        try:
            self.metrics_analyzer.load_data()
            sat_data = self.metrics_analyzer.get_saturation_by_genotype()

            self.saturation_figure.clear()
            ax = self.saturation_figure.add_subplot(111)

            if not sat_data:
                ax.text(0.5, 0.5, "Sem dados para exibir", ha="center", va="center")
                self.saturation_canvas.draw()
                return

            genotypes = list(sat_data.keys())
            sat_means = [sat_data[g]["mean"] for g in genotypes]
            sat_stds = [sat_data[g]["std"] for g in genotypes]

            x_pos = range(len(genotypes))
            ax.bar(x_pos, sat_means, yerr=sat_stds, capsize=5, color="forestgreen", alpha=0.7)
            ax.set_xlabel("Genótipo")
            ax.set_ylabel("Saturação Média (HSV)")
            ax.set_title("Saturação por Genótipo (Saúde das Plantas)")
            ax.set_xticks(x_pos)
            ax.set_xticklabels(genotypes, rotation=45)
            ax.grid(axis="y", alpha=0.3)

            self.saturation_figure.tight_layout()
            self.saturation_canvas.draw()

        except Exception as e:
            logger.error(f"Erro ao atualizar gráfico saturação: {e}")

    def closeEvent(self, event):
        """Limpa recursos ao fechar aplicação.

        Args:
            event: Evento de fechamento.
        """
        try:
            self.camera_manager.disconnect_all()
            logger.info("Aplicação fechada com sucesso.")
        except Exception as e:
            logger.error(f"Erro ao fechar aplicação: {e}")
        event.accept()

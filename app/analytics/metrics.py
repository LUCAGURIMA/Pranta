"""Módulo de análises consolidadas e cálculo de métricas estatísticas.

Responsável por:
- Carregar e agregar dados de results.csv
- Calcular ΔArea/dia por planta
- Agregar dados por genótipo
- Preparar dados para visualizações
"""

import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).parent.parent.parent
CONSOLIDATED_CSV = BASE_DIR / "data" / "results" / "index" / "results.csv"


class MetricsAnalyzer:
    """Analisa dados consolidados e prepara visualizações."""

    def __init__(self, csv_path: Optional[Path] = None):
        """Inicializa analisador de métricas.

        Args:
            csv_path: Caminho para CSV consolidado. Se None, usa padrão.
        """
        self.csv_path = csv_path or CONSOLIDATED_CSV
        self.df: Optional[pd.DataFrame] = None

    def load_data(self) -> bool:
        """Carrega dados do CSV consolidado.

        Returns:
            True se carregou com sucesso, False caso contrário.
        """
        try:
            if not self.csv_path.exists():
                logger.warning(f"CSV não encontrado: {self.csv_path}")
                self.df = pd.DataFrame()
                return False

            self.df = pd.read_csv(self.csv_path)
            self.df["timestamp"] = pd.to_datetime(self.df["timestamp"])
            self.df["date"] = self.df["timestamp"].dt.date
            logger.info(f"Dados carregados: {len(self.df)} registros.")
            return True

        except Exception as e:
            logger.error(f"Erro ao carregar CSV: {e}")
            self.df = pd.DataFrame()
            return False

    def calculate_daily_area_variations(
        self,
    ) -> Dict[str, Dict[str, list]]:
        """Calcula variação de área (ΔArea) por dia para cada gênótipo.

        Returns:
            Dicionário {genotype: {date: [delta_area_values]}}.
        """
        try:
            if self.df is None or self.df.empty:
                logger.warning("Nenhum dado carregado para cálculo de ΔArea.")
                return {}

            result = {}

            for genotype, group in self.df.groupby("genotype"):
                genotype_data = {}

                for plant, plant_group in group.groupby("plant_name"):
                    # Ordenar por timestamp
                    plant_group = plant_group.sort_values("timestamp")
                    
                    # Agrupar por data
                    for date, date_group in plant_group.groupby("date"):
                        # Calcular área média do dia
                        daily_avg_area = date_group["area_px"].mean()

                        if date not in genotype_data:
                            genotype_data[date] = []
                        genotype_data[date].append(daily_avg_area)

                # Calcular delta entre dias consecutivos
                delta_data = {}
                sorted_dates = sorted(genotype_data.keys())

                for i in range(1, len(sorted_dates)):
                    prev_date = sorted_dates[i - 1]
                    curr_date = sorted_dates[i]

                    prev_area = np.mean(genotype_data[prev_date])
                    curr_area = np.mean(genotype_data[curr_date])
                    delta_area = curr_area - prev_area

                    if curr_date not in delta_data:
                        delta_data[curr_date] = []
                    delta_data[curr_date].append(delta_area)

                if delta_data:
                    result[genotype] = delta_data

            logger.info(f"ΔArea calculada para {len(result)} genótipos.")
            return result

        except Exception as e:
            logger.error(f"Erro ao calcular ΔArea/dia: {e}")
            return {}

    def get_saturation_by_genotype(
        self,
    ) -> Dict[str, Dict[str, float]]:
        """Calcula sauratação média (sat_mean) por genótipo.

        Returns:
            Dicionário {genotype: {stats}} com mean, std, count.
        """
        try:
            if self.df is None or self.df.empty:
                logger.warning("Nenhum dado carregado para cálculo de saturação.")
                return {}

            result = {}

            for genotype, group in self.df.groupby("genotype"):
                sat_values = group["sat_mean"].dropna()

                if len(sat_values) > 0:
                    result[genotype] = {
                        "mean": float(sat_values.mean()),
                        "std": float(sat_values.std()),
                        "count": len(sat_values),
                        "min": float(sat_values.min()),
                        "max": float(sat_values.max()),
                    }

            logger.info(f"Saturação calculada para {len(result)} genótipos.")
            return result

        except Exception as e:
            logger.error(f"Erro ao calcular saturação por genótipo: {e}")
            return {}

    def get_area_summary_by_genotype(
        self,
    ) -> Dict[str, Dict[str, float]]:
        """Calcula resumo de área por genótipo.

        Returns:
            Dicionário {genotype: {stats}} com mean, std, count.
        """
        try:
            if self.df is None or self.df.empty:
                logger.warning("Nenhum dado carregado para cálculo de área.")
                return {}

            result = {}

            for genotype, group in self.df.groupby("genotype"):
                area_values = group["area_px"].dropna()

                if len(area_values) > 0:
                    result[genotype] = {
                        "mean": float(area_values.mean()),
                        "std": float(area_values.std()),
                        "count": len(area_values),
                        "min": float(area_values.min()),
                        "max": float(area_values.max()),
                    }

            logger.info(f"Resumo de área calculado para {len(result)} genótipos.")
            return result

        except Exception as e:
            logger.error(f"Erro ao calcular resumo de área: {e}")
            return {}

    def get_comparison_table_data(self) -> List[Dict]:
        """Prepara dados para tabela comparativa entre genótipos.

        Returns:
            Lista de dicionários com dados aggregados.
        """
        try:
            if self.df is None or self.df.empty:
                return []

            data = []

            for genotype, group in self.df.groupby("genotype"):
                area_values = group["area_px"].dropna()
                sat_values = group["sat_mean"].dropna()

                row = {
                    "genotype": genotype,
                    "area_mean": float(area_values.mean()) if len(area_values) > 0 else 0,
                    "area_std": float(area_values.std()) if len(area_values) > 0 else 0,
                    "area_count": len(area_values),
                    "sat_mean": float(sat_values.mean()) if len(sat_values) > 0 else 0,
                    "sat_std": float(sat_values.std()) if len(sat_values) > 0 else 0,
                    "plant_count": group["plant_name"].nunique(),
                }
                data.append(row)

            logger.info(f"Tabela comparativa preparada com {len(data)} genótipos.")
            return data

        except Exception as e:
            logger.error(f"Erro ao preparar tabela comparativa: {e}")
            return []

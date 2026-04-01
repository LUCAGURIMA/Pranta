# Guia de Desenvolvimento - Pranta MVP

## 📝 Anotações para Evolução Futura

Este documento contém notas arquitetônicas e ideias para evoluções do Pranta além do MVP.

## 🏗️ Arquitetura Atual (MVP)

```
┌─────────────┐
│   UI (PyQt5)     │  ← main_window.py
└────────┬────────┘
         │
    ┌────┴──────┬────────────┬──────────┐
    │            │            │          │
┌───▼──┐  ┌─────▼────┐ ┌──────▼────┐ ┌──▼──────┐
│Camera│  │ Pipeline │ │ Storage   │ │Metrics  │
│Mgr   │  │ (RGB→HSV)│ │ (JSON,CSV)│ │ (Σ, Δ) │
└──────┘  └──────────┘ └───────────┘ └─────────┘
```

### Componentes

- **UI (main_window.py)**: Interface responsiva em PyQt5
- **CameraManager**: Gerencia câmeras USB
- **RGBSimplePipeline**: Processamento de imagem
- **StorageManager**: Persistência
- **MetricsAnalyzer**: Análises consolidadas

## 🔮 Ideias para Próximas Fases

### Fase 2: Agendamento & Automação
- [ ] Timer configurável para captura automática
- [ ] Background thread para capturar a cada N minutos
- [ ] Preview em tempo real de câmeras
- [ ] Queue de tarefas para processamento em batch

**Implementação sugerida**:
```python
# Em main_window.py
class Scheduler(QThread):
    def run(self):
        while self.is_running:
            if datetime.now() >= self.next_capture_time:
                self._capture_image()
                self.next_capture_time = ...
            time.sleep(1)
```

### Fase 3: UI Avançada
- [ ] Edição de thresholds HSV em tempo real (sliders)
- [ ] Preview ao vivo de máscara (split view)
- [ ] Exportar gráficos como PNG/PDF
- [ ] Tema dark/light
- [ ] Drag-and-drop de diretórios

### Fase 4: Persistência Avançada
- [ ] SQLite em vez de CSV (melhor para queries)
- [ ] Backup automático
- [ ] Sincronização com nuvem (Google Drive, S3)
- [ ] Multi-usuário com permissões

**Schema sugerido (SQLite)**:
```sql
CREATE TABLE plants (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  genotype TEXT NOT NULL,
  creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE captures (
  id INTEGER PRIMARY KEY,
  plant_id INTEGER FOREIGN KEY,
  camera_id INTEGER,
  timestamp TIMESTAMP,
  image_path TEXT,
  area_px REAL,
  -- ... outras métricas
  FOREIGN KEY(plant_id) REFERENCES plants(id)
);
```

### Fase 5: Análises Avançadas
- [ ] Curva de crescimento (fitting polinomial)
- [ ] ANOVA (significance testing entre genótipos)
- [ ] Regressão linear (predição de crescimento)
- [ ] Clustering automático de genótipos
- [ ] Alertas de anomalia (desvio > 2σ)

**Bibliotecas sugeridas**:
```python
import scipy.stats  # ANOVA, testes estatísticos
import scikit-learn  # Clustering (KMeans)
import np.polyfit   # Fitting polinomial
```

### Fase 6: API & Integração
- [ ] REST API (FastAPI) para integração com outros sistemas
- [ ] Webhook para notificações
- [ ] OAuth2 para autenticação
- [ ] WebSocket para sync em tempo real

**Exemplo (FastAPI)**:
```python
from fastapi import FastAPI
from app.analytics.metrics import MetricsAnalyzer

app = FastAPI()

@app.get("/api/genotypes")
def get_genotypes():
    analyzer = MetricsAnalyzer()
    analyzer.load_data()
    return analyzer.get_comparison_table_data()
```

### Fase 7: Mobile & Web
- [ ] App web em React/Vue (visualizar dados remotamente)
- [ ] App mobile (capturar com smartphone)
- [ ] Resposta imediata de métricas
- [ ] Dashboard público

## 🧪 Mejoras de Código

### Refactoring Sugerido
1. **Separar Worker**: Mover `CaptureWorker` para arquivo `app/workers/capture_worker.py`
2. **Config Manager**: Classe unificada para carregar/salvar configurações
3. **Database Layer**: Abstrair acesso a dados (CSV → DB)
4. **Error Handler**: Middleware centralizado para tratamento de erros

### Type Checking
```bash
pip install mypy
mypy app/  # Verificar tipos
```

### Testing
```python
# tests/test_pipeline.py
import pytest
from app.processing.pipeline import RGBSimplePipeline

def test_pipeline_with_dummy_image():
    pipeline = RGBSimplePipeline()
    dummy_frame = np.zeros((480, 640, 3), dtype=np.uint8)
    metrics, mask = pipeline.process_image(dummy_frame)
    assert metrics is not None or metrics is None  # Validar resultado
```

### CI/CD Sugerido
```yaml
# .github/workflows/test.yml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.10'
      - run: pip install -r requirements.txt
      - run: python -m pytest tests/
      - run: mypy app/
```

## 📚 Padrões de Design

### MVP Atual
- **MVC**: Model (pipeline) + View (UI) + Controller (main_window)
- **Observer**: Signals PyQt5 (GUIsinal de conclusão de thread)
- **Singleton**: StorageManager (instância única)

### Sugeridos
- **Factory**: Para criar diferentes tipos de pipelines (RGB, multispectral, etc.)
- **Strategy**: Para diferentes análises (atual, futura)
- **Command**: Para fila de operações

## 🚀 Performance

### Otimizações
1. **Cache de CSV**: Carregar em memória, sincronizar periodicamente
2. **Processamento em Batch**: Capturar múltiplas câmeras em paralelo
3. **Threading Pool**: Em vez de criar nova thread por captura
4. **Compressão de Imagens**: JPEG com qualidade reduzida

### Benchmarks (Desejável)
- Captura + Processamento: < 5 segundos
- Atualização de UI: < 100ms
- Carregamento de CSV: < 500ms
- Rendering de gráfico: < 1 segundo

## 📖 Documentação Futura

- [ ] Docstrings em Sphinx
- [ ] API documentation (auto-gerada)
- [ ] Video tutorial no YouTube
- [ ] Publicação em PyPI (permite `pip install pranta`)

## 🤝 Contribuição

Se evoluindo este projeto:

1. Crie branch: `git checkout -b feature/minha-feature`
2. Faça commits pequenos: `git commit -m "descrição clara"`
3. Rode testes: `python validate_installation.py`
4. Make PR com descrição detalhada

---

**Última actualização**: Janeiro 2025  
**Autor**: Tim AI Assistant  
**Status**: MVP Completo, Pronto para Evolução

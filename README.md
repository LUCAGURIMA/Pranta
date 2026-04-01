# Pranta - MVP de Fenotipagem de Plantas com RGB Simples

## 📋 Visão Geral

**Pranta** é um aplicativo desktop local para fenotipagem automatizada de plantas baseado em análise de imagem RGB com pipeline simples. Detecta e segmenta plantas em imagens capturadas de 1 a 2 câmeras USB, extrai métricas de forma e cor (HSV), e fornece análises comparativas por genótipo.

### Funcionalidades Principais

- ✅ **Detecção automática** de 1-2 câmeras USB
- ✅ **Captura manual** de imagens por botão
- ✅ **Pipeline RGB→HSV** com threshold configurável
- ✅ **Segmentação de plantas** com limpeza morfológica
- ✅ **Extração de métricas**: área, perímetro, solidez, circularidade, aspectratio, HSV (média/desvio)
- ✅ **Persistência**: imagens, JSON por captura, CSV consolidado
- ✅ **Análises**: ΔArea/dia por genótipo, saturação (saúde)
- ✅ **Visualizações**: gráficos interativos em matplotlib (abas), tabela comparativa
- ✅ **Interface em português** (PyQt5)
- ✅ **Logging local** para debugging

## 🏗️ Estrutura de Pastas

```
Pranta/
├── main.py                      # Ponto de entrada
├── requirements.txt             # Dependências
├── README.md                    # Este arquivo
├── logs/                        # Logs da aplicação (gerado)
│   └── pranta.log
├── app/
│   ├── __init__.py
│   ├── capture/
│   │   ├── __init__.py
│   │   └── camera_manager.py    # Detecção e controle de câmeras
│   ├── processing/
│   │   ├── __init__.py
│   │   └── pipeline.py          # Pipeline RGB→HSV + segmentação
│   ├── data/
│   │   ├── __init__.py
│   │   └── storage.py           # Salvamento de imagens/JSON/CSV
│   ├── analytics/
│   │   ├── __init__.py
│   │   └── metrics.py           # Análises consolidadas (ΔArea, Sat)
│   └── ui/
│       ├── __init__.py
│       └── main_window.py       # Interface PyQt5
├── data/
│   ├── raw/
│   │   └── <nome_planta>/       # Imagens capturadas
│   ├── processed/
│   │   └── <nome_planta>/       # Máscaras segmentadas
│   └── results/
│       ├── <nome_planta>/       # output.json por captura
│       └── index/
│           └── results.csv      # CSV CONSOLIDADO
```

## 🚀 Instalação

### Pré-requisitos

- **Windows 10/11**
- **Python 3.10+**
- **Câmeras USB** conectadas (opcional para testes, obrigatório para uso)

### Passo 1: Clonar/Baixar Projeto

```bash
cd Pranta
```

### Passo 2: Criar Ambiente Virtual

```bash
python -m venv venv
.\venv\Scripts\activate
```

### Passo 3: Instalar Dependências

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Passo 4: Verificar Instalação

```bash
python -c "import cv2, PyQt5, plantcv, pandas, matplotlib; print('Todas as dependências instaladas!')"
```

## 🎯 Execução

### Iniciar Aplicação

```bash
python main.py
```

A janela principal abrirá com:
- Painel de configuração (left)
- Abas de visualização (right)

## 📖 Fluxo de Uso

### 1. **Detectar Câmeras**
   - Conecte 1 ou 2 câmeras USB
   - Inicie a aplicação
   - Câmeras disponíveis aparecem no painel com checkbox ✓

### 2. **Iniciar Sessão**
   - **Nome da Planta**: identifica o espécime (ex: "Tomate_01")
   - **Genótipo**: permite comparação (ex: "WT", "mutante_A")
   - **Câmeras**: selecione 1 ou 2 câmeras
   - Clique em **"Iniciar Sessão"**
   - Pastas são criadas automaticamente em `data/raw/<nome_planta>/`

### 3. **Capturar Imagens**
   - Clique em **"Capturar Agora"** para capturar de todas as câmeras selecionadas
   - Imagens são salvas com padrão: `<nome_planta>_YYYYMMDD_HHMMSS_cam<X>.jpg`
   - Pipeline de processamento executa automaticamente em thread (não trava UI)
   - Status exibe mensagens de sucesso ou erro

### 4. **Analisar Resultados**
   - Abra a aba **"Comparação"** para ver tabela com genótipos
   - Abra **"ΔArea/dia"** para gráfico de crescimento por genótipo
   - Abra **"Saturação (Saúde)"** para ver HSV médio com desvio

### 5. **Reatualizar Visualizações**
   - Use os botões "Atualizar" em cada aba para recarregar gráficos
   - Dados são lidos em tempo real do `data/results/index/results.csv`

## 📊 Pipeline de Processamento

### Entrada
Imagem RGB/BGR de câmera 640×480 (padrão)

### Etapas

#### 1. **Conversão HSV**
```python
HSV = cv2.cvtColor(BGR, cv2.COLOR_BGR2HSV)
```

#### 2. **Threshold HSV**
Limiar configurável (padrão):
- **Hue**: 25–90 (verde)
- **Sat**: ≥20 (cor vibrante)
- **Val**: ≥40 (luz suficiente)

```python
mask = cv2.inRange(H, 25, 90) & cv2.inRange(S, 20, 255) & cv2.inRange(V, 40, 255)
```

#### 3. **Segmentação (Morfologia)**
- Abertura: remove ruído pequeno
- Fechamento: preenche buracos

```python
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
```

#### 4. **Extração de Contorno**
- Encontra maior contorno (planta)
- Descarta se área < 500 px²

#### 5. **Cálculo de Métricas**
Para o contorno válido:

| Métrica | Fórmula |
|---------|---------|
| **area_px** | Pixels²  |
| **perimeter_px** | Comprimento arco |
| **solidity** | area / area_casco_convexo |
| **circularity** | 4π·A / P² |
| **aspect_ratio** | largura_bbox / altura_bbox |
| **hue_mean/std** | Média/desvio H no objeto |
| **sat_mean/std** | Média/desvio S no objeto |
| **val_mean/std** | Média/desvio V no objeto |

## 💾 Formatos de Saída

### Imagem Capturada
```
data/raw/<nome_planta>/<nome_planta>_YYYYMMDD_HHMMSS_cam<X>.jpg
```

### JSON de Métricas
```json
{
  "plant_name": "Tomate_01",
  "genotype": "WT",
  "camera_id": 0,
  "timestamp_iso": "2025-01-15T14:32:45.123456",
  "image_path": "data/raw/Tomate_01/Tomate_01_20250115_143245_cam0.jpg",
  "area_px": 45230.5,
  "perimeter_px": 850.2,
  "solidity": 0.92,
  "circularity": 0.78,
  "aspect_ratio": 1.15,
  "hue_mean": 52.3,
  "hue_std": 8.5,
  "sat_mean": 145.2,
  "sat_std": 25.3,
  "val_mean": 120.1,
  "val_std": 18.7
}
```

### CSV Consolidado
```csv
timestamp,plant_name,genotype,camera_id,image_path,area_px,perimeter_px,solidity,circularity,aspect_ratio,hue_mean,hue_std,sat_mean,sat_std,val_mean,val_std
2025-01-15T14:32:45.123456,Tomate_01,WT,0,data/raw/Tomate_01/Tomate_01_20250115_143245_cam0.jpg,45230.5,850.2,0.92,0.78,1.15,52.3,8.5,145.2,25.3,120.1,18.7
```

## 📈 Análises Disponíveis

### 1. **ΔArea/dia vs Genótipo** (Gráfico de Barras)
Mostra crescimento médio da planta por dia para cada genótipo:
- Agrupa por data (data da foto)
- Calcula área média do dia
- Calcula diferença entre dias consecutivos
- Média dos deltas por genótipo

**Interpretação**: Genótipos com ΔArea maior têm crescimento mais acelerado.

### 2. **Saturação (Saúde) por Genótipo** (Gráfico de Barras com Erro)
Mostra qualidade de cor (saturação HSV) média:
- Saturação alta = tecido saudável, cor vibrante
- Desvio padrão indica variabilidade

**Interpretação**: Genótipos com sat_mean alta e std baixa têm fotossíntese mais homogênea.

### 3. **Tabela Comparativa**
| Coluna | Significado |
|--------|------------|
| Genótipo | Nome do genótipo |
| Área Média | Media de area_px em todas as capturas |
| Desvio Área | σ (σ da área) |
| N Observações | Total de imagens |
| Sat Média | Média de sat_mean |
| Desvio Sat | σ (σ da saturação) |
| Plantas | Quantas plantas deste genótipo |

## 🔧 Configuração (Thresholds HSV)

Os thresholds são configuráveis em `app/processing/pipeline.py`:

```python
config = ProcessingConfig(
    hue_min=25,              # Verde mínimo
    hue_max=90,              # Verde máximo
    sat_min=20,              # Saturação mínima
    val_min=40,              # Valor (luminância) mínima
    morphology_kernel_size=5,
    min_contour_area=500,    # Área mínima da planta (pixels²)
)
```

**Para ajustar**:
1. Capture imagem de teste
2. Abra no editor de código
3. Modifique valores em `ProcessingConfig`
4. Reinicie aplicação
5. Compare resultados nas máscaras (armazenadas em `data/processed/`)

## 🐛 Troubleshooting

### Problema: "Nenhuma câmera USB detectada"
**Solução**:
- Desconecte e reconecte a câmera
- Reinstale drivers de câmera (buscar Site do fabricante)
- Teste câmera com aplicativo nativo (Windows Camera)
- Verifique permissões (executa como Admin?)

### Problema: Aplicação trava durante captura
**Solução**:
- Processamento está em thread (não deve travar)
- Se travar, possível erro em `camera_manager.py`
- Verifique logs em `logs/pranta.log`
- Aumente memória disponível

### Problema: Nenhuma planta segmentada (area_px = 0)
**Solução**:
- Verificar iluminação (necessária para threshold HSV)
- Ajustar thresholds HSV conforme fundo
- Verificar máscara em `data/processed/`
- Testar com background mais simples (fundo branco/preto)

### Problema: Arquivo results.csv vazio
**Solução**:
- Aplicação cria CSV na primeira captura
- Se nada foi capturado, será vazio
- Capture imagens com sucesso (veja status na UI)
- Recarregue visualizações (botão "Atualizar")

### Problema: Gráfico exibe "Sem dados para exibir"
**Solução**:
- CSV consolidado está vazio (capture imagens primeiro)
- Clique em "Atualizar Gráfico" para recarregar
- Verifique se métricas foram salvas (ver JSON em `data/results/`)

## 📝 Logs

Todas as ações são registradas em:
```
logs/pranta.log
```

**Exemplo**:
```
2025-01-15 14:32:45,123 - app.capture.camera_manager - INFO - Câmera 0 conectada: 640x480 @ 30 fps
2025-01-15 14:32:46,500 - app.processing.pipeline - INFO - PlantMetrics extraídas com sucesso
2025-01-15 14:32:47,100 - app.data.storage - INFO - Imagem salva: data/raw/Tomate_01/Tomate_01_20250115_143245_cam0.jpg
```

## 🔒 Segurança & Boas Práticas

- **Não sobrescreve imagens**: timestamp com segundos garante unicidade
- **Validação de entrada**: nome_planta e genótipo obrigatórios
- **Handling de erros**: tenta processar câmeras individualmente (uma falha ≠ app trava)
- **Resources cleanup**: câmeras liberadas ao fechar app
- **Type hints**: código tipado (Python 3.10+)

## 📚 Referências & Stack

| Componente | Biblioteca | Função |
|-----------|-----------|--------|
| Captura | OpenCV 4.6+ | cv2.VideoCapture, frame capture |
| Processamento | PlantCV 3.12+ | Funções vegetal (opcional; usamos OpenCV aqui) |
| Interface | PyQt5 5.15+ | UI, threads, canvas matplotlib |
| Análise | Pandas 1.4+ | CSV leitura/escrita, groupby |
| Visualização | Matplotlib 3.5+ | Gráficos embutidos (bar, errorbar) |
| Threading | Threading/QThread | Não trava UI durante processamento |

## 📋 Checklist de Aceite

- [x] Detecta e seleciona 1 ou 2 webcams
- [x] Cria pasta da planta ao iniciar sessão
- [x] Salva imagem com nome planta+timestamp+cam
- [x] Gera output.json com todos os campos obrigatórios
- [x] Atualiza consolidado results.csv
- [x] Exibe ΔArea/dia vs genótipo
- [x] Exibe sat_mean por genótipo
- [x] Aplicação estável sem travamentos em fluxo normal
- [x] Código modular, tipado, com logging
- [x] README com instalação/execução/troubleshooting

## 🚧 Próximas Fases (Futuro)

- [ ] Agendamento automático de capturas (timer)
- [ ] Preview em tempo real de câmeras
- [ ] Edição de thresholds na UI (não requer restart)
- [ ] Exportar gráficos como PNG/PDF
- [ ] Suporte a múltiplas plantas na mesma sessão
- [ ] Análises estatísticas avançadas (ANOVA, regressão)
- [ ] Banco de dados SQLite (em vez de CSV)
- [ ] API REST para integração com outros sistemas

## 📧 Suporte

Para questões ou problemas:
1. Verifique `logs/pranta.log`
2. Consulte seção "Troubleshooting"
3. Teste com câmera nativa do Windows
4. Considere atualizar drivers de câmera

---

**Versão MVP**: 1.0.0  
**Data**: Janeiro 2025  
**Stack**: Python 3.10+ | PyQt5 | OpenCV | PlantCV | Pandas | Matplotlib

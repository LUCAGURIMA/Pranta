# 📊 Exemplos - Pranta MVP

## Arquivos de Exemplo

Este diretório contém exemplos de saída da aplicação Pranta.

### 1. `output_example.json`

**Descrição**: Exemplo de JSON gerado pela aplicação após processar uma imagem.

**Estrutura**:
```json
{
  "plant_name": "Tomate_01",      // Nome da planta capturada
  "genotype": "WT",                // Genótipo para comparação
  "camera_id": 0,                  // ID da câmera (0 ou 1)
  "timestamp_iso": "2025-01-15T14:32:45.123456",  // ISO 8601
  "image_path": "data/raw/Tomate_01/...",         // Onde a imagem foi salva
  
  // Métricas de Forma
  "area_px": 45230.5,              // Área em pixels²
  "perimeter_px": 850.2,           // Perímetro em pixels
  "solidity": 0.92,                // Area / ConvexHullArea (0-1)
  "circularity": 0.78,             // 4π·A/P² (1 = círculo perfeito)
  "aspect_ratio": 1.15,            // Width / Height do bounding box
  
  // Estatísticas de Cor (HSV)
  "hue_mean": 52.3,                // Matiz média (0-179 em OpenCV)
  "hue_std": 8.5,                  // Desvio padrão do matiz
  "sat_mean": 145.2,               // Saturação média (0-255)
  "sat_std": 25.3,                 // Desvio padrão da saturação
  "val_mean": 120.1,               // Valor (luminância) média (0-255)
  "val_std": 18.7                  // Desvio padrão do valor
}
```

**Localização Real**: `data/results/<nome_planta>/output_YYYYMMDD_HHMMSS_cam<X>.json`

**Uso**: Importar em Python:
```python
import json

with open("output_example.json") as f:
    metrics = json.load(f)
    
print(f"Área: {metrics['area_px']} px²")
print(f"Saturação: {metrics['sat_mean']:.2f}")
```

---

### 2. `results_example.csv`

**Descrição**: Exemplo de CSV consolidado que acumula histórico de capturas.

**Estrutura**:
```
timestamp | plant_name | genotype | camera_id | image_path | area_px | ... | val_std
----------+------------+----------+-----------+------------+---------+-----+---------
20250115T14:32:45 | Tomate_01 | WT | 0 | data/raw/... | 45230.5 | ... | 18.7
20250115T14:45:22 | Tomate_01 | WT | 1 | data/raw/... | 46120.3 | ... | 19.2
20250115T15:10:15 | Tomate_02 | mutante_A | 0 | data/raw/... | 38950.7 | ... | 20.1
20250116T09:00:00 | Tomate_01 | WT | 0 | data/raw/... | 48500.1 | ... | 18.9
... (acumula cada captura)
```

**Localização Real**: `data/results/index/results.csv`

**Colunas** (16 no total):
1. `timestamp` - Quando foi capturada (ISO 8601)
2. `plant_name` - Nome da planta
3. `genotype` - Genótipo para comparação
4. `camera_id` - Qual câmera (0 ou 1)
5. `image_path` - Onde a imagem foi salva
6. `area_px` - Área do contorno
7. `perimeter_px` - Perímetro
8. `solidity` - Compactacao
9. `circularity` - Formato
10. `aspect_ratio` - Proporção
11. `hue_mean` - Matiz média
12. `hue_std` - Desvio matiz
13. `sat_mean` - Saturação média ← Indica saúde
14. `sat_std` - Desvio saturação
15. `val_mean` - Valor (brilho) médio
16. `val_std` - Desvio brilho

**Uso**: Abrir no Excel ou analisar em Python:
```python
import pandas as pd

df = pd.read_csv("results_example.csv")
print(df.head())                              # Primeiras 5 linhas
print(df.groupby("genotype")["area_px"].mean())  # Área média por genótipo
print(df.groupby("genotype")["sat_mean"].mean()) # Saturação média por genótipo
```

**Características**:
- ✅ Cumulativo (nunca sobrescreve)
- ✅ Headers na primeira linha
- ✅ Uma linha por captura
- ✅ Timestamps ISO para rastreabilidade temporal
- ✅ Excel compatível

---

## 📈 Interpretação dos Dados

### Métricas de Forma

| Métrica | Intervalo | Interpretação |
|---------|-----------|----------------|
| **area_px** | 0-∞ | Tamanho da planta (maior = maior) |
| **perimeter_px** | 0-∞ | Perímetro (maior = mais complexo) |
| **solidity** | 0-1 | Compactação (1 = convexo, <1 = concavo) |
| **circularity** | 0-1 | Formato (1 = círculo, <1 = alongado) |
| **aspect_ratio** | 0-∞ | Proporção L/A (1 = quadrado, >1 = alta) |

### Métricas de Cor (HSV)

| Métrica | Intervalo | Interpretação |
|---------|-----------|----------------|
| **hue_mean** | 0-179 | Cor predominante (verde = 25-90) |
| **sat_mean** | 0-255 | Saturação (vibrância) ← **Saúde!** |
| **val_mean** | 0-255 | Brilho (luminância) |

**Importante**: `sat_mean` é um **indicador de saúde**:
- Alta saturação = planta saudável, cores vibrantes
- Baixa saturação = possível estresse, cores pálidas

---

## 🧪 Como Reproduzir os Exemplos

1. **Primeira captura**:
   ```bash
   python main.py
   # Iniciar sessão > Capturar Agora
   ```

2. **Ver JSON gerado**:
   ```bash
   cat data/results/Tomate_01/output_*.json
   ```

3. **Ver CSV consolidado**:
   ```bash
   cat data/results/index/results.csv
   ```

4. **Analisar em Python**:
   ```python
   import pandas as pd
   import json
   
   # CSV
   df = pd.read_csv("data/results/index/results.csv")
   print(df.describe())
   
   # JSON
   with open("data/results/Tomate_01/output_*.json") as f:
       data = json.load(f)
   ```

---

## 🔍 Detalhes Técnicos

### Timestamps
- **Formato**: ISO 8601 (`YYYYMMDD_HHMMSS`)
- **Timezone**: Local machine (sem especificação)
- **Precisão**: Segundo (evita colisões em mesma câmera)

### Nomes de Arquivo
- **Imagem**: `<nome_planta>_<timestamp>_cam<X>.jpg`
  - Exemplo: `Tomate_01_20250115_143245_cam0.jpg`
- **JSON**: `output_<timestamp>_cam<X>.json`
- **Máscara**: `<nome_planta>_<timestamp>_cam<X>_mask.png`

### Rastreabilidade
- Cada captura tem timestamp único
- Histórico completo em CSV (nunca deleta)
- Imagens original + máscara salvas
- JSON descritivo com contexto

---

## 📊 Exemplo de Análise

### Comparar 2 Genótipos

```python
import pandas as pd

# Carregar dados
df = pd.read_csv("data/results/index/results.csv")
df["timestamp"] = pd.to_datetime(df["timestamp"])
df["date"] = df["timestamp"].dt.date

# Resumo por genótipo
summary = df.groupby("genotype").agg({
    "area_px": ["mean", "std", "count"],
    "sat_mean": ["mean", "std"]
})

print(summary)
# Output:
#              area_px                    sat_mean
#               mean std count              mean  std
# genotype
# mutante_A  40000 1500 8         143.5  2.1
# WT         47000 2000 8         148.2  1.8

# WT é maior (47k vs 40k) e mais saudável (sat mais alta)
```

### Calcular Crescimento por Dia

```python
# Agrupar por data e calcular área média
daily = df.groupby(["genotype", "date"])["area_px"].mean().reset_index()

# Calcular delta
daily["delta_area"] = daily.groupby("genotype")["area_px"].diff()

print(daily)
# delta_area > 0 = crescimento
# delta_area < 0 = decréscimo (stress?)
```

---

**Usando estes exemplos como guia, você pode criar suas próprias análises!**

Para mais informações, vide [README.md](../README.md§Análises).

# 🚀 PRÓXIMOS PASSOS - Pranta MVP

## ✅ Seu Projeto Está Pronto!

O Pranta MVP foi completamente implementado e está pronto para uso.

---

## 📋 Passo-a-Passo para Começar

### Passo 1: Abra o Terminal (1 min)
```powershell
# Abra PowerShell como Admin
cd "C:\Users\adm_luca.goulart\Desktop\Pranta"
```

### Passo 2: Criar Ambiente Virtual (1 min)
```powershell
python -m venv venv
.\venv\Scripts\activate
```

### Passo 3: Instalar Dependências (2 min)
```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

### Passo 4: Validar Instalação (1 min)
```powershell
python validate_installation.py
```

Se tudo OK, você verá:
```
✅ TODOS OS TESTES PASSARAM (14/14)
```

### Passo 5: Testar Sem Câmera (1 min)
```powershell
python test_without_camera.py
```

Se funcionar:
```
✅ TODOS OS TESTES PASSARAM
A aplicação está pronta para usar.
```

### Passo 6: Conecte Câmeras USB (1 min)
- Conecte 1 ou 2 câmeras USB
- Verifique se Windows as detecta (Windows Camera app)

### Passo 7: Execute Aplicação (∞ min)
```powershell
python main.py
```

A janela se abrirá. Agora:
1. Preencha: Nome da Planta, Genótipo
2. Selecione câmeras
3. Clique "Iniciar Sessão"
4. Clique "Capturar Agora"
5. Visualize resultados nas abas

---

## 📚 Documentação Recomendada

Leia nesta ordem:

1. **[QUICKSTART.md](QUICKSTART.md)** (5 min)
   - Guia rápido de início

2. **[README.md](README.md)** (20 min)
   - Documentação completa
   - Info técnica do pipeline
   - Troubleshooting

3. **[CHECKLIST_ACEITE.md](CHECKLIST_ACEITE.md)** (30 min)
   - Validação manual do sistema
   - Teste passo a passo

---

## 🎯 Funcionalidades para Testar

### ✅ Teste 1: Captura Básica
1. Execute `python main.py`
2. Preencha: Tomate_01, WT, câmera 0
3. "Iniciar Sessão"
4. "Capturar Agora"
5. Status muda para verde (sucesso)

### ✅ Teste 2: Verificar Arquivos
1. Abra `data/raw/Tomate_01/` (imagem salva)
2. Abra `data/results/Tomate_01/` (JSON)
3. Abra `data/results/index/results.csv` (no Excel)

### ✅ Teste 3: Visualizações
1. Clique aba "Comparação" (tabela com dados)
2. Clique aba "ΔArea/dia" (pode estar vazio - precisa 2+ dias)
3. Clique aba "Saturação" (gráfico de saúde)

### ✅ Teste 4: 2 Câmeras
1. Selecione câmeras 0 e 1
2. "Capturar Agora"
3. Verá 2 imagens em `data/raw/Tomate_01/`
4. 2 linhas no CSV (cam0 e cam1)

---

## 📊 Verificação de Arquivos Importantes

Após primeira captura, você deve ter:

```
✅ Imagem: data/raw/<planta>/<planta>_YYYYMMDD_HHMMSS_cam0.jpg
✅ JSON:   data/results/<planta>/output_YYYYMMDD_HHMMSS_cam0.json
✅ CSV:    data/results/index/results.csv (com 1 linha de dados)
✅ Log:    logs/pranta.log (com eventos)
```

---

## 🔧 Personalização

### Ajustar Thresholds HSV (Segmentação)

Se planta não é segmentada corretamente:

1. Abra `config.py`
2. Encontre `PROCESSING_CONFIG`
3. Ajuste valores:
   ```python
   PROCESSING_CONFIG = ProcessingConfig(
       hue_min=25,     # ← Verde mínimo, ajuste conforme sua planta
       hue_max=90,     # ← Verde máximo
       sat_min=20,     # ← Saturação mínima
       val_min=40,     # ← Brilho mínimo
   )
   ```
4. Reinicie `python main.py`

### Aumentar Resolução de Câmera

Em `config.py`:
```python
CAMERA_CONFIG = {
    "width": 1280,   # ← Aumentar de 640
    "height": 960,   # ← Aumentar de 480
    "fps": 30,
}
```

---

## 🐛 Se Algo der Errado

### "Nenhuma câmera USB detectada"
```
1. Desconecte e reconecte câmera
2. Teste com Windows Camera app
3. Atualize drivers da câmera
```

### "Erro ao conectar câmera"
```
1. Só pode conectar 1-2 câmeras simultaneamente
2. Teste com 1 câmera primeiro
3. Se erro persistir, verifique logs/pranta.log
```

### "Nada é segmentado (sem contorno)"
```
1. Máscara vazia em data/processed/
2. Pode ser iluminação fraca
3. Ajuste thresholds HSV em config.py
4. Teste com background mais simples
```

### "Gráficos vazios após captura"
```
1. Captura precisa estar OK (status verde)
2. Clique "Atualizar Gráfico" na aba
3. ΔArea precisa de 2+ dias de dados
4. Verifique data/results/index/results.csv
```

---

## 📈 Se Tudo Funcionar

Você pode agora:

1. **Capturar múltiplas plantas** com genótipos diferentes
2. **Comparar genótipos** em tempo real
3. **Acompanhar crescimento** dia após dia
4. **Exportar dados** em CSV para análise externa
5. **Ajustar pipeline** conforme necessário

---

## 🎓 Para Ser um Expert

Estude estes arquivos:

### Usuário
- README.md (20 min)
- examples/README.md (10 min)

### Desenvolvedor
- app/processing/pipeline.py (algoritmo)
- app/ui/main_window.py (interface PyQt5)
- DEVELOPMENT.md (arquitetura)

### Pesquisador
- examples/output_example.json (format o de dados)
- examples/results_example.csv (análise em Excel/Python)

---

## 💡 Ideias para Expansão

Veja [DEVELOPMENT.md](DEVELOPMENT.md) para:
- Agendamento automático
- Preview em tempo real
- Edição de thresholds na UI
- Exportação de gráficos
- Análises avançadas (ANOVA, predição)
- API REST
- Web dashboard

---

## 📞 Suporte Final

| Problema | Solução |
|----------|---------|
| Erro de importação | `python validate_installation.py` |
| Câmera não funciona | `README.md§Troubleshooting` |
| Segmentação ruim | Ajuste thresholds em `config.py` |
| Dúvida técnica | Leia `DEVELOPMENT.md` |
| Exemplo de dados | Veja `examples/README.md` |

---

## ✨ Resumo

✅ **Pranta está 100% funcional**

Você tem:
- ✅ Interface intuitiva em português
- ✅ Captura de 1-2 câmeras USB
- ✅ Pipeline robusto de análise
- ✅ Persistência confiável (JSON, CSV)
- ✅ Visualizações em tempo real
- ✅ Documentação completa
- ✅ Código manutenível e extensível

**Comece agora**: `python main.py`

---

**Boa sorte com sua fenotipagem de plantas! 🌱📊**

Qualquer dúvida, releia [INDEX.md](INDEX.md) para navegar toda documentação.

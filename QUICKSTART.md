# 🚀 Quick Start - Pranta MVP

## ⚡ 5 Minutos para Começar

### 1️⃣ Preparação (1 min)

```bash
# Abra CMD/PowerShell na pasta Pranta
cd C:\Users\adm_luca.goulart\Desktop\Pranta

# Crie ambiente virtual
python -m venv venv

# Ative
.\venv\Scripts\activate
```

### 2️⃣ Instalação (2 min)

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3️⃣ Validação (1 min)

```bash
# Teste instalação sem câmera
python test_without_camera.py

# Se OK, deve exibir ✅ TODOS OS TESTES PASSARAM
```

### 4️⃣ Execução (1 min)

```bash
# Conecte 1-2 câmeras USB
# Execute aplicação
python main.py
```

---

## 📸 Uso Básico

1. **Preencha o formulário**:
   - Nome da Planta (ex: "Tomate_01")
   - Genótipo (ex: "WT")
   - Selecione câmeras

2. **Clique "Iniciar Sessão"**

3. **Clique "Capturar Agora"**
   - Status muda para laranja (processando)
   - Volta verde (sucesso)

4. **Visualize resultados** nas abas:
   - Comparação (tabela)
   - ΔArea/dia (gráfico)
   - Saturação (gráfico)

---

## 🔧 Arquivos Importantes

| Arquivo | Descrição |
|---------|-----------|
| README.md | Documentação completa |
| config.py | Thresholds HSV (customizável) |
| main.py | Ponto de entrada |
| logs/pranta.log | Histórico de execução |
| data/results/index/results.csv | Dados consolidados |

---

## 🆘 Problema?

1. **Sem câmera detectada?**
   - Reconecte câmera
   - Teste com Windows Camera
   - Atualize drivers

2. **Aplicação trava?**
   - Verifique `logs/pranta.log`
   - Execute com admin
   - Reinstale PyQt5

3. **Sem dados nos gráficos?**
   - Capture pelo menos 1 imagem
   - Clique "Atualizar Gráfico"
   - ΔArea precisa de 2+ dias de dados

4. **Segmentação não funciona?**
   - Mude iluminação
   - Ajuste thresholds em `config.py`
   - Verifique máscara em `data/processed/`

---

## 📚 Próximos Passos

- Leia [README.md](README.md) para documentação completa
- Leia [CHECKLIST_ACEITE.md](CHECKLIST_ACEITE.md) para validação funcional
- Leia [DEVELOPMENT.md](DEVELOPMENT.md) para evolução futura

---

**Happy phenotyping! 🌱📊**

# 🎯 COMECE AQUI - Pranta MVP

## ⚡ 5 Minutos para Começar

Não sabe por onde começar? Este arquivo é para você!

---

## 🚀 Setup Rápido (Copie & Cole)

### 1. Abra PowerShell
```powershell
cd C:\Users\adm_luca.goulart\Desktop\Pranta
```

### 2. Crie ambiente
```powershell
python -m venv venv
.\venv\Scripts\activate
```

### 3. Instale tudo
```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Teste instalação
```powershell
python validate_installation.py
```

### 5. Execute!
```powershell
python main.py
```

**Pronto! Conecte câmera USB e divirta-se!**

---

## ✅ O Que Fazer na Interface

1. **Nome da Planta**: `Tomate_01` (ex: seu nome + número)
2. **Genótipo**: `WT` (ex: tipo/controle)
3. **Câmeras**: Marque 1 ou 2
4. **Clique**: "Iniciar Sessão"
5. **Clique**: "Capturar Agora"
6. **Visualize**: Abas de gráficos

---

## 📚 Leitura Recomendada

| Tempo | Arquivo | Motivo |
|--------|---------|--------|
| 5 min | [QUICKSTART.md](QUICKSTART.md) | Guia super rápido |
| 20 min | [README.md](README.md) | Documentação completa |
| 30 min | [CHECKLIST_ACEITE.md](CHECKLIST_ACEITE.md) | Validar tudo |

**Primeira vez?** Leia [PRÓXIMOS_PASSOS.md](PRÓXIMOS_PASSOS.md) para step-by-step completo.

---

## 🆘 Problema?

| Erro | Solução |
|------|---------|
| Não instala | `python validate_installation.py` |
| Sem câmera | Reconecte USB |
| Não funciona | Leia `README.md§Troubleshooting` |

---

## 📊 Exemplos

Os dados serão salvos aqui:
- **Imagens**: `data/raw/<seu_nome>/`
- **Análises**: `data/results/index/results.csv`
- **Logs**: `logs/pranta.log`

Você pode ver exemplos em `examples/` primeiro!

---

## 🎉 Pronto para Começar?

```powershell
python main.py
```

**Clique em "Iniciar Sessão" e boa diversão!**

---

**Para documentação completa**, veja [INDEX.md](INDEX.md)

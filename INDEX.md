# 📚 Index - Documentação Pranta MVP

## 🎯 Comece Aqui

**Não sabe por onde começar?** Siga este guia:

1. **Novo usuário?** → Leia [QUICKSTART.md](QUICKSTART.md) (5 min)
2. **Desenvolvedor?** → Leia [README.md](README.md) (20 min)
3. **Contribuidor?** → Leia [DEVELOPMENT.md](DEVELOPMENT.md) (15 min)
4. **Validação?** → Execute [CHECKLIST_ACEITE.md](CHECKLIST_ACEITE.md) (30 min)

---

## 📖 Documentação por Tópico

### 🚀 Instalação & Setup
- [QUICKSTART.md](QUICKSTART.md) - Início rápido (5 min)
- [README.md§Instalação](README.md#instalação) - Passo a passo detalhado
- [validate_installation.py](validate_installation.py) - Script de validação

### 📖 Usar a Aplicação
- [README.md§Execução](README.md#execução) - Como rodar
- [README.md§Fluxo de Uso](README.md#fluxo-de-uso) - Passo a passo do usuário
- [QUICKSTART.md§Uso Básico](QUICKSTART.md#-uso-básico) - Versão curta

### 🔧 Técnico
- [README.md§Pipeline](README.md#pipeline-de-processamento) - Detalhes do algoritmo
- [README.md§Formatos](README.md#-formatos-de-saída) - Estruturas de dado (JSON, CSV)
- [config.py](config.py) - Configuração centralizada
- [DEVELOPMENT.md](DEVELOPMENT.md) - Arquitetura & padrões

### 📊 Análise
- [README.md§Análises](README.md#-análises-disponíveis) - Descrição de cada gráfico
- [examples/output_example.json](examples/output_example.json) - Exemplo JSON
- [examples/results_example.csv](examples/results_example.csv) - Exemplo CSV

### 🧪 Testes
- [CHECKLIST_ACEITE.md](CHECKLIST_ACEITE.md) - Validação funcional completa
- [test_without_camera.py](test_without_camera.py) - Teste sem câmera
- [validate_installation.py](validate_installation.py) - Validação de dependências

### 🐛 Troubleshooting
- [README.md§Troubleshooting](README.md#-troubleshooting) - Problemas & soluções
- [QUICKSTART.md§Problema?](QUICKSTART.md#-problema) - FAQ rápido

### 🎓 Evolução Futura
- [DEVELOPMENT.md§Próximas Fases](DEVELOPMENT.md#-ideias-para-próximas-fases) - Roadmap
- [DEVELOPMENT.md§Refactoring](DEVELOPMENT.md#-mejoras-de-código) - Sugestões técnicas

---

## 📁 Estrutura de Arquivos

### Raiz do Projeto
```
Pranta/
├── main.py                       # Ponto de entrada
├── config.py                     # Configuração centralizada
├── requirements.txt              # Dependências
├── .gitignore                    # Exclusões git
│
├── 📚 DOCUMENTAÇÃO
│   ├── INDEX.md                  # Este arquivo (mapa de navegação)
│   ├── README.md                 # Documentação completa
│   ├── QUICKSTART.md             # Início rápido
│   ├── SUMMARY.md                # Resumo de entrega
│   ├── CHECKLIST_ACEITE.md       # Validação funcional
│   ├── DEVELOPMENT.md            # Arquitetura & futuro
│   └── (este arquivo)
│
├── 🧪 TESTES & VALIDAÇÃO
│   ├── validate_installation.py  # Validação de dependências
│   └── test_without_camera.py    # Teste sem câmera
│
├── 📂 CÓDIGO-FONTE
│   └── app/
│       ├── capture/              # Gerenciamento de câmeras
│       │   ├── __init__.py
│       │   └── camera_manager.py (189 linhas)
│       ├── processing/           # Pipeline de análise
│       │   ├── __init__.py
│       │   └── pipeline.py (323 linhas)
│       ├── data/                 # Persistência
│       │   ├── __init__.py
│       │   └── storage.py (270 linhas)
│       ├── analytics/            # Análises consolidadas
│       │   ├── __init__.py
│       │   └── metrics.py (220 linhas)
│       └── ui/                   # Interface PyQt5
│           ├── __init__.py
│           └── main_window.py (580 linhas)
│
├── 📊 EXEMPLOS DE DADOS
│   └── examples/
│       ├── output_example.json   # JSON com métricas
│       └── results_example.csv   # CSV consolidado
│
├── 📦 DADOS (Gerados em Runtime)
│   └── data/
│       ├── raw/                  # Imagens capturadas
│       ├── processed/            # Máscaras segmentadas
│       ├── results/              # JSONs de saída
│       └── results/index/        # CSV consolidado
│
└── 📝 LOGS (Gerados em Runtime)
    └── logs/
        └── pranta.log            # Histórico de execução
```

---

## 💡 Guias Rápidos

### Para Iniciante (Sem Conhecimento Técnico)
1. Leia [QUICKSTART.md](QUICKSTART.md)
2. Execute `python main.py`
3. Siga instruções na interface
4. Se tiver problema, leia [QUICKSTART.md§Problema?](QUICKSTART.md#-problema)

### Para Desenvolvedor Python
1. Leia [README.md](README.md)
2. Estude `app/processing/pipeline.py` (onde acontece a mágica)
3. Estude `app/ui/main_window.py` (interface PyQt5 com threading)
4. Leia [DEVELOPMENT.md](DEVELOPMENT.md) para ideias de melhoria

### Para Pesquisador
1. Leia [README.md§Pipeline](README.md#pipeline-de-processamento) (detalhes do algoritmo)
2. Estude [examples/output_example.json](examples/output_example.json) (métricas)
3. Estude [examples/results_example.csv](examples/results_example.csv) (dados consolidados)
4. Use CSV com Excel/R/Python para suas próprias análises

### Para Contribuidor
1. Execute [validate_installation.py](validate_installation.py) (validar setup)
2. Execute [test_without_camera.py](test_without_camera.py) (teste sem câmera)
3. Leia [DEVELOPMENT.md](DEVELOPMENT.md) (padrões & ideias)
4. Faça contribuições focadas em 1 feature

---

## 🎯 Objetivos Atingidos

✅ **MVP Completo**
- Captura de 1-2 câmeras USB
- Pipeline RGB→HSV com segmentação
- Extração de 11 métricas (forma + cor)
- Persistência (imagem, JSON, CSV)
- Análises (ΔArea/dia, Saturação, Comparação)
- UI responsiva em português
- Documentação completa
- Testes de validação

✅ **Qualidade**
- Código tipado (type hints)
- Modular & manutenível
- Logging centralizado
- Tratamento robusto de erros
- Threading (sem travamentos)
- ~1.900 linhas bem organizadas

---

## 🆘 FAQ Rápido

**P: Por onde começo?**
A: Leia [QUICKSTART.md](QUICKSTART.md) - 5 minutos!

**P: Como instalo?**
A: `python -m venv venv` → `pip install -r requirements.txt`

**P: Como executo?**
A: `python main.py`

**P: Não tenho câmera, posso testar?**
A: Sim! `python test_without_camera.py`

**P: Como mudo os thresholds HSV?**
A: Edite `config.py` ou `app/processing/pipeline.py`

**P: Onde são salvos meus dados?**
A: Em `data/raw/`, `data/processed/`, `data/results/`

**P: Como exporto os gráficos?**
A: Atualmente, tire screenshot. Futura: botão de exportação PNG/PDF

**P: Posso adicionar mais câmeras que 2?**
A: Atualmente máx 2. Veja [DEVELOPMENT.md](DEVELOPMENT.md) para futura expansão

---

## 📞 Contato & Suporte

1. **Erro de importação?** → Execute `python validate_installation.py`
2. **Câmera não funciona?** → Veja [README.md§Troubleshooting](README.md#-troubleshooting)
3. **Segmentação ruim?** → Ajuste thresholds em `config.py`
4. **Dúvida técnica?** → Leia [DEVELOPMENT.md](DEVELOPMENT.md)

---

## 📚 Referências

- [OpenCV Docs](https://docs.opencv.org/)
- [PyQt5 Docs](https://www.riverbankcomputing.com/static/Docs/PyQt5/)
- [PlantCV Docs](https://plantcv.readthedocs.io/)
- [Pandas User Guide](https://pandas.pydata.org/docs/)

---

**Última atualização**: Janeiro 2025  
**Versão**: 1.0.0 - MVP  
**Status**: ✅ Production Ready

---

## 🗺️ Roadmap de Leitura Recomendado

```
                    ┌──────────────┐
                    │  Este Index  │
                    └────────┬─────┘
                             │
                    ┌────────▼────────┐
                    │  QUICKSTART.md  │ 5 min
                    └────────┬────────┘
                             │
            ┌────────────────┼────────────────┐
            │                │                │
      ┌─────▼──────┐  ┌──────▼────────┐  ┌───▼──────────┐
      │ README.md  │  │ DEVELOPMENT.md│  │   Código   │
      │ 20 min     │  │  15 min       │  │   Fonte    │
      └────────────┘  └───────────────┘  └────────────┘
            │                │                │
            └────┬───────────┼────────────────┘
                 │           │
            ┌────▼───────────▼──────┐
            │  CHECKLIST_ACEITE.md  │ 30 min
            │  (Validação Funcional)│
            └───────────────────────┘
```

---

**Agora, escolha seu caminho e comece! 🚀**

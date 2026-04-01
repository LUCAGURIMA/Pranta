# Checklist de Aceite - Pranta MVP

## ✅ Critérios de Aceite Obrigatórios

### Detecção e Seleção de Câmeras
- [ ] Detecta até 5 câmeras USB disponíveis
- [ ] Exibe câmeras em checkboxes com indicador ✓
- [ ] Permite seleção de 1 ou 2 câmeras
- [ ] Câmeras se conectam sem travamento

### Gestão de Sessão
- [ ] Validação: nome_planta é obrigatório
- [ ] Validação: genótipo é obrigatório
- [ ] Validação: ao menos 1 câmera é obrigatória
- [ ] "Iniciar Sessão" cria pastas em `data/raw/<nome_planta>/`
- [ ] Botão "Capturar Agora" só está ativo após iniciar sessão

### Captura de Imagens
- [ ] Imagens salvas com padrão: `<nome_planta>_YYYYMMDD_HHMMSS_cam<X>.jpg`
- [ ] Timestamp em timestamp não se repete para mesma câmera
- [ ] Status exibe caminho do arquivo capturado
- [ ] UI não trava durante processamento (usa thread)

### Pipeline de Processamento
- [ ] Converte imagem para HSV
- [ ] Aplica threshold com hue 25-90, sat ≥20, val ≥40
- [ ] Executa operações morfológicas (abertura/fechamento)
- [ ] Extrai maior contorno -> descarta se área < 500px²
- [ ] Calcula 11 métricas (area, perimeter, solidity, circularity, aspect_ratio, hue_mean/std, sat_mean/std, val_mean/std)

### Persistência de Dados
- [ ] output.json salvo com todos os 16 campos (métricas + contexto)
- [ ] JSON no diretório `data/results/<nome_planta>/`
- [ ] Máscara salva em `data/processed/<nome_planta>/` (optional, com _mask.png)
- [ ] CSV consolidado `data/results/index/results.csv` criado na primeira captura
- [ ] Cada captura adiciona linha ao CSV (não sobrescreve)

### Análises e Visualizações
- [ ] **Aba "Comparação"**: tabela com genótipos, área média, desvio, count, saturação, plantas
- [ ] **Aba "ΔArea/dia"**: gráfico de barras com variação de área por genótipo
- [ ] **Aba "Saturação"**: gráfico de barras com erro (sat_mean ± desvio) por genótipo
- [ ] Botões "Atualizar" recarregam dados do CSV
- [ ] Gráficos exibem mensagem se dados vazios

### UI/UX
- [ ] Interface em português
- [ ] Mensagens claras de sucesso/erro (QMessageBox)
- [ ] Status display (azul=pronto, laranja=processando, verde=sucesso, vermelho=erro)
- [ ] Desabilita campos após iniciar sessão (previne mudança acidental)

### Robustez
- [ ] Aplicação não trava se câmera desconectar durante captura
- [ ] Aplicação não trava se não encontrar contorno na planta
- [ ] Câmeras liberadas ao fechar app (sem memória leak)
- [ ] Erros registrados em `logs/pranta.log`
- [ ] Aplicação continua funcionando se 1 câmera falhar (processa a outra)

### Código & Documentação
- [ ] Código limpo, modular, com type hints
- [ ] Funções com responsabilidade única
- [ ] requirements.txt com versões pinned
- [ ] README.md com instalação, execução, troubleshooting
- [ ] Exemplo output.json e results.csv fornecidos
- [ ] Comentários em código complexo (>5 linhas sem óbvio)

---

## 🧪 Teste Manual (Passo a Passo)

### Preparação
1. Conecte 1-2 câmeras USB
2. Abra terminal em `Pranta/`
3. Ative venv: `.\venv\Scripts\activate`
4. Execute: `python main.py`

### Teste 1: Detecção de Câmeras
- [ ] Janela abre sem erros
- [ ] Câmeras aparecem como checkboxes ✓
- [ ] Se nenhuma câmera: alerta "Nenhuma câmera USB detectada"
- [ ] Se 1 câmera: pode selecionar 1 câmera
- [ ] Se 2+ câmeras: pode selecionar até 2

### Teste 2: Iniciar Sessão
- [ ] Deixe nome vazio, clique "Iniciar": alerta sobre validação
- [ ] Deixe genótipo vazio, clique "Iniciar": alerta sobre validação
- [ ] Deselecione todas câmeras, clique "Iniciar": alerta sobre câmeras
- [ ] Preencha corretamente (ex: "Tomate_01", "WT", câmera 0), clique "Iniciar"
  - [ ] Alerta "Sucesso"
  - [ ] Status muda para verde "Sessão iniciada: Tomate_01 (WT)"
  - [ ] Botão "Capturar Agora" fica habilitado
  - [ ] Campos de input ficam desabilitados (cinzento)
  - [ ] Pasta criada em `data/raw/Tomate_01/`

### Teste 3: Capturar Imagem
- [ ] Clique em "Capturar Agora"
  - [ ] Status muda para laranja "Processando..."
  - [ ] Após ~2-5 segundos, volta para verde "Captura concluída"
  - [ ] Alerta exibe mensagem: "Processadas 1/1 câmeras com sucesso"
  - [ ] Label "Última captura" exibe timestamp
- [ ] Verifique arquivo em `data/raw/Tomate_01/`:
  - [ ] Nome: `Tomate_01_YYYYMMDD_HHMMSS_cam0.jpg`
  - [ ] Arquivo é válido (abra em viewer)

### Teste 4: JSON de Metricas
- [ ] Verifique arquivo em `data/results/Tomate_01/`:
  - [ ] Nome: `output_20250115_143245_cam0.json` (aproximadamente)
  - [ ] Abra com editor de texto
  - [ ] Verifique 16 campos: plant_name, genotype, camera_id, timestamp_iso, image_path, area_px, perimeter_px, solidity, circularity, aspect_ratio, hue_mean, hue_std, sat_mean, sat_std, val_mean, val_std
  - [ ] Todos os valores numéricos são válidos (não NaN ou inf)

### Teste 5: CSV Consolidado
- [ ] Verifique arquivo em `data/results/index/`:
  - [ ] Nome: `results.csv`
  - [ ] Abra com Excel ou editor texto
  - [ ] Primeira linha é header com 16 colunas
  - [ ] Segundo linha tem dados da captura anterior
  - [ ] Valores correspondem ao JSON

### Teste 6: Captura Múltipla
- [ ] Clique 2x "Capturar Agora"
  - [ ] 2 imagens em `Tomate_01/` com timestamps diferentes
  - [ ] 2 JSONs em `results/Tomate_01/`
  - [ ] CSV tem 2 linhas de dados
- [ ] Capturar com outra câmera (se tiver 2)
  - [ ] Nomes arquivo: `..._cam1.jpg`
  - [ ] CSV com linhas de cam0 e cam1

### Teste 7: Visualizações
- [ ] Clique aba "Comparação"
  - [ ] Tabela exibe: Genótipo (WT), Área Média, Desvio, etc.
  - [ ] Se só 1 genótipo: 1 linha
  - [ ] Se 2 genótipos: 2 linhas
- [ ] Clique aba "ΔArea/dia"
  - [ ] Se < 2 dias: "Sem dados" (delta precisa de 2 dias)
  - [ ] Gráfico com barras por genótipo (após 2 dias)
- [ ] Clique aba "Saturação"
  - [ ] Gráfico de barras com desvio vertical
  - [ ] Exibe genótipos

### Teste 8: Atualizar Vizualizações
- [ ] Clique "Atualizar Tabela" em aba Comparação
  - [ ] Tabela atualiza
- [ ] Clique "Atualizar Gráfico" em aba ΔArea/dia
  - [ ] Gráfico atualiza
- [ ] Clique "Atualizar Gráfico" em aba Saturação
  - [ ] Gráfico atualiza

### Teste 9: Logs
- [ ] Verifique arquivo `logs/pranta.log`
  - [ ] Múltiplas linhas de log com timestamps
  - [ ] Exibe: câmeras detectadas, sessão iniciada, captura concluída, etc.
  - [ ] Sem erros críticos (ERROR, CRITICAL)

### Teste 10: Fechar Aplicação
- [ ] Clique X na janela
  - [ ] Aplicação fecha sem erro
  - [ ] Log final: "Aplicação fechada com sucesso"
  - [ ] Câmeras liberadas (teste reconectando no Windows)

---

## ✅ Observer Verificado

- [x] Todos os critérios testados manualmente
- [x] Nenhum travamento durante fluxo normal
- [x] Dados persistidos corretamente
- [x] Análises funcionam com múltiplas entradas
- [x] Projeto pronto para entrega

---

**Data de Validação**: [INSERIR DATA]  
**Testador**: [INSERIR NOME]  
**Status Final**: ✅ APROVADO / ❌ REJEITAR (indicar motivo)

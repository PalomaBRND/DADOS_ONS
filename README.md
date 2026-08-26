# Dashboard ONS — Carga e Geração

Dashboard analítico desenvolvido em **Python + Streamlit** para exploração histórica de dados de **Carga e Geração do Sistema Interligado Nacional (SIN)** a partir de dados públicos do **Operador Nacional do Sistema Elétrico (ONS)**.

O projeto combina um **pipeline de atualização de dados**, um **dashboard interativo** e um **notebook de análise exploratória**, permitindo trabalhar com séries históricas de carga, geração por fonte e intercâmbio.

---

## 📌 Visão geral

A solução foi estruturada em três etapas:

```text
Dados públicos do ONS
        ↓
    pipeline.py
        ↓
Consolidação e padronização
        ↓
balanco_energia_ons.parquet
        ↓
    dashboard.py
        ↓
      Streamlit
```

O dashboard foi desenvolvido com inspiração na página **Carga e Geração** do ONS, mas acrescenta recursos de análise histórica e comparação.

---

## 🎯 Objetivo

O projeto transforma a base histórica de balanço energético em uma ferramenta de exploração visual para responder perguntas como:

- Como a carga se comportou em determinado dia?
- Qual foi o pico e o mínimo de carga?
- Como dois ou mais dias se comportaram?
- Como dois períodos históricos se comportaram?
- Como a carga varia ao longo das horas?
- Como diferentes subsistemas se comportam?
- Qual foi a participação de cada fonte de geração?
- Como hidráulica, térmica, eólica e solar variam ao longo do período?
- Como o intercâmbio se comportou?

Além do dashboard, o projeto possui um notebook específico para a análise dos jogos do Brasil nas Copas do Mundo de 2014 e 2026.

---

# 🏗️ Estrutura do projeto

```text
DADOS_ONS/
│
├── dashboard.py
├── pipeline.py
├── analise_copa_nova.ipynb
├── requirements.txt
├── README.md
└── .gitignore
```

### `dashboard.py`

Aplicação principal desenvolvida em Streamlit.

Responsável por:

- leitura da base consolidada;
- filtros interativos;
- seleção de subsistemas;
- seleção de fontes de geração;
- seleção de dias e períodos;
- seleção de horários;
- cálculo dos indicadores;
- geração dos gráficos;
- comparação entre recortes históricos.

### `pipeline.py`

Processo responsável por baixar os dados públicos do ONS e consolidar os arquivos anuais em uma única base Parquet.

O pipeline atualmente percorre os anos configurados, faz a leitura dos arquivos anuais, converte as colunas numéricas e consolida os dados em:

```text
balanco_energia_ons.parquet
```

### `analise_copa_nova.ipynb`

Notebook utilizado para a análise exploratória das partidas do Brasil nas Copas do Mundo de 2014 e 2026.

Entre as análises estão:

- carga média nos horários dos jogos;
- carga observada versus carga de referência;
- composição média da geração;
- comparação 2014 × 2026;
- variação da carga por jogo;
- conclusões e limitações metodológicas.

### `requirements.txt`

Lista de bibliotecas necessárias para executar o projeto.

### `.gitignore`

Evita o versionamento de arquivos locais e arquivos de dados grandes, como:

```text
*.parquet
```

O arquivo `balanco_energia_ons.parquet` é **gerado localmente pelo pipeline** e não precisa ser armazenado no GitHub.

---

# 🧰 Tecnologias e bibliotecas

## Python

Linguagem principal utilizada no projeto.

## Pandas

Utilizado para:

- leitura e transformação dos dados;
- filtros;
- agrupamentos;
- cálculos estatísticos;
- manipulação de séries temporais.

## PyArrow

Utilizado para leitura e escrita do formato **Parquet**.

## Streamlit

Utilizado para construção do dashboard interativo.

## Plotly

Utilizado para criação dos gráficos interativos.

## NumPy

Utilizado nas operações numéricas e no tratamento de valores ausentes das análises.

## Matplotlib

Utilizado no notebook de análise exploratória.

## Jupyter / Notebook

Utilizado para desenvolvimento e execução da análise exploratória.

---

# ⚙️ Instalação

## 1. Clonar o repositório

```bash
git clone https://github.com/PalomaBRND/DADOS_ONS.git
```

Entrar na pasta:

```bash
cd DADOS_ONS
```

---

## 2. Criar um ambiente virtual

### Windows

```bash
python -m venv .venv
```

Ativar:

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv .venv
```

Ativar:

```bash
source .venv/bin/activate
```

---

## 3. Instalar as dependências

```bash
python -m pip install -r requirements.txt
```

---

# 🔄 Atualização dos dados

O arquivo `balanco_energia_ons.parquet` não precisa ser baixado manualmente.

O projeto possui um pipeline para reconstruí-lo a partir dos dados públicos do ONS.

Execute:

```bash
python pipeline.py
```

O processo:

1. acessa os arquivos anuais publicados pelo ONS;
2. baixa os dados;
3. padroniza as colunas numéricas;
4. consolida os anos em um único DataFrame;
5. grava o resultado em:

```text
balanco_energia_ons.parquet
```

Após a execução, esse arquivo estará disponível localmente na mesma pasta do projeto.

> **Observação:** o tempo de execução depende da quantidade de anos processados e da velocidade da conexão com a internet.

---

# ▶️ Executando o dashboard

Depois de gerar a base, execute:

```bash
python -m streamlit run dashboard.py
```

O Streamlit disponibilizará uma URL local, normalmente:

```text
http://localhost:8501
```

Abra o endereço no navegador.

---

# 📊 Funcionalidades do dashboard

## Subsistemas

É possível selecionar um ou vários subsistemas, incluindo:

- NORTE
- NORDESTE
- SUL
- SUDESTE/CENTRO-OESTE
- SISTEMA INTERLIGADO NACIONAL

Quando mais de um subsistema é selecionado, os gráficos permitem visualizar as séries separadamente.

---

## Modo DIA

Permite analisar um dia específico.

A primeira data é exibida por padrão e o botão `+` permite adicionar outros dias para comparação, com limite de até **7 dias**.

Exemplo:

```text
25/08/2026
24/08/2026
23/08/2026
```

---

## Modo PERÍODO

Permite analisar um intervalo de datas.

Exemplo:

```text
21/08/2026 a 23/08/2026
```

O botão `+` permite adicionar um segundo período para comparação.

Exemplo:

```text
Período 1: 21/08/2026 a 23/08/2026
Período 2: 14/08/2026 a 16/08/2026
```

---

# 🕒 Filtro de horário

## HORA

Permite analisar uma hora específica.

Exemplo:

```text
08:00
```

O botão `+` permite adicionar outros horários para comparação.

---

## INTERVALO

Permite selecionar hora inicial e hora final.

Exemplo:

```text
08:00 às 18:00
```

---

## 24 HORAS

Considera todas as horas disponíveis no recorte selecionado.

---

# ⚡ Fontes de geração

As fontes disponíveis para análise são:

- Hidráulica
- Térmica
- Eólica
- Solar

É possível selecionar uma ou várias fontes.

---

# 📈 Indicadores

Dependendo do filtro utilizado, o dashboard apresenta indicadores como:

### Carga média

Média da carga observada no recorte selecionado.

### Pico

Maior valor de carga encontrado.

### Mínimo

Menor valor de carga encontrado.

### Intercâmbio médio

Média do intercâmbio observado no recorte.

---

# 📊 Gráficos

## Curva de Carga

Mostra a evolução horária da carga.

Permite comparar:

- diferentes dias;
- diferentes períodos;
- diferentes subsistemas;
- diferentes horários.

---

## Curva de Geração

Mostra a evolução horária das fontes selecionadas:

- hidráulica;
- térmica;
- eólica;
- solar.

---

## Composição da geração

Apresenta a participação média das fontes selecionadas no recorte analisado.

---

# 🔎 Análise exploratória — Copa do Mundo

O notebook `analise_copa_nova.ipynb` apresenta uma aplicação prática dos dados do ONS utilizando os jogos do Brasil nas Copas de 2014 e 2026.

A análise considera o **Sistema Interligado Nacional (SIN)** e relaciona os horários dos jogos com:

- carga;
- geração hidráulica;
- geração térmica;
- geração eólica;
- geração solar;
- intercâmbio.

## Principais análises

### Carga média nos horários dos jogos

Compara a carga média observada nos horários das partidas entre 2014 e 2026.

### Carga do jogo × carga de referência

Para cada jogo, é calculada uma **carga de referência do horário**, construída a partir da média da carga observada no mesmo horário em uma janela de aproximadamente ±7 dias, excluindo o próprio instante do jogo.

O cálculo utilizado é:

```text
Variação (%) =
(Carga no jogo - Carga de referência)
/
Carga de referência
× 100
```

Essa referência é uma construção estatística do estudo e não representa uma previsão oficial do ONS.

### Composição da geração

Compara a participação média das fontes:

- hidráulica;
- térmica;
- eólica;
- solar.

### Variação por jogo

Mostra a diferença percentual entre a carga observada durante cada partida e a carga de referência.

---

# 🧪 Metodologia da análise da Copa

O estudo segue as etapas:

1. identificação dos horários das partidas;
2. cruzamento com a série horária do ONS;
3. seleção do SIN;
4. extração da carga e das fontes de geração;
5. construção da referência horária;
6. comparação entre carga observada e referência;
7. agregação dos resultados por Copa;
8. geração dos gráficos e conclusões.

A interpretação é **observacional**.

A análise não permite afirmar, isoladamente, que os jogos foram a causa direta das alterações na carga.

Fatores como:

- dia da semana;
- temperatura;
- condições climáticas;
- feriados;
- características específicas dos dias;
- outros eventos operacionais;

também podem influenciar o comportamento da demanda.

---

# 📚 Fonte dos dados

Os dados utilizados no projeto são provenientes do:

**Operador Nacional do Sistema Elétrico — ONS**

Portal de dados:

https://dados.ons.org.br/

Página de referência visual de Carga e Geração:

https://www.ons.org.br/paginas/energia-agora/carga-e-geracao

# Dashboard ONS — Carga e Geração

Dashboard analítico desenvolvido em **Python + Streamlit** para exploração histórica de dados de **Carga e Geração do Sistema Interligado Nacional (SIN)** a partir do Balanço de Energia do ONS.

O projeto foi estruturado com inspiração na experiência de consulta da página **Carga e Geração** do ONS, mas com uma camada histórica e comparativa que permite selecionar diferentes datas, períodos, horários, subsistemas e fontes de geração.

---

## 📌 Visão geral

A solução permite explorar o comportamento da carga e da geração ao longo do tempo e comparar diferentes recortes históricos.

Entre os principais recursos estão:

- seleção de **um ou vários subsistemas**;
- seleção de **fontes de geração**;
- análise de **um dia**;
- comparação de **até 7 dias**;
- análise de **um período**;
- comparação de **dois períodos**;
- seleção de **uma hora**;
- comparação de **até 7 horários**;
- análise de um **intervalo horário**;
- análise de **24 horas**;
- curva horária de carga;
- curva horária de geração;
- indicadores de carga média, pico, mínimo e intercâmbio;
- comparação visual entre diferentes dias e períodos.

A aplicação utiliza a base histórica consolidada no arquivo:

```text
balanco_energia_ons.parquet
```

---

## 🎯 Objetivo

O objetivo do projeto é transformar uma base histórica de balanço energético em uma ferramenta visual para responder perguntas como:

- Como a carga se comportou em determinado dia?
- Qual foi o horário de maior carga?
- Como a geração hidráulica, térmica, eólica e solar variou?
- Como dois dias diferentes se comportaram?
- Como dois períodos históricos se comportaram?
- Como diferentes subsistemas se comparam?
- Como muda o perfil de geração quando selecionamos diferentes fontes?

O projeto também contém um notebook separado com uma análise exploratória aplicada às partidas do Brasil nas Copas do Mundo de 2014 e 2026.

---

## 🏗️ Estrutura do projeto

```text
dashboard-ons-echoenergia/
│
├── dashboard.py
├── analise_copa_nova.ipynb
├── requirements.txt
├── README.md
├── .gitignore
└── balanco_energia_ons.parquet
```

### Arquivos

#### `dashboard.py`

Aplicação principal desenvolvida em Streamlit.

É responsável por:

- carregamento da base;
- filtros;
- processamento dos dados;
- criação dos indicadores;
- criação dos gráficos;
- interação com o usuário.

#### `analise_copa_nova.ipynb`

Notebook de análise exploratória utilizado para estudar o comportamento da carga e da geração nos horários dos jogos do Brasil nas Copas de 2014 e 2026.

Entre as análises realizadas estão:

- carga média nos horários dos jogos;
- carga dos jogos versus carga de referência;
- composição média da geração;
- comparação 2014 × 2026;
- variação da carga por jogo;
- conclusões e limitações da análise.

#### `balanco_energia_ons.parquet`

Base histórica do ONS utilizada pelo projeto.

As principais variáveis utilizadas são:

```text
id_subsistema
nom_subsistema
din_instante
val_gerhidraulica
val_gertermica
val_gereolica
val_gersolar
val_carga
val_intercambio
```

> **Observação:** a base é um arquivo de dados de tamanho elevado. Caso o repositório seja público, recomenda-se avaliar se o arquivo deve ser versionado diretamente no GitHub ou disponibilizado separadamente.

---

# 🧰 Tecnologias e bibliotecas

## Python

Linguagem utilizada em toda a solução.

## Streamlit

Utilizado para construção da aplicação web interativa.

Permite:

- criação dos filtros;
- organização da interface;
- exibição dos indicadores;
- execução dos gráficos;
- interação com os dados sem necessidade de um front-end separado.

## Pandas

Utilizado para:

- leitura e transformação dos dados;
- filtragem;
- agrupamentos;
- cálculos de médias;
- comparação de períodos;
- tratamento das séries temporais.

## NumPy

Utilizado para operações numéricas e tratamento de valores ausentes nas análises.

## Plotly

Utilizado para construção dos gráficos interativos do dashboard.

## PyArrow

Utilizado pelo pandas para leitura do formato **Parquet**.

## Matplotlib

Utilizado no notebook `analise_copa_nova.ipynb` para geração dos gráficos da análise exploratória.

---

# ⚙️ Instalação

## 1. Clonar o repositório

```bash
git clone https://github.com/SEU_USUARIO/dashboard-ons-echoenergia.git
```

Entrar na pasta:

```bash
cd dashboard-ons-echoenergia
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
pip install -r requirements.txt
```

Caso o arquivo `requirements.txt` ainda não exista, as principais dependências são:

```text
streamlit
pandas
numpy
plotly
pyarrow
matplotlib
```

---

# ▶️ Executando o dashboard

Na pasta do projeto, execute:

```bash
python -m streamlit run dashboard.py
```

O Streamlit disponibilizará uma URL local, normalmente:

```text
http://localhost:8501
```

Abra o endereço no navegador.

---

# 📊 Como utilizar o dashboard

## 1. Subsistema

O usuário pode selecionar um ou vários subsistemas.

Exemplos:

- NORTE
- NORDESTE
- SUL
- SUDESTE/CENTRO-OESTE
- SISTEMA INTERLIGADO NACIONAL

Ao selecionar mais de um subsistema, os gráficos apresentam séries separadas para permitir comparação.

---

## 2. Modo de análise

O dashboard possui dois modos principais:

### DIA

Permite analisar um dia específico.

O usuário pode adicionar outros dias por meio do botão `+`, chegando a um máximo de **7 dias** para comparação.

Exemplo:

```text
25/08/2026
24/08/2026
23/08/2026
```

---

### PERÍODO

Permite analisar um intervalo de datas.

Exemplo:

```text
21/08/2026 a 23/08/2026
```

Também é possível adicionar um segundo período para comparação.

Exemplo:

```text
Período 1: 21/08/2026 a 23/08/2026
Período 2: 14/08/2026 a 16/08/2026
```

---

# 🕒 Filtro de horário

O dashboard permite três formas de seleção.

## HORA

Seleção de uma hora específica.

Exemplo:

```text
08:00
```

Também é possível adicionar outros horários por meio do botão `+`.

---

## INTERVALO

Permite definir hora inicial e hora final.

Exemplo:

```text
08:00 às 18:00
```

---

## 24 HORAS

Considera todas as horas disponíveis no dia.

---

# ⚡ Fontes de geração

As fontes disponíveis para análise são:

- Hidráulica
- Térmica
- Eólica
- Solar

O usuário pode selecionar uma ou várias fontes.

Os filtros afetam os gráficos e os indicadores relacionados à geração.

---

# 📈 Indicadores

Dependendo do recorte selecionado, o dashboard apresenta indicadores como:

### Carga média

Média da carga observada dentro do recorte selecionado.

### Pico

Maior valor de carga encontrado no recorte.

### Mínimo

Menor valor de carga encontrado no recorte.

### Intercâmbio médio

Média do intercâmbio observado no recorte.

---

# 📊 Gráficos

## Curva de Carga

Mostra a evolução horária da carga no período ou dia selecionado.

Quando mais de um dia ou período é comparado, as curvas podem ser visualizadas em conjunto.

---

## Curva de Geração

Mostra a evolução das fontes selecionadas ao longo das horas:

- hidráulica;
- térmica;
- eólica;
- solar.

---

## Composição da geração

Apresenta a participação média das fontes de geração no recorte analisado.

---

# 🔎 Análise exploratória — Copa do Mundo

O projeto também possui uma análise específica no notebook `analise_copa_nova.ipynb`.

O estudo compara o comportamento do sistema nos horários dos jogos do Brasil em:

- Copa de 2014;
- Copa de 2026.

A análise é realizada para o:

```text
Sistema Interligado Nacional (SIN)
```

## Principais análises

### Carga média nos horários dos jogos

Compara a carga média observada nos jogos de 2014 e 2026.

### Carga do jogo × carga de referência

Para cada partida, é calculada uma referência de carga usando o mesmo horário em uma janela de aproximadamente ±7 dias, excluindo o próprio instante do jogo.

A comparação permite calcular:

```text
Variação (%) =
(Carga no jogo - Carga de referência)
/
Carga de referência
× 100
```

A referência é uma construção estatística do estudo e não uma previsão oficial do ONS.

### Composição da geração

Compara a participação média de:

- hidráulica;
- térmica;
- eólica;
- solar.

### Variação por jogo

Mostra a diferença percentual entre a carga observada durante cada partida e a referência utilizada no estudo.

---

# 🧪 Metodologia da análise da Copa

A análise utiliza:

1. identificação dos horários das partidas;
2. cruzamento com a série horária do ONS;
3. seleção do SIN;
4. extração da carga e das fontes de geração;
5. construção da referência horária;
6. comparação entre observado e referência;
7. agregação por Copa;
8. visualização dos resultados.

A interpretação é **observacional**.

Os resultados não permitem afirmar, isoladamente, que a partida foi a causa da alteração na carga.

Fatores como temperatura, dia da semana, feriados, clima e demais condições operativas podem influenciar a demanda.

Além disso, o número de jogos analisados é diferente entre os períodos.

---

# 📚 Fonte dos dados

Os dados utilizados no projeto são provenientes do **Operador Nacional do Sistema Elétrico (ONS)**, especialmente do conjunto histórico de balanço de energia por subsistema.

Referência:

https://dados.ons.org.br/

Página de referência visual para Carga e Geração:

https://www.ons.org.br/paginas/energia-agora/carga-e-geracao

---

# Dashboard ONS — Carga e Geração

Dashboard analítico desenvolvido em **Python + Streamlit** para exploração histórica de dados de **Carga e Geração do Sistema Interligado Nacional (SIN)**, a partir de dados públicos do **Operador Nacional do Sistema Elétrico (ONS)**.

O projeto combina um **pipeline de atualização de dados**, um **dashboard interativo** e um **notebook de análise exploratória**, permitindo trabalhar com séries históricas de carga, geração por fonte e intercâmbio.

Repositório: https://github.com/PalomaBRND/DADOS_ONS

---

## 📌 Visão geral

A solução é estruturada em três etapas:

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

O dashboard foi desenvolvido com inspiração na página **Carga e Geração** do ONS, acrescentando recursos de análise histórica e comparação entre dias, períodos, horários, subsistemas e fontes de geração.

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

> **Intercambio** : fluxo líquido de energia associado às interligações entre subsistemas, conforme a convenção da base do ONS, em MWmed.


Além do dashboard, o projeto possui um **notebook** com uma aplicação prática desses dados: uma análise dos jogos do Brasil nas Copas do Mundo de 2014 e 2026.

---

## 🏗️ Estrutura do projeto

```text
DADOS_ONS/
│
├── dashboard.py
├── pipeline.py
├── analise_copa.ipynb
├── requirements.txt
├── README.md
└── .gitignore
```

> `balanco_energia_ons.parquet` **não fica versionado no repositório** (está no `.gitignore`, por ser um arquivo grande). Ele é gerado localmente ao rodar `pipeline.py` — veja a seção [Atualização dos dados](#-atualização-dos-dados).

### `dashboard.py`

Aplicação principal em Streamlit. Responsável por:

- leitura da base consolidada;
- filtros interativos (subsistemas, fontes de geração, dias/períodos, horários);
- cálculo dos indicadores (carga média, pico, mínimo, intercâmbio médio);
- geração dos gráficos (linha de carga, linha de geração, composição/pizza);
- comparação entre recortes históricos.

### `pipeline.py`

Script que baixa os arquivos anuais públicos do ONS (2000 até o ano corrente), padroniza as colunas numéricas e consolida tudo em um único arquivo:

```text
balanco_energia_ons.parquet
```

Antes de gravar o arquivo, o pipeline **valida a base consolidada**:

- confere se as colunas obrigatórias existem;
- confere se `din_instante` é uma data válida, sem nulos;
- confere se os subsistemas encontrados batem com os 5 esperados (NORTE, NORDESTE, SUL, SUDESTE/CENTRO-OESTE, SIN);
- checa duplicidade de `(din_instante, id_subsistema)`;
- checa valores de carga negativos;
- avisa (sem bloquear) se houver horas sem nenhum registro no período coberto — falhas pontuais de coleta do próprio ONS acontecem e não impedem o uso da base.

Se alguma validação falhar, o pipeline **não grava o Parquet** e encerra com uma mensagem explicando o que encontrou.

### `analise_copa.ipynb`

Notebook de análise exploratória aplicando os dados do ONS aos horários dos jogos do Brasil nas Copas do Mundo de **2014** e **2026**. Entre as análises:

- carga média nos horários dos jogos;
- carga observada versus carga de referência;
- composição média da geração;
- comparação 2014 × 2026;
- variação da carga por jogo;
- conclusões e limitações metodológicas.

Esse notebook **não é executado automaticamente** por `dashboard.py` — é um arquivo separado, aberto e rodado manualmente no Jupyter. Veja o passo a passo completo mais abaixo.

### `requirements.txt`

Lista de bibliotecas necessárias para o projeto **inteiro** (dashboard, pipeline e notebook) — ver seção de instalação.

### `.gitignore`

Evita versionar arquivos locais e arquivos de dados grandes, como `*.parquet`.

---

## 🧰 Tecnologias e bibliotecas

| Biblioteca | Usada em | Para quê |
|---|---|---|
| **Python** | tudo | linguagem principal |
| **Pandas** | dashboard, pipeline, notebook | leitura, filtros, agrupamentos, séries temporais |
| **PyArrow** | dashboard, pipeline, notebook | leitura/escrita do formato Parquet |
| **Streamlit** | dashboard | interface web interativa |
| **Plotly** | dashboard | gráficos interativos |
| **NumPy** | notebook | operações numéricas e tratamento de ausentes |
| **Matplotlib** | notebook | gráficos estáticos da análise da Copa |
| **Jupyter / Notebook / ipykernel** | notebook | ambiente para abrir e rodar o `.ipynb` |
| **Requests** | pipeline (indireto, via pandas) | leitura dos parquets remotos do ONS |

---


# ⚙️ Instalação

## 1. Clonar o repositório

```bash
git clone https://github.com/PalomaBRND/DADOS_ONS.git
cd DADOS_ONS
```

## 2. Criar um ambiente virtual

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**Linux / macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 3. Instalar as dependências

```bash
python -m pip install -r requirements.txt
```

---

# 🔄 Atualização dos dados

O arquivo `balanco_energia_ons.parquet` não vem no repositório — ele é reconstruído localmente a partir dos dados públicos do ONS.

```bash
python pipeline.py
```

O processo:

1. acessa os arquivos anuais publicados pelo ONS (2000–2026);
2. baixa os dados;
3. padroniza as colunas numéricas;
4. consolida os anos em um único DataFrame;
5. grava o resultado em `balanco_energia_ons.parquet`, na pasta do projeto.

> O tempo de execução depende da quantidade de anos processados e da velocidade da conexão — baixar 26 anos de dados pode levar alguns minutos.
>
> Se você já tem um `balanco_energia_ons.parquet` pronto (por exemplo, recebido de outra pessoa), pode colocá-lo direto na pasta do projeto e pular esta etapa.

---

# ▶️ Executando o dashboard

Depois de gerar (ou obter) o `balanco_energia_ons.parquet`:

```bash
python -m streamlit run dashboard.py
```

O Streamlit abre uma URL local, normalmente:

```text
http://localhost:8501
```

Para encerrar, volte ao terminal e pressione `Ctrl+C`.

## Acessando sem instalar nada (opcional)

Para quem só quer ver o dashboard sem clonar o repositório, o app pode ser publicado gratuitamente no [Streamlit Community Cloud](https://streamlit.io/cloud):

1. faça login em share.streamlit.io com a conta do GitHub;
2. clique em "New app", escolha o repositório `PalomaBRND/DADOS_ONS` e o arquivo `dashboard.py`;
3. como o `balanco_energia_ons.parquet` não é versionado, será preciso ajustar `dashboard.py` para gerar a base no primeiro acesso (chamando `pipeline.py`) ou disponibilizar o arquivo por outro meio (ex: um link de download que o app baixa na inicialização).

Alternativa mais simples: capturar 2–3 prints do dashboard rodando localmente e incluí-los neste README (pasta `docs/` ou `screenshots/`), para quem for avaliar o projeto sem precisar rodar nada.

---

# 📓 Executando o notebook da Copa (`analise_copa.ipynb`)

Esta seção assume que você já fez os passos de **Instalação** e de **Atualização dos dados** acima (o `.venv` está criado e ativado, o `requirements.txt` já foi instalado incluindo `numpy` e `matplotlib`, e o `balanco_energia_ons.parquet` já existe na pasta do projeto).

1. **Confirme que o ambiente virtual está ativado** — o terminal deve mostrar `(.venv)` no início da linha. Se não estiver:
   ```bash
   # Windows
   .venv\Scripts\activate
   # Linux/macOS
   source .venv/bin/activate
   ```

2. **Inicie o Jupyter** a partir da pasta do projeto:
   ```bash
   python -m notebook
   ```
   (ou `jupyter lab`, se preferir a interface mais nova — funciona do mesmo jeito, só muda a aparência).

3. Isso abre uma aba no navegador com a lista de arquivos da pasta. Clique em **`analise_copa.ipynb`** para abrir.

4. No menu do notebook, vá em **Cell → Run All** (no Jupyter Notebook clássico) ou **Run → Run All Cells** (no Jupyter Lab) para rodar tudo do início.

5. Os gráficos e as conclusões aparecem diretamente abaixo de cada célula, na própria página.

Para encerrar o Jupyter, volte ao terminal onde ele foi iniciado e pressione `Ctrl+C` (pode pedir confirmação com `y`).

---

# 📊 Funcionalidades do dashboard

## Subsistemas

Seleção de um ou vários subsistemas: NORTE, NORDESTE, SUL, SUDESTE/CENTRO-OESTE, SISTEMA INTERLIGADO NACIONAL. Com mais de um selecionado, os gráficos mostram as séries separadamente.

## Modo DIA

Analisa um dia específico. O botão `+` permite adicionar outros dias para comparação (até 7).

## Modo PERÍODO

Analisa um intervalo de datas, com opção de adicionar um segundo período para comparação.

## Filtro de horário

- **HORA** — uma ou mais horas específicas (`+` para adicionar);
- **INTERVALO** — hora inicial e final;
- **24 HORAS** — todas as horas do recorte.

## Fontes de geração

Hidráulica, Térmica, Eólica e Solar — uma ou várias.

## Indicadores

Carga média, pico, mínimo e intercâmbio médio do recorte selecionado.

## Gráficos

- **Curva de carga** — evolução horária, comparando dias/períodos/subsistemas/horários;
- **Curva de geração** — evolução das fontes selecionadas;
- **Composição da geração** — participação média de cada fonte no recorte.

---

# 🔎 Análise exploratória — Copa do Mundo

O notebook `analise_copa.ipynb` aplica os dados do ONS aos horários dos jogos do Brasil nas Copas de 2014 e 2026, para o **Sistema Interligado Nacional (SIN)**.

### Carga média nos horários dos jogos
Compara a carga média observada nos horários das partidas entre 2014 e 2026.

### Carga do jogo × carga de referência
Para cada jogo, é calculada uma carga de referência do horário: a média da carga observada no mesmo horário em uma janela de aproximadamente ±7 dias, excluindo o próprio instante do jogo.

```text
Variação (%) = (Carga no jogo − Carga de referência) / Carga de referência × 100
```

Essa referência é uma construção estatística do estudo, não uma previsão oficial do ONS.

### Composição da geração
Participação média de hidráulica, térmica, eólica e solar nos horários dos jogos.

### Variação por jogo
Diferença percentual entre a carga observada em cada partida e a referência.

---

# 🧪 Metodologia da análise da Copa

1. identificação dos horários das partidas;
2. cruzamento com a série horária do ONS;
3. seleção do SIN;
4. extração da carga e das fontes de geração;
5. construção da referência horária;
6. comparação entre observado e referência;
7. agregação por Copa;
8. visualização dos resultados e conclusões.

A interpretação é **observacional** — os resultados não permitem afirmar, isoladamente, que os jogos foram a causa direta das variações de carga. Fatores como dia da semana, temperatura, condições climáticas, feriados e outros eventos operacionais também influenciam a demanda. Além disso, o número de jogos analisados difere entre 2014 e 2026, o que limita a comparabilidade direta.

> **Nota sobre o recorte:** o notebook compara os horários dos jogos do Brasil em 2014 e 2026, de forma simétrica entre os dois anos. 
>
> **Nota sobre os horários:** os horários dos jogos de 2026 foram apurados manualmente a partir de cobertura jornalística da época.

---

# 📚 Fonte dos dados

Dados do **Operador Nacional do Sistema Elétrico (ONS)**:

- Portal de dados: https://dados.ons.org.br/
- Página de referência — Carga e Geração: https://www.ons.org.br/paginas/energia-agora/carga-e-geracao

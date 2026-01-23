# README -- Motor de Classificação Semântica para Proteção de Dados (IA GDF)

## 1. Objetivo da Solução

Esta solução tecnológica foi desenvolvida para o **1º Hackathon em
Controle Social: Desafio Participa DF**.\
O sistema atua como uma camada inteligente de segurança no ecossistema
de transparência pública, automatizando a identificação de **dados
pessoais** (nome, CPF, RG, contatos, endereço específico, entre outros)
em pedidos de acesso à informação (LAI).

O objetivo é garantir que o **direito à informação** não colida com o
**direito à privacidade**, prevenindo o vazamento inadvertido de dados
sensíveis e apoiando os processos de auditoria da **Controladoria-Geral
do Distrito Federal (CGDF)**.

------------------------------------------------------------------------

## 2. Proposta de Solução e Arquitetura

A solução utiliza um modelo de **rede neural profunda** baseado em
codificadores de linguagem com mecanismos de atenção (transformers).\
Diferente de abordagens puramente estatísticas ou baseadas em Regex, o
modelo passou por **Fine-Tuning** utilizando um amplo corpus em língua
portuguesa, com foco em sintaxe administrativa e escrita brasileira.

### Características Técnicas do Motor de IA

#### **Arquitetura Baseada em Contexto**

O modelo interpreta frases de forma bidirecional, compreendendo cada
palavra com base no contexto global.

#### **Classificação Binária**

O cabeçote final reduz as representações internas a duas classes: - **0
-- Público (Livre)** - **1 -- Não Público (Sensível)**

#### **Tokenização por Sub-palavras**

Permite analisar: - Termos técnicos - Palavras truncadas - Erros de
digitação - Variações morfológicas

Isso evita perda de significado e aumenta a robustez.

------------------------------------------------------------------------

## 3. Inteligência Artificial vs. Expressões Regulares (Regex)

Optou-se por IA pelas seguintes razões:

### **Variabilidade**

Um CPF pode ser escrito como: - 123.456.789-00\
- 12345678900\
- "um, dois, três..." (por extenso)

Regex falha facilmente diante dessas variações; a IA compreende o padrão
semântico.

### **Compreensão de Contexto**

A IA diferencia textos como: - "processo 1234567/2023" (público)\
- "telefone 123456789" (privado)

Isso só é possível com interpretação contextual.

### **Redução de Falsos Positivos**

A IA impede bloqueios indevidos em casos como: - "código de contrato" -
"número do documento administrativo" - "identificador de ocorrência
pública"

------------------------------------------------------------------------

## 4. Estrutura Detalhada do Projeto

    ├── modelos/
    │   └── IA_GDF/
    │       ├── model.safetensors
    │       ├── config.json
    │       ├── vocab.txt
    │       ├── tokenizer.json
    │       ├── tokenizer_config.json
    │       └── special_tokens_map.json
    │
    ├── scripts/
    │   ├── classificar_txt.py
    │   ├── classificar_csv.py
    │   └── classificar_xlsx.py
    │
    ├── dados/
    │   ├── texto.txt
    │   ├── textos.csv
    │   └── textos.xlsx
    │
    ├── resultados/
    │   ├── texto_classificado.txt
    │   ├── textos_classificados.csv
    │   └── textos_classificados.xlsx
    │
    └── env_hack_gdf/

------------------------------------------------------------------------

## 4.1. Pasta `modelos/IA_GDF/` -- Núcleo da Inteligência

  -----------------------------------------------------------------------
  Arquivo                             Função
  ----------------------------------- -----------------------------------
  `model.safetensors`                 Pesos da rede neural treinada;
                                      representa o conhecimento adquirido
                                      no Fine-Tuning.

  `config.json`                       Arquitetura interna: número de
                                      camadas, mecanismos de atenção,
                                      hiperparâmetros.

  `vocab.txt`                         Vocabulário técnico baseado em
                                      sub-palavras.

  `tokenizer.json` e                  Regras de tokenização e
  `tokenizer_config.json`             pré-processamento.

  `special_tokens_map.json`           Mapeamento de tokens especiais
                                      (CLS, SEP, PAD, etc.).
  -----------------------------------------------------------------------

------------------------------------------------------------------------

## 4.2. Pasta `scripts/` -- Lógica de Execução

### `classificar_txt.py`

Processamento de arquivos simples (texto único).\
Ideal para auditorias pontuais.

### `classificar_csv.py`

Processamento em lote utilizando dados estruturados.\
Indicado para grandes volumes.

### `classificar_xlsx.py`

Versão especializada para Excel, preservando quebras de linha e
caracteres especiais.

------------------------------------------------------------------------

## 4.3. Pasta `dados/` -- Entradas

-   `texto.txt`: texto único para classificação individual\
-   `textos.csv`: lista estruturada para análise em massa\
-   `textos.xlsx`: alternativa preferida ao CSV (evita erros de
    formatação)

------------------------------------------------------------------------

## 4.4. Pasta `resultados/` -- Saídas

-   `texto_classificado.txt`\
-   `textos_classificados.csv`\
-   `textos_classificados.xlsx`

Cada saída contém: - texto original\
- `label` (0 ou 1)\
- `status` (Público ou Não Público)

------------------------------------------------------------------------

## 4.5. Pasta `env_hack_gdf/` -- Ambiente Virtual

Ambiente Python isolado contendo: - Python **3.12.5** - Dependências
certificadas para execução estável

------------------------------------------------------------------------

## 5. Fluxo de Trabalho (Workflow)

### **1. Edição**

O usuário insere os textos nos arquivos dentro de **dados/**.

### **2. Execução**

Roda o script referente ao tipo de arquivo.

### **3. Produção**

A IA processa automaticamente e salva em **resultados/**.

------------------------------------------------------------------------

## 6. Instalação e Configuração

### **Pré-requisitos**

-   Python **3.12.5**
-   Windows ou Linux

### **Criar Ambiente Virtual**

    python -m venv env_hack_gdf

### **Ativar Ambiente**

Windows:

    .\env_hack_gdf\Scripts\activate

Linux:

    source env_hack_gdf/bin/activate

### **Instalar Dependências**

    pip install -r requirements.txt

------------------------------------------------------------------------

## 7. Como Usar (Entrada e Saída de Dados)

### 7.1. **Análise Individual (TXT)**

Entrada:

    dados/texto.txt

Execução:

    python scripts/classificar_txt.py

Saída:

    resultados/texto_classificado.txt

------------------------------------------------------------------------

### 7.2. **Análise em Lote (CSV / XLSX)**

Entrada: - `dados/textos.csv` - `dados/textos.xlsx`

Execução:

    python scripts/classificar_csv.py

Ou:

    python scripts/classificar_xlsx.py

Saída: - `resultados/textos_classificados.csv` -
`resultados/textos_classificados.xlsx`

------------------------------------------------------------------------

## 8. Especificações e Formatos de Dados

### 8.1. **Requisito de Cabeçalho**

A primeira coluna deve se chamar exatamente:

    textos

### 8.2. **Regras para CSV**

-   Cada texto deve estar entre **aspas duplas**:

```{=html}
<!-- -->
```
    "Texto, com vírgula"

-   Evita problemas com separadores, vírgulas e quebras.

### 8.3. **Exemplos de Entrada**

#### **TXT**

    Solicito acesso aos dados do servidor Fulano...

#### **CSV**

``` csv
textos
"Solicito acesso ao documento de Fulano, CPF 123..."
"Pedido de informação sobre o contrato 45/2023."
```

------------------------------------------------------------------------

## 9. Formato das Saídas

### **Saída em CSV/XLSX**

Inclui: - texto original\
- label (0/1)\
- status (Público / Não Público)

### **Saída em TXT**

    RESULTADO: 1
    STATUS: Não Público (Contém dados pessoais)

------------------------------------------------------------------------

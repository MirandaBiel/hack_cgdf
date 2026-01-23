# README  
# Motor de Classificação Semântica para Proteção de Dados (IA GDF)

## 1. Objetivo da Solução

Esta solução tecnológica foi desenvolvida para o **1º Hackathon em Controle Social: Desafio Participa DF**.  
O sistema atua como uma camada inteligente de segurança no ecossistema de transparência pública, automatizando a identificação de **dados pessoais** (nome, CPF, RG, contatos, endereço específico, entre outros) em pedidos de acesso à informação.

O objetivo principal é assegurar que o **direito constitucional de acesso à informação** não entre em conflito com o **direito à privacidade**, prevenindo o vazamento inadvertido de dados sensíveis e apoiando os processos de auditoria e conformidade conduzidos pela **Controladoria-Geral do Distrito Federal (CGDF)**.

---

## 2. Proposta de Solução e Arquitetura

A solução utiliza um modelo de **rede neural profunda** baseado em arquiteturas modernas de linguagem natural com mecanismos de atenção (transformers).  
Diferentemente de abordagens puramente estatísticas ou baseadas em expressões regulares (Regex), o modelo foi submetido a **Fine-Tuning** com um corpus extensivo em língua portuguesa, priorizando textos administrativos e jurídicos utilizados no contexto brasileiro.

> **Observação:** devido ao tamanho do modelo treinado, ele não está versionado diretamente no repositório.  
O modelo encontra-se hospedado no Hugging Face e pode ser obtido em:  
https://huggingface.co/MirandaBiel/IA_GDF/tree/main  
O download é realizado automaticamente por meio do script `download_modelo.py`.

### Características Técnicas do Motor de IA

#### Arquitetura Baseada em Contexto
O modelo realiza interpretação bidirecional das frases, compreendendo cada termo com base no contexto global do texto.

#### Classificação Binária
O cabeçote de saída reduz as representações internas para duas classes:
- **0 — Público (Livre)**
- **1 — Não Público (Sensível)**

#### Tokenização por Subpalavras
A tokenização permite lidar adequadamente com:
- Termos técnicos
- Palavras truncadas
- Erros de digitação
- Variações morfológicas

Essa abordagem reduz a perda semântica e aumenta a robustez da classificação.

---

## 3. Inteligência Artificial vs. Expressões Regulares (Regex)

A utilização de Inteligência Artificial foi escolhida pelos seguintes motivos:

### Variabilidade de Escrita
Um CPF pode aparecer de diversas formas:
- 123.456.789-00  
- 12345678900  
- Representação por extenso

Expressões regulares falham facilmente diante dessas variações, enquanto a IA reconhece o padrão semântico subjacente.

### Compreensão de Contexto
A IA distingue corretamente situações como:
- “processo 1234567/2023” — **público**
- “telefone 123456789” — **privado**

Esse nível de diferenciação só é possível com análise contextual.

### Redução de Falsos Positivos
A abordagem semântica evita bloqueios indevidos em casos como:
- Código de contrato
- Número de documento administrativo
- Identificadores de processos públicos

---

## 4. Estrutura do Projeto

```
├── modelos/
│   └── IA_GDF/
│       ├── model.safetensors
│       ├── config.json
│       ├── vocab.txt
│       ├── tokenizer.json
│       ├── tokenizer_config.json
│       └── special_tokens_map.json
├── scripts/
│   ├── classificar_txt.py
│   ├── classificar_csv.py
│   ├── classificar_xlsx.py
│   └── download_modelo.py
├── dados/
│   ├── texto.txt
│   ├── textos.csv
│   └── textos.xlsx
├── resultados/
│   ├── texto_classificado.txt
│   ├── textos_classificados.csv
│   └── textos_classificados.xlsx
├── env_hack_gdf/
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 4.1. Pasta `modelos/IA_GDF/` — Núcleo da Inteligência

| Arquivo | Função |
|-------|-------|
| `model.safetensors` | Pesos da rede neural treinada, representando o conhecimento adquirido no Fine-Tuning |
| `config.json` | Definição da arquitetura interna do modelo (camadas, atenção, hiperparâmetros) |
| `vocab.txt` | Vocabulário baseado em subpalavras |
| `tokenizer.json` | Regras completas de tokenização |
| `tokenizer_config.json` | Configurações de pré-processamento |
| `special_tokens_map.json` | Mapeamento de tokens especiais (CLS, SEP, PAD, etc.) |

---

## 4.2. Pasta `scripts/` — Lógica de Execução

### `download_modelo.py`
Responsável por realizar o download automático do modelo a partir do Hugging Face, caso ele ainda não esteja disponível localmente.  
Os demais scripts verificam a existência do modelo antes da execução.

### `classificar_txt.py`
Processa arquivos de texto simples, sendo indicado para auditorias pontuais.

### `classificar_csv.py`
Executa classificação em lote utilizando arquivos CSV estruturados.

### `classificar_xlsx.py`
Versão especializada para arquivos Excel, preservando quebras de linha, codificação e caracteres especiais.

---

## 4.3. Pasta `dados/` — Arquivos de Entrada

- `texto.txt`: texto único para análise individual  
- `textos.csv`: conjunto estruturado para análise em massa  
- `textos.xlsx`: alternativa recomendada ao CSV, reduzindo problemas de formatação

---

## 4.4. Pasta `resultados/` — Arquivos de Saída

- `texto_classificado.txt`  
- `textos_classificados.csv`  
- `textos_classificados.xlsx`  

Cada saída contém:
- Texto original  
- Label (0 ou 1)  
- Status (Público ou Não Público)

---

## 4.5. Pasta `env_hack_gdf/` — Ambiente Virtual

Ambiente Python isolado utilizado no projeto, contendo:
- Python **3.12.5**
- Dependências específicas para execução estável

---

## 5. Arquivo `requirements.txt`

O arquivo `requirements.txt` lista todas as bibliotecas Python necessárias para a execução do projeto, garantindo reprodutibilidade do ambiente e compatibilidade entre sistemas.

A instalação das dependências é realizada automaticamente por meio do comando:

```
pip install -r requirements.txt
```

---

## 6. Arquivo `.gitignore`

O arquivo `.gitignore` define quais arquivos e diretórios não devem ser versionados no repositório Git, incluindo:
- Ambiente virtual (`env_hack_gdf/`)
- Arquivos temporários
- Cache de execução
- Modelos de grande porte baixados externamente

Isso mantém o repositório limpo e reduz o tamanho do versionamento.

---

## 7. Fluxo de Trabalho

1. **Edição**: o usuário insere os textos nos arquivos localizados em `dados/`  
2. **Execução**: executa o script correspondente ao tipo de arquivo  
3. **Processamento**: a IA realiza a classificação automaticamente  
4. **Resultado**: os arquivos classificados são salvos em `resultados/`

---

## 8. Instalação e Configuração

### Pré-requisitos
- Python **3.12.5**
- Windows ou Linux

### Criar Ambiente Virtual
```
python -m venv env_hack_gdf
```

### Ativar Ambiente
Windows:
```
.\env_hack_gdf\Scripts\activate
```

Linux:
```
source env_hack_gdf/bin/activate
```

### Instalar Dependências
```
pip install -r requirements.txt
```

---

## 9. Formatos e Regras de Dados

### 9.1. Cabeçalho Obrigatório
A primeira coluna dos arquivos CSV ou XLSX deve se chamar exatamente:

```
textos
```

### 9.2. Regras para CSV
- Cada texto deve estar entre aspas duplas
- Essa prática evita erros com vírgulas, separadores e quebras de linha

Exemplo:
```
"textos"
"Texto com vírgula, sem erro"
```

### 9.3. Exemplo de Estrutura XLSX

| textos |
|--------|
| Solicito acesso ao documento do servidor Fulano |
| Pedido de informação sobre o contrato nº 45/2023 |
| Relatório contendo telefone e endereço do solicitante |

---

## 10. Formato das Saídas

### Saída em CSV/XLSX
Inclui:
- Texto original  
- Label (0 ou 1)  
- Status (Público / Não Público)

### Saída em TXT
```
RESULTADO: 1
STATUS: Não Público (Contém dados pessoais)
```

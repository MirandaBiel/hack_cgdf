# Motor de Classificação Semântica para Proteção de Dados (IA_CGDF)

## 1. Objetivo da Solução

Esta solução tecnológica foi desenvolvida para o **1º Hackathon em Controle Social: Desafio Participa DF**.  
O sistema atua como uma camada inteligente de segurança no ecossistema de transparência pública, automatizando a identificação de **dados pessoais** (nome, CPF, RG, contatos, entre outros) em pedidos de acesso à informação.

O objetivo principal é assegurar que o **direito constitucional de acesso à informação** não entre em conflito com o **direito à privacidade**, prevenindo o vazamento inadvertido de dados sensíveis e apoiando os processos de auditoria e conformidade conduzidos pela **Controladoria-Geral do Distrito Federal (CGDF)**.

---

## 2. Proposta de Solução e Arquitetura

A solução baseia-se em uma arquitetura de Rede Neural Profunda utilizando o modelo BERT (Bidirectional Encoder Representations from Transformers) como base. Diferente de abordagens genéricas, esta implementação é um modelo autoral otimizado especificamente para o Desafio Participa DF.

Customização da Camada de Saída: Foi implementada uma camada densa superior de classificação binária ($k=2$), projetada para mapear as representações contextuais do BERT diretamente nas classes alvo: Público ou Contém Dados Pessoais (Não Público).

Fine-Tuning Especializado: O modelo passou por um processo de ajuste fino (Fine-Tuning) utilizando uma base de dados própria, composta por textos administrativos e jurídicos do cenário brasileiro. Isso permite que a IA compreenda as nuances linguísticas de pedidos de informação e identifique dados sensíveis com maior precisão do que modelos estatísticos simples ou Regex.

Foco em Desempenho (P1): A arquitetura foi refinada para maximizar a relação entre Precisão e Sensibilidade (Recall), garantindo que o modelo minimize falsos negativos no tratamento de dados pessoais.

> **Observação:** Devido ao volume de parâmetros após o treinamento, o modelo não está versionado diretamente no repositório para manter a organização.
O modelo encontra-se hospedado no Hugging Face e pode ser obtido em:  
https://huggingface.co/MirandaBiel/IA_CGDF/tree/main  
O download é realizado automaticamente por meio do script `download_modelo.py` ou pode ser feito manualmente, bastando inserir o modelo na pasta `modelos/`.

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
│   ├── info.txt
│   └── IA_CGDF/
│       ├── model.safetensors
│       ├── config.json
│       ├── vocab.txt
│       ├── tokenizer.json
│       ├── tokenizer_config.json
│       └── special_tokens_map.json
├── scripts/
│   ├── classificar_txt.py
│   ├── classificar_xlsx.py
│   └── download_modelo.py
├── dados/
│   ├── texto.txt
│   └── textos.xlsx
├── resultados/
│   ├── texto_classificado.txt
│   └── textos_classificados.xlsx
├── env_hack_cgdf/
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 4.1. Pasta `modelos/` — Núcleo da Inteligência

### `info.txt`
Guia de orientações para obtenção do modelo, detalhando procedimentos de download automático e manual.

### `IA_CGDF/`
Subdiretório que armazena os artefatos do modelo BERT após o Fine-Tuning.

### `IA_CGDF/model.safetensors`
Pesos da rede neural treinada, representando o conhecimento adquirido para classificar pedidos de informação.

### `IA_CGDF/config.json`
Definição da arquitetura interna do modelo (camadas, mecanismos de atenção e hiperparâmetros).

### `IA_CGDF/vocab.txt`
Vocabulário de subpalavras utilizado para a compreensão do léxico administrativo brasileiro.

### `IA_CGDF/tokenizer.json`
Regras completas de tokenização para o processamento de texto.

### `IA_CGDF/tokenizer_config.json`
Configurações específicas de pré-processamento de strings.

### `IA_CGDF/special_tokens_map.json`
Mapeamento de tokens estruturais da arquitetura Transformer (ex: [CLS], [SEP]).

---

## 4.2. Pasta `scripts/` — Lógica de Execução

### `download_modelo.py`
Responsável por realizar o download automático do modelo a partir do Hugging Face, caso ele ainda não esteja disponível localmente. Os demais scripts verificam a existência do modelo antes da execução, e também realizam o download se necessário.

### `classificar_txt.py`
Processa um único texto em `dados/texto.txt`, e coloca o resultado em `resultados/texto_classificado.txt`.

### `classificar_xlsx.py`
Processa uma série de textos em `dados/textos.xlsx`, e coloca o resultado em `resultados/textos_classificados.xlsx`.

---

## 4.3. Pasta `dados/` — Arquivos de Entrada

- `texto.txt`: arquivo que contém um único texto a ser classificado.   
- `textos.xlsx`: arquivo que contém uma série de textos a serem classificados.

Para realizar a classificação de um texto individual ou de volumes em lote, basta inserir ou editar os conteúdos nos arquivos da pasta `dados/`, utilizando o formato de sua preferência (.txt ou .xlsx).

---

## 4.4. Pasta `resultados/` — Arquivos de Saída

Nessa pasta é possível ver o resultado da classificação do(s) texto(s) contidos em `dados/`.

- `texto_classificado.txt`: resultado da classificação de `texto.txt`. 
- `textos_classificados.xlsx`: resultado da classificação de `textos.xlsx`.  

No formato .txt apenas a classificação do texto será exibida no arquivo de saída, já no formato .xlsx o arquivo de saída contém:
- Texto original  
- Número da classe (0 ou 1)  
- Classe (Público ou Não Público)

---

## 4.5. Pasta `env_hack_cgdf/` — Ambiente Virtual

Ambiente Python isolado utilizado no projeto, contendo:
- Python **3.12.5** (é provável que outras versões sejam suportadas, mas a 3.12.5 é garantida)
- Dependências específicas para execução estável (detalhadas em requirements.txt)

O ambiente é gerado e ativado por meio dos comandos listados mais abaixo.

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
- Ambiente virtual (`env_hack_cgdf/`)
- Arquivos temporários
- Cache de execução
- Modelos de grande porte baixados externamente

Isso mantém o repositório limpo e reduz o tamanho do versionamento.

---

## 7. Fluxo de Trabalho - Como usar o modelo

1. **Edição**: o usuário insere o(s) texto(s) nos arquivos localizados em `dados/`, escolhe-se o formato que preferir, sendo .txt utilizado para classificar um único texto e .xlsx para classificar uma série de textos.
2. **Execução**: executa o script correspondente ao tipo de arquivo editado
3. **Processamento**: a IA realiza a classificação automaticamente  
4. **Resultado**: os arquivos classificados são salvos em `resultados/` no mesmo formato da entrada

> **Observação:** Já existem exemplos de arquivos .txt e .xlsx em `dados/`. O usuário pode inserir um novo arquivo de mesmo nome e apagar o antigo, ou simplesmente editar os existentes com os textos desejados.

---

## 8. Instalação e Configuração

### Pré-requisitos
- Python **3.12.5**
- Gerenciador de pacotes Pip
- Git (opcional para clonagem)
- Visual Studio Code (recomendado para facilitar a navegação nos arquivos e uso do terminal integrado)

Na grande maioria dos casos, especialmente em computadores modernos ou naqueles que já executaram aplicações com PyTorch, **não será necessária nenhuma instalação adicional**. Caso o seu sistema já possua o ambiente configurado para ciência de dados, o próximo pré-requisito provavelmente já terá sido atendido de forma nativa. Recomenda-se fortemente tentar a execução dos scripts **sem realizar qualquer download adicional**. **Somente se o modelo apresentar um erro de inicialização de DLL** (como o WinError 1114), siga o procedimento abaixo:

- Baixe e instale o **Microsoft Visual C++ Redistributable (X64)** através do site oficial da Microsoft.

Caso ainda não seja possível executar o PyTorch, siga alguns tutoriais de instalação e uso da ferramenta, como https://learn.microsoft.com/pt-br/windows/ai/windows-ml/tutorials/pytorch-analysis-installation.

O projeto foi desenvolvido em Python na versão **3.12.5**, até o momento não se encontraram limitações de execução para outras versões, contudo, caso o usuário deseje garantir o funcionamento do sistema, recomenda-se a versão de desenvolvimento utilizada.

Para iniciar, obtenha os arquivos deste repositório público realizando o download do ZIP (clicando em Code > Download ZIP e extraindo o conteúdo em sua máquina) ou utilizando o comando Git via terminal: 

```
git clone https://github.com/MirandaBiel/hack_cgdf.git
```

Na raiz do projeto execute os próximos comandos.

### Criar Ambiente Virtual
```
python -m venv env_hack_cgdf
```

### Ativar Ambiente
No Windows (PowerShell ou CMD): Se a pasta criada for Scripts:
```
.\env_hack_cgdf\Scripts\activate
```

No Git Bash, WSL, Linux ou macOS: Se a pasta criada for bin:
```
source env_hack_cgdf/bin/activate
```
Nota: Se você estiver no Windows e notar a pasta bin em vez de Scripts, provavelmente está utilizando o terminal Git Bash. Nesse caso, utilize o comando source indicado para Linux/Git Bash.

Dica para VS Code: Para garantir que o projeto utilize as dependências corretas, pressione `Ctrl + Shift + P`, selecione a opção `Python: Select Interpreter` e escolha o interpretador correspondente ao ambiente virtual criado.

### Instalar Dependências

Com o ambiente virtual ativado, execute o comando:

```
pip install -r requirements.txt
```

---

## 9. Execução dos scripts

Para que os caminhos relativos funcionem corretamente, você deve estar posicionado na raiz do projeto ao executar os comandos abaixo. Além disso, certifique-se de que o ambiente virtual (env_hack_cgdf) está ativado e que os arquivos em `dados` já contêm os textos que você deseja classificar.

### 9.1. Baixar o modelo
Para baixar o modelo hospedado no Hugging Face, utilize o comando:

```
python scripts/download_modelo.py
```

O modelo será armazenado no caminho `modelos/IA_CGDF`.

### 9.2. Classificação de texto individual
Para processar um único relato contido em `dados/texto.txt`, utilize o comando:

```
python scripts/classificar_txt.py
```

- Entrada: O texto em `dados/texto.txt`.
- Saída: O resultado será gerado em `resultados/texto_classificado.txt`.

### 9.3. Classificação em lote (Planilha)
Para processar múltiplos relatos contidos em `dados/textos.xlsx`, utilize o comando:

```
python scripts/classificar_xlsx.py
```

- Entrada: Os textos da tabela `dados/textos.xlsx`.
- Saída: Uma nova tabela com as classificações será gerada em `resultados/textos_classificados.xlsx`.

---

## 10. Formatos de entrada dos dados

### 10.1. Regras para `dados/texto.txt`
- Esse formato é utilizado para classificar apenas 1 único texto.
- Não há restrições claras, basta escrever no arquivo o texto a ser classificado.

Exemplo (**com dados fictícios**):
```
Protocolo de Reclamação - Ouvidoria Saúde

Gostaria de registrar uma reclamação formal quanto ao atendimento recebido no Hospital Regional da Asa Norte (HRAN) no dia de ontem.

Fui atendido pelo médico Dr. Renato Guimarães, CRM 12345-DF, que se recusou a solicitar os exames básicos de imagem, mesmo eu apresentando dores agudas.

Além disso, a atendente da recepção, Sra. Eliane Martins, foi extremamente ríspida durante o processo de triagem.

Solicito providências quanto à conduta dos profissionais citados.

Atenciosamente,

Marcos Paulo de Oliveira
```

### 10.2. Regras para `dados/textos.xlsx`

- Esse formato é utilizado para classificar uma série de textos. 
- O arquivo consiste em uma simples tabela de apenas uma coluna.
- A primeira célula da tabela deve conter a palavra `textos`.
- As células abaixo da primeira contêm, cada uma, os textos a serem analisados.

Aqui está um exemplo (**com dados fictícios**) de uma série de três textos. Note que o primeiro elemento, na primeira linha, é a label `textos`. Em seguida, logo abaixo, vem um texto simples sem quebra de linha: `Gostaria de agradecer pelos atendimentos anteriores, obrigado!`. O segundo texto é o mesmo utilizado no item anterior (`dados/texto.txt`). O terceiro texto é novamente um texto simples: `Gostaria de solicitar acesso a um documento público`.

| textos |
| :--- |
| Gostaria de agradecer pelos atendimentos anteriores, obrigado! |
| Protocolo de Reclamação - Ouvidoria Saúde<br><br>Gostaria de registrar uma reclamação formal quanto ao atendimento recebido no Hospital Regional da Asa Norte (HRAN) no dia de ontem.<br><br>Fui atendido pelo médico Dr. Renato Guimarães, CRM 12345-DF, que se recusou a solicitar os exames básicos de imagem, mesmo eu apresentando dores agudas.<br><br>Além disso, a atendente da recepção, Sra. Eliane Martins, foi extremamente ríspida durante o processo de triagem.<br><br>Solicito providências quanto à conduta dos profissionais citados.<br><br>Atenciosamente,<br><br>Marcos Paulo de Oliveira |
| Gostaria de solicitar acesso a um documento público |

---

## 11. Formato de saída dos dados

### 11.1. Saída em `resultados/texto_classificado.txt`
- Consiste em duas linhas.
- A primeira linha indica o resultado numérico da classificação: 0 ou 1.
- A segunda linha indica a classe: Público ou Não Público.

Exemplo correspondente ao texto do item **10.1**:

```
N_CLASSE: 1
CLASSE: Não Público (Contém dados pessoais)
```

### 11.2. Saída em `resultados/textos_classificados.xlsx`
- Consiste em uma tabela com 3 colunas.
- A primeira linha contém a legenda de cada coluna.
- A primeira coluna contém os textos que foram classificados.
- A segunda coluna contém os resultados numéricos da classificação: 0 ou 1.
- A terceira coluna contém o status da classificação: Público ou Não Público. 

Exemplo correspondente ao texto do item **10.2**:

| textos | n_classe | classe |
| :--- | :--- | :--- |
| Gostaria de agradecer pelos atendimentos anteriores, obrigado! | 0 | Público |
| Protocolo de Reclamação - Ouvidoria Saúde<br><br>Gostaria de registrar uma reclamação formal quanto ao atendimento recebido no Hospital Regional da Asa Norte (HRAN) no dia de ontem.<br><br>Fui atendido pelo médico Dr. Renato Guimarães, CRM 12345-DF, que se recusou a solicitar os exames básicos de imagem, mesmo eu apresentando dores agudas.<br><br>Além disso, a atendente da recepção, Sra. Eliane Martins, foi extremamente ríspida durante o processo de triagem.<br><br>Solicito providências quanto à conduta dos profissionais citados.<br><br>Atenciosamente,<br><br>Marcos Paulo de Oliveira | 1 | Não Público |
| Gostaria de solicitar acesso a um documento público | 0 | Público |
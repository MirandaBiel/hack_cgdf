import torch
import pandas as pd
import re
import os
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from huggingface_hub import snapshot_download # Interface para comunicação com o Hugging Face

def gerenciar_modelo_autoral(caminho_destino):
    """
    Assegura a disponibilidade dos pesos do modelo para a inferência. Se os arquivos
    não estiverem presentes no diretório especificado, o download é realizado de 
    forma automática a partir do repositório autoral no Hugging Face para permitir
    a execução imediata da classificação.
    """
    # Verifica se a pasta não existe ou se está vazia para garantir integridade técnica
    if not os.path.exists(caminho_destino) or len(os.listdir(caminho_destino)) <= 1:
        print(f"Diretório do modelo não localizado ou incompleto em: {caminho_destino}")
        print("Iniciando download automático do repositório MirandaBiel/IA_CGDF...")
        # local_dir_use_symlinks=False garante que arquivos reais sejam baixados para portabilidade
        snapshot_download(repo_id="MirandaBiel/IA_CGDF", local_dir=caminho_destino, local_dir_use_symlinks=False)
        print("Modelo autoral baixado e pronto para uso.")

def limpar_texto(text):
    """
    Padroniza o texto bruto, removendo quebras de linha e normalizando 
    espaçamentos para garantir a consistência na entrada do modelo.
    """
    if not isinstance(text, str): return ""
    # Substitui quebras de linha e retornos de carro por espaços simples
    text = text.replace('\n', ' ').replace('\r', ' ')
    # Remove espaços duplicados e espaços em branco nas extremidades
    return re.sub(r'\s+', ' ', text).strip()

def classificar_xlsx():
    """
    Lógica principal para carregamento do modelo e classificação de dados em lote (XLSX).
    """
    # Configura o dispositivo de execução: utiliza GPU (CUDA) se disponível ou CPU como fallback
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    # Define a raiz do projeto para localizar pastas de forma relativa, garantindo a portabilidade
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Define os caminhos absolutos para o modelo, entrada de dados e diretório de saída
    model_path = os.path.join(base_dir, "modelos", "IA_CGDF")
    
    # Valida a presença do modelo no caminho especificado antes de prosseguir
    gerenciar_modelo_autoral(model_path)
    
    input_path = os.path.join(base_dir, "dados", "textos.xlsx")
    output_path = os.path.join(base_dir, "resultados", "textos_classificados.xlsx")
    
    # Assegura que o diretório de destino exista antes da gravação dos resultados
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    print(f"Iniciando carga do modelo em: {device}...")
    try:
        # Carrega o tokenizador e o modelo de classificação a partir do diretório local
        tokenizer = AutoTokenizer.from_pretrained(model_path)
        model = AutoModelForSequenceClassification.from_pretrained(model_path).to(device)
        # Coloca o modelo em modo de avaliação para garantir predições determinísticas
        model.eval()
    except Exception as e:
        print(f"Erro ao carregar o modelo ou tokenizador: {e}")
        return

    # Tenta realizar a leitura do arquivo de dados de entrada
    try:
        # Requer a instalação prévia da biblioteca 'openpyxl'
        df = pd.read_excel(input_path)
    except Exception as e:
        print(f"Erro ao ler o arquivo Excel: {e}")
        return

    # Validação da estrutura mínima necessária para o processamento conforme especificado no README
    if 'textos' not in df.columns:
        print("Erro: A planilha deve conter a coluna 'textos'.")
        return

    print(f"Processando {len(df)} registros...")
    
    predicoes_numericas = []
    
    # Desativa o cálculo de gradientes para otimizar memória e acelerar a inferência
    with torch.no_grad():
        for texto in df['textos']:
            texto_limpo = limpar_texto(texto)
            # Converte o texto em tensores numéricos respeitando o limite de 512 tokens
            inputs = tokenizer(texto_limpo, return_tensors="pt", 
                               padding="max_length", truncation=True, 
                               max_length=512).to(device)
            
            # Executa a rede neural e identifica a classe com maior probabilidade
            logits = model(**inputs).logits
            label_id = torch.argmax(logits, dim=-1).item()
            predicoes_numericas.append(label_id)

    # Consolida os resultados e realiza o mapeamento das categorias de saída
    df['label'] = predicoes_numericas
    df['status'] = df['label'].map({0: 'Público', 1: 'Não Público'})
    
    # Exporta o resultado final para o formato de destino definido
    df.to_excel(output_path, index=False)
    print(f"[SUCESSO] Processamento concluído: {output_path}")

if __name__ == "__main__":
    classificar_xlsx()
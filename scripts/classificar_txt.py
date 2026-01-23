import torch
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
    if not os.path.exists(caminho_destino):
        print(f"Diretório do modelo não localizado em: {caminho_destino}")
        print("Iniciando download automático do repositório MirandaBiel/IA_CGDF...")
        # Realiza o download dos arquivos do modelo autoral para a pasta local
        snapshot_download(repo_id="MirandaBiel/IA_CGDF", local_dir=caminho_destino)
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

def classificar_txt():
    """
    Lógica principal para carregamento do modelo e classificação de arquivo individual (TXT).
    """
    # Configura o dispositivo de execução: utiliza GPU (CUDA) se disponível ou CPU como fallback
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    # Define a raiz do projeto para localizar pastas de forma relativa, garantindo a portabilidade
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Define os caminhos absolutos para o modelo, entrada de dados e diretório de saída
    model_path = os.path.join(base_dir, "modelos", "IA_CGDF")
    
    # Valida a presença do modelo no caminho especificado antes de prosseguir
    gerenciar_modelo_autoral(model_path)
    
    input_path = os.path.join(base_dir, "dados", "texto.txt")
    output_dir = os.path.join(base_dir, "resultados")
    
    # Assegura que o diretório de destino exista antes da gravação dos resultados
    os.makedirs(output_dir, exist_ok=True)

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
    if not os.path.exists(input_path):
        print(f"Erro: Arquivo {input_path} não encontrado.")
        return

    with open(input_path, 'r', encoding='utf-8') as f:
        texto_bruto = f.read()

    # Desativa o cálculo de gradientes para otimizar memória e acelerar a inferência
    with torch.no_grad():
        texto_limpo = limpar_texto(texto_bruto)
        # Converte o texto em tensores numéricos respeitando o limite de 512 tokens
        inputs = tokenizer(texto_limpo, return_tensors="pt", 
                           padding="max_length", truncation=True, 
                           max_length=512).to(device)
        
        # Executa a rede neural e identifica a classe com maior probabilidade
        logits = model(**inputs).logits
        pred = torch.argmax(logits, dim=-1).item()

    # Formatação do resultado final para o relatório de saída
    legenda = "Público (Sem dados pessoais)" if pred == 0 else "Não Público (Contém dados pessoais)"
    resultado_final = f"RESULTADO: {pred}\nSTATUS: {legenda}\n"

    # Exporta o resultado final para o formato de destino definido
    with open(os.path.join(output_dir, "texto_classificado.txt"), "w", encoding="utf-8") as f:
        f.write(resultado_final)
    
    print(f"[SUCESSO] Processamento concluído em resultados/texto_classificado.txt")

if __name__ == "__main__":
    classificar_txt()
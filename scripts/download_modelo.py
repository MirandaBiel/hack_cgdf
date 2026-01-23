from huggingface_hub import snapshot_download
import os

def download_model():
    """
    Função para gerenciar o download dos pesos do modelo de IA.
    NOTA DE AUTORALIDADE: Este modelo foi desenvolvido integralmente por mim para o 
    1º Hackathon em Controle Social - Desafio Participa DF.
    A hospedagem no Hugging Face foi escolhida exclusivamente para contornar a limitação 
    de tamanho de arquivos do GitHub, garantindo a integridade dos dados e facilidade 
    na execução pelos avaliadores.
    """
    
    # Identificador do repositório autoral no Hugging Face
    model_id = "MirandaBiel/IA_GDF"
    
    # Caminho local definido para armazenamento (conforme organização do projeto)
    save_path = "../modelos"
    
    if not os.path.exists(save_path):
        print(f"Iniciando download do modelo autoral [{model_id}] do Hugging Face...")
        
        # Realiza o download dos arquivos necessários para a execução da solução
        snapshot_download(repo_id=model_id, local_dir=save_path)
        
        print("Download concluído com sucesso!")
    else:
        # Evita downloads redundantes se a pasta já existir localmente
        print(f"O modelo já está presente em: {save_path}")

if __name__ == "__main__":
    download_model()
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
    model_id = "MirandaBiel/IA_CGDF"
    
    # Garante que o caminho seja relativo ao local deste script e não ao terminal
    # Isso evita que o modelo seja baixado fora da pasta do projeto
    script_dir = os.path.dirname(os.path.abspath(__file__))
    save_path = os.path.normpath(os.path.join(script_dir, "../modelos"))
    
    # Verifica se a pasta existe. Se estiver vazia ou não existir, inicia o download
    if not os.path.exists(save_path) or len(os.listdir(save_path)) <= 1:
        print(f"Iniciando download do modelo autoral [{model_id}] do Hugging Face...")
        
        # Realiza o download dos arquivos necessários para a execução da solução
        # local_dir_use_symlinks=False garante o download físico dos arquivos
        snapshot_download(repo_id=model_id, local_dir=save_path, local_dir_use_symlinks=False)
        
        print("Download concluído com sucesso!")
    else:
        # Evita downloads redundantes se a pasta já estiver presente e populada
        print(f"O modelo já está presente em: {os.path.abspath(save_path)}")

if __name__ == "__main__":
    download_model()
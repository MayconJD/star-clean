import cv2
import numpy as np
import os

# --- Configurações ---
# ATENÇÃO: Altere este caminho para a pasta onde estão suas imagens
PASTA_COMPARACAO = r'C:\Users\Maycon JD\Pictures\Comparacao' # <--- MUDE ESTE CAMINHO

# ATENÇÃO: Nomes dos arquivos ajustados para .jpg conforme as imagens enviadas
ARQUIVO_TRACO = 'traco.png'
ARQUIVO_ANTIGA = 'antiga.png'
ARQUIVO_SOLUCAO = 'solucao.png'

# --- CORREÇÃO PRINCIPAL: AUMENTO DA SENSIBILIDADE ---
# O valor mínimo de Saturação e Brilho foi diminuído de 80 para 40.
# Isso permite que o algoritmo detecte verdes mais escuros e "lavados",
# como os que sobraram na imagem 'antiga.jpg'.
VERDE_MIN = np.array([30, 40, 40])
VERDE_MAX = np.array([90, 255, 255])

# --- Funções ---

def carregar_e_verificar(pasta, nomes_arquivos):
    """Carrega as imagens e verifica se existem e têm o mesmo tamanho."""
    imagens = {}
    dimensoes = None

    for nome in nomes_arquivos:
        caminho = os.path.join(pasta, nome)
        if not os.path.exists(caminho):
            print(f"ERRO: Arquivo '{caminho}' não encontrado!")
            print("Por favor, verifique o caminho na variável PASTA_COMPARACAO e os nomes dos arquivos.")
            return None

        img = cv2.imread(caminho)
        if img is None:
            print(f"ERRO: Não foi possível carregar a imagem '{caminho}'.")
            return None

        if dimensoes is None:
            dimensoes = img.shape[:2]
        elif img.shape[:2] != dimensoes:
            print(f"ERRO: As imagens não têm as mesmas dimensões! ({nome} difere)")
            return None

        imagens[nome] = img

    print("Todas as imagens foram carregadas e verificadas com sucesso.")
    return imagens

def analisar_remocao_rastro(imagens):
    """
    Calcula a porcentagem do rastro VERDE que foi removido, agora com maior sensibilidade.
    """
    traco_img = imagens[ARQUIVO_TRACO]
    antiga_img = imagens[ARQUIVO_ANTIGA]
    solucao_img = imagens[ARQUIVO_SOLUCAO]

    # 1. Definir a área original do rastro usando a imagem 'traco.jpg'
    hsv_traco = cv2.cvtColor(traco_img, cv2.COLOR_BGR2HSV)
    mascara_rastro_original = cv2.inRange(hsv_traco, VERDE_MIN, VERDE_MAX)
    total_pixels_rastro_original = np.count_nonzero(mascara_rastro_original)

    if total_pixels_rastro_original == 0:
        print(f"\nAVISO: Nenhum rastro verde detectado em '{ARQUIVO_TRACO}' com a sensibilidade atual.")
        print("Se o rastro for de outra cor ou muito escuro, ajuste os valores de VERDE_MIN e VERDE_MAX.")
        return

    print(f"\n--- Análise da Remoção do Rastro Verde (Alta Sensibilidade) ---")
    print(f"Rastro original ('{ARQUIVO_TRACO}') contém {total_pixels_rastro_original} pixels verdes.")
    print("-" * 60)

    # 2. Analisar quantos pixels VERDES sobraram na imagem 'antiga.jpg'
    hsv_antiga = cv2.cvtColor(antiga_img, cv2.COLOR_BGR2HSV)
    mascara_verde_antiga = cv2.inRange(hsv_antiga, VERDE_MIN, VERDE_MAX)
    rastro_restante_antiga = cv2.bitwise_and(mascara_rastro_original, mascara_verde_antiga)
    pixels_verdes_restantes_antiga = np.count_nonzero(rastro_restante_antiga)

    # 3. Analisar quantos pixels VERDES sobraram na imagem 'solucao.png'
    hsv_solucao = cv2.cvtColor(solucao_img, cv2.COLOR_BGR2HSV)
    mascara_verde_solucao = cv2.inRange(hsv_solucao, VERDE_MIN, VERDE_MAX)
    rastro_restante_solucao = cv2.bitwise_and(mascara_rastro_original, mascara_verde_solucao)
    pixels_verdes_restantes_solucao = np.count_nonzero(rastro_restante_solucao)

    # 4. Calcular a porcentagem de ELIMINAÇÃO para cada imagem
    perc_eliminado_antiga = (1 - (pixels_verdes_restantes_antiga / total_pixels_rastro_original)) * 100
    perc_eliminado_solucao = (1 - (pixels_verdes_restantes_solucao / total_pixels_rastro_original)) * 100

    # 5. Exibir os resultados
    print(f"Análise de '{ARQUIVO_ANTIGA}':")
    print(f"  - Pixels verdes remanescentes na área do rastro: {pixels_verdes_restantes_antiga}")
    print(f"  - ✅ Porcentagem do rastro eliminada: {perc_eliminado_antiga:.2f}%")

    print(f"\nAnálise de '{ARQUIVO_SOLUCAO}' (STAR Clean):")
    print(f"  - Pixels verdes remanescentes na área do rastro: {pixels_verdes_restantes_solucao}")
    print(f"  - ✅ Porcentagem do rastro eliminada: {perc_eliminado_solucao:.2f}%")

    # 6. Conclusão
    print("\n--- Conclusão ---")
    if abs(perc_eliminado_solucao - perc_eliminado_antiga) < 0.01:
         print("Ambos os métodos tiveram a mesma eficácia na remoção do rastro verde.")
    elif perc_eliminado_solucao > perc_eliminado_antiga:
        print(f"O método 'STAR Clean' ('{ARQUIVO_SOLUCAO}') foi mais eficaz na remoção do rastro verde.")
    else:
        print(f"O método antigo ('{ARQUIVO_ANTIGA}') foi mais eficaz na remoção do rastro verde.")

# --- Execução Principal ---

def main():
    print("--- Iniciando Script de Comparação de Remoção de Rastro ---")
    nomes = [ARQUIVO_TRACO, ARQUIVO_ANTIGA, ARQUIVO_SOLUCAO]
    imagens = carregar_e_verificar(PASTA_COMPARACAO, nomes)

    if imagens:
        analisar_remocao_rastro(imagens)

    print("\n--- Análise Concluída ---")

if __name__ == "__main__":
    main()
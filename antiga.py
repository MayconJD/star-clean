import cv2
import numpy as np
import os
import time

# --- Configurações ---
PASTA_ENTRADA = r'C:\Users\Maycon JD\Pictures\STAR Clean IMAGENS'
PASTA_SAIDA_COMP = r'C:\Users\Maycon JD\Pictures\STAR Clean Comparativo'
ARQUIVO_TRACO = os.path.join(PASTA_SAIDA_COMP, 'IMAGEM_TRACO.png')
ARQUIVO_ANTIGA = os.path.join(PASTA_SAIDA_COMP, 'SOLUCAO_ANTIGA.png')

# Intervalo da cor verde em HSV (Use o mesmo que funcionou antes)
VERDE_MIN = np.array([30, 80, 80])
VERDE_MAX = np.array([90, 255, 255])

# --- Funções ---

def criar_imagem_traco(pasta_in, arq_out):
    """
    Carrega imagens e as mescla usando o método de 'Máximo'
    para realçar o rastro do satélite.
    """
    print(f"Iniciando criação de '{os.path.basename(arq_out)}'...")
    arquivos = sorted([f for f in os.listdir(pasta_in) if f.lower().endswith(('.png', '.jpg', '.jpeg'))])

    if not arquivos:
        print(f"Nenhuma imagem encontrada em: {pasta_in}")
        return None

    imagens_bgr = []
    for nome_arquivo in arquivos:
        caminho_completo = os.path.join(pasta_in, nome_arquivo)
        img = cv2.imread(caminho_completo)
        if img is not None:
            imagens_bgr.append(img)
        else:
            print(f"Aviso: Não foi possível carregar {nome_arquivo}")

    if not imagens_bgr:
        print("Nenhuma imagem válida carregada.")
        return None

    print(f"Mesclando {len(imagens_bgr)} imagens com método 'Máximo'...")
    start_time = time.time()

    # Empilha as imagens (N, H, W, 3)
    pilha_bgr = np.stack(imagens_bgr, axis=0)

    # Calcula o valor máximo ao longo do eixo N (axis=0)
    imagem_maximo = np.max(pilha_bgr, axis=0).astype(np.uint8)

    end_time = time.time()
    print(f"Mesclagem 'Máximo' concluída em {end_time - start_time:.2f} segundos.")

    # Salva a imagem com o traço
    cv2.imwrite(arq_out, imagem_maximo)
    print(f"Imagem com traço salva em: {arq_out}")
    return arq_out


def criar_solucao_antiga(arq_in, arq_out, verde_min, verde_max):
    """
    Carrega a imagem com o traço, detecta o verde e o substitui por preto.
    """
    print(f"\nIniciando criação de '{os.path.basename(arq_out)}'...")
    img = cv2.imread(arq_in)
    if img is None:
        print(f"Erro ao carregar a imagem de traço: {arq_in}")
        return None

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mascara_verde = cv2.inRange(hsv, verde_min, verde_max)

    # Opcional: Dilatar a máscara para pegar halos, se necessário
    # kernel = np.ones((3, 3), np.uint8) # Kernel menor pode ser suficiente
    # mascara_verde = cv2.dilate(mascara_verde, kernel, iterations=1)

    # Cria uma cópia para modificar
    img_modificada = img.copy()

    # Onde a máscara é verde (maior que 0), define os pixels para preto [0, 0, 0]
    img_modificada[mascara_verde > 0] = [0, 0, 0]

    # Salva a imagem com o traço preto
    cv2.imwrite(arq_out, img_modificada)
    print(f"Imagem com traço preto salva em: {arq_out}")
    return arq_out


# --- Execução Principal ---

def main():
    print("--- Iniciando Script Comparativo ---")

    # Cria a pasta de saída se ela não existir
    if not os.path.exists(PASTA_SAIDA_COMP):
        os.makedirs(PASTA_SAIDA_COMP)
        print(f"Pasta de saída criada: {PASTA_SAIDA_COMP}")

    # Verifica se a pasta de entrada existe
    if not os.path.exists(PASTA_ENTRADA):
        print(f"ERRO: A pasta de entrada '{PASTA_ENTRADA}' não foi encontrada.")
        return

    # Etapa 1: Criar a imagem com o traço visível
    caminho_traco = criar_imagem_traco(PASTA_ENTRADA, ARQUIVO_TRACO)

    # Etapa 2: Criar a imagem com o traço preto (se a Etapa 1 funcionou)
    if caminho_traco:
        criar_solucao_antiga(caminho_traco, ARQUIVO_ANTIGA, VERDE_MIN, VERDE_MAX)

    print("\n--- Script Comparativo Concluído ---")


# Executa o script
if __name__ == "__main__":
    main()
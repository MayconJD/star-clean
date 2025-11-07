import cv2
import numpy as np
import os
import time

# --- Configurações ---
PASTA_ENTRADA = r'C:\Users\Maycon JD\Pictures\STAR Clean IMAGENS'
PASTA_SAIDA = r'C:\Users\Maycon JD\Pictures\STAR Clean'
IMAGEM_FINAL = os.path.join(PASTA_SAIDA, 'resultado_final_20s.png')

# Intervalo da cor verde em HSV
VERDE_MIN = np.array([30, 80, 80])
VERDE_MAX = np.array([90, 255, 255])

# Tamanho do Kernel para Dilatação
TAMANHO_KERNEL_DILATACAO = 5

# --- NOVO: Limiar para Fundo Preto ---
# Pixels com todos os canais BGR abaixo deste valor serão considerados
# fundo e ignorados na mesclagem. Ajuste se necessário.
# Comece baixo (ex: 15-30) para não remover estrelas fracas.
LIMIAR_FUNDO_PRETO = 25

# --- Funções ---

def processar_imagem(caminho_imagem, caminho_saida):
    """
    Carrega, detecta verde, DILATA a máscara e torna transparente.
    """
    img = cv2.imread(caminho_imagem)
    if img is None:
        print(f"Erro ao carregar: {caminho_imagem}")
        return None

    img_rgba = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mascara_verde = cv2.inRange(hsv, VERDE_MIN, VERDE_MAX)

    kernel = np.ones((TAMANHO_KERNEL_DILATACAO, TAMANHO_KERNEL_DILATACAO), np.uint8)
    mascara_dilatada = cv2.dilate(mascara_verde, kernel, iterations=1)

    img_rgba[:, :, 3] = np.where(mascara_dilatada > 0, 0, 255)

    cv2.imwrite(caminho_saida, img_rgba)
    print(f"Processada e salva: {caminho_saida}")
    return caminho_saida

def mesclar_isolando_estrelas(caminhos_imagens, caminho_saida_final, threshold):
    """
    Mescla imagens ignorando satélite E fundo preto, usando np.nanmedian.
    """
    print("Carregando imagens para mesclagem...")
    imagens_rgba = []
    for p in caminhos_imagens:
        img = cv2.imread(p, cv2.IMREAD_UNCHANGED)
        if img is not None and img.shape[2] == 4:
            imagens_rgba.append(img)
        else:
            print(f"Aviso: Não foi possível carregar ou não é RGBA: {p}")

    if not imagens_rgba:
        print("Nenhuma imagem RGBA válida foi carregada para mesclagem.")
        return

    print(f"Mesclando {len(imagens_rgba)} imagens...")
    start_time = time.time()

    pilha_rgba = np.stack(imagens_rgba, axis=0) # (N, H, W, 4)
    pilha_bgr = pilha_rgba[:, :, :, :3].astype(float)
    pilha_alfa = pilha_rgba[:, :, :, 3]

    # --- DEBUG: Checa valores Alfa ---
    min_alfa, max_alfa = np.min(pilha_alfa), np.max(pilha_alfa)
    print(f"Valores Alfa (Min/Max): {min_alfa} / {max_alfa}")
    if max_alfa == 0:
        print("!!! ERRO CRÍTICO: Todas as imagens parecem ter Alfa=0. Verifique as .png tratadas.")
        return
    # --------------------------------

    # Máscara 1: Onde Alfa é 0 (satélite)
    mascara_transparente = pilha_alfa == 0 # (N, H, W)

    # Máscara 2: Onde BGR é 'preto' (abaixo do limiar)
    # np.all verifica se TODOS os canais BGR estão abaixo do limiar
    mascara_preto = np.all(pilha_bgr < threshold, axis=3) # (N, H, W)

    # Máscara Combinada: Onde é transparente OU preto
    mascara_combinada = mascara_transparente | mascara_preto # (N, H, W)

    # Aplica a máscara: Onde for True, vira NaN
    pilha_bgr[np.broadcast_to(mascara_combinada[..., None], pilha_bgr.shape)] = np.nan

    # Calcula a mediana, ignorando NaN
    print("Calculando mediana (ignorando fundo preto e satélite)...")
    imagem_final_float = np.nanmedian(pilha_bgr, axis=0)

    # Converte NaN (pixels sempre removidos) para 0 e volta para uint8
    imagem_final_bgr = np.nan_to_num(imagem_final_float, nan=0.0).astype(np.uint8)

    end_time = time.time()
    print(f"Mesclagem concluída em {end_time - start_time:.2f} segundos.")

    cv2.imwrite(caminho_saida_final, imagem_final_bgr)
    print(f"Imagem final mesclada salva em: {caminho_saida_final}")

    # Verifica se a imagem final não é toda preta
    if np.all(imagem_final_bgr == 0):
        print("\n!!! AVISO: A imagem final AINDA está preta! !!!")
        print("Tente aumentar o 'LIMIAR_FUNDO_PRETO' (ex: 30, 40) ou verifique")
        print("se as estrelas nas imagens originais são muito fracas ou se")
        print("as imagens tratadas estão corretas.")
    else:
        nao_pretos = np.count_nonzero(imagem_final_bgr)
        print(f"Imagem final gerada com {nao_pretos} pixels não-pretos.")

# --- Execução Principal ---

def main():
    if not os.path.exists(PASTA_SAIDA):
        os.makedirs(PASTA_SAIDA)
        print(f"Pasta de saída criada: {PASTA_SAIDA}")

    if not os.path.exists(PASTA_ENTRADA):
        print(f"ERRO: A pasta de entrada '{PASTA_ENTRADA}' não foi encontrada.")
        return

    imagens_processadas = []
    arquivos = sorted([f for f in os.listdir(PASTA_ENTRADA) if f.lower().endswith(('.png', '.jpg', '.jpeg'))])

    if not arquivos:
        print(f"Nenhuma imagem encontrada na pasta: {PASTA_ENTRADA}")
        return

    print(f"Encontradas {len(arquivos)} imagens. Iniciando processamento...")

    for nome_arquivo in arquivos:
        caminho_completo = os.path.join(PASTA_ENTRADA, nome_arquivo)
        nome_base, _ = os.path.splitext(nome_arquivo)
        caminho_saida_img = os.path.join(PASTA_SAIDA, f"{nome_base}_tratado.png")
        resultado = processar_imagem(caminho_completo, caminho_saida_img)
        if resultado:
            imagens_processadas.append(resultado)

    print("\nProcessamento individual concluído.")
    print("Iniciando mesclagem com remoção de fundo...")

    # Chama a nova função de mesclagem com o limiar
    mesclar_isolando_estrelas(imagens_processadas, IMAGEM_FINAL, LIMIAR_FUNDO_PRETO)

    print("\nSimulação concluída!")

if __name__ == "__main__":
    main()
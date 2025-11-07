# Simulando o Impacto do Lançamento de Satélites nas Observações Astronômicas - Solução STAR Clean
## 🧩 1. antiga.py — Método Clássico de Remoção de Rastro

🧠 Descrição

Este script aplica uma máscara de cor verde para detectar e remover rastros de satélites visíveis nas imagens astronômicas.



Ele representa a versão original (ou de referência) da técnica usada no projeto.

🔍 Funcionamento

-Carrega uma imagem com o traço do satélite.

-Converte para o espaço de cores HSV.

-Cria uma máscara para identificar pixels verdes (verde_min e verde_max).

-Substitui os pixels identificados por preto (0, 0, 0).

-Salva o resultado na pasta de saída.

📤 Saída esperada

SOLUCAO_ANTIGA.png → imagem final com os rastros removidos (em preto).

<img width="1920" height="1080" alt="SOLUCAO_ANTIGA" src="https://github.com/user-attachments/assets/cac46f42-bba4-447b-bce5-1fca493ce0c0" />


## 🚀 2. script.py — Solução STAR Clean

🧠 Descrição

O script.py é uma versão aprimorada da solução anterior.

Ele combina múltiplas imagens da mesma região do céu, detectando o movimento dos satélites e removendo-os automaticamente com um método de mesclagem inteligente e pós-processamento.

🔍 Funcionamento

-Carrega todas as imagens(snapshots) de uma pasta de entrada.

-Converte cada imagem para HSV e aplica a máscara de cor verde.

-Remove as áreas afetadas e combina as imagens limpas.

-Gera uma imagem final com melhor preservação das estrelas e menos artefatos.

📤 Saída esperada

STAR_CLEAN_FINAL.png → imagem limpa, sem rastros visíveis.
<img width="1920" height="1080" alt="resultado_final_20s" src="https://github.com/user-attachments/assets/16c2b6db-1ce7-4313-a8e9-c6dd0ae38ca0" />


## ⚖️ 3. comparacao.py — Teste de Desempenho e Qualidade

🧠 Descrição

O comparacao.py serve para comparar visualmente e em desempenho os resultados entre o método antigo (antiga.py) e o novo (script.py).

Ele gera uma imagem comparativa, facilitando a análise de eficiência e precisão de remoção dos rastros.


🔍 Funcionamento

-Combina todas as imagens da pasta de entrada usando o método de máximo para gerar o rastro do satélite.

<img width="1920" height="1080" alt="IMAGEM_TRACO" src="https://github.com/user-attachments/assets/18e56ad0-bd9c-430f-985c-c0d4125fbea9" />

-Aplica o método antigo de remoção de rastro (mesmo processo do antiga.py).

-Salva os resultados e mede o tempo de execução de cada etapa.

-O código lê os resultados gerados pelos diferentes métodos (por exemplo, antigo e novo) e organiza essas informações em estruturas comparáveis (arrays, dataframes, etc.).

-São aplicadas funções estatísticas para avaliar a diferença entre os métodos:

  -- Usa np.mean(valores) para calcular a média da variável selecionada;
  
  -- Usa np.std(valores) para calcular o desvio padrão (padrão populacional, não amostral);
  
  -- Usa mean_absolute_error(valores, media)(isto mede o erro médio entre cada valor e a média ou seja, quão distante os dados estão da média); 
  
  -- Usa np.corrcoef(valores1, valores2)[0,1] para calcular a correlação de Pearson entre duas variáveis (se o usuário escolher duas colunas). Caso só uma variável seja escolhida, o cálculo é ignorado. 
  
-Essas análises permitem medir a precisão e a consistência dos resultados.

-As métricas são comparadas entre os métodos para identificar qual apresenta melhor desempenho (menor erro, menor variação, maior correlação).

-O código produz um resumo numérico que destacam as diferenças estatísticas entre os métodos, facilitando a interpretação dos resultados.

-Com base nos valores obtidos, o código indica se há diferença significativa entre os métodos ou se ambos produzem resultados estatisticamente semelhantes.

<img width="587" height="239" alt="image" src="https://github.com/user-attachments/assets/cfb0f07b-baea-4fbf-a1d6-dc2e35bc421a" />



## 🪐 Licença

Este projeto é distribuído sob a licença MIT.



Sinta-se livre para estudar, modificar e contribuir!

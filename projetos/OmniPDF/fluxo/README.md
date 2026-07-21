📖 Fluxo da Aba Leitor
Etapa	Descrição
1. Upload	Usuário envia um arquivo PDF.
2. Configuração (sidebar)	Escolhe voz, velocidade, página inicial, ativa leitura contínua e define quantas páginas avançar.
3. Extração de texto	O sistema extrai o texto centralizado da página atual (ignorando cabeçalhos/rodapés) com @st.cache_data para reuso.
4. Exibição	Mostra o texto extraído na área principal.
5. Narração	Ao clicar em Narrar:
- Textos das páginas selecionadas são coletados (com cache).
- Áudios são gerados em paralelo (máx. 5 concorrentes) via edge-tts.
- Um player HTML é renderizado com os áudios e inicia a reprodução, avançando automaticamente para a próxima página ao final de cada áudio.
6. Saída	Áudio é reproduzido no navegador; texto permanece visível.
🛠️ Fluxo da Aba Ferramentas
Cada ferramenta segue o padrão: upload do PDF, configuração específica (se houver), processamento e download.

🔗 Juntar PDFs
Upload: Múltiplos PDFs.

Processamento: Ordena e mescla em um único PDF usando pypdf.PdfWriter.

Saída: Download do PDF unido.

✂️ Reorganizar ou Dividir
Upload: PDF único.

Configuração: Ordem personalizada (ex: "3,1,2,4") OU intervalo de páginas.

Processamento: Reorganiza páginas ou extrai intervalo.

Saída: Download do PDF reorganizado ou do intervalo.

📄 Extrair Texto / OCR
Extração de texto: Extrai todo o texto com pypdf, exibe prévia e permite download .txt.

OCR: Para PDFs escaneados, utiliza pytesseract (requer Tesseract instalado). O processo é progressivo com barra de progresso.

🗜️ Compressão e Marca d'Água
Compressão: Comprime os streams de conteúdo com compress_content_streams().

Marca d'água: Insere texto com opacidade em todas as páginas usando reportlab.

🖼️ Exportar como PNG
Upload: PDF.

Configuração: Lista de páginas (ex: "1,3,5").

Processamento: Usa PyMuPDF para renderizar cada página como PNG com fator de escala 1.5.

Saída: ZIP com as imagens.

✏️ Anotação Simples
Upload: PDF.

Configuração: Número da página, texto da anotação e posição (X,Y).

Processamento: Overlay de texto na página especificada com reportlab.

Saída: Download do PDF anotado.

📦 Processamento em Lote
Upload: Múltiplos PDFs.

Configuração: Operação (Extrair texto ou Comprimir).

Processamento: Aplica a operação a cada arquivo e empacota em um ZIP.

Saída: Download do ZIP.

✍️ Fluxo da Aba Assinar
Etapa	Descrição
1. Upload	PDF e imagem da assinatura (PNG/JPG).
2. Configuração (sidebar)	Número da página, posição X/Y e escala da imagem.
3. Processamento	Cria overlay da imagem sobre a página indicada usando reportlab e pypdf.merge_page.
4. Saída	Download do PDF com a assinatura aplicada.

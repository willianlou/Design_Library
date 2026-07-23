import asyncio
import base64
import html
import io
import re
import zipfile
from typing import List, Tuple, Optional

import edge_tts
import pypdf
import streamlit as st
import streamlit.components.v1 as components
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

# ======================== DEPENDÊNCIAS OPCIONAIS ========================
try:
    import fitz  # PyMuPDF
except ImportError:
    fitz = None

try:
    import pytesseract
    from PIL import Image
except ImportError:
    pytesseract = None
    Image = None

# ======================== CONFIGURAÇÃO DA PÁGINA ========================
st.set_page_config(
    page_title="Leitor PDF Pro",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="auto",
)

# ======================== KEEPALIVE (SIMULADO) ========================
def inject_keepalive():
    """Função dummy para manter compatibilidade (substitua se necessário)."""
    pass

inject_keepalive()

# ======================== CSS PERSONALIZADO ========================
st.markdown("""
<style>
/* Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Inter:opsz@14..32&family=Space+Grotesk:wght@500;600;700&display=swap');

/* Variáveis */
:root {
    --ink: #0f172a;
    --muted: #64748b;
    --primary: #6366f1;
    --primary-light: #818cf8;
    --primary-dark: #4f46e5;
    --soft: #f1f5f9;
    --line: #e2e8f0;
    --bg: #fafbff;
    --card-bg: #ffffff;
    --radius: 16px;
    --shadow: 0 4px 24px rgba(0,0,0,0.04);
}

/* Reset */
html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, sans-serif;
}

.stApp {
    background: var(--bg);
    color: var(--ink);
}

[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    max-width: 1200px;
    padding: 2rem 2.5rem 4rem;
}

/* Brand */
.brand {
    display: flex;
    align-items: center;
    gap: 0.85rem;
    margin-bottom: 0.25rem;
}
.brand-mark {
    width: 52px;
    height: 52px;
    border-radius: 16px;
    display: grid;
    place-items: center;
    font: 700 26px 'Space Grotesk', sans-serif;
    color: white;
    background: linear-gradient(135deg, #6366f1, #a78bfa);
    box-shadow: 0 12px 28px rgba(99,102,241,0.3);
}
.brand-name {
    font: 700 2rem 'Space Grotesk', sans-serif;
    letter-spacing: -0.03em;
    color: var(--ink);
}
.brand-subtitle {
    color: var(--muted);
    margin: -0.2rem 0 2rem 4.2rem;
    font-size: 1rem;
    font-weight: 400;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 0.25rem;
    border-bottom: 1px solid var(--line);
}
.stTabs [data-baseweb="tab"] {
    height: 3rem;
    padding: 0 1.25rem;
    color: var(--muted);
    font-weight: 600;
    font-size: 0.95rem;
}
.stTabs [aria-selected="true"] {
    color: var(--primary);
}
.stTabs [data-baseweb="tab-highlight"] {
    background: var(--primary);
    height: 3px;
    border-radius: 3px;
}

/* Buttons */
.stButton > button,
.stDownloadButton > button {
    border-radius: 12px;
    border: 1px solid var(--line);
    background: var(--card-bg);
    min-height: 2.75rem;
    font-weight: 600;
    transition: all 0.15s ease;
    box-shadow: 0 1px 2px rgba(0,0,0,0.02);
}
.stButton > button:hover,
.stDownloadButton > button:hover {
    border-color: var(--primary);
    color: var(--primary);
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(99,102,241,0.15);
}
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #6366f1, #818cf8);
    border: 0;
    color: #fff;
    box-shadow: 0 8px 20px rgba(99,102,241,0.25);
}
.stButton > button[kind="primary"]:hover {
    background: linear-gradient(135deg, #4f46e5, #6366f1);
    transform: translateY(-2px);
    box-shadow: 0 12px 28px rgba(99,102,241,0.35);
}

/* File uploader */
[data-testid="stFileUploader"] {
    border: 1.5px dashed #c7d2fe;
    border-radius: var(--radius);
    background: #f8faff;
    padding: 0.25rem;
}
[data-testid="stFileUploader"] section {
    padding: 0.75rem;
}

/* Inputs */
.stTextArea textarea,
.stTextInput input,
.stNumberInput input {
    border-radius: 12px;
    border-color: var(--line);
    background: white;
}
.stTextArea textarea:focus,
.stTextInput input:focus,
.stNumberInput input:focus {
    border-color: var(--primary);
    box-shadow: 0 0 0 3px rgba(99,102,241,0.1);
}

/* Alerts */
.stAlert {
    border-radius: 14px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #f8f9fe;
    border-right: 1px solid #e9edfb;
}
section[data-testid="stSidebar"] .block-container {
    padding: 2rem 1.25rem;
}

/* Metrics */
div[data-testid="stMetric"] {
    background: var(--card-bg);
    border: 1px solid var(--line);
    border-radius: var(--radius);
    padding: 1.25rem 1rem;
    box-shadow: var(--shadow);
}

/* Headers */
h1, h2, h3, h4 {
    font-family: 'Space Grotesk', sans-serif;
    letter-spacing: -0.02em;
}
h2 {
    margin-top: 1.5rem;
    font-size: 1.6rem;
}
h3 {
    font-size: 1.2rem;
}

/* Dividers */
hr {
    margin: 2rem 0;
    border: 0;
    border-top: 1px solid var(--line);
}

/* Custom cards */
.custom-card {
    background: var(--card-bg);
    border-radius: var(--radius);
    padding: 1.5rem;
    box-shadow: var(--shadow);
    border: 1px solid var(--line);
}

/* Progress bar */
[data-testid="stProgress"] > div > div {
    background: linear-gradient(90deg, #6366f1, #a78bfa);
}

/* Responsive */
@media (max-width: 640px) {
    .block-container { padding: 1.5rem; }
    .brand-name { font-size: 1.5rem; }
    .brand-subtitle { margin-left: 0; }
}
</style>
""", unsafe_allow_html=True)

# ======================== FUNÇÕES AUXILIARES ========================

def pdf_bytes(arquivo) -> io.BytesIO:
    """Converte um arquivo (UploadedFile ou bytes) em BytesIO."""
    if hasattr(arquivo, "getvalue"):
        return io.BytesIO(arquivo.getvalue())
    return io.BytesIO(arquivo)

def ler(arquivo) -> pypdf.PdfReader:
    """Retorna um PdfReader a partir de um arquivo."""
    return pypdf.PdfReader(pdf_bytes(arquivo))

def escrever_pdf(writer: pypdf.PdfWriter) -> bytes:
    """Escreve um PdfWriter em bytes."""
    saida = io.BytesIO()
    writer.write(saida)
    return saida.getvalue()

def download(nome: str, dados: bytes, tipo: str = "application/pdf"):
    """Botão de download unificado."""
    st.download_button(
        label=f"⬇️ Baixar {nome}",
        data=dados,
        file_name=nome,
        mime=tipo,
        key=f"dl_{nome}_{hash(dados)}"
    )

# ======================== FUNÇÕES CORE COM CACHE ========================

@st.cache_data(show_spinner=False)
def extrair_texto(arquivo_bytes: bytes) -> str:
    """Extrai todo o texto de um PDF."""
    reader = pypdf.PdfReader(io.BytesIO(arquivo_bytes))
    partes = []
    for num, pagina in enumerate(reader.pages, 1):
        texto = pagina.extract_text() or ""
        partes.append(f"--- Página {num} ---\n{texto}")
    return "\n\n".join(partes)

@st.cache_data(show_spinner=False)
def texto_centralizado(arquivo_bytes: bytes, pagina_numero: int) -> str:
    """Extrai o texto do corpo central da página (ignora cabeçalhos/rodapés)."""
    if fitz is None:
        # Fallback para pypdf
        reader = pypdf.PdfReader(io.BytesIO(arquivo_bytes))
        return reader.pages[pagina_numero - 1].extract_text() or ""

    doc = fitz.open(stream=arquivo_bytes, filetype="pdf")
    pagina = doc.load_page(pagina_numero - 1)
    largura, altura = pagina.rect.width, pagina.rect.height
    blocos = pagina.get_text("blocks")
    corpo = []
    for bloco in blocos:
        if len(bloco) < 5:
            continue
        x0, y0, x1, y1, texto = bloco[:5]
        texto = texto.strip()
        if texto and x0 >= largura * 0.12 and x1 <= largura * 0.88 and y0 >= altura * 0.10 and y1 <= altura * 0.90:
            corpo.append((y0, x0, texto))
    corpo.sort(key=lambda item: (item[0], item[1]))
    return "\n".join(item[2] for item in corpo)

# ======================== ÁUDIO E PLAYER ========================

async def gerar_audio_edge(texto: str, voz: str, velocidade: float) -> bytes:
    """Gera áudio via Edge TTS."""
    percentual = int((velocidade - 1) * 100)
    sinal = "+" if percentual >= 0 else ""
    comunicador = edge_tts.Communicate(texto, voz, rate=f"{sinal}{percentual}%")
    audio = b""
    async for parte in comunicador.stream():
        if parte["type"] == "audio":
            audio += parte["data"]
    return audio

async def gerar_varios_audios(textos: List[str], voz: str, velocidade: float, progresso=None) -> List[bytes]:
    """Gera múltiplos áudios em paralelo com limite de concorrência."""
    semaforo = asyncio.Semaphore(5)
    total = len(textos)

    async def limitada(idx, texto):
        async with semaforo:
            if progresso is not None:
                progresso.progress((idx + 1) / total, f"Gerando áudio {idx+1}/{total}")
            return await gerar_audio_edge(texto, voz, velocidade)

    tarefas = [limitada(i, t) for i, t in enumerate(textos)]
    return await asyncio.gather(*tarefas)

def player_continuo(audios: List[bytes], paginas: List[int]):
    """Player HTML com áudios embutidos e avanço automático."""
    if not audios:
        return
    encoded = [base64.b64encode(a).decode("ascii") for a in audios]
    fontes_js = "[" + ",".join(f"'data:audio/mp3;base64,{e}'" for e in encoded) + "]"
    paginas_js = str(paginas).replace(" ", "")

    markup = f"""
    <div style="font-family:Inter,sans-serif;padding:12px 0;color:#0f172a">
      <div style="display:flex;align-items:center;gap:12px;margin-bottom:8px">
        <span style="font-weight:600;font-size:15px;">🔊 Página <span id="label">{paginas[0]}</span></span>
        <span style="font-size:13px;color:#64748b;">• reprodução contínua</span>
      </div>
      <audio id="player" controls autoplay style="width:100%;border-radius:12px;"></audio>
      <div style="font-size:13px;color:#64748b;margin-top:6px;">⏭️ A próxima página será iniciada automaticamente.</div>
    </div>
    <script>
      const audios = {fontes_js};
      const paginas = {paginas_js};
      let indice = 0;
      const player = document.getElementById('player');
      const label = document.getElementById('label');
      function tocar() {{
        player.src = audios[indice];
        label.textContent = paginas[indice];
        player.play().catch(() => {{}});
      }}
      player.addEventListener('ended', () => {{
        if (indice < audios.length - 1) {{ indice += 1; tocar(); }}
      }});
      tocar();
    </script>
    """
    components.html(markup, height=130)

# ======================== OPERAÇÕES COM PDF ========================

def juntar_pdfs(arquivos) -> bytes:
    """Junta múltiplos PDFs em um único."""
    writer = pypdf.PdfWriter()
    for arquivo in arquivos:
        for pagina in ler(arquivo).pages:
            writer.add_page(pagina)
    return escrever_pdf(writer)

def reorganizar_pdf(arquivo, ordem: str) -> bytes:
    """Reorganiza páginas conforme ordem fornecida (ex: '3,1,2')."""
    reader = ler(arquivo)
    total = len(reader.pages)
    indices = []
    for item in ordem.split(","):
        item = item.strip()
        if item:
            try:
                idx = int(item) - 1
                if idx < 0 or idx >= total:
                    raise ValueError(f"Página {item} inválida (deve estar entre 1 e {total})")
                indices.append(idx)
            except ValueError:
                raise ValueError(f"Valor inválido: '{item}'")
    if not indices:
        raise ValueError("Nenhuma página válida fornecida.")
    writer = pypdf.PdfWriter()
    for idx in indices:
        writer.add_page(reader.pages[idx])
    return escrever_pdf(writer)

def dividir_pdf(arquivo, inicio: int, fim: int) -> bytes:
    """Extrai um intervalo de páginas."""
    reader = ler(arquivo)
    total = len(reader.pages)
    if inicio < 1 or fim > total or inicio > fim:
        raise ValueError("Intervalo inválido.")
    writer = pypdf.PdfWriter()
    for idx in range(inicio - 1, fim):
        writer.add_page(reader.pages[idx])
    return escrever_pdf(writer)

def comprimir_pdf(arquivo) -> bytes:
    """Comprime o PDF (comprime streams de conteúdo)."""
    reader = ler(arquivo)
    writer = pypdf.PdfWriter()
    for pagina in reader.pages:
        pagina.compress_content_streams()
        writer.add_page(pagina)
    return escrever_pdf(writer)

def overlay_texto(largura, altura, texto, x, y, tamanho, cor, opacidade=1.0) -> io.BytesIO:
    """Cria um PDF overlay com texto."""
    saida = io.BytesIO()
    c = canvas.Canvas(saida, pagesize=(largura, altura))
    c.setFillAlpha(opacidade)
    c.setFillColorRGB(*cor)
    c.setFont("Helvetica", tamanho)
    c.drawString(x, y, texto)
    c.save()
    saida.seek(0)
    return saida

def aplicar_marca_dagua(arquivo, texto: str, opacidade: float) -> bytes:
    """Aplica marca d'água em todas as páginas."""
    reader = ler(arquivo)
    writer = pypdf.PdfWriter()
    for pagina in reader.pages:
        largura, altura = float(pagina.mediabox.width), float(pagina.mediabox.height)
        marca = pypdf.PdfReader(overlay_texto(largura, altura, texto, largura*0.2, altura*0.5, 36, (0.6,0.6,0.6), opacidade))
        pagina.merge_page(marca.pages[0])
        writer.add_page(pagina)
    return escrever_pdf(writer)

def adicionar_anotacao(arquivo, pagina_numero: int, texto: str, x: float, y: float) -> bytes:
    """Adiciona uma nota em uma página específica."""
    reader = ler(arquivo)
    writer = pypdf.PdfWriter()
    for idx, pagina in enumerate(reader.pages, 1):
        if idx == pagina_numero:
            largura, altura = float(pagina.mediabox.width), float(pagina.mediabox.height)
            nota = pypdf.PdfReader(overlay_texto(largura, altura, "Nota: " + texto, x, y, 11, (0.8,0.35,0.05)))
            pagina.merge_page(nota.pages[0])
        writer.add_page(pagina)
    return escrever_pdf(writer)

def exportar_imagens(arquivo, paginas: List[int]) -> bytes:
    """Exporta páginas como imagens PNG em um ZIP."""
    if fitz is None:
        raise RuntimeError("PyMuPDF não instalado.")
    doc = fitz.open(stream=pdf_bytes(arquivo).getvalue(), filetype="pdf")
    zip_bytes = io.BytesIO()
    with zipfile.ZipFile(zip_bytes, "w", zipfile.ZIP_DEFLATED) as pacote:
        for num in paginas:
            if num < 1 or num > len(doc):
                continue
            pagina = doc.load_page(num - 1)
            pix = pagina.get_pixmap(matrix=fitz.Matrix(1.5, 1.5), alpha=False)
            pacote.writestr(f"pagina-{num}.png", pix.tobytes("png"))
    return zip_bytes.getvalue()

def ocr_pdf(arquivo, idioma: str, progresso=None) -> str:
    """Executa OCR local usando Tesseract."""
    if fitz is None or pytesseract is None or Image is None:
        raise RuntimeError("Instale PyMuPDF, Pillow e pytesseract. Tesseract também deve estar instalado.")
    try:
        pytesseract.get_tesseract_version()
    except Exception:
        raise RuntimeError("Tesseract não encontrado no sistema. Instale e configure o PATH.")
    doc = fitz.open(stream=pdf_bytes(arquivo).getvalue(), filetype="pdf")
    textos = []
    total = len(doc)
    for i, pagina in enumerate(doc, 1):
        if progresso is not None:
            progresso.progress(i / total, f"OCR página {i}/{total}")
        pix = pagina.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)
        img = Image.open(io.BytesIO(pix.tobytes("png")))
        texto = pytesseract.image_to_string(img, lang=idioma)
        textos.append(f"--- Página {i} ---\n{texto}")
    return "\n\n".join(textos)

def criar_overlay_assinatura(imagem_bytes, largura, altura, x, y, escala) -> io.BytesIO:
    """Cria overlay com imagem de assinatura."""
    leitor = ImageReader(io.BytesIO(imagem_bytes))
    iw, ih = leitor.getSize()
    saida = io.BytesIO()
    c = canvas.Canvas(saida, pagesize=(largura, altura))
    c.drawImage(leitor, x, y, width=iw*escala, height=ih*escala, mask="auto")
    c.save()
    saida.seek(0)
    return saida

def assinar_pdf(arquivo, imagem_bytes, pagina_numero: int, x: float, y: float, escala: float) -> bytes:
    """Insere imagem de assinatura em uma página."""
    reader = ler(arquivo)
    pagina = reader.pages[pagina_numero - 1]
    overlay = pypdf.PdfReader(criar_overlay_assinatura(
        imagem_bytes, float(pagina.mediabox.width), float(pagina.mediabox.height), x, y, escala
    ))
    pagina.merge_page(overlay.pages[0])
    writer = pypdf.PdfWriter()
    for p in reader.pages:
        writer.add_page(p)
    return escrever_pdf(writer)

# ======================== PAINÉIS ========================

def painel_leitor():
    """Aba de leitura com narração contínua."""
    st.markdown("### 📖 Leitor com Voz")
    arquivo = st.file_uploader("Selecione um PDF", type="pdf", key="leitor_pdf")
    if not arquivo:
        st.info("Envie um PDF para começar.")
        return

    arquivo_bytes = arquivo.getvalue()
    reader = ler(arquivo_bytes)
    total = len(reader.pages)

    # Sidebar
    with st.sidebar:
        st.markdown("#### Configurações de Leitura")
        st.metric("Total de páginas", total)
        estilo = st.selectbox("Estilo da voz", ["Homem (Antônio)", "Mulher (Francisca)"])
        velocidade = st.slider("Velocidade", 0.7, 1.5, 1.0, 0.05)
        st.divider()
        pagina_numero = st.number_input("Ir para página", 1, total, 1, step=1)
        modo_continuo = st.toggle("Leitura contínua", value=True, help="Narra as próximas páginas automaticamente.")
        if modo_continuo:
            max_paginas = min(10, total - pagina_numero + 1)
            quantidade = st.slider("Quantas páginas adiante", 1, max_paginas, min(3, max_paginas))
        else:
            quantidade = 1
        st.divider()
        st.caption("📌 O texto exibido é o corpo central da página (ignora cabeçalhos e rodapés).")

    # Obter texto centralizado com cache
    texto = texto_centralizado(arquivo_bytes, pagina_numero)
    st.markdown(f"#### Página {pagina_numero}")
    if texto.strip():
        with st.expander("📝 Visualizar texto", expanded=True):
            st.text_area("Conteúdo", texto, height=300, label_visibility="collapsed")
        col1, col2 = st.columns([1, 3])
        with col1:
            if st.button("🔊 Narrar", type="primary"):
                voz = "pt-BR-AntonioNeural" if "Homem" in estilo else "pt-BR-FranciscaNeural"
                paginas = list(range(pagina_numero, min(total, pagina_numero + quantidade - 1) + 1)) if modo_continuo else [pagina_numero]
                # Pega textos e filtra vazios
                textos = []
                paginas_validas = []
                for p in paginas:
                    t = texto_centralizado(arquivo_bytes, p)
                    if t.strip():
                        textos.append(t)
                        paginas_validas.append(p)
                if not textos:
                    st.warning("Nenhum texto centralizado legível nessas páginas.")
                    return

                progresso = st.progress(0, text="Gerando áudios...")
                try:
                    audios = asyncio.run(gerar_varios_audios(textos, voz, velocidade, progresso))
                except Exception as e:
                    st.error(f"Erro ao gerar áudio: {e}")
                    return
                progresso.empty()
                player_continuo(audios, paginas_validas)
    else:
        st.warning("Não foi possível extrair texto centralizado nesta página. Tente usar OCR na aba 'Ferramentas'.")

def painel_ferramentas():
    """Aba com todas as ferramentas de edição e extração."""
    st.markdown("### 🛠️ Ferramentas PDF")

    # ---------------------- JUNTAR ----------------------
    with st.expander("🔗 Juntar PDFs", expanded=False):
        arquivos = st.file_uploader("Selecione dois ou mais PDFs (ordem importa)", type="pdf", accept_multiple_files=True, key="merge")
        if arquivos and len(arquivos) >= 2 and st.button("Juntar", key="btn_merge"):
            with st.spinner("Juntando PDFs..."):
                resultado = juntar_pdfs(arquivos)
                download("documento-unido.pdf", resultado)

    # ---------------------- REORGANIZAR / DIVIDIR ----------------------
    with st.expander("✂️ Reorganizar ou Dividir", expanded=False):
        arq = st.file_uploader("PDF para reorganizar", type="pdf", key="reorg")
        if arq:
            total = len(ler(arq).pages)
            st.caption(f"Total de páginas: {total}")
            col1, col2 = st.columns(2)
            with col1:
                nova_ordem = st.text_input("Nova ordem (ex: 3,1,2,4)", key="order_input", placeholder="3,1,2,4")
                if nova_ordem and st.button("Reorganizar", key="btn_reorg"):
                    try:
                        resultado = reorganizar_pdf(arq, nova_ordem)
                        download("reorganizado.pdf", resultado)
                    except ValueError as e:
                        st.error(str(e))
            with col2:
                inicio = st.number_input("Página inicial", 1, total, 1, key="split_start")
                fim = st.number_input("Página final", 1, total, total, key="split_end")
                if st.button("Extrair intervalo", key="btn_split"):
                    if inicio <= fim:
                        resultado = dividir_pdf(arq, inicio, fim)
                        download(f"intervalo_{inicio}-{fim}.pdf", resultado)
                    else:
                        st.error("Início deve ser menor ou igual ao fim.")

    # ---------------------- EXTRAIR TEXTO & OCR ----------------------
    with st.expander("📄 Extrair Texto / OCR", expanded=False):
        arq_texto = st.file_uploader("PDF para extração", type="pdf", key="text_extract")
        if arq_texto:
            if st.button("Extrair texto (sem OCR)", key="btn_extract"):
                with st.spinner("Extraindo..."):
                    texto = extrair_texto(arq_texto.getvalue())
                    st.text_area("Prévia", texto, height=200)
                    download("texto-extraido.txt", texto.encode("utf-8"), "text/plain")
            st.markdown("---")
            idioma = st.selectbox("Idioma do OCR", ["por", "eng", "spa", "fra"], key="ocr_lang")
            if st.button("🔍 Executar OCR (local)", key="btn_ocr"):
                try:
                    progresso = st.progress(0, text="OCR em andamento...")
                    texto_ocr = ocr_pdf(arq_texto, idioma, progresso)
                    progresso.empty()
                    st.text_area("Texto reconhecido", texto_ocr, height=200)
                    download("texto-ocr.txt", texto_ocr.encode("utf-8"), "text/plain")
                except Exception as e:
                    st.error(f"Erro no OCR: {e}")

    # ---------------------- COMPRESSÃO & MARCA D'ÁGUA ----------------------
    with st.expander("🗜️ Compressão e Marca d'Água", expanded=False):
        arq_extra = st.file_uploader("PDF para comprimir ou marcar", type="pdf", key="extra")
        if arq_extra:
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Comprimir PDF", key="btn_compress"):
                    with st.spinner("Comprimindo..."):
                        resultado = comprimir_pdf(arq_extra)
                        download("comprimido.pdf", resultado)
            with col2:
                marca_texto = st.text_input("Texto da marca d'água", "CONFIDENCIAL", key="watermark_text")
                opacidade = st.slider("Opacidade", 0.1, 1.0, 0.25, 0.05, key="wm_opacity")
                if st.button("Aplicar marca d'água", key="btn_watermark"):
                    with st.spinner("Aplicando..."):
                        resultado = aplicar_marca_dagua(arq_extra, marca_texto, opacidade)
                        download("com-marca.pdf", resultado)

    # ---------------------- EXPORTAR IMAGENS ----------------------
    with st.expander("🖼️ Exportar páginas como PNG", expanded=False):
        arq_img = st.file_uploader("PDF para exportar", type="pdf", key="img_export")
        if arq_img:
            total = len(ler(arq_img).pages)
            paginas_input = st.text_input("Páginas (ex: 1,3,5)", "1", key="img_pages")
            if st.button("Exportar PNGs", key="btn_export_img"):
                try:
                    numeros = [int(x.strip()) for x in paginas_input.split(",") if x.strip()]
                    if any(n < 1 or n > total for n in numeros):
                        st.error("Páginas inválidas.")
                    else:
                        with st.spinner("Exportando..."):
                            zip_data = exportar_imagens(arq_img, numeros)
                            download("paginas-png.zip", zip_data, "application/zip")
                except ValueError:
                    st.error("Formato inválido. Use números separados por vírgula.")

    # ---------------------- ANOTAÇÃO ----------------------
    with st.expander("✏️ Anotação simples", expanded=False):
        arq_note = st.file_uploader("PDF para anotar", type="pdf", key="note_pdf")
        if arq_note:
            total = len(ler(arq_note).pages)
            col1, col2 = st.columns(2)
            with col1:
                pagina_note = st.number_input("Página", 1, total, 1, key="note_page")
                texto_note = st.text_input("Texto da anotação", key="note_text")
            with col2:
                x_note = st.number_input("Posição X", 0.0, 2000.0, 72.0, key="note_x")
                y_note = st.number_input("Posição Y", 0.0, 2000.0, 72.0, key="note_y")
            if texto_note and st.button("Adicionar anotação", key="btn_note"):
                with st.spinner("Adicionando..."):
                    resultado = adicionar_anotacao(arq_note, pagina_note, texto_note, x_note, y_note)
                    download("anotado.pdf", resultado)

    # ---------------------- PROCESSAMENTO EM LOTE ----------------------
    with st.expander("📦 Processamento em lote", expanded=False):
        lote = st.file_uploader("Selecione vários PDFs", type="pdf", accept_multiple_files=True, key="batch")
        operacao = st.selectbox("Operação", ["Extrair texto", "Comprimir PDFs"], key="batch_op")
        if lote and st.button("Processar lote", key="btn_batch"):
            with st.spinner("Processando lote..."):
                zip_out = io.BytesIO()
                with zipfile.ZipFile(zip_out, "w", zipfile.ZIP_DEFLATED) as pacote:
                    for arquivo in lote:
                        nome_base = re.sub(r"\.pdf$", "", arquivo.name, flags=re.I)
                        if operacao == "Extrair texto":
                            dados = extrair_texto(arquivo.getvalue()).encode("utf-8")
                            pacote.writestr(f"{nome_base}.txt", dados)
                        else:  # comprimir
                            dados = comprimir_pdf(arquivo)
                            pacote.writestr(f"{nome_base}_comprimido.pdf", dados)
                download("resultado-lote.zip", zip_out.getvalue(), "application/zip")

def painel_assinatura():
    """Aba para inserir assinatura visual."""
    st.markdown("### ✍️ Assinar PDF (visual)")
    col1, col2 = st.columns(2)
    with col1:
        documento = st.file_uploader("PDF", type="pdf", key="sign_pdf")
    with col2:
        imagem = st.file_uploader("Imagem da assinatura (PNG/JPG)", type=["png", "jpg", "jpeg"], key="sign_img")
    if not documento or not imagem:
        st.info("Envie o PDF e uma imagem da assinatura.")
        return

    total = len(ler(documento).pages)
    with st.sidebar:
        st.markdown("#### Posicionamento")
        pagina = st.number_input("Página", 1, total, 1, key="sign_page")
        x = st.number_input("Posição X", 0.0, 2000.0, 72.0, key="sign_x")
        y = st.number_input("Posição Y", 0.0, 2000.0, 72.0, key="sign_y")
        escala = st.number_input("Escala", 0.05, 3.0, 0.35, 0.05, key="sign_scale")
        if st.button("Aplicar assinatura", type="primary", key="btn_sign"):
            with st.spinner("Inserindo assinatura..."):
                resultado = assinar_pdf(documento, imagem.getvalue(), pagina, x, y, escala)
                download("documento-assinado.pdf", resultado)
    st.caption("ℹ️ Assinatura visual apenas, sem valor jurídico de certificação digital.")

# ======================== MAIN ========================

def main():
    # Cabeçalho
    st.markdown("""
    <div class="brand">
        <div class="brand-mark">📄</div>
        <div class="brand-name">OmniPDF</div>
    </div>
    <p class="brand-subtitle">Leitura inteligente, edição e organização de PDFs — tudo local e gratuito.</p>
    """, unsafe_allow_html=True)

    # Abas
    tab1, tab2, tab3 = st.tabs(["📖 Leitor", "🛠️ Ferramentas", "✍️ Assinar"])
    with tab1:
        painel_leitor()
    with tab2:
        painel_ferramentas()
    with tab3:
        painel_assinatura()

if __name__ == "__main__":
    main()
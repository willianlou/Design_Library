# 💻 Código e Implementação - Leitor PDF Pro

### 🛠️ Stack Tecnológica
- `Python` 3.9+
- `Streamlit` – interface web interativa
- `PyPDF2` / `pypdf` – manipulação de PDFs
- `edge-tts` – síntese de voz natural
- `ReportLab` – geração de overlays (marca d'água, anotações)
- `PyMuPDF` – extração precisa de texto e exportação de imagens
- `pytesseract` + `Pillow` – OCR para PDFs escaneados

### ⚙️ Componentes & Otimizações
- Aplicação principal em `app.py`
- Módulos separados por responsabilidade (`pdf_utils`, `audio_utils`, `ocr_utils`, `ui_components`, `config`)
- Cache com `@st.cache_data` para extração de texto
- Geração paralela de áudio com `asyncio` e limite de concorrência
- Player HTML contínuo com avanço automático entre páginas
- Recursos estáticos (CSS, logo) em `assets/`
- Dependências declaradas em `requirements.txt`
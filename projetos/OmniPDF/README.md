# 💡 Ideia e Contexto - OminiPDF

## ❌ O Problema

Ler documentos longos em PDF no computador pode ser cansativo e pouco acessível. 
Muitas vezes, o usuário precisa:

- **Navegar por páginas densas** sem recursos de leitura assistida.
- **Extrair trechos ou páginas** manualmente, recorrendo a ferramentas pagas ou complicadas.
- **Realizar OCR** em PDFs escaneados, o que exige softwares especializados e caros.
- **Adicionar anotações, marcas d'água ou assinaturas** sem perder a formatação original.
- **Processar múltiplos PDFs** em lote, tarefa repetitiva e demorada quando feita uma a uma.

Além disso, ferramentas online gratuitas muitas vezes impõem limites de tamanho, enviam dados para servidores externos (comprometendo a privacidade) ou exibem anúncios intrusivos.

## 🚀 A Solução

**Leitor PDF Pro** é uma aplicação web local que reúne, em uma única interface, as principais funcionalidades de manipulação de PDFs com foco em:

- **Leitura assistida por voz**: narração contínua com vozes naturais (Edge TTS), ajuste de velocidade e avanço automático entre páginas.
- **Organização e edição**: juntar, dividir, reorganizar, comprimir e extrair texto de PDFs.
- **Reconhecimento de texto (OCR)**: converte PDFs escaneados em texto editável, usando Tesseract localmente.
- **Anotações e marcação**: insere anotações, marcas d'água e assinaturas visuais sem alterar o layout original.
- **Processamento em lote**: aplica operações a vários arquivos de uma vez, gerando um único pacote ZIP.

Tudo funciona **localmente** – nenhum dado é enviado para a nuvem, garantindo privacidade total. A interface é intuitiva, responsiva e gratuita, construída com Python e Streamlit.

## 📈 Valor para o Portfólio

Este projeto evidencia competências técnicas e de design de solução, como:

- **Arquitetura modular**: separação clara entre interface, lógica de negócio e integrações com bibliotecas externas.
- **Otimização de performance**: uso de cache, paralelismo assíncrono (asyncio) e limites de concorrência para melhorar a experiência do usuário.
- **Interdisciplinaridade**: combina processamento de documentos, síntese de voz, OCR e geração de relatórios.
- **Privacidade por design**: todos os processamentos são locais, reforçando boas práticas de segurança.
- **Documentação e estruturação**: projeto com README, fluxos mapeados e código organizado, pronto para colaboração ou evolução futura.

Além disso, o Leitor PDF Pro resolve um problema real do dia a dia, mostrando capacidade de entregar valor prático com ferramentas open source.


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
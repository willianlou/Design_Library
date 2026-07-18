### 3️⃣ `codigo/README.md`

```markdown
# 💻 Código e Implementação - Phish Guard

### 🛠️ Stack Tecnológica
- `JavaScript (ES6+)`
- `Chromium Extension API (Manifest V3)`
- `HTML5 / CSS3` (Páginas internas de Alerta)

### 📂 Estrutura Modular do Repositório
O projeto é dividido entre scripts de plano de fundo (Service Workers),
scripts de contexto de página e módulos analíticos isolados:

phish-guard/
├── background.js          # Service Worker central - Gerenciador de Eventos
├── content.js             # Injetado na página - Manipula e protege o DOM
├── blocked.html           # Tela de bloqueio estática (Redirecionamento)
└── modules/               # Motores Isolados de Heurística
    ├── risk.js            # Concentra a lógica matemática do Score
    ├── domain.js          # Parser e higienização de URLs
    ├── settings.js        # Gerenciador de estado e persistência de configs
    ├── reputation.js      # Verificador de idade de domínio (Simulação Local/WHOIS)
    ├── webmail.js         # Tratamento especial para provedores (Gmail, Outlook)
    └── blocklist.js       # Repositório local de IOCs (Indicadores de Comprometimento)
# 💻 Código e Implementação - NexusPrompt
### 🛠️ Stack Tecnológica
- `JavaScript (ES6+)`
- `Chromium Web Extensions API (Manifest V3)`
- `HTML5 / CSS3` (Interface do Popup de gerenciamento)

### 📂 Arquitetura de Pastas de Engenharia
```text
agent-bridge/
├── popup.html             # Interface gráfica de gerenciamento
├── popup.js               # Controla o chaveamento de perfis manuais/automáticos
├── content.js             # Intercepta eventos de teclado e manipula inputs no DOM
└── core/
    └── core.js            # Biblioteca agnóstica - O coração de orquestração local
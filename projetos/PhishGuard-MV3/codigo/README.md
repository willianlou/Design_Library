PhishGuard é uma extensão de navegador (Manifest V3) que protege usuários contra ameaças online como phishing, malware e sites fraudulentos, utilizando análise local heurística e listas de confiança. Diferente de soluções baseadas em nuvem, nenhum dado é enviado para servidores externos, garantindo privacidade total.

A extensão atua como um assistente de decisão, exibindo uma pontuação de risco (0–100%) para cada site acessado e permitindo que o usuário decida se deseja prosseguir ou bloquear o acesso.

🎯 Público-alvo
Usuários com pouca experiência digital (idosos, crianças).

Pessoas que desejam uma camada extra de proteção sem dependência de serviços online.

Empresas que buscam uma solução de segurança leve e local.

🚀 Funcionalidades Principais
Funcionalidade	Descrição
Análise heurística local	Calcula um score de risco baseado em 12 critérios (TLDs suspeitos, typosquatting, palavras-chave, etc.)
Listas de confiança	Whitelist automática (domínios confiáveis) + whitelist do usuário (armazenada localmente)
Blacklist local	Domínios catalogados como maliciosos (atualizáveis via JSON)
Página de análise interativa	Exibe o score, motivos, lista de testes realizados e botões de decisão
Bloqueio transparente	Redireciona para página de bloqueio com explicação do motivo
Badge no canto da tela	Indica visualmente se o site é confiável, desconhecido ou perigoso
Privacidade total	Nenhuma requisição externa; todas as análises são feitas localmente
Personalizável	Listas de TLDs, palavras suspeitas e extensões podem ser editadas no código

🛠️ Stack Tecnológica
Linguagem: JavaScript (ES6+)

API do Navegador: Chromium Extension API (Manifest V3)

Interface: HTML5 + CSS3 (páginas internas de análise e bloqueio)

Persistência: chrome.storage.local (whitelist do usuário)

Modelo de módulos: ES Modules (import/export) no Service Worker


PhishGuard-MV3/
├── manifest.json
├── background/
│   └── service-worker.js          # Service Worker principal
├── content/
│   └── intent-engine.js           # Script injetado (badge)
├── pages/
│   ├── analyzing.html             # Página de análise interativa
│   ├── analyzing.css              # Estilos da página de análise
│   ├── analyzing.js               # Lógica da página de análise
│   ├── blocked.html               # Página de bloqueio
│   ├── blocked.css                # Estilos da página de bloqueio
│   └── blocked.js                 # Lógica da página de bloqueio
├── utils/
│   ├── constants.js               # Constantes (TLDs, padrões, listas)
│   ├── domain-utils.js            # Funções de análise e pontuação
│   ├── whitelist.json             # Lista de domínios confiáveis
│   └── blacklist.json             # Lista de domínios maliciosos
├── assets/
│   ├── icon16.png
│   ├── icon48.png
│   └── icon128.png
└── README.md






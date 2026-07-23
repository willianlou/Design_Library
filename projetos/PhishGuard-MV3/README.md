❌ O Problema
O phishing moderno é extremamente ágil. Criminosos conseguem subir páginas falsas – clones de bancos, portais corporativos e telas de login – e descartá-las em poucas horas. As abordagens tradicionais de segurança falham contra ataques Zero-Day porque dependem de bases de dados globais (blocklists) que demoram horas ou dias para serem atualizadas.

Além disso, extensões que protegem o usuário enviando as URLs acessadas para servidores de terceiros violam a privacidade de navegação, expondo dados sensíveis e criando um ponto central de falha.

🚀 A Solução
O Phish Guard é uma linha de defesa local em formato de extensão de navegador que avalia o risco de fraudes de forma 100% isolada e assíncrona, garantindo a privacidade do usuário. Ele analisa sinais comportamentais, semânticos e temporais diretamente no cliente (client-side) para calcular um score de risco e tomar ações defensivas imediatas.

Diferencial: não é um bloqueador automático, mas sim um assistente de decisão – ele alerta, mostra o domínio, apresenta uma pontuação clara e deixa o usuário escolher se deseja prosseguir. Essa abordagem é especialmente eficaz para usuários com pouca experiência digital (idosos, crianças), pois interrompe o clique automático e força uma reflexão antes de acessar sites desconhecidos.

🧠 O que já está implementado
Atualmente, o Phish Guard opera com duas camadas analíticas:

URL Engine

Extrai e normaliza o domínio (remove www.).

Detecta IPs puros, TLDs suspeitos (.top, .xyz, etc.), typosquatting (similaridade com domínios conhecidos), homógrafos Unicode e palavras-chave maliciosas.

Calcula um score de risco (0–100%) baseado em 12 critérios heurísticos.

Reputation Engine (local)

Mantém listas estáticas de domínios confiáveis (whitelist.json) e maliciosos (blacklist.json).

Permite ao usuário construir sua própria whitelist personalizada, armazenada localmente via chrome.storage.

Domínios essenciais (Google, Microsoft, GitHub, etc.) são sempre liberados sem análise.

🧪 Em desenvolvimento (próximas camadas)
A arquitetura do Phish Guard foi projetada para operar com 4 camadas analíticas complementares – duas já estão em produção e duas estão em fase de planejamento:

Download Engine (em estudo)

Interceptará a criação de arquivos perigosos originados de fontes não confiáveis, bloqueando downloads de executáveis suspeitos ou arquivos com extensões de risco (.exe, .msi, .vbs, etc.) antes que sejam salvos no disco.

Intent Engine (em desenvolvimento)

Realizará análise heurística comportamental do HTML/DOM para rastrear intenções maliciosas – por exemplo, presença de campos de senha combinados com palavras de urgência como "verify", "sua conta será bloqueada" ou "atualize seus dados".

Essa camada permitirá neutralizar ameaças antes mesmo que o domínio entre em listas de reputação, detectando páginas de phishing que ainda não foram catalogadas.

🔒 Privacidade em primeiro lugar
Todas as análises são feitas exclusivamente no navegador do usuário.

Nenhuma URL, domínio ou dado pessoal é enviado para servidores externos.

Nenhuma telemetria ou estatística é coletada.

As listas de bloqueio/confiança são armazenadas localmente e podem ser atualizadas pelo usuário.
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






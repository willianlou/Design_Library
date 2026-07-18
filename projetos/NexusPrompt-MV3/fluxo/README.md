# 🔄 Fluxo e Arquitetura - NexusPrompt

O Agent Bridge opera de forma transparente entre a intenção do usuário e o campo de entrada nativo do ecossistema de LLMs.

### 🗺️ Pipeline de Roteamento de Prompt (Core Logic)

```mermaid
graph TD
    A[Usuário digita comando simples] --> B[Content Script intercepta ENTER / CTRL+ENTER]
    B --> C[core.js: normalizeText]
    C --> D[core.js: keywordScore]
    C --> E[core.js: detectComplexity]
    
    D -->|Avalia pesos de palavras-chave| F{Define Perfil Router}
    E -->|Analisa tamanho/regras/estruturas| G{Define Nível de Complexidade}
    
    F -->|Ex: Alta pontuação técnica| H[Perfil: CODING]
    G -->|Ex: Longo / Presença de instruções SQL| I[Complexidade: ALTA]
    
    H & I --> J[selectCapability: Seleciona Agente Avançado]
    J --> K[sanitizeMemory: Coleta e limpa APS_MEMORY]
    K --> L[optimizePrompt: Monta o payload estruturado]
    
    L --> M[Injeta Marcador Mestre: AGENT_BRIDGE:v2]
    M --> N[Injeta resultado final na caixa de entrada da IA]
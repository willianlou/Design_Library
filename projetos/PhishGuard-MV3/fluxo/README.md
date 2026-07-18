# 🔄 Fluxo e Arquitetura - Phish Guard

O ciclo de vida do Phish Guard é baseado em eventos assíncronos disparados pelo navegador. 
Diferente de ferramentas invasivas, ele analisa a página imediatamente após o carregamento para evitar latência na navegação.

### 🗺️ Pipeline de Execução (Event Lifecycle)

```mermaid
graph TD
    A[Usuário acessa URL] --> B[Chrome abre a página]
    B --> C[Event: webNavigation.onCompleted / tabs.onUpdated]
    C --> D[Função: inspectTab]
    D --> E[Busca configurações locais: getSettings]
    E --> F{Domínio é confiável?}
    
    F -->|Sim| G[Libera Navegação]
    F -->|Não| H[Inicia Cálculo de Risco / Heurísticas]
    
    H --> H1[Blocklist? +100]
    H1 --> H2[Brand Spoofing? +25]
    H2 --> H3[Punycode? +35]
    H3 --> H4[IP Puro? +40]
    H4 --> H5[Idade Domínio < 15 dias? +30]
    
    H5 --> I{Avaliação do Score Final}
    
    I -->|Score < 60: Baixo Risco| J[Envia dados ao Content Script]
    J --> K[Content Script monitora DOM/Forms]
    
    I -->|Score >= 60: Alto Risco| L[Altera Badge da Extensão]
    L --> M[Redireciona para blocked.html]

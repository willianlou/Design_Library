🔄 Fluxo e Arquitetura - Phish Guard
O ciclo de vida do Phish Guard é baseado em eventos assíncronos disparados pelo navegador, utilizando o Manifest V3 com Service Worker como plano de fundo.
A interceptação ocorre antes do carregamento da página (webNavigation.onBeforeNavigate), 
garantindo que a análise seja feita previamente e o usuário seja redirecionado para a página de análise 
ou bloqueio sem nunca ver o conteúdo suspeito.

📋 Descrição Detalhada do Fluxo
Interceptação

O Service Worker escuta o evento webNavigation.onBeforeNavigate para todas as abas (frame principal).

A URL é capturada antes do carregamento.

Pré-processamento

Extrai o domínio (getDomainFromUrl) e normaliza removendo www. (normalizeDomain).

Verifica se é uma página restrita (chrome://, chrome-extension://, about:). Se sim, libera imediatamente.

Verificações Rápidas (Liberação)

Essenciais: Domínios como google.com, gmail.com etc. (lista ESSENTIAL_DOMAINS) – liberados sem análise.

Whitelist automática: Domínios carregados do whitelist.json (exceto os excluídos) – liberados.

Whitelist do usuário: Domínios adicionados pelo usuário via chrome.storage.local – liberados.

Blacklist

Se o domínio estiver na blacklistSet (carregada do blacklist.json), redireciona para blocked.html com motivo "blacklist" e score 0.

Análise Heurística (Score)

Para domínios não classificados, calcula um score de 0–100 usando a função calculateScore (em utils/domain-utils.js).

O score começa em 100 e sofre penalidades conforme 12 critérios (TLD suspeito, typosquatting, palavras-chave, etc.).

O resultado é passado como parâmetro na URL para a página de análise.

Página de Análise (analyzing.html)

Exibe a URL em destaque e uma animação de progresso.

Após a conclusão, mostra:

Score final com cor (verde/amarelo/vermelho).

Motivos resumidos (ex: "Domínio com características perigosas").

Lista detalhada de testes realizados (cada teste com ✔️ ou ❌), gerada por getTestResults.

Dica de segurança aleatória.

Botões:

"Prosseguir para o Site" – envia decisão allow para o Service Worker.

"Adicionar à Lista de Confiáveis" – adiciona o domínio à whitelist do usuário.

"Voltar" – retorna à página anterior.

Decisão do Usuário

Prosseguir: O Service Worker adiciona o domínio à whitelist do usuário (se ainda não estiver) e navega para a URL original.

Bloquear/Voltar: Redireciona para blocked.html com motivo "user_blocked".

Adicionar à whitelist: Apenas adiciona o domínio à whitelist sem navegar (o usuário deve clicar em "Prosseguir" depois).

Página de Bloqueio (blocked.html)

Exibe a URL bloqueada, o score (se disponível) e o motivo.

Oferece um botão "Prosseguir com Cuidado" que navega diretamente para a URL após confirmação.

Badge Visual (Content Script)

O script content/intent-engine.js é injetado em todas as páginas (document_start).

Consulta o Service Worker (checkDomain) para saber o status do domínio atual.

Injeta um badge no canto inferior direito:

🛡️ "Site Confiável" (verde) para whitelist.

⚠️ "Site Desconhecido" (amarelo) para domínios não classificados.

🚫 "Site Perigoso" (vermelho) para blacklist.


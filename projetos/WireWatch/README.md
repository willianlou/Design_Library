# NetworkSentinel

Ferramenta Windows para monitorar conexoes de rede e destacar trafego suspeito por processo.

## Recursos

- Dashboard visual nativo para Windows.
- Lista conexoes TCP/UDP ativas com processo, PID, endereco local/remoto e status.
- Categoriza portas por tipo: Web, DNS, Email, SSH/Admin, Banco de Dados, RDP e outras.
- Importa logs JSON/JSONL exportados do Elastic/Kibana.
- Gera uma amostra de dados para demonstracao e testes.
- Grava sessoes de escuta por 5 min, 15 min, 30 min ou 1 hora.
- Mostra graficos de risco e categorias de porta.
- Marca risco por heuristicas simples e explicaveis.
- Detecta portas remotas incomuns, muitos destinos em janela curta, conexoes externas por processo sensivel e processos com nome suspeito.
- Le logs JSONL para analise visual.

Use o executavel visual:

## Uso principal

- **Elastic/log** importa arquivos `.json`, `.jsonl` ou `.ndjson` exportados do Elastic/Kibana.
- **Gerar amostra** cria eventos simulados para validar tabela, graficos e classificacao.
- **Escuta** define a duracao da gravacao: 5 min, 15 min, 30 min ou 1 hora.
- **Gravar** inicia a captura temporizada e salva em `capture-session.jsonl`.
- A aba **Graficos** mostra distribuicao por risco e top categorias de portas.

## Observacoes

Esta versao nao inspeciona o conteudo dos pacotes. Ela analisa conexoes e comportamento por processo usando comandos e APIs locais do Windows.

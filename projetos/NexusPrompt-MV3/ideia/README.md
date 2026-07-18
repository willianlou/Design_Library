# 💡 Ideia e Contexto - Nexusprompt

## 📂 Categoria: IA / Extensão de Navegador (Manifest V3)

### ❌ O Problema
Trabalhar eficientemente com Grandes Modelos de Linguagem (LLMs) como ChatGPT, Claude e Gemini exige que o usuário constantemente 
forneça contextos ricos (ex: *"Aja como um engenheiro sênior, siga os padrões Clean Code, considere a stack X"*). 
Reescrever ou copiar e colar essas instruções repetidamente causa a chamada **fadiga de prompt**. 

Além disso, chats longos sofrem com o estouro da janela de contexto (Token Window), 
fazendo com que a IA misture logs antigos, repita erros já corrigidos ou simplesmente esqueça regras cruciais definidas no início da sessão.
### 🚀 A Solução
O **Agent Bridge** atua como um **Local Prompt Router & Context Management Engine**. 
Ele intercepta comandos simples do usuário diretamente no campo de entrada do navegador e, através de um motor de análise estática e heurística local ele
envelopa o pedido em uma estrutura semântica otimizada contendo instruções avançadas de comportamento e uma memória persistente de curto/médio prazo.
Tudo isso ocorre no cliente (client-side), sem latência e sem custo de tokens adicionais para classificação.

### 🌟 O Diferencial: Consolidação de Memória Crítica
Para mitigar a perda de contexto sem estourar o limite de tokens, o Agent Bridge implementa um compressor contextual inteligente (`buildConsolidationPrompt`).
Ele intercepta históricos massivos e ruidosos (de até 28 mil caracteres), aplicando algoritmos de higienização local que filtram logs inúteis e redundâncias,
reduzindo o estado do projeto para um bloco estruturado de exatos 2.400 caracteres com decisões de arquitetura e próximos passos consolidados.
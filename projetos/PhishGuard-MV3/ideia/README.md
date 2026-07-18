# 💡 Ideia e Contexto - Phish Guard

## 📂 Categoria: Segurança / Extensão Chromium (MV3)

### ❌ O Problema
O phishing moderno é extremamente ágil.
Criminosos conseguem subir páginas falsas (clones de bancos, portais corporativos e telas de login) e descartá-las em poucas horas.
As abordagens tradicionais de segurança falham contra ataques *Zero-Day*
porque dependem de bases de dados globais (blocklists) que demoram horas ou dias para serem atualizadas. 
Além disso, extensões que protegem o usuário enviando as URLs acessadas para servidores de terceiros
violam a privacidade de navegação.

### 🚀 A Solução
O **Phish Guard** é uma linha de defesa local em formato de extensão de navegador que 
avalia o risco de fraudes de forma 100% isolada e assíncrona, garantindo a privacidade do usuário.
Ele analisa sinais comportamentais, semânticos e temporais diretamente no cliente (client-side) para calcular um score de risco 
e tomar ações defensivas imediatas.
### 🧠 Visão de Futuro: O Quarto Motor (Intent Engine)
A arquitetura do Phish Guard foi projetada para operar em 4 camadas analíticas complementares:
1. **URL Engine:** Identifica anomalias na string de endereço (IPs puros, Punycode).
2. **Reputation Engine:** Avalia metadados de confiança (idade do domínio, listas locais).
3. **Download Engine:** Intercepta a criação de arquivos perigosos originados de fontes não confiáveis.
4. **Intent Engine (Em desenvolvimento):** Análise heurística comportamental do HTML/DOM para rastrear intenções maliciosas
(ex: presença de campos de senha combinados com palavras de urgência como *"verify"* ou *"sua conta será bloqueada"*), 
neutralizando ameaças antes mesmo que o domínio entre em listas de reputação.
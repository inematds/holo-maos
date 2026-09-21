# Análise — o que dá pra fazer com o HOLO na comunidade INEMA

Levantamento feito em **21/09/2026** a partir do post gratuito do Zubair Trabzada
(AI Workshop Lite), do zip e PDF da aula, e do vídeo de 12min32 transcrito.
Fontes (post, vídeo, PDF e transcrição) foram consultadas localmente e **não** ficam neste repositório.

---

## 1. O que é, em uma frase

Uma página HTML + um servidor Python de 180 linhas que usam a **webcam como mouse**:
o MediaPipe reconhece as mãos dentro do navegador e a página traduz belisco, arremesso,
zoom e sinal de paz em manipulação de cartões de notas e modelos 3D.

## 2. O que eu verifiquei rodando aqui (não é resumo de README)

| Verificação | Resultado |
|---|---|
| `python3 server.py` no Linux (spark-922b) | ✅ sobe na 4890, **só biblioteca padrão**, zero `pip install` |
| `GET /`, `/api/notes`, `/api/props` | ✅ 200 — página de 88 KB, notas e 2 modelos `.glb` |
| Bateria interna `?probe=1` no Chromium headless | ✅ **26/26 PASS**, nenhum erro de JS |
| Tamanho real | 77 MB clonado (o peso é o wasm do MediaPipe + os `.glb`) |
| Privacidade | ✅ MediaPipe **embarcado na pasta**, sem CDN, sem key, sem conta |

**Conclusão técnica:** roda no Linux sem tocar uma linha, embora a documentação dele só
fale de Mac/Windows. Isso já é um diferencial nosso — ninguém precisa de Mac.

## 3. O que é grátis e o que é isca (importante pra não prometer errado)

No vídeo o próprio autor separa: **"this Jarvis is not free on GitHub"**. O que é MIT e
livre é só a camada de gestos (HOLO). O JARVIS completo — telefone que liga de verdade,
inbox, agenda, timer, "AI employees" — é o produto da comunidade paga dele.

Nosso material tem que deixar isso explícito. Vender "o Jarvis do Homem de Ferro" e
entregar um deck de notas é a forma mais rápida de queimar a confiança da comunidade.

## 4. As lacunas — e é aqui que mora o nosso valor

O projeto é 100% em inglês, de ponta a ponta:

| Lacuna encontrada no código | Onde | O que fazer |
|---|---|---|
| Voz do JARVIS fixada em inglês britânico (`/daniel/i`, `v.lang === 'en-GB'`) | `holo.html:729-733` | cair pra `pt-BR` do `speechSynthesis`, ou plugar a voz do **inemavox** (chatterbox / rachel) |
| Falas do assistente em inglês (`'Filed, sir.'`, `'Clean slate, sir.'` …) | `holo.html:~736-745` | ~12 strings — traduzir com voz de mordomo em PT ("Arquivado, senhor.") |
| Legenda de gestos e avisos na tela em inglês (`RETRY CAMERA`, `PINCH ANYWHERE`…) | `holo.html` | tradução direta, é texto curto |
| Notas de exemplo em inglês, sobre a comunidade dele | `sample-notes/` | trocar por notas INEMA — aí o demo já vira conteúdo nosso |
| Instruções de câmera só pra Mac/Chrome | PDF do autor | escrever o passo a passo Linux/Windows, com o `?sim=1` pra quem não tem webcam |
| Constantes de sensibilidade sem explicação em PT | `PINCH_IN=.30, PINCH_OUT=.42, PINCH_EARN=2, AMP=1.45` | explicar o que cada número faz — é o que faz "não pega meu belisco" virar ajuste de 1 linha |

**Nenhuma dessas mudanças exige tocar no motor de rastreamento.** É tradução + configuração,
o tipo de trabalho que a gente já faz bem e barato.

## 5. O ângulo INEMA (o que NÃO é só traduzir o material dele)

1. **Apontar o `holo.json` para as notas de um curso INEMA.** As pastas viram orbes e os
   arquivos viram cartões — ou seja, dá pra "folhear com as mãos" o material de um curso.
   É uma demonstração de segundo cérebro usando conteúdo que já é nosso.
2. **Voz em português pelo inemavox.** O mordomo falando PT-BR muda completamente a
   recepção com o público 40+, que é o público do INEMA.PRO.
3. **Acessibilidade, não cosplay do Homem de Ferro.** Controlar a tela sem encostar no
   mouse tem leitura óbvia pra quem tem limitação motora ou dor no punho. Esse é o
   enquadramento que diferencia nosso conteúdo do "olha que legal" do YouTube.
4. **Prova de que roda em Linux/GPU server**, com o 26/26 documentado.

## 6. Formatos possíveis, com custo e o que cada um exige

| Formato | Esforço | Custo direto | Quando faz sentido |
|---|---|---|---|
| **Guia de projeto** (skill `projetos-landing-guia`, página `guia/index.html`) | baixo | 1–2 gerações de imagem (capa/banner via Codex) | **entrada natural**: "rode em 2 minutos", gestos, ajustes, créditos |
| **Curso** (`formato-curso-v2` ou `v5`) | alto | tradução PT/EN/ES medida em ~US$ 0,52 de API para 3 cursos inteiros (relatório de 21/09/2026) — o caro é o tempo de autoria, não a API | só se o tema render 4 trilhas: visão computacional no navegador, gesto→evento, privacidade local |
| **Vídeo/Reel de demonstração** | médio | render local | o gesto é visualmente viral; o sinal de paz que "desfaz a bagunça" é o gancho |
| **Post na Comunidade VIP** (e-mail/Telegram) | baixo | zero | divulgação depois que o guia estiver no ar |

## 7. Recomendação

**Fazer o guia de projeto primeiro** (`guia/index.html` neste repo, publicado no GitHub Pages
e registrado no portal), com a adaptação PT-BR mínima junto: voz em português, as ~12 falas
do mordomo traduzidas, legenda traduzida e notas de exemplo do INEMA. É o menor caminho até
algo que a comunidade *usa no mesmo dia*, e já produz o material bruto (prints, clipes de
gesto) para o vídeo e para o post VIP depois.

Curso só depois disso, se o guia mostrar tração — e aí você precisa escolher entre
**v2** e **v5**, que é decisão sua, não minha.

## 8. O que ficou fora deste levantamento

- Os **12 comentários** do post não vêm no HTML renderizado (carregam por chamada separada);
  não fui atrás deles. Seriam úteis pra saber onde as pessoas travam na instalação.
- Não testei com **câmera real** — o servidor aqui não tem webcam. A validação foi pelo
  `?probe=1` e pelo `?sim=1`, que exercitam o motor com mãos sintéticas.
- Não avaliei desempenho em máquina fraca (o público 40+ costuma estar em notebook modesto).

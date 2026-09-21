#!/usr/bin/env python3
"""Aplica a camada PT-BR do INEMA em cima do HOLO original (upstream/).

Por que patch e nao um fork: o codigo do Zubair continua evoluindo (v7 e contando).
Mantendo a traducao como um conjunto de substituicoes exatas, um `git pull` no
upstream + rodar isto de novo reaplica tudo. Se uma string mudar la, o script
AVISA em vez de aplicar pela metade — traducao silenciosamente incompleta e pior
que nenhuma.

Uso:  python3 scripts/aplicar-ptbr.py [--upstream upstream] [--check]
"""
import argparse, os, re, shutil, sys

# (o que procurar, pelo que trocar, rotulo)  — tudo substituicao literal e exata.
# Rotulo terminado em "?" = opcional (variante de outra linha; some sem avisar).
SUBS = [
    # ── titulo da pagina ────────────────────────────────────────────────────
    ("<title>HOLO — bare-hand control deck</title>",
     "<title>HOLO — controle com as mãos</title>", "title-zip?"),
    ("<title>HOLO — hand-gesture control deck</title>",
     "<title>HOLO — controle com as mãos</title>", "title2"),

    # ── HUD ─────────────────────────────────────────────────────────────────
    ('<div id="dock"><span>SHELF</span></div>',
     '<div id="dock"><span>PRATELEIRA</span></div>', "dock"),
    ('<i id="ringstate">ACTIVE</i>',
     '<i id="ringstate">ATIVO</i>', "ringstate"),
    ('<span class="chip" id="hands">HANDS ON</span>',
     '<span class="chip" id="hands">MÃOS LIGADAS</span>', "chip-hands"),
    ('<span class="chip off" id="reset">RESET</span>',
     '<span class="chip off" id="reset">REINICIAR</span>', "chip-reset"),
    ('<span class="chip off" id="debug">DEBUG</span>',
     '<span class="chip off" id="debug">DIAGNÓSTICO</span>', "chip-debug"),
    ('<span class="chip off" id="fx">EFFECTS</span>',
     '<span class="chip off" id="fx">EFEITOS</span>', "chip-fx"),
    ('<span class="chip" id="retry">RETRY CAMERA</span>',
     '<span class="chip" id="retry">TENTAR CÂMERA</span>', "chip-retry"),
    ('<span id="status">booting…</span>',
     '<span id="status">iniciando…</span>', "status-boot"),
    ("'HANDS ON' : 'HANDS OFF'", "'MÃOS LIGADAS' : 'MÃOS DESLIGADAS'", "toggle-hands"),
    ("tracking ? 'ACTIVE' : 'PAUSED'", "tracking ? 'ATIVO' : 'PAUSADO'", "toggle-ring"),

    # ── leitor + legenda ────────────────────────────────────────────────────
    ('<div class="hint">PINCH ANYWHERE · TAP · OR CLICK TO CLOSE</div>',
     '<div class="hint">BELISQUE EM QUALQUER LUGAR · TOQUE · OU CLIQUE PARA FECHAR</div>', "hint"),
    ('<b>PINCH</b> grab / tap = open &nbsp;·&nbsp; <b>FLICK</b> throw (off-screen = gone) &nbsp;·&nbsp; <b>2-HAND STRETCH</b> big = read · crush = TL;DR<br>',
     '<b>BELISCAR</b> pega / toque = abre &nbsp;·&nbsp; <b>ARREMESSAR</b> joga (fora da tela = some) &nbsp;·&nbsp; <b>ESTICAR COM 2 MÃOS</b> grande = lê · amassado = resumo<br>', "legend1"),
    ('<b>TWO PINCHES</b> (apart/together) zoom · twist = rotate &nbsp;·&nbsp; <b>2-HAND STRETCH</b> on a held card: big = read · crush = TL;DR · 3D comes APART<br>',
     '<b>DOIS BELISCOS</b> (afasta/junta) zoom · torcendo = gira &nbsp;·&nbsp; <b>ESTICAR</b> um cartão na mão: grande = lê · amassado = resumo · 3D se DESMONTA<br>', "legend2"),
    ('<b>PEACE ✌</b> = RESET everything &nbsp;·&nbsp; dock right = shelf &nbsp;·&nbsp; <b>J</b> jarvis mode &nbsp;·&nbsp; <b>F</b> = EFFECTS (pull · palm-hold push · ink · clap · tidy)<br>',
     '<b>PAZ ✌</b> = ARRUMA TUDO &nbsp;·&nbsp; leve até a direita = prateleira &nbsp;·&nbsp; <b>J</b> modo mordomo &nbsp;·&nbsp; <b>F</b> = EFEITOS (puxar · empurrar · desenhar · palma · arrumar)<br>', "legend3"),
    ('<b>3D PROPS</b> stretch = comes APART · shrink = back together &nbsp;·&nbsp; drop any .glb into props/',
     '<b>OBJETOS 3D</b> esticar = DESMONTA · encolher = monta de volta &nbsp;·&nbsp; jogue qualquer .glb em props/', "legend4"),

    # ── pedido de camera ────────────────────────────────────────────────────
    ('<b>HOLO needs your camera</b><br>',
     '<b>O HOLO precisa da sua câmera</b><br>', "perm-title"),
    ("""  Hand tracking runs entirely on this page — frames never leave your machine and no AI watches the feed.
  Allow the camera, then just reach out and touch things. (Press <b>H</b> for mouse-only mode.)""",
     """  O rastreamento das mãos acontece inteiro dentro desta página — as imagens não saem do seu
  computador e nenhuma IA fica olhando. Libere a câmera e estenda a mão. (Tecla <b>H</b> usa só o mouse.)""", "perm-body"),
    ("'camera BLOCKED · address-bar camera icon → Allow → RETRY'",
     "'câmera BLOQUEADA · ícone de câmera na barra de endereço → Permitir → TENTAR'", "cam-blocked"),
    ("'no camera found on this machine'",
     "'nenhuma câmera encontrada neste computador'", "cam-none"),
    ("'camera is busy in another app · close it, then RETRY'",
     "'a câmera está ocupada em outro programa · feche e clique TENTAR'", "cam-busy"),
    ("'camera unavailable (' + (name || 'unknown') + ') · RETRY'",
     "'câmera indisponível (' + (name || 'desconhecido') + ') · TENTAR'", "cam-other"),
    ("'hands live · on-device'",
     "'mãos ativas · tudo no seu computador'", "cam-live"),

    # ── voz: inglês britânico fixo → português do Brasil ────────────────────
    ("""  jVoice = vs.find(v => /daniel/i.test(v.name) && v.lang === 'en-GB')
        || vs.find(v => /arthur/i.test(v.name) && v.lang === 'en-GB')
        || vs.find(v => /uk english male/i.test(v.name))
        || vs.find(v => v.lang === 'en-GB') || null; }""",
     """  // INEMA: fala em português do Brasil. Preferimos uma voz masculina pt-BR (o
  // mordomo), caímos pra qualquer pt-BR e só então pro inglês do original.
  jVoice = vs.find(v => /pt[-_]BR/i.test(v.lang) && /(daniel|felipe|ricardo|male|google)/i.test(v.name))
        || vs.find(v => /pt[-_]BR/i.test(v.lang))
        || vs.find(v => /^pt/i.test(v.lang))
        || vs.find(v => v.lang === 'en-GB') || null; }""", "voz"),

    # ── falas do mordomo ────────────────────────────────────────────────────
    ("""  dock:    ['Filed, sir.', 'On the shelf.', 'Pinned for today.'],
  dismiss: ['Discarded.', 'Gone, sir.', "We won't miss it."],
  clear:   ['Clean slate, sir.'],
  tidy:    ['Order restored, sir.', 'Tidied.'],
  pull:    ['Incoming, sir.', 'As requested.'],
  push:    ['Back. All of it.', 'Cleared the air, sir.'],
  ink:     ['Taking dictation, sir.'],""",
     """  dock:    ['Arquivado, senhor.', 'Na prateleira.', 'Separado para hoje.'],
  dismiss: ['Descartado.', 'Foi embora, senhor.', 'Não vai fazer falta.'],
  clear:   ['Mesa limpa, senhor.'],
  tidy:    ['Ordem restaurada, senhor.', 'Tudo no lugar.'],
  pull:    ['Chegando, senhor.', 'Como pediu.'],
  push:    ['De volta. Tudo.', 'Está livre, senhor.'],
  ink:     ['Anotando, senhor.'],""", "falas"),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--upstream', default='upstream')
    ap.add_argument('--check', action='store_true', help='só verifica, não escreve')
    a = ap.parse_args()

    raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    alvo = os.path.join(raiz, a.upstream, 'holo.html')
    if not os.path.exists(alvo):
        sys.exit(f"[ptbr] não achei {alvo} — rode antes: bash scripts/baixar-upstream.sh")

    s = open(alvo, encoding='utf-8').read()
    ja, faltando, feitas = [], [], []
    for velho, novo, rotulo in SUBS:
        if novo in s and velho not in s:
            ja.append(rotulo); continue
        if velho not in s:
            if not rotulo.endswith('?'): faltando.append(rotulo)
            continue
        s = s.replace(velho, novo, 1)
        feitas.append(rotulo)

    if faltando:
        print(f"[ptbr] AVISO: {len(faltando)} trecho(s) não encontrado(s) no upstream "
              f"(provavelmente o autor mudou o código): {', '.join(faltando)}")
        print("[ptbr] a tradução ficaria incompleta — ajuste SUBS em scripts/aplicar-ptbr.py")

    if a.check:
        print(f"[ptbr] check: {len(feitas)} a aplicar, {len(ja)} já aplicadas, {len(faltando)} perdidas")
        sys.exit(1 if faltando else 0)

    if feitas:
        bkp = alvo + '.original'
        if not os.path.exists(bkp):
            shutil.copy(alvo, bkp)
        open(alvo, 'w', encoding='utf-8').write(s)
    print(f"[ptbr] {len(feitas)} trecho(s) traduzido(s), {len(ja)} já estavam, {len(faltando)} perdido(s)")

    # notas de exemplo do INEMA no lugar das notas em inglês do autor
    notas = os.path.join(raiz, 'notas-inema')
    if os.path.isdir(notas):
        cfg = os.path.join(raiz, a.upstream, 'holo.json')
        open(cfg, 'w', encoding='utf-8').write('{"folder": "%s"}\n' % notas)
        print(f"[ptbr] holo.json apontando para {notas}")
    sys.exit(1 if faltando else 0)


if __name__ == '__main__':
    main()

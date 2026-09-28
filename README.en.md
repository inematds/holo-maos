# 🖐️ HOLO Mãos — control your screen with your hands, in Portuguese

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

[![HOLO Mãos](guia/assets/banner.jpg)](https://inematds.github.io/holo-maos/guia/en/)

## 📖 User guide

Complete guide (landing page + step-by-step): **https://inematds.github.io/holo-maos/guia/en/**

An INEMA layer on top of **HOLO** (Zubair Trabzada, AI Workshop): a “deck” that runs in the
browser and turns your webcam into an interface — pinch a card in the air, drag it,
throw it, bring two hands together to zoom, and make the peace sign to put everything back in order.

Nothing goes to the cloud: hand tracking is **Google’s MediaPipe running inside the
page itself**, and camera frames never leave your machine. No API key, no account.

> **This repository is NOT the original project.** HOLO’s code is by Zubair Trabzada,
> MIT, and lives at **https://github.com/zubair-trabzada/holo-gestures**. Here you’ll find:
> the **analysis** of what can be done with this in INEMA ([ANALISE.md](ANALISE.md)), the
> **evidence** that it runs on Linux, and the **Brazilian Portuguese adaptation**.

## Get running in 2 minutes

```bash
bash scripts/baixar-upstream.sh     # clones the official repo into upstream/
python3 scripts/aplicar-ptbr.py     # applies the Brazilian Portuguese layer + INEMA notes
cd upstream && python3 server.py    # Python 3 standard library only
```

Open `http://localhost:4890` in Chrome and allow camera access. No camera? Use
`http://localhost:4890/?sim=1` (synthetic hands) — the mouse also works for everything.

## Tested here (09/21/2026, Linux — spark-922b)

| Item | Result |
|---|---|
| `python3 server.py` | ✅ starts on port 4890, stdlib only |
| `GET /`, `/api/notes`, `/api/props` | ✅ 200 (88 KB page, notes, and 2 3D models) |
| Page loads orbs + 3D models | ✅ deck assembled, no JS errors |
| Internal test suite `?probe=1` (Chromium headless) | ⚠️ passed **26/26** once and then kept stopping at **2/4** — **also in the original code**, without our patch. This is the test touching the card before the camera maps the screen in a headless browser; it’s not a translation regression |

The original documentation mentions
Mac/Windows; **it runs on Linux without changing a single line**.

## The gestures

| Do this | This happens |
|---|---|
| Pinch a card (thumb touches finger) | grabs, drags, and throws it with inertia |
| Quick pinch (tap) | opens the orb folder / opens the note |
| Throw off the screen | the note disappears (bring it back by reopening the orb) |
| Move two pinches apart/together | zoom; twist your hands to rotate the scene |
| Stretch a card with two hands | large = opens the reader; crumpled = the voice reads the summary |
| Hold the peace sign ✌ | **undoes any mess** — the gesture to memorize |
| `F` key | effects: repulsor, pull, drawing, palm, arrange in a grid |
| `J` key | JARVIS mode: turns golden and the voice narrates what your hands are doing |

## The Portuguese layer

`scripts/aplicar-ptbr.py` applies 25 exact replacements to the upstream `holo.html`:
gesture captions, camera warnings, butler lines, and voice selection (from fixed `en-GB`
to `pt-BR`). It saves the original as `holo.html.original` and **warns** if the author
changed any text, rather than partially translating it. After a `git pull` in
upstream, just run it again.

The sample notes in `notas-inema/` replace the author's — `holo.json` automatically
points to them.

## Your own notes

`holo.json` points to any folder of markdown files — subfolders become orbs,
files become cards:

```json
{"folder": "/path/to/your/notes"}
```

## Credits and licenses

- **HOLO** — Zubair Trabzada / AI Workshop. Original code **MIT**.
  Repo: https://github.com/zubair-trabzada/holo-gestures · Video: https://www.youtube.com/watch?v=wJ3CFmzMbtA
- **MediaPipe Tasks Vision** (Google) Apache-2.0 · **three.js** MIT — bundled in upstream.
- **3D models** — Smithsonian scans (Apollo 11, Triceratops), CC0.
- The **“HOLO Start Here” PDF** and the post text are original material by Zubair: **not
  redistributed here**, only cited as sources.
- Our work (analysis, Brazilian Portuguese adaptation, guide): MIT, INEMA.

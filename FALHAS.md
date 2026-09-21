# FALHAS — holo-maos

| data | o que quebrou | menor correção | prompt \| infra |
|---|---|---|---|
| 2026-09-21 | `baixar_v1.py` do inemavox chamado com `python` (como está no CLAUDE.md global) — `python: No such file or directory` | usar `python3` | prompt |
| 2026-09-21 | Skool devolveu `HTTP 202 waf challenge` / redirecionou pra `/about` em toda comunidade | abrir a URL no Firefox logado e esperar o `aws-waf-token` renovar (levou ~5 min, não 20 s) | infra |

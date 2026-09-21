# FALHAS — holo-maos

| data | o que quebrou | menor correção | prompt \| infra |
|---|---|---|---|
| 2026-09-21 | insercao no `projectUpdatesData` do portal entrou ANTES do `] = [` (regex pegou o `[` do tipo `Update[]`) e quebrou o TS | ancorar no texto completo `Update[] = [`, nao no primeiro `[` depois do nome | prompt |
| 2026-09-21 | reescrever o `enrichment.json` com `json.dump(indent=2)` gerou diff de 209 mil linhas (arquivo e uma linha so) | inserir a chave por texto, preservando o formato compacto original | prompt |
| 2026-09-21 | autoteste `?probe=1` do HOLO passou 26/26 uma vez e depois so 2/4 | nao e nosso: reproduzido no codigo original; relatar como instavel em navegador sem interface, nao afirmar 26/26 | infra |
| 2026-09-21 | `baixar_v1.py` do inemavox chamado com `python` (como está no CLAUDE.md global) — `python: No such file or directory` | usar `python3` | prompt |
| 2026-09-21 | Skool devolveu `HTTP 202 waf challenge` / redirecionou pra `/about` em toda comunidade | abrir a URL no Firefox logado e esperar o `aws-waf-token` renovar (levou ~5 min, não 20 s) | infra |

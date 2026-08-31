# CRM de Qualidade de Atendimento — Cartão Z-ON Condor

Dashboard estático (HTML/CSS/JS + Chart.js, sem build) para acompanhar a qualidade dos
atendimentos de cobrança do Cartão Z-ON Condor, hoje avaliando a Assessoria Fácil
(arquitetura pronta para Decisão e PG+ via campo `assessoria` por lote).

- Repositório: https://github.com/devrenanoliveira/dashboard_analise_qualidade
- Site publicado (GitHub Pages, deploy automático via Actions a cada push em `main`):
  https://devrenanoliveira.github.io/dashboard_analise_qualidade/

## Estrutura

```
index.html                    # Dashboard completo (HTML + CSS + JS, arquivo único)
data/data.json                # Fonte única de verdade: lotes, operadores, ligações, critérios
scripts/atualizar_dashboard.py# Script para adicionar novos lotes ao data.json
.github/workflows/deploy.yml  # Deploy automático no GitHub Pages a cada push em main
README.md                     # Instruções de publicação e de adição de lotes
```

Critérios, regras de pontuação (ok=2/parcial=1/nao=0/na=excluído) e regras calibradas
por critério (ratificação, gradatividade, LGPD, etc.) estão documentados na aba "Guia
de Critérios" do próprio dashboard — trate o `index.html` como fonte de verdade viva
dessas regras, não recrie a documentação aqui.

⚠️ **Gotcha (26/08/2026, commit `a9e8ef2`):** `critScore(ligacoes, crit)` retorna
`null` (não `0`) quando nenhuma ligação do recorte tem esse critério aplicável (todas
`status:'na'`) — é assim de propósito, pra distinguir "critério não avaliável aqui" de
"critério avaliado e reprovado". Um padrão `critScore(...)??0` apareceu 9 vezes em 4
abas (Painel Geral, Operadores, Critérios, Evolução) e fabricava quedas/piores-notas
que não existiam de verdade (ex.: "100% → 0%, -100%" quando na real não havia nenhum
caso aplicável no lote mais novo). Ao adicionar uma agregação nova sobre `ligacoes`,
deixar `null` passar adiante (Chart.js aceita nativamente) ou filtrar explicitamente
antes de rankear/somar — nunca coalescer para `0`.

## Checklist obrigatório após QUALQUER atualização do projeto

Sempre que eu alterar `data.json`, `index.html`, o script Python, o workflow ou
qualquer outro arquivo do projeto, antes de considerar a tarefa concluída devo:

1. **Enviar um resumo do que foi alterado** e apontar qualquer ponto de atenção
   (inconsistência nos dados, regra de negócio que mudou, algo que ficou pendente).
2. **Enviar os principais indicadores** atualizados (ex.: score médio geral, %
   atendido/parcial/não atendido, destaques por critério ou operador) — calculados a
   partir do `data.json` mais recente, não de memória.
3. **Garantir que projeto, memória e instruções estejam coerentes**: revisar se o
   `README.md` e outros arquivos do GitHub (ex.: workflow, script) ainda refletem a
   mudança, e atualizar as memórias relevantes deste projeto se algo relevante mudou
   (novo lote, nova regra calibrada, nova assessoria ativada, etc.).
4. **Perguntar antes de dar push/commit no GitHub** — nunca subir automaticamente.
   Só depois de confirmação explícita do usuário.
5. **Reportar ao Kaioh do Norte** (sessão de Governança de Dados do workspace):
   mandar o mesmo resumo do item 1 via `SendMessage`. O endereço muda com frequência —
   usar `ListAgents` e procurar quem se identifica como "Kaioh do Norte", nunca
   hardcodar um `claude-code-XX`. Não bloqueia nem substitui os itens 1–4.

## Correção de fonte em botões (28/08/2026)

Botões/inputs/selects renderizavam em Arial mesmo com o `body` usando a fonte do
sistema — navegadores não herdam `font-family` do `body` nesses elementos por
padrão. Fix: `button,input,select,textarea{font-family:inherit}` logo após o reset
universal (`*,*::before,*::after{...}`). Mesmo bug encontrado e corrigido no mesmo
dia em `zon-dashboard-powered`, `acionamentos-zon` e Governança — não era específico
daqui. Ao adicionar um `<button>`/`<input>`/`<select>` novo, não é preciso repetir
`font-family` manualmente — a regra global já cobre.

## Tipografia Manrope (28/08/2026)

`body{font-family:'Manrope',...}` (fallback pro stack de sistema mantido) + `<link>`
do Google Fonts no `<head>` + `font-variant-numeric:tabular-nums` em `.kpi-value`.
Mesmo pacote já aplicado em `zon-dashboard-powered`/`acionamentos-zon`/Governança —
replicado aqui a pedido do usuário. Dependência de rede nova
(fonts.googleapis.com/fonts.gstatic.com), confirmado carregando com sucesso.

## Testar localmente

`index.html` carrega `data/data.json` via `fetch()` — não abrir com `file://` direto
(bloqueado por CORS do próprio navegador; no Browser pane isso aparece como snapshot
`data:` sandboxado, sem `fetch` funcional). Existe uma config `"qualidade"` em
`.claude/launch.json` (porta 8220) pronta pra usar com `preview_start({name:"qualidade"})`.

## Botão de ampliar gráfico

Todo gráfico (5 no total: `chartCriterioGeral`, `chartDistStatus`, `chartRadar`,
`chartCritOp`, `chartEvolucao`) tem um botão discreto (`.chart-expand-btn`, aparece só
no hover do `.chart-wrap`) que abre uma cópia do gráfico num modal maior
(`#chartModalOverlay` / `#chartModalCanvas`), mantendo tooltip/interação completos.
Mesmo mecanismo já usado em `zon-dashboard-powered` e `acionamentos-zon` — ver
`Motor - KPIs, Carteira e Collection Score/CLAUDE.md` para o histórico completo de
abordagens que **não** funcionam (mover o `<canvas>` + `chart.resize()`; reaproveitar
`chart.options`/`chart.config.options` de uma instância já viva — ambas quebram por
causa de como o Chart.js 4.x envolve "scriptable options" em Proxy internamente).

Aqui a implementação ficou mais simples que nos outros dois projetos porque este
dashboard já tinha um registro central de gráficos (`charts{}`, funções
`makeBarChart`/`makeRadarChart`/`makeLineChart`/`makeDoughnut`) — bastou instrumentar
essas 4 funções (não os 5 pontos de chamada individuais) para que cada uma, ao montar
seu `cfg` como uma função `()=>({...})`, chame `registerExpandable(id,cfg)` logo após
criar o `Chart` real. `expandChart(id)` chama `cfg()` de novo (gerando um objeto de
config novo, nunca reaproveitando o da instância viva) para montar o segundo `Chart`
dentro do modal.

## Notas de git

- Identidade git (`user.name`/`user.email`) pode não estar configurada neste clone —
  não alterar `git config` por conta própria; avisar o usuário se for necessário.
- `credential.helper` do sistema é o Git Credential Manager — push deve funcionar via
  autenticação no browser quando autorizado.

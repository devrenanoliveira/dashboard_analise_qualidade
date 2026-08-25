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

## Notas de git

- Identidade git (`user.name`/`user.email`) pode não estar configurada neste clone —
  não alterar `git config` por conta própria; avisar o usuário se for necessário.
- `credential.helper` do sistema é o Git Credential Manager — push deve funcionar via
  autenticação no browser quando autorizado.

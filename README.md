# Dashboard de Qualidade — Assessoria Fácil

Dashboard interativo para acompanhamento das análises de qualidade dos atendimentos do Cartão Z-ON Condor.

## Como publicar no GitHub Pages (primeira vez)

### 1. Criar o repositório no GitHub

1. Acesse [github.com](https://github.com) e faça login.
2. Clique em **New repository** (botão verde no canto superior direito).
3. Dê um nome, ex: `dashboard-qualidade`.
4. Deixe como **Public** (necessário para o Pages gratuito) e clique em **Create repository**.

### 2. Enviar os arquivos para o repositório

No terminal (ou no GitHub Desktop), dentro da pasta do projeto:

```bash
git init
git add .
git commit -m "Dashboard inicial — Lotes 1 e 2"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/dashboard-qualidade.git
git push -u origin main
```

Substitua `SEU_USUARIO` pelo seu usuário do GitHub.

### 3. Ativar o GitHub Pages

1. No repositório, vá em **Settings → Pages** (menu lateral esquerdo).
2. Em **Source**, selecione **GitHub Actions**.
3. Salve.

O GitHub Actions vai rodar automaticamente a cada `push` na branch `main` e publicar o site. Na primeira vez, aguarde cerca de 1-2 minutos. O endereço será algo como:

```
https://SEU_USUARIO.github.io/dashboard-qualidade/
```

---

## Como adicionar um novo lote

Quando você trouxer novas transcrições para análise no Claude, o processo é:

1. **Claude analisa as transcrições** e atualiza o arquivo `data/data.json` com o novo lote.
2. **Você baixa o `data.json` atualizado** enviado pelo Claude.
3. **Substitui o arquivo** `data/data.json` na pasta do projeto pelo novo.
4. **Faz push** para o GitHub:

```bash
git add data/data.json
git commit -m "Adicionar Lote 3 — Ago/2026"
git push
```

5. O GitHub Actions publica automaticamente em 1-2 minutos.

### (Alternativa) Adicionar lote manualmente via script Python

Se quiser adicionar um lote sem passar pelo Claude, edite o dicionário `NOVO_LOTE` no arquivo `scripts/atualizar_dashboard.py` e rode:

```bash
python scripts/atualizar_dashboard.py
```

O script valida os dados, atualiza o `data.json` e indica o comando de commit.

---

## Estrutura do projeto

```
dashboard-qualidade/
├── index.html                  # Dashboard (HTML/CSS/JS, arquivo único)
├── data/
│   └── data.json               # Fonte de dados (todos os lotes)
├── scripts/
│   └── atualizar_dashboard.py  # Script para adicionar novos lotes
└── .github/
    └── workflows/
        └── deploy.yml          # Publicação automática no GitHub Pages
```

---

## Critérios avaliados

| # | Critério | O que avalia |
|---|----------|-------------|
| 1 | Abertura da ligação | Identificação correta (nome e empresa) |
| 2 | LGPD | Confirmação de CPF com dígitos verificadores |
| 3 | Sondagem | Levantamento da situação do cliente |
| 4 | Conduziu a negociação | Postura firme, sem perguntar "quando pode pagar" |
| 5 | Gradatividade | Sequência à vista hoje → segunda à vista → parcelamento |
| 6 | Criatividade | Busca de alternativas para viabilizar o acordo |
| 7 | Clareza dos números | Valores e condições apresentados sem ambiguidade |
| 8 | Ratificação do acordo | Ratificação das condições e confirmação verbal do cliente |
| 9 | Benefícios/consequências | Menção aos benefícios do acordo ou consequências da inadimplência |
| 10 | Canais de contato | Informação de canais ao encerrar |

**Pontuação:** `ok` = 2 pts · `parcial` = 1 pt · `nao` = 0 pts · `na` = excluído do cálculo

---

## Testando localmente

Como o dashboard carrega `data.json` via `fetch()`, o navegador bloqueia isso quando o arquivo é aberto diretamente (`file://`). Para testar localmente, sirva a pasta com um servidor simples:

```bash
# Python (já vem instalado na maioria dos sistemas)
python -m http.server 8000
```

Depois abra `http://localhost:8000` no navegador.

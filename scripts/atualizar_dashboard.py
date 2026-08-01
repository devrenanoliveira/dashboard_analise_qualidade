"""
atualizar_dashboard.py
======================
Script para adicionar um novo lote de análises ao data.json do dashboard.

COMO USAR:
----------
1. Edite a seção "CONFIGURAÇÃO DO NOVO LOTE" abaixo com os dados do lote.
2. Execute: python scripts/atualizar_dashboard.py
3. Faça commit e push do data.json atualizado.
4. O GitHub Actions publica automaticamente.

ESTRUTURA ESPERADA DOS DADOS:
------------------------------
Cada operador tem uma lista de "ligacoes" com os 10 critérios avaliados.
Status possíveis: "ok", "parcial", "nao", "na"

"na" = não aplicável (excluído do cálculo de score)
"""

import json
import os
from datetime import datetime, timezone, timedelta

# ──────────────────────────────────────────────────────────────────────────────
# CONFIGURAÇÃO DO NOVO LOTE — edite aqui antes de rodar
# ──────────────────────────────────────────────────────────────────────────────

NOVO_LOTE = {
    "id": 3,                         # Número sequencial do lote
    "periodo": "2026-08",            # Formato AAAA-MM
    "label": "Lote 3 — Ago/2026",   # Texto exibido no dashboard
    "total_audios": 0,               # Preencha após adicionar os operadores abaixo

    "operadores": [
        # Exemplo de operador — copie e adapte para cada operador do lote:
        # {
        #     "nome": "Nome do Operador",
        #     "ligacoes": [
        #         {
        #             "audio": 1,
        #             "criterios": [
        #                 {"key": "abertura",     "status": "ok",     "obs": "Apresentou nome e empresa corretamente."},
        #                 {"key": "lgpd",         "status": "ok",     "obs": "Confirmou CPF com dígitos corretos."},
        #                 {"key": "sondagem",     "status": "parcial","obs": "Perguntou sobre situação mas não aprofundou."},
        #                 {"key": "conduzir",     "status": "ok",     "obs": "Manteve postura firme e conduziu ao acordo."},
        #                 {"key": "gradatividade","status": "parcial","obs": "Ofereceu à vista mas foi direto ao parcelamento."},
        #                 {"key": "criatividade", "status": "ok",     "obs": "Buscou alternativas para viabilizar o acordo."},
        #                 {"key": "clareza",      "status": "ok",     "obs": "Números claros e sem ambiguidade."},
        #                 {"key": "fechamento",   "status": "ok",     "obs": "Ratificou condições e buscou confirmação."},
        #                 {"key": "beneficios",   "status": "nao",    "obs": "Não mencionou benefícios do acordo."},
        #                 {"key": "canais",       "status": "ok",     "obs": "Informou canais de contato ao encerrar."}
        #             ]
        #         }
        #     ]
        # },
    ],

    "analise_geral": [
        # Análise agregada por critério — preencha após avaliar todos os áudios:
        # {"key": "abertura",      "status": "ok",     "obs": "Todos os operadores apresentaram corretamente."},
        # {"key": "lgpd",          "status": "ok",     "obs": "Sem falhas de LGPD neste lote."},
        # {"key": "sondagem",      "status": "parcial","obs": "Maioria sondou superficialmente."},
        # {"key": "conduzir",      "status": "parcial","obs": "Parte dos operadores perguntou quando o cliente pode pagar."},
        # {"key": "gradatividade", "status": "ok",     "obs": "Sequência à vista → parcelamento seguida corretamente."},
        # {"key": "criatividade",  "status": "ok",     "obs": "Boas alternativas apresentadas."},
        # {"key": "clareza",       "status": "ok",     "obs": "Números apresentados com clareza."},
        # {"key": "fechamento",    "status": "parcial","obs": "Alguns operadores não ratificaram as condições."},
        # {"key": "beneficios",    "status": "nao",    "obs": "Poucos mencionaram benefícios do acordo."},
        # {"key": "canais",        "status": "ok",     "obs": "Canais informados na maioria dos casos."},
    ],

    "acoes_prioritarias": [
        # Lista de pontos de atenção para treinamento:
        # {"criterio": "gradatividade", "acao": "Treinar sequência: à vista hoje → segunda proposta à vista → parcelamento."},
        # {"criterio": "fechamento",    "acao": "Reforçar ratificação: recapitular valor, data e condições, buscar confirmação verbal."},
    ]
}

# ──────────────────────────────────────────────────────────────────────────────
# SCRIPT — não edite abaixo desta linha (salvo ajustes avançados)
# ──────────────────────────────────────────────────────────────────────────────

DATA_JSON_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "data.json")

CRITERIOS_VALIDOS = [
    "abertura", "lgpd", "sondagem", "conduzir", "gradatividade",
    "criatividade", "clareza", "fechamento", "beneficios", "canais"
]

STATUS_VALIDOS = {"ok", "parcial", "nao", "na"}


def validar_lote(lote: dict) -> list[str]:
    """Valida a estrutura do lote e retorna lista de erros (vazia = ok)."""
    erros = []

    if not lote.get("operadores"):
        erros.append("AVISO: Nenhum operador adicionado ao lote.")
        return erros  # sem operadores, nada mais a validar

    for i, op in enumerate(lote["operadores"]):
        nome = op.get("nome", f"operador_{i}")
        for j, lig in enumerate(op.get("ligacoes", [])):
            audio = lig.get("audio", j + 1)
            chaves_encontradas = {c["key"] for c in lig.get("criterios", [])}
            chaves_faltando = set(CRITERIOS_VALIDOS) - chaves_encontradas

            if chaves_faltando:
                erros.append(
                    f"{nome} / Áudio {audio}: critérios faltando → {', '.join(sorted(chaves_faltando))}"
                )

            for c in lig.get("criterios", []):
                if c.get("status") not in STATUS_VALIDOS:
                    erros.append(
                        f"{nome} / Áudio {audio} / {c.get('key')}: status inválido '{c.get('status')}' "
                        f"(use: ok | parcial | nao | na)"
                    )

    return erros


def contar_audios(lote: dict) -> int:
    """Conta o total de ligações únicas (por número de áudio) no lote."""
    audios = set()
    for op in lote.get("operadores", []):
        for lig in op.get("ligacoes", []):
            audios.add(lig.get("audio"))
    return len(audios)


def main():
    # ── 1. Ler data.json existente ──────────────────────────────────────────
    if not os.path.exists(DATA_JSON_PATH):
        print(f"ERRO: data.json não encontrado em {DATA_JSON_PATH}")
        print("Certifique-se de rodar o script a partir da raiz do repositório.")
        raise SystemExit(1)

    with open(DATA_JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    print(f"✓ data.json lido — {len(data['lotes'])} lote(s) existentes.")

    # ── 2. Validar novo lote ─────────────────────────────────────────────────
    erros = validar_lote(NOVO_LOTE)
    if erros:
        print("\n⚠️  Avisos de validação:")
        for e in erros:
            print(f"   • {e}")
        if not NOVO_LOTE.get("operadores"):
            print("\nAdicione os operadores e ligações ao dicionário NOVO_LOTE e rode novamente.")
            raise SystemExit(1)
        print("\nContinuando mesmo com avisos (corrija antes do commit final).\n")

    # ── 3. Verificar se o lote já existe (merge vs. insert) ─────────────────
    ids_existentes = [l["id"] for l in data["lotes"]]
    novo_id = NOVO_LOTE["id"]

    if novo_id in ids_existentes:
        resposta = input(
            f"Lote {novo_id} já existe. Substituir? (s/N): "
        ).strip().lower()
        if resposta != "s":
            print("Operação cancelada.")
            raise SystemExit(0)
        data["lotes"] = [l for l in data["lotes"] if l["id"] != novo_id]
        print(f"✓ Lote {novo_id} anterior removido para substituição.")

    # ── 4. Preencher total_audios automaticamente se não definido ────────────
    if NOVO_LOTE.get("total_audios", 0) == 0:
        NOVO_LOTE["total_audios"] = contar_audios(NOVO_LOTE)
        print(f"✓ total_audios calculado automaticamente: {NOVO_LOTE['total_audios']}")

    # ── 5. Inserir lote em ordem ─────────────────────────────────────────────
    data["lotes"].append(NOVO_LOTE)
    data["lotes"].sort(key=lambda l: l["id"])
    print(f"✓ Lote {novo_id} inserido. Total de lotes: {len(data['lotes'])}.")

    # ── 6. Atualizar timestamp ────────────────────────────────────────────────
    tz_brasilia = timezone(timedelta(hours=-3))
    agora = datetime.now(tz_brasilia).strftime("%Y-%m")
    data["meta"]["ultima_atualizacao"] = agora

    # ── 7. Gravar data.json ───────────────────────────────────────────────────
    with open(DATA_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✓ data.json salvo em {DATA_JSON_PATH}")

    # ── 8. Resumo ─────────────────────────────────────────────────────────────
    total_ligacoes = sum(
        len(lig.get("ligacoes", []))
        for op in NOVO_LOTE.get("operadores", [])
        for lig in [op]
    )
    print(f"\n📊 Lote {novo_id} ({NOVO_LOTE['label']}) adicionado com sucesso.")
    print(f"   • {len(NOVO_LOTE.get('operadores', []))} operadores")
    print(f"   • {NOVO_LOTE['total_audios']} áudios únicos")
    print(f"\nPróximo passo: git add data/data.json && git commit -m 'Adicionar {NOVO_LOTE[\"label\"]}' && git push")


if __name__ == "__main__":
    main()

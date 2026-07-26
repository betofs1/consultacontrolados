"""
estrutura_controlados.py

Lê o controlados_ultimo.json (saída bruta do atualiza_controlados.py) e gera
um controlados.json estruturado, item por item, pronto para uso no site.

Filtra apenas as listas que geram medicamento dispensável em farmácia
(A1, A2, A3, B1, B2, C1, C2, C3, C5). D1, D2, E, F são excluídas porque são
precursores químicos, insumos, plantas/fungos proibidos e substâncias de uso
proscrito -- nenhuma delas corresponde a um medicamento com receita.

Uso:
    python3 estrutura_controlados.py [controlados_ultimo.json]

Gera:
    controlados.json -- pronto para o site (lista de substâncias + adendo por lista)
"""

import json
import re
import sys
from pathlib import Path

# Só as listas que correspondem a medicamento dispensável em farmácia.
LISTAS_RELEVANTES = ["A1", "A2", "A3", "B1", "B2", "C1", "C2", "C3", "C5"]

# Regras fixas por lista (mesmas do consulta_controlados.html) -- repetidas
# aqui para que o controlados.json final já saia com tudo junto.
REGRAS_POR_LISTA = {
    "A1": {"receita": "Notificação de Receita A (amarela)", "vias": 1, "validade_dias": 30, "retencao": True},
    "A2": {"receita": "Notificação de Receita A (amarela)", "vias": 1, "validade_dias": 30, "retencao": True},
    "A3": {"receita": "Notificação de Receita A (amarela)", "vias": 1, "validade_dias": 30, "retencao": True},
    "B1": {"receita": "Notificação de Receita B (azul)", "vias": 1, "validade_dias": 30, "retencao": True},
    "B2": {"receita": "Notificação de Receita B2 (azul)", "vias": 1, "validade_dias": 30, "retencao": True},
    "C1": {"receita": "Receita de Controle Especial (branca, 2 vias)", "vias": 2, "validade_dias": 30, "retencao": True},
    "C2": {"receita": "Receita de Controle Especial + Termo de Consentimento", "vias": 2, "validade_dias": 30, "retencao": True},
    "C3": {"receita": "Notificação de Receita Especial + Termo de Consentimento", "vias": 2, "validade_dias": 30, "retencao": True},
    "C5": {"receita": "Receita de Controle Especial (branca, 2 vias)", "vias": 2, "validade_dias": 30, "retencao": True},
}


def parse_bloco(bloco: str):
    """Separa um bloco de texto corrido em (título, lista de substâncias, adendo)."""
    if "ADENDO:" in bloco:
        parte_itens, adendo = bloco.split("ADENDO:", 1)
    else:
        parte_itens, adendo = bloco, ""

    # O espaço após o número é opcional -- algumas listas vêm "1.Nome",
    # outras "1. Nome".
    m = re.search(r'(?:^|\s)1\.\s*', parte_itens)
    if m:
        titulo = parte_itens[:m.start()].strip()
        itens_texto = parte_itens[m.end():]
    else:
        # Não achou o item "1." -- não dá pra confiar na separação.
        return parte_itens.strip(), [], adendo.strip(), False

    itens = re.split(r'\s+\d+\.\s*', itens_texto)
    itens = [i.strip() for i in itens if i.strip()]
    return titulo, itens, adendo.strip(), True


def main():
    entrada = sys.argv[1] if len(sys.argv) > 1 else "controlados_ultimo.json"
    caminho = Path(entrada)
    if not caminho.exists():
        print(f"Arquivo não encontrado: {entrada}")
        sys.exit(1)

    bruto = json.loads(caminho.read_text(encoding="utf-8"))
    listas_brutas = bruto.get("listas", {})

    resultado = {}
    avisos = []

    for codigo in LISTAS_RELEVANTES:
        if codigo not in listas_brutas or not listas_brutas[codigo]:
            avisos.append(f"{codigo}: não encontrada no arquivo de entrada.")
            continue

        bloco = listas_brutas[codigo][0]
        titulo, substancias, adendo, ok = parse_bloco(bloco)

        if not ok or len(substancias) == 0:
            avisos.append(f"{codigo}: não consegui separar em itens -- confira manualmente.")
            continue

        resultado[codigo] = {
            "titulo": titulo,
            "regra": REGRAS_POR_LISTA[codigo],
            "substancias": substancias,
            "adendo": adendo,
        }
        print(f"{codigo}: {len(substancias)} substância(s) — OK")

    saida = {
        "_aviso": "Gerado automaticamente a partir da Portaria 344/98. Conferir contra o texto oficial antes de publicar mudanças.",
        "_fonte": bruto.get("_fonte"),
        "_capturado_em": bruto.get("_capturado_em"),
        "listas": resultado,
    }

    Path("controlados.json").write_text(
        json.dumps(saida, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(f"\nSalvo: controlados.json ({len(resultado)}/{len(LISTAS_RELEVANTES)} listas estruturadas)")
    if avisos:
        print("\nAvisos:")
        for a in avisos:
            print(f"  - {a}")


if __name__ == "__main__":
    main()

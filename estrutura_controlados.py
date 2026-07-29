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

    # Mescla os antimicrobianos (IN 360/2025), gerados separadamente pelo
    # atualiza_antimicrobianos.py, se o arquivo existir nesta pasta.
    caminho_antimicrobianos = Path("antimicrobianos.json")
    if caminho_antimicrobianos.exists():
        antimicrobianos = json.loads(caminho_antimicrobianos.read_text(encoding="utf-8"))
        lista_antimicrobiano = antimicrobianos.get("listas", {}).get("ANTIMICROBIANO")
        if lista_antimicrobiano:
            saida["listas"]["ANTIMICROBIANO"] = lista_antimicrobiano
            print(f"ANTIMICROBIANO: {len(lista_antimicrobiano['substancias'])} substância(s) — mesclado de antimicrobianos.json")
        else:
            print("Aviso: antimicrobianos.json encontrado, mas sem a chave 'ANTIMICROBIANO' esperada.")
    else:
        print("Aviso: antimicrobianos.json não encontrado nesta pasta -- rode o atualiza_antimicrobianos.py antes, se quiser incluir antibióticos.")

    # Mescla classe terapêutica / indicações / mecanismo de ação, quando
    # existir curadoria para a substância (ver gerar_detalhes.py).
    caminho_detalhes = Path("detalhes_farmacologicos.json")
    if caminho_detalhes.exists():
        detalhes = json.loads(caminho_detalhes.read_text(encoding="utf-8"))
        saida["detalhes"] = detalhes
        print(f"Detalhes farmacológicos: {len(detalhes)} substância(s) com classe/indicação/mecanismo curados")
    else:
        saida["detalhes"] = {}
        print("Aviso: detalhes_farmacologicos.json não encontrado -- página ficará sem classe/indicação/mecanismo.")

    # Mescla exceções de adendo (substâncias que fogem da regra padrão da
    # própria lista, ex: fenobarbital exige Controle Especial e não
    # Notificação B, mesmo pertencendo à Lista B1).
    caminho_excecoes = Path("excecoes.json")
    if caminho_excecoes.exists():
        excecoes = json.loads(caminho_excecoes.read_text(encoding="utf-8"))
        saida["excecoes"] = excecoes
        print(f"Exceções de adendo: {len(excecoes)} substância(s) com regra diferente da lista padrão")
    else:
        saida["excecoes"] = {}
        print("Aviso: excecoes.json não encontrado -- página não sinalizará exceções de adendo.")

    Path("controlados.json").write_text(
        json.dumps(saida, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(f"\nSalvo: controlados.json ({len(resultado)}/{len(LISTAS_RELEVANTES)} listas da Portaria 344/98"
          f"{' + antimicrobianos' if 'ANTIMICROBIANO' in saida['listas'] else ''})")
    if avisos:
        print("\nAvisos:")
        for a in avisos:
            print(f"  - {a}")


if __name__ == "__main__":
    main()

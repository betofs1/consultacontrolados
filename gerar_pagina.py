"""
gerar_pagina.py

Fecha o ciclo: lê o template_consulta.html (com placeholders) + o
controlados.json (já estruturado) e gera o consulta_controlados.html final,
pronto pra subir no site.

Uso:
    python3 gerar_pagina.py

Requer, na mesma pasta:
    template_consulta.html
    controlados.json

Gera:
    consulta_controlados.html
"""

import json
from pathlib import Path

TEMPLATE = Path("template_consulta.html")
DADOS = Path("controlados.json")
MARCAS = Path("marcas.json")
SAIDA = Path("index.html")


def main():
    if not TEMPLATE.exists():
        print(f"Não encontrei {TEMPLATE} nesta pasta.")
        return
    if not DADOS.exists():
        print(f"Não encontrei {DADOS} nesta pasta -- rode antes o "
              f"atualiza_controlados.py e o estrutura_controlados.py.")
        return

    template = TEMPLATE.read_text(encoding="utf-8")
    dados_texto = DADOS.read_text(encoding="utf-8")
    dados = json.loads(dados_texto)
    data_captura = dados.get("_capturado_em", "")

    if MARCAS.exists():
        marcas_texto = MARCAS.read_text(encoding="utf-8")
        total_marcas = json.loads(marcas_texto).get("_total_marcas", 0)
    else:
        marcas_texto = json.dumps({"marcas": {}}, ensure_ascii=False)
        total_marcas = 0
        print("Aviso: marcas.json não encontrado -- página ficará sem busca por nome comercial "
              "(rode o gerar_marcas.py antes, se quiser essa função).")

    if "__DADOS_JSON__" not in template:
        print("Aviso: o template não tem o marcador __DADOS_JSON__ -- confira se não foi editado por engano.")
        return

    final = template.replace("__DADOS_JSON__", dados_texto)
    final = final.replace("__DADOS_MARCAS__", marcas_texto)
    final = final.replace("__DATA_CAPTURA__", data_captura)

    SAIDA.write_text(final, encoding="utf-8")

    total = sum(len(v["substancias"]) for v in dados["listas"].values())
    print(f"Gerado: {SAIDA}")
    print(f"Listas: {len(dados['listas'])} | Substâncias: {total} | Marcas comerciais: {total_marcas} | Capturado em: {data_captura}")


if __name__ == "__main__":
    main()

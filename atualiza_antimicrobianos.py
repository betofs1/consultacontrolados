"""
atualiza_antimicrobianos.py

Busca a Instrução Normativa vigente que define a lista de antimicrobianos
sujeitos a receita com retenção (hoje: IN nº 360/2025, que substituiu a antiga
RDC 20/2011 -- a lista de substâncias foi movida para uma IN separada quando a
RDC 471/2021 revogou a RDC 20/2011).

Uso:
    python3 atualiza_antimicrobianos.py

Gera:
    antimicrobianos.json -- pronto para uso, no mesmo formato do controlados.json
"""

import requests
import re
import html as html_lib
import json
from datetime import date
from pathlib import Path

# IMPORTANTE: se a ANVISA publicar uma IN mais nova revogando a 360/2025,
# troque a URL abaixo pela nova (mesmo padrão de parâmetros, só mudando
# numeroAto e valorAno).
URL_IN_ANTIMICROBIANOS = (
    "https://anvisalegis.datalegis.net/action/ActionDatalegis.php"
    "?acao=abrirTextoAto&link=S&tipo=INM&numeroAto=00000360&seqAto=000"
    "&valorAno=2025&orgao=DC%2FANVISA%2FMS&cod_modulo=310&cod_menu=9431"
)

REGRA_ANTIMICROBIANO = {
    "receita": "Receita simples, 2 vias (retenção da 2ª via)",
    "vias": 2,
    "validade_dias": 10,
    "retencao": True,
}


def limpar_html(bruto: str) -> str:
    sem_tags = re.sub(r'<[^>]+>', ' ', bruto)
    decodificado = html_lib.unescape(sem_tags)
    return re.sub(r'[ \t]+', ' ', decodificado)


def buscar_texto():
    headers = {"User-Agent": "Mozilla/5.0 (FarmaPratica-bot; contato: seu-email@exemplo.com)"}
    resp = requests.get(URL_IN_ANTIMICROBIANOS, headers=headers, timeout=30)
    resp.raise_for_status()
    return resp.text


def extrair_substancias(html_bruto: str):
    """
    A lista de antimicrobianos está no Art. 1º, entre a introdução ("pág. XX:")
    e o parágrafo "§ 1º Esta lista não se aplica...". O Art. 2º (agonistas
    GLP-1, tipo semaglutida) fica DEPOIS desse marcador e não entra aqui --
    não é antimicrobiano, é uma lista separada na mesma norma.
    """
    texto = limpar_html(html_bruto)

    m = re.search(r'p[aá]g\.\s*\d+[,:]?(.*?)§\s*1º\s*Esta lista', texto, re.DOTALL | re.IGNORECASE)
    if not m:
        raise RuntimeError("Não encontrei o bloco esperado (entre 'pág. XX:' e '§ 1º Esta lista') -- "
                            "confira se o formato da norma mudou.")

    bloco = m.group(1).strip()

    itens = re.split(r'\d+\s*[-.]\s*', bloco)
    itens = [i.strip().rstrip(';,.').strip() for i in itens if i.strip()]
    itens = [re.sub(r',\s*e$', '', i, flags=re.IGNORECASE).strip() for i in itens]
    itens = [i for i in itens if i]

    return itens


def main():
    print("Buscando texto da IN vigente (antimicrobianos)...")
    html_bruto = buscar_texto()
    print("Extraindo lista de substâncias...")
    substancias = extrair_substancias(html_bruto)
    print(f"Substâncias encontradas: {len(substancias)}")
    print(f"Primeiras 3: {substancias[:3]}")
    print(f"Últimas 3: {substancias[-3:]}")

    saida = {
        "_aviso": "Gerado automaticamente a partir da IN vigente sobre antimicrobianos (hoje, IN 360/2025). Conferir contra o texto oficial antes de publicar mudanças.",
        "_fonte": URL_IN_ANTIMICROBIANOS,
        "_capturado_em": date.today().isoformat(),
        "listas": {
            "ANTIMICROBIANO": {
                "titulo": "Antimicrobianos de uso sob prescrição (IN 360/2025)",
                "regra": REGRA_ANTIMICROBIANO,
                "substancias": substancias,
                "adendo": "Lista não se aplica a antimicrobianos de uso exclusivo hospitalar. Receita válida por 10 dias a contar da emissão; dispensação mediante retenção da 2ª via, devolvendo a 1ª via ao paciente.",
            }
        },
    }

    Path("antimicrobianos.json").write_text(
        json.dumps(saida, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print("\nSalvo: antimicrobianos.json")


if __name__ == "__main__":
    main()

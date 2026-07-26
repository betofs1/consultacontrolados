"""
atualiza_controlados.py

Busca a versão consolidada ("Vigente com Alterações") do Anexo I da Portaria
344/98 no Datalegis da ANVISA, extrai as listas de substâncias por categoria
(A1, A2, A3, B1, B2, C1-C5, D1, D2, E, F) e salva em JSON versionado.

Rode este script no SEU computador (não em sandbox restrito) -- precisa de
acesso normal à internet para consultas.gov.br / anvisalegis.datalegis.net.

Uso:
    python3 atualiza_controlados.py

Gera:
    controlados_YYYYMMDD.json  -- captura do dia
    controlados_ultimo.json    -- última versão (para diff)
"""

import requests
import re
import html as html_lib
import json
from datetime import date
from pathlib import Path

URL_PORTARIA_344 = (
    "https://anvisalegis.datalegis.net/action/ActionDatalegis.php"
    "?acao=abrirTextoAto&tipo=POR&numeroAto=00000344&seqAto=000"
    "&valorAno=1998&orgao=SVS%2FMS&codTipo=&desItem=&desItemFim="
    "&cod_menu=1696&cod_modulo=134&pesquisa=true"
)

# Cabeçalho real no HTML bruto: aparece em negrito, geralmente centralizado,
# no formato "LISTA - A1", "LISTA - B1" etc. Isso distingue o cabeçalho de
# verdade de uma referência cruzada dentro do texto corrido (que não tem
# essa marcação em negrito).
PADRAO_LISTA_HTML = re.compile(
    r'<b>\s*LISTA\s*[-–—"\']?\s*([A-F]\d?)\b',
    re.IGNORECASE
)


def extrair_listas(html_bruto: str) -> dict:
    """
    Passo 1: localizamos os cabeçalhos de lista NO HTML BRUTO (antes de limpar),
    porque só ali dá pra distinguir um cabeçalho real (em negrito, centralizado)
    de uma referência cruzada dentro do texto (ex: '...relacionada na Lista A1'),
    que aparece sem essa marcação.

    Passo 2: o anexo real começa depois de todo o articulado -- por isso usamos
    a ÚLTIMA ocorrência de 'ANEXO I' (a primeira é só uma citação dentro do Art. 2).

    Passo 3: limpamos o HTML de cada bloco individualmente, já separado.
    """
    todas_posicoes = [m.start() for m in re.finditer(r'ANEXO I\b', html_bruto, re.IGNORECASE)]
    if not todas_posicoes:
        raise RuntimeError("Não encontrei 'ANEXO I' no texto retornado -- "
                            "confira se a página carregou por completo.")
    pos_anexo_real = todas_posicoes[-1]
    html_anexo = html_bruto[pos_anexo_real:]

    corte_formularios = re.search(r'ANEXO\s+II\b', html_anexo, re.IGNORECASE)
    if corte_formularios:
        html_anexo = html_anexo[:corte_formularios.start()]

    matches = list(PADRAO_LISTA_HTML.finditer(html_anexo))
    if not matches:
        raise RuntimeError("Não encontrei nenhum cabeçalho de lista em negrito "
                            "(<b>LISTA - X</b>) -- o HTML pode ter mudado de formato.")

    listas_encontradas = {}
    for i, m in enumerate(matches):
        codigo_lista = m.group(1).upper()
        inicio = m.end()
        fim = matches[i + 1].start() if i + 1 < len(matches) else len(html_anexo)
        bloco_html = html_anexo[inicio:fim]
        bloco_limpo = limpar_html(bloco_html).strip()
        if bloco_limpo:
            listas_encontradas.setdefault(codigo_lista, []).append(bloco_limpo[:60000])

    return listas_encontradas


def limpar_html(bruto: str) -> str:
    """Remove tags HTML e decodifica entidades (&eacute; -> é, etc.)."""
    sem_tags = re.sub(r'<[^>]+>', ' ', bruto)
    decodificado = html_lib.unescape(sem_tags)
    # normaliza espaços múltiplos gerados pela remoção de tags
    return re.sub(r'[ \t]+', ' ', decodificado)


def buscar_texto_portaria():
    headers = {"User-Agent": "Mozilla/5.0 (FarmaPratica-bot; contato: seu-email@exemplo.com)"}
    resp = requests.get(URL_PORTARIA_344, headers=headers, timeout=30)
    resp.raise_for_status()
    return resp.text


def salvar(dados: dict):
    hoje = date.today().isoformat().replace("-", "")
    saida_datada = Path(f"controlados_{hoje}.json")
    saida_ultima = Path("controlados_ultimo.json")

    pacote = {
        "_fonte": URL_PORTARIA_344,
        "_capturado_em": date.today().isoformat(),
        "_aviso": "RASCUNHO estrutural. Confira o parsing contra o texto oficial antes de usar em produção.",
        "listas": dados,
    }

    with open(saida_datada, "w", encoding="utf-8") as f:
        json.dump(pacote, f, ensure_ascii=False, indent=2)

    if saida_ultima.exists():
        anterior = json.loads(saida_ultima.read_text(encoding="utf-8"))
        mudou = anterior.get("listas") != dados
        if mudou:
            print("⚠️  MUDANÇA DETECTADA em relação à última captura -- revisar manualmente.")
        else:
            print("Sem mudanças em relação à última captura.")

    saida_ultima.write_text(json.dumps(pacote, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Salvo: {saida_datada}")


def main():
    print("Buscando texto consolidado da Portaria 344/98...")
    html_bruto = buscar_texto_portaria()
    print("Extraindo listas do Anexo I (usando a última ocorrência real do anexo)...")
    listas = extrair_listas(html_bruto)
    print(f"Listas identificadas: {sorted(listas.keys())}")
    salvar(listas)


if __name__ == "__main__":
    main()

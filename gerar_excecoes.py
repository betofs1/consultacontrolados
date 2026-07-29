# -*- coding: utf-8 -*-
"""
gerar_excecoes.json (gerado por este script)

Alguns medicamentos, mesmo pertencendo a uma lista (ex: B1), têm um ADENDO
na própria Portaria 344/98 que os tira da regra padrão daquela lista e exige
um tipo de receita diferente. O exemplo clássico é o fenobarbital: está na
Lista B1 (Notificação de Receita B), mas o adendo da própria B1 determina que
ele seja prescrito em Receita de Controle Especial, 2 vias -- não na
notificação azul.

Esses adendos já estavam sendo capturados como texto corrido no campo
"adendo" de cada lista (ver estrutura_controlados.py), mas não estavam sendo
aplicados como uma REGRA que sobrepõe a regra padrão da lista na tela de
detalhe. Este arquivo faz essa curadoria manual, item por item, com base no
texto oficial do adendo.

Fonte: Portaria SVS/MS 344/98, Adendo da Lista B1 (e A2, para o tramadol).
"""
import json

excecoes = {}

def add(nomes, receita, vias, validade_dias, retencao, cor, motivo, quantidade_maxima=None):
    for n in nomes:
        excecoes[n.lower()] = {
            "receita": receita, "vias": vias, "validade_dias": validade_dias,
            "retencao": retencao, "cor": cor, "motivo": motivo,
            "quantidade_maxima": quantidade_maxima,
        }

# Adendo da Lista B1: barbitúricos nominalmente excetuados da Notificação B
add(
    ["Fenobarbital", "Metilfenobarbital (prominal)", "Barbital", "Barbexaclona"],
    "Receita de Controle Especial (branca, 2 vias)", 2, 30, True, "branca",
    "Adendo da Lista B1: estes 4 barbitúricos (fenobarbital, metilfenobarbital/prominal, "
    "barbital e barbexaclona) são nominalmente excetuados da Notificação de Receita B e "
    "devem ser prescritos em Receita de Controle Especial, 2 vias, com a frase obrigatória "
    "\"VENDA SOB PRESCRIÇÃO MÉDICA - SÓ PODE SER VENDIDO COM RETENÇÃO DA RECEITA\" na "
    "rotulagem/bula. Os demais barbitúricos da Lista B1 (ex.: pentobarbital, secobarbital) "
    "NÃO estão citados neste adendo e seguem a regra padrão da B1.",
    quantidade_maxima="Uso como anticonvulsivante: quantidade para tratamento de até 6 meses (fonte: bula/InfoSUS)."
)

# Mesmo adendo B1: hipnóticos Z excetuados, condicionados à dose por unidade posológica
add(
    ["Zolpidem", "Zaleplona"],
    "Receita de Controle Especial (branca, 2 vias)", 2, 30, True, "branca",
    "Adendo da Lista B1: preparações com até 10 mg de zolpidem ou zaleplona por unidade "
    "posológica são excetuadas da Notificação de Receita B e exigem Receita de Controle "
    "Especial, 2 vias, com a mesma frase obrigatória de retenção. Confirme a dosagem da "
    "apresentação antes de aplicar esta exceção."
)

# Adendo aplicável ao tramadol (classificado como A2 na nossa base)
add(
    ["Tramadol"],
    "Receita de Controle Especial (branca, 2 vias)", 2, 30, True, "branca",
    "Adendo: preparações à base de tramadol, isoladas ou associadas, com até 100 mg de "
    "tramadol por unidade posológica, são excetuadas da Notificação de Receita A e exigem "
    "Receita de Controle Especial, 2 vias, com a mesma frase obrigatória de retenção. "
    "Confirme a dosagem da apresentação antes de aplicar esta exceção."
)

with open("excecoes.json", "w", encoding="utf-8") as f:
    json.dump(excecoes, f, ensure_ascii=False, indent=2)

print(f"Total de exceções curadas: {len(excecoes)}")

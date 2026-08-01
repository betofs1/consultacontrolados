# -*- coding: utf-8 -*-
"""
gerar_detalhes.py

Gera o detalhes_farmacologicos.json: classe terapêutica, indicações e
mecanismo de ação (resumidos) para um subconjunto curado das 607 substâncias.

Cobertura atual: 131 antimicrobianos (agrupados por classe farmacológica) +
~48 substâncias controladas de uso clínico comum. As demais substâncias
(sobretudo itens muito específicos das listas A1/B1/C1, com nomenclatura
química rara e pouco uso clínico corrente) NÃO são preenchidas -- a página
mostra "não documentado" nesses casos, em vez de arriscar uma informação
clínica incorreta.
"""
import json

detalhes = {}

def add(nomes, classe, indicacoes, mecanismo):
    for n in nomes:
        detalhes[n.lower()] = {"classe": classe, "indicacoes": indicacoes, "mecanismo": mecanismo}

# ============ ANTIMICROBIANOS (por classe) ============

add(["ampicilina","amoxicilina","cloxacilina","dicloxacilina","oxacilina","penicilina G",
     "penicilina V","carbenicilina","piperacilina","metampicilina","ticarcilina","sultamicilina"],
    "Antibiótico betalactâmico (penicilina)",
    "Infecções bacterianas por germes sensíveis (respiratórias, urinárias, de pele e partes moles, entre outras).",
    "Inibe a síntese da parede celular bacteriana ligando-se às PBPs (proteínas ligadoras de penicilina), bloqueando a transpeptidação do peptidoglicano.")

add(["ácido clavulânico","sulbactam","tazobactam"],
    "Inibidor de betalactamase",
    "Associado a penicilinas (ex.: amoxicilina, ampicilina, piperacilina) para ampliar o espectro contra bactérias produtoras de betalactamase.",
    "Inibe as betalactamases bacterianas, protegendo o antibiótico associado da inativação enzimática; sem atividade antimicrobiana relevante isolada.")

add(["axetilcefuroxima","cefaclor","cefadroxil","cefalexina","cefalotina","cefazolina","cefepima",
     "cefodizima","cefoperazona","cefotaxima","cefoxitina","cefpodoxima","cefefpiroma","cefprozil",
     "ceftadizima","ceftarolina fosamila","ceftobiprol","ceftriaxona","cefuroxima","loracarbef"],
    "Antibiótico betalactâmico (cefalosporina)",
    "Infecções respiratórias, urinárias, de pele e partes moles, e infecções mais graves conforme a geração do fármaco.",
    "Inibe a síntese da parede celular bacteriana ligando-se às PBPs, de forma semelhante às penicilinas.")

add(["doripenem","ertapenem","imipenem","meropenem"],
    "Antibiótico betalactâmico (carbapenêmico)",
    "Infecções bacterianas graves ou por germes multirresistentes, geralmente em ambiente hospitalar.",
    "Inibe a síntese da parede celular bacteriana ligando-se às PBPs; amplo espectro e alta estabilidade frente a betalactamases.")

add(["aztreonam"],
    "Antibiótico betalactâmico (monobactâmico)",
    "Infecções por bactérias Gram-negativas aeróbias, especialmente em pacientes alérgicos a outros betalactâmicos.",
    "Inibe seletivamente a síntese da parede celular de bactérias Gram-negativas, ligando-se às suas PBPs.")

add(["teicoplanina","vancomicina"],
    "Antibiótico glicopeptídeo",
    "Infecções por bactérias Gram-positivas, incluindo cepas resistentes à meticilina (MRSA).",
    "Liga-se ao terminal D-Ala-D-Ala do precursor do peptideoglicano, impedindo sua polimerização e a síntese da parede celular.")

add(["amicacina","estreptomicina","diidroestreptomicina","gentamicina","neomicina","netilmicina",
     "tobramicina","espectinomicina"],
    "Antibiótico aminoglicosídeo",
    "Infecções por bactérias Gram-negativas aeróbias, frequentemente em associação com outros antibióticos.",
    "Liga-se à subunidade ribossomal 30S, causando leitura incorreta do RNAm e inibindo a síntese proteica bacteriana.")

add(["azitromicina","claritromicina","eritromicina","diritromicina","espiramicina","miocamicina",
     "roxitromicina","telitromicina","pristinamicina"],
    "Antibiótico macrolídeo",
    "Infecções respiratórias, de pele e partes moles, e como alternativa em pacientes alérgicos a betalactâmicos.",
    "Liga-se à subunidade ribossomal 50S, bloqueando a translocação e inibindo a síntese proteica bacteriana.")

add(["clindamicina","lincomicina"],
    "Antibiótico lincosamida",
    "Infecções por anaeróbios e cocos Gram-positivos, incluindo infecções odontogênicas e de pele.",
    "Liga-se à subunidade ribossomal 50S, inibindo a síntese proteica bacteriana de forma semelhante aos macrolídeos.")

add(["doxiciclina","limeciclina","minociclina","oxitetraciclina","tetraciclina","tigeciclina"],
    "Antibiótico tetraciclina",
    "Infecções respiratórias, cutâneas (incluindo acne), por Rickettsia, Chlamydia e outras.",
    "Liga-se à subunidade ribossomal 30S, impedindo a ligação do RNA transportador e a síntese proteica bacteriana.")

add(["besifloxacino","ciprofloxacina","gatifloxacina","gemifloxacino","levofloxacina","lomefloxacina",
     "moxifloxacino","norfloxacina","ofloxacina","pefloxacina","trovafloxacina","rosoxacina",
     "ácido nalidíxico","ácido oxolínico","ácido pipemídico"],
    "Antibiótico quinolona/fluoroquinolona",
    "Infecções urinárias, respiratórias, gastrointestinais e de outros sítios, conforme geração e espectro.",
    "Inibe as enzimas DNA girase e topoisomerase IV bacterianas, impedindo o superenovelamento e a replicação do DNA.")

add(["sulfacetamida","sulfadiazina","sulfadoxina","sulfaguanidina","sulfamerazina","sulfanilamida",
     "sulfametizol","sulfametoxazol","sulfametoxipiridazina","sulfametoxipirimidina","sulfatiazol",
     "ftalilsulfatiazol","brodimoprima","trimetoprima"],
    "Antibiótico sulfonamida / diaminopirimidina",
    "Infecções urinárias, respiratórias e outras, conforme associação e espectro do fármaco.",
    "Inibe a síntese de ácido fólico bacteriano: sulfonamidas bloqueiam a di-hidropteroato sintetase; trimetoprima e brodimoprima bloqueiam a di-hidrofolato redutase, com efeito frequentemente sinérgico quando associados.")

add(["metronidazol","nitrofurantoína"],
    "Antimicrobiano nitroimidazólico / nitrofurano",
    "Infecções por anaeróbios e protozoários (metronidazol); infecções urinárias baixas (nitrofurantoína).",
    "Após redução intracelular, danifica o DNA do microrganismo, levando à sua morte.")

add(["rifabutina","rifamicina","rifampicina","rifapentina"],
    "Antibiótico rifamicínico",
    "Tuberculose e outras micobacterioses; rifampicina também usada em profilaxia de meningite meningocócica.",
    "Inibe a RNA polimerase DNA-dependente bacteriana, bloqueando a transcrição.")

add(["isoniazida","etambutol","etionamida","pirazinamida","protionamida","capreomicin","delamanide"],
    "Antimicobacteriano (tuberculostático)",
    "Tratamento da tuberculose, geralmente em esquemas combinados.",
    "Mecanismos variados conforme o fármaco: interferência na síntese do ácido micólico da parede micobacteriana, na síntese proteica ou em outras vias metabólicas essenciais ao bacilo.")

add(["clofazimina","dapsona","difenilsulfona"],
    "Antimicobacteriano (antileprótico)",
    "Tratamento da hanseníase, geralmente em esquema poliquimioterápico.",
    "Dapsona (difenilsulfona) inibe a síntese de ácido fólico bacteriano; clofazimina liga-se ao DNA micobacteriano e apresenta ação anti-inflamatória associada.")

add(["daptomicina"],
    "Antibiótico lipopeptídeo",
    "Infecções por bactérias Gram-positivas, incluindo cepas multirresistentes (ex.: MRSA).",
    "Insere-se na membrana celular bacteriana, causando despolarização e morte celular.")

add(["linezolida","tedizolida"],
    "Antibiótico oxazolidinona",
    "Infecções por Gram-positivos multirresistentes (incluindo MRSA e enterococo resistente à vancomicina).",
    "Liga-se à subunidade ribossomal 50S, impedindo a formação do complexo de iniciação da síntese proteica bacteriana.")

add(["cloranfenicol","tianfenicol"],
    "Antibiótico fenicol",
    "Infecções graves selecionadas, quando outras opções não são adequadas, devido ao perfil de toxicidade.",
    "Liga-se à subunidade ribossomal 50S, inibindo a peptidil-transferase e a síntese proteica bacteriana.")

add(["polimixina B"],
    "Antibiótico polipeptídico (polimixina)",
    "Infecções por bactérias Gram-negativas multirresistentes, uso tópico ou sistêmico restrito.",
    "Atua como detergente catiônico sobre a membrana externa de bactérias Gram-negativas, aumentando sua permeabilidade.")

add(["bacitracina","gramicidina","tirotricina","mupirocina","retapamulina","nitrofural","mandelamina",
     "nitroxolina","clorfenesina","ácido fusídico"],
    "Antimicrobiano de uso tópico ou urinário",
    "Infecções cutâneas localizadas ou infecções urinárias baixas não complicadas, conforme o fármaco.",
    "Mecanismos variados (interferência na síntese de parede, membrana ou síntese proteica bacteriana), geralmente restritos a uso tópico ou como antisséptico urinário.")

add(["fosfomicina"],
    "Antibiótico fosfonato",
    "Infecção urinária não complicada, geralmente em dose única.",
    "Inibe a enzima MurA, bloqueando uma etapa inicial da síntese da parede celular bacteriana.")

add(["dactinomicina","mitomicina"],
    "Antibiótico antitumoral",
    "Uso oncológico especializado (não como antibacteriano de rotina em farmácia comunitária).",
    "Intercala-se no DNA (dactinomicina) ou forma ligações cruzadas no DNA (mitomicina), inibindo a replicação celular.")

# ============ CONTROLADOS DE USO CLÍNICO COMUM (curadoria seletiva) ============

add(["Morfina"], "Analgésico opioide (agonista opioide forte)",
    "Dor moderada a intensa, incluindo dor oncológica e pós-operatória.",
    "Agonista dos receptores opioides μ (mu), reduzindo a percepção da dor no sistema nervoso central.")

add(["Metadona"], "Analgésico opioide (agonista opioide forte)",
    "Dor crônica intensa; também usada em programas de manutenção para dependência de opioides.",
    "Agonista dos receptores opioides μ, com meia-vida longa; também antagoniza receptores NMDA.")

add(["Petidina"], "Analgésico opioide (agonista opioide forte)",
    "Dor moderada a intensa, incluindo uso obstétrico e pré-anestésico.",
    "Agonista dos receptores opioides μ, com potência inferior à morfina e ação mais curta.")

add(["Fentanila"], "Analgésico opioide (agonista opioide forte)",
    "Dor intensa, especialmente em anestesia e dor oncológica (uso transdérmico/parenteral).",
    "Agonista potente dos receptores opioides μ, com início de ação rápido e alta lipossolubilidade.")

add(["Tapentadol"], "Analgésico opioide (mecanismo duplo)",
    "Dor moderada a intensa, aguda ou crônica.",
    "Agonista dos receptores opioides μ combinado à inibição da recaptação de noradrenalina.")

add(["Oxicodona"], "Analgésico opioide (agonista opioide forte)",
    "Dor moderada a intensa.",
    "Agonista dos receptores opioides μ e kappa no sistema nervoso central.")

add(["Hidrocodona"], "Analgésico opioide (agonista opioide)",
    "Dor moderada; antitussígeno em algumas formulações.",
    "Agonista dos receptores opioides μ.")

add(["Hidromorfona"], "Analgésico opioide (agonista opioide forte)",
    "Dor moderada a intensa.",
    "Agonista dos receptores opioides μ, com maior potência que a morfina.")

add(["Buprenorfina"], "Analgésico opioide (agonista parcial)",
    "Dor moderada a intensa; tratamento de dependência de opioides.",
    "Agonista parcial dos receptores opioides μ e antagonista kappa, com efeito teto para depressão respiratória.")

add(["Codeína"], "Analgésico opioide fraco / antitussígeno",
    "Dor leve a moderada; supressão da tosse.",
    "Agonista opioide fraco; parcialmente convertido em morfina no fígado (via CYP2D6).")

add(["Tramadol"], "Analgésico opioide (mecanismo duplo)",
    "Dor moderada a intensa.",
    "Agonista fraco dos receptores opioides μ combinado à inibição da recaptação de serotonina e noradrenalina.")

add(["Dextropropoxifeno"], "Analgésico opioide fraco",
    "Dor leve a moderada.",
    "Agonista opioide fraco dos receptores μ, estruturalmente relacionado à metadona.")

add(["Nalbufina"], "Analgésico opioide (agonista-antagonista)",
    "Dor moderada a intensa.",
    "Agonista dos receptores kappa e antagonista parcial dos receptores μ.")

add(["Anfetamina","Dexanfetamina","Levanfetamina"], "Psicoestimulante (anfetamínico)",
    "Transtorno de déficit de atenção e hiperatividade (TDAH); narcolepsia, conforme o país.",
    "Aumenta a liberação e bloqueia a recaptação de dopamina e noradrenalina nas terminações nervosas.")

add(["Metilfenidato"], "Psicoestimulante",
    "Transtorno de déficit de atenção e hiperatividade (TDAH); narcolepsia.",
    "Inibe a recaptação de dopamina e noradrenalina, aumentando sua concentração na fenda sináptica.")

add(["Lisdexanfetamina"], "Psicoestimulante (pró-fármaco anfetamínico)",
    "Transtorno de déficit de atenção e hiperatividade (TDAH); transtorno da compulsão alimentar.",
    "Pró-fármaco convertido em dexanfetamina no organismo, que aumenta a neurotransmissão dopaminérgica e noradrenérgica.")

add(["Dronabinol"], "Canabinoide sintético",
    "Náusea e vômito associados à quimioterapia; estímulo do apetite.",
    "Agonista dos receptores canabinoides CB1/CB2.")

add(["Diazepam","Clonazepam","Alprazolam","Bromazepam","Lorazepam","Clordiazepóxido","Clorazepato",
     "Flurazepam","Nitrazepam","Triazolam","Midazolam","Oxazepam","Temazepam","Estazolam","Clobazam"],
    "Ansiolítico/hipnótico benzodiazepínico",
    "Ansiedade, insônia, espasmo muscular, crises convulsivas e sedação pré-procedimento (conforme o fármaco). Clobazam também usado como adjuvante em epilepsias refratárias (ex.: síndrome de Lennox-Gastaut).",
    "Potencializa a ação do GABA no receptor GABA-A, aumentando a frequência de abertura dos canais de cloreto e a inibição neuronal.")

add(["Zolpidem"], "Hipnótico não benzodiazepínico (análogo Z)",
    "Insônia, tratamento de curta duração.",
    "Agonista seletivo do receptor GABA-A (subunidade alfa-1), com efeito predominantemente hipnótico.")

add(["Zopiclona","Eszopiclona"], "Hipnótico não benzodiazepínico (análogo Z)",
    "Insônia, tratamento de curta duração.",
    "Potencializa a ação do GABA no receptor GABA-A, de forma semelhante aos benzodiazepínicos.")

add(["Fenobarbital"], "Anticonvulsivante / sedativo barbitúrico",
    "Epilepsia (diversas formas de crise); sedação.",
    "Potencializa e prolonga a abertura dos canais de cloreto mediados pelo GABA-A, deprimindo a atividade neuronal.")

add(["Cetamina","Escetamina"], "Anestésico dissociativo",
    "Indução e manutenção de anestesia; escetamina também em depressão resistente ao tratamento.",
    "Antagonista dos receptores NMDA de glutamato.")

add(["Carisoprodol"], "Relaxante muscular de ação central",
    "Espasmo muscular agudo doloroso.",
    "Metabolizado em meprobamato; deprime a atividade do sistema nervoso central, com ação relaxante muscular.")

add(["Modafinila","Armodafinila"], "Estimulante do sistema nervoso central (promotor de vigília)",
    "Narcolepsia e outros distúrbios com sonolência excessiva.",
    "Mecanismo não totalmente elucidado; envolve modulação dopaminérgica e de outros sistemas de vigília no SNC.")

add(["Sibutramina"], "Anorexígeno (inibidor de recaptação)",
    "Obesidade, como adjuvante de dieta e exercício (uso restrito).",
    "Inibe a recaptação de serotonina e noradrenalina, promovendo saciedade.")

add(["Anfepramona","Femproporex","Fendimetrazina","Fentermina","Mazindol","Mefenorex"], "Anorexígeno (anfetamínico ou correlato)",
    "Obesidade, como adjuvante de dieta e exercício (uso restrito e por tempo limitado).",
    "Estimula a liberação de catecolaminas no SNC, promovendo saciedade e redução do apetite.")

add(["Isotretinoína"], "Retinoide sistêmico",
    "Acne nodulocística grave refratária a outros tratamentos.",
    "Reduz o tamanho e a secreção das glândulas sebáceas e normaliza a queratinização folicular; ação mediada por receptores nucleares de ácido retinoico.")

add(["Acitretina"], "Retinoide sistêmico",
    "Psoríase grave e outras dermatoses de queratinização.",
    "Normaliza a proliferação e diferenciação dos queratinócitos via receptores nucleares de ácido retinoico.")

add(["Adapaleno","Tretinoína"], "Retinoide tópico",
    "Acne vulgar.",
    "Normaliza a queratinização folicular e reduz a formação de comedões via receptores de ácido retinoico.")

add(["Bexaroteno"], "Retinoide (rexinoide) sistêmico",
    "Linfoma cutâneo de células T.",
    "Ativa seletivamente os receptores retinoides X (RXR), modulando a proliferação e diferenciação celular.")

add(["Ftalimidoglutarimida (talidomida)"], "Imunomodulador",
    "Hanseníase (eritema nodoso hansênico) e mieloma múltiplo.",
    "Ação imunomoduladora e anti-inflamatória, incluindo inibição do TNF-alfa; efeito antiangiogênico. Uso contraindicado na gestação por risco teratogênico grave.")

add(["Lenalidomida","Pomalidomida"], "Imunomodulador (análogo da talidomida)",
    "Mieloma múltiplo e outras neoplasias hematológicas selecionadas.",
    "Ação imunomoduladora, antiangiogênica e antineoplásica; análogos estruturais da talidomida com perfil de eficácia distinto.")

add(["Testosterona","Metiltestosterona"], "Andrógeno / esteroide anabolizante",
    "Reposição em hipogonadismo masculino.",
    "Ativa receptores androgênicos, promovendo efeitos anabólicos e virilizantes.")

add(["Nandrolona","Oxandrolona","Estanozolol","Boldenona","Metandienona ou metandrostenolona",
     "Mesterolona","Drostanolona"], "Esteroide anabolizante androgênico",
    "Uso terapêutico restrito (ex.: certas formas de caquexia ou osteoporose); amplamente associado ao uso não terapêutico para ganho de massa muscular.",
    "Ativa receptores androgênicos, estimulando a síntese proteica muscular; efeitos virilizantes associados.")

add(["Somatropina (hormônio do crescimento humano)","Somapacitana","Somatrogona"], "Hormônio de crescimento (GH recombinante)",
    "Deficiência de hormônio do crescimento e outras condições específicas de baixa estatura.",
    "Atua no receptor de GH, estimulando a produção hepática de IGF-1 e promovendo crescimento linear e efeitos metabólicos.")

add(["Prasterona (deidroepiandrosterona - DHEA)"], "Precursor hormonal esteroide",
    "Uso terapêutico restrito, conforme indicação específica.",
    "Precursor de andrógenos e estrogênios, convertido perifericamente em hormônios sexuais ativos.")

# ============ LISTA C1: cobertura ampla por classe (antidepressivos, antipsicóticos, anticonvulsivantes etc.) ============

add(["Amitriptilina","Amoxapina","Butriptilina","Clomipramina","Desipramina","Dibenzepina",
     "Dimetracrina","Doxepina","Imipramina","Imipraminóxido","Maprotilina","Mianserina",
     "Nortriptilina","Noxiptilina","Opipramol","Protriptilina","Trimipramina"],
    "Antidepressivo tricíclico/tetracíclico",
    "Depressão; alguns também usados em dor neuropática crônica, enxaqueca profilática e enurese noturna.",
    "Inibe a recaptação de serotonina e noradrenalina nas terminações nervosas; vários têm ação antihistamínica e anticolinérgica associada.")

add(["Citalopram","Escitalopram","Fluoxetina","Fluvoxamina","Paroxetina","Sertralina"],
    "Antidepressivo ISRS (inibidor seletivo da recaptação de serotonina)",
    "Depressão, transtornos de ansiedade, transtorno obsessivo-compulsivo e outros transtornos relacionados.",
    "Inibe seletivamente a recaptação de serotonina na fenda sináptica, aumentando sua disponibilidade.")

add(["Desvenlafaxina","Duloxetina","Levomilnaciprana","Milnaciprana","Venlafaxina"],
    "Antidepressivo IRSN (inibidor da recaptação de serotonina e noradrenalina)",
    "Depressão e transtornos de ansiedade; alguns também usados em dor neuropática e fibromialgia.",
    "Inibe a recaptação de serotonina e noradrenalina na fenda sináptica.")

add(["Fenelzina","Feniprazina","Iproclozida","Isocarboxazida","Moclobemida","Nialamida",
     "Tranilcipromina","Selegilina","Rasagilina","Caroxazona"],
    "Antidepressivo/antiparkinsoniano IMAO (inibidor da monoaminoxidase)",
    "Depressão resistente a outros tratamentos (IMAOs clássicos); selegilina e rasagilina usadas na doença de Parkinson.",
    "Inibe a enzima monoaminoxidase, reduzindo a degradação de serotonina, noradrenalina e dopamina.")

add(["Agomelatina","Bupropiona","Mirtazapina","Nefazodona","Reboxetina","Tianeptina","Trazodona",
     "Vilazodona","Vortioxetina","Nomifensina","Minaprina"],
    "Antidepressivo atípico",
    "Depressão; alguns também usados como auxiliares no manejo da insônia associada ou na cessação do tabagismo (bupropiona).",
    "Mecanismos variados conforme o fármaco (ex.: bupropiona inibe a recaptação de dopamina/noradrenalina; mirtazapina antagoniza receptores alfa-2 e serotoninérgicos; trazodona antagoniza receptores de serotonina).")

add(["Dapoxetina"], "Inibidor seletivo da recaptação de serotonina (ação curta)",
    "Ejaculação precoce.",
    "Inibe a recaptação de serotonina de forma rápida e curta, retardando o reflexo ejaculatório.")

add(["Atomoxetina"], "Inibidor seletivo da recaptação de noradrenalina",
    "Transtorno de déficit de atenção e hiperatividade (TDAH), como alternativa não estimulante.",
    "Inibe seletivamente a recaptação de noradrenalina, sem ação estimulante direta sobre a dopamina.")

add(["Clorpromazina","Levomepromazina","Flufenazina","Perfenazina","Trifluoperazina","Tioridazina",
     "Mesoridazina","Promazina","Proclorperazina","Metopromazina","Mepazina",
     "Periciazina (propericiazina)","Dixirazina","Homofenazina","Imicloprazina","Butaperazina",
     "Tioproperazina","Haloperidol","Droperidol","Moperona","Trifluperidol","Penfluridol","Pimozida",
     "Clorprotixeno","Tiotixeno","Zuclopentixol","Flupentixol","Clotiapina","Loxapina","Oxipertina",
     "Sulpirida","Sultoprida","Tiaprida","Amissulprida","Veraliprida"],
    "Antipsicótico típico (fenotiazínico, butirofenona ou tioxanteno)",
    "Esquizofrenia e outros transtornos psicóticos; alguns também usados como antieméticos ou sedativos, conforme o fármaco.",
    "Antagoniza principalmente os receptores dopaminérgicos D2 no sistema nervoso central.")

add(["Aripiprazol","Asenapina","Brexpiprazol","Clozapina","Lurasidona","Olanzapina","Paliperidona",
     "Quetiapina","Risperidona","Ziprasidona","Zotepina","Pipamperona","Pipotiazina"],
    "Antipsicótico atípico (de segunda geração)",
    "Esquizofrenia, transtorno bipolar e outros transtornos psicóticos, conforme o fármaco.",
    "Antagoniza receptores dopaminérgicos D2 e serotoninérgicos 5-HT2A, com perfil de efeitos extrapiramidais geralmente menor que os antipsicóticos típicos.")

add(["Ácido valpróico","Divalproato de sódio","Valproato sódico","Beclamida","Brivaracetam",
     "Carbamazepina","Cenobamato","Estiripentol","Etossuximida","Fenitoina","Gabapentina",
     "Lacosamida","Lamotrigina","Levetiracetam","Oxcarbazepina","Pregabalina","Primidona",
     "Rufinamida","Tiagabina","Topiramato","Vigabatrina"],
    "Anticonvulsivante",
    "Epilepsia (diversas formas de crise); alguns também usados em dor neuropática (gabapentina, pregabalina) e transtorno bipolar (valproato, carbamazepina, lamotrigina).",
    "Mecanismos variados conforme o fármaco (bloqueio de canais de sódio/cálcio voltagem-dependentes ou potencialização do GABA, entre outros), reduzindo a excitabilidade neuronal excessiva.")

add(["Buspirona"], "Ansiolítico não benzodiazepínico (azapirona)",
    "Transtorno de ansiedade generalizada.",
    "Agonista parcial dos receptores serotoninérgicos 5-HT1A.")

add(["Amantadina","Biperideno","Entacapona","Pramipexol","Ropinirol","Rotigotina","Tolcapona",
     "Pergolida","Lisurida","Deutetrabenazina","Tetrabenazina"],
    "Antiparkinsoniano / modulador do sistema dopaminérgico",
    "Doença de Parkinson e outros distúrbios do movimento, conforme o fármaco.",
    "Mecanismos variados (agonismo dopaminérgico direto, inibição da COMT, ação anticolinérgica, ou depleção de dopamina em tetrabenazina/deutetrabenazina).")

add(["Donepezila","Galantamina","Rivastigmina","Tacrina","Memantina"], "Antidemencial",
    "Doença de Alzheimer e outras demências, conforme estágio e fármaco.",
    "Inibidores da acetilcolinesterase (donepezila, galantamina, rivastigmina, tacrina) aumentam a disponibilidade de acetilcolina; memantina antagoniza receptores NMDA de glutamato.")

add(["Desflurano","Enflurano","Halotano","Isoflurano","Metoxiflurano","Sevoflurano"],
    "Anestésico geral inalatório",
    "Indução e/ou manutenção de anestesia geral.",
    "Deprime o sistema nervoso central por mecanismos ainda não totalmente elucidados, envolvendo canais iônicos neuronais, induzindo perda de consciência.")

add(["Etomidato","Propofol","Propanidina","Hidroxidiona","Dexmedetomidina"],
    "Anestésico geral / sedativo intravenoso",
    "Indução e manutenção de anestesia geral; dexmedetomidina também usada como sedativo em UTI.",
    "Potencializa a ação do GABA no receptor GABA-A (maioria) ou age em receptores alfa-2 adrenérgicos (dexmedetomidina), deprimindo o SNC.")

add(["Tetracaína","Proximetacaina","Oxibuprocaína (benoxinato)"], "Anestésico local (uso oftálmico/tópico)",
    "Anestesia tópica, especialmente oftálmica.",
    "Bloqueia os canais de sódio voltagem-dependentes nos nervos sensoriais, impedindo a condução do impulso doloroso.")

add(["Ciclopentolato"], "Midriático e cicloplégico anticolinérgico",
    "Exame oftalmológico (dilatação pupilar) e cicloplegia.",
    "Antagoniza os receptores muscarínicos da íris e do músculo ciliar, causando midríase e paralisia da acomodação.")

add(["Naloxona","Naltrexona","Metilnaltrexona"], "Antagonista opioide",
    "Reversão de intoxicação/overdose por opioides (naloxona); manutenção da abstinência (naltrexona); constipação induzida por opioides (metilnaltrexona).",
    "Bloqueia competitivamente os receptores opioides (principalmente μ), revertendo os efeitos de agonistas opioides.")

add(["Flumazenil"], "Antagonista benzodiazepínico",
    "Reversão da sedação por benzodiazepínicos (intoxicação ou pós-procedimento).",
    "Antagoniza competitivamente o receptor GABA-A no sítio benzodiazepínico, revertendo a sedação.")

add(["Lítio"], "Estabilizador de humor",
    "Transtorno bipolar (fases maníaca e de manutenção).",
    "Mecanismo não totalmente elucidado; envolve modulação de vias de sinalização intracelular no sistema nervoso central.")

add(["Celecoxibe","Etoricoxibe","Lumiracoxibe","Parecoxibe","Rofecoxibe","Valdecoxibe"],
    "Anti-inflamatório não esteroide (inibidor seletivo da COX-2)",
    "Dor e inflamação, especialmente em condições osteoarticulares.",
    "Inibe seletivamente a enzima ciclo-oxigenase-2 (COX-2), reduzindo a síntese de prostaglandinas pró-inflamatórias com menor impacto na COX-1 gástrica.")

add(["Canabidiol (CBD)"], "Canabinoide não psicoativo",
    "Formas raras e graves de epilepsia refratária (ex.: síndromes de Dravet e Lennox-Gastaut), conforme registro.",
    "Ação moduladora sobre o sistema endocanabinoide e outros receptores (ex.: TRPV1, 5-HT1A); mecanismo anticonvulsivante não totalmente elucidado.")

add(["Cisaprida"], "Procinético gastrointestinal",
    "Distúrbios da motilidade gastrointestinal (uso restrito por risco cardíaco).",
    "Agonista dos receptores serotoninérgicos 5-HT4, aumentando a motilidade do trato gastrointestinal.")

add(["Loperamida"], "Antidiarreico opioide (ação periférica)",
    "Diarreia aguda não complicada.",
    "Agonista dos receptores opioides μ no trato gastrointestinal, reduzindo a motilidade intestinal, com mínima ação central.")

add(["Dissulfiram"], "Sensibilizador ao álcool (dissuasor)",
    "Tratamento adjuvante da dependência alcoólica.",
    "Inibe a enzima aldeído desidrogenase, causando acúmulo de acetaldeído e reação desagradável após ingestão de álcool.")

add(["Misoprostol"], "Análogo de prostaglandina E1",
    "Prevenção de úlcera péptica associada a AINEs; uso obstétrico conforme protocolo específico.",
    "Atua nos receptores de prostaglandina, com ação citoprotetora gástrica e efeito uterotônico.")

add(["Molnupiravir","Ribavirina"], "Antiviral",
    "Infecções virais específicas, conforme o fármaco (ex.: COVID-19 para molnupiravir; hepatite C e outras viroses para ribavirina).",
    "Interfere na replicação viral (molnupiravir induz erros na cópia do RNA viral; ribavirina inibe a síntese de RNA/DNA viral por mecanismos variados).")

add(["Teriflunomida","Leflunomida"], "Imunomodulador (inibidor da síntese de pirimidinas)",
    "Esclerose múltipla remitente-recorrente (teriflunomida); artrite reumatoide (leflunomida).",
    "Inibe a enzima di-hidro-orotato desidrogenase, reduzindo a proliferação de linfócitos ativados.")

with open("detalhes_farmacologicos.json", "w", encoding="utf-8") as f:
    json.dump(detalhes, f, ensure_ascii=False, indent=2)

print(f"Total de substâncias com detalhes curados: {len(detalhes)}")

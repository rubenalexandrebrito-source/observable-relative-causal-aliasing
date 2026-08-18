# -*- coding: utf-8 -*-
"""
POST-CONFIRMATORY / EXPLORATORY — Pré-registo A v8.3, Fase 6.
Prevalência do CANCELAMENTO POR AGREGAÇÃO em novas instâncias II.

O resultado confirmatório permanece NEGATIVO e imutável. Este script NÃO lê
nem escreve artefactos confirmatórios além das cópias de leitura já feitas,
NÃO altera C1' e NÃO propõe critério novo. É medição descritiva.

Amostra: famílias II elegíveis, semente exploratória NOVA 910000001
(fluxo posicional [0] de SeedSequence.spawn(4), idêntico ao gerar_lote;
fluxos [1..3] não usados: análise estrutural canónica, sem cegamento).

Por aresta canal->processador (C_AB->B, C_BA->A), com a fibra counterfactual
COMPLETA (exactamente a maquinaria de C1'):
  dep_sites : nº de (intervenção, configuração-livre) em que a resposta do
              receptor difere entre m=0 e m=1 (dependência ponto-a-ponto)
  L1_d_iguais               : d_0 == d_1 (cancela já na soma de Hamming)
  L2_rank_igual_d_diferente : d_0 != d_1 mas rank(d_0) == rank(d_1)
  L3_rank_diferente         : rank(d_0) != rank(d_1)  (C1' individua)

Por instância (o ciclo A->C_AB->B->C_BA->A só se parte com >=1 aresta L3):
  individua_ambas / individua_uma / colapso_total (=classe do erro fam-20)

NOTA E1/E2: os módulos D1/D2 são inertes para este estatístico — configurações
da fibra que diferem só nos bits D têm respostas idênticas do receptor, pelo
que d^{E2} = 4*d^{E1}, mesmos ranks, mesmas igualdades. n=10 transfere para E2.
"""
import sys, json, time, hashlib
from dataclasses import asdict
import numpy as np

DST = "/root/causal-A-postconfirmatory-analysis"
sys.path.insert(0, DST + "/frozen-copy")
import gerador as g            # congelado (12/12 vs manifesto)
import classificador as cl     # congelado

SEED_EXPLORATORIO = 910000001
N_ALVO = 5000
MAX_TENTATIVAS = 200000
TEMPO_MAX_S = 420
SAIDA = DST + "/prevalencia/prevalencia-cancelamento-II.json"

# arestas canal->processador no layout canónico II (n=10)
ARESTAS = (("C_AB->B", [6, 7], [3, 4, 5], [5]),
           ("C_BA->A", [8, 9], [0, 1, 2], [2]))


def analisa_aresta(T, n, bits_a, bits_b, membits):
    eB = cl.extractor(bits_b, n)
    popB = cl.popcount_tab(len(bits_b))
    ints = cl.intervencoes(bits_a)
    Z0 = cl.estados_da_fibra(n, membits, 0)
    Z1 = cl.estados_da_fibra(n, membits, 1)
    nx0 = eB[T[Z0]]
    nx1 = eB[T[Z1]]
    d0, d1, dep = [], [], 0
    for (mk, vl) in ints:
        x0 = eB[T[(Z0 & ~np.int64(mk)) | np.int64(vl)]] ^ nx0
        x1 = eB[T[(Z1 & ~np.int64(mk)) | np.int64(vl)]] ^ nx1
        d0.append(int(popB[x0].sum()))
        d1.append(int(popB[x1].sum()))
        dep += int((x0 != x1).sum())
    if d0 == d1:
        nivel = "L1_d_iguais"
    elif cl.rank_canonico(d0) == cl.rank_canonico(d1):
        nivel = "L2_rank_igual_d_diferente"
    else:
        nivel = "L3_rank_diferente"
    return {"nivel": nivel, "dep_sites": dep, "d0": d0, "d1": d1}


def theta_sha(th):
    return hashlib.sha256(
        json.dumps(asdict(th), sort_keys=True).encode()).hexdigest()


def fam20_referencia():
    """Classifica nos mesmos níveis as duas arestas da instância confirmatória
    falhada (leitura das CÓPIAS na área exploratória; nada é alterado)."""
    import pontuacao as pt
    ID = "7bb0baab3a8ed7aa"
    chave = json.load(open(DST + "/chave-e2.json"))
    inst = json.load(open(DST + "/conf-e2/instancias/%s.json" % ID))
    tipos = pt._tipos_e2(chave[ID])
    _, n, T, mods, _ = cl.carregar(inst)
    T = np.asarray(T, dtype=np.int64)
    idx = {t: i for i, t in enumerate(tipos)}
    out = {}
    for nome, a_t, b_t in (("C_AB->B", "C_AB", "B"), ("C_BA->A", "C_BA", "A")):
        a_i, b_i = idx[a_t], idx[b_t]
        r = analisa_aresta(T, n, mods[a_i]["bits"], mods[b_i]["bits"],
                           mods[b_i]["bits_memoria"])
        out[nome] = r
    return out


def main():
    t0 = time.time()
    ss = np.random.SeedSequence(SEED_EXPLORATORIO)
    filhos = ss.spawn(4)
    rng_theta = np.random.Generator(np.random.PCG64(filhos[0]))

    rejeicoes = {}
    tentativa = 0
    registos = []
    edge_niveis = {"L1_d_iguais": 0, "L2_rank_igual_d_diferente": 0,
                   "L3_rank_diferente": 0}
    edge_dep_zero = 0
    inst_classes = {"individua_ambas": 0, "individua_uma": 0,
                    "colapso_total": 0}
    subtipos_colapso = {}
    anomalias_mem_reach = 0
    parou_por_tempo = False

    while len(registos) < N_ALVO and tentativa < MAX_TENTATIVAS:
        if tentativa % 200 == 0 and (time.time() - t0) > TEMPO_MAX_S:
            parou_por_tempo = True
            break
        tentativa += 1
        th = g.sample_theta_base(rng_theta)
        if th.pi[0] == th.pi[1]:
            rejeicoes["pi_identicas"] = rejeicoes.get("pi_identicas", 0) + 1
            continue
        ok, razao, _ = g.elegibilidade(th, False)
        if not ok:
            rejeicoes[razao] = rejeicoes.get(razao, 0) + 1
            continue

        tab, n, lay = g.tabela_transicao("II", th, False)
        T = np.asarray(tab, dtype=np.int64)
        s0 = g._campos_para_int(g.estado_inicial("II", th), lay)
        orb = cl.orbita(T, s0)
        for mb in (2, 5):                       # mA, mB canónicos
            if {(int(z) >> mb) & 1 for z in orb} != {0, 1}:
                anomalias_mem_reach += 1

        rec = {"fam": len(registos), "tentativa": tentativa,
               "theta_sha": theta_sha(th), "arestas": {}}
        niveis = []
        for nome, bits_a, bits_b, mem in ARESTAS:
            r = analisa_aresta(T, n, bits_a, bits_b, mem)
            edge_niveis[r["nivel"]] += 1
            if r["dep_sites"] == 0:
                edge_dep_zero += 1
            niveis.append(r["nivel"])
            keep = {"nivel": r["nivel"], "dep_sites": r["dep_sites"]}
            if r["nivel"] != "L3_rank_diferente":     # guardar d apenas nos colapsos
                keep["d0"] = r["d0"]
                keep["d1"] = r["d1"]
            rec["arestas"][nome] = keep
        n_l3 = sum(1 for v in niveis if v == "L3_rank_diferente")
        classe = {2: "individua_ambas", 1: "individua_uma",
                  0: "colapso_total"}[n_l3]
        rec["classe"] = classe
        inst_classes[classe] += 1
        if classe == "colapso_total":
            st = tuple(sorted(niveis))
            subtipos_colapso[str(st)] = subtipos_colapso.get(str(st), 0) + 1
        registos.append(rec)
        if len(registos) % 1000 == 0:
            print("progresso: %d aceites, %d tentativas, %.0fs"
                  % (len(registos), tentativa, time.time() - t0), flush=True)

    total = len(registos)
    # amostras a preservar: TODOS os colapsos + primeiras 20 de cada outra classe
    exemplos = {"colapso_total": [r for r in registos
                                  if r["classe"] == "colapso_total"],
                "individua_uma": [r for r in registos
                                  if r["classe"] == "individua_uma"][:20],
                "individua_ambas": [r for r in registos
                                    if r["classe"] == "individua_ambas"][:20]}

    try:
        sha_script = hashlib.sha256(open(__file__, "rb").read()).hexdigest()
    except Exception:
        sha_script = None

    import platform
    saida = {
        "rotulo": "POST-CONFIRMATORY / EXPLORATORY",
        "objectivo": "prevalencia do cancelamento por agregacao em novas II",
        "semente_exploratoria": SEED_EXPLORATORIO,
        "fluxo": "SeedSequence(910000001).spawn(4)[0] = theta nuclear (como gerar_lote); [1..3] nao usados",
        "exclusoes_respeitadas": "distinta das 20 da auditoria e das confirmatorias 3786434918/3786434919",
        "n_alvo": N_ALVO,
        "tentativas": tentativa,
        "aceites_total_instancias": total,
        "taxa_aceitacao": (total / tentativa) if tentativa else None,
        "parou_por_tempo": parou_por_tempo,
        "rejeicoes": rejeicoes,
        "anomalias_mem_reach": anomalias_mem_reach,
        "contagens_por_ARESTA": {
            "total_arestas": 2 * total,
            "com_dependencia_ponto_a_ponto": 2 * total - edge_dep_zero,
            "sem_dependencia_ponto_a_ponto": edge_dep_zero,
            "L1_d_iguais": edge_niveis["L1_d_iguais"],
            "L2_rank_igual_d_diferente": edge_niveis["L2_rank_igual_d_diferente"],
            "L3_rank_diferente": edge_niveis["L3_rank_diferente"],
            "dependencia_desaparece_apos_agregacao_L1_mais_L2":
                edge_niveis["L1_d_iguais"] + edge_niveis["L2_rank_igual_d_diferente"],
        },
        "contagens_por_INSTANCIA": {
            "individua_ambas": inst_classes["individua_ambas"],
            "individua_uma": inst_classes["individua_uma"],
            "colapso_total_erro_C1p": inst_classes["colapso_total"],
            "subtipos_colapso_total": subtipos_colapso,
        },
        "fam20_confirmatoria_referencia": fam20_referencia(),
        "duracao_s": round(time.time() - t0, 1),
        "ambiente": {"python": platform.python_version(),
                     "numpy": np.__version__,
                     "plataforma": platform.platform()},
        "sha256_script": sha_script,
        "exemplos": exemplos,
    }
    corpo = json.dumps(saida, sort_keys=True, indent=1).encode()
    open(SAIDA, "wb").write(corpo)
    print("\n===== RESUMO =====")
    print("instancias II aceites          :", total,
          "(tentativas %d, aceitacao %.3f)" % (tentativa, total / tentativa))
    ca = saida["contagens_por_ARESTA"]
    print("arestas com dep ponto-a-ponto  : %d / %d  (sem dep: %d)"
          % (ca["com_dependencia_ponto_a_ponto"], ca["total_arestas"],
             ca["sem_dependencia_ponto_a_ponto"]))
    print("  L1 d0==d1                    :", ca["L1_d_iguais"])
    print("  L2 d0!=d1, rank igual        :", ca["L2_rank_igual_d_diferente"])
    print("  L3 rank diferente            :", ca["L3_rank_diferente"])
    ci = saida["contagens_por_INSTANCIA"]
    print("instancias individua_ambas     :", ci["individua_ambas"])
    print("instancias individua_uma       :", ci["individua_uma"])
    print("instancias COLAPSO TOTAL       : %d  (%.3f%%)  subtipos=%s"
          % (ci["colapso_total_erro_C1p"],
             100.0 * ci["colapso_total_erro_C1p"] / total,
             ci["subtipos_colapso_total"]))
    f20 = saida["fam20_confirmatoria_referencia"]
    print("fam20 (confirmatoria, ref)     :",
          {k: (v["nivel"], "dep=%d" % v["dep_sites"]) for k, v in f20.items()})
    print("saida:", SAIDA)
    print("sha256_saida:", hashlib.sha256(corpo).hexdigest())
    print("sha256_script:", sha_script)


if __name__ == "__main__":
    main()

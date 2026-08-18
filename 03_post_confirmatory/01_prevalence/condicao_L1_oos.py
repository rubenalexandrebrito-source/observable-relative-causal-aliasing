# -*- coding: utf-8 -*-
"""
POST-CONFIRMATORY / EXPLORATORY — Condição estrutural K para L1.

DERIVAÇÃO (dinâmica congelada, variante II canónica, aresta canal->processador):
No passo II: y' = G0[y][pi[mB][cAB]] ^ sigmaB[mB]; mB' = K[mB][y] (não lê canal).
No XOR contrafactual (intervenção vs baseline no MESMO contexto m):
  * sigma cancela sempre (offset constante do contexto);
  * mB' nunca muda => Hamming só nos bits não-memória;
  * a contribuição de cada ponto da fibra depende apenas de (r, c) —
    r = valor não-memória do receptor, c = valor do canal — cada par (r,c)
    aparece com multiplicidade 2^5 = 32 na fibra n=10.
Logo, exactamente:
    d_m(a) = 32 * sum_c Wtil_m(c, sub_a(c)),
    Wtil_m(c1,c2) = sum_r pc2( M[r][pi_m(c1)] ^ M[r][pi_m(c2)] ),
com M = G0 (aresta C_AB->B) ou F0 (aresta C_BA->A) e sub_a a substituição da
intervenção nos 2 bits do canal.

CONDIÇÃO K (por aresta):  Wtil_0 == Wtil_1
  <=>  tau := pi1 o pi0^{-1} é ISOMETRIA de W(p,q) = sum_r pc2(M[r][p]^M[r][q]).

TEOREMA (previsto; testado aqui exaustivamente): K <=> L1.
  Suficiência: trivial pela fórmula. Necessidade: as 9 intervenções impõem a
  Delta = Wtil_0 - Wtil_1 (simétrica, diagonal nula, 6 g.l.):
    somas-linha nulas (do(c=γ), 4 eqs) e e01+e23=0, e02+e13=0 (bits isolados);
  o sistema só tem a solução Delta=0.

Este script:
 (1) REPLAY determinístico dos lotes exploratórios (sementes em SEEDS) e, por
     aresta: nível L1/L2/L3 pela fibra (maquinaria congelada) + K estrutural
     + verificação exacta da fórmula d_m == 32*sum_c Wtil_m(c,sub_a(c));
 (2) matriz de confusão K vs L1 (TP/FP/TN/FN, sens/espec/precisão);
 (3) estatística por classe de conjugação de tau + explicação da correlação
     entre arestas (mesmo tau; Jensen);
 (4) controlos emparelhados: mesmo tau, K falso => L3;
 (5) família confirmatória 20 (cega, n=12): phi_m(r,c) bem definida e
     Wtil_0 == Wtil_1 verificado directamente na tabela.
NÃO altera C1', targets, thresholds nem artefactos confirmatórios.
"""
import sys, json, time, hashlib, itertools
import numpy as np

DST = "/root/causal-A-postconfirmatory-analysis"
sys.path.insert(0, DST + "/frozen-copy")
import gerador as g
import classificador as cl

SEEDS = [910000004]
N_POR_SEED = 5000
INCLUI_FAM20 = False
SAIDA = DST + "/prevalencia/condicao-L1-oos.json"

ARESTAS = (("C_AB->B", [6, 7], [3, 4, 5], [5], "G0"),
           ("C_BA->A", [8, 9], [0, 1, 2], [2], "F0"))


def pc2(v):
    return bin(v).count("1")


def wtil(M, perm):
    return tuple(tuple(sum(pc2(M[r][perm[c1]] ^ M[r][perm[c2]])
                           for r in range(4)) for c2 in range(4))
                 for c1 in range(4))


def w_base(M):
    return tuple(tuple(sum(pc2(M[r][p] ^ M[r][q]) for r in range(4))
                       for q in range(4)) for p in range(4))


def grupo_iso(W):
    return [p for p in itertools.permutations(range(4))
            if all(W[p[a]][p[b]] == W[a][b] for a in range(4) for b in range(4))]


def tau_de(pi0, pi1):
    inv0 = [0] * 4
    for c, p in enumerate(pi0):
        inv0[p] = c
    return tuple(pi1[inv0[p]] for p in range(4))


def cycle_type(perm):
    seen = [False] * 4
    t = []
    for i in range(4):
        if not seen[i]:
            l, j = 0, i
            while not seen[j]:
                seen[j] = True
                j = perm[j]
                l += 1
            t.append(l)
    return tuple(sorted(t))


def fibra(T, n, ints, bits_b, mem):
    eB = cl.extractor(bits_b, n)
    popB = cl.popcount_tab(len(bits_b))
    Z0 = cl.estados_da_fibra(n, mem, 0)
    Z1 = cl.estados_da_fibra(n, mem, 1)
    nx0 = eB[T[Z0]]
    nx1 = eB[T[Z1]]
    d0, d1, dep = [], [], 0
    for (mk, vl) in ints:
        x0 = eB[T[(Z0 & ~np.int64(mk)) | np.int64(vl)]] ^ nx0
        x1 = eB[T[(Z1 & ~np.int64(mk)) | np.int64(vl)]] ^ nx1
        d0.append(int(popB[x0].sum()))
        d1.append(int(popB[x1].sum()))
        dep += int((x0 != x1).sum())
    return d0, d1, dep


def nivel_de(d0, d1):
    if d0 == d1:
        return "L1"
    if cl.rank_canonico(d0) == cl.rank_canonico(d1):
        return "L2"
    return "L3"


def subs_canal(ints, bits_a):
    lo, hi = bits_a
    out = []
    for (mk, vl) in ints:
        mc = ((mk >> lo) & 1) | (((mk >> hi) & 1) << 1)
        vc = ((vl >> lo) & 1) | (((vl >> hi) & 1) << 1)
        out.append((mc, vc))
    return out


def fam20_check():
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
        A, B = mods[idx[a_t]], mods[idx[b_t]]
        mb = B["bits_memoria"][0]
        rb = [b for b in B["bits"] if b != mb]
        cb = A["bits"]
        er = cl.extractor(rb, n)
        ec = cl.extractor(cb, n)
        em = cl.extractor([mb], n)
        phi = {}
        memnext = {}
        consistente = True
        for z in range(1 << n):
            key = (int(em[z]), int(er[z]), int(ec[z]))
            val = int(er[T[int(z)]])
            mval = int(em[T[int(z)]])
            if key in phi and phi[key] != val:
                consistente = False
                break
            phi[key] = val
            k2 = (key[0], key[1])
            if k2 in memnext and memnext[k2] != mval:
                # mem-next pode depender de r e m apenas; canal nao entra
                consistente = False
                break
            memnext[k2] = mval
        Ws = {}
        if consistente:
            for m in (0, 1):
                W = [[sum(pc2(phi[(m, r, c1)] ^ phi[(m, r, c2)])
                          for r in range(4)) for c2 in range(4)]
                     for c1 in range(4)]
                Ws[m] = W
        out[nome] = {"phi_bem_definida": consistente,
                     "Wtil_m0": Ws.get(0), "Wtil_m1": Ws.get(1),
                     "K": (Ws.get(0) == Ws.get(1)) if consistente else None}
    return out


def main():
    t0 = time.time()
    ints_por_aresta = {}
    conf = {"C_AB->B": {"TP": 0, "FP": 0, "TN": 0, "FN": 0},
            "C_BA->A": {"TP": 0, "FP": 0, "TN": 0, "FN": 0}}
    formula_falhas = 0
    iso_vs_K_mismatch = 0
    por_classe = {}
    tau_exemplos = {}
    n_fam = 0
    both_L1 = 0
    L1_B = 0
    L1_A = 0
    niveis_inst = {"colapso_total": 0, "individua_uma": 0, "individua_ambas": 0}
    exemplos_L1 = []
    exemplos_ctrl = []
    w_sym_sem_K = {"C_AB->B": 0, "C_BA->A": 0}

    for seed in SEEDS:
        ss = np.random.SeedSequence(seed)
        rng_theta = np.random.Generator(np.random.PCG64(ss.spawn(4)[0]))
        aceites = 0
        tent = 0
        while aceites < N_POR_SEED and tent < 200000:
            tent += 1
            th = g.sample_theta_base(rng_theta)
            if th.pi[0] == th.pi[1]:
                continue
            ok, _, _ = g.elegibilidade(th, False)
            if not ok:
                continue
            aceites += 1
            n_fam += 1
            tab, n, lay = g.tabela_transicao("II", th, False)
            T = np.asarray(tab, dtype=np.int64)
            tau = tau_de(th.pi[0], th.pi[1])
            cls = str(cycle_type(tau))
            reg = por_classe.setdefault(cls, {"n": 0, "K_B": 0, "K_A": 0,
                                              "L1_B": 0, "L1_A": 0})
            reg["n"] += 1
            niveis = []
            for nome, ba, bb, mem, tn in ARESTAS:
                if nome not in ints_por_aresta:
                    ints_por_aresta[nome] = (cl.intervencoes(ba),
                                             subs_canal(cl.intervencoes(ba), ba))
                ints, sc = ints_por_aresta[nome]
                d0, d1, dep = fibra(T, n, ints, bb, mem)
                nv = nivel_de(d0, d1)
                niveis.append(nv)
                M = th.G0 if tn == "G0" else th.F0
                W0 = wtil(M, th.pi[0])
                W1 = wtil(M, th.pi[1])
                K = (W0 == W1)
                dp0 = [32 * sum(W0[c][(c & ~mc) | vc] for c in range(4))
                       for (mc, vc) in sc]
                dp1 = [32 * sum(W1[c][(c & ~mc) | vc] for c in range(4))
                       for (mc, vc) in sc]
                if dp0 != d0 or dp1 != d1:
                    formula_falhas += 1
                Wb = w_base(M)
                isos = grupo_iso(Wb)
                if (tau in [tuple(p) for p in isos]) != K:
                    iso_vs_K_mismatch += 1
                if len(isos) > 1 and not K:
                    w_sym_sem_K[nome] += 1
                eL1 = (nv == "L1")
                c = conf[nome]
                if K and eL1:
                    c["TP"] += 1
                elif K and not eL1:
                    c["FP"] += 1
                elif (not K) and eL1:
                    c["FN"] += 1
                else:
                    c["TN"] += 1
                if nome == "C_AB->B":
                    reg["K_B"] += int(K)
                    reg["L1_B"] += int(eL1)
                    if eL1:
                        L1_B += 1
                else:
                    reg["K_A"] += int(K)
                    reg["L1_A"] += int(eL1)
                    if eL1:
                        L1_A += 1
                chave_t = (nome, tau)
                slot = tau_exemplos.setdefault(chave_t, {"L1": None, "L3": None})
                if nv == "L1" and slot["L1"] is None:
                    slot["L1"] = (seed, tent)
                if nv == "L3" and slot["L3"] is None:
                    slot["L3"] = (seed, tent)
                if eL1 and len(exemplos_L1) < 60:
                    exemplos_L1.append({"seed": seed, "tentativa": tent,
                                        "aresta": nome, "tau": list(tau),
                                        "classe_tau": cls, "dep": dep})
            n_l1 = sum(1 for v in niveis if v == "L1")
            if n_l1 == 2:
                both_L1 += 1
            n_l3 = sum(1 for v in niveis if v == "L3")
            classe_i = {2: "individua_ambas", 1: "individua_uma",
                        0: "colapso_total"}[n_l3]
            niveis_inst[classe_i] += 1

    # controlos emparelhados: mesmo tau exacto, um L1 e um L3
    for (nome, tau), slot in tau_exemplos.items():
        if slot["L1"] and slot["L3"] and len(exemplos_ctrl) < 20:
            exemplos_ctrl.append({"aresta": nome, "tau": list(tau),
                                  "L1_em": slot["L1"], "L3_em": slot["L3"]})

    # métricas
    def metricas(c):
        tp, fp, tn, fn = c["TP"], c["FP"], c["TN"], c["FN"]
        return {"TP": tp, "FP": fp, "TN": tn, "FN": fn,
                "sensibilidade": tp / (tp + fn) if tp + fn else None,
                "especificidade": tn / (tn + fp) if tn + fp else None,
                "precisao": tp / (tp + fp) if tp + fp else None}

    # correlação entre arestas via tau partilhado
    pB = L1_B / n_fam
    pA = L1_A / n_fam
    pred_indep = pA * pB
    pred_tau = sum(r["n"] / n_fam * (r["K_B"] / r["n"]) * (r["K_A"] / r["n"])
                   for r in por_classe.values())
    obs_both = both_L1 / n_fam

    out = {
        "rotulo": "POST-CONFIRMATORY / EXPLORATORY",
        "condicao_K": "Wtil_0 == Wtil_1  <=>  tau = pi1 o pi0^-1 e isometria de W_M",
        "teorema_previsto": "K <=> L1 (necessidade: sistema linear das 9 intervencoes so tem Delta=0)",
        "seeds": SEEDS, "n_por_seed": N_POR_SEED, "familias": n_fam,
        "verificacao_formula_d": {"falhas": formula_falhas,
                                  "total_arestas": 2 * n_fam},
        "equivalencia_iso_vs_K": {"mismatches": iso_vs_K_mismatch},
        "confusao_K_vs_L1": {k: metricas(v) for k, v in conf.items()},
        "W_com_simetria_mas_K_falso_(edge)": w_sym_sem_K,
        "por_classe_de_tau": {k: {"n": v["n"],
                                  "P_K_B": round(v["K_B"] / v["n"], 5),
                                  "P_K_A": round(v["K_A"] / v["n"], 5),
                                  "P_L1_B": round(v["L1_B"] / v["n"], 5),
                                  "P_L1_A": round(v["L1_A"] / v["n"], 5)}
                              for k, v in sorted(por_classe.items())},
        "correlacao_entre_arestas": {
            "P_L1_aresta_B": round(pB, 6), "P_L1_aresta_A": round(pA, 6),
            "obs_ambas_L1": both_L1, "obs_P_ambas": round(obs_both, 6),
            "pred_independencia": round(pred_indep, 6),
            "pred_modelo_tau_partilhado": round(pred_tau, 6),
            "razao_obs_sobre_indep": round(obs_both / pred_indep, 2)
            if pred_indep else None,
            "razao_pred_tau_sobre_indep": round(pred_tau / pred_indep, 2)
            if pred_indep else None},
        "instancias": niveis_inst,
        "controlos_emparelhados_mesmo_tau": exemplos_ctrl,
        "exemplos_L1": exemplos_L1,
        "fam20": fam20_check() if INCLUI_FAM20 else None,
        "duracao_s": round(time.time() - t0, 1),
    }
    corpo = json.dumps(out, sort_keys=True, indent=1).encode()
    open(SAIDA, "wb").write(corpo)

    print("familias:", n_fam, " duracao: %.1fs" % out["duracao_s"])
    print("verificacao da formula d (exacta):",
          "OK em todas" if formula_falhas == 0 else "FALHOU em %d" % formula_falhas)
    print("equivalencia (tau in Iso(W)) == K :",
          "OK em todas" if iso_vs_K_mismatch == 0 else "%d mismatches" % iso_vs_K_mismatch)
    for k, v in out["confusao_K_vs_L1"].items():
        print("confusao", k, v)
    print("W simetrico mas K falso (por aresta):", w_sym_sem_K)
    print("classes de tau:", json.dumps(out["por_classe_de_tau"], indent=1))
    print("correlacao:", json.dumps(out["correlacao_entre_arestas"], indent=1))
    print("instancias:", niveis_inst)
    if INCLUI_FAM20:
        f20 = out["fam20"]
        for a, r in f20.items():
            print("fam20", a, "phi_bem_definida=", r["phi_bem_definida"],
                  "K=", r["K"])
            print("   Wtil_m0=", r["Wtil_m0"])
            print("   Wtil_m1=", r["Wtil_m1"])
    print("saida:", SAIDA)
    print("sha256_saida:", hashlib.sha256(corpo).hexdigest())
    try:
        print("sha256_script:",
              hashlib.sha256(open(__file__, "rb").read()).hexdigest())
    except Exception:
        pass


if __name__ == "__main__":
    main()

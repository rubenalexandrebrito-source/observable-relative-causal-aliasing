# -*- coding: utf-8 -*-
"""
POST-CONFIRMATORY / EXPLORATORY — WS1 (álgebra do L1), script s14 (pós-firewall).
Tentativa ACTIVA de refutação da conclusão prévia (condicao_L1.py: K ⟺ L1 com
K = [Wtil_0==Wtil_1] ⟺ [τ=π1π0⁻¹ ∈ Iso(W)]) e da minha própria (K ⟺ (a)∧(b)∧(c)
sobre agregados). Três frentes, TODAS determinísticas (sem sementes novas):

 (1) EQUIVALÊNCIA FORMAL: prova simbólica (posto/determinante inteiro) de que o
     sistema {somas-linha de Δ nulas; Δ01+Δ23=0; Δ02+Δ13=0} tem núcleo {0} no
     espaço 6-dim das matrizes simétricas de diagonal nula ⟹ os meus agregados
     (a,b,c) ⟺ Δ=0 entrada a entrada (a condição prévia). Se o posto fosse <6,
     as duas condições NÃO seriam equivalentes e haveria espaço para
     contra-exemplos entre elas.
 (2) VARRIMENTO DE CASOS-CANTO CONSTRUÍDOS (aresta C_BA→A, n=10 canónico):
     tabelas F0 desenhadas para degenerescências extremas (constantes, sem
     dependência do canal, colunas iguais, latinas, esparsas com zeros, perfis
     de empate) × todos os 23 ρ (π0=id) × 2 σA. Para cada instância: nível pela
     maquinaria congelada vs K_prev (Δ=0) vs K_mine (a∧b∧c) vs fórmula compacta
     prévia dp=32·Σ_c Wtil[c][sub(c)]. Qualquer divergência = contra-exemplo.
 (3) BUSCA DIRIGIDA de K∧¬L1 e ¬K∧L1 no material já existente: reutiliza o
     resultado s12/s13 (30000 arestas, 0 excepções) e regista-o como busca
     falhada de contra-exemplos.
Escreve apenas em ws1-algebra-l1/.
"""
import sys, json, hashlib, itertools
import numpy as np

DST = "/root/causal-A-postconfirmatory-analysis"
WS = DST + "/multiagent/ws1-algebra-l1"
sys.path.insert(0, DST + "/frozen-copy")
import gerador as g
import classificador as cl
from gerador import Theta

PC2 = [bin(v).count("1") for v in range(8)]
ORD_PARES = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]


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
        nivel = "L1"
    elif cl.rank_canonico(d0) == cl.rank_canonico(d1):
        nivel = "L2"
    else:
        nivel = "L3"
    return nivel, d0, d1, dep


def frente1_posto():
    # linhas: (a); (b); R0..R3 — colunas na ordem ORD_PARES
    linhas = []
    linhas.append([1 if p == (0, 1) or p == (2, 3) else 0 for p in ORD_PARES])
    linhas.append([1 if p == (0, 2) or p == (1, 3) else 0 for p in ORD_PARES])
    for r in range(4):
        linhas.append([1 if r in p else 0 for p in ORD_PARES])
    A = np.array(linhas, dtype=np.int64)
    # determinante inteiro por eliminação sem fracções (Bareiss)
    M = A.astype(object).copy()
    det = 1
    nn = 6
    prev = 1
    for k in range(nn - 1):
        if M[k][k] == 0:
            swap = next((i for i in range(k + 1, nn) if M[i][k] != 0), None)
            if swap is None:
                det = 0
                break
            M[[k, swap]] = M[[swap, k]]
            det = -det
        for i in range(k + 1, nn):
            for j in range(k + 1, nn):
                M[i][j] = (M[i][j] * M[k][k] - M[i][k] * M[k][j]) // prev
            M[i][k] = 0
        prev = M[k][k]
    if det != 0:
        det = det * M[nn - 1][nn - 1]
    posto = int(np.linalg.matrix_rank(A.astype(float)))
    return {"matriz": A.tolist(), "det_Bareiss": int(det), "posto": posto,
            "nucleo_trivial": det != 0}


F_LIST = {
    "constante0":      [[0, 0, 0, 0]] * 4,
    "so_x":            [[x, x, x, x] for x in range(4)],
    "so_u":            [[0, 1, 2, 3]] * 4,
    "xor":             [[x ^ u for u in range(4)] for x in range(4)],
    "soma_mod4":       [[(x + u) % 4 for u in range(4)] for x in range(4)],
    "colunas_01_iguais": [[0, 0, 1, 2], [1, 1, 0, 3], [2, 2, 3, 0], [3, 3, 2, 1]],
    "esparsa_zeros":   [[3, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
    "latina_2":        [[(2 * x + u) % 4 for u in range(4)] for x in range(4)],
    "perfil_empate":   [[0, 3, 1, 2], [3, 0, 2, 1], [0, 3, 2, 1], [3, 0, 1, 2]],
}
SIGMAS = [(0, 0), (1, 2)]
G0_FIX = [[1, 0, 3, 2], [2, 3, 0, 1], [0, 1, 2, 3], [3, 2, 1, 0]]
H_FIX = [[0, 1, 0, 1], [1, 0, 1, 0]]
K_FIX = [[1, 0, 0, 1], [0, 1, 1, 0]]


def frente2_cantos():
    id4 = list(range(4))
    perms = [list(p) for p in itertools.permutations(range(4)) if list(p) != id4]
    tot, err = 0, []
    niveis = {"L1": 0, "L2": 0, "L3": 0}
    zeros_W = 0
    for fname, F0 in F_LIST.items():
        for rho in perms:
            for sA in SIGMAS:
                th = Theta(F0=[row[:] for row in F0], G0=G0_FIX,
                           H=H_FIX, K=K_FIX,
                           sigmaA=list(sA), sigmaB=[0, 1],
                           pi=[id4[:], rho[:]],
                           x0=0, mA0=0, y0=0, mB0=0, cAB0=0, cBA0=0)
                tab, n, lay = g.tabela_transicao("II", th, False)
                T = np.asarray(tab, dtype=np.int64)
                nivel, d0, d1, dep = analisa_aresta(T, n, [8, 9], [0, 1, 2], [2])
                # pesos no contexto 0 e 1 (Wtil da análise prévia)
                def wt(perm):
                    # sigma cancela em todos os XOR de pares; omiti-lo é exacto
                    return [[sum(PC2[F0[x][perm[a]] ^ F0[x][perm[b]]]
                                 for x in range(4)) for b in range(4)]
                            for a in range(4)]
                W0 = wt(id4)
                W1 = wt(rho)
                K_prev = W0 == W1
                A0 = W0[0][1] + W0[2][3]
                B0 = W0[0][2] + W0[1][3]
                V0 = [sum(W0[w][c] for c in range(4)) for w in range(4)]
                A1 = W1[0][1] + W1[2][3]
                B1 = W1[0][2] + W1[1][3]
                V1 = [sum(W1[w][c] for c in range(4)) for w in range(4)]
                K_mine = (A0 == A1) and (B0 == B1) and (V0 == V1)
                # fórmula compacta prévia dp = 32*sum_c Wtil[c][sub(c)]
                ints = cl.intervencoes([8, 9])
                ok_dp = True
                for (mk, vl), dd0, dd1 in zip(ints, d0, d1):
                    mc = ((mk >> 8) & 1) | (((mk >> 9) & 1) << 1)
                    vc = ((vl >> 8) & 1) | (((vl >> 9) & 1) << 1)
                    dp0 = 32 * sum(W0[c][(c & ~mc) | vc] for c in range(4))
                    dp1 = 32 * sum(W1[c][(c & ~mc) | vc] for c in range(4))
                    if dp0 != dd0 or dp1 != dd1:
                        ok_dp = False
                tot += 1
                niveis[nivel] += 1
                if all(all(v == 0 for v in row) for row in W0):
                    zeros_W += 1
                casos = {"K_prev==K_mine": K_prev == K_mine,
                         "K_prev==L1": K_prev == (nivel == "L1"),
                         "K_mine==L1": K_mine == (nivel == "L1"),
                         "formula_prev_ok": ok_dp}
                if not all(casos.values()):
                    err.append({"F0": fname, "rho": rho, "sigmaA": list(sA),
                                "nivel": nivel, "K_prev": K_prev,
                                "K_mine": K_mine, "casos": casos,
                                "d0": d0, "d1": d1})
    return {"instancias_construidas": tot, "niveis": niveis,
            "W_nulo": zeros_W, "contra_exemplos": err}


def main():
    f1 = frente1_posto()
    f2 = frente2_cantos()
    out = {"rotulo": "POST-CONFIRMATORY / EXPLORATORY",
           "script": "s14_refutacao.py (pos-firewall)",
           "frente1_equivalencia_formal": f1,
           "frente2_cantos_construidos": f2,
           "frente3_busca_em_30000_arestas": {
               "fonte": "out-s12.json (20000 in-sample) + out-s13.json (10000 OOS)",
               "K_e_nao_L1": 0, "L1_e_nao_K": 0,
               "nota": "0 excepcoes; busca de contra-exemplos falhou"}}
    corpo = json.dumps(out, sort_keys=True, indent=1).encode()
    open(WS + "/out-s14.json", "wb").write(corpo)
    print("=== s14 RESUMO (refutação activa) ===")
    print("frente1: posto=%d det=%d nucleo_trivial=%s"
          % (f1["posto"], f1["det_Bareiss"], f1["nucleo_trivial"]))
    print("frente2: %d instâncias construídas, níveis=%s, W_nulo=%d, contra-exemplos=%d"
          % (f2["instancias_construidas"], f2["niveis"], f2["W_nulo"],
             len(f2["contra_exemplos"])))
    if f2["contra_exemplos"]:
        print(json.dumps(f2["contra_exemplos"][:5], indent=1))
    print("sha256 out-s14.json:", hashlib.sha256(corpo).hexdigest())


if __name__ == "__main__":
    main()

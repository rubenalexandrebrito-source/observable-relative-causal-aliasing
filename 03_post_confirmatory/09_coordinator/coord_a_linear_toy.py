# -*- coding: utf-8 -*-
# POST-CONFIRMATORY / EXPLORATORY — coordenador Fase 6.
# coord_a_linear_toy.py: (i) auditoria da Direccao 2 (sistema linear das 9
# intervencoes; rank/det/unicidade; reconstrucao explicita; lattice empobrecido);
# (ii) verificacao por script do toy model minimo calculado a mao.
# Nao usa sementes; nao le nada fora de frozen-copy (nem sequer precisa dele).
import json, itertools
from fractions import Fraction

out = {"rotulo": "POST-CONFIRMATORY / EXPLORATORY", "script": "coord_a_linear_toy.py"}

# ---------- (i) Sistema linear: incognitas Delta = (e01,e02,e03,e12,e13,e23) ----------
# d0=d1 impoe (por componente do vector d):
#   comp 1-2:  e01+e23 = 0            (A)
#   comp 3-4:  e02+e13 = 0            (B)
#   comp 5+g:  soma-linha g de Delta = 0, g=0..3   (V0..V3)
# Matriz 6x6 nas incognitas [e01,e02,e03,e12,e13,e23]:
rows = {
 "A":  [1,0,0,0,0,1],
 "B":  [0,1,0,0,1,0],
 "V0": [1,1,1,0,0,0],
 "V1": [1,0,0,1,1,0],
 "V2": [0,1,0,1,0,1],
 "V3": [0,0,1,0,1,1],
}
M = [[Fraction(x) for x in rows[k]] for k in ["A","B","V0","V1","V2","V3"]]

def det_frac(A):
    A = [r[:] for r in A]; n = len(A); d = Fraction(1)
    for i in range(n):
        p = next((r for r in range(i,n) if A[r][i] != 0), None)
        if p is None: return Fraction(0)
        if p != i: A[i],A[p] = A[p],A[i]; d = -d
        d *= A[i][i]
        inv = 1/A[i][i]
        for r in range(i+1,n):
            f = A[r][i]*inv
            if f:
                for c in range(i,n): A[r][c] -= f*A[i][c]
    return d

def inv_frac(A):
    n = len(A); Aug = [r[:] + [Fraction(int(i==j)) for j in range(n)] for i,r in enumerate(A)]
    for i in range(n):
        p = next(r for r in range(i,n) if Aug[r][i] != 0)
        Aug[i],Aug[p] = Aug[p],Aug[i]
        piv = Aug[i][i]
        Aug[i] = [x/piv for x in Aug[i]]
        for r in range(n):
            if r != i and Aug[r][i]:
                f = Aug[r][i]
                Aug[r] = [x - f*y for x,y in zip(Aug[r],Aug[i])]
    return [r[n:] for r in Aug]

D = det_frac(M)
out["sistema_completo"] = {"det": str(D), "rank": 6 if D != 0 else "<6",
                           "conclusao": "nucleo trivial => d0=d1 força Delta=0 entrada a entrada"}
Minv = inv_frac(M)
out["reconstrucao_Wtil_de_(A,B,V0..V3)"] = {
    "colunas_entrada": ["A","B","V0","V1","V2","V3"],
    "linhas_saida": ["e01","e02","e03","e12","e13","e23"],
    "matriz_inversa": [[str(x) for x in r] for r in Minv]}
# verificacao da reconstrucao em 200 Wtil inteiros pseudo-arbitrarios (deterministico, sem RNG)
ok_rec = 0
for t in range(200):
    e = [((t*7+3*i*i+11) % 9) for i in range(6)]  # e01,e02,e03,e12,e13,e23 em 0..8
    A_ = e[0]+e[5]; B_ = e[1]+e[4]
    V = [e[0]+e[1]+e[2], e[0]+e[3]+e[4], e[1]+e[3]+e[5], e[2]+e[4]+e[5]]
    rhs = [Fraction(x) for x in [A_,B_]+V]
    sol = [sum(Minv[i][j]*rhs[j] for j in range(6)) for i in range(6)]
    if all(sol[i] == e[i] for i in range(6)): ok_rec += 1
out["reconstrucao_verificada"] = f"{ok_rec}/200"

# lattice empobrecido: apenas bits isolados (sem do(c=g)) -> equacoes A,B
M2 = [[Fraction(x) for x in rows[k]] for k in ["A","B"]]
# rank de M2
def rank_frac(A):
    A = [r[:] for r in A]; n = len(A); m = len(A[0]); rk = 0
    for c in range(m):
        p = next((r for r in range(rk,n) if A[r][c] != 0), None)
        if p is None: continue
        A[rk],A[p] = A[p],A[rk]
        piv = A[rk][c]
        for r in range(n):
            if r != rk and A[r][c]:
                f = A[r][c]/piv
                A[r] = [x - f*y for x,y in zip(A[r],A[rk])]
        rk += 1
    return rk
out["lattice_empobrecido"] = {
    "equacoes": ["e01+e23=0","e02+e13=0"], "rank": rank_frac(M2), "dim_nucleo": 6-rank_frac(M2),
    "base_nucleo_exemplos": [[1,0,0,0,0,-1],[0,1,0,0,-1,0],[0,0,1,0,0,0],[0,0,0,1,0,0]],
    "conclusao": "sem as 4 intervencoes do(c=g), a reciproca (cegueira=>isometria) FALHA (nucleo nao trivial)"}

# lattice so-do(c=g): equacoes V0..V3 -> rank?
M3 = [[Fraction(x) for x in rows[k]] for k in ["V0","V1","V2","V3"]]
out["lattice_so_full"] = {"rank": rank_frac(M3), "dim_nucleo": 6-rank_frac(M3)}

# ---------- (ii) Toy model minimo (verificacao das contas manuais) ----------
# M: 2 linhas (r=0,1), 3 simbolos; saida 1 bit. M[0]=(0,0,1); M[1]=(0,1,0).
Mt = [[0,0,1],[0,1,0]]
Wt = [[sum(abs(Mt[r][p]-Mt[r][q]) for r in range(2)) for q in range(3)] for p in range(3)]
iso = []
for perm in itertools.permutations(range(3)):
    if all(Wt[perm[p]][perm[q]] == Wt[p][q] for p in range(3) for q in range(3)):
        iso.append(perm)
tau = (0,2,1)  # (12)
pi0 = (0,1,2); pi1 = tau
X = {}
for m,pi in ((0,pi0),(1,pi1)):
    for v in range(3):
        for c in range(3):
            X[(m,v,c)] = tuple(Mt[r][pi[v]] ^ Mt[r][pi[c]] for r in range(2))
dif = [(v,c) for v in range(3) for c in range(3) if X[(0,v,c)] != X[(1,v,c)]]
d0 = [sum(sum(X[(0,v,c)]) for c in range(3)) for v in range(3)]
d1 = [sum(sum(X[(1,v,c)]) for c in range(3)) for v in range(3)]
# celulas: igualdade dos totais por celula (v,c) sob isometria
cel_eq = all(sum(X[(0,v,c)]) == sum(X[(1,v,c)]) for v in range(3) for c in range(3))
out["toy"] = {
 "M": Mt, "W": Wt, "Iso(W)": [list(p) for p in iso], "tau": list(tau),
 "pi0": list(pi0), "pi1": list(pi1),
 "campos_X0": {f"v{v}c{c}": list(X[(0,v,c)]) for v in range(3) for c in range(3)},
 "campos_X1": {f"v{v}c{c}": list(X[(1,v,c)]) for v in range(3) for c in range(3)},
 "celulas_ponto_a_ponto_diferentes": [list(x) for x in dif],
 "n_sitios_linha_diferentes": sum(sum(1 for r in range(2) if X[(0,v,c)][r] != X[(1,v,c)][r]) for v,c in dif),
 "d0": d0, "d1": d1, "d0==d1": d0 == d1,
 "totais_por_celula_iguais": cel_eq,
 "conclusao": "X0!=X1 em 4/9 celulas (8/18 sitios-linha) e mesmo assim d0==d1; a perda e a LOCALIZACAO r (troca de linha que responde)"}

print(json.dumps(out, indent=1, ensure_ascii=False))

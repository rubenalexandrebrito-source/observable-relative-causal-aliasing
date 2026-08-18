# -*- coding: utf-8 -*-
# POST-CONFIRMATORY / EXPLORATORY - WS5 sanity check (precommit-ws5-taucheck.txt)
import sys, json, math, itertools, hashlib
import numpy as np
DST = "/root/causal-A-postconfirmatory-analysis"
sys.path.insert(0, DST + "/frozen-copy")
import gerador as g

MATCHINGS = [frozenset([frozenset([0,1]),frozenset([2,3])]),
             frozenset([frozenset([0,2]),frozenset([1,3])]),
             frozenset([frozenset([0,3]),frozenset([1,2])])]
def compoe(a,b): return tuple(a[b[c]] for c in range(4))
def inverte(p):
    inv=[0]*4
    for c,v in enumerate(p): inv[v]=c
    return tuple(inv)
def cycle_type(p):
    seen=[False]*4; t=[]
    for i in range(4):
        if not seen[i]:
            l,j=0,i
            while not seen[j]: seen[j]=True; j=p[j]; l+=1
            t.append(l)
    return tuple(sorted(t))
def perm_matching(p,mi):
    return frozenset(frozenset(p[v] for v in b) for b in MATCHINGS[mi])
def matching_de_dt(t):
    return frozenset(frozenset([a,t[a]]) for a in range(4))
def celula(tau,lam):
    ct=cycle_type(tau)
    if ct==(1,1,2):
        ab=frozenset(a for a in range(4) if tau[a]!=a)
        return "T_in" if ab in lam else "T_out"
    if ct==(2,2):
        return "DT_lam" if matching_de_dt(tau)==lam else "DT_oth"
    if ct==(4,):
        return "FC_lam" if matching_de_dt(compoe(tau,tau))==lam else "FC_oth"
    return "C3"

ss = np.random.SeedSequence(910000032)
rng = np.random.Generator(np.random.PCG64(ss.spawn(4)[0]))
N = 200000
cnt_cl = {}
cnt_cell = {}
n = 0
while n < N:
    th = g.sample_theta_base(rng)
    if th.pi[0] == th.pi[1]:
        continue
    n += 1
    pi0, pi1 = tuple(th.pi[0]), tuple(th.pi[1])
    tau = compoe(pi1, inverte(pi0))
    ct = str(cycle_type(tau))
    cnt_cl[ct] = cnt_cl.get(ct, 0) + 1
    cell = celula(tau, perm_matching(pi0, 2))
    cnt_cell[cell] = cnt_cell.get(cell, 0) + 1
esp = {"(1, 1, 2)": 6/23, "(1, 3)": 8/23, "(2, 2)": 3/23, "(4,)": 6/23}
out = {"rotulo": "POST-CONFIRMATORY / EXPLORATORY", "semente": 910000032,
       "N": N, "classes": cnt_cl, "celulas": cnt_cell, "z": {}}
for k, p in esp.items():
    e = N * p
    out["z"][k] = round((cnt_cl.get(k, 0) - e) / math.sqrt(N * p * (1 - p)), 3)
corpo = json.dumps(out, sort_keys=True, indent=1).encode()
open(DST + "/multiagent/ws5-failure-structure/ws5-taucheck.json", "wb").write(corpo)
print(json.dumps(out, sort_keys=True, indent=1))
print("sha256:", hashlib.sha256(corpo).hexdigest())

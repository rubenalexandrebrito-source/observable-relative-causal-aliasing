# POST-CONFIRMATORY / EXPLORATORY
# Autopsia da instancia 7bb0baab3a8ed7aa (E2, variante II) - reconstrucao factual.
# Le (NAO modifica) copias dos artefactos confirmatorios; usa o instrumento CONGELADO.
# NAO altera C1'/C2/C3 nem qualquer criterio. NAO recalcula o resultado confirmatorio.
import sys, json
DST = "/root/causal-A-postconfirmatory-analysis"
sys.path.insert(0, DST + "/frozen-copy")
import classificador as cl
import pontuacao as pt

ID = "7bb0baab3a8ed7aa"
chave = json.load(open(DST + "/chave-e2.json"))
inst = json.load(open(DST + "/conf-e2/instancias/%s.json" % ID))
escala = json.load(open(DST + "/escala-e2.json"))
equiv = json.load(open(DST + "/equiv-agregado.json"))

k = chave[ID]
tipos = pt._tipos_e2(k)                     # tipo canonico por indice de modulo


def types_of(listoflists):
    return sorted([sorted(tipos[m] for m in c) for c in listoflists])


print("=" * 72)
print("POST-CONFIRMATORY / EXPLORATORY  ---  autopsia", ID)
print("=" * 72)

print("\n[1] CHAVE")
print("  variante      :", k["variante"])
print("  familia       :", k["familia"])
print("  ordem_modulos :", k["ordem_modulos"])
print("  perm          :", k.get("perm"))
print("  theta_sha     :", k.get("theta_sha"))
print("  tipo por idx  :", list(enumerate(tipos)))

print("\n[2] INSTANCIA (parametros)")
print("  n             :", inst["n"], " |transicao| =", len(inst["transicao"]))
print("  estado_inicial:", inst["estado_inicial"])
for i, m in enumerate(inst["modulos"]):
    print("   idx %d %s bits=%s mem=%s  -> tipo %s"
          % (i, m["id"], m["bits"], m["bits_memoria"], tipos[i]))

res = cl.classificar(inst)
print("\n[3] CLASSIFICACAO (instrumento congelado)")
print("  |orbita|      :", res["orbita"])
print("  E_C (tipos)   :", sorted([(tipos[a], tipos[b]) for (a, b) in res["E_C"]]))
print("  arestas (tipo->tipo : C1p / C2 / C3):")
for kk, v in sorted(res["arestas"].items()):
    a, b = map(int, kk.split("->"))
    print("     %s->%s : C1p=%-6s C2=%-6s C3=%s"
          % (tipos[a], tipos[b], v["C1p"], v["C2"], v["C3"]))
for cand in ("C1p", "C2", "C3"):
    print("  %-3s componentes:" % cand, types_of(res[cand]["componentes"]))
    print("  %-3s meios      :" % cand, types_of(res[cand]["meios"]))

tc = pt.ALVOS_E2["II"]["comps"]
tm = pt.ALVOS_E2["II"]["meios"]
print("\n[4] ALVO (variante II, E2)")
print("  comps alvo    :", sorted([sorted(s) for s in tc]))
print("  meios alvo    :", sorted([sorted(s) for s in tm]))

print("\n[5] DIVERGENCIA C1p vs alvo (ESTE e o erro)")
cc = {frozenset(tipos[m] for m in c) for c in res["C1p"]["componentes"]}
mm = {frozenset(tipos[m] for m in c) for c in res["C1p"]["meios"]}
print("  componentes: match =", cc == tc)
print("     a MAIS  (no C1p, fora do alvo):", sorted([sorted(s) for s in cc - tc]))
print("     em FALTA(no alvo, fora do C1p):", sorted([sorted(s) for s in tc - cc]))
print("  meios      : match =", mm == tm)
print("     a MAIS  :", sorted([sorted(s) for s in mm - tm]))
print("     em FALTA:", sorted([sorted(s) for s in tm - mm]))
print("  => C1p PASSA nesta instancia:", (cc == tc and mm == tm))

print("\n[6] C2 e C3 nesta instancia (vs alvo II)")
for cand in ("C2", "C3"):
    c2 = {frozenset(tipos[m] for m in c) for c in res[cand]["componentes"]}
    m2 = {frozenset(tipos[m] for m in c) for c in res[cand]["meios"]}
    print("  %s: comps_match=%s meios_match=%s passa=%s"
          % (cand, c2 == tc, m2 == tm, (c2 == tc and m2 == tm)))
    print("     comps:", types_of(res[cand]["componentes"]))
    print("     meios:", types_of(res[cand]["meios"]))

print("\n[7] ESCALA desta instancia (E2)")
e = escala.get(ID, {})
print("  n_admissiveis :", e.get("n_admissiveis"),
      " granularidades:", e.get("granularidades_admissiveis"),
      " validade_6_4:", e.get("validade_6_4"))
print("  falhas por cand:", {c: e.get("falhas", {}).get(c) for c in ("C1p", "C2", "C3")})

print("\n[8] EQUIVALENCIAS desta instancia")
q = equiv.get(ID, {})
print("  grupo_total=%s testados=%s discrepancias=%s base=%s"
      % (q.get("grupo_total"), q.get("testados"),
         q.get("discrepancias"), q.get("discrepancias_base")))

print("\n[9] VARIANTE III da MESMA familia (familia %s)" % k["familia"])
fam = k["familia"]
irmas = [(i, chave[i]["variante"]) for i in chave if chave[i]["familia"] == fam]
print("  ids da familia:", sorted(irmas, key=lambda x: x[1]))
for i, var in irmas:
    if var == "III":
        i3 = json.load(open(DST + "/conf-e2/instancias/%s.json" % i))
        r3 = cl.classificar(i3)
        t3 = pt._tipos_e2(chave[i])
        c3 = {frozenset(t3[m] for m in c) for c in r3["C1p"]["componentes"]}
        m3 = {frozenset(t3[m] for m in c) for c in r3["C1p"]["meios"]}
        a3c, a3m = pt.ALVOS_E2["III"]["comps"], pt.ALVOS_E2["III"]["meios"]
        print("  III id:", i)
        print("    C1p comps:", sorted([sorted(t3[m] for m in c)
                                        for c in r3["C1p"]["componentes"]]))
        print("    C1p meios:", sorted([sorted(t3[m] for m in c)
                                        for c in r3["C1p"]["meios"]]))
        print("    III passa C1p:", (c3 == a3c and m3 == a3m))
print("\n[fim reconstrucao factual]")

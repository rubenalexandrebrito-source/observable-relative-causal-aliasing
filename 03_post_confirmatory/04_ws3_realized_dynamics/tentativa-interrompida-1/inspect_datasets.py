# POST-CONFIRMATORY / EXPLORATORY — WS3 inspeção READ-ONLY de datasets (nada é escrito)
import json, sys

DST = "/root/causal-A-postconfirmatory-analysis"

for lote, path in (("lote1", DST + "/prevalencia/prevalencia-cancelamento-II.json"),
                   ("lote2", DST + "/prevalencia/prevalencia-cancelamento-II-lote2.json")):
    d = json.load(open(path))
    ex = d["exemplos"]
    print("=== %s  seed=%s  aceites=%s tentativas=%s" % (
        lote, d.get("semente_exploratoria"), d.get("aceites_total_instancias"), d.get("tentativas")))
    for cls in ("colapso_total", "individua_uma", "individua_ambas"):
        rs = ex.get(cls, [])
        print("  %s: n=%d" % (cls, len(rs)))
        for r in rs[:3]:
            print("    fam=%s tent=%s sha=%s.. niveis=%s" % (
                r["fam"], r["tentativa"], r["theta_sha"][:12],
                {k: v["nivel"] for k, v in r["arestas"].items()}))
        if rs:
            print("    tentativas: min=%d max=%d" % (min(r["tentativa"] for r in rs),
                                                     max(r["tentativa"] for r in rs)))
    if "fam20_confirmatoria_referencia" in d:
        print("  fam20 ref:", {k: (v["nivel"], v["dep_sites"]) for k, v in d["fam20_confirmatoria_referencia"].items()})

print()
comb = json.load(open(DST + "/prevalencia/prevalencia-combinada-N10000.json"))
print("=== combinada:", json.dumps(comb, sort_keys=True)[:900])

print()
chave = json.load(open(DST + "/chave-e2.json"))
ID = "7bb0baab3a8ed7aa"
k = chave[ID]
print("=== chave-e2[%s]: variante=%s familia=%s ordem_modulos=%s theta_sha=%s" % (
    ID, k["variante"], k["familia"], k["ordem_modulos"], k["theta_sha"][:16]))
print("    perm=%s" % (k["perm"],))

inst = json.load(open(DST + "/conf-e2/instancias/%s.json" % ID))
print("=== instancia keys:", sorted(inst.keys()))
print("    n=%s estado_inicial=%s" % (inst["n"], inst["estado_inicial"]))
for i, m in enumerate(inst["modulos"]):
    print("    mod %d id=%s bits=%s mem=%s" % (i, m["id"], m["bits"], m["bits_memoria"]))

sys.path.insert(0, DST + "/frozen-copy")
import pontuacao as pt
print("    tipos_e2 =", pt._tipos_e2(k))

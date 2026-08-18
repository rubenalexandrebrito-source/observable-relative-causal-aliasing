# -*- coding: utf-8 -*-
"""Testes de pontuacao.py: positivo C1p, negativo, canário, integridade,
E2 inválido, equivalência incompleta, discrepância só de C2 não derrota C1p."""
import json, os, tempfile, unittest
import pontuacao as pt

def res_perfeito(var, c3_ab_estado=True):
    tipos = pt.CANON[var]
    idx = {t: i for i, t in enumerate(tipos)}
    if var == "I":
        arestas = {f"{idx['A']}->{idx['B']}": {}, f"{idx['B']}->{idx['A']}": {}}
        comps_c1 = [[idx["A"], idx["B"]]]; meios_c1 = comps_c1
    else:
        arestas = {f"{idx['A']}->{idx['C_AB']}": {},
                   f"{idx['C_AB']}->{idx['B']}": {},
                   f"{idx['B']}->{idx['C_BA']}": {},
                   f"{idx['C_BA']}->{idx['A']}": {}}
        if var == "II":
            comps_c1 = [[idx["A"]], [idx["B"]], [idx["C_AB"]], [idx["C_BA"]]]
            meios_c1 = [[idx["A"]], [idx["B"]]]
        else:
            comps_c1 = [[idx["A"], idx["B"], idx["C_AB"], idx["C_BA"]]]
            meios_c1 = comps_c1
    for k in arestas:
        arestas[k] = {"C1p": "sinal" if var == "II" and "C_" in "x" else "estado",
                      "C2": "estado", "C3": "estado"}
    if var == "II":
        arestas[f"{idx['C_AB']}->{idx['B']}"]["C1p"] = "sinal"
        arestas[f"{idx['C_BA']}->{idx['A']}"]["C1p"] = "sinal"
        if not c3_ab_estado:
            arestas[f"{idx['C_AB']}->{idx['B']}"]["C3"] = "sinal"
    # C2/C3: componente única (falham alvos de II, como no dev)
    todos = [[i for i in range(len(tipos))]]
    return {"arestas": arestas,
            "C1p": {"componentes": comps_c1, "meios": meios_c1},
            "C2": {"componentes": todos if var == "II" else comps_c1,
                    "meios": todos if var == "II" else meios_c1},
            "C3": {"componentes": todos if var == "II" else comps_c1,
                    "meios": todos if var == "II" else meios_c1}}

def micro_e2(var, errado=False, canario_mau=False):
    canon = ["A","B","C_AB","C_BA","D1","D2"]
    i = {t: k for k, t in enumerate(canon)}
    if var == "II":
        comps = [[i["A"]],[i["B"]],[i["C_AB"]],[i["C_BA"]],[i["D1"]],[i["D2"]]]
        meios = [[i["A"]],[i["B"]]]
    else:
        comps = [[i["A"],i["B"],i["C_AB"],i["C_BA"]],[i["D1"]],[i["D2"]]]
        meios = [[i["A"],i["B"],i["C_AB"],i["C_BA"]]]
    if errado:
        comps = [[j for j in range(6)]]     # tudo numa componente: ERRADO
        meios = [[j for j in range(6)]]
    arestas = {f"{i['A']}->{i['C_AB']}": {"C3": "estado"},
               f"{i['C_AB']}->{i['B']}": {"C3": "sinal" if canario_mau
                                           else "estado"},
               f"{i['B']}->{i['C_BA']}": {"C3": "estado"},
               f"{i['C_BA']}->{i['A']}": {"C3": "estado"}}
    out = {c: {"componentes": comps, "meios": meios}
           for c in ("C1p","C2","C3")}
    out["E_C"] = [[0, 2], [2, 1], [1, 3], [3, 0]]
    out["arestas"] = arestas
    return out


def fixtures(d, n1=(1,1,1), n2=(1,1), quebra=None):
    chave1, chave2, classif, escala1, escala, equiv = {}, {}, {}, {}, {}, {}
    c = 0
    for var, n in zip(("I","II","III"), n1):
        for _ in range(n):
            iid = f"e1-{c}"; c += 1
            chave1[iid] = {"variante": var,
                           "ordem_modulos": list(range(len(pt.CANON[var])))}
            classif[iid] = res_perfeito(var,
                c3_ab_estado=not (quebra=="canario" and var=="II"))
            escala1[iid] = {"n_admissiveis": 0, "validade_6_4": False,
                            "falhas": {"C1p": ["S"] if quebra=="escalaE1"
                                       else [], "C2": [], "C3": []}}
            equiv[iid] = {"grupo_total": 10, "testados": 10,
                          "discrepancias_base": 0,
                          "discrepancias": {"C1p":0,"C2":0,"C3":0}}
    for var, n in zip(("II","III"), n2):
        for _ in range(n):
            iid = f"e2-{c}"; c += 1
            chave2[iid] = {"variante": var, "ordem_modulos": list(range(6))}
            escala[iid] = {"validade_6_4": quebra != "e2invalido",
                           "micro": micro_e2(var,
                               errado=(quebra == "e2microerrado"),
                               canario_mau=(quebra == "canarioE2"
                                            and var == "II")),
                           "falhas": {"C1p": [], "C2": [], "C3": []}}
            equiv[iid] = {"grupo_total": 10,
                          "testados": 10 if quebra != "equivincompleta" else 3,
                          "discrepancias_base": 3 if quebra == "basegc" else 0,
                          "discrepancias": {"C1p":0,"C2":0,"C3":0}}
    if quebra == "faltainstancia":
        classif.pop(next(iter(classif)))
    if quebra == "c2equiv":
        k = next(iter(equiv))
        equiv[k]["discrepancias"]["C2"] = 4
    caminhos = {}
    for nome, obj in (("classif",classif),("escala1",escala1),
                      ("escala",escala),("equiv",equiv),
                      ("ch1",chave1),("ch2",chave2)):
        p = os.path.join(d, nome + ".json")
        json.dump(obj, open(p,"w")); caminhos[nome] = p
    return caminhos

ESP1 = {"I":1,"II":1,"III":1}; ESP2 = {"II":1,"III":1}
GRP = {("E1","I"):10, ("E1","II"):10, ("E1","III"):10,
       ("E2","II"):10, ("E2","III"):10}

def correr(d, quebra=None, grp=None):
    c = fixtures(d, quebra=quebra)
    return pt.pontuar(c["classif"], c["escala1"], c["escala"], c["equiv"],
                      c["ch1"], c["ch2"], ESP1, ESP2, grp or GRP)

class T(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp()
    def test_positivo_via_C1p(self):
        s = correr(self.d)
        self.assertEqual(s["resultado_confirmatorio_A"], "positivo")
        self.assertTrue(s["veredicto_por_candidata"]["C1p"]["passa"])
        self.assertFalse(s["veredicto_por_candidata"]["C2"]["passa"])
    def test_canario_anula(self):
        s = correr(self.d, "canario")
        self.assertEqual(s["resultado_confirmatorio_A"],
                         "ANULAR_EXECUCAO_CANARIO")
    def test_integridade_falta_instancia(self):
        s = correr(self.d, "faltainstancia")
        self.assertEqual(s["resultado_confirmatorio_A"],
                         "ANULAR_EXECUCAO_INTEGRIDADE")
    def test_e2_invalido_anula(self):
        s = correr(self.d, "e2invalido")
        self.assertEqual(s["resultado_confirmatorio_A"],
                         "ANULAR_EXECUCAO_ESTRATO2_INVALIDO")
    def test_equivalencia_incompleta_anula(self):
        s = correr(self.d, "equivincompleta")
        self.assertEqual(s["resultado_confirmatorio_A"],
                         "ANULAR_EXECUCAO_INTEGRIDADE")
    def test_grupo_total_inesperado_anula(self):
        grp = dict(GRP); grp[("E1","I")] = 999
        s = correr(self.d, grp=grp)
        self.assertEqual(s["resultado_confirmatorio_A"],
                         "ANULAR_EXECUCAO_INTEGRIDADE")

    def test_discrepancia_de_base_anula_nao_derrota(self):
        s = correr(self.d, "basegc")
        self.assertEqual(s["resultado_confirmatorio_A"],
                         "ANULAR_EXECUCAO_INTEGRIDADE")

    def test_falha_de_escala_no_E1_derrota_candidata(self):
        # 10.1(4) cobre TODAS as instâncias confirmatórias: uma projecção
        # admissível instável num sistema do Estrato 1 derrota a candidata.
        s = correr(self.d, "escalaE1")
        v = s["veredicto_por_candidata"]["C1p"]
        self.assertFalse(v["passa"])
        self.assertFalse(v["itens"]["escala"])
        # e a validade 6.4 do E1 a False NAO anula (só é exigida no E2):
        self.assertNotIn("ANULAR", s["resultado_confirmatorio_A"])

    def test_canario_no_E2_anula(self):
        s = correr(self.d, "canarioE2")
        self.assertEqual(s["resultado_confirmatorio_A"],
                         "ANULAR_EXECUCAO_CANARIO")

    def test_errado_mas_estavel_nao_passa(self):
        # O caso da auditoria: E1 perfeito, projecções estáveis,
        # equivalências limpas, MAS a partição micro do E2 está errada.
        # A estabilidade de uma resposta errada não pode contar como sucesso.
        s = correr(self.d, "e2microerrado")
        self.assertEqual(s["resultado_confirmatorio_A"], "negativo")
        for cand in ("C1p", "C2"):
            v = s["veredicto_por_candidata"][cand]
            self.assertFalse(v["passa"])
            self.assertFalse(v["itens"]["alvos_E2"])
            self.assertTrue(v["itens"]["escala"])      # estável, e errado

    def test_discrepancia_so_de_C2_nao_derrota_C1p(self):
        s = correr(self.d, "c2equiv")
        self.assertEqual(s["resultado_confirmatorio_A"], "positivo")
        self.assertFalse(s["veredicto_por_candidata"]["C2"]["itens"]["equivalencias"])
        self.assertTrue(s["veredicto_por_candidata"]["C1p"]["itens"]["equivalencias"])

if __name__ == "__main__":
    unittest.main(verbosity=1)

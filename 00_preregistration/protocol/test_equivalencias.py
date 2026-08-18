# -*- coding: utf-8 -*-
"""Testes de equivalencias.py: identidade, sabotagem de s0 detectada e
enumeração continua, discrepância por candidata, contagem completa em I."""
import unittest
import gerador as g
import equivalencias as eq

SEMENTE_DEV = 777000111

def instancias_dev():
    inst, chave, _, _ = g.gerar_lote(SEMENTE_DEV, 1, False)
    return {chave[i["id"]]["variante"]: i for i in inst}

class T(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.por_var = instancias_dev()

    def test_exaustivo_em_I_grupo_completo_sem_discrepancias(self):
        r = eq.testar_instancia(self.por_var["I"], amostra=None)
        self.assertEqual(r["testados"], r["grupo_total"])
        self.assertEqual(r["discrepancias"], {"C1p": 0, "C2": 0, "C3": 0})
        self.assertEqual(r["discrepancias_base"], 0)

    def test_identidade_nao_discrepa(self):
        inst = self.por_var["II"]
        n = inst["n"]
        import classificador as cl
        res = cl.classificar(inst)
        sigma = {i: i for i in range(len(inst["modulos"]))}
        p = list(range(n))
        inst2 = eq.transformar_instancia(inst, p, 0)
        res2 = cl.classificar(inst2)
        falhas = eq.comparar(res, res2, sigma)
        self.assertEqual(falhas, {"C1p": None, "C2": None, "C3": None})

    def test_s0_e_conjugado_propriedade_directa(self):
        # determinístico: o estado inicial transformado tem de ser phi(s0)
        inst = self.por_var["II"]
        n = inst["n"]
        p = list(reversed(range(n)))
        flips = 0b1010101010
        inst2 = eq.transformar_instancia(inst, p, flips)
        self.assertEqual(inst2["estado_inicial"],
                         eq.aplicar_phi(inst["estado_inicial"], p, flips, n))

    def test_sabotagem_s0_detectada_e_enumeracao_continua(self):
        # configuração detectora conhecida (dev): II, amostra 200, semente 0.
        # A sabotagem só é visível quando muda uma classificação; em I foi
        # invisível em 512/512, o que fica registado como limitação: o arnês
        # verifica invariância de RESULTADOS, não de órbitas.
        inst = self.por_var["II"]
        orig = eq.transformar_instancia
        def sab(i, p, f):
            out = orig(i, p, f)
            out["estado_inicial"] = i["estado_inicial"]
            return out
        eq.transformar_instancia = sab
        try:
            r = eq.testar_instancia(inst, amostra=200, semente_amostra=0)
        finally:
            eq.transformar_instancia = orig
        total = sum(r["discrepancias"].values()) + r["discrepancias_base"]
        self.assertGreater(total, 0)
        self.assertEqual(r["testados"], 200)     # sem break (P0.5)
        for c in ("C1p", "C2", "C3"):
            self.assertLessEqual(len(r["exemplos"][c]), 5)

    def test_discrepancia_de_EC_e_base_nao_candidata(self):
        res_o = {"E_C": [(0, 1)], "arestas": {"0->1": {"C1p": "estado",
                 "C2": "estado", "C3": "estado"}},
                 "C1p": {"componentes": [[0, 1]], "meios": [[0, 1]]},
                 "C2": {"componentes": [[0, 1]], "meios": [[0, 1]]},
                 "C3": {"componentes": [[0, 1]], "meios": [[0, 1]]}}
        import copy
        res_t = copy.deepcopy(res_o)
        res_t["E_C"] = [(1, 0)]
        self.assertEqual(eq.comparar(res_o, res_t, {0: 0, 1: 1}), "BASE")

    def test_amostra_sem_reposicao(self):
        inst = self.por_var["I"]
        r = eq.testar_instancia(inst, amostra=512, semente_amostra=5)
        self.assertEqual(r["testados"], 512)   # choice sem reposição cobre tudo

    def test_discrepancia_atribuida_por_candidata(self):
        # falha só nas componentes de C2: comparar deve isolar C2
        res_o = {"E_C": [(0, 1)], "arestas": {"0->1": {"C1p": "estado",
                 "C2": "estado", "C3": "estado"}},
                 "C1p": {"componentes": [[0, 1]], "meios": [[0, 1]]},
                 "C2": {"componentes": [[0, 1]], "meios": [[0, 1]]},
                 "C3": {"componentes": [[0, 1]], "meios": [[0, 1]]}}
        import copy
        res_t = copy.deepcopy(res_o)
        res_t["C2"]["componentes"] = [[0], [1]]
        falhas = eq.comparar(res_o, res_t, {0: 0, 1: 1})
        self.assertIsNone(falhas["C1p"])
        self.assertEqual(falhas["C2"], "componentes")
        self.assertIsNone(falhas["C3"])

class TAgregador(unittest.TestCase):
    def test_dois_directorios_uniao_deterministica(self):
        import tempfile, os, json
        d = tempfile.mkdtemp()
        d1, d2 = os.path.join(d, "a"), os.path.join(d, "b")
        os.makedirs(d1); os.makedirs(d2)
        inst, chave, _, _ = g.gerar_lote(777000111, 1, False)
        alvo = [i for i in inst if chave[i["id"]]["variante"] == "I"][0]
        json.dump(alvo, open(os.path.join(d1, "x.json"), "w"))
        alvo2 = dict(alvo); alvo2["id"] = "outro"
        json.dump(alvo2, open(os.path.join(d2, "y.json"), "w"))
        saida = os.path.join(d, "agg.json")
        sha1 = eq.correr_lote([d1, d2], saida, amostra=4, semente_amostra=1)
        agg = json.load(open(saida))
        self.assertEqual(set(agg), {alvo["id"], "outro"})
        os.remove(saida)
        sha2 = eq.correr_lote([d1, d2], saida, amostra=4, semente_amostra=1)
        self.assertEqual(sha1, sha2)

    def test_id_repetido_lanca_erro(self):
        import tempfile, os, json
        d = tempfile.mkdtemp()
        d1, d2 = os.path.join(d, "a"), os.path.join(d, "b")
        os.makedirs(d1); os.makedirs(d2)
        inst, chave, _, _ = g.gerar_lote(777000111, 1, False)
        alvo = [i for i in inst if chave[i["id"]]["variante"] == "I"][0]
        json.dump(alvo, open(os.path.join(d1, "x.json"), "w"))
        json.dump(alvo, open(os.path.join(d2, "y.json"), "w"))
        with self.assertRaises(ValueError):
            eq.correr_lote([d1, d2], os.path.join(d, "agg.json"), amostra=2)

    def test_selector_dryrun_deterministico(self):
        import dryrun
        ch1 = {f"i{k}": {"variante": v} for k, v in
               enumerate(["I"]*4 + ["II"]*4 + ["III"]*4)}
        ch2 = {f"j{k}": {"variante": v} for k, v in
               enumerate(["II"]*4 + ["III"]*4)}
        s1 = dryrun.seleccionar(ch1, ch2)
        s2 = dryrun.seleccionar(ch1, ch2)
        self.assertEqual(s1, s2)
        self.assertEqual(sorted(s1), ["E1:I", "E1:II", "E1:III",
                                      "E2:II", "E2:III"])
        for ids in s1.values():
            self.assertEqual(len(ids), 3)
            self.assertEqual(len(set(ids)), 3)


class TRunnerTemporal(unittest.TestCase):
    def test_cronometrar_devolve_os_cinco_grupos(self):
        import dryrun, tempfile, os, json
        d = tempfile.mkdtemp()
        d1, d2 = os.path.join(d, "e1"), os.path.join(d, "e2")
        os.makedirs(d1); os.makedirs(d2)
        inst1, ch1, _, _ = g.gerar_lote(777000210, 4, False)
        inst2, ch2, _, _ = g.gerar_lote(777000211, 4, True)
        for i in inst1:
            json.dump(i, open(os.path.join(d1, i["id"] + ".json"), "w"))
        for i in inst2:
            json.dump(i, open(os.path.join(d2, i["id"] + ".json"), "w"))
        sel = dryrun.seleccionar(ch1, ch2)
        r = dryrun.cronometrar(sel, d1, d2, amostra=2)   # fumo do runner
        self.assertEqual(sorted(r["t_por_grupo_segundos"]),
                         ["E1:I", "E1:II", "E1:III", "E2:II", "E2:III"])
        soma = (50/3) * sum(r["t_por_grupo_segundos"][k]
                            for k in ("E1:I", "E1:II", "E1:III")) \
             + (25/3) * sum(r["t_por_grupo_segundos"][k]
                            for k in ("E2:II", "E2:III"))
        self.assertAlmostEqual(r["T_equiv_estimado_horas"], soma / 3600.0)


class TRunnerRobustez(unittest.TestCase):
    def test_id_seleccionado_ausente_lanca_erro(self):
        # NÃO-VÁCUO: primeiro selecciona-se, depois remove-se precisamente
        # um ID que se SABE seleccionado; o ramo ValueError é sempre testado.
        import dryrun, tempfile, os, json
        d = tempfile.mkdtemp()
        d1, d2 = os.path.join(d, "e1"), os.path.join(d, "e2")
        os.makedirs(d1); os.makedirs(d2)
        inst1, ch1, _, _ = g.gerar_lote(777000210, 4, False)
        inst2, ch2, _, _ = g.gerar_lote(777000211, 4, True)
        for i in inst1:
            json.dump(i, open(os.path.join(d1, i["id"] + ".json"), "w"))
        for i in inst2:
            json.dump(i, open(os.path.join(d2, i["id"] + ".json"), "w"))
        sel = dryrun.seleccionar(ch1, ch2)
        removido = sel["E1:I"][0]                  # sabidamente seleccionado
        os.remove(os.path.join(d1, removido + ".json"))
        with self.assertRaises(ValueError):
            dryrun.cronometrar(sel, d1, d2, amostra=1)

    def test_indexacao_por_conteudo_nao_por_nome(self):
        import dryrun, tempfile, os, json
        d = tempfile.mkdtemp()
        d1, d2 = os.path.join(d, "e1"), os.path.join(d, "e2")
        os.makedirs(d1); os.makedirs(d2)
        inst1, ch1, _, _ = g.gerar_lote(777000210, 4, False)
        inst2, ch2, _, _ = g.gerar_lote(777000211, 4, True)
        for k, i in enumerate(inst1):
            json.dump(i, open(os.path.join(d1, f"renomeado-{k}.json"), "w"))
        for k, i in enumerate(inst2):
            json.dump(i, open(os.path.join(d2, f"outro-{k}.json"), "w"))
        sel = dryrun.seleccionar(ch1, ch2)
        r = dryrun.cronometrar(sel, d1, d2, amostra=1)   # nomes irrelevantes
        self.assertEqual(len(r["t_por_grupo_segundos"]), 5)


if __name__ == "__main__":
    unittest.main(verbosity=1)

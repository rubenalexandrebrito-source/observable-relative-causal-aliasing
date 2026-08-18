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


def fixture_resultado_sintetico(inst, amostra=None, semente_amostra=0):
    """Fixture SINTÉTICO e determinístico (NÃO científico) da camada de
    resultados: dado um 'inst' (só precisa de 'id'), devolve um resultado
    com discrepâncias NÃO-ZERO e testemunhos CONHECIDOS, função pura do id.

    Existe ao NÍVEL DO MÓDULO para ser picklable e correr em processos
    independentes, exactamente pela mesma primitiva da camada real
    (ProcessPoolExecutor + map + WORKERS_EQUIV). Serve para testar a
    semântica da paralelização/agregação — contagens, ordem dos
    testemunhos, JSON e SHA — sem depender de qualquer definição
    científica nem de testar_instancia()."""
    iid = inst["id"]
    s = sum(ord(c) for c in iid)          # inteiro determinístico do id (sem hash())
    n_c1 = (s % 3) + 1                     # 1..3: discrepância SEMPRE > 0
    n_c2 = (s // 3) % 2                    # 0 ou 1
    exemplos = {
        "C1p": [{"sigma": {0: 1, 1: 0}, "p": [1, 0], "flips": s % 4,
                 "tipo": "componentes", "id": iid}],
        "C2": ([{"sigma": {0: 0, 1: 1}, "p": [0, 1], "flips": (s + 1) % 4,
                 "tipo": "meios", "id": iid}] if n_c2 else []),
        "C3": [],
        "BASE": [],
    }
    return {"grupo_total": 100, "testados": 100,
            "discrepancias_base": 0,
            "discrepancias": {"C1p": n_c1, "C2": n_c2, "C3": 0},
            "exemplos": exemplos}


def worker_sintetico(args):
    """Worker de MÓDULO (picklable) injectado na camada batch: recebe o mesmo
    tuplo (inst, amostra, semente_amostra) do worker científico real e
    devolve o fixture sintético com discrepâncias/testemunhos conhecidos.
    Não usa testar_instancia() nem qualquer definição científica."""
    inst, amostra, semente_amostra = args
    return fixture_resultado_sintetico(inst, amostra, semente_amostra)


def worker_que_rebenta(args):
    """Worker de módulo (picklable) que levanta sempre. Usa uma excepção
    BUILTIN (RuntimeError) de propósito: uma classe própria definida no
    módulo principal duplica-se entre __main__/__mp_main__ sob forkserver e
    a identidade poderia não coincidir. Verifica que a excepção se propaga
    através da camada paralela, nunca é silenciada."""
    raise RuntimeError("falha deliberada no worker injectado")

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


class TParaleloAMD2(unittest.TestCase):
    """Pre-data Amendment No. 2: paralelização determinística ENTRE
    instâncias (WORKERS_EQUIV=3). Prova que o paralelo é byte-a-byte igual
    ao sequencial e que nada foi flexibilizado."""

    @classmethod
    def setUpClass(cls):
        cls.por_var = instancias_dev()

    def test_workers_fixo_em_tres(self):
        # número de workers CONGELADO; nunca dinâmico/os.cpu_count().
        self.assertEqual(eq.WORKERS_EQUIV, 3)

    def test_workers1_igual_workers3_estruturalmente(self):
        # varia max_workers => usa o NÚCLEO INTERNO (não a API de produção)
        insts = [self.por_var["I"], self.por_var["II"], self.por_var["III"]]
        r1 = eq._testar_instancias_em_lote_com_worker(
            insts, amostra=150, semente_amostra=0, max_workers=1)
        r3 = eq._testar_instancias_em_lote_com_worker(
            insts, amostra=150, semente_amostra=0, max_workers=3)
        self.assertEqual(r1, r3)
        # e ambos iguais à chamada sequencial directa, uma a uma
        seq = [eq.testar_instancia(i, amostra=150, semente_amostra=0)
               for i in insts]
        self.assertEqual(r3, seq)
        # e iguais à API de PRODUÇÃO (W=3 + worker real, sem parâmetros)
        self.assertEqual(eq.testar_instancias_em_lote(
            insts, amostra=150, semente_amostra=0), seq)

    def test_exaustivo_batch_testados_igual_grupo_total(self):
        # modo exaustivo (amostra=None) pela API de PRODUÇÃO: a enumeração
        # continua total, testados == grupo_total, sem break.
        r = eq.testar_instancias_em_lote([self.por_var["I"]], amostra=None)[0]
        self.assertEqual(r["testados"], r["grupo_total"])
        self.assertEqual(r["discrepancias"], {"C1p": 0, "C2": 0, "C3": 0})
        self.assertEqual(r["discrepancias_base"], 0)

    def test_paralelo_repetido_e_identico(self):
        # API de produção (W=3); repetir dá exactamente o mesmo
        insts = [self.por_var["II"], self.por_var["III"]]
        a = eq.testar_instancias_em_lote(insts, amostra=200, semente_amostra=0)
        b = eq.testar_instancias_em_lote(insts, amostra=200, semente_amostra=0)
        self.assertEqual(a, b)

    def test_ordem_de_entrada_preservada_nao_de_conclusao(self):
        # instâncias com grupos de tamanhos MUITO diferentes; o resultado
        # tem de vir na ordem de ENTRADA, não na de conclusão dos workers.
        insts = [self.por_var["III"], self.por_var["I"]]   # grupos 65536, 512
        r = eq.testar_instancias_em_lote(insts, amostra=1, semente_amostra=0)
        self.assertEqual(r[0]["grupo_total"], 65536)   # III veio em 1.º
        self.assertEqual(r[1]["grupo_total"], 512)     # I veio em 2.º

    def test_batch_sintetico_discrepancias_seq_igual_par(self):
        # Discrepância NÃO-ZERO + testemunhos: camada paralela testada por
        # INJECÇÃO de worker no NÚCLEO INTERNO (dependency injection), sem
        # monkeypatch e sem depender do start method. O worker sintético NÃO
        # é alcançável pela API de produção. Fixture determinístico.
        import json, hashlib
        insts = [{"id": iid} for iid in
                 ("0a11", "0b22", "0c33", "0d44", "0e55")]
        # referência SEQUENCIAL: chamadas directas ao worker de módulo
        seq = [worker_sintetico((i, None, 0)) for i in insts]
        # PARALELO (núcleo interno) com 1 e 3 workers, worker injectado
        par1 = eq._testar_instancias_em_lote_com_worker(
            insts, max_workers=1, worker=worker_sintetico)
        par3 = eq._testar_instancias_em_lote_com_worker(
            insts, max_workers=3, worker=worker_sintetico)
        # (a) workers=1 e workers=3 agregam EXACTAMENTE o mesmo
        self.assertEqual(par1, par3)
        # (b) ordem dos resultados = ordem de ENTRADA (id embebido), não de
        #     conclusão dos workers
        self.assertEqual([r["exemplos"]["C1p"][0]["id"] for r in par3],
                         [i["id"] for i in insts])
        # (c) contagens e testemunhos idênticos ao sequencial
        self.assertEqual(seq, par3)
        # discrepâncias deliberadamente NÃO-ZERO
        self.assertTrue(all(sum(r["discrepancias"].values()) > 0
                            for r in par3))
        # (d) JSON e SHA idênticos: agregação canónica (a mesma de correr_lote)
        #     sobre paralelo vs sequencial
        def agregar(ids, resultados):
            corpo = json.dumps({i: r for i, r in zip(ids, resultados)},
                               sort_keys=True, indent=1, default=str).encode()
            return corpo, hashlib.sha256(corpo).hexdigest()
        ids = [i["id"] for i in insts]
        corpo_par, sha_par = agregar(ids, par3)
        corpo_seq, sha_seq = agregar(ids, seq)
        self.assertEqual(corpo_par, corpo_seq)                 # JSON idêntico
        self.assertEqual(sha_par, sha_seq)                     # SHA idêntico

    def test_batch_sintetico_excepcao_worker_propaga(self):
        # uma excepção de worker injectado TEM de propagar pelo núcleo interno
        insts = [{"id": "x1"}, {"id": "x2"}, {"id": "x3"}]
        with self.assertRaises(RuntimeError):
            eq._testar_instancias_em_lote_com_worker(
                insts, max_workers=3, worker=worker_que_rebenta)

    def test_agregador_paralelo_igual_referencia_sequencial(self):
        # JSON e SHA do correr_lote (paralelo) == referência sequencial pura.
        import tempfile, os, json, hashlib
        d = tempfile.mkdtemp()
        dir_i = os.path.join(d, "in")
        os.makedirs(dir_i)
        inst, chave, _, _ = g.gerar_lote(777000111, 1, False)
        # dois sistemas independentes, IDs distintos, nomes que forçam ordem
        a0 = [i for i in inst if chave[i["id"]]["variante"] == "I"][0]
        a1 = [i for i in inst if chave[i["id"]]["variante"] == "III"][0]
        json.dump(a0, open(os.path.join(dir_i, "aaa.json"), "w"))
        json.dump(a1, open(os.path.join(dir_i, "bbb.json"), "w"))
        saida = os.path.join(d, "agg-par.json")
        sha_par = eq.correr_lote([dir_i], saida, amostra=120, semente_amostra=1)
        corpo_par = open(saida, "rb").read()
        # referência sequencial: mesma ordem de leitura, chamadas directas
        ids, results = [], []
        for f in sorted(os.listdir(dir_i)):
            if f.endswith(".json"):
                ii = json.load(open(os.path.join(dir_i, f)))
                ids.append(ii["id"])
                results.append(eq.testar_instancia(ii, amostra=120,
                                                   semente_amostra=1))
        ref = {iid: res for iid, res in zip(ids, results)}
        corpo_ref = json.dumps(ref, sort_keys=True, indent=1,
                               default=str).encode()
        sha_ref = hashlib.sha256(corpo_ref).hexdigest()
        self.assertEqual(corpo_par, corpo_ref)       # bytes idênticos
        self.assertEqual(sha_par, sha_ref)           # SHA idêntico

    def test_ids_repetidos_ainda_lancam_valueerror_no_paralelo(self):
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

    def test_excepcao_de_worker_nao_e_silenciada(self):
        # instância malformada => testar_instancia levanta; a excepção TEM
        # de propagar pela API de PRODUÇÃO (worker científico real), nunca
        # ser engolida.
        inst_mau = {"id": "mau", "n": 4}          # falta 'transicao'/'modulos'
        with self.assertRaises(Exception):
            eq.testar_instancias_em_lote([inst_mau], amostra=1)

    def test_selector_dryrun_regra_pcg64_intacta(self):
        # o selector NÃO foi tocado: mesma seed, mesma regra, mesmos 3 IDs.
        import dryrun, numpy as np
        ch1 = {f"i{k}": {"variante": v} for k, v in
               enumerate(["I"]*5 + ["II"]*5 + ["III"]*5)}
        ch2 = {f"j{k}": {"variante": v} for k, v in
               enumerate(["II"]*5 + ["III"]*5)}
        sel = dryrun.seleccionar(ch1, ch2)
        # reproduzir a regra congelada de forma independente
        self.assertEqual(dryrun.SEMENTE_DRYRUN, 777000300)
        rng = np.random.Generator(np.random.PCG64(777000300))
        esperado = {}
        for estrato, var in (("E1", "I"), ("E1", "II"), ("E1", "III"),
                             ("E2", "II"), ("E2", "III")):
            chave = ch1 if estrato == "E1" else ch2
            ids = sorted(i for i, k in chave.items() if k["variante"] == var)
            idx = rng.choice(len(ids), size=3, replace=False)
            esperado[f"{estrato}:{var}"] = [ids[int(i)] for i in sorted(idx)]
        self.assertEqual(sel, esperado)

    def test_formula_T_equiv_inalterada(self):
        # a fórmula congelada de extrapolação permanece EXACTAMENTE a mesma.
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
        r = dryrun.cronometrar(sel, d1, d2, amostra=1)
        tg = r["t_por_grupo_segundos"]
        esperado = ((50.0 / 3.0) * (tg["E1:I"] + tg["E1:II"] + tg["E1:III"])
                    + (25.0 / 3.0) * (tg["E2:II"] + tg["E2:III"])) / 3600.0
        self.assertEqual(r["T_equiv_estimado_horas"], esperado)


if __name__ == "__main__":
    unittest.main(verbosity=1)

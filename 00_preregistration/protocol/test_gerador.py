# -*- coding: utf-8 -*-
"""Testes unitários do gerador — Pré-registo A v8.3, marco 1.
Cobrem: determinismo total, rejeição por H constante, pi0 != pi1,
fecho da órbita, testemunhas de E6, exportação sem rótulos semânticos."""

import copy
import json
import unittest
import numpy as np

import gerador as g


def theta_valida_qualquer(semente=7, estrato2=False):
    """Percorre sementes até obter uma família elegível (uso só em testes)."""
    rng = np.random.Generator(np.random.PCG64(semente))
    for _ in range(50000):
        th = g.sample_theta_base(rng)
        if th.pi[0] == th.pi[1]:
            continue
        ok, _, tst = g.elegibilidade(th, estrato2)
        if ok:
            return th, tst
    raise RuntimeError("não encontrada família elegível no espaço de teste")


class TestDeterminismo(unittest.TestCase):
    def test_mesma_semente_mesmos_bytes(self):
        a = g.gerar_lote(123456, 2, False)
        b = g.gerar_lote(123456, 2, False)
        self.assertEqual(g.sha_serializacao(a[0]), g.sha_serializacao(b[0]))
        self.assertEqual(g.sha_serializacao(a[1]), g.sha_serializacao(b[1]))

    def test_sementes_diferentes_lotes_diferentes(self):
        a = g.gerar_lote(1, 2, False)
        b = g.gerar_lote(2, 2, False)
        self.assertNotEqual(g.sha_serializacao(a[0]), g.sha_serializacao(b[0]))


class TestElegibilidade(unittest.TestCase):
    def test_H_constante_rejeitado(self):
        th, _ = theta_valida_qualquer()
        th2 = copy.deepcopy(th)
        th2.H = [[0, 0, 0, 0], [0, 0, 0, 0]]          # H constante
        ok, razao, _ = g.elegibilidade(th2, False)
        self.assertFalse(ok)
        # Com H constante a rejeição vem por E1 (memoria sem variacao na
        # orbita) ou por E3 (Rec falha); ambas sao correctas na cascata.
        self.assertTrue(razao.startswith(("E1", "E3")), razao)

    def test_H_constante_com_memoria_inicial_divergente_cai_em_E3(self):
        th, _ = theta_valida_qualquer()
        th2 = copy.deepcopy(th)
        th2.H = [[0, 0, 0, 0], [0, 0, 0, 0]]
        th2.mA0 = 1                                    # visita m=1 e m=0: E1 passa
        th2.K = [[0, 0, 0, 0], [0, 0, 0, 0]]
        th2.mB0 = 1
        ok, razao, _ = g.elegibilidade(th2, False)
        self.assertFalse(ok)
        self.assertTrue(razao.startswith("E3"), razao)

    def test_sigma_constante_rejeitado(self):
        th, _ = theta_valida_qualquer()
        th2 = copy.deepcopy(th)
        th2.sigmaA = [1, 1]                            # sigma sem variacao
        ok, razao, _ = g.elegibilidade(th2, False)
        self.assertFalse(ok)
        self.assertTrue(razao.startswith("E5"), razao)

    def test_pi_identicas_nunca_aceites(self):
        _, chave, log, fams = g.gerar_lote(42, 3, False)
        for th, _ in fams:
            self.assertNotEqual(th.pi[0], th.pi[1])

    def test_testemunha_E6_verifica(self):
        th, tst = theta_valida_qualquer()
        w = tst["E6(II)"]
        b = w["dir_B"]
        self.assertNotEqual(th.G0[b["y"]][th.pi[b["m1"]][b["c"]]],
                            th.G0[b["y"]][th.pi[b["m2"]][b["c"]]])
        a = w["dir_A"]
        self.assertNotEqual(th.F0[a["x"]][th.pi[a["m1"]][a["c"]]],
                            th.F0[a["x"]][th.pi[a["m2"]][a["c"]]])


class TestOrbita(unittest.TestCase):
    def test_fecho_da_orbita(self):
        th, _ = theta_valida_qualquer()
        for var in ("I", "II", "III"):
            fn = g.step_fn(var)
            orb = g.orbita(g.estado_inicial(var, th), fn, th)
            conjunto = set(orb)
            for s in orb:
                self.assertIn(fn(s, th), conjunto)     # sucessor sempre visitado


class TestExportacaoCega(unittest.TestCase):
    def test_sem_rotulos_semanticos(self):
        inst, chave, log, _ = g.gerar_lote(99, 2, False)
        proibidos = ("variante", "familia", "II", "III", "theta")
        for i in inst:
            texto = json.dumps({k: v for k, v in i.items() if k != "transicao"})
            for p in proibidos:
                self.assertNotIn(f'"{p}"', texto)
            for m in i["modulos"]:
                self.assertTrue(m["id"].startswith("Q"))

    def test_chave_reconstroi_variante(self):
        inst, chave, log, _ = g.gerar_lote(99, 2, False)
        self.assertEqual(len(inst), 6)                 # 2 familias x 3 variantes
        variantes = [chave[i["id"]]["variante"] for i in inst]
        self.assertEqual(sorted(variantes), ["I", "I", "II", "II", "III", "III"])

    def test_dimensoes_congeladas(self):
        inst, chave, log, _ = g.gerar_lote(7, 1, False)
        por_var = {chave[i["id"]]["variante"]: i for i in inst}
        self.assertEqual(por_var["I"]["n"], 6)
        self.assertEqual(por_var["II"]["n"], 10)
        self.assertEqual(por_var["III"]["n"], 10)
        self.assertEqual(len(por_var["II"]["transicao"]), 1024)

    def test_estrato2_dimensao_e_par(self):
        inst, chave, log, _ = g.gerar_lote(11, 1, True)
        self.assertEqual(len(inst), 2)                 # par II/III
        for i in inst:
            self.assertEqual(i["n"], 12)
            self.assertEqual(len(i["transicao"]), 4096)


class TestEndurecimentos(unittest.TestCase):
    def test_ids_sem_colisoes(self):
        inst, chave, log, _ = g.gerar_lote(555, 5, False)
        ids = [i["id"] for i in inst]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(set(ids), set(chave.keys()))

    def test_theta_sha_completo(self):
        _, chave, _, _ = g.gerar_lote(556, 1, False)
        for k in chave.values():
            self.assertEqual(len(k["theta_sha"]), 64)

    def test_directorio_existente_falha(self):
        import subprocess, tempfile, os, sys
        with tempfile.TemporaryDirectory() as d:
            alvo = os.path.join(d, "lote")
            os.makedirs(alvo)
            r = subprocess.run([sys.executable, "gerador.py", "--semente", "1",
                                "--familias", "1", "--saida", alvo],
                               capture_output=True, text=True)
            self.assertNotEqual(r.returncode, 0)
            self.assertIn("existe", r.stderr)

    def test_manifesto_verificavel_ficheiro_a_ficheiro(self):
        import subprocess, tempfile, os, sys, hashlib, json as js
        with tempfile.TemporaryDirectory() as d:
            alvo = os.path.join(d, "lote")
            r = subprocess.run([sys.executable, "gerador.py", "--semente", "77",
                                "--familias", "2", "--saida", alvo],
                               capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stderr)
            man = js.load(open(os.path.join(alvo, "manifesto.json")))
            for nome, sha in man["ficheiros"].items():
                corpo = open(os.path.join(alvo, "instancias", nome), "rb").read()
                self.assertEqual(hashlib.sha256(corpo).hexdigest(), sha)
            corpo_chave = open(os.path.join(alvo, "CHAVE-NAO-ABRIR.json"), "rb").read()
            self.assertEqual(hashlib.sha256(corpo_chave).hexdigest(), man["sha_chave"])

    def test_estrato2_extensao_so_apos_aceitacao(self):
        # A extensao E2 nao pode influenciar a aceitacao: o conjunto de nucleos
        # aceites com estrato2=True tem de coincidir com estrato2=False para a
        # mesma semente (mesmo fluxo de sorteio do nucleo).
        _, _, _, fams_e1 = g.gerar_lote(888, 3, False)
        _, _, _, fams_e2 = g.gerar_lote(888, 3, True)
        for (t1, _), (t2, _) in zip(fams_e1, fams_e2):
            self.assertEqual(t1.F0, t2.F0)
            self.assertEqual(t1.pi, t2.pi)
            self.assertIsNone(t1.R1)
            self.assertIsNotNone(t2.R1)



if __name__ == "__main__":
    unittest.main(verbosity=2)

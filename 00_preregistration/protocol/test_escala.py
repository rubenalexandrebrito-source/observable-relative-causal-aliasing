# -*- coding: utf-8 -*-
"""Testes de escala.py: validade 6.4 por granularidade, quociente
comutativo, memória/módulo eliminados, projecção não admissível rejeitada."""
import unittest
import numpy as np
import gerador as g
import escala
import classificador as cl

SEMENTE_DEV = 777000111

class TValidade(unittest.TestCase):
    def test_granularidades_iguais_nao_validam(self):
        self.assertFalse(escala.validade_6_4([(0,1,2), (0,1,3)]))
    def test_granularidades_distintas_validam(self):
        self.assertTrue(escala.validade_6_4([(0,1,2), (0,1)]))
    def test_menos_de_duas_nao_valida(self):
        self.assertFalse(escala.validade_6_4([(0,1,2)]))

class TQuociente(unittest.TestCase):
    def setUp(self):
        inst, chave, _, _ = g.gerar_lote(SEMENTE_DEV, 1, True)
        self.inst = inst[0]
        self.n = self.inst["n"]
        self.T = np.asarray(self.inst["transicao"], dtype=np.int64)
    def test_quociente_comuta(self):
        # proj(T[z]) == T_S[proj(z)] para todo z, numa S admissível
        import itertools
        S = next(tuple(s) for r in range(2, self.n)
                 for s in itertools.combinations(range(self.n), r)
                 if escala.a1_admissivel(self.T, self.n, s))
        inst_S = escala.projectar_instancia(self.inst, S)
        T_S = np.asarray(inst_S["transicao"], dtype=np.int64)
        proj = cl.extractor(sorted(S), self.n)
        for z in range(1 << self.n):
            self.assertEqual(int(proj[self.T[z]]), int(T_S[proj[z]]))
    def test_nao_admissivel_rejeitada(self):
        # esquecer um bit de MEMORIA de um processador (estrutura declarada,
        # nao posicao: a instancia e cega e as posicoes estao permutadas)
        bit_mem = next(m["bits_memoria"][0] for m in self.inst["modulos"]
                       if m["bits_memoria"])
        S_ma = tuple(b for b in range(self.n) if b != bit_mem)
        self.assertFalse(escala.a1_admissivel(self.T, self.n, S_ma))

class TProjeccaoEstrutural(unittest.TestCase):
    def test_memoria_eliminada_colapsa_contexto(self):
        inst = {"id": "t", "n": 2,
                "modulos": [{"id": "Q0", "bits": [0, 1], "bits_memoria": [1]}],
                "estado_inicial": 0, "transicao": [0, 1, 2, 3]}
        inst_S = escala.projectar_instancia(inst, (0,))
        self.assertEqual(inst_S["modulos"][0]["bits_memoria"], [])
    def test_modulo_eliminado_desaparece(self):
        inst = {"id": "t", "n": 2,
                "modulos": [{"id": "Q0", "bits": [0], "bits_memoria": []},
                             {"id": "Q1", "bits": [1], "bits_memoria": []}],
                "estado_inicial": 0, "transicao": [0, 1, 2, 3]}
        inst_S = escala.projectar_instancia(inst, (0,))
        self.assertEqual([m["id"] for m in inst_S["modulos"]], ["Q0"])

class TAuditTrail(unittest.TestCase):
    def test_projeccoes_admissiveis_preservadas(self):
        inst, chave, _, _ = g.gerar_lote(SEMENTE_DEV, 1, True)
        r = escala.testar_instancia(inst[0])
        self.assertEqual(len(r["admissiveis"]), r["n_admissiveis"])
        self.assertEqual(len(r["projeccoes"]), r["n_admissiveis"])
        n = inst[0]["n"]
        for p in r["projeccoes"]:
            self.assertEqual(sorted(p["S"] + p["bits_removidos"]),
                             list(range(n)))
        self.assertEqual(r["granularidades_admissiveis"],
                         sorted({len(S) for S in r["admissiveis"]}))


if __name__ == "__main__":
    unittest.main(verbosity=1)

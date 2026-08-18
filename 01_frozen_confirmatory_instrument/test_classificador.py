import copy
# -*- coding: utf-8 -*-
"""Testes do classificador — marco 3. Semente de desenvolvimento 777000111,
declarada e excluída da confirmação (secção 11.1)."""

import unittest
import gerador as g
import classificador as cl

SEMENTE_DEV = 777000111

def lote_dev(n_fam=2, estrato2=False):
    return g.gerar_lote(SEMENTE_DEV, n_fam, estrato2)

def tipos_da_chave(k, variante):
    canon = ["A", "B"] if variante == "I" else ["A", "B", "C_AB", "C_BA"]
    return [canon[j] for j in k["ordem_modulos"]]


class TestDeterminismo(unittest.TestCase):
    def test_mesma_instancia_mesmo_resultado(self):
        inst, chave, _, _ = lote_dev(1)
        r1 = cl.classificar(inst[0])
        r2 = cl.classificar(inst[0])
        self.assertEqual(cl.sha_resultado(r1), cl.sha_resultado(r2))


class TestEstruturaCausal(unittest.TestCase):
    def test_EC_e_o_ciclo_esperado(self):
        inst, chave, _, _ = lote_dev(2)
        for i in inst:
            k = chave[i["id"]]
            r = cl.classificar(i)
            tipos = tipos_da_chave(k, k["variante"])
            arcos = {(tipos[a], tipos[b]) for (a, b) in r["E_C"]}
            if k["variante"] == "I":
                self.assertEqual(arcos, {("A", "B"), ("B", "A")})
            else:
                self.assertEqual(arcos, {("A", "C_AB"), ("C_AB", "B"),
                                         ("B", "C_BA"), ("C_BA", "A")})

    def test_sem_auto_arestas(self):
        inst, _, _, _ = lote_dev(2)
        for i in inst:
            r = cl.classificar(i)
            for (a, b) in r["E_C"]:
                self.assertNotEqual(a, b)


class TestCandidatas(unittest.TestCase):
    def test_receptor_sem_memoria_e_estado(self):
        # Arestas cujo receptor é canal (contexto {⊥}): estado nas três.
        inst, chave, _, _ = lote_dev(2)
        for i in inst:
            k = chave[i["id"]]
            if k["variante"] == "I":
                continue
            r = cl.classificar(i)
            tipos = tipos_da_chave(k, k["variante"])
            for aresta, v in r["arestas"].items():
                a, b = map(int, aresta.split("->"))
                if tipos[b].startswith("C_"):
                    for cand in ("C1p", "C2", "C3"):
                        self.assertEqual(v[cand], "estado", (aresta, cand))

    def test_canario_C3_falha_onde_a_derivacao_preve(self):
        # v8, derivação: em II, C3 classifica canal->processador como estado
        # NECESSARIAMENTE; se classificar sinal, a implementação está errada.
        inst, chave, _, _ = lote_dev(3)
        for i in inst:
            k = chave[i["id"]]
            if k["variante"] != "II":
                continue
            r = cl.classificar(i)
            tipos = tipos_da_chave(k, "II")
            for aresta, v in r["arestas"].items():
                a, b = map(int, aresta.split("->"))
                if tipos[a].startswith("C_") and tipos[b] in ("A", "B"):
                    self.assertEqual(v["C3"], "estado", aresta)

    def test_C1p_alvos_no_fumo_dev(self):
        # Diagnóstico de desenvolvimento (não critério confirmatório):
        # C1' recupera as partições-alvo nas instâncias dev.
        inst, chave, _, _ = lote_dev(3)
        for i in inst:
            k = chave[i["id"]]
            r = cl.classificar(i)
            tipos = tipos_da_chave(k, k["variante"])
            comps = {frozenset(tipos[m] for m in c) for c in r["C1p"]["componentes"]}
            meios = {frozenset(tipos[m] for m in c) for c in r["C1p"]["meios"]}
            if k["variante"] == "I":
                self.assertEqual(comps, {frozenset({"A", "B"})})
                self.assertEqual(meios, {frozenset({"A", "B"})})
            elif k["variante"] == "III":
                self.assertEqual(comps, {frozenset({"A", "B", "C_AB", "C_BA"})})
            else:
                self.assertEqual(comps, {frozenset({"A"}), frozenset({"B"}),
                                         frozenset({"C_AB"}), frozenset({"C_BA"})})
                self.assertEqual(meios, {frozenset({"A"}), frozenset({"B"})})


class TestMeios(unittest.TestCase):
    def test_canais_nunca_sao_meios(self):
        inst, chave, _, _ = lote_dev(2)
        for i in inst:
            k = chave[i["id"]]
            if k["variante"] == "I":
                continue
            r = cl.classificar(i)
            tipos = tipos_da_chave(k, k["variante"])
            for cand in ("C1p", "C2", "C3"):
                for c in r[cand]["meios"]:
                    if len(c) == 1:
                        self.assertFalse(tipos[c[0]].startswith("C_"), (cand, c))

    def test_estrato2_jusante_fora_dos_meios(self):
        inst, chave, _, _ = lote_dev(1, estrato2=True)
        canon = ["A", "B", "C_AB", "C_BA", "D1", "D2"]
        for i in inst:
            k = chave[i["id"]]
            r = cl.classificar(i)
            tipos = [canon[j] for j in k["ordem_modulos"]]
            for cand in ("C1p", "C2", "C3"):
                for c in r[cand]["meios"]:
                    for m in c:
                        self.assertFalse(tipos[m].startswith("D"), (cand, c))


def theta_valida_qualquer(semente=7):
    import numpy as np
    rng = np.random.Generator(np.random.PCG64(semente))
    for _ in range(50000):
        th = g.sample_theta_base(rng)
        if th.pi[0] == th.pi[1]:
            continue
        ok, _, tst = g.elegibilidade(th, False)
        if ok:
            return th, tst
    raise RuntimeError("sem familia elegivel")


class TestCancelamentoSigmaPi(unittest.TestCase):
    def test_meio_por_certificado_quando_efeito_liquido_cancela(self):
        """Constrói o caso da auditoria: F0(x, pi1(c)) = F0(x, pi0(c)) XOR
        delta com delta = sigmaA(0) XOR sigmaA(1) != 0. O efeito líquido da
        memória em x' é NULO, mas Rec do protocolo é verdadeiro (sigma
        eficaz). A decisão por certificado rho tem de marcar A como meio."""
        import numpy as np
        # Procura determinística: sorteiam-se familias base e aplica-se a
        # construção de cancelamento até uma satisfazer a ELEGIBILIDADE
        # COMPLETA (o contra-exemplo tem de pertencer à classe confirmatória;
        # a primeira família tentada NÃO pertencia, e essa falha ficou como
        # razão desta procura). Com a semente 7, encontra-se na 2.a tentativa.
        rng = np.random.Generator(np.random.PCG64(7))
        th2 = None
        for _ in range(200000):
            th = g.sample_theta_base(rng)
            if th.pi[0] == th.pi[1]:
                continue
            cand = copy.deepcopy(th)
            cand.sigmaA = [0, 3]                  # delta = 3
            cand.pi = [[0, 1, 2, 3], [1, 0, 3, 2]]   # pi0=id, pi1=(01)(23)
            tau = [cand.pi[0].index(cand.pi[1][c]) for c in range(4)]
            for x in range(4):                    # g em representantes 0,2
                cand.F0[x][tau[0]] = cand.F0[x][0] ^ 3
                cand.F0[x][tau[2]] = cand.F0[x][2] ^ 3
            if g.elegibilidade(cand, False)[0]:
                th2 = cand
                break
        self.assertIsNotNone(th2, "nenhuma família elegível com cancelamento")
        # verificação da construção: efeito líquido nulo em x'
        for x in range(4):
            for c in range(4):
                self.assertEqual(th2.F0[x][th2.pi[0][c]] ^ th2.sigmaA[0],
                                 th2.F0[x][th2.pi[1][c]] ^ th2.sigmaA[1])
        # dupla verificação explícita da pertença à classe confirmatória
        ok, razao, _ = g.elegibilidade(th2, False)
        self.assertTrue(ok, f"contra-exemplo fora da classe elegível: {razao}")
        tab, n, _ = g.tabela_transicao("II", th2, False)
        mods = g._modulos_canonicos("II", False)
        inst = {"id": "cancel", "n": n,
                "modulos": [{"id": f"Q{i}", "bits": m["bits"],
                             "bits_memoria": m["mem"]}
                            for i, m in enumerate(mods)],
                "estado_inicial": g._campos_para_int(
                    g.estado_inicial("II", th2), g._layout("II", False)),
                "transicao": tab}
        r = cl.classificar(inst)
        # replicar o criterio ANTIGO (efeito líquido) e mostrar que falha:
        T = np.asarray(tab, dtype=np.int64)
        membits = [2]                             # m^A no layout canónico
        outros = [0, 1]
        eout = cl.extractor(outros, n)
        Z0 = cl.estados_da_fibra(n, membits, 0)
        Z1 = cl.estados_da_fibra(n, membits, 1)
        efeito_liquido = not np.array_equal(eout[T[Z0]], eout[T[Z1]])
        self.assertFalse(efeito_liquido)          # o cancelamento existe
        # e ainda assim A é meio por rho; a situação tem de OCORRER
        # (não-vacuidade exigida: um teste que passa sem observar o caso
        # que afirma testar não testa nada):
        encontrou = False
        for cand in ("C1p", "C2", "C3"):
            for c in r[cand]["componentes"]:
                if c == [0]:                      # módulo A canónico
                    encontrou = True
                    self.assertIn([0], r[cand]["meios"], cand)
        self.assertTrue(encontrou,
                        "A nunca apareceu como SCC singular no caso construído")


if __name__ == "__main__":
    unittest.main(verbosity=1)

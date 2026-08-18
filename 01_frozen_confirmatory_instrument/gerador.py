# -*- coding: utf-8 -*-
"""
gerador.py — Pré-registo A, v8.3 (congelado). Fase: implementação, marco 1.

Gera famílias theta e instâncias cegas conforme as secções 2, 3, 8 e 9 do
protocolo. Este ficheiro implementa EXCLUSIVAMENTE o que o protocolo fixa;
onde o protocolo remete para o código (nada, por desenho), não há decisões
novas aqui. Qualquer divergência entre este ficheiro e o protocolo é bug.

Convenções congeladas (secção 8, "Dimensões e distribuições"):
  x, y, c em {0,1}^2, representados como inteiros 0..3
  m^A, m^B em {0,1}
  Sistemas II/III: n = 10;  Sistema I: n = 6;  Estrato 2: n = 12

Empacotamento canónico de bits (documentado; a ordem é parte da serialização):
  bit 0 = x LSB, bit 1 = x MSB, bit 2 = m^A,
  bit 3 = y LSB, bit 4 = y MSB, bit 5 = m^B,
  bits 6-7 = c^AB, bits 8-9 = c^BA, bit 10 = D1, bit 11 = D2.

Aleatoriedade (exigência 1 do marco): função pura da semente, PCG64 explícito,
quatro fluxos derivados por SeedSequence.spawn(4), com atribuição POSICIONAL
fixa e documentada: [0] theta nuclear, [1] permutações de exportação,
[2] baralhamento, [3] extensões do Estrato 2. O fluxo [3] separado garante
que o sorteio nuclear é idêntico entre estratos para a mesma semente.
"""

import json
import hashlib
from dataclasses import dataclass, field, asdict
from typing import Optional
import numpy as np

# ----------------------------------------------------------------------
# Constantes congeladas
# ----------------------------------------------------------------------

X_SYMBOLS = 4          # |X| = 2 bits
M_SYMBOLS = 2          # |M| = 1 bit
N_I, N_II_III, N_E2 = 6, 10, 12
# Fail-safe de engenharia, ausente do protocolo por ser operacional e nao
# cientifico. Semantica fixada: se atingido, a geracao ABORTA sem produzir
# conjunto confirmatorio; nao autoriza relaxar elegibilidade, mudar
# distribuicoes nem reutilizar amostra parcial. Consta do relatorio.
MAX_TENTATIVAS_POR_FAMILIA = 100000

VARIANTES = ("I", "II", "III")   # apenas interno; NUNCA exportado em claro

# ----------------------------------------------------------------------
# theta (secção 9): unidade geradora, condições iniciais incluídas
# ----------------------------------------------------------------------

@dataclass
class Theta:
    F0: list          # 4x4 -> 0..3
    G0: list          # 4x4 -> 0..3
    H: list           # 2x4 -> 0..1
    K: list           # 2x4 -> 0..1
    sigmaA: list      # 2 -> 0..3
    sigmaB: list      # 2 -> 0..3
    pi: list          # [pi0, pi1], cada uma permutação de 0..3; pi0 != pi1
    x0: int; mA0: int; y0: int; mB0: int
    cAB0: int; cBA0: int
    # Extensão Estrato 2 (secção 8: D_{i,t+1} = R_i(s_core_t)):
    R1: Optional[list] = None    # 1024 -> 0..1
    R2: Optional[list] = None
    d10: int = 0
    d20: int = 0

def sample_theta_base(rng: np.random.Generator) -> Theta:
    """Sorteio uniforme do NUCLEO dentro das famílias congeladas (secção 8).
    A extensão do Estrato 2 é sorteada SO DEPOIS da aceitação (secção 9,
    passo 2 do procedimento por família): famílias rejeitadas não consomem
    números do fluxo destinados a R1, R2 e D_{i,0}."""
    F0 = rng.integers(0, 4, size=(4, 4)).tolist()
    G0 = rng.integers(0, 4, size=(4, 4)).tolist()
    H  = rng.integers(0, 2, size=(2, 4)).tolist()
    K  = rng.integers(0, 2, size=(2, 4)).tolist()
    sigmaA = rng.integers(0, 4, size=2).tolist()
    sigmaB = rng.integers(0, 4, size=2).tolist()
    pi0 = rng.permutation(4).tolist()
    pi1 = rng.permutation(4).tolist()
    return Theta(
        F0=F0, G0=G0, H=H, K=K, sigmaA=sigmaA, sigmaB=sigmaB, pi=[pi0, pi1],
        x0=int(rng.integers(0, 4)), mA0=int(rng.integers(0, 2)),
        y0=int(rng.integers(0, 4)), mB0=int(rng.integers(0, 2)),
        cAB0=int(rng.integers(0, 4)), cBA0=int(rng.integers(0, 4)),
    )

def estender_theta_e2(th: Theta, rng: np.random.Generator) -> None:
    """Extensão do Estrato 2, aplicada apenas a famílias ACEITES."""
    th.R1 = rng.integers(0, 2, size=1024).tolist()
    th.R2 = rng.integers(0, 2, size=1024).tolist()
    th.d10 = int(rng.integers(0, 2))
    th.d20 = int(rng.integers(0, 2))

# ----------------------------------------------------------------------
# Dinâmica (secção 8) — estado como tuplos de campos
# Estado nuclear: (x, mA, y, mB[, cAB, cBA])
# ----------------------------------------------------------------------

def step_I(s, th: Theta):
    x, mA, y, mB = s
    u, v = y, x                                   # v_t = x_t, u_t = y_t
    return (th.F0[x][u] ^ th.sigmaA[mA], th.H[mA][x],
            th.G0[y][v] ^ th.sigmaB[mB], th.K[mB][y])

def step_III(s, th: Theta):
    x, mA, y, mB, cAB, cBA = s
    u, v = cBA, cAB                               # interface directa
    return (th.F0[x][u] ^ th.sigmaA[mA], th.H[mA][x],
            th.G0[y][v] ^ th.sigmaB[mB], th.K[mB][y],
            x, y)                                 # c^AB' = x, c^BA' = y

def step_II(s, th: Theta):
    x, mA, y, mB, cAB, cBA = s
    v = th.pi[mB][cAB]                            # remapeamento pela memória
    u = th.pi[mA][cBA]
    return (th.F0[x][u] ^ th.sigmaA[mA], th.H[mA][x],
            th.G0[y][v] ^ th.sigmaB[mB], th.K[mB][y],
            x, y)

def pack_core10(s):
    x, mA, y, mB, cAB, cBA = s
    return x | (mA << 2) | (y << 3) | (mB << 5) | (cAB << 6) | (cBA << 8)

def step_E2(s, th: Theta, base_step):
    core, d1, d2 = s[:-2], s[-2], s[-1]
    ncore = base_step(core, th)
    idx = pack_core10(core)                       # D lê o núcleo em t (jusante)
    return ncore + (th.R1[idx], th.R2[idx])

def estado_inicial(variante, th: Theta, estrato2=False):
    if variante == "I":
        s = (th.x0, th.mA0, th.y0, th.mB0)
    else:
        s = (th.x0, th.mA0, th.y0, th.mB0, th.cAB0, th.cBA0)
    if estrato2:
        s = s + (th.d10, th.d20)
    return s

def step_fn(variante, estrato2=False):
    base = {"I": step_I, "II": step_II, "III": step_III}[variante]
    if not estrato2:
        return base
    return lambda s, th: step_E2(s, th, base)

def orbita(s0, fn, th: Theta):
    """Fecho da trajectória determinística (secção 3): lista de estados
    visitados a partir de s0 até à primeira repetição."""
    vistos, ordem = set(), []
    s = s0
    while s not in vistos:
        vistos.add(s)
        ordem.append(s)
        s = fn(s, th)
    return ordem

# ----------------------------------------------------------------------
# Elegibilidade (secção 8, condições 1-6) — funções puras com testemunhas
# ----------------------------------------------------------------------

def _entrada_actual(variante, s, th):
    """(v_t, u_t) no estado s, conforme a interface da variante."""
    if variante == "I":
        x, mA, y, mB = s[0], s[1], s[2], s[3]
        return x, y
    x, mA, y, mB, cAB, cBA = s[:6]
    if variante == "III":
        return cAB, cBA
    return th.pi[mB][cAB], th.pi[mA][cBA]

def cond1_memoria(orb):
    mAs = {s[1] for s in orb}
    mBs = {s[3] for s in orb}
    ok = len(mAs) >= 2 and len(mBs) >= 2
    return ok, {"mA_alc": sorted(mAs), "mB_alc": sorted(mBs)}

def cond2_eficacia_entradas(variante, orb, th):
    tv = tu = None
    for s in orb:
        v, u = _entrada_actual(variante, s, th)
        y, x = s[2], s[0]
        if tv is None:
            for v2 in range(4):
                if v2 != v and th.G0[y][v2] != th.G0[y][v]:
                    tv = {"estado": s, "v": v, "v_alt": v2}
                    break
        if tu is None:
            for u2 in range(4):
                if u2 != u and th.F0[x][u2] != th.F0[x][u]:
                    tu = {"estado": s, "u": u, "u_alt": u2}
                    break
        if tv and tu:
            break
    return (tv is not None and tu is not None), {"v": tv, "u": tu}

def cond3_rec(orb, th):
    """Rec (secção 8, condição 3): x~>m por testemunha alcançável;
    m~>x coincide com a condição 5 e é verificada lá."""
    tA = tB = None
    for s in orb:
        x, mA, y, mB = s[0], s[1], s[2], s[3]
        if tA is None:
            for x2 in range(4):
                if th.H[mA][x2] != th.H[mA][x]:
                    tA = {"m": mA, "x": x, "x_alt": x2}
                    break
        if tB is None:
            for y2 in range(4):
                if th.K[mB][y2] != th.K[mB][y]:
                    tB = {"m": mB, "y": y, "y_alt": y2}
                    break
        if tA and tB:
            break
    return (tA is not None and tB is not None), {"A": tA, "B": tB}

def cond4_alcancabilidade(orb):
    pA = {(s[0], s[1]) for s in orb}
    pB = {(s[2], s[3]) for s in orb}
    return (len(pA) >= 4 and len(pB) >= 4), {"|A|": len(pA), "|B|": len(pB)}

def cond5_sigma(orb, th):
    sA = {th.sigmaA[s[1]] for s in orb}
    sB = {th.sigmaB[s[3]] for s in orb}
    return (len(sA) >= 2 and len(sB) >= 2), {"sigmaA": sorted(sA), "sigmaB": sorted(sB)}

def cond6_remapeamento(orb_II, th):
    """Secção 8, condição 6, nas duas direcções, com m1 != m2 alcançáveis."""
    mAs = sorted({s[1] for s in orb_II})
    mBs = sorted({s[3] for s in orb_II})
    if len(mAs) < 2 or len(mBs) < 2:
        return False, {"razao": "memoria_sem_variacao"}
    tB = tA = None
    for c in range(4):
        for y in range(4):
            if th.G0[y][th.pi[mBs[0]][c]] != th.G0[y][th.pi[mBs[1]][c]]:
                tB = {"c": c, "y": y, "m1": mBs[0], "m2": mBs[1]}
                break
        if tB:
            break
    for c in range(4):
        for x in range(4):
            if th.F0[x][th.pi[mAs[0]][c]] != th.F0[x][th.pi[mAs[1]][c]]:
                tA = {"c": c, "x": x, "m1": mAs[0], "m2": mAs[1]}
                break
        if tA:
            break
    return (tB is not None and tA is not None), {"dir_B": tB, "dir_A": tA}

def elegibilidade(th: Theta, estrato2: bool):
    """Elig(theta) <=> E_{1:5}(I) ∧ E_{1:5}(II) ∧ E_{1:5}(III) ∧ E_6(II).
    (Secção 9, elegibilidade por variante.) A elegibilidade avalia o núcleo;
    os módulos a jusante do Estrato 2 são causalmente inertes para o núcleo
    por equação (secção 3, tipificação), e não entram aqui."""
    testemunhas = {}
    orb_II = None
    for var in VARIANTES:
        orb = orbita(estado_inicial(var, th), step_fn(var), th)
        if var == "II":
            orb_II = orb
        for nome, f in (("E1", lambda o: cond1_memoria(o)),
                        ("E2", lambda o: cond2_eficacia_entradas(var, o, th)),
                        ("E3", lambda o: cond3_rec(o, th)),
                        ("E4", lambda o: cond4_alcancabilidade(o)),
                        ("E5", lambda o: cond5_sigma(o, th))):
            ok, w = f(orb)
            if not ok:
                return False, f"{nome}({var})", None
            testemunhas[f"{nome}({var})"] = w
    ok, w = cond6_remapeamento(orb_II, th)
    if not ok:
        return False, "E6(II)", None
    testemunhas["E6(II)"] = w
    return True, None, testemunhas

# ----------------------------------------------------------------------
# Empacotamento binário canónico e tabela de transição completa
# ----------------------------------------------------------------------

def _layout(variante, estrato2):
    """Lista de (nome_interno, largura_bits) na ordem canónica congelada."""
    lay = [("x", 2), ("mA", 1), ("y", 2), ("mB", 1)]
    if variante != "I":
        lay += [("cAB", 2), ("cBA", 2)]
    if estrato2:
        lay += [("d1", 1), ("d2", 1)]
    return lay

def _campos_para_int(s, lay):
    v, off = 0, 0
    for valor, (_, w) in zip(s, lay):
        v |= (valor << off)
        off += w
    return v

def _int_para_campos(v, lay):
    out = []
    for _, w in lay:
        out.append(v & ((1 << w) - 1))
        v >>= w
    return tuple(out)

def tabela_transicao(variante, th, estrato2):
    lay = _layout(variante, estrato2)
    n = sum(w for _, w in lay)
    fn = step_fn(variante, estrato2)
    tab = [0] * (1 << n)
    for v in range(1 << n):
        tab[v] = _campos_para_int(fn(_int_para_campos(v, lay), th), lay)
    return tab, n, lay

def _modulos_canonicos(variante, estrato2):
    """Grupos de bits por módulo no layout canónico (secção 3, tipificação)."""
    mods = [{"bits": [0, 1, 2], "mem": [2]},        # A = (x, mA)
            {"bits": [3, 4, 5], "mem": [5]}]        # B = (y, mB)
    if variante != "I":
        mods += [{"bits": [6, 7], "mem": []},        # C_AB
                 {"bits": [8, 9], "mem": []}]        # C_BA
    if estrato2:
        mods += [{"bits": [10], "mem": []},          # D1
                 {"bits": [11], "mem": []}]          # D2
    return mods

# ----------------------------------------------------------------------
# Exportação cega (secção 9, passos 3-5)
# ----------------------------------------------------------------------

def exportar_instancia(variante, th, estrato2, rng: np.random.Generator):
    """Permutação independente de identificadores; fronteiras modulares
    visíveis SEM rótulos semânticos; nenhuma indicação de gémeas."""
    tab, n, lay = tabela_transicao(variante, th, estrato2)
    perm = rng.permutation(n)                    # pos_export = perm[bit_interno]
    def reindex(v):
        out = 0
        for i in range(n):
            out |= ((v >> i) & 1) << int(perm[i])
        return out
    tab_exp = [0] * (1 << n)
    for s_exp in range(1 << n):
        s_int = 0
        for i in range(n):
            s_int |= ((s_exp >> int(perm[i])) & 1) << i
        tab_exp[s_exp] = reindex(tab[s_int])
    mods = _modulos_canonicos(variante, estrato2)
    ordem_mods = rng.permutation(len(mods))
    mods_exp = []
    for k, j in enumerate(ordem_mods):
        m = mods[int(j)]
        mods_exp.append({
            "id": f"Q{k}",
            "bits": sorted(int(perm[b]) for b in m["bits"]),
            "bits_memoria": sorted(int(perm[b]) for b in m["mem"]),
        })
    s0 = _campos_para_int(estado_inicial(variante, th, estrato2),
                          _layout(variante, estrato2))
    inst = {
        "n": n,
        "modulos": mods_exp,
        "estado_inicial": reindex(s0),
        "transicao": tab_exp,
    }
    chave = {"variante": variante, "perm": [int(p) for p in perm],
             "ordem_modulos": [int(j) for j in ordem_mods]}
    return inst, chave

# ----------------------------------------------------------------------
# Geração de lotes com registo de rejeições (secção 8)
# ----------------------------------------------------------------------

def gerar_lote(semente_raiz: int, n_familias: int, estrato2: bool):
    """Função pura da semente. Fluxos: SeedSequence(raiz).spawn(4) ordenado:
    [0] theta nuclear; [1] permutações de exportação; [2] baralhamento;
    [3] extensões E2, consumidas apenas por famílias aceites."""
    ss = np.random.SeedSequence(semente_raiz)
    filhos = ss.spawn(4)
    rng_theta = np.random.Generator(np.random.PCG64(filhos[0]))
    rng_export = np.random.Generator(np.random.PCG64(filhos[1]))
    rng_shuffle = np.random.Generator(np.random.PCG64(filhos[2]))
    rng_e2 = np.random.Generator(np.random.PCG64(filhos[3]))

    rejeicoes = {}
    familias = []
    tentativas_total = 0
    while len(familias) < n_familias:
        if tentativas_total >= MAX_TENTATIVAS_POR_FAMILIA * n_familias:
            raise RuntimeError("limite de tentativas excedido; registar e investigar")
        tentativas_total += 1
        th = sample_theta_base(rng_theta)
        if th.pi[0] == th.pi[1]:
            rejeicoes["pi_identicas"] = rejeicoes.get("pi_identicas", 0) + 1
            continue
        ok, razao, testemunhas = elegibilidade(th, estrato2)
        if not ok:
            rejeicoes[razao] = rejeicoes.get(razao, 0) + 1
            continue
        if estrato2:
            estender_theta_e2(th, rng_e2)      # so apos aceitacao (v8.3, sec. 9)
        familias.append((th, testemunhas))

    variantes = ("II", "III") if estrato2 else ("I", "II", "III")
    instancias, chave = [], {}
    for fam_idx, (th, _) in enumerate(familias):
        for var in variantes:
            inst, k = exportar_instancia(var, th, estrato2, rng_export)
            iid = rng_shuffle.bytes(8).hex()
            inst["id"] = iid
            instancias.append(inst)
            k["familia"] = fam_idx
            k["theta_sha"] = hashlib.sha256(
                json.dumps(asdict(th), sort_keys=True).encode()).hexdigest()
            chave[iid] = k
    ordem = rng_shuffle.permutation(len(instancias))
    instancias = [instancias[int(i)] for i in ordem]

    log = {
        "semente_raiz": semente_raiz,
        "estrato2": estrato2,
        "n_familias": n_familias,
        "tentativas": tentativas_total,
        "rejeicoes": rejeicoes,
        "taxa_aceitacao": n_familias / tentativas_total,
    }
    return instancias, chave, log, familias

def sha_serializacao(objecto) -> str:
    """Serialização canónica congelada: JSON, chaves ordenadas, sem espaços."""
    return hashlib.sha256(
        json.dumps(objecto, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()

# ----------------------------------------------------------------------
if __name__ == "__main__":
    import argparse, os, sys, platform
    ap = argparse.ArgumentParser()
    ap.add_argument("--semente", type=int, required=True)
    ap.add_argument("--familias", type=int, required=True)
    ap.add_argument("--estrato2", action="store_true")
    ap.add_argument("--saida", type=str, required=True)
    a = ap.parse_args()

    # Directório novo e imutável (auditoria do marco 1, ponto 2): uma execução
    # confirmatória nunca escreve sobre restos de outra.
    if os.path.exists(a.saida):
        raise FileExistsError(
            f"O directório de saída '{a.saida}' já existe. "
            "Uma execução exige directório novo; apague ou escolha outro.")
    os.makedirs(os.path.join(a.saida, "instancias"))

    inst, chave, log, _ = gerar_lote(a.semente, a.familias, a.estrato2)

    # Serialização canónica ficheiro a ficheiro: os bytes gravados são
    # exactamente os bytes hasheados (ficheiro -> bytes -> SHA-256).
    ficheiros = {}
    ordered_ids = []
    for i in inst:
        corpo = json.dumps(i, sort_keys=True, separators=(",", ":")).encode()
        nome = i["id"] + ".json"
        with open(os.path.join(a.saida, "instancias", nome), "wb") as f:
            f.write(corpo)
        ficheiros[nome] = hashlib.sha256(corpo).hexdigest()
        ordered_ids.append(i["id"])

    corpo_chave = json.dumps(chave, sort_keys=True, separators=(",", ":")).encode()
    with open(os.path.join(a.saida, "CHAVE-NAO-ABRIR.json"), "wb") as f:
        f.write(corpo_chave)

    manifesto = {
        "semente_raiz": a.semente,
        "estrato2": a.estrato2,
        "n_familias": a.familias,
        "ordered_ids": ordered_ids,
        "ficheiros": ficheiros,
        "sha_chave": hashlib.sha256(corpo_chave).hexdigest(),
        "ambiente": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "bit_generator": "PCG64",
            "plataforma": platform.platform(),
        },
        "log_geracao": log,
        "nota_cegamento": (
            "Cegamento PROCEDIMENTAL, nao criptografico: codigo + semente "
            "regeneram a chave. Regras: (1) a chave sai do directorio "
            "acessivel ao classificador antes da analise; (2) o gerador nao "
            "volta a correr com a semente confirmatoria durante a analise; "
            "(3) a chave abre-se apenas no passo pre-especificado (11.3), "
            "verificada contra sha_chave."),
        "nota_failsafe": (
            "MAX_TENTATIVAS: se atingido, aborta sem produzir conjunto; "
            "nao autoriza relaxar elegibilidade nem reutilizar amostra parcial."),
    }
    corpo_man = json.dumps(manifesto, sort_keys=True, indent=1).encode()
    with open(os.path.join(a.saida, "manifesto.json"), "wb") as f:
        f.write(corpo_man)
    print(json.dumps({"sha_manifesto": hashlib.sha256(corpo_man).hexdigest(),
                      **{k: log[k] for k in ("tentativas", "taxa_aceitacao")}},
                     sort_keys=True, indent=1))

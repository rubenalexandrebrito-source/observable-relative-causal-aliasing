# -*- coding: utf-8 -*-
"""
fases_0_3.py — Orquestrador das Fases 0 a 3 do guião, para a MÁQUINA
REGISTADA. Executa exactamente os passos escritos, pela ordem escrita,
sem decisões: pára ao primeiro falhanço, grava um registo datado, e no fim
imprime os oito números e o veredicto aritmético do gate das 72 horas.

Uso oficial:   python3 fases_0_3.py  (colocado ao lado de prereg-A/; entra nele sozinho)
Fumo mecânico: python3 fases_0_3.py --fumo   (parâmetros minúsculos, modo
               amostra, num subdirectório; serve só para verificar que a
               canalização corre de ponta a ponta antes de gastar horas)
"""

import argparse
import datetime
import hashlib
import json
import os
import platform
import subprocess
import sys
import time

SUITES = ["test_gerador.py", "test_classificador.py", "test_escala.py",
          "test_pontuacao.py", "test_equivalencias.py"]
GATE_HORAS = 72.0


def abortar_registado(registo, estado, mensagem):
    """Quando o PROTOCOLO decide não executar (gate não passa), a decisão é
    um resultado legítimo e persiste no registo consolidado. Falhas de
    engenharia (suite vermelha, ficheiro corrompido) continuam a abortar
    sem registo oficial: não são decisões do protocolo."""
    registo["estado"] = estado
    registo["fim"] = datetime.datetime.now().astimezone().isoformat()
    registo["dados_confirmatorios_gerados"] = False
    open("registo-fases-0-3.json", "w").write(
        json.dumps(registo, sort_keys=True, indent=1))
    sys.exit(mensagem + " Registo gravado em registo-fases-0-3.json.")


def correr(cmd, descricao):
    print(f"\n== {descricao}\n$ {' '.join(cmd)}")
    t0 = time.perf_counter()
    r = subprocess.run(cmd)
    dt = time.perf_counter() - t0
    if r.returncode != 0:
        sys.exit(f"FALHOU: {descricao} (código {r.returncode}). "
                 "Parar aqui; nada mais corre.")
    return dt


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fumo", action="store_true")
    a = ap.parse_args()

    # O orquestrador é externo: vive ao lado de prereg-A/ e ENTRA nele
    # sozinho, eliminando a decisão humana sobre o directório de trabalho.
    # Topologia ÚNICA exigida: orquestrador externo, ao lado de prereg-A/
    # com exactamente os 12 ficheiros do instrumento lá dentro. Sem
    # fallbacks: menos estados possíveis, menos decisões.
    raiz = os.path.dirname(os.path.abspath(__file__))
    instrumento = os.path.join(raiz, "prereg-A")
    if not os.path.isdir(instrumento):
        sys.exit(f"Topologia exigida: {raiz}/prereg-A/ com os 12 ficheiros "
                 "do instrumento. Não encontrado; nada correu.")
    os.chdir(instrumento)
    if a.fumo:
        os.makedirs("fumo-fases", exist_ok=True)
        for f in os.listdir("."):
            if f.endswith(".py") and f != "fases_0_3.py":
                subprocess.run(["cp", f, "fumo-fases/"])
        os.chdir("fumo-fases")
        fam_e1, fam_e2 = 3, 3
    else:
        fam_e1, fam_e2 = 50, 25

    # PREFLIGHT: falhar por ficheiro existente ANTES de gastar horas, não no fim
    for saida in ("registo-fases-0-3.json", "benchmark-oficial.json",
                  "dry-e1", "dry-e2", "dryrun-seleccao.json",
                  "dryrun-tempos.json", "hashes-codigo.txt", "hardware.txt"):
        if os.path.exists(saida):
            sys.exit(f"PREFLIGHT: '{saida}' já existe. Directório de execução "
                     "tem de estar limpo; nada correu.")

    registo = {"inicio": datetime.datetime.now().isoformat(),
               "fumo": a.fumo}

    # Fase 0: hashes contra o manifesto, hardware, versões, suites
    # (no fumo, os ficheiros em fumo-fases/ são cópias byte a byte do
    # instrumento, pelo que a verificação contra o manifesto vale igual)
    # O orquestrador é EXTERNO ao instrumento e não entra nos doze hashes.
    # INTEGRIDADE: não basta contar doze ficheiros; os hashes calculados
    # têm de coincidir EXACTAMENTE com o manifesto pré-registado
    # hashes-finais-dev.txt, que vive AO LADO do orquestrador, fora de
    # prereg-A/. Código executado = código auditado = código cujo hash
    # foi pré-registado. Qualquer divergência aborta antes de tudo.
    hashes = {}
    for f in sorted(os.listdir(".")):
        if f.endswith(".py") and f != "fases_0_3.py":
            hashes[f] = hashlib.sha256(open(f, "rb").read()).hexdigest()
    manifesto = os.path.join(raiz, "hashes-finais-dev.txt")
    if not os.path.isfile(manifesto):
        sys.exit(f"Não encontro o manifesto {manifesto}. Nada correu.")
    esperados = {}
    with open(manifesto) as fh:
        for linha in fh:
            linha = linha.strip()
            if not linha:
                continue
            sha, nome = linha.split(None, 1)
            esperados[nome.strip()] = sha.strip()
    if hashes != esperados:
        faltam = sorted(set(esperados) - set(hashes))
        sobram = sorted(set(hashes) - set(esperados))
        alterados = sorted(n for n in set(hashes) & set(esperados)
                           if hashes[n] != esperados[n])
        sys.exit("HASHES DO INSTRUMENTO NÃO CONFEREM. "
                 f"Faltam={faltam}; sobram={sobram}; alterados={alterados}. "
                 "Nada correu.")
    open("hashes-codigo.txt", "w").write(
        "\n".join(f"{v}  {k}" for k, v in hashes.items()))
    import numpy
    import uuid
    registo["hardware"] = {"plataforma": platform.platform(),
                           "node": hex(uuid.getnode()),
                           "python": sys.version,
                           "numpy": numpy.__version__}
    open("hardware.txt", "w").write(json.dumps(registo["hardware"], indent=1))
    for s in SUITES:
        correr([sys.executable, s], f"suite {s}")

    # Fase 1: benchmark oficial (completo; no fumo, truncado)
    bench = [sys.executable, "benchmark.py", "--saida", "benchmark-oficial.json"]
    if a.fumo:
        bench += ["--max-projeccoes", "50", "--dimensoes", "6", "10"]
    correr(bench, "benchmark 11.0")
    # FAIL-CLOSED: benchmark incompleto => ABORTAR, nunca assumir zero.
    # O contrato do JSON é verificado também no fumo; só o gate numérico
    # das 72 h é exclusivo da execução oficial (o fumo trunca dimensões e
    # não produz estimativa completa por construção).
    b = json.load(open("benchmark-oficial.json"))
    if not a.fumo:
        try:
            est = b["estimativa_confirmatoria"]
            e1_h = float(est["estrato1_A1_horas"])
            e2_h = float(est["estrato2_A1_horas"])
        except (KeyError, TypeError, ValueError) as e:
            sys.exit(f"Benchmark sem os campos temporais obrigatórios: {e!r}. "
                     "Parar; não assumir zero.")
        if e1_h < 0 or e2_h < 0:
            sys.exit("Benchmark contém estimativa temporal negativa. Parar.")
        a1_h = e1_h + e2_h
        registo["A1_estimativa_horas"] = a1_h
        if a1_h > GATE_HORAS:
            abortar_registado(
                registo, "NAO_PASSA_GATE_BENCHMARK_A1",
                f"GATE DO BENCHMARK: componente A1 estimada em "
                f"{a1_h:.1f} h > {GATE_HORAS} h. Parar (passo 7 do guião): "
                f"emenda pré-dados; nenhum dry run corre.")
    else:
        # fumo: verificar o CONTRATO estrutural sem aplicar o gate
        if "resultados" not in b or "declaracao" not in b:
            sys.exit("Fumo: JSON do benchmark sem os campos estruturais "
                     "obrigatórios. Parar.")

    # Fase 3a: lotes descartáveis do dry run (sementes do guião)
    correr([sys.executable, "gerador.py", "--semente", "777000200",
            "--familias", str(fam_e1), "--saida", "dry-e1"], "gerar dry-e1")
    correr([sys.executable, "gerador.py", "--semente", "777000201",
            "--familias", str(fam_e2), "--estrato2", "--saida", "dry-e2"],
           "gerar dry-e2")

    # Fase 3b: cronometrar os três executores
    # Saídas classificatórias do dry run: em /tmp e ELIMINADAS depois de
    # recolhidos os tempos (o guião manda descartar sem inspecção; conservar
    # estes ficheiros criaria uma via de olhar para o que devia desaparecer).
    import tempfile
    import shutil
    tmpdir = tempfile.mkdtemp(prefix="dry-descartavel-")
    T = {}
    try:
        T["classificador_E1"] = correr(
            [sys.executable, "classificador.py", "--instancias",
             "dry-e1/instancias", "--saida",
             os.path.join(tmpdir, "dry-class-e1.json")], "classificador E1")
        T["escala_E1"] = correr(
            [sys.executable, "escala.py", "--instancias", "dry-e1/instancias",
             "--saida", os.path.join(tmpdir, "dry-escala-e1.json")],
            "escala E1")
        T["escala_E2"] = correr(
            [sys.executable, "escala.py", "--instancias", "dry-e2/instancias",
             "--saida", os.path.join(tmpdir, "dry-escala-e2.json")],
            "escala E2")
    finally:
        # a promessa "estas classificações não sobrevivem" vale também
        # numa execução interrompida
        shutil.rmtree(tmpdir, ignore_errors=True)

    # Fase 3c: runner temporal das equivalências (selector + 15 exaustivos)
    correr([sys.executable, "dryrun.py",
            "--chave-e1", "dry-e1/CHAVE-NAO-ABRIR.json",
            "--chave-e2", "dry-e2/CHAVE-NAO-ABRIR.json",
            "--saida", "dryrun-seleccao.json",
            "--cronometrar", "dry-e1/instancias", "dry-e2/instancias"]
           + (["--amostra", "2"] if a.fumo else []),
           "runner temporal das equivalências")
    tempos = json.load(open("dryrun-tempos.json"))
    tg = tempos["t_por_grupo_segundos"]

    # Fase 3d: a fórmula congelada, e só ela
    T_equiv = ((50.0 / 3.0) * (tg["E1:I"] + tg["E1:II"] + tg["E1:III"])
               + (25.0 / 3.0) * (tg["E2:II"] + tg["E2:III"]))
    T_total = (T["classificador_E1"] + T["escala_E1"] + T["escala_E2"]
               + T_equiv)

    registo["oito_numeros"] = {
        "T_classificador_E1_s": T["classificador_E1"],
        "T_escala_E1_s": T["escala_E1"],
        "T_escala_E2_s": T["escala_E2"],
        "t_E1_I_s": tg["E1:I"], "t_E1_II_s": tg["E1:II"],
        "t_E1_III_s": tg["E1:III"],
        "t_E2_II_s": tg["E2:II"], "t_E2_III_s": tg["E2:III"],
    }
    registo["T_equiv_horas"] = T_equiv / 3600.0
    registo["T_total_horas"] = T_total / 3600.0
    passa = T_total / 3600.0 <= GATE_HORAS
    registo["gate_72h"] = ("PASSA -> Fase 4 (congelamento)" if passa
                           else "NAO PASSA -> parar; emenda pre-dados; "
                                "nenhum dado confirmatorio e gerado")
    registo["estado"] = ("PASSA_GATE_72H" if passa
                         else "NAO_PASSA_GATE_72H")
    registo["dados_confirmatorios_gerados"] = False   # fases 0-3 nunca geram
    registo["fim"] = datetime.datetime.now().astimezone().isoformat()
    nome = "registo-fases-0-3.json"
    if os.path.exists(nome):
        sys.exit(f"{nome} já existe; não sobrescrevo um registo.")
    open(nome, "w").write(json.dumps(registo, sort_keys=True, indent=1))

    print("\n========== OITO NÚMEROS (segundos) ==========")
    for k, v in registo["oito_numeros"].items():
        print(f"  {k}: {v:.2f}")
    print(f"  T_equiv:  {registo['T_equiv_horas']:.2f} h")
    print(f"  T_total:  {registo['T_total_horas']:.2f} h")
    print(f"  GATE:     {registo['gate_72h']}")
    print(f"  registo em {nome}")


if __name__ == "__main__":
    main()

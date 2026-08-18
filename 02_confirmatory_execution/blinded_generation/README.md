# Blinded generation

*Archival packaging documentation.*

The actual confirmatory instances: `conf-e1/` (150 = 50 families × System I/II/III) and `conf-e2/` (50 = 25 extended families × System II/III with downstream modules D₁, D₂), generated **once** with the confirmatory seeds (`S_E1 = 3786434918`, `S_E2 = 3786434919`) and immediately blinded (state-bit permutation + module-order permutation; anonymous `Q₀, Q₁, …` identifiers; hidden key moved out before analysis).

Each contains a `manifesto.json` (per-instance SHA-256, generation log) and an `instancias/` directory of blinded per-instance JSON transition tables. No `CHAVE-NAO-ABRIR.json` is present here — for the confirmatory generation the key was moved to `../integrity/chaves-confirmatorias/` and opened only at the prespecified scoring step, per the frozen blinding protocol.

Epistemic status: `CONFIRMATORY`.

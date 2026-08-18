# FASE 6 — AUTÓPSIA DA INSTÂNCIA 7bb0baab3a8ed7aa
**POST-CONFIRMATORY / EXPLORATORY** — Pré-registo A v8.3 (Amendments 1, 2, 3 congeladas)

> **CONFIRMATORY RESULT: NEGATIVE** — `resultado_confirmatorio_A = "negativo"`,
> fechado, imutável, não reinterpretado. Tudo neste documento é exploratório.
> Nenhuma proposta de C1″ é feita.

---

## 1. Factos (reconstrução, instrumento congelado sobre cópias)

- `7bb0baab3a8ed7aa`, família 20, variante II, Estrato 2 (n=12), órbita 25.
- Único erro de C1′ em 200 (E1 150/150; E2 49/50); C2/C3 também erram aqui.
- Erro: C1′ funde o núcleo `{A,B,C_AB,C_BA}` (estrutura de III); alvo II = singletons.
- Escala limpa; equivalências exaustivas 524288/524288 com 0 discrepâncias.
- A variante III da mesma família dá a mesma classificação do núcleo e passa.

## 2. Mecanismo observado (passos 3a/3b)

- Arestas decisivas: `C_BA->A`, `C_AB->B`. Nas 24 II corretas de E2 há ≥1 aresta
  com mudança ordinal de `d_m` entre contextos alcançados; na família 20 não há.
- Ambos os contextos de memória são alcançados; a dependência ponto-a-ponto
  existe (4608 sítios/aresta) mas o agregado de C1′ coincide em m=0 e m=1.
- Hipótese "II arquitetural mas III realizado" falsificada: restrita à órbita a
  distinguibilidade reaparece. O ponto cego é do agregado counterfactual global.

## 3. Prevalência (N=10 000 pré-fixado, 2 lotes pré-declarados)

- Por aresta (20 000): dependência ponto-a-ponto em 99,97%;
  **L1** (d₀=d₁) 3,53% · **L2** (rank igual, d≠) 1,13% · **L3** 95,35%;
  perda na agregação (L1+L2) 4,65% [IC95 4,37–4,95].
- Por instância: **P(falha de identificabilidade de C1′ | II) = 46/10 000 = 0,46%**
  [IC95 0,345–0,613]; lotes 22/5000 e 24/5000 (replicação limpa).
- Subtipos do colapso: 29×(L1,L1) · 10×(L1,L2) · 7×(L2,L2) → domina a soma de
  Hamming (L1), não o rank. fam-20 = (L1,L1).
- Consistência confirmatória: P(≥1 em 25 II de E2) ≈ 10,9%; P(0 em 50 de E1) ≈ 79,4%.
- Lema E1↔E2 (d^{E2}=4·d^{E1}) demonstrado e verificado em n=12 → a medição em
  n=10 transfere exactamente para o regime confirmatório.

## 4. CONDIÇÃO K — explicação matemática do L1 (necessária e suficiente)

### 4.1 Decomposição exacta de d_m (derivada do código congelado)
Para a aresta canal→processador na variante II (canónica), com M = G0 (aresta
`C_AB->B`, r = y) ou M = F0 (aresta `C_BA->A`, r = x):

    d_m(a) = 32 · Σ_c  W̃_m(c, sub_a(c)),
    W̃_m(c1,c2) = Σ_{r=0..3} pc2( M[r][π_m(c1)] ⊕ M[r][π_m(c2)] )

- **Lema do σ:** σ_A/σ_B cancelam em todos os XOR contrafactuais → o perfil d
  é cego ao efeito aditivo directo da memória; **a memória entra em d apenas
  através de π_m**.
- A contribuição de cada ponto da fibra depende só de (r, c); multiplicidade 32.
- **Verificação exacta:** a fórmula reproduz `d_m` da fibra em TODAS as
  30 000 arestas testadas (15 000 famílias), sem uma única discrepância.

### 4.2 O teorema
    d_0 = d_1  ⟺  W̃_0 = W̃_1  ⟺  τ := π_1∘π_0⁻¹ ∈ Iso(W_M)
    com W_M(p,q) = Σ_r pc2(M[r][p] ⊕ M[r][q])   (geometria de resposta de M)

- *Suficiência:* imediata pela fórmula.
- *Necessidade:* as 9 intervenções impõem a Δ = W̃_0−W̃_1 (simétrica, diagonal
  nula, 6 g.l.): somas-linha nulas (do(c=γ), 4 eqs) e e01+e23=0, e02+e13=0
  (bits isolados). O sistema só tem Δ=0.
- **Nível exacto da igualdade:** as respostas ponto-a-ponto DIFEREM (dep>0);
  as distâncias por r podem diferir; o primeiro nível em que m=0 e m=1
  coincidem é a soma por par de símbolos do canal, W̃(c1,c2) — e o teorema
  mostra que esse nível e a igualdade do vetor d são equivalentes.
- **Natureza do cancelamento:** τ permuta os termos da soma preservando as
  magnitudes W — *permutação isométrica dos pares*, não complementaridade nem
  coincidência de respostas individuais. "R_0 ≠ R_1 mas d_0 = σ-permutação(d_0)".

### 4.3 Teste empírico exaustivo (K vs L1)
| amostra | aresta | TP | FP | TN | FN | sens | espec | prec |
|---|---|---|---|---|---|---|---|---|
| in-sample 10 000 (replay lotes 1+2) | C_AB->B | 370 | 0 | 9630 | 0 | 1,0 | 1,0 | 1,0 |
| in-sample 10 000 | C_BA->A | 335 | 0 | 9665 | 0 | 1,0 | 1,0 | 1,0 |
| **OOS pré-comprometido** (semente 910000004, N=5000) | C_AB->B | 187 | 0 | 4813 | 0 | 1,0 | 1,0 | 1,0 |
| OOS | C_BA->A | 181 | 0 | 4819 | 0 | 1,0 | 1,0 | 1,0 |

- Equivalência `(τ ∈ Iso(W)) == K` confirmada em todas; fórmula exacta em todas.
- **K ⟺ L1 sem uma única exceção em 30 000 arestas** (15 000 famílias) +
  verificação directa na instância confirmatória (abaixo).
- Prevalência prevista = observada por construção (P_K = P_L1 em todas as
  classes e amostras); OOS: colapso_total 21/5000 = 0,42% (vs 0,46% in-sample).

### 4.4 A família 20, à luz de K (verificado na tabela CEGA, n=12)
- φ_m(r,c) bem definida na instância confirmatória (valida a redução estrutural).
- `C_BA->A`: **W̃ = matriz equidistante (todos os pares = 4)** — Iso = S₄
  completo. *Qualquer* τ é isometria: esta aresta colapsaria com QUALQUER par
  (π_0,π_1). Degenerescência máxima da geometria de resposta de F0.
- `C_AB->B`: W̃ = [[0,4,5,5],[4,0,3,3],[5,3,0,4],[5,3,4,0]] — grupo de
  isometria {id, troca de 2 símbolos}; τ acertou exactamente na única isometria
  não trivial. K verdadeiro em ambas ⇒ (L1,L1) ⇒ fusão. 

### 4.5 O que separa L1 dos controlos (propriedade mínima)
- **Classe de τ sozinha não chega:** P(L1 | transposição) ≈ 7–9%,
  P(L1 | dupla transposição) ≈ 7–9%, P(L1 | 3-ciclo) ≈ 0,7%,
  P(L1 | 4-ciclo) ≈ 0,9–1,1% — a maioria em todas as classes é L3.
  (Coerente com a contagem de restrições: 2 igualdades vs 3–4.)
- **Simetria de W sozinha não chega:** ~46% das arestas têm |Iso(W)|>1 e mesmo
  assim K falso (τ fora do grupo) → L3.
- A propriedade mínima é a **compatibilidade conjunta τ ∈ Iso(W_M)**.
  Controlos emparelhados com o MESMO τ (um L1, um L3) preservados no JSON.

### 4.6 Correlação entre arestas (o factor ~2,1–2,4×)
As duas arestas partilham o MESMO τ (o par (π_0,π_1) é único por θ), com
geometrias independentes (G0 vs F0):
- in-sample: obs P(ambas L1)=0,29% vs indep. 0,124% (razão 2,34);
  modelo de τ partilhado prevê 0,237% (razão 1,91);
- OOS: obs 0,32% vs indep. 0,135% (2,36); modelo prevê 0,26% (1,92);
- combinado: 45 eventos observados vs ~36,7 previstos pelo modelo (~1,4σ) —
  o mecanismo de τ partilhado explica o grosso da correlação; o resíduo é
  compatível com ruído/tilt de elegibilidade (E2/E6 acoplam F0,G0,π).

### 4.7 Conclusão desta etapa
    K(θ) ⟺ L1,  com  K: τ = π_1∘π_0⁻¹ é isometria da geometria de resposta
    W_M do receptor  (por aresta; M = G0 ou F0)
— demonstrada analiticamente (com necessidade via sistema linear das
intervenções), verificada sem exceção em 30 000 arestas + na instância
confirmatória cega. É uma explicação mecanística, não uma correção: nada em
C1′, targets ou artefactos foi alterado.

## 5. Classificação da falha (A–E, atualizada)

- **D (bug): descartado.** — **A (contraexemplo a C1′ como formulado): confirmado
  e agora explicado.** — **C (operacionalização): confirmado e localizado** (o
  agregado por soma de Hamming é invariante sob remapeamentos isométricos da
  geometria de resposta; o rank acrescenta a franja L2). — **B:** a classe é a
  variedade {τ ∈ Iso(W_M)}, prevalência ~0,46% por instância.

## 6. Questões em aberto (por ordem do guião da Fase 6)

1. ~~Condição algébrica mínima do L1~~ → **resolvida (secção 4)**.
2. Teste estrito em configurações realizadas em AMBOS os contextos de memória.
3. Especificidade em III (falsos positivos simétricos sob operacionalizações
   mais finas).

## 7. Ficheiros e reprodução (área `prevalencia/`)

| ficheiro | sha256 |
|---|---|
| `prevalencia_cancelamento.py` / lote 1 JSON | `48825a60…a77d` / `a4429be6…8cfc` |
| `precommit-lote2.txt` → lote 2 `.py`/JSON | — / `8d6e4133…c8fd` / `d810e581…bd4f` |
| `verifica_E1_E2.py` + `.out` | `522e5e25…3577` |
| `prevalencia-combinada-N10000.json` | `a092cb8e…3c1f` |
| `condicao_L1.py` → `condicao-L1-insample.json` | `07e17e66…37d4` → `4e2d5931…645f` |
| `precommit-oos-condicaoL1.txt` → `condicao_L1_oos.py` → `condicao-L1-oos.json` | — → `62ad08e4…1e34` → `9c1717ef…3d2c` |

Ambiente: `/root/prereg-env/bin/python` (3.14.4) + NumPy 2.5.2; instrumento de
`frozen-copy/` (12/12 vs manifesto). Tudo função pura das sementes documentadas
(910000001/2/3/4); replays determinísticos; artefactos confirmatórios intactos.

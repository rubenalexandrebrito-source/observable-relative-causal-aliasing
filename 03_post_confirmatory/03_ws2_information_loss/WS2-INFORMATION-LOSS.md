# WS2 — DECOMPOSIÇÃO DA PERDA DE INFORMAÇÃO
**POST-CONFIRMATORY / EXPLORATORY** — Pré-registo A v8.3 (Amendments congeladas), Fase 6 multiagente, workstream ws2-information-loss.

> **RESULTADO CONFIRMATÓRIO: NEGATIVO** — `resultado_confirmatorio_A = "negativo"`, fechado e imutável; C1′ 199/200
> (E1 150/150, E2 49/50); único erro: instância `7bb0baab3a8ed7aa`, família 20, variante II, Estrato 2 (n=12).
> Nada neste relatório recalcula ou reinterpreta esse resultado. **Nenhuma correção (C1″) é proposta**; diagnóstico
> mecanístico apenas. Pergunta do mandato: *em que transformação exacta da cadeia a informação causal deixa de ser
> identificável?* Cadeia analisada: respostas ponto-a-ponto → Hamming por sítio → agregação (soma na fibra) → d_m →
> rank(d_m) → estado/sinal.

**Sumário executivo.** A cadeia de agregação de C1′ perde informação em três operadores distintos e a perda que produz
L1 (d₀=d₁) fica sempre resolvida *localmente por bloco* (k,c) — nunca por compensação entre blocos (B4=0/22560; teorema).
Nas 705 arestas L1: 4,2% perdem já no popcount pontual (F_pc; equivale exactamente a τ∈∩_r Iso(w_r) — 36=29+7, 0 exceções),
24,9% perdem na invariância-a-permutações da soma (multiconjuntos por bloco iguais, sítios trocados), 70,9% perdem por
cancelamento aritmético estrito dentro de blocos (multiconjuntos diferentes, somas iguais). O vetor d é uma **bijeção
linear** de W̃ (inversão exacta, erro 0): a agregação não destrói nada além de W̃, pelo que L1 ⟺ W̃₀=W̃₁ ⟺ τ∈Iso(W)
(condição K do agente único, auditada e reconfirmada 370/335 TP, 0 FP/FN). Na franja L2, o rank destrói magnitude
cardinal com quantum 64 (E1), movimento confinado às classes estruturais {k1,k2}/{k3,k4} e bloco do(c=γ) imóvel (0/225;
demonstrado sob Δm=0). fam-20: ambas as arestas perdem no modo dominante (cancelamento por bloco), com dependência
pontual maciça (4608 sítios/aresta) — a informação existe ao nível de sítio e morre na agregação.

---

## 1. FACT

F1. Integridade: os 12 ficheiros de `frozen-copy/` têm sha256 idêntico ao `multiagent/shared-readonly/MANIFEST.txt`
(verificado antes de qualquer análise). Instrumento apenas importado; nada em `/root/causal-A-amd2-official/` tocado.

F2. Fontes (todas registadas, nenhuma amostra nova, nenhuma semente nova; intervalo atribuído 910000040..049 ficou
intacto): `prevalencia-cancelamento-II.json` (semente registada 910000001, N=5000), `-lote2.json` (910000002, N=5000),
`prevalencia-combinada-N10000.json`, cópia read-only `conf-e2/instancias/7bb0baab3a8ed7aa.json` + `chave-e2.json`
(chave aberta na Fase 5), `verifica_E1_E2.out` (lema d_E2 = 4·d_E1, módulos D inertes → análises em n=10 transferem
exactamente para E2/n=12).

F3. Procedimento desta retoma: uma tentativa anterior do WS2 ficou interrompida antes do relatório (arquivada em
`tentativa-interrompida-1/`, com o precommit original). Os seus 6 scripts foram auditados linha a linha contra as
definições congeladas, adoptados VERBATIM e **re-executados**: os 6 outputs re-gerados são byte-idênticos aos arquivados
(sha256 iguais; determinismo total). Novo precommit `precommit-ws2-v2.txt` fixado ANTES das execuções; dois scripts novos
(G: operador F; H: ponta-a-ponta) pré-declarados nele.

F4. Casos pré-comprometidos analisados ao nível de sítio (ordem dos ficheiros registados): S1 = os 46 colapso_total
(22 lote1 + 24 lote2; 92 arestas), S2 = primeiras 6 individua_ambas do lote1 (12 arestas L3), S3 = primeiras 6
individua_uma do lote1 (6 L3 + 5 L1 + 1 L2), mais fam-20 na tabela CEGA E2 (n=12). Todos os 58 thetas replayados
verificaram `theta_sha` contra o registo; 0 discrepâncias em d0/d1/dep/nível vs os JSONs registados.

F5. População (replay analítico integral dos 2 lotes registados, 10000 famílias / 20000 arestas canal→processador):
níveis L1=705 (3,53%), L2=225 (1,13%), L3=19070 (95,35%); dep>0 em 19993/20000; colapsos 46/10000 com subtipos
29×(L1,L1), 10×(L1,L2), 7×(L2,L2) — tudo igual ao registado. Confusão K vs L1 reproduzida de forma independente:
C_AB→B TP=370, C_BA→A TP=335, FP=FN=0.

F6. fam-20 (tabela cega, n=12, chave só para localizar módulos): ambas as arestas L1 com dep=4608 sítios (=36 células
(k,c,r) diferentes × multiplicidade 128, uniformidade verificada célula a célula; bit de memória do receptor nunca
responde). C_AB→B: s1=3840 sítios com pc diferente, 768 swaps; W̃=[[0,4,5,5],[4,0,3,3],[5,3,0,4],[5,3,4,0]] igual nos
dois contextos. C_BA→A: s1=3072, swaps=1536; W̃ equidistante (todos os pares=4). d₀=d₁ = [0,1024,1024,1024,1024,
1792,1280,1536,1536] e [0,1024,1024,1024,1024,1536,1536,1536,1536] respectivamente (escala E2 = 4× E1).

F7. Convenção de índices usada abaixo: k0 = intervenção nula; k1,k2 = do(bit-baixo=0/1); k3,k4 = do(bit-alto=0/1);
k5..k8 = do(c=0..3) — a ordem exacta de `cl.intervencoes` num canal de 2 bits. Fibra n=10: 512 sítios = 16 células
(c,r) × 32; r = estado não-memória do receptor (y para C_AB→B, x para C_BA→A).

## 2. DERIVATION

D1. **Forma fechada do campo de respostas (S0).** Pela dinâmica congelada (passo II), sob intervenção k que substitui
o canal c por c₂=sub_k(c), a resposta do receptor no sítio z=(c,r,resto) é
`X_m[k][z] = M[r][π_m(c)] ⊕ M[r][π_m(c₂)]`, com M=G0 (aresta C_AB→B, r=y) ou M=F0 (C_BA→A, r=x); σ_A/σ_B cancelam em
todos os XOR; o bit de memória do receptor (m_B′=K[m_B][y], m_A′=H[m_A][x]) não depende do canal e nunca responde.
O campo é constante em cada célula (k,c,r); multiplicidade 32 (E1) / 128 (E2). [Verificação: sítio a sítio contra a
tabela congelada, 116 arestas × 9 k × 512 sítios × 2 contextos ≈ 1,07M comparações, 0 falhas; em E2 a constância por
célula com mult. 128 foi verificada na própria tabela cega.]

D2. **Os operadores da cadeia.** Com w_r(p,q) := pc2(M[r][p]⊕M[r][q]) e W(p,q) := Σ_r w_r(p,q) (geometria de resposta
de M), e W̃_m(c₁,c₂) := W(π_m c₁, π_m c₂):
- F_pc (S0→S1): padrão → popcount por sítio. Em padrões de 2 bits as fibras de pc2 são {00},{01,10},{11}: a ÚNICA
  identificação não trivial é 01↔10 — troca de papel dos dois bits não-memória do receptor.
- F_hist (S1→S1.5): campo → multiconjunto por intervenção (invariância a permutações de sítios).
- F_Σ (S1.5→S2/S3): soma na fibra. A soma de cada bloco (k,c) é 32·W̃_m(c,sub_k(c)); d_m[k] = 32·Σ_c W̃_m(c,sub_k(c)).
- F_rank (S3→S4): rank_canonico (ordem fraca densa com empates); decisão estado/sinal = igualdade dos ranks nos dois
  contextos de memória; o núcleo funde sse AMBAS as arestas canal→processador ficam «estado».

D3. **Empates estruturais (T1).** d[k0]=0 sempre. Para o bit b: as intervenções do(b=0) e do(b=1) somam sobre o MESMO
par não-ordenado de símbolos {c,c⊕b} ⇒ `d[k1]=d[k2] = 32·(W̃(0,1)+W̃(2,3)) =: 32·m1` e `d[k3]=d[k4] = 32·(W̃(0,2)+W̃(1,3))
=: 32·m2`. O vetor d tem no máximo 6 graus de liberdade: (m1, m2, rs_0..rs_3), rs_γ := Σ_c W̃(c,γ) = d[5+γ]/32.
[Verificado: 39295 vetores, 0 falhas.]

D4. **Bijeção linear d ↔ W̃ (T2).** O sistema (m1, m2, rs_γ) inverte-se exactamente para os 6 valores de pares:
Σ=(Σ_γ rs_γ)/2, m3=Σ−m1−m2, e01=(rs_0+rs_1−m2−m3)/2, e23=m1−e01, e02=(rs_0+rs_2−m1−m3)/2, e13=m2−e02,
e03=(rs_0+rs_3−m1−m2)/2, e12=m3−e03. **A agregação não perde nada além de W̃**: d determina W̃ e vice-versa.
Corolário (necessidade da condição K, por inversão explícita): d₀=d₁ ⟺ W̃₀=W̃₁ ⟺ τ:=π₁∘π₀⁻¹ ∈ Iso(W). Em particular
**B4=0 é teorema**: numa aresta L1 toda a soma de bloco coincide; compensação entre blocos no total NUNCA é o mecanismo
de L1. [Verificado: inversão com erro máximo 0.0 em 1392 valores; B4=0 em 22560/22560 blocos de arestas L1.]

D5. **Lema das somas-linha (bloco do(c=γ)).** d_m[5+γ] = 32·R(π_m γ), R(q):=Σ_p W(p,q) ⇒ o bloco completo do contexto 1
é a permutação ρ = π₀⁻¹τπ₀ do bloco do contexto 0. Corolários exactos, válidos em TODAS as arestas (mesmo L3):
multiset{d[5..8]} e Σ d[5..8] são invariantes entre contextos. Sob Δm1=Δm2=0, uma troca não trivial de valores
distintos no bloco completo altera o rank denso ⇒ L2 exige bloco completo pontualmente fixo. [Verificado: 0 violações
dos invariantes em 20000 arestas; bloco movido pontualmente: L2 0/225, L3 17448/19070.]

D6. **Paridade (quantum 64).** pc2(a⊕b) ≡ pc2(a)+pc2(b) (mod 2) ⇒ W̃_m(c₁,c₂) ≡ P(π_m c₁)+P(π_m c₂) (mod 2), com
P(p):=Σ_r pc2(M[r][p]). Daí m1_m ≡ m2_m ≡ Σ_p P(p) (mod 2) e R(q) ≡ Σ_p P(p) (mod 2) — todos invariantes de contexto ⇒
**toda a componente de Δd é múltipla de 64** (E1; 256 em E2). [Verificado: 84022 componentes não nulas, 0 violações;
distribuição |Δ|: 64→51514, 128→23965, 192→7010, 256→1360, 320→152, 384→21.]

D7. **Hierarquia de invariância de τ e estágios de perda (L1).** As 9 intervenções realizam todos os 16 pares (c₁,c₂)
(k5..k8 são do(c=γ) completos). Logo:
- s1=0 (pc pontual igual em todo o sítio) ⟺ w_r(τp,τq)=w_r(p,q) ∀r,p,q ⟺ **τ ∈ ∩_r Iso(w_r)**;
- todos os blocos ≤B2 (multiconjuntos por bloco iguais) ⟺ τ preserva o perfil-multiconjunto {w_r(p,q)}_r de cada par;
- L1 ⟺ τ ∈ Iso(Σ_r w_r) = Iso(W) (condição K).
Três classes encaixadas ∩_r Iso(w_r) ⊆ Iso_multiset ⊆ Iso(W); o estágio de perda é o primeiro nível da cadeia em que a
igualdade se instala. [Verificação de D7(i): equivalência exacta nas 705 arestas L1 — 36 = 29 (F1_pc_pontual) + 7
(dep=0), 0 contra-exemplos nos dois sentidos.]

D8. **Fibra da ordinalização.** Para um padrão de rank com t valores distintos, o nº de vetores d na grelha
{0,32,...,1024}⁹ que o realizam é C(33,t) (contagem teórica; a fibra observada é muito menor por D3-D6).

## 3. EMPIRICAL SUPPORT

E1. **Estágios de perda nas 705 arestas L1** (população registada, replay analítico validado sítio-a-sítio nos casos):
`F1_pc_pontual` 29 (4,2% das 698 com dep>0) · `F1.5_histograma` 174 (24,9%) · `F2_soma_por_bloco` 495 (70,9%) ·
`F2_global_INESPERADO` 0 · dep=0: 7. Censo de blocos (k,c) em L1 (22560 blocos não nulos): B0 12604 (55,9%), B1 616
(2,7%), B2 4728 (21,0%), B3 4612 (20,4%), **B4 0**. Por (aresta,k) não nulo (5640): campo idêntico 854 (15,1%);
pc pontual igual 224 (4,0%); histograma igual 2650 (47,0%); igual SÓ na soma 1912 (33,9%); soma desigual 0.

E2. **Refinamentos.** (i) TODAS as 174 arestas F1.5 têm todos os blocos ≤B2 — 0 casos de multiconjunto-por-bloco
diferente compensado entre blocos no histograma global. (ii) Nas 495 F2, 459 (92,7%) têm ≥1 intervenção com histograma
global igual à custa de compensação ENTRE blocos (mas a soma iguala sempre bloco a bloco, D4). (iii) Distribuição por
aresta F2 do nº de intervenções que só igualam na soma: 2→136, 4→258, 5→4, 6→93, 7→2, 8→2 (paridade dominante par —
consequência dos empates estruturais D3). (iv) |∩_r Iso(w_r)| nas L1: 1→609, 2→78, 4→17, 8→1.

E3. **Casos (nível de sítio, enumeração pela tabela congelada).** 92 arestas dos 46 colapsos: 68 L1 (3 F1 · 19 F1.5 ·
45 F2 · 1 dep=0) + 24 L2. Controlos: 12/12 L3 (individua_ambas); individua_uma: 6 L3 + 5 L1 + 1 L2. A única aresta
dep=0 dos casos: seed 910000001, fam 4159, C_AB→B (colapso com uma aresta sem QUALQUER dependência pontual entre
contextos). Médias de sítios por aresta (máx 4608 = 9×512): dep L1 1290 / L2 1485 / L3 1695; s1 (pc diferente)
L1 1058 / L2 1175 / L3 1410 — **a massa de sinal pontual em L1 é da mesma ordem da de L3**.

E4. **Testemunhas concretas X₀≠X₁ → F(X₀)=F(X₁)** (extraídas analiticamente dos thetas replayados):
- B1 (fam 380, C_BA→A, célula k1,c=1,r=1): X₀=`10`, X₁=`01` — bits trocados, pc=1 em ambos. F_pc destrói a identidade
  do bit que responde.
- B2 (fam 380, C_AB→B, bloco k1,c=1): pc por r: m0=[0,1,2,0] vs m1=[2,0,1,0] — multiconjunto {0,0,1,2} igual,
  posições trocadas. F_hist/F_Σ é cega à localização (que r transporta que distância).
- Histograma global igual com 160 sítios pontualmente diferentes (fam 380, C_AB→B, k1): hist [352,128,32] idêntico
  nos dois contextos; d=192.
- B3 (fam 289 — o exemplar; C_AB→B, bloco k1,c=3): pc por r: m0=[1,2,0,0] vs m1=[0,1,1,1] — multiconjuntos
  {0,0,1,2}≠{0,1,1,1}, somas 3=3. Um sítio-2 e um sítio-0 trocados por dois sítios-1: **cancelamento aritmético puro**.
  No histograma global do mesmo k: [384,96,32] vs [352,160,0], d₀=d₁=160 (32 sítios de peso 2 → 64 sítios de peso 1).
- L2 (fam 1910, C_BA→A): d₀=[0,256,256,320,320,576,448,448,448] → d₁ muda SÓ a classe {k3,k4}: 320→384 (Δ=+64);
  rank comum [0,1,1,2,2,4,3,3,3]; a classe movida fica a 64 do vizinho seguinte (448). F_rank destrói a magnitude
  dentro da célula de ordem.
- Exemplar completo (fam 289, C_AB→B, L1/F2): dep=2048, s1=2048, swap=0; Δpc por sítio: −1×1024, +1×1024, 0×2560;
  d₀=d₁=[0,160,160,160,160,288,160,224,288]; blocos B0 20 · B2 8 · B3 8 · B4 0; τ=(3,1,2,0), K verdadeiro.

E5. **L2 — o que o rank destrói (225 arestas).** Componentes mudadas SEMPRE dentro das classes estruturais:
{k1,k2} 96 · {k3,k4} 97 · {k1..k4} 32; bloco do(c=γ) imóvel 225/225. |Δ| por componente (514): 64→412 (80,2%),
128→88, 192→12, 256→2. Classes de empate movem-se em bloco (988 classes, 0 violações); margem mínima pós-movimento:
64 em 208 arestas, 128 em 17. Tamanhos de classes de empate: 1→346, 2→402, 3→109, 4→109, 5→20, 6→2; t (valores
distintos) 3→2, 4→133, 5→90. Fibra da ordinalização: global 403 padrões ← 4895 vetores distintos (≤52 por padrão);
nas L2: 51 padrões, 140 pares (d₀,d₁) distintos, ≤8 vetores observados por padrão; teórico C(33,t) (ex.: t=4 → 40920).
Contraste L3 (19070): mudança mista 17002, só inversões 1228, só empates 840; 2..8 componentes mudadas; bloco completo
movido em 91,5%. Atenuação (Σ|Δd| / sítios s1): L1 = 0 exacto, L2 0,153, L3 0,300.

E6. **fam-20 na tabela cega (n=12).** Ambas as arestas L1, estágio `F2_soma_por_bloco`, mult. 128 uniforme, bit de
memória mudo: C_AB→B blocos B0 20 · B2 6 · B3 6, histogramas globais desiguais em k∈{3,4,7,8}; C_BA→A blocos B0 20 ·
**B3 12**, desiguais em k∈{1,2}; Δpc por sítio: C_AB→B {−2:512, −1:1280, +1:1792, +2:256}, C_BA→A {−1:1536, +1:1536}.
W̃ reconstruído dos dados de sítio = o da autópsia (auditoria independente): C_BA→A equidistante (Iso=S4, qualquer τ
colapsa esta aresta); C_AB→B com Iso={id, uma transposição} e τ é essa transposição. Ranks comuns [0,1,1,1,1,4,2,3,3]
e [0,1,1,1,1,2,2,2,2].

E7. **Ponta-a-ponta (classificador congelado, `cl.classificar`).** (1) Primeira família colapso_total do lote1
(fam 289, órbita 8), reconstrução canónica II/n=10: C1′ funde {A,B,C_AB,C_BA}. (2) Controlo individua_ambas (fam 0,
órbita 28): sem fusão. (3) Instância confirmatória cega (órbita 25): funde {A,B,C_AB,C_BA} — reprodução do erro
conhecido, sem reinterpretação. Tudo conforme o precommit.

E8. **Verificações agregadas.** Reprodução byte-idêntica dos 6 outputs da tentativa interrompida (sha256 iguais);
58/58 theta_sha dos casos; 126/126 theta_sha dos exemplos registados na população e 252/252 concordâncias de
dados por aresta; 0 falhas na verificação sítio-a-sítio; T1 0/39295 falhas; T2 erro 0.0/1392; T3 0 falhas;
corolários D5 0 violações/20000; K vs L1 370+335 TP, 0 FP, 0 FN.

## 4. INFERENCE

I1. **Resposta ao mandato — onde morre a informação.** Para L1, a identificabilidade NÃO morre nas respostas
ponto-a-ponto (dep>0 em 698/705; médias ~1290 sítios) nem «na cadeia inteira por acumulação difusa»: morre em
operadores identificáveis, sempre resolvida ao nível do bloco (k,c):
- **modo B1 — F = pc2 por sítio** (29 arestas + 7 dep=0): os multiconjuntos coincidem porque cada sítio já coincide
  em contagem; a única informação destruída é QUAL bit responde (01↔10). Condição exacta: τ ∈ ∩_r Iso(w_r).
- **modo B2 — F = invariância-a-permutações da soma** (174): os valores de Hamming existem e diferem sítio a sítio,
  mas o multiconjunto por bloco (e por consequência o histograma por intervenção) é o mesmo; destrói-se a LOCALIZAÇÃO
  (que célula r transporta que distância). Sem QUALQUER compensação entre blocos neste modo (0/174).
- **modo B3 — F = soma aritmética** (495, o dominante, 70,9%; 45/68 das arestas L1 dos colapsos; fam-20 nas duas
  arestas): até os multiconjuntos diferem; apenas as somas por bloco coincidem (trocas do tipo {2,0}↔{1,1});
  histogramas globais podem até diferir por k e compensar entre blocos (459/495), mas a soma iguala bloco a bloco.
- **nunca no total global**: B4=0 é teorema (D4) — a igualdade de d nunca precisa de compensação entre blocos.

I2. **A agregação é isomorfa a W̃** (D4): d₀=d₁ ⟺ W̃₀=W̃₁ ⟺ τ∈Iso(W). A «perda na agregação» de C1′ é exactamente o
quociente do campo de respostas pela geometria de resposta W̃ — os três modos B1/B2/B3 dizem apenas QUÃO ABAIXO de W̃
a distinção microscópica sobrevive antes de ser apagada. A condição K do agente único fica assim auditada e refinada
numa filtração: ∩_r Iso(w_r) (36) ⊂ Iso_multiset (36+174=210) ⊂ Iso(W) (705).

I3. **L2 — F = rank_canonico.** A ordinalização destrói magnitude cardinal com quantum 64 e amplitude ≤256 (E1),
com movimento CONFINADO às classes estruturais {k1,k2} e {k3,k4} (m1/m2); o bloco do(c=γ) é imóvel (0/225; teorema sob
Δm=0 via lema das somas-linha). O rank sobrevive por margem mínima de um quantum (64) em 92% das arestas L2. Os empates
que o tornam possível são em parte ESTRUTURAIS (D3: k1=k2, k3=k4 sempre; k0=0), pelo que o perfil de 9 componentes tem
≤6 graus de liberdade efectivos — a ordem fraca é mais colapsável do que o comprimento 9 sugere.

I4. **fam-20 enquadrada.** O único erro confirmatório é um caso do modo dominante (B3/F2 nas duas arestas), com
dependência pontual máxima observada por célula (36 células/aresta) e assinatura de troca {2,0}↔{1,1} e ±1/∓1 nos
sítios. A aresta C_BA→A tinha geometria maximamente degenerada (W equidistante — qualquer τ a colapsaria); a C_AB→B
exigiu o acerto de τ na única isometria não trivial. Nada na instância é atípico do mecanismo populacional.

I5. **Hierarquia de robustez implícita no instrumento congelado** (leitura diagnóstica, não prescritiva): a informação
que sobrevive até d é W̃; a que sobrevive até ao veredicto é rank(d). As 225 L2 mostram que o passo cardinal→ordinal
custa 24% dos colapsos de aresta (225/930) e os 46 colapsos de instância repartem-se 29 (L1,L1) / 10 (L1,L2) / 7 (L2,L2)
— o mecanismo de soma (L1) domina, o ordinal alarga a franja.

## 5. SPECULATION

S1. O domínio do modo B3 (70,9%) é plausivelmente volumétrico: a igualdade de somas é a restrição mais fraca da
filtração (fibra maior em espaço de θ), enquanto τ∈∩_r Iso(w_r) exige preservar 4 geometrias de linha em simultâneo
(apenas 96/705 arestas L1 têm sequer |∩_r Iso(w_r)|>1). Não foi feita contagem formal de volume.

S2. dep=0 ocorreu só com τ de tipo 2×2 (7/7), e os modos F1 concentram-se em τ de ordem 2 (29/29 em 1x1x2 ou 2x2);
especulativamente, involuções alinham-se mais facilmente com simetrias exactas de M ao nível de linha. As classes de
τ nas F2 incluem 3-ciclos e 4-ciclos, coerente com K ser a única condição operante ao nível da soma.

S3. A imobilidade do bloco do(c=γ) em L2 sem a hipótese Δm=0 (não demonstrada aqui) sugere que perfis com bloco
completo permutado e m1/m2 compensantes são possíveis em princípio mas de medida ínfima; se existissem, seriam L2
«exóticos» com mudança no bloco completo — 0 observados em 225.

S4. A degenerescência equidistante de W (fam-20, C_BA→A) é um atributo só de M=F0 (pré-π): especulativamente há uma
classe de matrizes M «planas» cuja geometria de resposta não separa símbolos, tornando a aresta vulnerável a QUALQUER
par (π₀,π₁); a prevalência dessa classe em θ elegíveis não foi medida neste WS (fica para o censo de geometrias).

## 6. QUESTÕES ABERTAS

Q1. Demonstrar (ou refutar) sem a hipótese Δm=0: «L2 ⇒ bloco do(c=γ) pontualmente fixo» (aqui: teorema parcial + 0/225).
Q2. Demonstrar ou delimitar «histogramas globais iguais em todos os k ⇒ todos os blocos ≤B2» (aqui: 174/174 empírico;
a compensação entre blocos existe ao nível do histograma DENTRO de arestas F2 — porquê nunca em todos os k?).
Q3. Censo populacional das geometrias degeneradas: prevalência de |Iso(w_r)| e |∩_r Iso(w_r)| não triviais e de W
equidistante em θ elegíveis (aqui só medido dentro das L1), e o seu acoplamento com E2/E6 (resíduo ~1σ do factor ~2,3×
entre arestas, cf. agente único).
Q4. Caracterização algébrica fechada da condição de dep=0 (identidade de padrões M[r][π₀c₁]⊕M[r][π₀c₂] =
M[r][π₁c₁]⊕M[r][π₁c₂] ∀r,c₁,c₂) e a sua relação exacta com τ 2×2 (7/7 aqui).
Q5. Distribuição teórica das margens L2. Entre componentes não nulas, «múltipla de 64» segue de D6 (todas partilham a
paridade Σ_p P(p) em unidades de 32); a margem envolvendo a classe nula (k0=0) não está coberta por esse argumento e
mesmo assim nunca foi <64 (0/225) — falta a razão; e que estrutura de W produz as margens 128 (17/225)?

## 7. FICHEIROS E REPRODUÇÃO

Área (única com escrita): `/root/causal-A-postconfirmatory-analysis/multiagent/ws2-information-loss/`.
Pipeline (ordem): `precommit-ws2-v2.txt` (fixado antes) → `ws2_a_replay_cases.py` → `ws2_b_sitelevel_cases.py` →
`ws2_c_population.py` → `ws2_d_fam20.py` → `ws2_e_ordinal.py` → `ws2_f_teoremas.py` → `ws2_g_operator.py` →
`ws2_h_endtoend.py`; outputs `ws2-*.json` + logs `ws2_[a-h].out`; arquivo da tentativa interrompida em
`tentativa-interrompida-1/` (byte-idêntica na re-execução). SHAs de todos os ficheiros: `SHAS.txt`.
Ambiente: `/root/prereg-env/bin/python` (3.14.4, NumPy 2.5.2); instrumento `frozen-copy/` 12/12 vs MANIFEST.
Execução: `cd <ws2 dir> && PYTHONDONTWRITEBYTECODE=1 /root/prereg-env/bin/python <script>.py`. Nenhuma amostra nova;
nenhuma semente consumida; artefactos confirmatórios intactos.

*Rótulo em todos os ficheiros deste WS: POST-CONFIRMATORY / EXPLORATORY. O resultado confirmatório permanece NEGATIVO e
intocado; nenhuma regra alternativa a C1′ foi procurada ou proposta.*

# WS4 — ESPECIFICIDADE NA CLASSE III

**POST-CONFIRMATORY / EXPLORATORY** — Pré-registo A v8.3, Fase 6 multiagente.
Workstream: `ws4-classIII-specificity`. Data: 2026-08-17.
Versão: 2.ª passagem (integra a 1.ª passagem desta área — relatório anterior
sha256 `f9cd27a459ee276b0ddad0bba6364d5c4b3588d540e40761f3ea64c151b9b0a3` —
mais a auditoria da mesma e a extensão pré-comprometida de horizonte 2).

**REAFIRMAÇÃO DO RESULTADO CONFIRMATÓRIO (fechado, imutável):**
`resultado_confirmatorio_A = "negativo"`. C1' obteve 199/200 (E1 150/150,
E2 49/50); único erro: instância `7bb0baab3a8ed7aa`, família 20, variante II,
Estrato 2 (n=12). Nada neste relatório recalcula, reinterpreta ou reabre esse
resultado. Este documento é diagnóstico mecanístico exploratório; não propõe
C1'', não propõe correcção, não propõe regra de decisão nem threshold.

**Pergunta do mandato:** observando a causalidade à maior resolução
(ponto-a-ponto, Hamming, d_m, ranks), sistemas III VERDADEIROS apresentam
alguma estrutura que pudesse ser confundida com SINAL? E: recuperar a
informação perdida em II poderia, EM PRINCÍPIO, introduzir ambiguidade do
lado de III?

**Resposta em duas frases.** (1) Ao estatístico congelado — funcionais do
campo de resposta XOR a intervenções sobre fibra completa com UMA aplicação
da transição — um III verdadeiro é EXACTAMENTE nulo: P(dependência de
memória | III) = 0 por teorema, 0/4000 arestas empiricamente; a fusão do
núcleo em III é determinística e correcta. (2) Essa segurança é uma
propriedade de gume de faca do horizonte 1: a memória de um III é
causalmente ACTIVA nos baselines (100% dos pontos, 100% das arestas), na
composição de visitação da órbita (100% das órbitas) e — resultado novo da
2.ª passagem — no MESMO estatístico XOR-intervencional em fibra completa
aplicado à transição iterada T∘T, onde 99,90% das arestas de III exibem
dependência de memória genuína com magnitudes da ordem das de um II
verdadeiro a horizonte 1; recuperação de informação que saia do horizonte 1
ou da classe XOR-em-fibra-completa pode portanto, em princípio, introduzir
ambiguidade do lado de III.

---

## FACT

Factos verificados nesta área (fontes: instrumento congelado, datasets
exploratórios existentes — nunca editados —, medições pré-comprometidas
desta área, e auditoria da 2.ª passagem).

**F1. Integridade.** `sha256sum frozen-copy/*.py` coincide com as 12 linhas
correspondentes de `multiagent/shared-readonly/MANIFEST.txt` (12/12;
reverificado na 2.ª passagem). `SHAS.txt` da 1.ª passagem verificou 8/8
antes de qualquer acção da 2.ª. Nenhum ficheiro fora desta área ws foi
escrito; nada foi editado fora dela.

**F2. Semântica congelada do passo III** (`gerador.step_III`, canónico n=10;
bit0-1=x, bit2=mA, bit3-4=y, bit5=mB, bits6-7=cAB, bits8-9=cBA):
`x' = F0[x][cBA] ^ sigmaA[mA]; mA' = H[mA][x]; y' = G0[y][cAB] ^ sigmaB[mB];
mB' = K[mB][y]; cAB' = x; cBA' = y`. Sem pi: a interface é directa. A
semântica intervencional congelada do classificador é "substituir bits e
aplicar UMA transição global" (docstring de `classificador.py`).

**F3. Procedência das medições.**
- 1.ª passagem: `precommit-ws4-classIII-especificidade.txt` depositado às
  13:33 UTC, ANTES da execução (~13:35-13:36 UTC), com as previsões P1-P8
  derivadas antes de medir, N=2000 e semente 910000020 fixados (intervalo
  WS4; distinta das confirmatórias e das 20 queimadas). Fluxo idêntico ao
  `gerar_lote`: `SeedSequence(910000020).spawn(4)[0]` → PCG64; rejeitar
  `pi0==pi1`; aceitar sse `elegibilidade(th, False)[0]`. 2000 aceites em
  6952 tentativas (taxa 0,288). Instâncias canónicas III via
  `tabela_transicao("III", th, False)`; maquinaria de análise = funções
  congeladas de `classificador.py` (`extractor`, `popcount_tab`,
  `intervencoes` — 9 por canal, incluindo a nula —, `estados_da_fibra`,
  `rank_canonico`). Execução única, 4,8 s, sequencial.
- 2.ª passagem: `precommit-ws4-adenda-h2-auditoria.txt` depositado às
  14:28 UTC, ANTES das execuções da adenda (auditoria 0,1 s; horizonte 2
  4,9 s), com o Teorema III-2 e as previsões PH1-PH4 enunciados antes de
  medir. NENHUMA semente nova: a corrente 910000020 foi reproduzida
  deterministicamente (identidade verificada: theta_sha e tentativa iguais
  em 2000/2000 famílias) e o replay 910000001 tocou apenas famílias
  REGISTADAS do dataset existente. Sem multiprocessing em parte alguma.

**F4. Resultados da medição de horizonte 1 (1.ª passagem; 2000 instâncias
III, 4000 arestas canal→processador; `ws4-classIII-medicao.json`):**

| Previsão (enunciada antes) | Resultado |
|---|---|
| P1 dep_sites = 0 | **4000/4000** arestas (dep>0: 0) |
| P2 d0==d1 entrada-a-entrada; nível L1 | **4000/4000**; L2: 0; L3: 0 |
| P3 forma fechada d = 32·Σ_c W_M(c,sub(c)) | exacta em **4000/4000** (ambos os m) |
| P4 C2-eficácia igual entre contextos; C3-suporte igual | **4000/4000** e **4000/4000** |
| P5 bdep (baseline alinhado) = previsto; sigmaR[0]≠sigmaR[1] | **4000/4000**; bdep=512 (saturado) em **4000/4000**; sigma_diff em 4000/4000 |
| P6 ambos os contextos de memória alcançados na órbita | **4000/4000** |
| P7 factorização S_m = Σ Cnt_m·resp (Teorema III-1 na órbita) | **4000/4000**; Cnt_0==Cnt_1: **0/4000**; S_0==S_1: **0/4000**; perfis normalizados iguais: **0/4000** |
| Sanidade: max(d0)=0 (canal ineficaz) | 0/4000 |
| Anomalias (qualquer previsão falhada) | **0** |

Órbitas: comprimento 5-71 (mediana 20). delta_norm (máx. sobre intervenções
de |S_0/|V_0| − S_1/|V_1||): mediana ≈ 0,53 (C_AB→B) / 0,55 (C_BA→A)
bits/estado, p90 ≈ 1,0, máx 2,0; zeros: 0/2000 em cada aresta.

**F5. Auditoria da 1.ª passagem (2.ª passagem, adenda A;
`ws4-auditoria-2a.json`): 0 falhas em todas as comparações.**
- A1 (reprodução determinística): as primeiras 25 famílias da corrente
  910000020 reproduzem exactamente tentativa, theta_sha e, por aresta
  (50 arestas), dep_sites, nivel, bdep, V0, V1; e os 6 exemplos preservados
  reproduzem d0/d1 integrais.
- A2 (validação end-to-end do dep em regime NÃO-nulo — em III o dep é 0 por
  teorema, logo a 1.ª passagem nunca exercitara dep>0): replay das famílias
  REGISTADAS do lote 1 (semente registada 910000001): fam 0 (tentativa 9,
  individua_ambas) e fam 289 (tentativa 1003, colapso_total); theta_sha
  exactos; dep_sites reproduzidos exactamente (2176/2176 e 2048/1536);
  níveis idênticos (L3/L3 e L1/L1); d0/d1 do colapso idênticos. A fórmula
  prévia do agente único com pi (d_m = 32·Σ_c W̃_m(c,sub(c)),
  W̃_m(c1,c2)=Σ_r pc2(M[r][pi_m(c1)]^M[r][pi_m(c2)])) verificou exacta nas
  4 arestas replayadas — auditoria da derivação prévia no caso pi0≠pi1,
  complementar à auditoria P3 (caso degenerado pi=id, 4000/4000).
- A3 (recontagem independente do contraste): todos os agregados de
  `ws4-contraste-II.json` reproduzidos (46 colapsos, 92 arestas, min=0,
  mediana=1152, máx=2048, 1 aresta dep=0, 45/46 com ambas dep>0, 7 arestas
  dep=0 no agregado 4+3).

**F6. Datasets existentes (leitura apenas; `ws4-contraste-II.json`).**
No agregado II N=10000 (sementes 910000001/910000002, alheias): 20000
arestas, L1=705, L2=225, L3=19070; dep ponto-a-ponto presente em
19993/20000 (7 arestas com dep=0); 46 instâncias colapso_total (subtipos
29 (L1,L1), 10 (L1,L2), 7 (L2,L2)). Nas 92 arestas dos 46 colapsos:
dep_sites min=0, p25=1024, mediana=1152, p75=1536, máx=2048; exactamente
**1** aresta de colapso com dep=0 (theta_sha 964a55337a7a502f, C_AB→B, L1);
**45/46** colapsos têm AMBAS as arestas com dep>0. As restantes 6 arestas
dep=0 do agregado estão fora do conjunto de colapsos. Referência fam-20
(confirmatória, n=12): dep=4608 em cada aresta, com d0==d1 =
[0,1024,1024,1024,1024,1792,1280,1536,1536] (C_AB→B) e
[0,1024,1024,1024,1024,1536,1536,1536,1536] (C_BA→A).

**F7. Lema de transferência** (`verifica_E1_E2.out`, existente): d_E2 =
4·d_E1, mesmos ranks, mesmos níveis, dep_E2 = 4·dep_E1 (módulos D inertes
para os extractores dos receptores) → análises em n=10 transferem
exactamente ao regime confirmatório E2 (n=12); consistente com fam-20:
4608 = 4×1152.

**F8. Elegibilidade e estrutura de memória.** A elegibilidade congelada
avalia E1-E5 na órbita de CADA variante (I, II, III) e E6 na II
(`gerador.elegibilidade`): em toda a família elegível, a órbita III alcança
ambos os valores de mA e mB (E1(III)) e ≥2 valores de sigma (E5(III)) —
logo sigmaA[0]≠sigmaA[1] e sigmaB[0]≠sigmaB[1] SEMPRE. Distribuição
empírica de `mem_rows_dif` (nº de posições em que as duas linhas de K —
resp. H — diferem), sobre as 4000 arestas da amostra: 0:247, 1:1001,
2:1477, 3:1051, 4:224.

**F9. Resultados de horizonte 2 (2.ª passagem, adenda B; MESMAS 2000
famílias; estatístico exploratório T2=T∘T com a mesma maquinaria congelada;
`ws4-horizonte2.json`):**

| Previsão (enunciada antes) | Resultado |
|---|---|
| PH1 dep2>0 na maioria das arestas | **3996/4000** (99,90%; IC95 CP [0,99744, 0,99973]) |
| PH1 por instância (≥1 aresta) | **2000/2000** (IC95 [0,99816, 1]) |
| PH1 por instância (ambas as arestas) | **1996/2000** (99,80%; IC95 [0,99489, 0,99946]) |
| PH2 forma fechada d2 = 8·Σ_{o,r,c}[…] (Teorema III-2) | exacta em **4000/4000** (ambos os m) |
| PH3 níveis a h2 (d2_0 vs d2_1) | L3: 3334 (83,4%); L2: 632 (15,8%); L1: 34 (0,85%) |
| PH4 magnitudes dep2 | mediana 1312/1344 por aresta, p25 1088, p75 1536, máx 2176; mínimo >0 = 160 |
| Corrente idêntica à 1.ª passagem | **2000/2000** theta_sha+tentativa |
| Anomalias | **0** |

**F10. Os 4 casos dep2=0 (caracterização, prevista no precommit PH1):**
fam 968 (C_BA→A), fams 1323, 1912, 1970 (C_AB→B); todos com nivel2=L1,
sigma_diff=true e `mem_rows_dif=4` — as duas linhas de K (resp. H) diferem
nas 4 posições, i.e., linha 1 = complemento bit-a-bit da linha 0 (taxa base
de mem_rows_dif=4 na amostra: 224/4000 ≈ 5,6%). **0/2000** instâncias têm
AMBAS as arestas com dep2=0. Das 34 arestas L1 a h2, 4 são nulidade pontual
(dep2=0) e 30 são cancelamento agregado (dep2>0 com d2_0==d2_1) — o análogo
a h2 do fenómeno L1 do lado II a h1.

---

## DERIVATION

Derivações exactas a partir das definições congeladas. (D1-D5 enunciadas no
precommit da 1.ª passagem; D6-D7 no da adenda — sempre ANTES das medições
correspondentes; as medições são guardas de implementação.)

**D1. Teorema III-1 (invariância pontual à memória, horizonte 1).** Aresta
C_AB→B (canal a=[6,7], receptor b=[3,4,5], memória do receptor mB=bit5).
Ponto z da fibra com mB=m; extractor eB(T[z]) = y'(z) | (mB'(z)<<2).
Intervenção (mk,vl) ⊆ bits do canal substitui cAB por sub(cAB)=(cAB&~mc)|vc
e não toca x, mA, y, mB, cBA. Então:

    xr(z) = eB(T[z_int]) ^ eB(T[z])
          = [(G0[y][sub(cAB)]^sigmaB[m]) ^ (G0[y][cAB]^sigmaB[m])] | [(K[m][y]^K[m][y])<<2]
          = (G0[y][sub(cAB)] ^ G0[y][cAB]) | 0.

sigmaB[m] cancela no XOR; K[m][y] cancela porque a intervenção no canal não
altera y no estado corrente. Logo xr(z) depende APENAS de (y, cAB) e da
intervenção — não de m, nem de x, mA, cBA. Como `estados_da_fibra` alinha
Z0 e Z1 pela mesma enumeração dos 9 bits livres, os vectores de resposta
são iguais entrada a entrada entre m=0 e m=1. Simétrico na C_BA→A com
(x, cBA), F0, sigmaA, H. A prova usa só as equações do passo, não usa n:
em Estrato 2 os bits D são bits livres adicionais da fibra e não entram em
eB (multiplicidade ×4; consistente com F7). ∎

**D2. Corolários (probabilidade 1 sobre theta elegível).**
(i) dep_sites ≡ 0 nas duas arestas canal→processador: **P(dependência de
memória de alta resolução | III) = 0** — afirmação analítica, não
estatística. (ii) d_0 ≡ d_1 entrada a entrada ⇒ nível L1 sempre ⇒ C1'
marca 'estado' em ambas as arestas ⇒ o núcleo A→C_AB→B→C_BA→A funde SEMPRE
em III — comportamento correcto para a classe; a fusão é determinística,
não um evento de amostragem. (iii) Forma fechada: d_m(mk,vl) =
32·Σ_{c=0..3} W_M(c, sub(c)), W_M(p,q) = Σ_{r=0..3} pc2(M[r][p]^M[r][q]);
M=G0, r=y na C_AB→B; M=F0, r=x na C_BA→A; 32 = 2^5 bits livres após fixar
(r,c). É a fórmula W̃ do resultado prévio com pi_m = id para ambos os m:
**III é o ponto degenerado da condição K** — tau = pi1∘pi0⁻¹ substituído
por id, que é isometria de qualquer W_M. (iv) C2: os conjuntos de eficácia
por bit são funcionais de xr ⇒ idênticos entre contextos. C3: as
assinaturas nxt diferem entre contextos apenas por complemento constante
por bit (sigma) e pela constante K[m][y] no bit de memória; o número de
assinaturas distintas por bit através das intervenções é invariante a
complemento ⇒ suporte idêntico. As TRÊS candidatas congeladas dão 'estado'
deterministicamente nestas arestas em III.

**D3. Baseline (via de mimetismo nº1).** nx_m alinhado:
nx_m(z) = (G0[y][cAB]^sigmaB[m]) | (K[m][y]<<2). Pontos discordantes entre
contextos: bdep = 512 se sigmaB[0]≠sigmaB[1]; senão
128·|{y: K[0][y]≠K[1][y]}|. Nas famílias ELEGÍVEIS, E1(III)+E5(III) forçam
sigma diferente (F8): logo **bdep = 512 — TODOS os pontos da fibra — em
ambas as arestas, em 100% das famílias elegíveis**. Num III verdadeiro a
memória é causalmente activa em todos os pontos do baseline; o estatístico
congelado aniquila essa actividade exactamente, por diferenciação XOR.

**D4. Órbita (via de mimetismo nº2).** Com V = órbita(s0), V_m = {s∈V:
mem_receptor(s)=m}, S_m(k) = Σ_{s∈V_m} pc2(xr_k(s)): pelo Teorema III-1,
xr_k(s) depende só do par (r(s),c(s)), logo S_m(k) = Σ_{r,c}
Cnt_m[r][c]·resp_k(r,c), com Cnt_m a matriz de visitação 4×4 do contexto m.
**Proposição:** Cnt_0=Cnt_1 ⇒ S_0=S_1; qualquer diferença S_0 vs S_1 num
III é portanto composição de visitação (selecção), nunca mecanismo.
(Factorização verificada 4000/4000.)

**D5. Situação do lado II à mesma resolução (contexto, não proposta).**
Num II, xr(z) = G0[y][pi_m(sub(cAB))] ^ G0[y][pi_m(cAB)] (mesmos
cancelamentos de sigma e K). dep=0 numa aresta II ⇔ condição PONTUAL:
M[r][pi_0(sub(c))]^M[r][pi_0(c)] == M[r][pi_1(sub(c))]^M[r][pi_1(c)] para
todo (r, c, intervenção) — estritamente mais forte do que a condição K
agregada (dep=0 ⇒ L1 ⇒ K; F6 mostra dep>0 com L1 em 91/92 arestas de
colapso). O ponto fixo xr≡(campo III) é atingível do lado II, mas
raramente (F6: 7/20000 arestas).

**D6. Teorema III-2 (horizonte 2: a invariância NÃO itera).** Mesma aresta
C_AB→B, mesmo ponto z, mesma intervenção; sB:=sigmaB. A t=1:
y1 = G0[y][c]^sB[m]; mB1 = K[m][y]; cAB1 = x; (x1, mA1, cBA1=y) não
afectados. A t=2, campos do receptor B:

    y2  = G0[y1][x] ^ sB[mB1]
    mB2 = K[mB1][y1]

XOR intervencional (c→c*): o termo aditivo sB[mB1] CANCELA (mB1 igual nos
dois ramos), mas sB[m] SOBREVIVE dentro dos índices de linha
(não-linearidade da composição) e K[m][y] selecciona a linha de K:

    xr2(z) = ( G0[G0[y][c*]^sB[m]][x] ^ G0[G0[y][c]^sB[m]][x] )
           | ( ( K[K[m][y]][G0[y][c*]^sB[m]] ^ K[K[m][y]][G0[y][c]^sB[m]] ) << 2 )

⇒ xr2 depende de (x,y,c) e, genericamente, de m, por DUAS vias:
deslocamento sigma do índice de linha (sB[0]≠sB[1] garantido em famílias
elegíveis, F8) e selecção de linha de K. São exactamente as estruturas cujo
cancelamento exacto a horizonte 1 dá o Teorema III-1. Simétrico na C_BA→A
com (F0, H, sigmaA). Multiplicidade 8 = 2^3 (bits livres após fixar o
índice exterior o, o estado do receptor r e o valor do canal c); forma
fechada d2_m(a) = 8·Σ_{o,r,c} [pc2(parte-M) + pc1(parte-K)] — verificada
exacta em 4000/4000 arestas, ambos os m (PH2). A memory-dependence de um
III a h2 é GENUÍNA (mecanismo, não selecção): existe na fibra completa,
alinhada, XOR-diferenciada — o mesmo tipo de objecto que a h1 é
identicamente nulo. ∎

**D7. Lema das linhas complementares (caracterização parcial dos zeros de
h2).** Se K[1][w] = 1⊕K[0][w] para todo w (mem_rows_dif=4), então para
qualquer k: K[1⊕k][w] = 1⊕K[k][w], donde a parte-K de xr2 no contexto
m=1, K[k_1(y)][a_1]^K[k_1(y)][b_1] = (1⊕K[k_0(y)][a_1])^(1⊕K[k_0(y)][b_1])
= K[k_0(y)][a_1]^K[k_0(y)][b_1]: a via de SELECÇÃO de linha K desaparece
identicamente, restando apenas a via sigma (nos índices a_m,b_m) em ambas
as partes. dep2=0 exige adicionalmente que a via sigma cancele para o par
(M, sB[0]⊕sB[1]) concreto — coincidência combinatória rara. Consistente
com F10: os 4 zeros observados têm todos mem_rows_dif=4 (base 5,6%). O lema
dá suficiência da neutralização da via K, não necessidade de
mem_rows_dif=4 para dep2=0; a associação 4/4 é empírica. ∎ (lema)

---

## EMPIRICAL SUPPORT

**E1. Zero ocorrências de dependência de memória de alta resolução em III
(horizonte 1).** 0/2000 instâncias com dep>0 em qualquer aresta → limite
superior unilateral exacto (Clopper-Pearson) a 95%: P ≤ 1−0,05^(1/2000) =
1,497×10⁻³. Por aresta: 0/4000 → P ≤ 7,487×10⁻⁴. Estes limites são GUARDAS
DE IMPLEMENTAÇÃO: a afirmação substantiva é o Teorema III-1 (P=0
analítico), que a amostra não pode melhorar.

**E2. Concordância total previsão-medição.** As previsões P1-P8 (1.ª
passagem) e PH1-PH4 (2.ª) verificaram-se sem excepção (F4, F9; 0
anomalias). A forma fechada reproduziu d_m entrada a entrada nas 4000
arestas a h1 (P3, caso pi=id) e d2_m nas 4000 a h2 (PH2) — e a fórmula W̃
com pi≠id verificou nas 4 arestas II replayadas (F5/A2): a cadeia
derivação→implementação está auditada nos três regimes.

**E3. A implementação do dep foi validada em regime não-nulo** (F5/A2):
reproduziu exactamente dep_sites 2176/2176 (L3/L3) e 2048/1536 (L1/L1) de
famílias II registadas, e a fatia determinística de 25 famílias da própria
medição. Um dep avariado que devolvesse 0 por defeito teria sido apanhado.

**E4. Exemplo concreto (fam 0, seed 910000020, C_AB→B):** d0 = d1 = dpred =
[0,320,320,192,192,320,384,448,384]; dep=0; bdep=512; órbita 27 com V_0=5,
V_1=22; S_0 = [0,2,6,3,2,2,6,4,6] vs S_1 = [0,9,15,7,13,10,15,18,17]. O
estatístico congelado (fibra completa) vê zero dependência de memória; a
MESMA maquinaria restringida aos estados visitados por contexto "veria"
dependência — fabricada pela visitação.

**E5. Magnitude do mimetismo de órbita.** Perfis normalizados S_m/|V_m|
diferem em 100% das 4000 arestas (Cnt_0==Cnt_1 nunca ocorreu); delta_norm
mediana ≈ 0,53-0,55 bits/estado, p90 ≈ 1,0, máx 2,0.

**E6. Saturação do baseline.** bdep = 512/512 pontos em 4000/4000 arestas,
com a previsão estrutural exacta confirmada (sigma difere sempre, por
E1+E5). A actividade causal da memória em III não é rara nem subtil: é
máxima — e invisível ao estatístico congelado por construção.

**E7. Horizonte 2: a mesma classe de estatístico, iterada uma vez, vê
memória em III quase sempre.** dep2>0 em 3996/4000 arestas (99,90%;
IC95 [0,99744, 0,99973]); 2000/2000 instâncias com ≥1 aresta dep2>0
(IC95 inferior 0,99816); níveis a h2: L3 83,4%, L2 15,8%, L1 0,85%.
Magnitudes: dep2 mediana 1312-1344, máx 2176 — a MESMA escala do dep
horizonte-1 do lado II registado (mediana 1152 nas arestas de colapso;
2176 nos exemplos individua_ambas; F6). Um analista que aplicasse o teste
de ranks de C1' ao operador T² concluiria 'sinal' (rank diferente) em
~83% das arestas de IIIs verdadeiros.

**E8. Contraste com o lado II à resolução dep (datasets existentes).**
III h1 = 0 exacto (4000/4000); II h1 = dep>0 em 19993/20000; mesmo entre
as 92 arestas dos 46 colapsos (que C1' não separa), 91 têm dep>0 (min 384,
mediana 1152). O único ponto de contacto exacto II∩III neste dataset são
7/20000 arestas II com dep=0 (1 delas dentro de um colapso; 0 colapsos com
ambas). Simetricamente, III toca o "campo II-típico" a h2 em 99,9% das
arestas, com 4/4000 excepções (F10) e 0 instâncias com ambas as arestas
nulas a h2.

---

## INFERENCE

**I1.** A especificidade da classe III face ao instrumento congelado é
PERFEITA e determinística: nenhum III verdadeiro pode exibir d_0≠d_1,
ranks diferentes, dep>0, eficácia C2 dependente do contexto ou suporte C3
dependente do contexto nas arestas canal→processador, sob a semântica
congelada (UMA transição). O erro confirmatório (fam 20) é um fenómeno
EXCLUSIVAMENTE do lado II (colapso de agregação na sensibilidade); não
existe fenómeno simétrico do lado III ao nível do instrumento. A fusão do
núcleo em III é o comportamento correcto, alcançado por razão estrutural
(interface directa), não por acaso amostral.

**I2.** A memória de um III verdadeiro é causalmente ACTIVA — em quatro
estruturas de alta resolução: (a) baseline por contexto (offset sigma +
dinâmica K/H), saturado (100% dos pontos, 100% das arestas); (b) composição
de visitação da órbita por contexto (100% das órbitas); (c) campos de
assinatura brutos (diferem por complemento constante; o suporte C3 é o
quociente que os apaga); (d) — novo — o próprio campo XOR-intervencional em
fibra completa APLICADO A T², onde a actividade é genuinamente mecanística
(Teorema III-2), quase universal (99,9% das arestas) e com magnitude
igual à de um II verdadeiro a h1. As três primeiras estão fora da classe de
funcionais do instrumento; a quarta está DENTRO da classe em tudo excepto
no horizonte. A cegueira do instrumento a todas elas é o que compra a
especificidade perfeita de I1 — e essa cegueira assenta CRITICAMENTE na
aplicação de exactamente uma transição: o cancelamento sigma/K de D1 é uma
identidade de primeira ordem que a composição destrói (D6).

**I3. Resposta à pergunta-objectivo (tarefa 5).** Recuperar a informação
perdida em II (o campo pontual xr, que a agregação d_m e o rank descartam)
pode, EM PRINCÍPIO, introduzir ambiguidade do lado de III? Resposta
refinada pela 2.ª passagem:
— **Não**, se a recuperação permanecer nos funcionais do campo de resposta
XOR a intervenções sobre fibra COMPLETA **a horizonte exactamente 1**:
nessa classe o III é o campo identicamente nulo (Teorema III-1) e nenhuma
variabilidade entre contextos pode surgir do lado III; o funcional mais
fino da classe (o próprio campo pontual) mantém III exactamente em zero.
— **Sim**, fora dela — e "fora" é mais perto do que a 1.ª passagem
sugeria: basta iterar a transição UMA vez. A horizonte ≥2, baselines por
contexto, agregados condicionados à órbita, campos de assinatura
não-quocientados ou observáveis da dinâmica H/K, um III verdadeiro tem
estrutura dependente de memória genuína, quase universal (99,9-100% nesta
amostra) e com magnitudes indistinguíveis das de um II a h1 (E7).
— Direcção do risco DENTRO do canal seguro (h1): residual e
unidireccional — II pode atingir o campo nulo (7/20000 arestas; D5) e
tornar-se pontualmente indistinguível de III; III nunca sai do campo nulo.
FORA do canal seguro a ambiguidade é bidireccional e massiva. Este WS não
propõe como explorar nem como resolver nada disto.

**I4.** Transferência de regime: pelo argumento de D1/D6 (independentes de
n) e pelo lema F7, as conclusões valem no regime confirmatório (Estrato 2,
n=12, módulos D inertes para eB dos receptores; multiplicidades ×4).

**I5.** A associação dos 4 zeros de h2 com linhas K/H complementares
(4/4 observados vs base 5,6%; lema D7 explica a neutralização exacta da via
K) indica que mesmo as excepções de h2 são degenerescências combinatórias
identificáveis, não memória inerte — a elegibilidade (F8) proíbe a inércia.

---

## SPECULATION

**S1.** O acesso observacional realista é em forma de órbita; a fibra
completa é um dispositivo teórico. Especulamos que qualquer estimador
prático da "informação perdida" que não faça completamento exacto da fibra
herda o confundimento de visitação de D4/E5 — universal nesta amostra, não
patológico.

**S2.** Vista unificada especulativa: III é o ponto fixo (tau=id) da
geometria de modulação; os colapsos II (condição K) aproximam-se dele no
agregado W̃, e as 7 arestas II com dep=0 atingem-no pontualmente. A
correlação inter-arestas ~2,1-2,4× do lado II (tau partilhado, resultado
prévio) sugere que a "distância ao ponto fixo" é propriedade da família,
não da aresta.

**S3.** Especulamos que a dependência de memória de III cresce com o
horizonte k≥2 até saturar na escala de mistura da dinâmica (a h2 já está
na escala de um II a h1), tornando qualquer estatístico multi-passo
progressivamente cego à DISTINÇÃO de classes — a separação II/III seria
uma propriedade quase exclusiva da primeira ordem. Não medido para k≥3.

**S4.** Os 30 casos de cancelamento agregado a h2 (L1 com dep2>0) sugerem
que fenómenos tipo condição-K reaparecem a cada horizonte com a sua própria
geometria (aqui W de segunda ordem); especulamos que admitem caracterização
por isometria análoga — não derivada aqui.

---

## QUESTÕES ABERTAS

1. Identidade e nível das 6 arestas II com dep=0 fora do conjunto de
   colapsos (agregado F6): localizá-las exigiria replay extensivo dos
   fluxos 910000001/910000002 (alheios); prevê-se (D5) que sejam L1 com a
   outra aresta L3.
2. Prevalência e caracterização algébrica da condição pontual de D5 no
   lado II (que pares (pi0,pi1,M) a satisfazem) e a sua relação de
   inclusão estrita com a condição K.
3. Necessidade (vs suficiência parcial, D7) nas nulidades de h2: existe
   dep2=0 sem linhas complementares? Caracterização completa do conjunto
   de cancelamento da via sigma para (M, s0⊕s1) dados.
4. Crescimento de dep_k com o horizonte k≥3 e a conjectura de saturação S3.
5. Estrato 2: vias compostas canal→D→… não medidas (a tipificação
   congelada di-las inertes; F7 cobre os extractores dos receptores).
6. delta_norm de órbita em II genuínos (comparável a E5) não medido —
   ficaria a cargo de outro WS se relevante.

---

## ANEXO — Ficheiros desta área (todos POST-CONFIRMATORY / EXPLORATORY)

1.ª passagem:
- `precommit-ws4-classIII-especificidade.txt` — derivação P1-P8 + plano, ANTES da medição.
- `medicao_ws4_classIII.py` → `ws4-classIII-medicao.json` + `.out` (N=2000, seed 910000020, 4,8 s).
- `contraste_II_ws4.py` → `ws4-contraste-II.json` + `.out` (leitura determinística; sem amostragem).

2.ª passagem (esta versão do relatório):
- `precommit-ws4-adenda-h2-auditoria.txt` — auditoria + Teorema III-2 + PH1-PH4, ANTES das execuções.
- `auditoria_ws4_2a.py` → `ws4-auditoria-2a.json` + `.out` (A1-A3; 0 falhas; 0,1 s).
- `horizonte2_ws4.py` → `ws4-horizonte2.json` + `.out` (T2=T∘T, mesmas 2000 famílias; 4,9 s).
- `WS4-CLASSIII-SPECIFICITY.md` — este relatório (substitui a versão sha
  `f9cd27a4…`, cujo conteúdo factual é integralmente preservado acima).
- `SHAS.txt` — sha256 de todos os ficheiros desta área (regenerado no fim).

Sementes: 910000020 (única consumida; reproduzida deterministicamente na
2.ª passagem); 910000001 usada SOMENTE para replay de famílias registadas
do dataset existente (procedimento de replay do briefing). Nenhuma das
queimadas/confirmatórias. Instrumento: frozen-copy (12/12 vs MANIFEST).
Nenhuma escrita fora desta área; nenhuma alteração ao confirmatório.
Sem multiprocessing. Execuções da 2.ª passagem: 2 (0,1 s + 4,9 s) mais um
sumário de leitura do próprio JSON.

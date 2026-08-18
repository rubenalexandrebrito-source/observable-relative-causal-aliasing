# FASE 6 — SÍNTESE MULTIAGENTE (COORDENADOR / RED-TEAM)

**POST-CONFIRMATORY / EXPLORATORY** — Pré-registo A v8.3 (Amendments 1-3 congeladas), Fase 6 multiagente.
Autor: coordenador/red-team. Data: 2026-08-17. Área: `/root/causal-A-postconfirmatory-analysis/multiagent/coordinator/`.

> **CONFIRMATORY RESULT: NEGATIVE.** `resultado_confirmatorio_A = "negativo"`, fechado e imutável.
> C1′ obteve 199/200 (E1 150/150, E2 49/50); único erro: instância `7bb0baab3a8ed7aa`, família 20,
> variante II, Estrato 2 (n=12). Nada nesta síntese recalcula, reinterpreta ou atenua esse resultado.
> Nenhuma C1″ é formulada; a síntese termina no que aprendemos sobre o limite de identificabilidade.

**Taxonomia de evidência usada em todo o documento (B5):**
**A** = PROVEN ANALYTICALLY · **B** = EXHAUSTIVELY VERIFIED IN A FINITE DOMAIN ·
**C** = EMPIRICALLY VALIDATED OOS (amostra pré-comprometida independente) ·
**D** = INTERNALLY REPRODUCED (outro agente/workstream, mesmo repositório) ·
**E** = SUPPORTED / CONJECTURED. Uma conclusão pode ter vários rótulos.
**Nota A1/B4:** toda a concordância entre agentes descrita abaixo é *verificação interna
independente ao nível do workflow* — nunca replicação científica externa, que ainda NÃO ocorreu.

---

## 1. Estado confirmatório

- `resultado_confirmatorio_A = "negativo"`. C1′: E1 150/150; E2 49/50; `passa: false` (alvo E2 falhado);
  único erro `7bb0baab3a8ed7aa` (fam 20, II, E2). C2: 74 erros; C3 (canário): 75 erros. Equivalências
  exaustivas 524288/524288 com 0 discrepâncias; escala limpa.
- Imutabilidade verificada por este coordenador (2026-08-17, `lsattr`): atributo `i` presente em
  `/root/causal-A-amd2-official/prereg-A/equiv-agregado.json`, `/root/causal-A-amd2-official/prereg-A/class-e1.json`
  e `/root/causal-A-amd2-official/resultado-pontuacao-A.txt`. **Nota de auditoria:** o mandato indicava
  `prereg-A/resultado-pontuacao-A.txt`; o ficheiro real está um nível acima (na raiz de
  `causal-A-amd2-official/`) — desvio de caminho no mandato, não do artefacto; nada foi alterado.
- `frozen-copy/*.py`: sha256 12/12 idênticos ao `MANIFEST.txt` (verificado por mim e por cada um dos 5 WS).
- Os cinco relatórios têm sha256 real idêntico ao declarado nos outputs estruturados e nos respectivos
  `SHAS.txt` (verificação directa; tabela na secção 21).

## 2. Factos estabelecidos antes da análise multiagente

Da Fase 5/6 (agente único; ficheiros em `prevalencia/` e `FASE6-AUTOPSIA-7bb0baab3a8ed7aa.md`, sha `b828e85c…`):

1. Instância falhada: fam 20, II, n=12, órbita 25; C1′ funde o núcleo {A,B,C_AB,C_BA}; ambos os contextos
   de memória alcançados; dependência ponto-a-ponto 4608 sítios/aresta; C2/C3 também erram aqui.
2. Prevalência (N=10000, sementes 910000001/2): 46 colapsos/10000 instâncias II (0,46% [IC95 0,345-0,613]);
   por aresta: L1=705 (3,53%), L2=225 (1,13%), L3=19070; dep>0 em 19993/20000; subtipos 29×(L1,L1),
   10×(L1,L2), 7×(L2,L2); correlação entre arestas ~2,1-2,4× a independência.
3. Lema d_E2 = 4·d_E1 (módulos D inertes) [A+B] — análises em n=10 transferem exactamente para E2.
4. Condição K: d_m(a) = 32·Σ_c W̃_m(c,sub_a(c)) com W̃_m(c1,c2)=Σ_r pc2(M[r][π_m c1]⊕M[r][π_m c2]);
   σ cancela; **d_0=d_1 ⟺ τ=π1∘π0⁻¹ ∈ Iso(W_M)** — verificada sem excepção em 30000 arestas
   (in-sample + OOS 910000004: TP 705+368, FP=FN=0) [A+B+C].
5. fam-20: C_BA→A com W̃ equidistante (Iso=S4); C_AB→B com Iso={id, transposição} e τ = essa transposição.
6. Correlação: modelo de τ partilhado ~1,91× vs ~2,33× observado (resíduo ~1σ, por explicar à data).

## 3. Resultados WS1 (condição algébrica do L1) — veredicto do coordenador: CONFIRMADO

- Derivação independente **sob firewall** (ver §21): d_m = 2^(n-5)·(0,A_m,A_m,B_m,B_m,V_m(0..3)) e
  **Teorema 5**: d_0=d_1 ⟺ K(θ): ρ=π0⁻¹∘π1 preserva os agregados (WM nos dois emparelhamentos sondados
  + V∘ρ=V) [A]. Prova de equivalência com a condição prévia (sistema 6×6, det −8, posto 6) [A].
- Validação: replay integral dos 2 lotes (0 divergências fórmula vs maquinaria em 20000 arestas; 0 excepções
  K⟺L1) [B+D]; **OOS pré-comprometida 910000005** (precommit sha `454821ad…`, verificado): K vs L1 TP 307
  FP 0 FN 0; ordinal vs L1∪L2 404/0/0; colapso 16/0/0 [C].
- Extras: Prop. 8 (marca 'estado' ⟺ invariância ordinal do perfil, validada contra `cl.classificar`
  252/252 + fusão 126/126) [B]; Corolário 8.1 (ρ∈V4 ⟹ L2 impossível; 0 L2 em 3958 arestas V4) [A+B];
  caracterização do dep (dep=0 ⟺ invariância do tensor de padrões) [A]; tabela por classe de ρ
  (codimensão 2 vs 4 prevê a dominância de transposições/V4) [A+B]; refutação activa falhada
  (414 casos-canto; 40000 verificações, 4 sementes) [B+C].
- Reexecução do coordenador: det −8/posto 6 reproduzido com implementação própria (fracções exactas),
  inversa explícita verificada 200/200; K⟺L1 sem excepção em 800 arestas novas (semente minha 910000050);
  classes de τ com taxas L1 compatíveis (T 9,1%, DT 9,7%, C3 0,4%, FC 1,4%) [D].

## 4. Resultados WS2 (decomposição da perda) — veredicto: CONFIRMADO

- **Bijeção linear d ↔ W̃** (inversão explícita, erro 0): a agregação não destrói nada além de W̃; logo
  L1 ⟺ W̃_0=W̃_1 ⟺ τ∈Iso(W) — necessidade re-obtida por inversão [A+B]. **B4=0 é teorema**: em L1 a soma
  coincide bloco a bloco; compensação entre blocos nunca é o mecanismo (22560/22560 blocos) [A+B].
- Estágios da perda nas 705 arestas L1: F1 pc-pontual 29 (4,2% das 698 com dep>0) ⟺ τ∈∩_r Iso(w_r)
  (36=29+7, 0 excepções nos dois sentidos) [A+B]; F1.5 histograma 174 (24,9%); **F2 soma-por-bloco 495
  (70,9%, modo dominante; fam-20 nas duas arestas)**; filtração ∩_r Iso(w_r) (36) ⊂ Iso_multiset (210)
  ⊂ Iso(W) (705) [B].
- L2: rank destrói magnitude cardinal com quantum 64 (paridade, teorema; 84022 componentes, 0 violações)
  [A+B]; movimento confinado a {k1,k2}/{k3,k4}; bloco do(c=γ) imóvel 225/225 (teorema parcial sob Δm=0) [A parcial+B].
- Proveniência: tentativa interrompida auditada e re-executada **byte-idêntica** (6/6 outputs) [D].
- Reexecução do coordenador (910000050): estágios F1/F1.5/F2 = 4/9/22 (11%/26%/63% vs 4,2/24,9/70,9 — compatível
  com N=35); B4=0 e igualdade célula-a-célula em TODAS as arestas L1 novas; quantum-64 sem violações [C+D].

## 5. Resultados WS3 (dinâmica realizada estrita) — veredicto: CONFIRMADO (1 rótulo cosmético corrigido)

- **fam-20: dependência ESTRITAMENTE realizada em ambas as arestas** — células (r,c) visitadas nos DOIS
  contextos com resposta intervencional diferente (9 sítios estritos/aresta) e testemunha observacional
  sem cirurgia em ambas [B]. Prop. 1 (resposta depende só de (r,c) dado m; σ e memória cancelam) [A] justifica
  a granularidade (r,c) como partição de comparabilidade exacta mais grossa e invariante ao embedding E1↔E2;
  o critério por configuração completa é inadequado (interseções vazias por escassez + dependência dos bits D).
- Bateria: ESTRITO em 74/92 arestas dos colapsos (80,4%), 65/80 controlos (81,3%), 64/80 mistos (80,0%) —
  colapsos NÃO deficitários em realização [B]; baseline fresco 910000010: 86,3% arestas, 98,0% instâncias ≥1;
  PURO_CONTRAFACTUAL raro (1/652) [C]. Verificação independente própria do WS3 (rota por testemunhas): 4312
  comparações, 0 discrepâncias [D].
- Reexecução do coordenador: fam-20 reproduzida integralmente pela minha própria despermutação da tabela cega
  (|C0|/|C1|, n_I=4/5, 9+9 sítios estritos, 30/27 união, testemunhas observacionais idênticas) [D]; amostra
  fresca 910000050: ESTRITO 85,6% das arestas, ≥1 94,8% das instâncias, ambas 76,5%, PURO_CTF 1/800,
  testemunha observacional 43,6% (vs 42,8% WS3) [C].
- **Achado de auditoria (cosmético):** na aresta C_AB→B da fam-20, o WS3 rotulou a célula estrita (2,0)
  onde o layout canónico congelado (bit3 = y LSB) dá (1,0) — os bits de y foram lidos por ordem invertida
  na despermutação do WS3 (verifiquei decisivamente: os conjuntos C0/C1/I do JSON do WS3 coincidem com os
  meus sob a bijecção r:1↔2). Todas as contagens (n_I, sítios, dep, testemunhas) são invariantes ao rótulo;
  nenhum resultado é afectado. Na aresta C_BA→A (bits de x) o rótulo do WS3 é canónico.

## 6. Resultados WS4 (especificidade da classe III) — veredicto: CONFIRMADO

- **Teorema III-1** [A]: no passo III, o campo XOR-intervencional em fibra completa a horizonte 1 é
  identicamente nulo (σ cancela no XOR; a linha de K não depende do canal) ⟹ dep≡0, d_0≡d_1, L1 sempre,
  fusão determinística e CORRECTA em todo o III; independente de n ⟹ vale no Estrato 2. Medição: 0/4000
  arestas (semente 910000020, precommit anterior) [C]. **Não existe fenómeno simétrico do lado III**: o erro
  confirmatório é exclusivamente do lado II.
- A memória de um III é causalmente ACTIVA fora desse funcional: baseline saturado (512/512 pontos,
  4000/4000 arestas — E1+E5 forçam σ[0]≠σ[1]) [A+C]; visitação da órbita (100%) [C]; e — **Teorema III-2**
  [A], novo no run2 — no MESMO estatístico aplicado a T∘T: dep2>0 em 99,90% das arestas, níveis L3 em 83,4%,
  magnitudes iguais às de um II a h1 [C]. Os 4 zeros de dep2 têm todos linhas K/H complementares
  (lema de suficiência [A]; associação 4/4 empírica).
- **Fronteira exacta**: a especificidade de III é propriedade do horizonte exactamente 1 dentro da classe
  XOR-em-fibra-completa; iterar a transição UMA vez já destrói o cancelamento (não-linearidade da composição).
- Reexecução do coordenador (semente minha 910000051, N=250): h1 0/500 arestas com dep>0 ou d_0≠d_1, fórmula
  exacta; h2 com implementação própria (T[T]): dep2>0 em 500/500, níveis2 L3 83,0% / L2 16,4% / L1 0,6%,
  mediana dep2 1312 — tudo dentro dos ICs do WS4 [C+D].

## 7. Resultados WS5 (estrutura da classe de falha) — veredicto: CONFIRMADO

- **Uma só classe mecanística** [B+C+E]: colapso ⟺ π1 na classe-de-rank de π0 do perfil W observável;
  estratos internos (L1 métrico vs L2 ordinal × 7 células de (τ,lam)) são ANALÍTICOS; clustering sem k
  não encontra classes discretas robustas (silhueta ≤0,41; ARI vs subtipo −0,13).
- **Teorema do alinhamento** [A]: se ψ(τ) fixa a emparelhação não sondada lam, o perfil de m=1 é permutação
  posicional do de m=0 ⟹ colapso ⟹ L1; L2 impossível em células alinhadas. Verificação: 0 arestas L2 em
  21390 arestas alinhadas (in-sample + OOS 910000030 + RAW 910000031) [B+C]; DT_lam≡DT_oth (corolário) [A+C].
- **Mecanismo de valor de L2** [A+B]: troca de uma emparelhação sondada pela cega; valor novo = S(lam)
  (225/225 na população, 193/193 com identidade exacta; C3 = dupla troca 32/32; bloco D imóvel 225/225).
- **Correlação explicada sem resíduo**: M3 = Σ(|EqB∩EqA|−1)/23 (sem parâmetros livres) dá z=+0,32 in-sample,
  z=+0,57 OOS; both-L1 z=+0,19/+0,58; tilt de elegibilidade |z|≤1,62; RAW M1≈M3 [A(fórmula)+C].
- fam-20 típica: (L1,L1) modal com uma aresta forçada (equidistante, |Iso|=24) e uma τ-seleccionada (|Iso|=2).
- Auditoria de 2.ª passagem do próprio WS5: reimplementação independente 29/29 PASS; re-execuções byte-idênticas [D].
- Reexecução do coordenador (910000050): alinhamento sem contra-exemplo (0 L2 alinhadas; o único colapso
  em célula alinhada é (L1,L1), como o teorema exige); assinatura L2 11/11 (um par P com valor novo =
  32·S(lam) em T; dupla troca em C3); M3 soma 1,57 vs 2 colapsos observados; transporte (pares e V)
  verificado em 800 arestas sem violação [C+D].

## 8. Auditoria cruzada

**8.1 Integridade e proveniência.** frozen-copy 12/12 = MANIFEST (6 verificações independentes: 5 WS + coordenador).
Relatórios: sha real = sha declarado nos 5 casos. `SHAS.txt` de cada WS lista o próprio relatório com o hash correcto.
Precommits com timestamps anteriores às execuções correspondentes (verificados por mtime nos casos WS1 s13,
WS4 1.ª/2.ª, WS5 OOS/taucheck/audit, WS3 strict/emenda). Área confirmatória intacta (secção 1).

**8.2 Reexecuções do coordenador** (precommit próprio `precommit-coordinator.txt` fixado antes; sementes novas
APENAS 910000050/910000051 do meu intervalo; scripts `coord_a…d`, outputs `coord_a…d.out` nesta área):

| alvo | resultado |
|---|---|
| Sistema linear das 9 intervenções | det = **−8**, posto 6, inversa explícita verificada 200/200 (WS1/WS5 confirmados) |
| Lattices empobrecidos | só bits isolados: posto 2 (núcleo dim 4); só do(c=γ): posto 4 (núcleo dim 2) — a recíproca exige a COMBINAÇÃO |
| fam-20 (tabela cega, despermutação própria) | órbita 25; d_0=d_1 exactos aos registados; dep=4608/aresta; W̃_0=W̃_1; W matrizes = autópsia; Iso = 2 e 24; transporte ρ único = (23) = a única isometria não trivial da aresta B; 9+9 sítios estritos; testemunhas observacionais; `cl.classificar` funde {A,B,C_AB,C_BA} |
| Replay lote1 até tentativa 14155 | aceite n.º 4160 (índice 0-based **4159**); theta_sha prefixo **964a55337a7a502f**; τ classe (2,2); aresta B dep=0 L1 V=(14,14,14,14); aresta A dep=1152 L1; colapso — reconcilia WS1 (“fam 4159”), WS3/WS5 (“t=14155”), WS4 (theta_sha) numa só família |
| Amostra fresca II (910000050, N=400, 1342 tentativas) | 0 violações em TODOS os critérios pré-fixados: fórmula, K⟺L1 (800 arestas), impressão digital, multiset d[5..8], transporte, células L1 (B4), quantum-64, L2-alinhada, assinatura-L2, consistência M3. Níveis 35/11/754; colapsos 2 vs M3 1,57; estrito 85,6%; testemunha obs. 43,6%; 202 contra-exemplos do lattice truncado; |Iso|>1 em 50,6% |
| Amostra fresca III (910000051, N=250) | Teorema III-1: 0/500; fórmula exacta; h2: dep2>0 500/500, L3 83,0%, mediana 1312 |

**8.3 Consistência entre agentes e com os datasets.** Totais unânimes (L1 705=370+335; L2 225; L3 19070;
dep>0 19993/20000; 46 colapsos 29/10/7 — WS5 desagrega os 10 em 5+5 ordenados). Estágios WS2 somam 705
(29+174+495+7). 36 = 29 F1 + 7 dep=0 = |{τ∈∩_r Iso(w_r)}| (WS2⟷WS1 coerentes). A aresta dep=0 do colapso é a
MESMA família em quatro contabilidades distintas (fam 4159 = t 14155 = 964a5533… = DT_oth aresta B), agora
provado por replay. A cadeia 4608 = 4×1152 = 128×36 células bate com o lema E1↔E2 e com a multiplicidade.

**8.4 Tensões encontradas (nenhuma substantiva):**
1. Rótulo (2,0) vs (1,0) do WS3 na fam-20 aresta B — inversão de ordem de bits do y na despermutação;
   cosmético, contagens invariantes (secção 5).
2. WS4 run1 afirmava segurança de TODA a classe XOR-em-fibra-completa; o run2 restringe-a correctamente a
   horizonte exactamente 1 (Teorema III-2). Refinamento, não contradição — mas a formulação do run1, isolada,
   era mais forte do que o demonstrado (secção 21).
3. Resíduo de correlação: a autópsia deixou ~1σ por explicar com hipótese de tilt de elegibilidade; o WS5
   fecha-o com o modelo exacto M3 e desfavorece o tilt (teste directo). Supersede, sem conflito.
4. Taxas de colapso entre amostras: 0,46% in-sample, 0,32% OOS-WS1, 0,48% OOS-WS5, 0,50% minha (2/400) —
   dispersão Poisson-compatível (extremo ~1,5σ).
5. Autópsia §4.5 “K falso → L3” devia ler ¬L1=L2∪L3 (apanhado pelo WS1; prosa, não dados).
6. Caminho do mandato para `resultado-pontuacao-A.txt` (secção 1).

## 9. Mecanismo final da falha

**9.1 Cadeia demonstrada.** No passo II congelado, a resposta do receptor a intervenções no canal factoriza:
σ cancela em todos os XOR contrafactuais; a memória do receptor entra APENAS por π_m; a resposta é constante
em cada célula (r,c) com multiplicidade 2^(n-5) [A]. O vector d tem a forma 2^(n-5)·(0,A,A,B,B,V(0..3)) e é
**bijecção linear de W̃_m** [A]. Os dois contextos vêem a MESMA geometria W_M relabeled: W̃_1 = W̃_0 ∘ (ρ×ρ)
[A]. Logo:

> **C1′ falhou na fam-20 porque τ=π1∘π0⁻¹ ∈ Iso(W_M) em ambas as arestas** — o remapeamento relativo entre
> contextos de memória é uma simetria exacta da geometria de resposta agregada do receptor; o somatório de
> Hamming sobre a fibra é invariante sob essa simetria, apesar de as respostas ponto-a-ponto diferirem em
> 4608 sítios por aresta, 9 deles em células estritamente realizadas nos dois contextos. A informação
> discriminante morre DENTRO das células de agregação (identidade do bit B1 / localização r B2 / partição
> intra-célula B3 — o modo da fam-20), nunca entre blocos (B4=0) e nunca por ausência de realização.

**9.2 Respostas directas Q1-Q9** (estatuto entre parênteses):

- **Q1 (mecanismo exacto de L1):** d_m = 2^(n-5)·(0,A_m,A_m,B_m,B_m,V_m) factoriza por W̃_m;
  **L1 ⟺ W̃_0=W̃_1 ⟺ τ∈Iso(W_M)** — cancelamento por agregação sob permutação isométrica dos pares
  (A: ambas as direcções; B: 30000+10000+800 arestas; C: 3 OOS; D: 4 implementações internas).
- **Q2 (condição formulável):** sim, necessária E suficiente: K ≡ τ∈Iso(W_M) para L1; invariância ordinal do
  perfil para a marca 'estado' (L1∪L2); teorema do alinhamento dá a condição de fase para L2 (só células
  não alinhadas) (A+B+C+D). Suficientes estruturais: W equidistante ⟹ colapso da aresta para QUALQUER τ.
- **Q3 (onde se perde a informação):** não nos pontos (dep>0 em 99,97% das arestas), não entre blocos (B4=0),
  não no suporte realizado (WS3): perde-se na agregação intra-célula — 4,2% já no popcount pontual,
  24,9% na invariância a permutações (localização r), 70,9% no colapso aritmético da soma (modo da fam-20);
  a franja L2 perde adicionalmente magnitude cardinal no rank (quantum 64) (A+B).
- **Q4 (dependência realizada?):** SIM, estritamente: células (r,c) visitadas em AMBOS os contextos com
  resposta diferente — 9 sítios/aresta na fam-20, com testemunha observacional sem cirurgia; padrão
  populacional: 80-86% das arestas (B+C). O colapso não é desculpável por suporte.
- **Q5 (simétrico em III?):** NÃO ao instrumento congelado: Teorema III-1 dá campo identicamente nulo
  (especificidade estrutural, determinística) (A+B+C). MAS é gume de faca de primeira ordem: a h2 o mesmo
  estatístico vê memória em 99,9% dos III (Teorema III-2) — qualquer extensão fora de h1 enfrentaria
  ambiguidade do lado III (A+C).
- **Q6 (uma classe ou várias?):** UMA classe mecanística (compatibilidade de τ com o perfil observável da
  geometria da aresta), com estratificação interna analítica (L1/L2 × células de (τ,lam)); clustering não
  encontra estrutura empírica adicional (B+C+E).
- **Q7 (natureza):** combinação precisa: **degenerescência rara** (colisões inteiras da geometria W sob τ;
  ~0,4-0,5%/instância) que produz **cancelamento por agregação**, i.e., **falha de identificabilidade do
  observável agregado** — uma violação de tipo-faithfulness relativa a C1′, de origem SIMÉTRICA (grupo
  Iso(W)) e não acidental-numérica; não é bug, não é escala, não é amostragem, não é suporte não realizado.
- **Q8 (pronto para o artigo):** ver secções 13, 15 e 20.
- **Q9 (perguntas antes de qualquer C1″):** ver secção 16.

**9.3 Critério de encerramento (B11).** (1) porquê: τ∈Iso(W_M) nas duas arestas — provado e verificado;
(2) onde: agregação intra-célula (B1/B2/B3), nunca inter-blocos; (3) dependência realizada: sim, estrita;
(4) condição de L1: K; (5) necessária e suficiente: sim (A, com recíproca não trivial); (6) simétrico em III:
não a h1 (teorema), sim em princípio fora de h1; (7) classes: uma; (8) matemática conhecida vs (9) resultado
específico: secção 22; (10) afirmações para o artigo: secções 13/15/20. **Nenhuma pergunta do critério fica
aberta**; as questões remanescentes (secção 16) são de extensão, não de fecho.

## 10. Condições necessárias/suficientes encontradas

| condição | enunciado | direcções | estatuto |
|---|---|---|---|
| K (L1) | d_0=d_1 ⟺ τ∈Iso(W_M) ⟺ W̃_0=W̃_1 | ambas | A+B+C+D |
| 'estado' (L1∪L2) | rank_canonico(d_0)=rank_canonico(d_1) ⟺ invariância ordinal do perfil sob transporte | ambas (definicional + recíproca pelo perfil) | A+B+C |
| dep=0 | tensor de padrões ρ-invariante (⟹K; recíproca falsa: 91/92 arestas de colapso têm dep>0) | ⟹ | A+B |
| Alinhamento (L2) | ψ(τ) fixa lam ⟹ colapso⟹L1 (L2 impossível); toda a L2 vive em T_out/FC_oth/C3 | ⟹ | A+B+C+D |
| V4 sem L2 | ρ∈V4 ⟹ multiconjunto de d conservado ⟹ L2 impossível | ⟹ | A+B |
| B4=0 | L1 nunca precisa de compensação entre blocos (igualdade célula a célula) | ⟹ | A+B+D |
| III h1 | variante III ⟹ campo XOR-intervencional ≡ 0 ⟹ fusão correcta | ⟹ (determinístico) | A+B+C+D |
| III h2 | composição destrói o cancelamento: dep2 genuíno (σ nos índices; selecção de linha K) | ⟹ genérico; zeros caracterizados parcialmente (linhas complementares: suficiência) | A+C |
| Direcção 2 (recíproca de K) | d determina W̃ (det −8; conjunto determinante) — depende do lattice COMPLETO das 9 intervenções | ⟹ | A+B+D |

## 11. Evidência contra explicações alternativas

- **Bug de implementação:** excluído — ≥4 implementações internas independentes (maquinaria congelada;
  fórmulas WS1/WS2/WS5; testemunhas WS3; scripts do coordenador) coincidem inteiro a inteiro em ~75000
  verificações de aresta somadas, com re-execuções byte-idênticas e replays com theta_sha exacto.
- **Artefacto de escala/estrato:** excluído — lema d_E2=4·d_E1 [A+B]; fam-20 reproduz 4608=4×1152.
- **Mecanismo não realizado / só contrafactual:** excluído — WS3 (9 sítios estritos/aresta na fam-20;
  padrão populacional 80-86%; PURO_CONTRAFACTUAL 0,25%).
- **Acaso amostral do desenho confirmatório:** o colapso é determinístico dado θ; a taxa ~0,46% prevê
  P(≥1 erro nas 75 II confirmatórias) ≈ 27-29% — o único erro em 200 é desfecho ordinário [C+E].
- **Múltiplas classes de falha:** desfavorecido — critério único + clustering sem estrutura robusta (WS5).
- **Tilt de elegibilidade / acoplamento extra entre arestas:** desfavorecido — frequências de classes ≈ a priori
  (WS1 S3), tilt |z|≤1,62, M3 sem parâmetros fecha a correlação (z≤0,6, replicado OOS) (WS5).
- **Ambiguidade simétrica do lado III:** excluída ao instrumento congelado (Teorema III-1) [A].
- **“Coincidência numérica sem estrutura”:** excluída — a condição é algébrica (grupo de isometrias), prevê
  taxas por classe via codimensão, prevê assinaturas L2 e a correlação inter-arestas, tudo confirmado OOS.

## 12. Limitações

1. **Toda a verificação é interna** (dados, código e agentes do mesmo workflow). Não houve replicação
   científica externa nem revisão humana independente; a concordância entre agentes é corroboração interna (B4).
2. Run2 de WS4/WS5 NÃO é cego face ao run1 (mesmo diretório); a independência analítica plena existe apenas
   no WS1 (firewall), e mesmo essa é atestação de workflow, não prova criptográfica de não-acesso (§21).
3. Domínio dos teoremas: gerador congelado (canal de 2 bits, π por memória de 1 bit, actualizações
   XOR-σ, lattice de 9 intervenções, fibra completa, horizonte 1). A prevalência 0,4-0,5% é da lei θ do
   gerador; não transfere automaticamente para outras distribuições.
4. Lemas parciais em aberto: imobilidade do bloco do(c=γ) em L2 sem Δm=0; “histogramas globais iguais ⟹
   blocos ≤B2” (174/174 empírico); margens L2 ≥64 envolvendo a classe nula; ordenação das taxas L2 por célula.
5. Resíduo M3 (+0,3 a +0,6σ, consistente em 3 conjuntos): provavelmente ruído; não fechado (≲10% do efeito).
6. dep=0 (7/20000): sem caracterização fechada nem fórmula de medida.
7. C2/C3 não autopsiados além do facto confirmatório (74/75 erros; ambos fundem a fam-20).
8. Estrato 2: transporte formal completo além do lema d (vias canal→D; contagens dep com bits D) não fechado.
9. **Prior art:** nenhuma pesquisa de literatura foi feita nesta execução; a auditoria de prior art decorre
   separadamente. Onde a novidade importa: *Scientific novelty pending completion of dedicated prior-art audit.*

## 13. O que está demonstrado

(A = prova analítica; com verificação B/C/D como indicado.)

1. Forma fechada e factorização: d_m = 2^(n-5)·(0,A,A,B,B,V); σ cancela; memória só via π_m; multiplicidade
   2^(n-5); d ↔ W̃ bijecção linear [A+B+D].
2. **K ⟺ L1** (τ∈Iso(W_M)); recíproca pelo conjunto determinante (det −8, posto 6) [A+B+C+D].
3. Marca 'estado' ⟺ invariância ordinal; fusão do núcleo ⟺ ambas as arestas 'estado' (contra `cl.classificar`) [A+B].
4. B4=0; quantum 64; invariância do multiset d[5..8]; impressão digital (0,a,a,b,b,·) [A+B(+C na minha amostra)].
5. Corolário V4-sem-L2; teorema do alinhamento e assinatura de valor de L2 (S(lam); dupla troca C3; bloco D imóvel) [A+B+C+D].
6. Localidade da resposta por (r,c); boa definição das comparações no suporte realizado; contraste observacional [A+B].
7. Teorema III-1 (III h1 ≡ 0; especificidade estrutural) e Teorema III-2 (a composição destrói o cancelamento) [A+B/C+D].
8. Direcção 2 depende do lattice: sub-lattices dão posto 2/4 e a recíproca falha (202 contra-exemplos concretos na minha amostra fresca) [A+B].
9. Na fam-20: W̃ equidistante na C_BA→A (Iso=S4); Iso={id,(23)} na C_AB→B com transporte ρ=(23);
   d_0=d_1 com dep=4608 e 9 sítios estritos por aresta [B+D, cálculo mostrado em §18.3].

## 14. O que permanece hipótese

(E = suportado/conjecturado; sem prova.)

1. Escalamento: prevalência de K cai rapidamente com alfabetos maiores (birthday de colisões inteiras).
2. Volumetria do modo B3 (70,9%) como consequência de contagem de restrições; ordenação T_out≫FC_oth>C3.
3. dep=0 e modos F1 associados a involuções (7/7 e 29/29 empírico; sem derivação).
4. Resíduo M3 +0,3-0,6σ = ruído (alternativa: acoplamento fino ≲10%).
5. Conjectura de saturação: dep_k cresce com o horizonte k≥2 até à escala de mistura; separação II/III como
   propriedade quase exclusiva da primeira ordem (não medido k≥3).
6. Fenómenos tipo-K a cada horizonte (os 30 cancelamentos agregados a h2) com geometria própria.
7. Assimetria B vs A (~2σ) nas taxas L1 por classe: ruído (a confirmar noutros lotes).
8. Heurística da dominância do ESTRITO (WS3) e acoplamento fraco K↔riqueza do suporte (não significativo).

## 15. Implicações para o artigo 1

- O facto principal é o **resultado confirmatório negativo** com o protocolo pré-registado cumprido; a autópsia
  entra como análise pós-confirmatória rotulada, com a taxonomia A-E explícita por afirmação.
- O que pode ser afirmado com segurança: as duas formulações finais da secção 20; o mecanismo (secção 9);
  a especificidade estrutural de III a h1 e o seu carácter de primeira ordem; a prevalência exploratória
  0,4-0,5% (IC por amostra); fam-20 como membro típico da classe modal.
- Rotular TODA a concordância entre agentes como verificação interna ao nível do workflow (nunca
  “independent replication”); distinguir prova analítica / enumeração / OOS / reprodução interna (secção 23).
- Não afirmar novidade científica de nenhum componente sem a auditoria de prior art:
  *Scientific novelty pending completion of dedicated prior-art audit.*
- Não incluir qualquer C1″, nem sugerir que o negativo “teria passado” sob outra operacionalização.

## 16. Questões que devem preceder qualquer C1″

1. Fórmula fechada de P(K | classe de τ) sob a lei de W (combinatória dos popcounts de M uniforme) e o seu
   escalamento com |alfabeto| e |memória| — quantifica o risco de colisão de QUALQUER agregado.
2. Caracterização fechada da sub-família dep=0 (invariância de padrões) e a sua medida.
3. Fecho dos lemas L2 (imobilidade sem Δm=0; histogramas F1.5; margens; ordenação por célula).
4. Fronteira sensibilidade/especificidade fora de h1: qualquer estatístico com horizonte ≥2 ou condicionado
   à órbita enfrenta o Teorema III-2 do lado III — qual é o trade-off exacto? (WS4 mostra que “fora de h1”
   começa imediatamente.)
5. Especificidade de III sob critérios estritos-realizados (a pergunta 3 da autópsia continua aberta).
6. Papel de C2/C3 nos mesmos colapsos (fundem a fam-20; mecanismo próprio não autopsiado).
7. Transporte formal completo da taxonomia ao Estrato 2 (além do lema d).
8. Resíduo M3 com N≈10^5 (fora do orçamento actual).
9. Medida das geometrias degeneradas (W equidistante; |∩_r Iso(w_r)|>1) sob θ elegível.
10. Assimetria B/A (~2σ) noutros lotes.

## 17. Q10 e domínio exacto do teorema

**17.1 Formulação mais geral autorizada (sem C1′, ESTADO/SINAL, II/III, gerador):**

> Sejam dois contextos m∈{0,1} cujos campos de resposta a um conjunto de intervenções são pull-backs de um
> tensor fixo por relabelings π_m de um alfabeto finito C (relabeling relativo τ=π1∘π0⁻¹), e seja W a
> geometria induzida no alfabeto por uma dissimilaridade dos padrões de resposta agregada por par
> (aqui: soma de Hamming por linha). Então:
> **(Direcção 1)** qualquer observável que compare os contextos APENAS através dos valores por par de W
> (i.e., que factorize pelo campo de células {W̃_m(c, sub_a(c))}) toma o mesmo valor nos dois contextos
> sempre que τ∈Iso(W) — mesmo quando os campos ponto-a-ponto diferem (X_0≠X_1): **falsa invariância por
> isometria**. A igualdade é célula a célula, logo vale para QUALQUER ponderação/função das células.
> **(Direcção 2)** se os agregados medidos formam um **conjunto determinante** de W̃ — como o lattice
> congelado: (A,B,V0..V3) com matriz de posto 6 e det −8 — então a recíproca vale: igualdade do observável
> ⟹ W̃_0=W̃_1 ⟹ τ∈Iso(W). O conteúdo identificável do contexto por tais observáveis é exactamente
> **W̃ módulo nada / τ módulo Iso(W)** — o quociente da geometria pelo seu grupo de simetrias.

**17.2 Domínio exacto (A4).** Estados: fibra completa com memória do receptor fixa; intervenções: reescrita
de subconjuntos dos bits do canal (o lattice congelado tem 9); contexto m: valor do bit de memória do
receptor; π_m: permutações do alfabeto do canal seleccionadas pela memória; τ=π1∘π0⁻¹; W=W_M(p,q)=
Σ_r pc2(M[r][p]⊕M[r][q]); Iso(W) = permutações do alfabeto que preservam W; F: qualquer função do campo de
células (o d congelado é o caso soma). **Hipóteses indispensáveis:** (i) a forma fechada — que requer:
resposta do receptor = R[r][π_m(c)]⊕σ[m], actualização de memória independente do canal, diferenciação XOR
(cancela σ), fibra alinhada; (ii) para a Direcção 2: a propriedade de conjunto determinante do lattice.
**Específicas deste gerador:** a identidade concreta de R (F0/G0), canal de 2 bits, 9 intervenções, n.
**Removíveis:** n (multiplicidade escalar); a métrica de Hamming (qualquer kernel por par dá a mesma
estrutura com o SEU Iso(W^κ)); o número de intervenções, DESDE QUE mantenham o posto 6. **Teorema sobre C1′**
vs **teorema sobre a classe**: C1′ é o caso F=soma com o lattice congelado, onde AMBAS as direcções valem;
a classe geral garante Direcção 1 sempre e Direcção 2 apenas com conjunto determinante.

**17.3 Auditoria da alegação “qualquer estatístico desta forma” (A5).** A alegação prévia era EXCESSIVA se
lida literalmente; o resultado exacto é:
1. NÃO “qualquer” estatístico: a impossibilidade prova-se para a classe que factoriza pelo campo de células
   de W̃. O d congelado está nessa classe E determina W̃ — por isso tem a caracterização exacta.
2. NÃO “qualquer soma de Hamming”: somas resolvidas por linha r são cegas apenas em ∩_r Iso(w_r)
   (36 das 705 arestas L1); multiconjuntos por célula, em Iso_multiset (210); o campo de padrões completo,
   apenas em dep=0 (7/20000). Cadeia estrita 7 ⊂ 36 ⊂ 210 ⊂ 705 [B].
3. Pesos não uniformes SOBRE CÉLULAS: a cegueira mantém-se (igualdade célula a célula — Direcção 1);
   pesos que resolvam linhas/bits saem da classe e encolhem o conjunto cego.
4. Outras métricas: substituir pc2 por qualquer kernel por par κ dá o mesmo teorema com Iso(W^κ).
5. Guardar a DISTRIBUIÇÃO (multiconjunto) em vez da soma: cegueira estritamente menor (210 vs 705) mas não nula.
6. Preservar a identidade dos termos (localização r): cegueira 36; ainda não nula.
7. **Classe MÁXIMA provável:** funcionais do campo de pesos por célula — para essa classe a impossibilidade
   com condição Iso(W) é teorema nas duas direcções (com conjunto determinante); qualquer alargamento é falso.

**17.4 Recíproca sob sub-lattices (B6, decidido):** as 9 intervenções NÃO observam directamente os 6 g.l. de
W̃ — observam A (par {01|23}), B (par {02|13}) e os 4 graus V(w); a entrada do par cego {03|12} (o “lam”)
só é forçada INDIRECTAMENTE pela conservação ΣV=2(A+B+C) e pela inversa explícita (e.g. e03 = −A/2 − B/2 +
(V0+V3)/2). Sem os do(c=γ): posto 2 (recíproca falsa); só com eles: posto 4 (falsa); com ambos: posto 6
(verdadeira). Empírico: 202/800 arestas frescas não-L1 têm ΔA=ΔB=0 — cegas ao d truncado sem serem
isométricas. A Direcção 2 é portanto não-trivial (propriedade do lattice), e a Direcção 1, dada a forma
fechada, é a invariância elementar de funções constantes em órbitas.

## 18. Toy model mínimo

**Estatuto: POST-CONFIRMATORY / ILLUSTRATIVE** — independente do código confirmatório; todas as contas
verificadas À MÃO (e cross-checked por `coord_a_linear_toy.py`).

**18.1 Definição.** Alfabeto C={0,1,2}; receptor com 2 linhas (r∈{0,1}) e saída de 1 bit:
M[0]=(0,0,1), M[1]=(0,1,0). Intervenções: do(c:=v), v∈{0,1,2}. Contextos: π0=id, π1=(12), τ=(12).
Campo de resposta: X_m(r; v,c) = M[r][π_m v] ⊕ M[r][π_m c]. Observável: d_m(v) = Σ_{r,c} X_m(r;v,c).

**18.2 Contas (à mão).**
- Geometria: W(p,q)=Σ_r |M[r][p]−M[r][q]| ⟹ W(0,1)=1, W(0,2)=1, W(1,2)=2.
- Iso(W): (01) falha (W(1,2)=2≠1=W(0,2)); (02) falha; 3-ciclos falham; **(12) preserva tudo ⟹ Iso(W)={id,(12)}**
  e τ=(12) é exactamente a isometria não trivial.
- Campos (linhas = (X(r=0),X(r=1))): contexto 0: X_0(v=1,c=0)=(0,1); contexto 1: X_1(v=1,c=0)=(1,0).
  As células (v,c) ∈ {(0,1),(0,2),(1,0),(2,0)} têm padrões DIFERENTES entre contextos (8 dos 18 sítios-linha
  mudam): a MESMA intervenção no MESMO ponto afecta a linha 1 do receptor num contexto e a linha 0 no outro —
  mudança causal real, ponto a ponto, “antes vs depois” explícito.
- Agregado: d_0 = (V(0),V(1),V(2)) com V=(2,3,3); d_1 = (V(τv)) = (V(0),V(2),V(1)) = **(2,3,3) = d_0**.
  Mais forte: os totais POR CÉLULA coincidem (W(τv,τc)=W(v,c)); a perda é exclusivamente a LOCALIZAÇÃO r
  (que linha responde) — o modo B2 do WS2, em miniatura.
- Recíproca no toy: V determina W (V0=w01+w02 etc., sistema 3×3 de det −2 ⟹ w01=(V0+V1−V2)/2, …), e a
  aplicação V é equivariante (V_{W∘(τ×τ)} = V∘τ) ⟹ d_0=d_1 ⟺ V∘τ=V ⟺ τ∈Iso(W). O toy exibe as duas
  direcções com álgebra de 3×3.

**18.3 Correspondência com a família 20 (A7, cálculo mostrado).** A fam-20 instancia a mesma estrutura com
|C|=4, 4 linhas, 2 bits:
- (i) **C_BA→A:** W̃ (obtido da tabela cega por TRÊS reconstruções independentes — autópsia, WS2, coordenador)
  tem TODOS os pares off-diagonais = 4. Qualquer permutação preserva trivialmente todas as distâncias ⟹
  **Iso(W)=S4 (|24|)** — a alegação verifica-se por definição de isometria, sem software.
- (ii) **C_AB→B:** W̃ = [[0,4,5,5],[4,0,3,3],[5,3,0,4],[5,3,4,0]]; graus V=(14,10,12,12). Uma isometria
  preserva graus ⟹ fixa 0 (grau 14, único) e 1 (grau 10, único); resta no máximo trocar {2,3}. Verificação
  da troca (23): W(0,2)=5=W(0,3) ✓; W(1,2)=3=W(1,3) ✓; W(2,3)↦W(3,2) ✓ ⟹ **Iso={id,(23)}, |2|**.
  O transporte extraído da tabela cega é ÚNICO: ρ=[0,1,3,2]=(23), com δ=3 — **τ é exactamente a única
  isometria não trivial**. (Na C_BA→A o mesmo ρ=(23) com δ=1, trivialmente em S4.)
- Consequência aritmética verificável à mão: d = 128·(0, A,A,B,B, V) com A=B=8 (pares 4+4 e 5+3) dá
  [0,1024,1024,1024,1024, 1792,1280,1536,1536] (V×128) na aresta B e [0,1024×4, 1536×4] na A — exactamente
  os vectores registados; e dep=4608=128×36 células discrepantes, com 9 células estritamente realizadas.

## 19. Hierarquia final das descobertas

| resultado | estatuto (B5) | generalidade |
|---|---|---|
| C1′ = 199/200; resultado negativo | FACTO CONFIRMATÓRIO (imutável) | bateria A deste pré-registo |
| Prevalência do colapso ≈0,46% (0,32-0,50% entre amostras) | C (+D) | gerador II congelado, lei θ elegível |
| d factoriza por W̃; bijecção d↔W̃; B4=0; quantum 64 | A+B+D | arestas canal→processador do gerador congelado (III = caso π=id) |
| **d_0=d_1 ⟺ τ∈Iso(W_M)** | Dir. 1: A (invariância); Dir. 2: A (conjunto determinante, det −8) + B(30k)+C(3 OOS)+D(4 implementações) | lattice congelado de 9 intervenções; Dir. 1 vale para toda a classe de observáveis de células |
| 'estado' ⟺ invariância ordinal; alinhamento (L2 só desalinhada); V4-sem-L2; assinatura S(lam) | A+B+C+D | idem; L2 depende também do desenho (par não sondado + rank) |
| L1 dominado pela agregação intra-célula (B1 4,2% / B2 24,9% / B3 70,9%); filtração 36⊂210⊂705 | A (operadores) + B (censo) + D | população N=10000 + minha amostra |
| Dependência estritamente realizada (9 sítios/aresta na fam-20; 80-86% em geral) | B+C+D | idem |
| Especificidade III: campo h1 ≡ 0 (Teorema III-1); gume de faca h2 (Teorema III-2, 99,9%) | A+B+C+D | h1: estrutural, todo o III elegível; h2: idem, excepções caracterizadas parcialmente |
| Correlação inter-arestas = partilha de (τ,lam); M3 sem parâmetros, resíduo ≤0,6σ | A(fórmula)+C+D | população do gerador |
| Falsa invariância por isometria (X_0≠X_1 com F igual) | A (toy + fam-20 + classe de células) | classe de observáveis que factorizam por W̃; FALSA para refinamentos |
| Implicação para individuação causal (fronteira ESTADO/SINAL não é invariante do sistema, mas do par {sistema, observável}) | INTERPRETAÇÃO (não teorema) | leitura conceptual |

## 20. Conservative claim e Strongest justified claim

**20.1 CONSERVATIVE CLAIM (apta ao escrutínio mais adversarial):**
> No teste confirmatório pré-registado, C1′ classificou correctamente 199 de 200 instâncias e o resultado
> confirmatório é negativo. A autópsia pós-confirmatória demonstra analiticamente — e verifica sem uma única
> excepção em ≥30000 arestas in-sample, três amostras fora-da-amostra pré-comprometidas e reexecuções
> internas por quatro implementações distintas — que, para o gerador e instrumento congelados, a igualdade
> dos perfis agregados de C1′ numa aresta canal→processador equivale exactamente a
> τ=π1∘π0⁻¹ ∈ Iso(W_M); que na instância falhada a dependência de memória era real e estritamente
> realizada na dinâmica visitada; que a perda ocorre na agregação intra-célula do somatório de Hamming; que
> a prevalência do fenómeno é ≈0,4-0,5% por instância II sob a lei do gerador; e que nenhuma instância III
> pode produzir o erro simétrico ao estatístico congelado (campo intervencional identicamente nulo a
> horizonte 1). Sustentam-na: os teoremas 13.1-13.7, as validações OOS 910000004/5/30/50/51 e a auditoria
> multiagente interna (não replicação externa).

**20.2 STRONGEST JUSTIFIED CLAIM (sem extrapolação):**
> Quando dois contextos causais diferem apenas por um relabeling π_m de uma interface finita, todo o
> observável que os compare através dos pesos agregados por par da geometria de resposta W é constante em
> órbitas do grupo Iso(W): se o relabeling relativo τ pertence a Iso(W), o observável coincide nos dois
> contextos apesar de os efeitos ponto-a-ponto diferirem — e, para o lattice congelado de nove intervenções,
> cujos agregados formam um conjunto determinante de W̃ (posto 6, det −8), a recíproca também vale, pelo que
> o estatístico identifica a modulação de contexto exactamente a menos de Iso(W). A classe para a qual a
> impossibilidade está provada é a dos funcionais do campo de pesos por célula; para observáveis mais finos
> (por linha, por multiconjunto, por padrão) o conjunto cego encolhe estritamente (36 ⊂ 210 ⊂ 705 nas
> 20000 arestas; 7 no limite do campo completo) e a generalização seria falsa. Sustentam-na: a forma fechada
> [A], o teorema do conjunto determinante [A], o toy model manual (§18), a instância confirmatória falhada
> como caso real, e as verificações B/C/D. A Direcção 1 é matemática clássica de invariância; a novidade de
> qualquer componente é *pending completion of dedicated prior-art audit*.

## 21. Comparação run1 vs run2 (WS4/WS5) e estatuto de independência do WS1

**21.1 Proveniência e hashes** (mtimes UTC do servidor; snapshot run1 congelado pelo orquestrador às 14:15:44Z;
run2 iniciado ~14:12Z; o run2 TINHA acesso aos ficheiros do run1 — não é cego nem independente):

| item | run1 (sha256; mtime) | run2 (sha256; mtime) |
|---|---|---|
| WS4 relatório | `f9cd27a459ee276b0ddad0bba6364d5c4b3588d540e40761f3ea64c151b9b0a3`; 13:40:57 | `ef95ce478825316d4a35b04d6ae0641ba2d9290c6be3808f5a5badac54c868b2`; 14:33:50 |
| WS5 relatório | `7a4696aaab8a26585bdea311c268da7a75a57a0a5409d74d44f6b493012fa77a`; 14:04:49 | `3a5e1048f8a4b3d531799ff5ce7c9c2884bbbdd5998f8fb852dfc643aebf17d4`; 14:32:32 |
| WS4 SHAS.txt | `118f30c5…`; 13:40:58 | `f7a72524…`; 14:33:52 |
| WS5 SHAS.txt | `9ca40f82…`; 14:05:07 | `4cc456bc…`; 14:32:34 |

WS2/WS3: run1 interrompido SEM relatório (restos em `tentativa-interrompida-1/`, com precommits); o run2
auditou e re-executou: outputs byte-idênticos (WS2 6/6; WS3 fam20 byte-idêntico, bateria igual excepto
`duracao_s`). WS1: uma única execução (13:42-14:03), não interrompida.

**21.2 Comparação WS4.** Reproduzido nas duas execuções: Teorema III-1, medição h1 0/4000, baselines
saturados, órbita 100%, contraste II. Apenas run2: auditoria A1-A3 (0 falhas), Teorema III-2 + medição h2
(precommit 14:28, anterior à execução), lema das linhas complementares. **Diferença de formulação com
consequência:** o run1 concluía que dentro da classe XOR-em-fibra-completa a recuperação de informação
“não pode” introduzir ambiguidade em III; o run2 demonstra que essa segurança se restringe a horizonte
exactamente 1 (a h2 o mesmo estatístico vê memória em 99,9% dos III). Classifico: h1 = reproduzido nas duas
execuções; h2 e a fronteira de horizonte = apenas run2; a formulação do run1 fica SUPERADA (compatível mas
demasiado forte se lida sem a restrição implícita de 1 transição). Sem contradições quantitativas.

**21.3 Comparação WS5.** Todas as conclusões e números do run1 preservados verbatim no run2 (46 casos,
teorema do alinhamento, escada M0-M3, OOS/RAW/taucheck, clustering, fam-20). Apenas run2: auditoria
independente de 2.ª passagem (29/29 PASS; semente 910000033 pré-comprometida) e F4-bis (as 225 arestas L2
populacionais 100% conformes; identidade S(lam) 193/193; bloco D imóvel 225/225). Zero divergências;
concordância = corroboração interna, não replicação.

**21.4 Estatuto do WS1 (firewall).** (i) O rascunho pré-firewall (`WS1-ALGEBRA-L1-DRAFT-prefirewall.md`,
sha `3b57fbab4ff7ffb532dac4efd7437acb621b3931e08f43117ef6f1a61aa1d1ef`, 13:55:46Z) contém a derivação
completa e o Teorema 5 na forma agregada — ρ=π0⁻¹∘π1, WM nos emparelhamentos, V∘ρ=V — **sem qualquer
menção a τ, Iso(W) ou aos ficheiros da análise prévia** (verifiquei por grep: as únicas ocorrências são a
declaração do firewall e o cabeçalho do §7 vazio); os outputs s10-s13 têm mtimes 13:42-13:48, anteriores ao
draft; os ficheiros prévios existiam desde 12:25-12:28. A auditoria NÃO pode provar criptograficamente a
não-leitura — o estatuto é: atestação ao nível do workflow + evidência circunstancial forte (formalismo,
notação e via de prova distintos). (ii) Formulação obtida: igualdade dos agregados {WM[ρ*(M1)], WM[ρ*(M2)],
V∘ρ}. (iii) Coincide matematicamente com d_0=d_1 ⟺ τ∈Iso(W_M): sim — o próprio WS1 provou a equivalência
(sistema 6×6, det −8), que eu re-provei de forma independente (coord_a: det −8, inversa explícita).
(iv) Classificação: **equivalente após mudança de notação** (com prova de equivalência, não apenas
semelhança); dado (i), conta como a verificação interna mais forte da Fase 6 — derivação independente ao
nível analítico dentro do mesmo workflow.

## 22. DECOMPOSIÇÃO DA CONTRIBUIÇÃO

**I. Matemática já conhecida.** Invariância de funções constantes em órbitas de uma acção de grupo (base da
Direcção 1); a noção de invariante maximal / quociente por grupo de simetrias (o “conteúdo identificável
= W̃ mod Iso” é um caso); conjuntos determinantes em álgebra linear (Direcção 2 é um cálculo de posto);
o homomorfismo ψ:S4→S3 com núcleo V4 (teoria de grupos clássica); paridade do popcount; equivariância de
somas marginais. Nada disto é novo enquanto matemática.

**II. Resultado matemático específico eventualmente novo** (elementar mas não tautológico; *scientific
novelty pending completion of dedicated prior-art audit*): a forma fechada d=2^(n-5)·(0,A,A,B,B,V) para o
passo II congelado com cancelamento de σ e inércia da memória; o teorema do conjunto determinante das nove
intervenções (det −8; o par cego determinado só indirectamente pela conservação); a bijecção d↔W̃ com B4=0;
o teorema do alinhamento (ψ(τ) fixa lam ⟹ L2 impossível) e a assinatura de valor S(lam); o corolário
V4-sem-L2; os Teoremas III-1/III-2 (cancelamento exacto de primeira ordem e a sua destruição pela
composição); a caracterização dep=0 = invariância do tensor de padrões.

**III. Descoberta causal.** Existe, com prevalência mensurável (~0,4-0,5% sob a lei do gerador), uma classe
de sistemas com modulação causal real, realizada e massiva ponto-a-ponto, que é INVISÍVEL a um observável
intervencional agregado — e a condição é exacta e simétrica: o remapeamento relativo entre contextos é uma
isometria da geometria de resposta. A invisibilidade não é ruído nem infidelidade genérica: é um subespaço
algébrico caracterizado, com taxas previstas por classe de conjugação e assinaturas verificáveis. A fronteira
de especificidade do lado III é uma propriedade de PRIMEIRA ORDEM do instrumento (h1) que a composição
temporal destrói.

**IV. Descoberta de individuação.** A fusão do núcleo na fam-20 mostra que a partição ESTADO/SINAL produzida
por C1′ não é um invariante do sistema causal subjacente mas do par {sistema, observável}: sob τ∈Iso(W), um
anel II com quatro módulos causalmente distintos é individuado como um III (fronteira causal colapsada),
embora a informação que os separa exista no próprio suporte realizado — abaixo do quociente W̃ (identidade
de bit, localização r, partição intra-célula) e fora do horizonte 1. (Interpretação conceptual apoiada nos
teoremas; não é, ela própria, um teorema.)

## 23. Taxonomia de independência e classificação A-E aplicada às conclusões

**Taxonomia (B4):** *independência de DADOS* — sementes novas pré-comprometidas (910000004/5, 910000010/20,
910000030-33, 910000050/51); *independência de IMPLEMENTAÇÃO* — fórmulas/rotas distintas da maquinaria
congelada (WS1 fórmula, WS2 site-level, WS3 testemunhas, WS5 audit-agent2, coordenador); *independência
ANALÍTICA INTERNA* — apenas WS1 (firewall; §21.4); *REPRODUÇÃO INTERNA* — tudo o resto (agentes com acesso
ao repositório comum, incl. run2 de WS4/WS5 face ao run1); *REPLICAÇÃO CIENTÍFICA EXTERNA* — **não ocorreu**.

**Rótulos finais por conclusão central:**
- K ⟺ L1 (τ∈Iso(W_M)): **A + B + C + D** (e derivação analítica interna independente do WS1).
- Bijecção d↔W̃, B4=0, quantum 64, impressão digital: **A + B + D**.
- Estágios B1/B2/B3 e filtração 36⊂210⊂705: **B + D** (operadores caracterizados analiticamente: A parcial).
- Realização estrita (fam-20 e população): **B + C + D**.
- Teorema III-1: **A + B + C + D**. Teorema III-2: **A + C + D**.
- Teorema do alinhamento + assinatura L2: **A + B + C + D**.
- Correlação = (τ,lam) partilhado, M3: **A(fórmula) + C + D**.
- Prevalência 0,46%: **C + D** (exploratória).
- fam-20 típica da classe modal: **B + C + D**.
- Escalamento com alfabeto, saturação de horizonte, volumetria B3, resíduo M3: **E**.

---

*Ficheiros do coordenador nesta área: `precommit-coordinator.txt`, `coord_a_linear_toy.py`,
`coord_b_fam20.py`, `coord_c_fresh_II.py`, `coord_d_fresh_III.py`, `coord_a.out`…`coord_d.out`,
`FASE6-MULTIAGENT-SYNTHESIS.md`, `SHAS.txt`. Sementes novas consumidas: 910000050, 910000051
(910000052-59 intactas). Nada fora desta área foi escrito; o instrumento e o confirmatório permanecem
intactos. POST-CONFIRMATORY / EXPLORATORY — a Fase 6 termina aqui; nenhuma C1″ é formulada e nenhum
passo seguinte é iniciado (B12).*

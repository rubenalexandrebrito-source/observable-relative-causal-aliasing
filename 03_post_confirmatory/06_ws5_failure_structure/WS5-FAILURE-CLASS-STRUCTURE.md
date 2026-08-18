# WS5 — ESTRUTURA DA CLASSE DE FALHA DE C1'

**ROTULO: POST-CONFIRMATORY / EXPLORATORY** — Pré-registo A v8.3, Fase 6 multiagente, workstream ws5-failure-structure.

**O resultado confirmatório permanece NEGATIVO e imutável**: `resultado_confirmatorio_A = "negativo"`; C1' obteve 199/200 (E1 150/150, E2 49/50); o único erro é a instância `7bb0baab3a8ed7aa` (família 20, variante II, Estrato 2, n=12). Nada neste relatório recalcula, reinterpreta ou atenua esse resultado. Nenhum artefacto confirmatório foi tocado. Este documento é diagnóstico mecanístico da classe de falha, sem qualquer proposta de correcção de C1'.

- Data: 2026-08-17. Área de escrita: `/root/causal-A-postconfirmatory-analysis/multiagent/ws5-failure-structure/` (única área escrita, além do scratch local do agente).
- Sementes novas usadas (todas do intervalo atribuído 910000030..39, todas pré-comprometidas ANTES de correr): 910000030 (OOS elegível, N=5000; `precommit-ws5-oos.txt`, sha256 `7edc4d39...`, registado 2026-08-17T13:53:16Z), 910000031 (RAW sem elegibilidade, N=20000; mesmo precommit), 910000032 (sanity check da lei de tau, N=200000; `precommit-ws5-taucheck.txt`, sha256 `35fba111...`, registado 13:59:10Z), e 910000033 (auditoria de 2.ª passagem: busca determinística de contraexemplo da consequência do teorema do alinhamento, 200 matrizes W × todos os tau alinhados; `precommit-ws5-audit.txt`; NÃO é amostra estatística — nenhuma taxa é estimada dela). O replay dos lotes 910000001/910000002 é reconstrução determinística de dados JÁ REGISTADOS (não é amostra nova).
- Integridade: `sha256sum frozen-copy/*.py` coincide 12/12 com `multiagent/shared-readonly/MANIFEST.txt` (verificado antes de qualquer uso).
- Pergunta do mandato: os 46 colapsos em 10000 são UMA classe estrutural ou várias? O mecanismo de L2 é o de L1 em versão parcial? O que explica a correlação ~2,1–2,4x entre as duas arestas?

## Sumário executivo (5 pontos)

1. **Uma só classe mecanística, com taxonomia interna analítica.** Os 46 colapsos são todos instâncias do mesmo fenómeno: o remapeamento partilhado tau = pi1∘pi0^{-1} é compatível com o perfil observável da geometria W de CADA aresta — exactamente (L1: tau ∈ Iso(W)) ou apenas ordinalmente (L2). Não há classes empíricas robustas além dos estratos analíticos: o clustering sem k fixado dá estrutura fraca (silhueta máx. 0,41) e instável entre linkages (ARI 0,21–0,54), e NÃO alinha com o subtipo L1/L2 (ARI = −0,13).
2. **Teorema novo (alinhamento):** com psi: S4→S3 a acção nas 3 emparelhações perfeitas (núcleo = grupo de Klein V4), se psi(tau) fixa a emparelhação NÃO sondada lam, então L2 é impossível (colapso ⟹ L1). Corolários: L2 inexistente em T_in, DT_lam, DT_oth, FC_lam; toda a aresta L2 vive em T_out, FC_oth ou C3. Verificado: 0 arestas L2 em 6102 (in-sample) + 3018 (OOS) + 12270 (RAW) arestas de células alinhadas; e as 24 arestas L2 dos 46 casos mudam SEMPRE exactamente as 2 posições de UMA soma de emparelhação — a assinatura prevista; na população completa, as 225 arestas L2 seguem 100% a taxonomia prevista, com o valor novo sempre igual à soma da emparelhação cega e o bloco D universalmente inalterado (F4-bis).
3. **L2 é a versão ordinal do mesmo mecanismo de L1, mas relativa ao instrumento**: o conjunto de 9 intervenções sonda 2 das 3 emparelhações; tau contrabandeia a soma da emparelhação cega (lam) para uma posição sondada com valor diferente mas o MESMO lugar na ordem fraca. 17/24 arestas L2 têm Iso(W) trivial — L2 não é "uma simetria exacta mais pequena", é simetria do perfil observado.
4. **A correlação entre arestas está explicada quantitativamente**: as duas arestas partilham (tau, lam) e têm geometrias W independentes. A escada de modelos dá, in-sample: independência 21,6; modelo por classe 39,0 (1,81x); por 7 células 39,8 (1,84x); geometria exacta por família (M3 = Σ(|EqB∩EqA|−1)/23) 44,0 (2,04x) contra 46 observados (z=0,31). OOS pré-comprometido: 24 obs vs M3 21,4 (z=0,57); both-L1 16 vs 13,9 (z=0,58). Não sobra resíduo que exija outra propriedade; dentro de cada célula as duas arestas são independentes (Fisher todos n.s.; único p=0,018 em FC_oth in-sample não replica OOS).
5. **fam-20 é um membro típico da classe**, não um caso raro à parte: subtipo (L1,L1) — o subtipo modal (29/46) — com o padrão "uma aresta equidistante forçada (|Iso|=24) × uma aresta seleccionada (|Iso|=2, tau = a transposição certa)"; o par (2,24) ocorre em 2 dos 29 (L1,L1) in-sample e ≥1 aresta equidistante em 5/29.

---

## 1. Materiais, proveniência e auditoria do trabalho prévio

Ficheiros produzidos (todos em `ws5-failure-structure/`, sha256 em `SHAS.txt`):

| ficheiro | conteúdo |
|---|---|
| `ws5_replay.py`, `ws5_replay.log` | replay determinístico dos lotes 910000001/2 + extracção de características + auditorias |
| `ws5-familias-N10000.json` | 10000 famílias: célula, níveis por aresta, |Iso|, n_eq, intersecções |
| `ws5-casos46.json` | os 46 casos com detalhe completo (pi0, pi1, tau, W, perfis, d, dep, órbita) |
| `ws5_analise46.py`, `ws5-analise46.json`, `ws5_analise46.log` | lema de necessidade, características, mecanismo L2, fam-20, clustering |
| `ws5_correlacao.py`, `ws5-correlacao.json`, `ws5_correlacao.log` | escada de modelos M0–M3, efeito-lam, tilt, independência condicional |
| `precommit-ws5-oos.txt` | pré-compromisso OOS/RAW (ANTES da execução; P1–P7) |
| `ws5_oos.py`, `ws5-oos.json`, `ws5_oos.log` | OOS 910000030 + RAW 910000031 + avaliação P1–P7 |
| `precommit-ws5-taucheck.txt`, `ws5_taucheck.py`, `ws5-taucheck.json` | sanity check da lei de tau (910000032) |
| `precommit-ws5-audit.txt`, `ws5_audit_agent2.py`, `ws5-audit-agent2.json` | auditoria de 2.ª passagem (implementação independente; ver abaixo) |
| `WS5-FAILURE-CLASS-STRUCTURE.md`, `SHAS.txt` | este relatório e o manifesto de shas |

Auditoria das alegações do agente único que este WS reutiliza (regra: verificar o que se usa):

| alegação prévia | resultado da auditoria WS5 |
|---|---|
| d_m = 32·Σ_c Wtil_m(c, sub_a(c)); sigma cancela; multiplicidade 32 | REPRODUZIDA: verificação maquinaria-vs-fórmula exacta em 164 famílias auditadas (0 falhas) e, ao nível de contagens, os níveis por fórmula reproduzem exactamente os totais registados (L1=705, L2=225, L3=19070) |
| K ⟺ L1 sem excepções (TP 370/335, FP=FN=0) | REPRODUZIDA: consistência estado⟺(pi1∈classe-de-rank) e L1⟺(tau∈Iso) verificada 20000/20000; os meus totais L1 por aresta = 370/335 |
| Necessidade via sistema das 9 intervenções | RE-PROVADA independentemente: eliminação de Gauss exacta sobre Q, rank 6, núcleo trivial (secção 3.2) |
| fam-20: Wtil iguais nos dois contextos; C_BA→A equidistante (todos 4); C_AB→B com grupo {id, transposição} | CONFIRMADA a partir das matrizes Wtil publicadas (obtidas da tabela cega): |Iso| = 24 e 2; graus [10,12,12,14] na C_AB→B |
| Correlação: obs 29 both-L1 (2,34x), modelo por classe 1,91x | REPRODUZIDA exactamente (M1 = 23,65 = 1,908x; obs 29 = 2,34x) |
| "W com simetria mas K falso": 4620 / 4619 | REPRODUZIDA exactamente pelo meu replay independente |

Contadores de auditoria do replay (`ws5_replay.log`): `cell_agree` 10000/10000 (célula por (tau,lam) ≡ célula por órbita-D4 de rho); `coset` 80/80; `estado_consistente` 20000/20000; `maquinaria` 164/164; `stored_match` 126/126 (46 colapsos + 80 controlos: theta_sha, níveis, d0/d1, dep_sites TODOS iguais aos registados); `sha` 126/126. O conjunto {(seed,tentativa)} dos meus colapsos coincide exactamente com o registado.

**Auditoria de 2.ª passagem (implementação independente; `ws5_audit_agent2.py`, resultados em `ws5-audit-agent2.json`): 29/29 verificações PASS.** Reimplementação de raiz (sem reutilizar código dos scripts ws5_*, apenas o instrumento congelado) que verificou: (A0) a ordem congelada das 9 intervenções e a estrutura [0,P1,P1,P2,P2,D0..D3] com emparelhação cega M_C; (A1) o teorema do alinhamento por enumeração exaustiva (69 combos (tau,lam): psi(tau) fixa lam ⟺ célula ∈ {T_in, DT_lam, DT_oth, FC_lam}) e a sua consequência (multiconjunto do perfil invariante; zero L2 possível) em 200 geometrias W × todos os tau alinhados (semente 910000033, pré-comprometida; busca de contraexemplo, não amostra); (A2) o lema de necessidade re-re-provado (rank 6, eliminação exacta em Q); (A3) reprodução campo-a-campo das 10000 linhas de `ws5-familias-N10000.json` (0 divergências) e das contagens de células; (A4) via da maquinaria congelada (tabela de transição + fibra `cl.*`) para TODOS os 46 casos — theta_sha, pi0/pi1/tau, célula, subtipo, W, |Iso|, n_eq, d0/d1, dep_sites e órbita idênticos a `ws5-casos46.json` (46/46) — e para as famílias-controlo determinísticas (fam_global % 67 == 0; 195 famílias auditadas no total incluindo os colapsos, fórmula ≡ maquinaria em todas); (A5) recomputação independente de TODOS os agregados de F5/F6/F7 (histogramas |Iso|, 4620/4619, 60 forçadas, tilts 360,5/362,7/467,9/462,8, escada M0/M1/M2/M3 e Fisher FC_oth) com coincidência exacta com `ws5-correlacao.json` e com este relatório; (A6) estatísticas dos 46 (órbitas 7/21/40; dep 0..2048 e 384..2048; 11 sigmaA; dep=0 apenas em 910000001/14155 aresta B). Determinismo: re-execução de `ws5_analise46.py` e `ws5_correlacao.py` reproduz byte a byte os JSON publicados (sha256 idênticos). O campo `sem_dependencia_ponto_a_ponto` dos lotes de prevalência dá 4+3=7 arestas com dep=0 em 20000 (fonte do facto em F3); `anomalias_mem_reach`=0 nos dois lotes. A 2.ª passagem acrescentou um facto novo à população (F4-bis abaixo).

---

## 2. FACT — factos verificados por máquina

**F1. Reconstituição.** O replay determinístico (fluxo `SeedSequence(S).spawn(4)[0]`, contador por CADA theta amostrado) reproduz integralmente os dois lotes: 5000+5000 aceites em 17135+16845 tentativas; os 46 colapsos coincidem em identidade (theta_sha), níveis, vectores d e dep_sites.

**F2. Estrutura do estatístico.** As 9 intervenções de um módulo de 2 bits são, na ordem congelada, `[(0,0),(lo,0),(lo,1),(hi,0),(hi,2),(full,0),(full,1),(full,2),(full,3)]`. O vector d_m tem SEMPRE a forma `[0, P1, P1, P2, P2, D0, D1, D2, D3]` com P1/P2 as somas de W sobre as duas emparelhações sondadas (imagens por pi_m das emparelhações canal {{0,1},{2,3}} e {{0,2},{1,3}}) e D_w = grau de pi_m(w) em W; e d_m = 32·S_m (n=10; em E2, ×4 pelo lema d_E2=4·d_E1 já verificado na Fase 6).

**F3. Os 46 casos.** Subtipos ordenados (aresta B=C_AB→B, A=C_BA→A): (L1,L1)=29, (L1,L2)=5, (L2,L1)=5, (L2,L2)=7. Classes de tau: transposição 33, dupla-transposição 10, 4-ciclo 3, 3-ciclo 0. Células: T_out 26, T_in 7, DT_oth 7, DT_lam 3, FC_oth 3, FC_lam 0, C3 0. Cruzamento célula×subtipo: TODOS os 17 casos com alguma aresta L2 estão em T_out (15) ou FC_oth (2); T_in/DT_lam/DT_oth são 100% (L1,L1). Órbitas (n=10): mín 7, mediana 21, máx 40. dep_sites: 0..2048 (aresta B) e 384..2048 (aresta A), com UM caso de dep=0 (910000001/14155, DT_oth, aresta B: cancelamento ao nível do padrão, não só da soma — o extremo absoluto da classe; 7 arestas em 20000 têm dep=0). Controlo negativo: sigmaA/sigmaB sem concentração (11 pares sigmaA distintos em 46) — como esperado, sigma cancela no estatístico.

**F4. Geometria das arestas dos 46.** Arestas L1 (68): |Iso(W)| ∈ {2:40, 4:8, 6:4, 8:11, 24:5}; 5 equidistantes; nº de valores distintos do perfil ∈ {3:10, 4:28, 5:29, 6:1}. Arestas L2 (24): |Iso| ∈ {1:17, 2:2, 4:5} — 17/24 SEM nenhuma simetria exacta; 0 equidistantes; classes de rank pequenas (n_eq ∈ {2:8, 3:9, 4:2, 8:1, 12:4}); graus-regulares 5/24. Em TODAS as 24 arestas L2, exactamente 2 das 9 posições do perfil mudam de valor, e são sempre as duas posições duplicadas de UMA soma de emparelhação: P1 (posições 1,2) em 10 arestas, P2 (posições 3,4) em 14.

**F4-bis. Assinaturas L2 na população completa (225 arestas L2 in-sample; 2.ª passagem).** Distribuição das posições alteradas do perfil, 100% conforme a teoria (3.4/3.5): T_out 159 (77 mudam o par P1, 82 o par P2) e FC_oth 34 (19×P1, 15×P2) mudam EXACTAMENTE um par P, e o valor novo é SEMPRE a soma da emparelhação cega S(lam) (identidade verificada aresta a aresta, 193/193); C3 32/32 mudam os DOIS pares P (a "dupla troca" prevista para psi(tau) 3-ciclo — sem nenhum caso de igualdade acidental de somas); o bloco D (posições 5–8) NUNCA muda em nenhuma das 225 — a preservação dos graus não é só típica, é universal na amostra. As 24 arestas L2 dos 46 colapsos são o subconjunto T_out/FC_oth disto (F4).

**F5. População (20000 arestas in-sample).** |Iso|>1 em ~50% das arestas (4990 B, 4954 A); "W simétrico mas tau falhou" = 4620 (B) / 4619 (A). Dos 705 L1, só 60 (8,5%) são geometricamente forçados (|Iso|=24); histograma |Iso| (B): {1:5010, 2:4102, 4:534, 6:169, 8:157, 24:28}. Identidades de calibração: Σ(|IsoB|−1)/23 = 360,5 vs 370 L1 observados (z=+0,55); Σ(|neqB|−1)/23 = 467,9 vs 475 estado (z=+0,37); análogos A: 362,7 vs 335 (z=−1,62); 462,8 vs 455 (z=−0,41).

**F6. Escada de correlação (in-sample, alvo estado=colapso C1', obs=46).** M0 independência 21,61 (obs/M0 = 2,13); M1 por classe de tau 39,01 (1,81x; z=+1,12); M2 por 7 células 39,75 (1,84x; z=+0,99); M3 geometria exacta por família Σ(|EqB∩EqA|−1)/23 = 44,00 ± 6,34 (2,04x; z=+0,32). Alvo both-L1 (obs=29): M0 12,40 (2,34x); M1 23,65 (1,91x; z=+1,10); M2 23,67; M3' Σ(|IsoB∩IsoA|−1)/23 = 28,04 ± 5,10 (2,26x; z=+0,19). Independência condicional dentro de células (Fisher bicaudal): T_out 0,82; T_in 0,48; DT_oth 0,35; DT_lam 0,76; FC_lam 1,0; C3 1,0; FC_oth 0,018 (único nominalmente <0,05 em 7 testes; NÃO replica OOS — 0 colapsos FC_oth OOS).

**F7. Efeito-lam por classe (in-sample).** L2: T_out 68/1780 (B) e 91/1780 (A) vs T_in 0/835+0/835 (Fisher p<1e-12); FC_oth 22/1718 e 12/1718 vs FC_lam 0/895+0/895 (p=0,00014 / 0,011); DT 0 L2 nas duas sub-células; C3 15 (B) / 17 (A) L2. L1 é PLANO no lam: T p=1,0 (A) / 0,25 (B); DT p=0,82/0,59; FC p=0,24/0,28.

**F8. OOS pré-comprometido (910000030, N=5000, 17046 tentativas; auditoria maquinaria 34/34 ok).** Colapsos 24 (taxa 0,48% vs 0,46% in-sample): T_out 16 (9 L1L1 + 1 (L1,L2) + 5 (L2,L1) + 1 (L2,L2)), T_in 3 (L1,L1), DT_lam 2 + DT_oth 2 (L1,L1), C3 1 (L2,L2) — o primeiro colapso de 3-ciclo alguma vez observado, e é (L2,L2). Predições: P1 (0 L2 em células alinhadas) CUMPRIDA; P2 (q fixos) z global B −1,75, A −0,87; P3 obs 24 vs M2-congelado 19,2 (z=1,09) e M3 21,4 (z=0,57); P4 both-L1 16 vs M3' 13,9 (z=0,58); P5 DT_lam=DT_oth (p=0,75/1,0); P6 T_out é a maior taxa L2 (0,036/0,037), FC_oth>0 (0,0024/0,0072), alinhadas 0.

**F9. Controlo RAW (910000031, N=20000 sem elegibilidade).** 0 L2 nas 12270 arestas de células alinhadas. both-L1 59 obs; modelo por classe 50,5; M3' 47,9 ± 6,7 — no RAW o modelo por classe e o geométrico coincidem (diff −2,6), como a independência exacta exige; taxas por célula quase iguais às elegíveis (ex.: T_out raw 0,123/0,114 vs OOS 0,121/0,113) — a elegibilidade quase não move os q.

**F10. Sanity check da lei de tau (910000032, N=200000).** Classes: z ∈ {−0,10 (T), +1,59 (C3), −1,33 (DT), −0,61 (FC)}; sub-células nas fracções 1/3–2/3 correctas. O défice C3 do RAW-910000031 (6709 vs 6956,5; z=−3,7) fica documentado como flutuação da semente (o caminho de amostragem está correcto); nenhum resultado condicional depende disso.

**F11. Clustering (46 casos, Gower, 3 conjuntos de features × 3 linkages).** Melhor silhueta: nuclear/average k=3 (0,4125); salto sugere k=5; complete sugere k=2 (salto) ou k=8 (silhueta 0,387); single k=4. Estabilidade: ARI average-vs-complete 0,21; vs single 0,54; nuclear-vs-alargado 0,79; nuclear-vs-geometria 0,84. A partição de referência (k=3) compõe-se: C0 n=3 (todos (L1,L1), uma aresta |Iso|=24), C1 n=33 (transposições, |Iso| pequenos, TODOS os subtipos misturados), C2 n=10 (DT+FC, |Iso| médios, 8 L1L1 + 2 L2L2). ARI da partição vs subtipo = −0,13; vs classe de tau = +0,52; vs padrão-forçado(|Iso|=24) = +0,42.

**F12. fam-20 (referência; SEM tocar sementes proibidas — usa as matrizes Wtil já extraídas da tabela cega na Fase 6).** C_AB→B: W=[[0,4,5,5],[4,0,3,3],[5,3,0,4],[5,3,4,0]], off-diag {3,3,4,4,5,5}, graus [10,12,12,14], |Iso|=2 ({id, transposição}); C_BA→A: equidistante (todos os pares 4), |Iso|=24. Subtipo (L1,L1). Como Iso(W_B)∩Iso(W_A)∋tau e Iso(W_B)={id,t}, tau = t: classe transposição (na base re-rotulada do canal). dep 4608 por aresta e órbita 25 no regime n=12 (factos confirmatórios dados).

---

## 3. DERIVATION — derivações analíticas (com estado de prova)

**3.1 Forma exacta do estatístico (recap, auditada).** No passo II, y' = G0[y][pi_mB(cAB)] ⊕ sigmaB[mB] e mB' = K[mB][y] não lê o canal. No XOR contrafactual o sigma cancela e mB' cancela; cada par (estado-receptor r, valor-canal c) tem multiplicidade 32 na fibra n=10. Logo d_m(a) = 32·Σ_c Wtil_m(c, sub_a(c)) com Wtil_m(c1,c2) = W_M(pi_m c1, pi_m c2), W_M(p,q) = Σ_r pc2(M[r][p]⊕M[r][q]), M=G0 na aresta C_AB→B e M=F0 na C_BA→A. Pela estrutura das 9 intervenções (F2), o perfil é [0, P1,P1, P2,P2, D0..D3]. [Prova por expansão directa; verificação exaustiva em F1/F5.]

**3.2 Lema de necessidade (re-provado).** Para Delta = Wtil_1−Wtil_0 (simétrica, diagonal nula, 6 g.l. e_{c1c2}), d0=d1 impõe: linha nula da intervenção nula; e01+e23=0 (×2); e02+e13=0 (×2); somas-linha nulas nas 4 intervenções do(c=w). Eliminação exacta sobre Q: rank 6 ⟹ Delta=0. Logo **L1 ⟺ Wtil_0=Wtil_1 ⟺ tau ∈ Iso(W_M)**, com Iso(W) o grupo de isometrias do grafo pesado W. Lema do coset: {p: Wtil(p)=Wtil(pi0)} = Iso(W)∘pi0, de cardinal |Iso(W)| (verificado 80/80).

**3.3 Evento 'estado' e estatística suficiente exacta.** 'Estado' na aresta ⟺ rank_canonico(perfil(pi0)) = rank_canonico(perfil(pi1)) ⟺ pi1 ∈ EqClass(W, pi0). Por invariância à esquerda (relabeling dos vértices, lei de W invariante), a probabilidade do evento depende de (pi0,pi1) apenas através de rho = pi0^{-1}∘pi1; e as classes de equivalência de rho sob a simetria residual são as órbitas de conjugação por D4 = Stab(M_C) (|D4|=8): **7 células** = {T_in, T_out} (transposições com aresta dentro/fora de lam), {DT_lam, DT_oth}, {FC_lam, FC_oth} (4-ciclos com emparelhação fixa igual/diferente de lam), {C3} (3-ciclos), onde lam = pi0({{0,3},{1,2}}) é a emparelhação NÃO sondada pelo conjunto de intervenções, e tau = pi1∘pi0^{-1}. As DUAS arestas da mesma família partilham (tau, lam); as geometrias W_G, W_F são independentes. [Prova algébrica; verificação: rótulo por (tau,lam) ≡ rótulo por órbita-D4 de rho, 10000/10000.]

**3.4 TEOREMA DO ALINHAMENTO (novo).** Seja psi: S4→S3 a acção nas 3 emparelhações perfeitas; ker(psi) = V4 (Klein). Se psi(tau) fixa lam — equivalentemente, tau estabiliza o PAR sondado {mu,nu} — então o perfil de m=1 é uma permutação posicional dos valores do perfil de m=0 (P-bloco fixo ou trocado; D-bloco permutado por tau). Multiconjuntos iguais + formas de rank iguais ⟹ igualdade posição a posição ⟹ d0=d1 ⟹ (3.2) Wtil_0=Wtil_1. **Logo: em célula alinhada, colapso ⟹ L1; L2 é impossível.** Corolários: (i) psi(transposição) fixa a emparelhação que contém a sua aresta ⟹ T_in sem L2; (ii) psi(DT)=id fixa TUDO ⟹ DT sem L2 nas DUAS sub-células, e a lei do evento é idêntica em DT_lam e DT_oth; (iii) FC_lam sem L2; (iv) toda a aresta L2 tem psi(tau)(lam)≠lam ⟹ células T_out, FC_oth ou C3. [Prova completa; suporte empírico: F4, F7, F8-P1, F9 — 0 excepções em 21390 arestas alinhadas somando os três conjuntos.]

**3.5 Mecanismo de valor de L2 (troca de emparelhação pela zona cega).** Em célula não alinhada, psi(tau) envia exactamente uma emparelhação sondada M_x para lam: o valor da posição correspondente muda de S(M_x) para S(lam) (2 posições duplicadas). Para preservar a ordem fraca é preciso, além do slot ordinal de S(lam) coincidir com o de S(M_x): valores D preservados — o que tau força por igualdades de graus (transposição (ab): deg a = deg b; 4-ciclo: os 4 graus iguais; 3-ciclo: 3 graus iguais e dupla troca nos P — mais exigente). Assinatura prevista: exactamente 2 posições alteradas, sempre um par P — observado em 24/24 (F4). Exemplo real (910000001/6365, C_BA→A, tau=(23), T_out): graus (14,14,14,18) com deg2=deg3; somas de emparelhação (8,10,12), sondadas 8 e 10, lam=12; S0=[0,8,8,10,10,18,14,14,14] → S1=[0,8,8,12,12,18,14,14,14]: o 10 é substituído pelo 12 da emparelhação cega, mesmo lugar ordinal (entre 8 e 14), rank igual, d diferente.

**3.6 Probabilidades exactas por família.** Dado (W_B, W_A, pi0) e pi1 uniforme em S4\{pi0}: P(colapso) = (|EqB∩EqA|−1)/23; P(both-L1) = (|IsoB∩IsoA|−1)/23 (via lema do coset). Estas identidades definem o modelo M3 (sem parâmetros livres) e os diagnósticos de tilt de elegibilidade (F5): a elegibilidade quase não perturba a uniformidade de pi1 dada a geometria (|z|≤1,62).

**3.7 Porque há correlação entre as arestas.** As arestas partilham (tau, lam) e ambas contêm pi0 nos seus conjuntos de colapso, que são estruturados (cosets de subgrupos para L1). A correlação é Jensen sobre a heterogeneidade de q(célula) MAIS a sobreposição grupal por família (|EqB∩EqA| ≥ estrutura de subgrupos comuns): a escada M0→M1→M2→M3 quantifica cada contributo (F6). No RAW, M1≈M3 (F9), confirmando que M3 não introduz viés.

---

## 4. EMPIRICAL SUPPORT — correspondência derivação ↔ medição

| derivação | suporte |
|---|---|
| 3.1 fórmula d=32·S | 164 famílias maquinaria-vs-fórmula sem falha (F1); reprodução exacta dos totais registados L1/L2/L3 e dos 46 d-vectores; (+20000 arestas do agente único, auditadas por reprodução) |
| 3.2 K⟺L1 | consistência 20000/20000; contagens L1 370/335 = TP prévios; coset 80/80 |
| 3.3 células | rótulos (tau,lam) ≡ órbitas-D4 10000/10000; frequências de células compatíveis com a lei uniforme (e F10) |
| 3.4 alinhamento | 0 L2 em 6102+3018+12270 arestas alinhadas; DT_lam≡DT_oth (p 0,59–1,0 nos três conjuntos); L1 plano no lam (F7); OOS P1/P5 cumpridas |
| 3.5 troca pela zona cega | 24/24 arestas L2 com exactamente o par P alterado (10×P1, 14×P2); população 225/225 conforme (F4-bis: um par P + valor=S(lam) em T_out/FC_oth 193/193, dupla troca em C3 32/32, bloco D inalterado 225/225); graus-regulares nas L2 de 4-ciclo; L2 concentrado em T_out≫FC_oth,C3 (F7, P6 OOS) |
| 3.6/3.7 correlação | escada in-sample (F6), OOS (F8: z≤1,1 nos modelos, z≤0,6 no M3), RAW (F9: M1≈M3); tilt |z|≤1,62; independência condicional dentro de células (F6) |

---

## 5. INFERENCE — respostas às perguntas do mandato

**(1) Uma classe ou várias?** UMA classe mecanística: falha de individuação de C1' na aresta canal→processador ⟺ pi1 pertence à classe-de-rank de pi0 do perfil W observável — um único critério, cuja estratificação interna é ANALÍTICA, não empírica: estrato exacto (L1 = isometria; 68 arestas) vs estrato ordinal (L2 = ordem-isomorfismo do perfil sondado; 24 arestas), cruzado com a taxonomia de células (tau, lam). O clustering sem k a priori NÃO encontra classes discretas robustas (silhueta ≤0,41; ARI entre linkages até 0,21; ARI vs subtipo −0,13): os agrupamentos que aparecem seguem a classe de tau e a permissividade da geometria (|Iso|), i.e., são um contínuo dentro da mesma classe, organizado pelos eixos analíticos. As divisões discretas verdadeiras (alinhado/não-alinhado; DT fundida) são teoremas, e o clustering não as contradiz.

**(2) L2 = L1 parcial?** Sim e não, com precisão: é o MESMO tipo de fenómeno — compatibilidade do tau partilhado com a estrutura da aresta — mas ao nível do PERFIL OBSERVADO pelo instrumento, não da métrica W: (i) 17/24 arestas L2 têm Iso(W)={id} — não existe simetria exacta parcial subjacente; (ii) L2 só existe através da zona cega do conjunto de intervenções (a emparelhação não sondada) mais a coarsening ordinal do rank; (iii) L2 exige alinhamento psi(tau)(lam)≠lam — uma condição de fase entre tau e pi0 que L1 ignora. Portanto: mesma família causal (simetria sob o remapeamento), grau de exigência diferente (métrica vs ordinal), e o estrato ordinal é uma propriedade conjunta {dinâmica θ + desenho do instrumento}.

**(3) Correlação 2,1–2,4x.** Explicada pela partilha de (tau, lam) com geometrias independentes: o modelo por classe de tau já dá 1,81–1,91x; a célula-7 acrescenta pouco (o efeito-lam é forte em L2 mas L2 é minoritário); o modelo exacto por família (M3, sem parâmetros) dá 2,04x (estado) e 2,26x (both-L1) vs 2,13x/2,34x observados — resíduos z=0,32/0,19 in-sample, replicados OOS (z=0,57/0,58). Dentro das células as arestas são independentes; o tilt de elegibilidade é nulo dentro do erro; no RAW o modelo por classe já fecha. Conclusão: NÃO é necessária (nem suportada) qualquer propriedade adicional de theta para explicar a correlação; a propriedade partilhada é (tau, lam) e, residualmente, a sobreposição exacta dos conjuntos de simetria por família — que é consequência determinística de (W_B, W_A, pi0), não uma variável nova.

**(4) Posição de fam-20.** Típica do regime maioritário: (L1,L1) com uma aresta "geometricamente forçada" (equidistante, colapsa com QUALQUER tau) e outra "tau-seleccionada" (|Iso|=2 e tau acertou na única transposição). Na população, só 8,5% das arestas L1 são forçadas; ~50% das geometrias têm alguma simetria e a selecção de tau é o gargalo (4620/4619 arestas com W simétrico onde tau falhou). fam-20 não é um mecanismo à parte nem um outlier estrutural.

**(5) Nota sobre 3-ciclos.** C3 (34,5% das famílias) não produziu nenhum dos 46; o primeiro colapso C3 surge OOS e é (L2,L2), como a teoria permite (L1 de 3-ciclo exige simetria ternária rara; a rota L2 de C3 exige dupla troca + 3 graus iguais). A ausência de C3 nos 46 é esperada, não anómala.

---

## 6. SPECULATION — hipóteses além do provado (claramente marcadas)

- **Ordem de grandeza das taxas L2 por célula** (T_out ≫ FC_oth > C3 ≈ 0,4%): heurística de contagem de restrições — 1 igualdade de graus (T_out) vs 4 graus iguais (FC_oth) vs 3 graus iguais + dupla troca (C3). Não formalizei as probabilidades exactas sob a lei de W; os sentidos e magnitudes observados (0,04 / 0,007–0,013 / 0,004) são consistentes com esta leitura.
- **Resíduo positivo minúsculo e consistente** (obs−M3 ≈ +0,3σ, +0,6σ, +0,6σ nos três conjuntos): pode ser ruído; se for real, sugere um acoplamento de ordem superior (elegibilidade a favorecer levemente pi1 dentro das classes de rank, ou correlação fina entre empates dos perfis das duas arestas). Magnitude ≲10% do efeito; distingui-lo exigiria ~10× mais amostra.
- **Leitura de desenho de instrumento (diagnóstico, NÃO proposta de correcção, fora do mandato alterar C1')**: o estrato ordinal existe porque (a) a comparação entre contextos usa a ordem fraca com empates e (b) as 9 intervenções de 2 bits deixam uma emparelhação do canal não sondada. A classe de falha "vive" na intersecção destas duas escolhas com a partilha de pi entre as duas direcções do anel. Registo apenas como caracterização do espaço onde a falha reside.
- **O défice C3 do RAW-910000031** (z=−3,7) é, à luz de F10, uma flutuação da semente; a especulação alternativa (viés do gerador de permutações) está desfavorecida pelo teste directo com 200000 amostras.

---

## 7. Questões abertas

1. Cálculo fechado de q(célula) sob a lei exacta de W (combinatória dos popcounts de colunas XOR de M uniforme) — tornaria M1/M2 totalmente paramétricos e testáveis sem Monte Carlo.
2. Prova formal da ordenação das taxas L2 (T_out > FC_oth > C3) e da taxa nula-ou-não de configurações limite (ex.: existe alguma W com colapso C3 both-L1? esperado ~1 por ~65k famílias; nunca observado).
3. O caso dep_sites=0 (910000001/14155, aresta B): caracterizar exactamente o conjunto de theta com invariância ao nível do PADRÃO (não só das somas) — é o extremo absoluto da classe e tem medida própria (7 arestas em 20000).
4. O resíduo +0,3..0,6σ de M3: teste dedicado com N≈10^5 famílias (fora do orçamento actual de CPU partilhada).
5. Transporte formal completo da taxonomia para o Estrato 2 além do lema d_E2=4·d_E1 (dep_sites e órbitas têm escalas diferentes; os níveis transferem, as contagens de dep não são 4× triviais na presença de bits D no eixo da fibra).
6. A ligeira assimetria B vs A nas taxas L1 por classe (0,082 vs 0,071 em T; mesma direcção em DT) — compatível com ruído (~2σ); se persistir noutros lotes, procurar a origem na assimetria x/y da elegibilidade.

---

*Elaborado pelo agente WS5 (Fase 6 multiagente). Todos os ficheiros citados estão em `/root/causal-A-postconfirmatory-analysis/multiagent/ws5-failure-structure/` com sha256 em `SHAS.txt`. POST-CONFIRMATORY / EXPLORATORY: nada aqui altera o resultado confirmatório negativo nem propõe critérios novos.*

# WS4 — ESPECIFICIDADE NA CLASSE III

**POST-CONFIRMATORY / EXPLORATORY** — Pré-registo A v8.3, Fase 6 multiagente.
Workstream: `ws4-classIII-specificity`. Data: 2026-08-17.

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

**Resposta em uma frase:** à resolução do instrumento congelado (padrões de
resposta XOR a intervenções sobre fibra completa, e qualquer funcional deles:
dep ponto-a-ponto, d_m, ranks, eficácia C2, suporte C3) um III verdadeiro é
EXACTAMENTE nulo — P(dependência de memória | III) = 0 analiticamente,
0/4000 arestas empiricamente — mas a memória de um III é causalmente ACTIVA
fora dessa classe de funcionais (baselines saturados em 100%, composição de
visitação da órbita assimétrica em 100%, dinâmica H/K), pelo que recuperação
da informação perdida em II que saia da classe XOR-intervencional em fibra
completa pode, em princípio, introduzir ambiguidade do lado de III; dentro
dessa classe, não pode.

---

## FACT

Factos verificados nesta sessão (fontes: instrumento congelado, datasets
exploratórios existentes, e a medição pré-comprometida desta área).

**F1. Integridade.** `sha256sum frozen-copy/*.py` coincide com as 12 linhas
correspondentes de `multiagent/shared-readonly/MANIFEST.txt` (12/12).
Nenhum ficheiro fora desta área ws foi escrito; nada foi editado.

**F2. Semântica congelada do passo III** (`gerador.step_III`, canónico n=10;
bit0-1=x, bit2=mA, bit3-4=y, bit5=mB, bits6-7=cAB, bits8-9=cBA):
`x' = F0[x][cBA] ^ sigmaA[mA]; mA' = H[mA][x]; y' = G0[y][cAB] ^ sigmaB[mB];
mB' = K[mB][y]; cAB' = x; cBA' = y`. Sem pi: a interface é directa.

**F3. Procedência da medição.** Precommit
`precommit-ws4-classIII-especificidade.txt` depositado nesta área às
13:33 UTC de 2026-08-17, ANTES da execução (script depositado e corrido
~13:36 UTC), com a derivação analítica (previsões P1–P8) enunciada antes de
medir, N=2000 e semente 910000020 fixados. Semente do intervalo atribuído ao
WS4; distinta das confirmatórias e das 20 queimadas. Execução única,
sequencial, 4.8 s; sem multiprocessing; sem paragem opcional
(correu até N=2000). Fluxo idêntico ao `gerar_lote`:
`SeedSequence(910000020).spawn(4)[0]` → PCG64; rejeitar `pi0==pi1`; aceitar
sse `elegibilidade(th, False)[0]`. 2000 aceites em 6952 tentativas
(taxa 0.288). Instâncias canónicas III via `tabela_transicao("III", th,
False)`; maquinaria de análise = funções congeladas de `classificador.py`
(`extractor`, `popcount_tab`, `intervencoes` — 9 por canal, incluindo a
nula —, `estados_da_fibra`, `rank_canonico`).

**F4. Resultados da medição (2000 instâncias III, 4000 arestas
canal→processador; ficheiro `ws4-classIII-medicao.json`):**

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

Órbitas: comprimento 5–71 (mediana 20). delta_norm (máx. sobre intervenções
de |S_0/|V_0| − S_1/|V_1||): mediana ≈ 0.53 (C_AB→B) / 0.55 (C_BA→A)
bits/estado, p90 ≈ 1.0, máx 2.0; zeros: 0/2000 em cada aresta.

**F5. Datasets existentes (leitura apenas; `ws4-contraste-II.json`).**
No agregado II N=10000 (sementes 910000001/910000002, alheias): 20000
arestas, L1=705, L2=225, L3=19070; dep ponto-a-ponto presente em
19993/20000 (7 arestas com dep=0); 46 instâncias colapso_total
(subtipos 29 (L1,L1), 10 (L1,L2), 7 (L2,L2)). Nas 92 arestas dos 46
colapsos: dep_sites min=0, p25=1024, mediana=1152, p75=1536, máx=2048;
exactamente **1** aresta de colapso com dep=0 (theta_sha 964a55337a7a502f,
C_AB→B, L1); **45/46** colapsos têm AMBAS as arestas com dep>0. As restantes
6 arestas dep=0 do agregado estão fora do conjunto de colapsos (instâncias
individua_uma; não constam dos exemplos preservados, que guardam só 20 por
classe). Referência fam-20 (confirmatória, n=12): dep=4608 em cada aresta
com d0==d1 = [0,1024,1024,1024,1024,1792,1280,1536,1536] (C_AB→B) e
[0,1024,1024,1024,1024,1536,1536,1536,1536] (C_BA→A).

**F6. Lema de transferência** (`verifica_E1_E2.out`, existente): d_E2 =
4·d_E1, mesmos ranks, mesmos níveis, dep_E2 = 4·dep_E1 (10 famílias, todas
as arestas; consistente com dep fam-20: 4608 = 4·1152).

**F7.** A elegibilidade congelada avalia E1–E5 na órbita de CADA variante
(I, II e III) e E6 na II (`gerador.elegibilidade`): logo, em toda a família
elegível, a órbita III alcança ambos os valores de mA e de mB (E1(III)) e
alcança ≥2 valores de sigma (E5(III)).

---

## DERIVATION

Derivações exactas a partir das definições congeladas. (Enunciadas no
precommit ANTES da medição; a medição é guarda de implementação.)

**D1. Teorema III-1 (invariância pontual à memória).** Aresta C_AB→B
(canal a=[6,7], receptor b=[3,4,5], memória do receptor mB=bit5). Ponto z da
fibra com mB=m; extractor eB(T[z]) = y'(z) | (mB'(z)<<2). Intervenção
(mk,vl) ⊆ bits do canal substitui cAB por sub(cAB)=(cAB&~mc)|vc e não toca
x, mA, y, mB, cBA. Então:

    xr(z) = eB(T[z_int]) ^ eB(T[z])
          = [(G0[y][sub(cAB)]^sigmaB[m]) ^ (G0[y][cAB]^sigmaB[m])] | [(K[m][y]^K[m][y])<<2]
          = (G0[y][sub(cAB)] ^ G0[y][cAB]) | 0.

sigmaB[m] cancela no XOR; K[m][y] cancela porque a intervenção no canal não
altera y no estado corrente. Logo xr(z) depende APENAS de (y, cAB) e da
intervenção — não de m, nem de x, mA, cBA. Como `estados_da_fibra` alinha
Z0 e Z1 pela mesma enumeração dos 9 bits livres, os vectores de resposta são
iguais entrada a entrada entre m=0 e m=1. Simétrico na C_BA→A com (x, cBA),
F0, sigmaA, H. A prova usa só as equações do passo, não usa n: em Estrato 2
os bits D são bits livres adicionais da fibra e não entram em eB
(multiplicidade ×4; consistente com F6). ∎

**D2. Corolários (probabilidade 1 sobre theta elegível).**
(i) dep_sites ≡ 0 nas duas arestas canal→processador: **P(dependência de
memória de alta resolução | III) = 0** — afirmação analítica, não
estatística. (ii) d_0 ≡ d_1 entrada a entrada ⇒ nível L1 sempre (nunca L2,
nunca L3) ⇒ C1' marca 'estado' em ambas as arestas ⇒ o núcleo
A→C_AB→B→C_BA→A funde SEMPRE em III — que é o comportamento correcto para a
classe. A fusão em III é determinística, não um evento de amostragem.
(iii) Forma fechada: d_m(mk,vl) = 32·Σ_{c=0..3} W_M(c, sub(c)), com
W_M(p,q) = Σ_{r=0..3} pc2(M[r][p]^M[r][q]); M=G0, r=y na C_AB→B; M=F0, r=x
na C_BA→A; 32 = 2^5 bits livres após fixar (r,c). É a fórmula Wtil do
resultado prévio (auditada aqui pela verificação P3, 4000/4000) com
pi_m = id para ambos os m: **III é o ponto degenerado da condição K** —
tau = pi1∘pi0⁻¹ substituído por id, que é isometria de qualquer W_M.
(iv) C2: os conjuntos de eficácia por bit são funcionais de xr ⇒ idênticos
entre contextos. C3: as assinaturas nxt diferem entre contextos apenas por
complemento constante por bit (sigma) e pela constante K[m][y] no bit de
memória; o número de assinaturas distintas por bit através das intervenções
é invariante a complemento ⇒ suporte idêntico. As TRÊS candidatas congeladas
dão 'estado' deterministicamente nestas arestas em III.

**D3. Baseline (via de mimetismo nº1).** nx_m alinhado:
nx_m(z) = (G0[y][cAB]^sigmaB[m]) | (K[m][y]<<2). Pontos discordantes entre
contextos: bdep = 512 se sigmaB[0]≠sigmaB[1]; senão 128·|{y: K[0][y]≠K[1][y]}|.
Nas famílias ELEGÍVEIS, E1(III)+E5(III) forçam sigmaA[0]≠sigmaA[1] e
sigmaB[0]≠sigmaB[1] (E5 exige ≥2 valores de sigma alcançados e a memória só
tem 2 valores): logo **bdep = 512 — TODOS os pontos da fibra — em ambas as
arestas, em 100% das famílias elegíveis**. Num III verdadeiro a memória é
causalmente activa em todos os pontos do baseline; o estatístico congelado
aniquila essa actividade exactamente, por diferenciação XOR.

**D4. Órbita (via de mimetismo nº2).** Com V = órbita(s0), V_m = {s∈V:
mem_receptor(s)=m}, S_m(k) = Σ_{s∈V_m} pc2(xr_k(s)) (o mesmo funcional por
ponto, restringido aos estados visitados): pelo Teorema III-1, xr_k(s)
depende só do par p(s)=(r(s),c(s)), logo S_m(k) = Σ_{r,c} Cnt_m[r][c]·
resp_k(r,c), onde Cnt_m é a matriz de visitação 4×4 do contexto m.
**Proposição:** Cnt_0=Cnt_1 ⇒ S_0=S_1 para todas as intervenções; qualquer
diferença S_0 vs S_1 num III é portanto composição de visitação (selecção),
nunca mecanismo. (A identidade de factorização foi verificada 4000/4000 —
é ela que estabelece a proposição empiricamente, não a classe vazia da
premissa.)

**D5. Situação do lado II à mesma resolução (contexto, não proposta).**
Num II, xr(z) = G0[y][pi_m(sub(cAB))] ^ G0[y][pi_m(cAB)] (mesmos
cancelamentos de sigma e K). dep=0 numa aresta II ⇔ condição PONTUAL:
M[r][pi_0(sub(c))]^M[r][pi_0(c)] == M[r][pi_1(sub(c))]^M[r][pi_1(c)] para
todo (r, c, intervenção) — estritamente mais forte do que a condição K
agregada (K ⇔ L1 pelo resultado prévio; dep=0 ⇒ L1 ⇒ K, e F5 mostra
dep>0 com L1 em 91/92 arestas de colapso). O ponto fixo xr≡(campo III) é
atingível do lado II, mas raramente (F5: 7/20000 arestas).

---

## EMPIRICAL SUPPORT

**E1. Zero ocorrências de dependência de memória de alta resolução em III.**
0/2000 instâncias com dep>0 em qualquer aresta → limite superior unilateral
exacto (Clopper–Pearson) a 95%: P ≤ 1−0.05^(1/2000) = 1.497×10⁻³.
Por aresta: 0/4000 → P ≤ 7.487×10⁻⁴. Regra de três: 3/N idêntico à 4ª casa.
Estes limites são GUARDAS DE IMPLEMENTAÇÃO: a afirmação substantiva é o
Teorema III-1 (P=0 analítico), que a amostra não pode melhorar.

**E2. Concordância total previsão–medição.** As oito previsões P1–P8 do
precommit verificaram-se sem excepção (tabela em F4; 0 anomalias). Em
particular a forma fechada (P3) reproduziu d0 e d1 entrada a entrada nas
4000 arestas — auditoria independente, no caso pi=id, da derivação Wtil do
agente único, que este WS usa como enquadramento.

**E3. Exemplo concreto (fam 0, seed 910000020, tentativa 1, C_AB→B):**
d0 = d1 = dpred = [0,320,320,192,192,320,384,448,384]; dep=0; bdep=512;
órbita 27 com V_0=5, V_1=22; S_0 = [0,2,6,3,2,2,6,4,6] vs
S_1 = [0,9,15,7,13,10,15,18,17]. O estatístico congelado (fibra completa)
vê zero dependência de memória; a MESMA maquinaria restringida aos estados
visitados por contexto "veria" dependência — fabricada pela visitação.

**E4. Magnitude do mimetismo de órbita.** Perfis normalizados
S_m/|V_m| diferem em 100% das 4000 arestas (Cnt_0==Cnt_1 nunca ocorreu em
2000 órbitas); delta_norm mediana ≈ 0.53–0.55 bits/estado, p90 ≈ 1.0,
máx 2.0 — a mesma ordem de grandeza do efeito por estado que um II genuíno
exibe. Sem a fibra completa, um III verdadeiro é indistinguível de um
sistema "com memória moduladora" por estatísticas condicionadas ao contexto
sobre a órbita.

**E5. Saturação do baseline.** bdep = 512/512 pontos em 4000/4000 arestas
(P5), com a previsão estrutural exacta confirmada (sigma difere sempre, por
E1+E5). A actividade causal da memória em III não é rara nem subtil: é
máxima — e invisível ao estatístico congelado por construção.

**E6. Contraste com o lado II (datasets existentes).** À resolução dep:
III = 0 exacto (4000/4000); II = dep>0 em 19993/20000 arestas; mesmo entre
as 92 arestas dos 46 colapsos (que C1' não separa), 91 têm dep>0
(min 384, mediana 1152 — igual ao valor nuclear da fam-20 confirmatória,
4608/4 pelo lema F6). O único ponto de contacto exacto II∩III neste dataset
são 7/20000 arestas II com dep=0 (1 delas dentro de um colapso).

---

## INFERENCE

**I1.** A especificidade da classe III face ao instrumento congelado é
PERFEITA e determinística: nenhum III verdadeiro pode exibir d_0≠d_1,
ranks diferentes, dep>0, eficácia C2 dependente do contexto ou suporte C3
dependente do contexto nas arestas canal→processador. O erro confirmatório
(fam 20) é um fenómeno EXCLUSIVAMENTE do lado II (sensibilidade/colapso de
agregação); não existe fenómeno simétrico do lado III ao nível do
instrumento. A fusão do núcleo em III é o comportamento correcto e é
alcançada por razão estrutural (interface directa), não por acaso amostral.

**I2.** A memória de um III verdadeiro é causalmente ACTIVA — em três
estruturas de alta resolução, todas fora da classe de funcionais do campo
XOR-intervencional em fibra completa: (a) baseline por contexto (offset
sigma + dinâmica K/H), empiricamente saturado (100% dos pontos, 100% das
arestas); (b) composição de visitação da órbita por contexto (100% das
órbitas desta amostra); (c) campos de assinatura brutos (diferem por
complemento constante; o suporte C3 é o quociente que os apaga). Estas são
exactamente as estruturas que "poderiam ser confundidas com SINAL" — e o
instrumento congelado é cego a todas por construção (diferenciação XOR,
fibra completa, quocientes de suporte). Essa cegueira é o que compra a
especificidade perfeita de I1.

**I3. Resposta à pergunta-objectivo (tarefa 5).** Recuperar a informação
perdida em II (o campo pontual xr, que a agregação d_m e o rank descartam)
pode, EM PRINCÍPIO, introduzir ambiguidade do lado de III? Depende
exclusivamente do canal de recuperação:
— **Não**, se a recuperação permanecer na classe dos funcionais do campo de
resposta XOR a intervenções sobre fibra COMPLETA: nessa classe o III é o
campo identicamente nulo (Teorema III-1); qualquer funcional avalia-o num
valor fixo e nenhuma variabilidade entre contextos pode surgir do lado III.
O funcional mais fino dessa classe (o próprio campo pontual) mantém III
exactamente em zero.
— **Sim**, se a recuperação tocar baselines por contexto, agregados
condicionados à órbita/visitação, campos de assinatura não-quocientados ou
observáveis da dinâmica de memória H/K: aí um III verdadeiro tem estrutura
genuína, universal nesta amostra (100%), com magnitude por estado comparável
à de um II genuíno (E4) — ambiguidade em princípio.
Nota de fronteira: mesmo no canal "seguro", a ambiguidade RESIDUAL é
unidireccional — II pode atingir o campo nulo (7/20000 arestas; D5) e
tornar-se pontualmente indistinguível de III; III nunca sai do campo nulo.
A direcção do risco é sempre II→parece-III (perda de sensibilidade), nunca
III→parece-II (perda de especificidade). Este WS não propõe como explorar
nem como resolver nada disto.

**I4.** Transferência de regime: pelo argumento de D1 (independente de n) e
pelo lema F6, todas as conclusões valem sem alteração no regime
confirmatório (Estrato 2, n=12, módulos D inertes para eB dos receptores).

---

## SPECULATION

**S1.** O acesso observacional realista é em forma de órbita (estados
visitados); a fibra completa é um dispositivo teórico. Especulamos que
qualquer estimador prático da "informação perdida" que não faça
completamento exacto da fibra herda o confundimento de visitação de D4/E4 —
e este é universal (100% nesta amostra), não patológico. A robustez do
instrumento congelado vem de intervencionar TODas as configurações livres,
não de amostragem.

**S2.** Vista unificada especulativa: III é o ponto fixo (tau=id) da
geometria de modulação; os colapsos II (condição K) aproximam-se dele no
agregado Wtil, e as 7 arestas II com dep=0 atingem-no pontualmente. A
correlação inter-arestas ~2.1–2.4× do lado II (tau partilhado, resultado
prévio) sugere que a "distância ao ponto fixo" é uma propriedade da família
(theta), não da aresta — não testado aqui além dos dados citados.

**S3.** Se uma futura versão do protocolo (fora deste mandato) viesse a
considerar estatísticos mais finos, especulamos que a fronteira de segurança
do lado III coincide exactamente com o fecho da classe de funcionais do
campo XOR-intervencional em fibra completa; a caracterização formal desse
fecho (que operações preservam a nulidade em III) está em aberto e NÃO é
aqui proposta como desenvolvimento.

---

## QUESTÕES ABERTAS

1. Identidade e nível das 6 arestas II com dep=0 fora do conjunto de
   colapsos (agregado F5): localizá-las exigiria replay dos fluxos das
   sementes 910000001/910000002 (alheias a este WS); não foi feito por
   disciplina de sementes. Prevê-se (D5) que sejam L1 com a outra aresta L3.
2. Prevalência precisa da condição pontual de D5 no lado II
   (7/20000 arestas ≈ 0.035%): caracterização algébrica (que pares (pi0,pi1,M)
   a satisfazem) e a sua relação de inclusão estrita com a condição K.
3. Fronteira formal (fecho) da classe de funcionais "seguros" de S3.
4. Estrato 2: arestas para os módulos D (sem memória) não têm comparação de
   contexto definida; ficou fora do âmbito verificar se alguma via composta
   (canal→D→…) poderia transportar estrutura de contexto — a tipificação
   congelada diz que não (D é jusante e sem memória), mas não foi medido.
5. delta_norm de órbita em III (E4) tem mediana ~0.5 bits/estado; a
   distribuição comparável para II genuínos (mesma estatística de órbita)
   não foi medida — ficaria a cargo de outro WS se relevante.

---

## ANEXO — Ficheiros desta área (todos POST-CONFIRMATORY / EXPLORATORY)

- `precommit-ws4-classIII-especificidade.txt` — derivação + plano, ANTES da medição.
- `medicao_ws4_classIII.py` → `ws4-classIII-medicao.json` + `ws4-classIII-medicao.out` (N=2000, seed 910000020, 4.8 s).
- `contraste_II_ws4.py` → `ws4-contraste-II.json` + `ws4-contraste-II.out` (leitura determinística; sem amostragem).
- `WS4-CLASSIII-SPECIFICITY.md` — este relatório.
- `SHAS.txt` — sha256 de todos os ficheiros acima.

Sementes usadas: 910000020 (única; nenhuma outra foi consumida).
Instrumento: frozen-copy (12/12 vs MANIFEST). Sem alterações a nada fora
desta área. Sem multiprocessing. Execuções: 2 (medição 4.8 s; contraste <1 s).

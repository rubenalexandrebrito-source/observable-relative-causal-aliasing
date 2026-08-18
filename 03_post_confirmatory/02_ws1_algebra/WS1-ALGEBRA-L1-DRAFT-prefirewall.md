# WS1 — A condição algébrica do L1 (cancelamento por agregação)

**POST-CONFIRMATORY / EXPLORATORY** — Pré-registo A v8.3, Fase 6 multiagente, workstream WS1.
Data: 2026-08-17. Área: `/root/causal-A-postconfirmatory-analysis/multiagent/ws1-algebra-l1/`.

> **O resultado confirmatório permanece NEGATIVO e imutável**: C1' obteve 199/200
> (E1 150/150, E2 49/50); único erro: instância `7bb0baab3a8ed7aa`, família 20,
> variante II, Estrato 2 (n=12). Nada neste relatório recalcula, reinterpreta ou
> reabre esse resultado; isto é diagnóstico mecanístico exploratório. Nenhuma
> candidata corrigida (C1'') é proposta, em cumprimento do mandato.

**Firewall de independência**: a derivação (NOTAS-DERIVACAO.md), os scripts
s10-s13 e todos os outputs foram concluídos e escritos ANTES de qualquer leitura
de `condicao_L1.py`, `condicao_L1_oos.py`, `condicao-L1-insample.json`,
`condicao-L1-oos.json`, `FASE6-AUTOPSIA-7bb0baab3a8ed7aa.md` e
`precommit-oos-condicaoL1.txt`. A comparação com a análise prévia está no
capítulo 7, escrito depois.

---

## 1. Sumário

**Pergunta do mandato**: qual é a condição matemática mínima que permite
simultaneamente dependência causal ponto-a-ponto presente E d0=d1?

**Resposta (Teorema 5 + Proposição 7, demonstrados e validados)**: numa aresta
canal→processador do Sistema II, o vector d_m factoriza EXACTAMENTE por sete
inteiros agregados do contexto m — (A_m, B_m, V_m(0..3)), somas de pesos de
Hamming da tabela de resposta condicionada Φ_m — e os dois contextos estão
ligados por uma permutação de transporte ρ = π0⁻¹∘π1 do alfabeto do canal:
o contexto m=1 vê os MESMOS pesos com as colunas permutadas por ρ. Então

**d0 = d1 ⟺ K(θ): ρ preserva os agregados** — WM[ρ*(M1)]=WM[M1] ∧
WM[ρ*(M2)]=WM[M2] ∧ V∘ρ=V —

e a dependência ponto-a-ponto persiste (dep>0) sse ρ NÃO preserva o tensor de
padrões. O colapso de C1' é portanto **cancelamento por agregação**: colisões
inteiras entre pesos agregados (trocas de igual magnitude sob ρ), invisíveis à
soma de Hamming mas visíveis ponto-a-ponto. K é necessária E suficiente (iff
exacto, sem resto), foi verificada com 0 excepções em 20000 arestas in-sample e
10000 arestas fora-da-amostra pré-registadas (sens=espec=prec=NPV=1,0), e
explica a instância confirmatória falhada (fam 20) como membro TÍPICO da classe
modal de colapso (ρ transposição), com uma das arestas totalmente degenerada
(V constante ⟹ K para qualquer ρ).

---

## 2. FACT (factos verificados, sem inferência)

F1. Integridade: sha256 de `frozen-copy/*.py` coincide 12/12 com
    `multiagent/shared-readonly/MANIFEST.txt` (verificado 2026-08-17).

F2. Definições congeladas (lidas do código, não parafraseadas de memória):
  - `step_II` (gerador.py): v=π[mB][cAB]; u=π[mA][cBA]; x'=F0[x][u]⊕σA[mA];
    mA'=H[mA][x]; y'=G0[y][v]⊕σB[mB]; mB'=K[mB][y]; cAB'=x; cBA'=y.
  - Layout canónico: bit0=x LSB, bit1=x MSB, bit2=mA, bit3=y LSB, bit4=y MSB,
    bit5=mB, bits6-7=cAB, bits8-9=cBA (LSB primeiro); E2: bits10-11=D1,D2.
  - `intervencoes(bits)` (classificador.py): TODOS os (J⊆bits, η∈{0,1}^|J|);
    para canal de 2 bits, |I|=3²=9, na ordem: nula; LSB:=0; LSB:=1; MSB:=0;
    MSB:=1; canal:=0; canal:=1; canal:=2; canal:=3.
  - `estados_da_fibra`: fibra completa com o bit de memória do receptor fixo;
    eixo r idêntico entre contextos (emparelhamento contrafactual).
  - `rank_canonico`: forma canónica da ordem fraca com empates.
  - Níveis do dataset de prevalência: L1 ⟺ d0==d1 (vectores de 9 componentes);
    L2 ⟺ d0≠d1 mas rank_canonico igual; L3 caso contrário. dep = nº de pares
    (intervenção, ponto-da-fibra) com padrão xr diferente entre m=0 e m=1.
  - `sample_theta_base`: F0,G0,H,K,σA,σB uniformes; π0,π1 permutações uniformes
    independentes; rejeição sse π0==π1. Elegibilidade E1-E5(I,II,III)+E6(II).

F3. Datasets permitidos usados: `prevalencia-cancelamento-II.json` (semente
    910000001, 5000 famílias, 17135 tentativas) e `-lote2.json` (910000002,
    5000, 16845). Agregados publicados: L1=358+347=705, L2=113+112=225,
    L3=9529+9541=19070; dep>0 em 9996+9997=19993 de 20000 arestas; colapsos
    22+24=46 com subtipos (L1,L1)=29, (L1,L2)=10, (L2,L2)=7.

F4. Instância confirmatória falhada (cópia read-only + referência no dataset):
    fam 20, II, E2 (n=12), ambas as arestas L1 com dep=4608;
    d0=d1=[0,1024,1024,1024,1024,1792,1280,1536,1536] (C_AB→B) e
    [0,1024,1024,1024,1024,1536,1536,1536,1536] (C_BA→A).

F5. Todos os vectores d registados nos datasets exibem d[1]=d[2] e d[3]=d[4]
    (impressão digital prevista pelo Corolário 3.1 antes de qualquer execução).

F6. Lema d_E2 = 4·d_E1 (módulos D inertes) já demonstrado e verificado em
    `verifica_E1_E2.out`; reobtido aqui como caso do Lema 2 (factor 2^(n-5)).

---

## 3. DERIVATION (prova analítica; enumeração usada só como verificação)

Notação: aresta canal→processador do Sistema II; para C_BA→A o receptor tem
tabela R=F0, deslocamento σ=σA, memória mA; para C_AB→B, R=G0, σ=σB, memória
mB. pc = peso de Hamming em 2 bits. Tudo o que segue vale para AMBAS as
arestas, com o MESMO par (π0, π1).

**Lema 1 (localização da resposta).** Para z na fibra do contexto m, com campos
x (parte não-memória do receptor) e c (valor do canal), e qualquer intervenção
ι sobre os bits do canal:

E(T[do_ι(z)]) ⊕ E(T[z]) tem componente de memória nula e componente x' igual a
Φ_m(x, ι(c)) ⊕ Φ_m(x, c), onde **Φ_m(x,c) = R[x][π_m(c)] ⊕ σ[m]**.

*Prova.* do_ι altera apenas c. A memória seguinte (H[m][x] ou K[m][y]) não
depende de c. σ[m] é comum aos dois termos e cancela no XOR. ∎

**Lema 2 (multiplicidade).** A fibra (2^(n-1) pontos) parte-se em classes (x,c)
de 2^(n-5) pontos; logo d_m[ι] = 2^(n-5)·Σ_{x,c} pc(Φ_m(x,ι(c))⊕Φ_m(x,c)).
n=10 dá factor 32; n=12 dá 128 — reprova d_E2=4·d_E1 para estas arestas. ∎

**Proposição 3 (forma fechada dos 9 componentes).** Com
W_m(a,b) = Σ_x pc(Φ_m(x,a)⊕Φ_m(x,b)) (simétrica, diagonal 0, valores 0..8),
A_m = W_m(0,1)+W_m(2,3), B_m = W_m(0,2)+W_m(1,3), V_m(w) = Σ_c W_m(w,c):

**d_m = 2^(n-5) · (0, A_m, A_m, B_m, B_m, V_m(0), V_m(1), V_m(2), V_m(3))**

*Prova.* Nula → 0. (LSB:=v): termos não nulos exactamente nos c com LSB≠v, um
endpoint de cada par {c,c⊕1}; o valor é simétrico no par ⟹ soma = A_m,
independente de v. (MSB:=v) idem com pares {c,c⊕2} ⟹ B_m. (canal:=w):
Σ_c pc(Φ_m(x,w)⊕Φ_m(x,c)) ⟹ V_m(w). ∎

Corolário 3.1: d[1]=d[2] e d[3]=d[4] sempre (F5 confirma).
Corolário 3.2 (conservação): Σ_w V_m(w) = 2·(WM_m[M1]+WM_m[M2]+WM_m[M3]), com
M1={{0,1},{2,3}}, M2={{0,2},{1,3}}, M3={{0,3},{1,2}} os três emparelhamentos
perfeitos de K4 e WM_m[M] a soma de W_m nas arestas de M. Note-se
A_m=WM_m[M1], B_m=WM_m[M2].

**Lema 4 (transporte entre contextos).** Seja **ρ = π0⁻¹∘π1** (≠id, porque o
gerador rejeita π0=π1). Então Φ_1(x,c) = Φ_0(x, ρ(c)) ⊕ δ com δ constante
(=σ[0]⊕σ[1]), logo W_1(a,b) = W_0(ρa,ρb) e

A_1 = WM_0[ρ*(M1)], B_1 = WM_0[ρ*(M2)], V_1 = V_0∘ρ,

onde ρ* é a acção induzida em {M1,M2,M3} (homomorfismo S4→S3, núcleo
V4={id,(01)(23),(02)(13),(03)(12)}). ∎

**Teorema 5 (condição K; a resposta exacta).** Com ambos os contextos de
memória alcançados (garantido por E1(II) nas famílias elegíveis):

**d_0 = d_1 ⟺ K(θ) ≡ (a) WM_0[ρ*(M1)]=WM_0[M1] ∧ (b) WM_0[ρ*(M2)]=WM_0[M2]
∧ (c) V_0∘ρ = V_0.**

*Prova.* Igualdade componente a componente da Proposição 3 via Lema 4:
componentes 1-2 ⟺ (a); 3-4 ⟺ (b); 5-8 ⟺ (c); nula trivial. É um ⟺ sem
folga — K é simultaneamente necessária e suficiente ("a recíproca" pedida no
mandato está incluída). ∎

Leitura estrutural: ρ tem de ser uma **simetria do sistema de pesos agregados**
{V_0; WM_0 em (M1,M2)} — grafo K4 pesado por W_0 — sem ter de ser simetria dos
padrões subjacentes.

**Proposição 6 (análise por classe de conjugação de ρ).** ρ* leva transposições
e 4-ciclos a transposições de {M1,M2,M3}; 3-ciclos a 3-ciclos; V4\{id} a id.
Igualdades genericamente exigidas por K:

| classe de ρ (23 casos) | prob. a priori | igualdades WM | igualdades V | codim. total |
|---|---|---|---|---|
| V4\{id} (3)      | 3/23  | 0 (automáticas) | 2 | 2 |
| transposição (6) | 6/23  | 1               | 1 | 2 |
| 3-ciclo (8)      | 8/23  | 2 (WM todos iguais) | 2 | 4 |
| 4-ciclo (6)      | 6/23  | 1               | 3 (V constante) | 4 |

Previsão: L1 dominado por transposições e V4; 3-/4-ciclos raros. (Confirmada —
ver §4.)

**Proposição 7 (dep e a caracterização pedida).**
dep = 2^(n-5)·#{(ι≠nula, x, c): Φ_0(x,ι(c))⊕Φ_0(x,c) ≠ Φ_1(x,ι(c))⊕Φ_1(x,c)},
e dep=0 ⟺ o tensor de padrões D_0(x;a,b)=Φ_0(x,a)⊕Φ_0(x,b) é ρ-invariante:
D_0(x;ρa,ρb)=D_0(x;a,b) para todos x,a,b. Como pc(·) esquece o padrão e retém
só o peso, invariância dos padrões ⟹ K, mas não o inverso. **Logo: dependência
ponto-a-ponto presente com d0=d1 ⟺ ρ preserva os agregados (K) sem preservar
os padrões.** Este é o mecanismo mínimo — e único — do fenómeno. ∎

**Proposição 8 (nível 'estado' de C1' / L1∪L2).** C1' marca a aresta 'estado'
⟺ rank_canonico(d_0)=rank_canonico(d_1) ⟺ a ordem fraca do perfil agregado
(0, A, A, B, B, V(0..3)) é invariante pelo transporte ρ. L1 = invariância
cardinal; L2 = ordinal sem cardinal; L3 = nenhuma. O núcleo funde sse AMBAS as
arestas canal→processador são 'estado' (verificado contra `cl.classificar` em
§4, s12b).

**Corolário 8.1 (conservação de histograma: em V4 não há L2).** Para ρ∈V4:
A_1=A_0, B_1=B_0 e V_1 é permutação de V_0 — o MULTICONJUNTO de valores do
vector d é conservado. Se os ranks coincidem e o multiconjunto é o mesmo, os
vectores coincidem. Logo ranks iguais ⟹ d_0=d_1: **L2 é impossível em ρ∈V4**;
as arestas V4 são L1 ou L3. (Empiricamente: 0 L2 em 2642+1316 arestas V4.) ∎

**Teorema 9 (correlação inter-arestas).** As duas arestas partilham ρ (mesmo
π); condicionado a ρ, K_A depende só de F0 e K_B só de G0 — independentes.
Logo P(L1_A∧L1_B) = Σ_classe P(classe)·P(K|classe)² ≥ P(L1)², com desigualdade
estrita sob heterogeneidade entre classes (Cauchy-Schwarz) — a origem do
excesso de correlação observado (~2,1-2,4×). ∎

---

## 4. EMPIRICAL SUPPORT (tudo com igualdade EXACTA, inteiro a inteiro)

Scripts e outputs no ws dir (SHAS.txt): s10 (exemplos registados), s11 (fam20
cega), s12 (replay completo), s12b (classificador real), s13 (OOS pré-registada).

**S1 — Exemplos registados (s10).** 126 famílias replayadas por (semente,
tentativa) com theta_sha verificado 126/126: os 46 colapsos + 40 individua_uma
+ 40 individua_ambas — estes últimos são os CONTROLOS L3/L3, com critério
objectivo: são os "primeiros 20 de cada classe por lote" fixados pelo script
original do dataset, não escolhidos por este agente. Resultado: 252/252 arestas
com nível igual nas três vias (registado = maquinaria congelada = fórmula);
132/132 arestas com d registado reproduzido exactamente; 252/252 com d
congelado = fórmula (inclui os L3, onde o dataset não guarda d); dep exacto
252/252.

**S2 — Replay completo in-sample (s12).** Reexecução fiel do loop gerador
(sample → rejeição π → elegibilidade) das sementes 910000001 e 910000002:
tentativas reproduzidas exactamente (17135 e 16845), e TODOS os agregados
publicados reconciliados (L1/L2/L3, dep=0, colapsos, subtipos — 6/6 por lote).
Em 20000 arestas: **0 divergências** fórmula vs congelado (d, nível, dep) e
**0 excepções** a K⟺L1.

**S3 — Tabela por classe de ρ (10000 famílias in-sample; s12).**

| classe | famílias (esperado uniforme) | L1/aresta | L2/aresta | colapsos |
|---|---|---|---|---|
| transposição | 2615 (2608,7) | 399/5230 = 7,63% | 159 (3,04%) | 33 |
| V4           | 1321 (1304,3) | 207/2642 = 7,83% | **0**       | 10 |
| 3-ciclo      | 3451 (3478,3) | 46/6902 = 0,67%  | 32 (0,46%)  | 0  |
| 4-ciclo      | 2613 (2608,7) | 53/5226 = 1,01%  | 34 (0,65%)  | 3  |

Confirma: (i) elegibilidade ≈ ortogonal à classe de ρ (frequências ≈ a priori);
(ii) ordem prevista pela codimensão (7,6-7,8% nas classes de codim. 2 vs
0,7-1,0% nas de codim. 4); (iii) Corolário 8.1 (0 L2 em V4); (iv) colapsos
concentrados em transposição+V4 (43/46), 3-ciclos ausentes.

**S4 — Correlação inter-arestas (s12).** P(L1)=3,525%/aresta;
P(L1,L1)=0,290%/instância; independência global preveria 0,124% (lift 2,33);
o modelo classe-condicional do Teorema 9 prevê 0,238% (lift 1,91). O resíduo
(29 observados vs 23,8 do modelo) está dentro do ruído (≈1σ Poisson) —
consistente com independência condicional exacta dado ρ.

**S5 — Estrutura dos 46 colapsos (s10).** 92 arestas: 68 L1, todas com
(a)∧(b)∧(c); 24 L2, TODAS com (c) verdadeira e exactamente UMA de (a)/(b)
falsa. dep>0 em 91/92; a única excepção (lote1 fam 4159, C_AB→B, ρ∈V4,
V=(14,14,14,14) constante) tem dep=0 — invariância ao nível dos padrões, L1
trivial; o colapso dessa família assenta na outra aresta (dep=1152>0).

**S6 — fam20 confirmatória, teste CEGO (s11).** Sem θ e sem sementes
confirmatórias: Φ_m extraído directamente da tabela exportada da instância
(Lema 1 verificado: resposta bem-definida por (m,x,c) em todo o espaço 2^12),
fórmula com factor 2^(12-5)=128. Resultado: d previsto = d registado = d
recomputado pela maquinaria congelada, nas DUAS arestas, dep=4608 exacto,
nível L1 ambas. Transporte ρ' único, classe **transposição** (a classe modal
dos colapsos). Agregados: C_AB→B: WM=(8,8,8), V=(14,10,12,12) com a colisão
V(2)=V(3) exigida pela transposição; C_BA→A: WM=(8,8,8) e V=(12,12,12,12)
constante — **sistema de pesos totalmente degenerado: K vale para QUALQUER ρ**.

**S7 — Elo com o classificador real (s12b).** `cl.classificar` (o objecto
congelado da fase confirmatória) nas 126 instâncias canónicas: 252/252 arestas
canal→processador com C1p==('estado' ⟺ previsão ordinal da fórmula); 252/252
arestas processador→canal 'estado' (como afirmado na derivação da v8); fusão
do núcleo {A,B,C_AB,C_BA} ⟺ colapso_total em 126/126.

**S8 — Validação FORA-DA-AMOSTRA pré-registada (s13; precommit-ws1-oos.txt,
sha 454821ad…, escrito antes de correr).** Semente 910000005 (intervalo WS1),
N=5000 famílias (16890 tentativas), condição K congelada antes do teste:

| confusão | TP | FP | FN | TN | sens. | espec. | prec. | NPV |
|---|---|---|---|---|---|---|---|---|
| K vs L1 (por aresta)          | 307 | 0 | 0 | 9693 | 1,0 | 1,0 | 1,0 | 1,0 |
| ordinal vs L1∪L2 (por aresta) | 404 | 0 | 0 | 9596 | 1,0 | 1,0 | 1,0 | 1,0 |
| colapso (por instância)       | 16  | 0 | 0 | 4984 | 1,0 | 1,0 | 1,0 | 1,0 |

0 divergências d/nível/dep em 10000 arestas novas. Réplica da estrutura por
classe (L1: transposição 6,87%, V4 7,52%, 3-ciclo 0,57%, 4-ciclo 0,68%;
colapsos: 10 transposição + 6 V4 + 0 + 0; subtipos 12/2/2).

---

## 5. INFERENCE (interpretação suportada pelos factos acima)

I1. **Mecanismo do erro confirmatório.** C1' agrega a resposta intervencional
por soma de pesos de Hamming sobre a fibra completa. Pela Proposição 3, essa
agregação factoriza por 7 inteiros; a comparação entre contextos reduz-se a
comparar um sistema de pesos de um grafo K4 consigo próprio permutado por ρ.
Quando os pesos colidem nos agregados certos (K), C1' fica cego à modulação de
memória mesmo com milhares de sítios de dependência ponto-a-ponto (fam20:
4608 por aresta). O erro não é numérico nem de escala: é a projecção
matemática do estatístico.

I2. **fam20 é típica, não exótica.** ρ transposição (classe modal, 33/46 dos
colapsos in-sample), com uma aresta em degenerescência total (V constante e WM
iguais ⟹ K para qualquer ρ) e a outra com exactamente a colisão V(2)=V(3)
requerida. A probabilidade de colapso por instância (~0,42-0,46%) e o acerto
esperado de C1' em 75 instâncias II (~99,7% por instância; P(≥1 falha em 75)
≈ 1−0,9958^75 ≈ 27%) tornam o único erro em 200 um desfecho ordinário do
processo, não um outlier estrutural.

I3. **Correlação inter-arestas explicada.** A partilha de ρ entre as duas
arestas (mesmo π) com independência condicional dos pesos (F0 vs G0) reproduz
o lift observado dentro do ruído (1,91 modelado vs 2,33 observado, resíduo
≈1σ). Não é preciso postular acoplamento adicional entre arestas.

I4. **Porque L2 acompanha L1 nos colapsos.** Os 24 casos L2 dos colapsos têm
todos (c) válida e uma única condição de emparelhamento falhada — a falha
cardinal mínima que ainda preserva a ordem fraca. L2 é a orla ordinal do mesmo
fenómeno de colisão; em V4 essa orla é vazia por conservação de histograma
(Corolário 8.1).

I5. **A elegibilidade não protege contra K.** As frequências das classes de ρ
pós-elegibilidade são as a priori (S3), e E6(II) apenas exige eficácia do
remapeamento algures — não exclui colisões agregadas. O desenho amostral do
protocolo não tinha (nem pretendia ter) um guard-rail contra este quociente.

---

## 6. SPECULATION (claramente marcado; não são conclusões)

S-a. A taxa de colisão deve depender fortemente da cardinalidade do alfabeto:
com |X|=4 e pesos em 0..8/0..24, os "birthday hits" inteiros são frequentes
(≈7-8% nas classes de codim. 2). Com alfabetos maiores (mais bits por campo),
esperar-se-ia queda rápida da prevalência de K — não testado aqui.

S-b. Qualquer estatístico que compare contextos APENAS através de somas de
Hamming sobre fibras completas herdará quocientes análogos (a factorização do
Lema 2/Prop. 3 é genérica para intervenções de reescrita em subconjuntos de
bits); a identidade precisa das colisões dependerá da estrutura do lattice de
intervenções. Não se propõe aqui qualquer candidata alternativa.

S-c. O caso dep=0 (fam 4159, V constante) sugere uma sub-família rara de
θ com simetria genuína de padrões sob ρ; a sua prevalência (7/20000 arestas)
parece consistente com colisões de padrões exigirem ~16 igualdades
simultâneas, mas não foi derivada uma fórmula de contagem.

---

## 7. Comparação com a análise prévia (escrito APÓS levantar a firewall)

[PREENCHIDO NO FINAL — ver versão final deste ficheiro.]

---

## 8. Questões em aberto

Q1. Fórmula fechada para P(K|classe de ρ) sob θ uniforme (distribuição exacta
    dos pesos W e das colisões) — os valores empíricos (7,6-7,8% e 0,7-1,0%)
    pedem derivação combinatória.
Q2. Prevalência de K em variantes do desenho com |c|>2 bits ou π dependente de
    mais estados (escalamento das colisões com a dimensão).
Q3. Caracterização exacta da sub-família dep=0 (simetria de padrões) e da sua
    medida.
Q4. O papel EXACTO das colisões em C2 (inclusão de conjuntos de intervenções
    eficazes) nos mesmos 46 colapsos — fica para os workstreams respectivos;
    aqui só se nota que C2 e C3 também fundiram o núcleo na fam20 (facto
    confirmatório), o que é consistente com degenerescência a nível de padrões
    parcial, mas não foi analisado por WS1.

## 9. Reprodutibilidade e inventário

- Derivação independente: `NOTAS-DERIVACAO.md` (pré-firewall).
- Scripts: `s10_exemplos_validacao.py`, `s11_fam20_cega.py`,
  `s12_replay_completo.py`, `s12b_classificar_real.py`, `s13_oos.py`
  (+ `s14_*` do capítulo 7).
- Outputs: `out-s10.json`, `out-s11.json`, `out-s12.json`, `out-s12b.json`,
  `out-s13.json`, logs `s1*.log`.
- Pré-registo OOS: `precommit-ws1-oos.txt` (semente 910000005; sementes
  910000006-9 reservadas, uso só com novo precommit).
- Sementes usadas por WS1: apenas 910000005 (nova); 910000001/910000002 são
  reanálise de datasets existentes. Nenhuma semente proibida foi tocada; nada
  em `/root/causal-A-amd2-official/` foi lido ou escrito.
- Hashes de tudo: `SHAS.txt`.

# WS1 — NOTAS DE DERIVAÇÃO INDEPENDENTE (pré-firewall)

**POST-CONFIRMATORY / EXPLORATORY** — Pré-registo A v8.3, Fase 6, WS1 (álgebra do L1).
Escrito ANTES de ler qualquer ficheiro da análise prévia de agente único
(condicao_L1.py, condicao_L1_oos.py, condicao-L1-insample.json, condicao-L1-oos.json,
FASE6-AUTOPSIA-7bb0baab3a8ed7aa.md, precommit-oos-condicaoL1.txt). Serve de evidência
da independência exigida pela firewall do mandato.

O resultado confirmatório permanece **negativo** (C1' 199/200; único erro
7bb0baab3a8ed7aa, fam 20, II, Estrato 2) e é imutável; nada aqui o recalcula.

Fontes usadas até este ponto: frozen-copy/{gerador,classificador,pontuacao}.py
(sha256 12/12 = MANIFEST), prevalencia/prevalencia_cancelamento.py,
prevalencia-cancelamento-II.json, -lote2.json, prevalencia-combinada-N10000.json.

## 0. Definições exactas herdadas do código congelado

Passo II (gerador.step_II), campos (x, mA, y, mB, cAB, cBA):

    v = pi[mB][cAB];  u = pi[mA][cBA]
    x'  = F0[x][u] ^ sigmaA[mA];   mA' = H[mA][x]
    y'  = G0[y][v] ^ sigmaB[mB];   mB' = K[mB][y]
    cAB' = x;  cBA' = y

Layout canónico: bit0=x LSB, bit1=x MSB, bit2=mA, bit3=y LSB, bit4=y MSB,
bit5=mB, bits6-7=cAB (bit6=LSB), bits8-9=cBA (bit8=LSB); E2 junta d1=bit10,
d2=bit11 (jusante, inertes para o núcleo).

Arestas canal→processador: C_AB→B (bits_a=[6,7], bits_b=[3,4,5], mem=[5]) e
C_BA→A (bits_a=[8,9], bits_b=[0,1,2], mem=[2]).

Estatístico C1' por aresta (classificador.perfis_aresta / prevalencia.analisa_aresta):
para cada contexto de memória alcançado m, fibra completa Z_m (todos os bits
livres excepto o bit de memória do receptor), e para cada intervenção
(mk,vl) ∈ intervencoes(bits_a) — todos os J ⊆ bits_a com todos os valores,
|I| = 3^2 = 9, na ordem congelada

    ι0=(0,0) nula; ι1,ι2 = (LSB:=0),(LSB:=1); ι3,ι4 = (MSB:=0),(MSB:=1);
    ι5..ι8 = (canal:=0),(canal:=1),(canal:=2),(canal:=3)

calcula-se d_m[ι] = Σ_{z∈Z_m} HamB( E_B(T[do_ι(z)]) ⊕ E_B(T[z]) ), onde E_B é o
extractor dos bits do receptor. Níveis: L1 ⟺ d_0 == d_1 (vector);
L2 ⟺ d_0 ≠ d_1 mas rank_canonico(d_0) == rank_canonico(d_1); L3 caso contrário.
dep (ponto-a-ponto) = nº de pares (ι, ponto-da-fibra) com padrão xr diferente
entre m=0 e m=1 (fibras alinhadas pelo eixo r).

## 1. Lema 1 (localização da resposta)

Para a aresta C_BA→A (mutatis mutandis C_AB→B com G0, σB, cAB, mB): seja z na
fibra Z_m com campos (x, y, mB, cAB, c=cBA). Para qualquer intervenção ι sobre
os bits do canal, com ι(c) o valor intervencionado do canal:

    E_A(T[do_ι(z)]) ⊕ E_A(T[z]) = [ Φ_m(x, ι(c)) ⊕ Φ_m(x, c) ]  nos slots de x',
                                   0 no slot de memória,

onde **Φ_m(x,c) = F0[x][π_m(c)] ⊕ σA[m]** (tabela de resposta condicionada ao
contexto). Prova: do_ι só altera c; mA' = H[m][x] não depende de c; σA[m] é
comum e cancela no XOR; x' = F0[x][π_m(c)] ⊕ σA[m]. ∎

Consequência: o padrão de resposta num ponto depende só de (m, x, c, ι);
os restantes n−5 bits livres da fibra (y, mB, cAB; +d1,d2 no E2) são inertes.

## 2. Lema 2 (multiplicidade) e transferência E1→E2

A fibra Z_m parte-se em classes de equivalência por (x,c), cada uma com
2^(n−5) pontos. Logo

    d_m[ι] = 2^(n−5) · Σ_{x∈{0..3}} Σ_{c∈{0..3}} pc( Φ_m(x, ι(c)) ⊕ Φ_m(x, c) )

com pc = peso de Hamming em 2 bits. n=10 → factor 32; n=12 (E2) → factor 128.
Isto REPROVA, para estas arestas, o lema d_E2 = 4·d_E1 (módulos D inertes),
consistente com verifica_E1_E2.out.

## 3. Proposição 3 (forma fechada dos 9 componentes)

Defina-se a matriz de pesos de pares do receptor no contexto m:

    W_m(a,b) = Σ_x pc( Φ_m(x,a) ⊕ Φ_m(x,b) )   (simétrica, diagonal nula, 0..8)

e os agregados
    A_m = W_m(0,1) + W_m(2,3)        (emparelhamento M1 = {{0,1},{2,3}}, flips do LSB)
    B_m = W_m(0,2) + W_m(1,3)        (emparelhamento M2 = {{0,2},{1,3}}, flips do MSB)
    V_m(w) = Σ_c W_m(w,c)            (soma da linha w)

Então, na ordem congelada das intervenções,

    d_m = 2^(n−5) · ( 0, A_m, A_m, B_m, B_m, V_m(0), V_m(1), V_m(2), V_m(3) ).

Prova: ι nula → 0. ι=(LSB:=v): termos não nulos exactamente nos c com
LSB(c)≠v; estes percorrem um endpoint de cada par {c, c⊕1}; o valor
pc(Φ_m(x,c⊕1)⊕Φ_m(x,c)) é simétrico no par, logo a soma é A_m e não depende
de v. Análogo para MSB → B_m. ι=(canal:=w): Σ_c pc(Φ_m(x,w)⊕Φ_m(x,c)) → V_m(w). ∎

Corolário 3.1 (impressão digital): em TODO o d_m, d[1]=d[2] e d[3]=d[4].
(Verificado em todos os vectores registados nos datasets.)

Corolário 3.2 (identidade de conservação): Σ_w V_m(w) = 2·(WM_m[M1]+WM_m[M2]+WM_m[M3])
onde WM_m[M] é a soma de W_m nas duas arestas do emparelhamento M, e
M3 = {{0,3},{1,2}}. Em particular A_m + B_m + WM_m[M3] = ½·Σ_w V_m(w).

## 4. Lema 4 (transporte entre contextos por ρ)

Seja **ρ = π_0⁻¹ ∘ π_1** (permutação de {0..3}; ρ ≠ id porque o gerador rejeita
π_0=π_1). Então

    Φ_1(x,c) = Φ_0(x, ρ(c)) ⊕ δ,   δ = σA[0]⊕σA[1] constante,

logo W_1(a,b) = W_0(ρa, ρb) e portanto

    A_1 = WM_0[ρ*(M1)],   B_1 = WM_0[ρ*(M2)],   V_1 = V_0 ∘ ρ,

onde ρ* é a acção induzida nos três emparelhamentos perfeitos {M1,M2,M3} de K4
(homomorfismo S4 → S3 com núcleo V4 = {id,(01)(23),(02)(13),(03)(12)}). ∎

Nota: as DUAS arestas canal→processador partilham o MESMO ρ (o π é o mesmo);
diferem apenas nos pesos (Φ de F0 vs Φ de G0).

## 5. Teorema 5 (condição K, exacta — a resposta do mandato)

Para uma aresta canal→processador do Sistema II com ambos os contextos
alcançados:

    d_0 = d_1  ⟺  K(θ) ≡ (a) ∧ (b) ∧ (c), com
      (a) WM_0[ρ*(M1)] = WM_0[M1]
      (b) WM_0[ρ*(M2)] = WM_0[M2]
      (c) V_0 ∘ ρ = V_0          (4 igualdades pontuais)

Prova: componente a componente da Proposição 3 com o Lema 4; nula trivial;
componentes 1-2 dão (a); 3-4 dão (b); 5-8 dão (c). É um ⟺ sem resto. ∎

Leitura: K diz que ρ é uma **simetria do sistema de pesos agregados**
{V_0, WM_0 restrito a (M1,M2)} — não necessariamente dos padrões.

## 6. Proposição 6 (análise por classe de conjugação de ρ)

ρ* : transposições e 4-ciclos ↦ transposições de {M1,M2,M3}; 3-ciclos ↦ 3-ciclos;
V4\{id} ↦ id. Nº de igualdades exigidas (genéricas):

| classe de ρ (23 casos) | prob. a priori | WM exigidas | V exigidas | total |
|---|---|---|---|---|
| V4\{id} (3)        | 3/23 | 0 (auto)            | 2 (pares de V iguais) | 2 |
| transposição (6)   | 6/23 | 1 (WM_i = WM_j)     | 1 (V(a)=V(b))         | 2 |
| 3-ciclo (8)        | 8/23 | 2 (WM todos iguais) | 2 (V igual no 3-ciclo)| 4 |
| 4-ciclo (6)        | 6/23 | 1                   | 3 (V constante)       | 4 |

(ρ uniforme em S4\{id} porque π_0,π_1 são uniformes independentes condicionadas
a diferir.) Previsão qualitativa P4: o L1 deve ser dominado por ρ transposição
e ρ∈V4; 3-ciclos e 4-ciclos exigem coincidências duplas e devem ser raros no L1.

## 7. Proposição 7 (dep e a caracterização do colapso)

dep = 2^(n−5) · #{(ι≠nula, x, c) : Φ_0(x,ι(c))⊕Φ_0(x,c) ≠ Φ_1(x,ι(c))⊕Φ_1(x,c)}.

dep = 0 ⟺ o tensor de diferenças D_0(x;a,b) = Φ_0(x,a)⊕Φ_0(x,b) é invariante
por ρ nos dois argumentos de canal: D_0(x; ρa, ρb) = D_0(x; a,b) ∀x,a,b
(invariância ao NÍVEL DOS PADRÕES).

K NÃO implica invariância dos padrões: K só iguala somas de pesos de Hamming.
**Resposta à pergunta do mandato**: dependência ponto-a-ponto presente com
d_0=d_1 ⟺ ρ preserva os agregados (K) sem preservar os padrões (¬invariância
do tensor D_0). O colapso é cancelamento por agregação: d_m factoriza pelo
invariante de dimensão baixa (A_m, B_m, V_m) — 6 inteiros de W_m — enquanto a
informação ponto-a-ponto vive num espaço muito maior.

## 8. Proposição 8 (nível L2 / 'estado' de C1')

rank_canonico(d_0) = rank_canonico(d_1) ⟺ a ordem fraca (com empates) do
perfil (0, A_0, A_0, B_0, B_0, V_0(0..3)) coincide com a de
(0, A_1, A_1, B_1, B_1, V_1(0..3)) = perfil transportado por ρ. C1' marca
'estado' sse esta invariância ORDINAL vale; o núcleo funde sse vale nas duas
arestas. L1 = invariância cardinal; L2 = ordinal sem cardinal; L3 = nem ordinal.

## 9. Teorema 9 (correlação inter-arestas)

As duas arestas partilham ρ; condicionado à classe de ρ, os pesos das duas
arestas provêm de tabelas independentes (F0 vs G0). Logo
P(L1_A ∧ L1_B) = Σ_classe P(classe) · P(K_A|classe) · P(K_B|classe)
≥ [Σ_classe P(classe) P(K|classe)]² = P(L1)² (Cauchy–Schwarz, estrita com
heterogeneidade entre classes) — explica o excesso ~2,1-2,4× observado.

## 10. Previsões empíricas pré-registadas (a testar nos scripts s10-s13)

P1 d[1]=d[2] ∧ d[3]=d[4] em todos os vectores (já visto nos registados).
P2 A fórmula da Prop. 3 reproduz EXACTAMENTE (=, inteiro a inteiro) os d
   registados e os recomputados pelo classificador congelado.
P3 K ⟺ L1 em todas as arestas (as duas direcções; 0 excepções).
P4 Distribuição de classes de ρ nos L1 concentrada em transposições e V4.
P5 A decomposição por classe reproduz o excesso de correlação (L1,L1).
P6 fam20 (cega, n=12): factor 128; d previstos = registados; K satisfeita
   nas duas arestas com dep=4608>0.

# WS3 — DINÂMICA REALIZADA ESTRITA
**POST-CONFIRMATORY / EXPLORATORY** — Pré-registo A v8.3 (Amendments 1-3 congeladas), Fase 6 multiagente, workstream ws3.

> **CONFIRMATORY RESULT: NEGATIVE** — `resultado_confirmatorio_A = "negativo"`, fechado e
> imutável: C1′ 199/200 (E1 150/150, E2 49/50); erro único na instância `7bb0baab3a8ed7aa`
> (família 20, variante II, Estrato 2, n=12). Nada neste relatório recalcula ou
> reinterpreta esse resultado; nenhuma correção de C1′ é proposta. Tudo aqui é
> diagnóstico mecanístico exploratório.

Pergunta do mandato: *a dependência causal de memória do mecanismo II está efectivamente
realizada em configurações COMPARÁVEIS visitadas pela órbita em AMBOS os contextos de
memória (critério estrito, interseção dos suportes), e não apenas na união dos suportes
(critério OR anterior: 51 e 54 sítios/aresta na fam-20) ou na fibra contrafactual
completa?*

**Resposta curta: SIM — estritamente realizada.** Na instância confirmatória falhada, em
AMBAS as arestas do núcleo, existem células comparáveis (r,c) visitadas pela órbita nos
dois contextos de memória onde a resposta intervencional difere (9 sítios estritos por
aresta), e em ambas as arestas existe uma testemunha **observacional** (sem qualquer
cirurgia) da dependência π_m. O colapso de C1′ é um artefacto de agregação (condição K,
cancelamento isométrico do somatório da fibra), não de suporte realizado.

---

## 1. Definições (congeladas em `precommit-ws3-strict.txt` ANTES da execução)

Por aresta canal a → processador b (arestas `C_AB->B` e `C_BA->A`; maquinaria congelada
`cl.*` de `frozen-copy/`, 12/12 vs MANIFEST):

- **D1 Órbita** = `cl.orbita(T, s0)`: trajetória desde o estado inicial até à primeira
  repetição (transiente + ciclo). "Realizado" = visitado pela órbita.
- **D2 Fibras alinhadas** `Z_m = cl.estados_da_fibra(n, membits_b, m)`, m=0,1: eixo livre
  idêntico (emparelhamento contrafactual congelado do classificador).
- **D3 Granularidade CONFIGURAÇÃO**: R_m = {configurações do eixo livre realizadas com
  memória do receptor = m}. Estrito = R_0 ∩ R_1 (equivalente: par de estados da órbita
  que difere EXATAMENTE no bit de memória do receptor); união = R_0 ∪ R_1 = critério OR
  do teste anterior.
- **D4/D5 Granularidade (r,c)**: r = estado do processador do receptor (bits de b sem a
  memória), c = valor do canal a. C_m = {(r,c) realizados com memória m};
  **I = C_0 ∩ C_1** (estrito), U = C_0 ∪ C_1. A redução que legitima esta granularidade
  é provada e verificada (secção 3).
- **D6 Sítio de dependência**: par (intervenção, ponto/célula) com padrão de resposta
  xr_0 ≠ xr_1 (convenção idêntica a prevalencia/autopsia step3b). As 9 intervenções são
  I_A completo do classificador (todos os J ⊆ bits(a), η ∈ {0,1}^|J|, incluindo a nula).
- **D7 Contraste observacional (sem cirurgia)**: para (r,c1),(r,c2) ∈ I com o mesmo r:
  O_m = eB[T[s(r,c1,m)]] ⊕ eB[T[s(r,c2,m)]] avaliado em testemunhas realizadas;
  sítio observacional sse O_0 ≠ O_1.
- **D8 Categorias por aresta** (em cada granularidade):
  `ESTRITO` (≥1 sítio na interseção estrita) · `UNIAO_APENAS` (0 estritos, ≥1 na união;
  B1 = interseção vazia, B2 = interseção não-vazia sem sítio) · `PURO_CONTRAFACTUAL`
  (0 sítios na união, dep_total > 0) · `SEM_DEP` (dep_total = 0).
- **D9 Instância**: "mecanismo II estritamente realizado" sse ≥1 aresta ESTRITO
  (primário); "ambas as arestas" reportado a par.
- **D10 Granularidade primária** = (r,c); configuração completa reportada como
  sensibilidade ultra-estrita; na fam-20 (n=12) também a intermédia "configuração
  nuclear" (núcleo sem o bit de memória do receptor, excluindo D1/D2).

**Justificação de (r,c) e alternativas.** A contribuição causal de cada ponto da fibra
depende apenas de (r,c) dado m (Proposição 1, secção 3): células (r,c) são a partição de
comparabilidade EXATA mais grossa — refiná-la (configuração nuclear/completa) só encolhe
o suporte estrito exigindo igualdade de bits provadamente irrelevantes para a resposta
comparada; engrossá-la juntaria pontos com respostas distintas. Além disso (r,c) é
invariante ao embedding E1↔E2 (módulos D inertes não entram em (r,c) nem em m), enquanto
a interseção por configuração completa NÃO é (os bits D entram na chave) — a fam-20
exibe exactamente essa instabilidade (secção 4.1). Alternativas rejeitadas: ponderação
por multiplicidade de visita (adotou-se suporte, não frequência); órbita = só ciclo
(D1 fixou transiente+ciclo; sensibilidade não recomputada — questão aberta Q2).

## 2. FACT (execuções, integridade, resultados numéricos)

**Integridade e proveniência.** `frozen-copy/*.py` 12/12 sha-iguais ao MANIFEST
partilhado; instância cega `conf-e2/instancias/7bb0baab3a8ed7aa.json`
sha256 `8747188e0c3dd360b348f45e7809d488403edbc963ad12758406a9a58c77cede` (read-only,
intocada); `chave-e2.json` sha `78de6304…5615` (= MANIFEST), usada apenas para tipos de
módulo (`pt._tipos_e2`). Nenhum artefacto confirmatório foi modificado. Este ws3 dir
continha uma primeira execução interrompida (`tentativa-interrompida-1/`, precommit
escrito 13:32-13:35 UTC, outputs 13:41-13:42 UTC, sem relatório/SHAS): foi **auditada e
totalmente verificada** (abaixo), os scripts re-executados no ws root reproduziram
`ws3-strict-fam20.json` **byte-idêntico** (sha `e402dca3…76c7e`) e
`ws3-strict-bateria.json` idêntico exceto o campo de duração.

**Verificação independente** (`ws3_indep.py` + `ws3_verifica.py`): reimplementação de
raiz, por rota distinta — testemunhas nos ESTADOS REALIZADOS da órbita (sem fibra para os
sítios estritos/união; fibra com indexação própria apenas para dep_total/d e prova da
redução), replay próprio, tabela de transição II própria a partir de θ, fórmula-θ
própria, K-audit próprio. **4312 comparações, 0 discrepâncias**
(`ws3-verificacao-independente.json`: `VERIFICADO_SEM_DISCREPANCIAS`), incluindo, na
bateria, igualdade com os registos dos DATASETS registados (nivel, dep_sites, d0/d1
onde presentes) e replay theta_sha 126/126.

**2.1 fam-20 (7bb0baab3a8ed7aa, n=12, tabela cega).** Órbita 25 (=Fase 5), s0=1689,
tipos [C_BA, D2, A, B, D1, C_AB]. Ambas as arestas: nível L1 (d_0=d_1), dep_total
4608 = 128 × 36 células-sítio (de 144 = 16 células × 9 intervenções), ambos os contextos
de memória alcançados (C_AB->B: 15 estados m=0 / 10 m=1; C_BA->A: 12/13).

| aresta | granularidade | suporte m0/m1 | união | interseção | sítios união | sítios ESTRITOS | categoria |
|---|---|---|---|---|---|---|---|
| C_AB->B | configuração (n=12) | 15/10 | 25 | **0** | 54 | 0 | UNIAO_APENAS_B1 |
| C_AB->B | config. nuclear (s/ D) | 14/10 | 23 | **1** | 51 | **3** | **ESTRITO** |
| C_AB->B | **(r,c)** | 11/7 | 14 | **4** | 30 | **9** | **ESTRITO** |
| C_BA->A | configuração (n=12) | 12/13 | 25 | **0** | 51 | 0 | UNIAO_APENAS_B1 |
| C_BA->A | config. nuclear (s/ D) | 12/12 | 24 | **0** | 48 | 0 | UNIAO_APENAS_B1 |
| C_BA->A | **(r,c)** | 8/10 | 13 | **5** | 27 | **9** | **ESTRITO** |

- Replicação exata do critério OR anterior: sítios de união por configuração (n=12) =
  {54, 51} — os "51 e 54 sítios/aresta" do teste OR eram uniões com um dos lados
  contrafactual; a parte bilateral-realizada é o que este relatório isola.
- Células estritas: C_AB->B I = {(0,1),(2,0),(3,1),(3,3)}; C_BA->A I =
  {(0,0),(0,3),(1,0),(1,3),(3,2)} (confirmadas manualmente na tabela de coordenadas da
  órbita, `orbita_coords`).
- 9 testemunhas estritas por aresta (intervenção × célula com padrão m0 ≠ m1); exemplos:
  C_AB->B int#7 (mk=1025,vl=1024) em (0,1): padrão 6 vs 0; C_BA->A int#2 (mk=128,vl=128)
  em (1,0): 0 vs 1. Lista completa em `ws3-strict-fam20.json`.
- **Contraste observacional (D7, sem cirurgia)**: C_AB->B r=3 (c1=1,c2=3): O_m0=2,
  O_m1=0 → difere; C_BA->A r=1 (c1=0,c2=3): 1 vs 0 → difere (r=0 (0,3): 1 vs 1, não).
  Ou seja, π_0 ≠ π_1 é visível em AMBAS as arestas só com transições realizadas.
- Instância: ≥1 aresta ESTRITO = sim; ambas = **sim**.

**2.2 Bateria pré-definida** (precommit G2 = TODOS os 46 colapso_total dos lotes
910000001/910000002; G3 = 40 controlos L3/L3; G4 = 40 mistos; replay theta_sha 126/126;
cross-checks X1-X6: 252/252 arestas em nivel, dep_sites, d0/d1 (132 presentes), redução
(r,c) sem exceções, fórmula-θ (d e padrões), K⟺L1).

Categorias por aresta, granularidade primária (r,c):

| grupo | n arestas | ESTRITO | UNIAO_B1 | UNIAO_B2 | PURO_CTF | SEM_DEP |
|---|---|---|---|---|---|---|
| G2 colapso (total) | 92 | **74 (80,4% [71,2-87,3])** | 6 | 11 | 0 | 1 |
| — G2 L1+L1 | 58 | 46 | 3 | 8 | 0 | 1 |
| — G2 L1+L2 | 20 | 16 | 2 | 2 | 0 | 0 |
| — G2 L2+L2 | 14 | 12 | 1 | 1 | 0 | 0 |
| G3 controlo L3/L3 | 80 | **65 (81,3% [71,3-88,3])** | 15 | 0 | 0 | 0 |
| G4 misto | 80 | **64 (80,0% [70,0-87,3])** | 8 | 8 | 0 | 0 |

Configuração completa (ultra-estrita): ESTRITO G2 15/92 (16,3%), G3 15/80 (18,8%),
G4 8/80 (10,0%); domina UNIAO_APENAS_B1 (interseções vazias). Por nível de aresta,
(r,c): L1 (97): 75 ESTRITO, 14 B2, 7 B1, 1 SEM_DEP; L2 (35): 29 ESTRITO; L3 (120):
99 ESTRITO. Instâncias, (r,c): G2 ambas 32/46, ≥1 42/46 (91,3% [80,0-96,6]); G3 29/40 e
36/40 (90,0%); G4 27/40 e 37/40 (92,5%). |I| mediana 2-4 células; sítios estritos por
aresta: mediana 6 (G2 L1+L1), 9 (L1+L2), 5,5 (L2+L2), 11,5 (G3), 4 (G4). Observacional:
par presente em 46/92 (G2), 48/80 (G3), 36/80 (G4); par DIFERENTE em 29/92 (G2; 19/58
nos L1+L1), 45/80 (G3), 23/80 (G4). Único SEM_DEP: lote 910000001 t=14155, C_AB->B,
dep_total=0 (nível L1) — sem dependência em parte alguma da fibra.

**2.3 Baseline populacional fresco** (EMENDA 1 precommit, escrita antes de correr; seed
910000010 da reserva ws3; N=200 famílias II aceites de 650 amostradas, taxa 0,308;
mesmas definições; implementação verificada acima). Por aresta (400): níveis L3 385
(96,25%), L1 14 (3,5%), L2 1 (0,25%) — consistente com N=10000 (95,35/3,53/1,13).
Categorias (r,c): **ESTRITO 345/400 = 86,3% [82,5-89,3]**, UNIAO_B1 40, UNIAO_B2 14,
**PURO_CONTRAFACTUAL 1 (0,25%)**; configuração completa: ESTRITO 46/400 = 11,5%.
Instâncias: ≥1 ESTRITO 196/200 = **98,0% [95,0-99,2]**; ambas 149/200 = 74,5%. Órbitas:
mediana 19 estados (min 6, max 61). Observacional: par diferente em 171/400 (42,8%).
Cross-tab nas L1 frescas (14): 12 ESTRITO, 1 UNIAO_B2, 1 PURO_CONTRAFACTUAL. O único
caso PURO_CONTRAFACTUAL (t=113, C_AB->B, L1): dep_total=384 (12 células-sítio na fibra)
mas 0 sítios mesmo na união dos suportes realizados; |I|=3; par observacional presente
sem diferença — dependência exclusivamente contrafactual, existe mas é rara (1/652
arestas analisadas nesta fase).

## 3. DERIVATION (analítica; precede e fundamenta a enumeração)

**Proposição 1 (localidade da resposta; cancelamento de σ e da memória).** Na variante
II, aresta C_AB->B, fibra condicionada em mB=m. Seja z um ponto da fibra com y(z)=r,
cAB(z)=c, e (J,η) uma intervenção nos bits de C_AB com valor efetivo c′=(c&~m_J)|η no
canal. Pelo passo congelado (y′ = G0[y][π_mB(cAB)] ⊕ σB[mB]; mB′ = K[mB][y];
intervenção transitória = substituir bits e aplicar UMA transição):

    xr(z; J,η) = eB[T[z_do]] ⊕ eB[T[z]] = ( G0[r][π_m(c)] ⊕ G0[r][π_m(c′)] , 0 )

— σB[m] cancela no XOR; a componente de memória K[m][r] não depende de cAB, logo é 0.
A resposta depende do ponto APENAS através de (r,c), dado m e a intervenção. Análogo
exato para C_BA->A com (F0, π_mA, σA, H; r=x, c=cBA). ∎
*Corolário 1 (partição canónica):* as células (r,c) são a partição de comparabilidade
exata mais grossa (pontos da mesma célula têm respostas idênticas para todas as
intervenções; células distintas podem diferir).
*Corolário 2 (multiplicidade):* d_m = mult · Σ_células pc(padrão), mult = 2^{n-1}/16
(32 em n=10, 128 em n=12) — reproduz a decomposição da autópsia e o lema d_E2 = 4·d_E1.
*Corolário 3 (invariância de embedding):* C_m, I, U e os sítios (r,c) são invariantes ao
acrescento de módulos inertes (bits D não entram em (r,c) nem em m); a interseção
estrita por CONFIGURAÇÃO não é invariante (bits D entram na chave de igualdade).
Instanciação na fam-20: C_AB->B tem interseção nuclear 1 (3 sítios estritos) que
desaparece (0) na configuração n=12 — os dois estados nucleares coincidentes visitam
bits D diferentes.

**Proposição 2 (boa definição no suporte realizado).** Por Prop. 1, para (r,c) ∈ I a
comparação xr_0 vs xr_1 avaliada em QUAISQUER testemunhas realizadas (estados da órbita,
um por contexto) é bem definida e igual à comparação na fibra alinhada. Verificação:
asserts de igualdade testemunha-vs-fibra e constância por célula em TODAS as arestas
analisadas (252 da bateria com fibras completas n=10; fam-20 com fibras n=12 de 2048
pontos; 400 do baseline): **0 exceções**.

**Proposição 3 (contraste observacional).** Para (r,c1),(r,c2) ∈ I com o mesmo r e
testemunhas realizadas do mesmo contexto m: O_m = eB[T[s(r,c1,m)]] ⊕ eB[T[s(r,c2,m)]] =
( M[r][π_m(c1)] ⊕ M[r][π_m(c2)] , 0 ): σ cancela entre as duas células (mesmo m) e a
componente K cancela (mesmo r). Logo O_0 ≠ O_1 ⇒ π_0 ≠ π_1 testemunhado SEM cirurgia,
apenas com transições realizadas. (Recíproco não vale: O_0 = O_1 não implica π_0 = π_1.)

**Proposição 4 (relação com a condição K).** K (τ = π_1∘π_0⁻¹ ∈ Iso(W_M)) ⟺ d_0 = d_1
(agregado na fibra COMPLETA; teorema da autópsia, reverificado aqui em 252/252 arestas
via K-audit próprio). K NÃO implica igualdade ponto-a-ponto nas células comparáveis
realizadas: a fam-20 satisfaz K em ambas as arestas e mesmo assim tem 9 sítios estritos
por aresta. O cancelamento de K vive no somatório sobre a fibra completa; o suporte
realizado estrito não o herda.

## 4. EMPIRICAL SUPPORT (resumo do que sustenta cada facto)

- Prop. 1-3 verificadas exaustivamente por duas implementações independentes (fibra
  alinhada, `ws3_lib.py`; testemunhas realizadas, `ws3_indep.py`) com 4312 comparações
  cruzadas e 0 discrepâncias; padrões por célula derivados SÓ de θ coincidem com os da
  tabela em 126/126 famílias (2×9×16 padrões cada aresta).
- Replays: theta_sha verificado em 126/126 alvos das sementes REGISTADAS
  910000001/910000002; nenhum uso de sementes proibidas; baseline fresco só com
  910000010, N e plano fixados em precommit-emenda antes da execução.
- Cross-checks contra dados registados: nivel/dep_sites 252/252, d0/d1 132/132; fam-20:
  L1/L1, dep 4608/4608, OR {51,54} replicado; órbita 25 = Fase 5.
- Reprodutibilidade: re-execução dos scripts da tentativa interrompida produziu
  `ws3-strict-fam20.json` byte-idêntico; bateria idêntica exceto `duracao_s`.
- Todos os números da secção 2 têm origem em `ws3-strict-fam20.json`,
  `ws3-strict-bateria.json`, `ws3-fresh-baseline.json` (IC95 Wilson) no ws3 dir.

## 5. INFERENCE (interpretação suportada pelos factos acima)

1. **O mecanismo II está presente na dinâmica realizada da instância confirmatória
   falhada, no sentido estrito.** Em ambas as arestas do núcleo há células (r,c)
   visitadas nos DOIS contextos de memória com resposta intervencional diferente
   (9 sítios/aresta), e há testemunhas observacionais sem cirurgia em ambas. A
   classificação da fam-20 é ESTRITO/ESTRITO na granularidade canónica; na aresta
   C_AB->B a dependência sobrevive até à granularidade ultra-estrita nuclear.
2. **O colapso de C1′ na fam-20 não é desculpável por "mecanismo não realizado", "só na
   união dos suportes" ou "puramente contrafactual"** — as três alternativas ficam
   excluídas pelos dados. Combinado com a condição K, o quadro fecha: a informação que
   distingue II existe no suporte realizado comparável; perde-se exclusivamente na
   agregação (soma de Hamming na fibra completa, invariante sob a isometria τ).
3. **Realização estrita é a norma populacional, não a exceção**: 80-86% das arestas e
   90-98% das instâncias (≥1 aresta) em colapsos, controlos L3/L3, mistos e baseline
   fresco. Os colapsos NÃO são deficitários em realização estrita face aos controlos
   (ICs sobrepostos) — o que reforça: o defeito de C1′ é de agregação, não de suporte.
4. **O critério por configuração completa é inadequado como critério estrito canónico**:
   interseções quase sempre vazias (órbitas de ~20-25 estados vs 512/2048 configurações
   livres), leitura dependente do embedding (Corolário 3; fam-20 nuclear 1 vs n=12 0), e
   exige igualdade de bits provadamente irrelevantes para a resposta comparada. Os "0
   sítios estritos" da fam-20 nessa granularidade são artefacto de escassez de suporte e
   dos bits D, não ausência de dependência realizada.
5. **Dependência puramente contrafactual existe mas é rara** (1/652 arestas nesta fase;
   0 na bateria, 1 no baseline): quase sempre a dependência de memória da fibra toca o
   suporte realizado, e tipicamente a sua interseção bilateral.
6. Os 51/54 sítios do teste OR anterior decompõem-se agora: parte bilateral-realizada
   não-vazia e decisiva (9 sítios estritos/aresta na fam-20 ao nível (r,c)) + resto com
   um lado contrafactual.

## 6. SPECULATION (rotulado; sem qualquer proposta de correção)

- A separação perfeita observada (fam-20 e a maioria dos colapsos têm sítios estritos
  realizados) sugere que a informação discriminante de II está frequentemente disponível
  em estatísticas pontuais sobre o suporte realizado comparável; se alguma
  operacionalização admissível a poderia usar SEM falsos positivos em III é
  desconhecido, não foi testado, e está fora do âmbito (regra 4; pergunta 3 da autópsia).
- O défice não significativo de ESTRITO nos colapsos vs baseline (80,4% vs 86,3%,
  ICs sobrepostos) poderia refletir acoplamento fraco entre a condição K e a riqueza do
  suporte realizado (via órbitas/elegibilidade); sem suporte estatístico atual.
- Heurística para a dominância do ESTRITO: com ~25% das 144 células-sítio diferentes
  (caso típico L1; 36/144 na fam-20) e |I| mediano ~3 células, a probabilidade de ≥1
  sítio estrito é alta; PURO_CONTRAFACTUAL exigiria que TODAS as células de I e U
  caíssem em células sem diferença — raro, como observado (0,25%).
- A testemunha observacional (43% das arestas no baseline) sugere que uma fração
  substancial do mecanismo II é identificável apenas com dados realizados, sem qualquer
  intervenção — mas não universalmente (fam-20 tem-na; o caso PURO_CONTRAFACTUAL não).

## 7. Questões abertas

1. Especificidade em III: sob os mesmos critérios estritos realizados, com que
   frequência instâncias III exibiriam "diferenças" espúrias? (Pergunta 3 da autópsia;
   fora do mandato ws3.)
2. Sensibilidade da classificação a órbita = só-ciclo (D1 fixou transiente+ciclo; não
   recomputado).
3. Caracterização formal da prevalência de PURO_CONTRAFACTUAL (~0,25% de arestas) e a
   sua dependência do comprimento da órbita.
4. Ligação quantitativa entre a classe de conjugação de τ / |Iso(W_M)| e a contagem de
   sítios estritos realizados (ponte para o workstream da condição K).
5. Variante ponderada por multiplicidade de visita no ciclo (aqui: suporte não
   ponderado, por decisão precommit).

## 8. Ficheiros e reprodução (tudo em `multiagent/ws3-realized-dynamics/`)

Precommits: `precommit-ws3-strict.txt` (definições D1-D10, bateria, cross-checks;
anterior à execução) · `precommit-ws3-fresh-emenda.txt` (baseline; anterior à execução).
Scripts de análise: `ws3_lib.py`, `ws3_fam20.py`, `ws3_bateria.py` (execução principal);
`ws3_indep.py`, `ws3_verifica.py` (verificação independente); `ws3_fresh.py` (baseline).
Outputs: `ws3-strict-fam20.json`, `ws3-strict-bateria.json`,
`ws3-verificacao-independente.json`, `ws3-fresh-baseline.json`, `*.out`.
Proveniência: `tentativa-interrompida-1/` (primeira execução, interrompida antes do
relatório; auditada; outputs sha-verificados e reproduzidos byte-a-byte).
Ambiente: `/root/prereg-env/bin/python` 3.14.4 + NumPy 2.5.2; instrumento congelado
`frozen-copy/` (12/12 vs MANIFEST, verificado no início E no fim desta sessão; nota de
proveniência: `frozen-copy/__pycache__/` (bytecode) foi criado às 13:37:48Z pela
primeira execução interrompida, anterior a esta sessão — as execuções desta sessão
usaram `PYTHONDONTWRITEBYTECODE=1` e não escreveram lá nada; os fontes `.py` estão
sha-intactos). Sementes usadas: APENAS 910000001/910000002
(replay de famílias registadas) e 910000010 (baseline, reserva ws3, precommit-emenda);
sementes confirmatórias e queimadas nunca tocadas. sha256 de todos os ficheiros:
`SHAS.txt` neste diretório.

*Fim — POST-CONFIRMATORY / EXPLORATORY; o resultado confirmatório NEGATIVO permanece
fechado e imutável.*

# BOUNDARY I — FASE 6: ENCERRAMENTO FORMAL
**POST-CONFIRMATORY / EXPLORATORY — Pré-registo A v8.3**

> Este documento é **apenas um registo de encerramento**. Não altera a síntese,
> os workstreams, a autópsia ou qualquer artefacto; não recalcula resultados;
> não executa simulações; não consome sementes; não propõe C1″; não reinterpreta
> o resultado confirmatório; não inicia o BOUNDARY II; não faz análise de prior
> art. Usa exclusivamente os artefactos finais já fechados
> (`FASE6-MULTIAGENT-SYNTHESIS.md`, sha256 `bd8b19e58a35696e111c92b65538c621526f49f7d9d6498bbbfba33b4c44e185`,
> e os relatórios WS1–WS5 nele auditados).

---

## 1. Resultado confirmatório

```text
resultado_confirmatorio_A = "negativo"
```

C1′ no teste confirmatório pré-registado:

- E1 = **150/150**
- E2 = **49/50**
- total = **199/200**
- `passa = false`
- única instância errada: **`7bb0baab3a8ed7aa`**, família 20, variante II, Estrato 2

> **O resultado confirmatório é NEGATIVO, definitivo e não é reinterpretado
> pela Fase 6.** A autópsia pós-confirmatória explica a falha; não modifica o
> resultado.

---

## 2. Estatuto da Fase 6

Toda a Fase 6 é classificada como **POST-CONFIRMATORY / EXPLORATORY**.

Regista-se que:

- os artefactos confirmatórios (`/root/causal-A-amd2-official/`) permaneceram
  **imutáveis** durante toda a fase (atributo `i` verificado pelo coordenador
  no fecho; nota registada na síntese: `resultado-pontuacao-A.txt` reside na
  raiz de `causal-A-amd2-official/`, não em `prereg-A/`);
- **nenhuma C1″ foi formulada**;
- **nenhum critério foi alterado** (protocolo v8.3, Amendments, candidatos,
  targets, thresholds e instrumento congelado intactos);
- **nenhuma análise pós-confirmatória foi usada para alterar o scoring
  oficial**.

---

## 3. Perguntas que a Fase 6 tinha de resolver — ENCERRADAS

Com base exclusiva nas respostas da síntese final (Q1–Q9):

1. **Porque falhou C1′ na família 20?** — Porque τ = π₁∘π₀⁻¹ pertence a
   Iso(W_M) nas duas arestas canal→processador: o remapeamento de memória é
   uma permutação isométrica da geometria de resposta, e o agregado de C1′ é
   constante em órbitas dessa isometria (cancelamento por agregação
   intra-célula de dependência real). [Q1, Q7]
2. **Onde exatamente desaparece a informação causal?** — Exclusivamente na
   agregação intra-célula (k,c): o popcount pontual destrói a identidade do
   bit (B1), a soma invariante a permutações destrói a localização (B2), a
   soma aritmética destrói a partição do total (B3, dominante); nunca entre
   blocos (B4=0, teorema); em L2 o rank destrói adicionalmente magnitude
   cardinal (quantum 64). [Q3]
3. **A modulação causal estava realmente realizada ou era apenas
   contrafactual?** — Estritamente realizada: células (r,c) visitadas pela
   órbita nos dois contextos de memória com resposta intervencional diferente
   (9 sítios estritos por aresta na família 20), com testemunhas
   observacionais sem cirurgia; a realização estrita é a norma populacional
   (80–86% das arestas). [Q4]
4. **Existe condição necessária e suficiente para L1?** — Sim:
   d₀=d₁ ⟺ W̃₀=W̃₁ ⟺ τ∈Iso(W_M). [Q2]
5. **Existe falha simétrica em III ao instrumento congelado?** — Não, por
   teorema (III-1): a horizonte 1 o campo XOR-intervencional é identicamente
   nulo; a especificidade de III é estrutural e determinística. [Q5]
6. **Os 46 colapsos representam uma classe mecanística ou várias?** — Uma
   única classe (compatibilidade de τ com o perfil observável da geometria W
   de cada aresta; L1 = versão métrica, L2 = versão ordinal do mesmo
   mecanismo); o clustering sem k não encontra estrutura empírica robusta.
   [Q6]
7. **A falha é bug, acaso, escala, suporte, ou mecanismo estrutural?** —
   Mecanismo estrutural: degenerescência rara de origem simétrica (grupo
   Iso(W_M)) que produz cancelamento por agregação — uma falha de
   identificabilidade do observável agregado, tipo-faithfulness relativa a
   C1′. Não é bug (≥4 implementações concordam inteiro a inteiro), não é
   escala (d_E2 = 4·d_E1), não é amostragem (determinístico dado θ), não é
   suporte não realizado. [Q7]
8. **Quais resultados estão provados e quais continuam conjecturais?** — Ver
   as listas "demonstrado" (11 itens, rotulados A/B/C/D) e "hipóteses"
   (8 itens, rotulados E) da síntese; resumo nas secções 4–6 deste registo.
   [Q8]

---

## 4. Conclusões formais encerradas

### 4.1 Condição L1

Para arestas canal→processador do Sistema II no instrumento congelado:

    d_0 = d_1  ⟺  W̃_0 = W̃_1  ⟺  τ = π_1∘π_0⁻¹ ∈ Iso(W_M)

**Estatuto: A + B + C + D** (taxonomia da síntese: provado analiticamente nas
duas direções; verificado exaustivamente no domínio finito; validado OOS em
amostras pré-comprometidas — sementes 910000004/5 e 910000050 —; reproduzido
internamente por múltiplos workstreams, incluindo a derivação sob firewall do
WS1, provadamente equivalente). **Não se reivindica novidade científica nesta
nota.**

### 4.2 Recíproca não tautológica no lattice congelado

- as nove intervenções **não** observam diretamente todos os seis graus de
  liberdade de W;
- só bits isolados → **posto 2**;
- só `do(c=γ)` → **posto 4**;
- lattice completo → **posto 6**;
- **determinante = −8** (inversa explícita; reproduzido pelo coordenador;
  202 contra-exemplos frescos para sub-lattices).

Logo a recíproca depende da combinação completa das nove sondas.

> **Nota epistemológica:** este resultado é matematicamente correto e não
> tautológico no instrumento congelado, mas o seu estatuto de novidade
> matemática depende da auditoria de prior art; a interpretação atual é que
> pertence à moldura conhecida de conjuntos determinantes/invariantes
> maximais. **Não é apresentado como novo teorema geral.**

### 4.3 Localização da perda

A perda L1 ocorre **dentro da agregação intra-célula**, e não: por ausência de
dependência ponto-a-ponto; por compensação entre blocos (B4=0, teorema); por
falta de realização dinâmica; por erro de escala.

Taxonomia observada das 705 arestas L1:

| modo | fração |
|---|---|
| perda já no popcount pontual (B1) | 4,2% |
| perda de localização por invariância a permutações (B2) | 24,9% |
| cancelamento aritmético estrito dentro de blocos (B3) | 70,9% |

A família 20 pertence ao **modo dominante** (B3, nas duas arestas).

### 4.4 Realização causal

A hipótese *"II apenas arquitetural, mas III na dinâmica realizada"* foi
**falsificada**. Na família 20:

- dependência total = **4608 sítios por aresta**;
- **9 sítios estritos por aresta** em células (r,c) realizadas nos dois
  contextos;
- existem **testemunhas observacionais sem cirurgia**.

> **A diferença causal existia na dinâmica realizada; a invisibilidade foi
> produzida pelo observável agregado.**

### 4.5 Classe de falha

- prevalência exploratória ≈ **0,46% por instância II sob a lei específica do
  gerador** (46/10 000; IC95 [0,345%, 0,613%]);
- subtipos: **29 L1/L1 · 10 L1/L2 · 7 L2/L2**;
- os casos pertencem a **uma única classe mecanística**:

> compatibilidade do remapeamento τ com o perfil observável da geometria de
> resposta de ambas as arestas, exatamente em L1 e ordinalmente em L2.

A correlação inter-arestas (~2,1–2,4×) fica explicada sem resíduo pelo
(τ, lam) partilhado com geometrias independentes (modelo exato M3: z=0,32
in-sample, z=0,57 OOS). **0,46% não é uma taxa universal** — é específica da
lei do gerador congelado.

### 4.6 Família 20

**C_BA→A:** Iso(W) = **S₄**. Geometria equidistante (todos os pares à
distância 4); a aresta é invisível a **qualquer** τ ao nível do observável
considerado.

**C_AB→B:** Iso(W) = **{id, (23)}**. O remapeamento realizado coincide
precisamente com a **única isometria não trivial** (transporte ρ = (23);
verificado com cálculo mostrado pelo coordenador, por despermutação própria da
tabela cega).

Consequentemente, as duas arestas são marcadas como ESTADO e o núcleo II é
fundido como III — o único erro confirmatório.

---

## 5. Resultado sobre III

### Horizonte 1 — Teorema III-1

> No campo XOR-intervencional congelado de uma única aplicação da transição, a
> dependência do estado de memória do receptor cancela exatamente.

Consequências: `dep = 0` **estruturalmente**; d₀=d₁; C1′ funde corretamente
III. **Não é regularidade estatística — é propriedade analítica do passo III**
(0/4000 arestas no WS4; 0/500 na amostra própria do coordenador).

### Horizonte 2 — Teorema III-2

> A invariância de primeira ordem não é estável sob composição temporal.

Medição exploratória: **3996/4000 arestas III (99,90%)** exibem dependência de
memória a h=2 (100% na amostra do coordenador; níveis L3 em ~83%; magnitudes
comparáveis às de um II a h1).

Formulação registada: **não-estabilidade temporal da invariância de III.**

O que **não** foi demonstrado: que "nenhuma extensão de C1′ por horizonte pode
funcionar". O que **foi** demonstrado: uma extensão direta que simplesmente
aplique o mesmo tipo de estatístico a T² perde a especificidade estrutural que
existe em T.

---

## 6. O que NÃO foi descoberto

A Fase 6 **não** demonstrou:

- uma lei universal de individuação causal;
- que todo o observável causal sofre exatamente esta falha (refutado para
  refinamentos: conjuntos cegos estritos 7 ⊂ 36 ⊂ 210 ⊂ 705);
- que toda a distinção ESTADO/SINAL depende necessariamente do horizonte;
- que nenhuma C1″ pode existir;
- que nenhuma individuação independente da resolução seja possível;
- uma teoria da consciência;
- uma taxa universal de 0,46%;
- novidade científica definitiva de qualquer teorema antes da auditoria de
  prior art.

---

## 7. Interpretação conceptual autorizada

*(Separada dos teoremas.)* A Fase 6 sustenta a seguinte interpretação:

> Para C1′, a fronteira causal obtida não é determinada apenas pelo sistema
> causal subjacente; depende também do observável utilizado. A análise de III
> mostra adicionalmente que a informação causal acessível ao observável pode
> depender do horizonte temporal.

Formulação conceptual de trabalho:

    individuação observada = f(sistema, observável, horizonte)

**INTERPRETAÇÃO / HIPÓTESE DE PROGRAMA — NÃO TEOREMA UNIVERSAL.**

---

## 8. Independência e validação

- **WS1** — derivação analítica **internamente independente sob firewall**
  (draft pré-firewall preservado como evidência); formulação própria
  (ρ = π₀⁻¹∘π₁ preserva agregados de Hamming) provadamente equivalente a
  τ∈Iso(W).
- **WS2–WS5** — reprodução/auditoria **interna** ao workflow.
- **Coordenador** — red-team com sementes próprias (910000050/51) e
  implementações próprias (sistema linear reproduzido, fam-20 reconstruída por
  despermutação independente, amostras frescas II N=400 e III N=250 com zero
  violações dos critérios pré-fixados).
- **Leitura posterior, externa ao workflow**, confirmou independentemente:
  determinante −8 / posto 6; forma fechada; K⟺L1; Teorema III-1; cálculos da
  família 20.

Mas:

> **Replicação científica externa plena ainda não ocorreu.** Toda a
> concordância entre agentes é verificação interna ao nível do workflow.

---

## 9. Questões abertas — congeladas, não executadas

Registadas como trabalho futuro, **sem iniciar qualquer trabalho**:

1. auditoria final de prior art;
2. fórmula fechada para P(K | classe de τ);
3. escalamento com o tamanho do alfabeto/memória;
4. caracterização completa da sub-família `dep = 0`;
5. limites formais de L2 (fecho dos lemas restantes);
6. trade-off sensibilidade/especificidade fora de h=1;
7. autópsia própria de C2/C3;
8. eventual desenho futuro de C1″ / BOUNDARY II.

Nenhuma destas questões faz parte da Fase 6 encerrada.

---

## 10. Declaração formal de encerramento

> **FASE 6 — CLOSED**
>
> A autópsia pós-confirmatória da única falha de C1′ está encerrada. O
> mecanismo da falha, a sua condição algébrica, o ponto de perda de
> informação, a realização dinâmica, a estrutura da classe de colapso e a
> especificidade de III no horizonte congelado foram suficientemente
> caracterizados para os objetivos definidos para esta fase.
>
> O resultado confirmatório permanece **NEGATIVO e imutável**.
>
> **Não foi formulada C1″.**
>
> Nenhum novo experimento é iniciado por este documento.
>
> O próximo passo do programa é externo à Fase 6 e exige decisão humana após
> conclusão da auditoria de prior art.

---

*Registo compilado exclusivamente a partir dos artefactos fechados da Fase 6:
`FASE6-MULTIAGENT-SYNTHESIS.md` (sha256 `bd8b19e5…e185`) e relatórios
WS1–WS5 auditados (shas no `SHA256SUMS.txt` histórico, inalterado). Nenhuma
computação nova, nenhuma semente consumida, nenhum artefacto alterado.*

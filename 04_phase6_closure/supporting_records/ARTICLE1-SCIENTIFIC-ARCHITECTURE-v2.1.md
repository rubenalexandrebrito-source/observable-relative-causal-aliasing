# BOUNDARY I — PASSO 4: ARQUITETURA CIENTÍFICA DO ARTIGO 1 — v2.1

**WORKING DOCUMENT — pós-confirmatório / pós-auditoria de prior art / pós-red-team**  
**Data:** 17-08-2026  
**Substitui editorialmente a v2, sem a apagar.**  
**Função:** versão candidata a freeze da arquitetura científica antes do Claim–Evidence Ledger e antes de qualquer redação do manuscrito.

> Este documento não altera o pré-registo, o scoring, a Fase 6, a autópsia ou a auditoria de prior art.
>
> O resultado confirmatório permanece:
>
> `resultado_confirmatorio_A = "negativo"`  
> `C1′ = 199/200`  
> `passa = false`

---

# 0. Regras epistemológicas obrigatórias

## 0.1 Resultado confirmatório

O resultado permanece literalmente negativo.

- E1: `150/150`;
- E2: `49/50`;
- total C1′: `199/200`;
- `passa = false`.

`199/200` é descrição do teste, não argumento de “near success”.

---

## 0.2 C1′ possui duas rotas de cegueira distintas

A condição exata

`d₀=d₁ ⇔ W̃₀=W̃₁ ⇔ τ∈Iso(W_M)`

caracteriza **L1**, isto é, a rota métrica de igualdade exata do perfil.

Não caracteriza toda a marca `STATE` de C1′.

C1′ usa invariância ordinal; existe também:

### L2 — ordinal aliasing

`d₀ ≠ d₁`

mas

`rank(d₀)=rank(d₁)`.

Logo:

- **L1:** metric aliasing;
- **L2:** ordinal aliasing;
- **STATE em C1′:** `rank(d₀)=rank(d₁)` = L1 ∪ L2.

A classe completa de colapso de uma instância II exige que ambas as arestas relevantes sejam marcadas `STATE`, por L1 ou L2.

---

## 0.3 Blindness não implica false invariance

A condição

`τ∈Iso(W)`

garante cegueira do observável da classe especificada:

`F(X₀)=F(X₁)`.

Mas isso não garante:

`X₀≠X₁`.

Portanto distinguir sempre:

### Blindness
`F(X₀)=F(X₁)`.

### Causal aliasing / false invariance
`F(X₀)=F(X₁)` **e** `X₀≠X₁`.

### Strictly realized causal aliasing
além do anterior, existe diferença causal numa granularidade local causalmente suficiente realmente visitada nos dois contextos.

Na família 20, esta terceira condição é satisfeita.

---

## 0.4 “Strictly realized” significa à granularidade causalmente suficiente `(r,c)`

A expressão não significa que a configuração global completa tenha de ser idêntica nos dois contextos.

No contraste estudado, condicionando em `m`, a resposta intervencional depende exatamente do par local `(r,c)`. Bits globais adicionais podem ser causalmente irrelevantes para esta resposta e tornar artificiais as interseções entre contextos.

Logo, a formulação autorizada é:

> **strictly realized at the causally sufficient local-state granularity `(r,c)`**

Na família 20 existem 9 sítios estritos por aresta a esta granularidade, além de testemunhas observacionais.

---

## 0.5 STATE/SIGNAL é target operacional do desenho

`STATE` e `SIGNAL` são rótulos operacionais pré-fixados no testbed.

Não constituem uma ontologia universal estabelecida.

Preferir:

- `pre-specified operational target`;
- `System-II target by construction`;
- `System-III target by construction`.

Evitar:

- `ground truth` sem qualificador;
- `genuinely belongs to STATE/SIGNAL`;
- qualquer leitura ontológica de sistemas naturais.

---

## 0.6 C2 e C3 devem ser reportados

O artigo não pode omitir os restantes resultados confirmatórios scored.

Devem aparecer, de forma compacta:

- C2: 74 erros;
- C3: 75 erros;
- ambos também erram a família 20.

Não foram mecanisticamente autopsiados nesta fase e não devem ser reinterpretados.

O foco pós-confirmatório em C1′ deve ser justificado porque foi o seu contraexemplo único que revelou o mecanismo estudado.

---

## 0.7 III-2 é dividido em analítico e empírico

### III-2a — proposição analítica
A identidade de cancelamento de `h=1` não se estende algebraicamente, de forma geral, a `T²`; após composição, a memória pode reaparecer nos índices/seletores internos.

### III-2b — resultado empírico exploratório
Na amostra estudada:

`dep2>0` em `3996/4000 = 99,90%` das arestas III.

Existem `4/4000` exceções.

Nunca apresentar `3996/4000` como teorema.

---

## 0.8 “Non-identifiability” deve ser qualificada

O fenómeno não é impossibilidade de identificação a partir de toda a informação causal disponível.

Observáveis mais finos encolhem o blind set.

Preferir:

- `observable-relative causal aliasing`;
- `interventional aliasing induced by aggregation`;
- `symmetry-induced blindness of the aggregate`.

---

## 0.9 Cronologia epistemológica visível

O artigo deve mostrar:

`PREREGISTRATION → CONFIRMATORY NEGATIVE → FAILURE IDENTIFIED → POST-CONFIRMATORY AUTOPSY → ANALYTIC CHARACTERIZATION → PRIOR-ART AUDIT`

Isto deve estar no main paper ou Extended Data.

---

# 1. Decisão editorial central

O Artigo 1 deve ser um paper sobre **observable-relative causal aliasing**, descoberto através de uma falha confirmatória pré-registada.

Não deve ser:

- um paper a defender C1′;
- um paper sobre “99,5% de acerto”;
- um paper sobre a descoberta genérica de que simetrias causam não-observabilidade;
- um paper sobre a descoberta genérica de que o horizonte temporal importa;
- um paper sobre uma solução universal do problema STATE/SIGNAL;
- um paper que confunda L1 com toda a decisão de C1′.

A história principal é:

1. C1′ foi pré-registado e testado cegamente;
2. o resultado confirmatório foi negativo;
3. os restantes candidatos confirmatórios C2/C3 também falharam e são reportados;
4. a instância falhada de C1′ continha diferença causal real;
5. essa diferença era estritamente realizada a uma granularidade local causalmente suficiente;
6. uma rota métrica de cegueira foi caracterizada exatamente por simetria da geometria de resposta;
7. C1′ contém ainda uma rota ordinal L2, distinta da isometria exata;
8. observáveis mais finos recuperam parte da informação;
9. a conclusão é sobre o quociente preservado por um observável, não sobre ausência de causalidade.

---

# 2. Pergunta científica do artigo

> **When can an interventional observable become invariant across receiver states even though the underlying causal response changes?**

Em formulação operacional:

> **Quando pode um observável intervencional declarar invariância entre contextos internos do receptor apesar de a resposta causal subjacente mudar — inclusive numa granularidade causalmente suficiente realmente visitada?**

A resposta principal tem duas camadas:

- uma rota métrica L1, caracterizada exatamente;
- uma rota ordinal L2, instrumentalmente distinta.

---

# 3. Tese científica principal em quatro camadas

## 3.1 Camada A — existe diferença causal abaixo do observável

Na família confirmatória 20:

`X₀ ≠ X₁`

no campo de resposta intervencional.

A diferença é estritamente realizada à granularidade local `(r,c)` em ambos os contextos.

---

## 3.2 Camada B — o Sistema II realiza uma estrutura de pull-back contextual

No passo II congelado, a resposta relevante assume a forma:

`R[r][π_m(c)] ⊕ σ[m]`

com atualização de memória independente do canal no passo corrente.

Sob diferenciação XOR:

- `σ[m]` cancela;
- a memória entra no contraste através de `π_m`;
- os dois contextos correspondem a relabelings da mesma geometria causal subjacente.

O transporte relativo é:

`τ = π₁ ∘ π₀⁻¹`.

Este é o elo causal que liga o gerador ao teorema abstrato de invariância.

---

## 3.3 Camada C — rota métrica de blindness

O mecanismo receptor induz a geometria de resposta `W_M`.

Se:

`τ∈Iso(W_M)`,

então os observáveis da classe que factoriza pelo campo de pesos/células preservado por essa geometria são invariantes.

Isto produz **blindness**.

Quando, adicionalmente, `X₀≠X₁`, há **causal aliasing**.

Na família 20, `X₀≠X₁` e a diferença é estritamente realizada.

---

## 3.4 Camada D — rota ordinal adicional de C1′

Mesmo quando:

`τ∉Iso(W_M)`,

C1′ pode ainda marcar `STATE` se:

`rank(d₀)=rank(d₁)`.

Esse estrato L2 resulta da combinação entre:

- o emparelhamento não sondado;
- a ação de `τ`;
- o coarsening por weak rank.

Logo, a simetria métrica exata explica L1, mas não esgota a cegueira de C1′.

---

# 4. Hierarquia formal dos resultados

## 4.1 Lemma 1 — contextual pull-back realization in frozen System II

### Conteúdo

O gerador congelado realiza a forma:

`X_m = pullback_{π_m}(X_base)`

para o contraste relevante, porque:

- resposta do receptor = `R[r][π_m(c)]⊕σ[m]`;
- atualização de memória não depende do canal no passo;
- XOR cancela `σ`;
- a fibra é alinhada.

### Estatuto

Pós-confirmatório, analítico, específico das hipóteses formais explicitadas.

---

## 4.2 Proposition 1 — symmetry blindness for cell-factorizing observables

### Domínio

Dois contextos cujos campos são pull-backs de um tensor fixo por relabelings `π_m`, com geometria de resposta par-a-par `W`.

### Conteúdo

Se `F` factoriza apenas pelo campo de células induzido por `W`, então:

`τ∈Iso(W) ⇒ F(X₀)=F(X₁)`.

### Limite

Isto demonstra blindness.

Só existe **false invariance/causal aliasing** se também:

`X₀≠X₁`.

### Estatuto

- analítico;
- geral dentro das hipóteses da classe;
- matemática de invariância subjacente conhecida;
- não é novelty claim de teoria de grupos.

---

## 4.3 Theorem 1 — exact characterization of the metric blind route in the frozen instrument

Para as arestas canal→processador e o lattice congelado:

`d₀=d₁ ⇔ W̃₀=W̃₁ ⇔ τ∈Iso(W_M)`.

A recíproca depende do conjunto determinante:

- sub-lattice A: posto 2;
- sub-lattice B: posto 4;
- lattice completo: posto 6;
- determinante `−8`.

### Estatuto

- exato para L1 no instrumento;
- não caracteriza L2;
- não caracteriza sozinho toda a marca STATE;
- não constitui novo princípio matemático geral.

---

## 4.4 Proposition 2 — ordinal blind route of C1′

### Conteúdo

C1′ marca uma aresta `STATE` quando:

`rank(d₀)=rank(d₁)`.

Logo:

- L1: `d₀=d₁`;
- L2: `d₀≠d₁` mas ranks iguais.

No instrumento, L2 depende da interação entre o remapeamento `τ`, a emparelhação não sondada e o weak-rank coarsening.

O teorema do alinhamento restringe onde L2 pode ocorrer.

### Estatuto

- pós-confirmatório;
- analítico + empírico;
- secondary technical novelty candidate;
- a matemática-base de `S₄→S₃`, `V₄` e weak orders é conhecida.

---

# 5. Distinção conceptual obrigatória

O artigo deve mostrar:

### Campo causal completo
`X₀≠X₁` pode ou não ocorrer.

### Campo de células / geometria
pode tornar-se invariante por isometria.

### Perfil métrico
L1 se `d₀=d₁`.

### Perfil ordinal
L2 se `d₀≠d₁` mas ranks iguais.

### C1′
STATE se L1 ou L2.

Portanto:

> **“Invariant under the measured representation” does not entail “causally unchanged”.**

Mas apenas quando existe, separadamente, evidência de `X₀≠X₁`.

---

# 6. Estrutura final do manuscrito

## 1. Introduction

Apresentar:

- problema operacional de distinguir interações mecanisticamente diferentes;
- invariância intervencional como estratégia plausível;
- teste pré-registado;
- resultado negativo;
- contraexemplo;
- pergunta científica aberta pela falha.

### Quatro contribuições headline

1. **Transparent preregistered negative result.**
2. **Exact characterization of a metric symmetry-induced blind route.**
3. **Demonstration that the confirmatory counterexample contains a strictly realized causal difference at a causally sufficient local-state granularity.**
4. **Characterization of how observable refinement and ordinal coarsening alter the blind set.**

P7 não é headline.

---

## 2. Results

### 2.1 The preregistered evaluation is negative

Mostrar todos os outputs confirmatórios relevantes.

#### C1′
- E1 = 150/150;
- E2 = 49/50;
- total = 199/200;
- `passa=false`.

#### C2
- 74 erros.

#### C3
- 75 erros.

Explicar que o artigo autopsia mecanisticamente C1′, não C2/C3.

Fechar com:

> **Why did C1′ fail on a system constructed under the preregistered System-II target?**

---

### 2.2 The C1′ counterexample contains a real, strictly realized causal difference

Mostrar:

- `dep=4608` por aresta;
- ambos os contextos de memória atingidos;
- resposta condicionada por `(r,c)`;
- `(r,c)` como granularidade causalmente suficiente do contraste;
- 9 sítios estritos por aresta;
- testemunhas observacionais;
- rejeição da hipótese “II arquitetural mas dinamicamente indistinguível”.

---

### 2.3 Receiver state induces a contextual pull-back

Introduzir:

`m_B → π_m → τ`.

Derivar a forma do contraste congelado:

`R[r][π_m(c)]⊕σ[m]`.

Mostrar:

- cancelamento de `σ`;
- memória via `π_m`;
- atualização de memória independente do canal no passo;
- correspondência com o Lemma 1.

---

### 2.4 Mechanism-dependent symmetry creates metric blindness

Introduzir `W_M`.

Apresentar Proposition 1:

`τ∈Iso(W_M) ⇒ F(X₀)=F(X₁)`.

Dizer explicitamente:

> this is a blindness condition; it becomes causal aliasing only when the underlying fields differ.

Aplicar à família 20:

- uma aresta: `Iso(W)=S₄`;
- outra: `Iso(W)={id,(23)}`;
- transporte realizado `(23)`;
- `X₀≠X₁`;
- portanto a família 20 é witness de causal aliasing, não apenas de invariância.

---

### 2.5 The frozen intervention set makes the metric condition exact

Apresentar Theorem 1:

`d₀=d₁ ⇔ W̃₀=W̃₁ ⇔ τ∈Iso(W_M)`.

Incluir:

- posto 2/4/6;
- det `−8`;
- determining set.

Título e texto devem dizer sempre:

> **metric blind route / L1**

e não “complete C1′ blindness”.

---

### 2.6 Beyond exact isometry: ordinal aliasing in C1′

Definir L2:

`d₀≠d₁` mas `rank(d₀)=rank(d₁)`.

Mostrar:

- L2 não exige isometria exata;
- 17/24 arestas L2 dos 46 colapsos têm `Iso(W)` trivial;
- a zona cega do instrumento está ligada à emparelhação não sondada;
- weak rank pode preservar a posição ordinal apesar de mudança cardinal.

Enunciar o teorema do alinhamento em forma curta.

Prova completa → Methods/Supplement.

---

### 2.7 Where information is lost — and where it survives

Usar conjuntos nomeados, não apenas números:

`B_pattern ⊂ B_row ⊂ B_multiset ⊂ B_W`.

Na população estudada de 20 000 arestas II:

- `|B_pattern| = 7`;
- `|B_row| = 36`;
- `|B_multiset| = 210`;
- `|B_W| = 705`.

Explicar que:

- o nesting/refinement é estrutural;
- as cardinalidades são empíricas e generator-specific.

Pipeline:

`full response field`
→ `pointwise pattern/popcount`
→ `row-resolved`
→ `multiset`
→ `cell-weight geometry`
→ `d`
→ `weak rank`.

Mensagem:

> **the blind set shrinks under refinement.**

---

### 2.8 Population scope under the frozen generator

Apresentar:

- 46/10 000 colapsos na população principal;
- intervalos;
- OOS/replicações internas em torno da mesma ordem de grandeza;
- taxas observadas entre amostras aproximadamente 0,32%–0,50%;
- 29 L1/L1, 10 mistos L1/L2, 7 L2/L2 na amostra principal;
- nenhuma generalização para frequência natural/universal.

Não apresentar `0,46%` como constante da classe de sistemas.

---

### 2.9 Extended result — temporal composition

**Recomendação: mover para Extended Results / Supplement na primeira versão.**

Se mantido no corpo:

- III-1: nulidade exata em `h=1`;
- III-2a: não-iteração algébrica;
- III-2b: `3996/4000` empiricamente.

Nunca apresentar a taxa como teorema.

---

## 3. Discussion

### 3.1 What failed?
C1′ falhou o critério conjuntivo pré-registado; C2 e C3 também falharam e são reportados.

### 3.2 What was characterized?
Uma rota métrica de cegueira relativa ao observável, determinada pela compatibilidade entre contextual relabeling e response-geometry symmetry.

### 3.3 What else does C1′ lose?
Uma rota ordinal L2 adicional, dependente do instrumento.

### 3.4 What is not being claimed?
- não universalidade;
- não ontologia STATE/SIGNAL;
- não impossibilidade global de individuação;
- não nova teoria de simetrias;
- não nova teoria geral de causal abstraction;
- não causal aliasing sempre que `τ∈Iso(W)`;
- não claim sobre consciência.

### 3.5 Why does it matter?
Porque a invariância medida pode ser propriedade do quociente/representação preservado pelo observável.

---

## 4. Methods

### 4.1 Operational targets and construct validity
### 4.2 Preregistered protocol and blinding
### 4.3 Full confirmatory scoring: C1′/C2/C3
### 4.4 Response-field definitions
### 4.5 Proof that `(r,c)` is causally sufficient for strict comparability
### 4.6 Contextual pull-back lemma for System II
### 4.7 Response geometry `W_M`
### 4.8 Class-level symmetry blindness proposition
### 4.9 Exact L1 theorem for the determining intervention set
### 4.10 L2 / alignment theorem
### 4.11 Strict-realization analysis
### 4.12 Information-loss refinement hierarchy
### 4.13 Population/prevalence study
### 4.14 Temporal analysis
### 4.15 Internal verification / reproducibility

---

# 7. Epistemic provenance box

| Etapa | Estatuto |
|---|---|
| protocolo + C1′/C2/C3 | pré-registado |
| E1/E2 | confirmatório, cego |
| C1′ 199/200, `passa=false` | confirmatório |
| C2 74 erros; C3 75 erros | confirmatório |
| identificação da família 20 | pós-scoring |
| autópsia de C1′ | pós-confirmatório |
| Lemma 1 / Proposition 1 / Theorem 1 | pós-confirmatório analítico |
| L2/alignment | pós-confirmatório |
| prevalence study | pós-confirmatório / exploratório |
| III-1/III-2 | pós-confirmatório |
| prior-art audit | posterior à caracterização |
| eventual estudo futuro | separado; não pertence a este dataset |

---

# 8. Evidence-status map

| Resultado | Estatuto | Evidência |
|---|---|---|
| C1′ 199/200, negativo | confirmatório | scoring pré-registado |
| C2 74 erros | confirmatório | scoring pré-registado |
| C3 75 erros | confirmatório | scoring pré-registado |
| `X₀≠X₁` fam-20 | pós-confirmatório demonstrado | B+D |
| estrito `(r,c)` fam-20 | pós-confirmatório demonstrado | A+B+D |
| System-II pull-back form | pós-confirmatório analítico | A+B+D |
| `τ∈Iso(W) ⇒ blindness` na classe | pós-confirmatório analítico | A |
| `d₀=d₁ ⇔ τ∈Iso(W_M)` | pós-confirmatório analítico + validação | A+B+C+D |
| L2 / ordinal aliasing | pós-confirmatório analítico + empírico | A+B+C+D |
| blind-set refinement | pós-confirmatório | A parcial+B+D |
| prevalência 46/10 000 | exploratório generator-specific | C+D |
| III-1 | pós-confirmatório analítico | A+B+C+D |
| III-2a | pós-confirmatório analítico | A |
| III-2b 3996/4000 | exploratório | C+D |
| implicação ampla para individuação | interpretação | não teorema |
| sistema–observável–horizonte | hipótese conceptual | não teorema |

---

# 9. Figuras principais

## Figure 1 — Preregistered evaluation and why it is negative

Painéis:

A. target operacional System II vs III  
B. C1′ decision logic  
C. preregistration → blind run → scoring  
D. resultados confirmatórios:
- C1′ E1 150/150;
- C1′ E2 49/50;
- conjunctive target failed;
- `passa=false`;
- C2/C3 summary.

Não destacar “99,5%”.

---

## Figure 2 — The counterexample contains a strictly realized causal difference

Painéis:

A. arquitetura fam-20  
B. contextos de memória  
C. prova da suficiência local `(r,c)`  
D. 9+9 strict witnesses / observational witnesses.

Mensagem:

`X₀≠X₁` antes de qualquer agregação.

---

## Figure 3 — Metric blindness and ordinal aliasing

Painel A — rota métrica:

`m_B`
→ `π_m`
→ `τ`
→ `W_M`
→ `τ∈Iso(W_M)`
→ `W̃₀=W̃₁`
→ `d₀=d₁`
→ L1.

Painel B — rota ordinal:

`d₀≠d₁`
→ same weak rank
→ L2
→ same C1′ STATE label.

Painel C — família 20:
- `S₄`;
- `{id,(23)}`;
- `τ=(23)`.

Esta é a figura central.

---

## Figure 4 — Blindness shrinks under observable refinement

Painel A:

`B_pattern ⊂ B_row ⊂ B_multiset ⊂ B_W`

com contagens:

`7 ⊂ 36 ⊂ 210 ⊂ 705 / 20,000`.

Painel B:

L1/L2/L3 + colapsos por instância.

Painel C opcional:
OOS range / generator-specific note.

Temporal h1/h2 vai preferencialmente para Extended Data.

---

# 10. Toy model mínimo

O toy model aparece imediatamente após Proposition 1.

Funções:

- mostrar `X₀≠X₁`;
- mostrar `τ∈Iso(W)`;
- mostrar igualdade do agregado;
- tornar o mecanismo verificável à mão.

Marcar:

> **illustrative, post-confirmatory, not confirmatory evidence.**

Não usar o toy para sustentar “strictly realized in the system dynamics”; isso pertence à família 20.

---

# 11. Relação com prior art

Estrutura por concessões:

1. known symmetry-induced unobservability;
2. known invariance groups / quotients;
3. known lossy causal abstraction;
4. known micro-realization dependence;
5. known endogenous causal contexts;
6. known finite-horizon observability;
7. no T0 identified for the specific composition audited.

Formulação autorizada:

> **we did not identify an equivalent antecedent in our adversarial audit**

e não:

> no previous work exists.

A novelty candidate principal continua a ser a composição causal específica, não a matemática de isometrias.

---

# 12. Construct validity — obrigatório

O paper deve afirmar:

> **The study tests whether an interventional observable preserves a preregistered mechanistic distinction in a controlled synthetic domain. The System-II/System-III and STATE/SIGNAL labels are operational targets of the generative design, not a claim of universal ontology for physical or biological interactions.**

Não usar “genuinely belongs” nem “ground truth” sem a qualificação “by construction”.

---

# 13. External-validation gate

## Study G — generalization within the theorem class

Preservar as hipóteses estruturais e variar:

- tamanho do alfabeto;
- response table;
- pairwise kernel;
- determining intervention set;
- implementação.

Pré-registar:
- blindness under `τ∈Iso(W)`;
- recovery when refinements break the relevant symmetry;
- falsification criteria.

---

## Study B — boundary/falsification outside the theorem class

Quebrar deliberadamente:

- channel-independent memory update;
- XOR cancellation;
- aligned fiber;
- pure contextual relabeling.

Objetivo:

testar onde deixa de valer a estrutura de pull-back / symmetry blindness.

Estes são estudos diferentes e não devem ser misturados.

Nenhum deles reabre a Fase 6.

---

# 14. Título — direção pós-red-team

Não congelar antes do abstract.

### Recomendado

**When Receiver-State Relabeling Becomes Invisible to an Interventional Observable**

### Alternativa mecanística

**Mechanism-Dependent Symmetry Can Hide Receiver-State-Dependent Causal Modulation**

### Alternativa narrativa

**A Preregistered Counterexample Reveals a Symmetry-Induced Blind Class of an Interventional Observable**

Evitar títulos que impliquem que todo receiver-state relabeling produz aliasing.

---

# 15. Abstract — arquitetura v2.1

1. **Problem:** interventional invariance can be used to operationalize stability across contexts.
2. **Preregistered evaluation:** the conjunctive C1′ criterion was tested blindly and the confirmatory outcome was negative (`199/200`, `passa=false`); the other scored candidates also failed and are reported.
3. **Counterexample:** the C1′ failure retained a causal difference strictly realized at a causally sufficient local-state granularity.
4. **Metric mechanism:** receiver state induced contextual relabelings; when the relative relabeling was an isometry of the receiver-response geometry, the aggregate became invariant.
5. **Exact result:** for the frozen determining intervention set, `d₀=d₁ ⇔ τ∈Iso(W_M)`.
6. **Ordinal extension:** C1′ has an additional L2 route in which cardinal profiles differ but weak ranks coincide.
7. **Scope:** finer observables shrink the blind set; the blindness is observable-relative.
8. **Conclusion:** measured causal invariance can reflect representation-induced aliasing rather than absence of causal modulation, when an underlying causal difference is independently established.

P7 só entra no abstract se voltar ao corpo principal.

---

# 16. Regra editorial de linguagem

Preferir:

- `metric blind route`;
- `ordinal aliasing`;
- `observable-relative causal aliasing`;
- `symmetry-induced blindness`;
- `receiver-state-dependent relabeling`;
- `mechanism-dependent response geometry`;
- `strictly realized at the causally sufficient local-state granularity`;
- `pre-specified operational target`.

Evitar:

- `C1′ blindness is exactly τ∈Iso(W)`;
- `τ∈Iso(W) proves false invariance`;
- `causal non-identifiability` sem qualificador;
- `ground-truth causal individuation`;
- `genuinely belongs to STATE/SIGNAL`;
- `symmetry proves no causal change`;
- `horizon determines causal individuation`;
- `C1′ almost passed`.

---

# 17. Hierarquia final de resultados no paper

## Headline
H1. Preregistered negative result.  
H2. Exact metric blindness theorem.  
H3. Strictly realized causal witness in the confirmatory counterexample.  
H4. Observable-refinement dependence of the blind set.

## Supporting
S1. Ordinal L2 route / alignment theorem.  
S2. Generator-specific prevalence.

## Extended / Supplementary
E1. III-1 / III-2a / III-2b.  
E2. M3 correlation model.

---

# 18. Ordem de escrita

1. Claim–Evidence Ledger
2. Results 2.1–2.8
3. Methods / formal definitions
4. construct-validity section
5. prior-art positioning
6. Discussion
7. Limitations
8. Introduction
9. Abstract
10. Title

P7 só é reintegrado no main text se melhorar claramente a Discussion do núcleo P3/P4.

---

# 19. Freeze criteria

Esta arquitetura pode ser congelada se:

1. o diff v2→v2.1 contiver apenas correções derivadas da red-team;
2. nenhuma nova claim empírica ou matemática for introduzida;
3. nenhuma claim pós-confirmatória for promovida a confirmatória;
4. P3 permanecer decomposto em mecanismo analítico + witness realizado;
5. L1 e L2 permanecerem separados;
6. C2/C3 forem reportados sem autópsia inventada;
7. P7 permanecer secundário/extended;
8. prior art permanecer limitado ao estatuto já fechado.

---

`BOUNDARY I — PASSO 4: ARTICLE ARCHITECTURE v2.1 — CANDIDATE FOR FREEZE`

# BOUNDARY I — PASSO 3: ENCERRAMENTO DA AUDITORIA DE PRIOR ART

**POST-CONFIRMATORY / PRIOR-ART AUDIT — Pré-registo A v8.3**  
**Data de fecho:** 17-08-2026  
**Estatuto:** `PASSO 3 — PRIOR-ART AUDIT — CLOSED`

> Este documento encerra exclusivamente a auditoria bibliográfica e de prioridade conceptual iniciada após o encerramento formal da Fase 6 e após a Nota Interpretativa v2. Não reabre a Fase 6, não altera o protocolo, não altera o scoring confirmatório, não propõe C1″, não inicia BOUNDARY II e não converte resultados pós-confirmatórios em resultados confirmatórios.
>
> O resultado confirmatório permanece literalmente:
>
> `resultado_confirmatorio_A = "negativo"`  
> `C1′ = 199/200`  
> `passa = false`
>
> A autópsia pós-confirmatória explica o erro; não o apaga nem o transforma em resultado “quase positivo”.

---

## 1. Objetivo e mandato da auditoria

A auditoria foi desenhada para tentar **eliminar**, e não proteger, as candidatas a novidade fixadas em `FASE6-INTERPRETIVE-NOTE-v2.md`.

Claims auditadas:

| ID | Claim auditada | Prioridade pré-auditoria |
|---|---|---:|
| P1 | invariância sob `Iso(W)` | matemática conhecida; sem claim de novidade |
| P2 | recíproca pelo lattice determinante | baixa; T2 provável |
| P3 | `receiver-state → τ → Iso(W_M) → falsa invariância causal` | **máxima** |
| P4 | na construção estudada, a falsa invariância altera a partição ESTADO/SINAL de C1′ apesar de existir informação causal separadora realizada | **máxima** |
| P5 | teorema do alinhamento / mecanismo L2 | alta |
| P6 | III-1: nulidade estrutural exata em `h=1` | alta |
| P7 | a nulidade de III em `h=1` para o campo XOR-intervencional não é preservada sob `T∘T`; em `h=2`, `dep2>0` em 3996/4000 arestas III sob a lei estudada | **máxima** |
| P8 | `individuação observada = f(sistema, observável, horizonte)` | conceptual; não teorema |

A pergunta de fecho não é “há literatura relacionada?”, mas:

> **Existe prior art que antecipe essencialmente a mesma estrutura causal/matemática e a mesma consequência científica, de modo a tornar uma das claims P3–P7 não-original na sua formulação específica?**

---

## 2. Escala de classificação

Foi usada a seguinte escala adversarial:

### T0 — antecipação essencialmente equivalente
O trabalho anterior contém o mesmo mecanismo estrutural ou um mecanismo matematicamente isomorfo, com mapeamento direto dos objetos essenciais e a mesma conclusão substantiva. Um T0 elimina a claim de novidade.

### T1 — antecedente estrutural próximo
Partilha uma parte central do mecanismo, mas muda um objeto essencial, a direção causal, o problema de identificação, o observável, ou a consequência científica. Obriga a estreitar e citar; não elimina automaticamente a claim.

### T2 — ancestral genérico
Contém matemática, princípios ou fenómenos de base conhecidos — p.ex. invariância por simetrias, quotienting, perda de observabilidade, abstrações lossy, equivalence classes ou dependência do horizonte.

### T3 — analogia/contexto
Sem equivalência estrutural relevante para prioridade.

> **Regra de decisão:** similaridade verbal ou temática nunca foi tratada como antecipação. Para T0/T1 exigiu-se um mapeamento dos objetos do paper para os objetos da claim auditada.

---

## 3. Âmbito e método

A auditoria combinou:

1. **snowballing de rede de citações** com seeds de observabilidade, bisimulação, abstração causal e identifiabilidade;
2. pesquisa direta por literatura primária em:
   - causal abstraction;
   - causal representation learning;
   - causal aggregation / macro–micro causality;
   - endogenous/context-specific causal mechanisms;
   - nonlinear observability;
   - symmetry-induced unobservability;
   - switching/hybrid systems;
   - internal/latent-variable observability;
   - finite-horizon distinguishability;
   - equivalence classes, invariance and quotient representations;
3. inspeção adversarial dos vizinhos mais próximos, incluindo literatura de **2024–2026**;
4. buscas negativas dirigidas por termos estruturais: `symmetry`, `isometry`, `permutation/relabeling`, `internal state/context`, `lossy abstraction`, `micro-realization`, `interventional equivalence`, `finite horizon`, `composition`;
5. comparação explícita com o mecanismo fechado da Fase 6.

A auditoria **não pretende provar ausência universal de prior art**. Uma revisão de literatura não pode demonstrar logicamente que nenhum trabalho relevante existe. O standard usado foi:

> busca adversarial, multidomínio e suficientemente profunda para testar os ancestrais mais plausíveis e os vizinhos contemporâneos mais perigosos.

---

# PARTE I — RESULTADOS POR CLAIM

## 4. P1 — invariância sob `Iso(W)`

### Veredicto
**T2 / matemática conhecida. Sem claim de novidade.**

Se um funcional factoriza por uma geometria/invariante e uma transformação pertence ao grupo que preserva essa geometria, a invariância resultante pertence ao quadro clássico de ações de grupo, isometrias, estabilizadores, quocientes e invariantes.

Nada na auditoria justifica apresentar:

`τ ∈ Iso(W) ⇒ F(τ·X)=F(X)`

como novo princípio matemático geral.

### Estatuto final
**CONCEDED — known mathematics.**

---

## 5. P2 — recíproca pelo lattice determinante

### Resultado interno relevante
No instrumento congelado, as nove intervenções não medem diretamente os seis graus de liberdade independentes de `W`; sub-lattices dão posto 2 ou 4, enquanto o lattice completo tem posto 6 e determinante `−8`, permitindo recuperar indiretamente o emparelhamento não sondado.

### Veredicto
**T2 provável / aplicação específica de determining or separating sets.**

A auditoria não revelou fundamento para reivindicar como novo princípio matemático a ideia de que um conjunto de medições de posto completo determina o objeto/invariante subjacente.

O facto de o **lattice concreto de nove intervenções** possuir essa propriedade é um resultado correto e não tautológico do instrumento, mas não deve ser elevado a contribuição matemática geral.

### Estatuto final
**NO INDEPENDENT NOVELTY CLAIM.**

---

## 6. P3 — `receiver-state → τ → Iso(W_M) → falsa invariância causal`

### 6.1 Formulação exata auditada

No domínio fechado da Fase 6:

- o contexto é o **estado interno retido do receptor**, `m_B`;
- esse estado seleciona relabelings `π_m` da interface;
- o remapeamento relativo é

`τ = π_1 ∘ π_0^{-1}`;

- o próprio mecanismo receptor `M` induz uma geometria de resposta

`W_M(p,q)`;

- se `τ ∈ Iso(W_M)`, o observável que factoriza pela geometria pode ser exatamente invariante entre contextos;
- ainda assim, os campos causais ponto-a-ponto podem diferir;
- na família confirmatória 20, a diferença existe **também no suporte estritamente realizado**, com testemunhas observacionais;
- a falsa invariância contribui diretamente para a classificação errada ESTADO/SINAL.

A candidata a novidade não é nenhum destes ingredientes isoladamente. É a **composição estrutural acima**.

### 6.2 Antecedentes mais perigosos

#### Martinelli — observability invariance groups
Agostino Martinelli introduz explicitamente um **group of invariance of observability**, isto é, transformações relativamente às quais a observabilidade permanece invariante.

**O que antecipa:**  
symmetry/invariance → unobservability / indistinguishability.

**O que não foi encontrado:**  
estado interno do receptor gerando relabeling de interface; geometria `W_M` induzida pelo mecanismo receptor; condição `τ∈Iso(W_M)`; modulação causal realizada que persiste abaixo do observável; consequência ESTADO/SINAL.

**Classificação:** **T2**.

#### Mesbahi, Bu & Mesbahi — symmetry and nonlinear observability
Derivam uma relação analítica entre simetria da dinâmica e perda de observabilidade via Koopman; funções de medição que espelham simetrias podem manter o sistema não observável.

**O que antecipa:**  
symmetry of dynamics/measurements → loss of observability.

**Diferença decisiva:**  
a simetria não é produzida por um estado interno do receptor como relabeling contextual da interface, nem é definida como isometria da geometria de resposta causal do receptor.

**Classificação:** **T2**.

#### Kolar, Rams & Schöberl — symmetry groups and observability
Mostram que uma transformação de simetria pode levar soluções distintas a trajetórias iguais de input/output, provando não-observabilidade.

**Classificação:** **T2**.

#### Whalen et al. — nonlinear networks and symmetry
Usam teoria de representações de grupos para analisar como tipos de simetria afetam observabilidade e controlabilidade em redes não lineares.

**Classificação:** **T2**.

#### Günther et al. — endogenous context variables
Tratam explicitamente contextos endógenos, incluindo **estados internos**, que correspondem a alterações nos mecanismos/relacionamentos causais.

**O que antecipa:**  
internal/endogenous state → context-specific causal mechanism.

**O que falta para P3:**  
relabeling relativo da interface; simetria/isometria do response geometry; mecanismo exato de invisibilidade por agregação; condição necessária/suficiente `τ∈Iso(W_M)`; persistência da diferença causal abaixo do observável.

**Classificação:** **T1/T2**.

#### Xia & Bareinboim — causal abstraction under lossy representations
Este é o vizinho causal mais importante. O trabalho formaliza abstrações lossy em que **valores/intervenções low-level diferentes, com efeitos downstream diferentes, podem ser mapeados para o mesmo objeto high-level**, violando a Abstract Invariance Condition.

A notação deve ser cuidadosamente distinguida: o `τ` de Xia & Bareinboim é uma **função de abstração low→high definida entre representações**, não o nosso `τ=π_1∘π_0^{-1}` gerado por dois estados internos do receptor.

**O que antecipa:**  
causal information can be lost when distinct low-level causal interventions are identified by a lossy representation.

**Diferença decisiva:**  
em P3 não se começa por escolher uma abstração que funde os dois casos. O estado do receptor produz uma transformação contextual; a cegueira ocorre quando essa transformação pertence à simetria da geometria de resposta do próprio receptor.

Buscas no texto por `isometry`, `relabel` e `symmetry` não revelaram o mecanismo `context → relative relabeling → response-geometry isometry`.

**Classificação:** **T1**.

#### Zhu et al. — meaningful causal aggregation
Mostram que diferentes micro-realizações da mesma macro-intervenção podem gerar efeitos diferentes e até alterar se uma relação macro aparenta ser confundida ou não. Explicitam que relações macro podem ter de ser definidas com referência aos micro-estados.

**O que antecipa:**  
aggregation can hide or distort causally relevant microstructure; causal meaning may depend on micro-realization.

**O que não antecipa:**  
a cadeia específica estado do receptor → relabeling → isometria de `W_M` → invariância exata do observável com dependência realizada persistente.

**Classificação:** **T1** para P4; **T1/T2** como vizinho de P3.

#### von Kügelgen et al.; Li, Kaba & Ravanbakhsh
Ambos formalizam limites de identifiabilidade em causal representation learning / causal abstraction.

- von Kügelgen et al.: identificação de variáveis latentes e causal graph apenas até ambiguidades irresolúveis por dados intervencionais;
- Li et al.: grau de identificação de um modelo causal, dado um conjunto de intervenções, até uma abstração de maior granularidade.

**Classificação:** **T2** para P3.

#### Literatura 2026
`Coarsening Causal DAG Models` (Madaleno, Misra & Markham, 2026) acrescenta novos resultados de identifiabilidade de causal graphs abstratos a partir de dados intervencionais.  
`Contrastive representations of structured treatments` (Corcoll et al., 2026) formaliza representações que devem colapsar tratamentos interventionally equivalent relativamente ao outcome.

Ambos reforçam que **equivalence under causal representation/coarsening é terreno ocupado**. Nenhum deles, na inspeção realizada, contém a composição específica de P3.

### 6.3 Mapeamento adversarial

| Elemento P3 | Prior art forte? | Encontrado equivalente conjunto? |
|---|---:|---:|
| estado interno/endógeno altera mecanismo causal | sim — Günther et al. | não |
| simetria pode destruir observabilidade | sim — Martinelli, Mesbahi, Kolar, Whalen | não |
| abstração lossy pode fundir efeitos causais diferentes | sim — Xia & Bareinboim | não |
| agregação pode ocultar micro-realizações causalmente diferentes | sim — Zhu et al. | não |
| ambiguidades / equivalence classes em CRL | sim — von Kügelgen et al., Li et al. | não |
| **estado interno do receptor gera `π_m`** | não encontrado como mecanismo relevante | — |
| **`τ=π_1π_0^{-1}` testado contra `Iso(W_M)`** | não encontrado | — |
| **`W_M` depende do mecanismo receptor concreto** | não encontrado em combinação equivalente | — |
| **invariância exata apesar de diferença causal ponto-a-ponto e realizada** | conceitos parciais existem | não na construção conjunta |
| **efeito direto na partição ESTADO/SINAL de C1′** | não encontrado | não |

### Veredicto P3
**NENHUM T0 ENCONTRADO.**

A literatura ocupa todos os ingredientes genéricos. A candidata a novidade sobrevive **apenas** na composição causal específica:

> **contexto interno do receptor → relabeling contextual da interface → simetria da geometria de resposta induzida pelo próprio receptor → invariância exata do observável apesar de modulação causal ponto-a-ponto e estritamente realizada.**

### Estatuto final
**PRIMARY NOVELTY CANDIDATE — SURVIVES PRIOR-ART AUDIT.**

Isto não autoriza “first ever”, “proved novel” ou qualquer declaração de prioridade histórica absoluta.

---

## 7. P4 — consequência para individuação ESTADO/SINAL

### Facto fechado
Na família 20:

- o sistema é II;
- existem módulos causalmente distintos;
- existe dependência causal real e estritamente realizada;
- C1′ marca as duas arestas relevantes como ESTADO;
- o núcleo II é fundido na partição correspondente a III.

### Prior art
Zhu et al., Xia & Bareinboim e a literatura de causal abstraction mostram que uma agregação/representação pode eliminar informação causalmente relevante ou tornar ambígua a interpretação macro.

Portanto, não é novo afirmar genericamente:

- “a agregação pode perder causalidade”;
- “a estrutura causal aparente depende da granularidade”;
- “micro-estados diferentes podem ser fundidos num macro-estado”.

### O que sobrevive
O caso específico:

> **a falsa invariância caracterizada em P3 altera a partição ESTADO/SINAL produzida por C1′ apesar de a dinâmica realizada conter informação causal separadora.**

### Veredicto P4
- **Princípio geral:** T1/T2 — **CONCEDED**.
- **Consequência específica de P3 na construção estudada:** nenhum T0 encontrado.

### Estatuto final
**SPECIFIC CONSEQUENCE OF P3 — NOT AN INDEPENDENT GENERAL NOVELTY CLAIM.**

A interpretação mais ampla

`individuação observada = f(sistema, observável)`

permanece **interpretação conceptual**, não teorema universal.

---

## 8. P5 — alinhamento / L2

### Resultado auditado
Na ação

`ψ : S4 → S3`

sobre as três emparelhações perfeitas, com kernel `V4`, se `ψ(τ)` fixa o emparelhamento não sondado `λ`, então L2 é impossível; qualquer colapso nessa célula é L1.

Na construção, L2 ocorre apenas em células desalinhadas e corresponde a transporte da soma do emparelhamento cego para uma posição sondada preservando a ordem fraca, apesar de alterar valores cardinais.

### Prior art
São clássicos:

- a ação de `S4` nos três perfect matchings;
- o quotient `S4/V4 ≅ S3`;
- invariância/equivariância sob ações de grupo;
- weak orders / ordinal profiles.

A auditoria **não encontrou** um antecedente que combine essa ação com:

1. o emparelhamento não sondado do instrumento;
2. o transporte do valor cego para uma posição medida;
3. a preservação de weak rank;
4. a conclusão `aligned ⇒ L2 impossible`.

### Veredicto P5
**Nenhum T0 encontrado**, mas a matemática-base é T2.

### Estatuto final
**TECHNICAL NOVELTY CANDIDATE / SECONDARY LEMMA.**

Não deve ser apresentado como “nova matemática de `S4`, `S3` ou `V4`”.

---

## 9. P6 — III-1

### Resultado
No campo XOR-intervencional congelado a horizonte exatamente 1, a dependência de memória de III cancela analiticamente:

`dep = 0`

estruturalmente para o contraste considerado.

### Veredicto
O mecanismo abstrato “um termo comum cancela numa diferença/XOR” é elementar. A auditoria não dá base para uma claim matemática geral.

O que é legítimo é:

> **proposição analítica específica do Sistema III e do campo intervencional estudado.**

### Estatuto final
**SYSTEM-SPECIFIC ANALYTIC RESULT — NO INDEPENDENT PRIORITY CLAIM.**

A sua importância científica vem sobretudo da ligação a P7.

---

## 10. P7 — `h=1` exato vs `T²`

### 10.1 O que a literatura já ocupa

A literatura de observabilidade de sistemas híbridos/switching contém há décadas dependência explícita da distinguibilidade relativamente ao horizonte.

- Baglietto, Battistelli & Scardovi (2007) tratam **mode observability in a finite-horizon setting**, reconstruindo sequências de modos a partir de observações e controlos.
- Collins & van Schuppen (2004) distinguem condições de observabilidade em tempo infinitesimal e após um evento discreto.
- De Santis, Di Benedetto & Pola (2006/2008) tratam reconstrução de estados híbridos e variáveis internas ao longo da evolução input/output.

Consequentemente, não são novas as proposições genéricas:

- “algo pode ser indistinguível num horizonte curto e distinguível num horizonte maior”;
- “a observabilidade depende do tempo/história”;
- “internal variables can become reconstructible from sequences of observations”.

### 10.2 Claim estreita que foi realmente auditada

Em III:

1. a `h=1`, o termo de memória relevante cancela **identicamente** no campo XOR-intervencional;
2. ao compor a transição, o mecanismo de primeira ordem não itera;
3. em `T²`, a memória reaparece **dentro dos índices/seletores internos** que determinam a segunda resposta;
4. empiricamente, na lei estudada:

`dep2 > 0` em `3996/4000 = 99,90%` das arestas III;

5. há `4/4000` exceções — portanto não existe claim universal de dependência em `h=2`.

### 10.3 Resultado da pesquisa
A auditoria encontrou muitos T2 para “horizon matters”, mas **não encontrou T0** para:

> cancelamento algébrico exato do mesmo campo causal a `h=1` que deixa de valer sob composição porque a variável cancelada passa a parametrizar índices internos na segunda transição.

### Veredicto P7
- **horizon-dependent distinguishability:** T2 — conhecido.
- **mecanismo III-1 → III-2 específico:** nenhum T0 encontrado.

### Estatuto final
**NARROW TECHNICAL NOVELTY CANDIDATE.**

Afirmações proibidas continuam:

- “nenhuma extensão temporal pode funcionar”;
- “III é sempre dependente em h=2”;
- “provámos uma impossibilidade universal de individuação temporal”.

---

## 11. P8 — `individuação observada = f(sistema, observável, horizonte)`

### Veredicto
A literatura de causal abstraction, aggregation e observability já dá ampla ancestralidade à ideia de que informação inferível depende da representação/observável e da janela de observação.

A expressão continua útil como síntese do programa, mas não é teorema nem claim prioritária.

### Estatuto final
**CONCEPTUAL HYPOTHESIS / PROGRAMMATIC INTERPRETATION ONLY.**

---

# PARTE II — MATRIZ FINAL DE PRIORIDADE

## 12. Veredicto consolidado

| Claim | Resultado da auditoria | Estatuto autorizado após Passo 3 |
|---|---|---|
| P1 | T2 claro | matemática conhecida |
| P2 | T2 provável | aplicação específica; sem novelty claim |
| **P3** | **nenhum T0; T1/T2 fortes em todos os ingredientes genéricos** | **principal novelty candidate** |
| P4 | claim geral T1/T2; caso específico sem T0 | consequência específica de P3 |
| P5 | matemática-base T2; mecanismo instrumental específico sem T0 | secondary technical novelty candidate |
| P6 | mecanismo-base elementar | resultado analítico específico, não headline |
| **P7** | horizonte genérico T2; mecanismo h1→h2 específico sem T0 | **narrow technical novelty candidate** |
| P8 | ancestralidade conceptual ampla | interpretação/hipótese, não theorem |

---

# PARTE III — CONCESSÕES OBRIGATÓRIAS

## 13. O que o futuro artigo DEVE conceder explicitamente

Não são contribuições novas deste projeto:

1. invariância de funcionais sob grupos de simetria/isometrias;
2. quocientes, estabilizadores, maximal/separating invariants e determining sets;
3. symmetry-induced unobservability;
4. existência de grupos de transformações sob os quais observabilidade é invariante;
5. causal abstractions e representações lossy;
6. possibilidade de intervenções low-level causalmente diferentes colapsarem na mesma representação high-level;
7. dependência de causalidade macro relativamente a micro-realizações;
8. contextos endógenos/internos que alteram mecanismos causais;
9. identificabilidade causal apenas até classes de equivalência/abstrações;
10. dependência genérica da distinguibilidade/observabilidade relativamente ao horizonte;
11. a matemática clássica da ação `S4 → S3` e `V4`;
12. o facto abstrato de que um termo comum pode cancelar numa diferença/XOR.

---

## 14. Claims proibidas após a auditoria

Continuam proibidas:

- “novo teorema geral de invariância causal”;
- “nova matemática de isometrias”;
- “descobrimos que simetria causa não-observabilidade”;
- “descobrimos que abstrações lossy podem perder causalidade”;
- “descobrimos que o horizonte importa”;
- “C1′ validado”;
- “C1′ quase passou”;
- “resultado confirmatório essencialmente positivo”;
- “0,46% é universal”;
- “nenhuma extensão temporal pode funcionar”;
- “a individuação causal depende necessariamente do observável”;
- “resolvemos o problema das fronteiras causais”;
- “somos os primeiros” / “first ever” sem auditoria bibliográfica externa adicional;
- qualquer claim sobre consciência.

---

# PARTE IV — FORMULAÇÕES AUTORIZADAS

## 15. Novelty candidate principal — P3

### Formulação recomendada

> **No domínio estudado, o estado interno do receptor induz relabelings contextuais de uma interface finita. Demonstramos uma classe específica de falsa invariância causal: quando o relabeling relativo entre contextos é uma isometria da geometria de resposta induzida pelo próprio mecanismo receptor, um observável intervencional que factoriza por essa geometria pode tornar-se exatamente invariante apesar de existir modulação causal ponto-a-ponto e estritamente realizada. Na instância confirmatória falhada, essa invisibilidade faz C1′ fundir uma partição ESTADO/SINAL que a dinâmica realizada contém informação suficiente para separar.**

### Estatuto epistemológico

`NOVELTY CANDIDATE — SURVIVED ADVERSARIAL PRIOR-ART AUDIT`

Não escrever:

`PROVED NOVEL`

nem:

`FIRST DISCOVERY`.

---

## 16. Formulação técnica secundária — P7

> **Para o Sistema III e o campo XOR-intervencional estudado, a dependência do estado de memória cancela exatamente a horizonte 1. Esta identidade não é preservada pela composição direta da transição: em T², a dependência de memória reaparece nos índices internos usados para determinar a resposta subsequente; sob a lei estudada, 3996/4000 arestas III exibiram dep2>0.**

Estatuto:

`NARROW TECHNICAL NOVELTY CANDIDATE`

Não generalizar para qualquer sistema, qualquer funcional ou qualquer horizonte.

---

## 17. Formulação técnica secundária — P5

> **No instrumento estudado, a ação do remapeamento sobre as três emparelhações perfeitas determina uma condição de alinhamento: se a ação fixa o emparelhamento não sondado, um colapso ordinal L2 é impossível e qualquer colapso pertence a L1; L2 requer desalinhamento capaz de transportar a soma do emparelhamento cego para uma posição sondada sem alterar a ordem fraca.**

Estatuto:

`SECONDARY TECHNICAL NOVELTY CANDIDATE`

---

# PARTE V — VIZINHOS BIBLIOGRÁFICOS QUE DEVEM SER CITADOS

## 18. Núcleo mínimo de referências de posicionamento

### Symmetry / observability

**Whalen, A. J., Brennan, S. N., Sauer, T. D., & Schiff, S. J. (2015).**  
*Observability and Controllability of Nonlinear Networks: The Role of Symmetry.*  
Physical Review X, 5, 011005.  
DOI: `10.1103/PhysRevX.5.011005`

**Martinelli, A. (2018; versão analítica atualizada posteriormente).**  
*Nonlinear Unknown Input Observability: The General Analytic Solution.*  
IEEE Transactions on Automatic Control.  
DOI relacionado: `10.1109/TAC.2018.2798806`  
Versão posterior/ampliada: *Nonlinear unknown input observability and unknown input reconstruction: The general analytical solution* (2022).

**Kolar, B., Rams, H., & Schöberl, M. (2018).**  
*Application of Symmetry Groups to the Observability Analysis of Partial Differential Equations.*  
arXiv:1804.01717.

**Mesbahi, A., Bu, J., & Mesbahi, M. (2020).**  
*Nonlinear Observability via Koopman Analysis: Characterizing the Role of Symmetry.*  
Automatica. Preprint: arXiv:1904.08449.

### Causal aggregation / abstraction

**Zhu, Y., Budhathoki, K., Kübler, J. M., & Janzing, D. (2024).**  
*Meaningful Causal Aggregation and Paradoxical Confounding.*  
Proceedings of CLeaR, PMLR 236:1192–1217.

**Xia, K. M., & Bareinboim, E. (2025).**  
*Causal Abstraction Inference under Lossy Representations.*  
ICML 2025, PMLR 267:68225–68235.  
arXiv:2509.21607.

**Li, X., Kaba, S.-O., & Ravanbakhsh, S. (2025).**  
*On the Identifiability of Causal Abstractions.*  
AISTATS 2025, PMLR 258:3241–3249.  
arXiv:2503.10834.

**Madaleno, F., Misra, P., & Markham, A. (2026).**  
*Coarsening Causal DAG Models.*  
CLeaR 2026, PMLR 323:1318–1344.

### Endogenous context / causal representation

**Günther, W., Popescu, O.-I., Rabel, M., Ninad, U., Gerhardus, A., & Runge, J. (2024).**  
*Causal discovery with endogenous context variables.*  
NeurIPS 2024. arXiv:2412.04981.

**von Kügelgen, J., Besserve, M., Wendong, L., Gresele, L., Kekić, A., Bareinboim, E., Blei, D. M., & Schölkopf, B. (2023).**  
*Nonparametric Identifiability of Causal Representations from Unknown Interventions.*  
NeurIPS 2023. DOI: `10.52202/075280-2110`.

### Horizon / hybrid observability

**Collins, P. J., & van Schuppen, J. H. (2004).**  
*Observability of Piecewise-Affine Hybrid Systems.*  
HSCC 2004, LNCS, pp. 265–279.  
DOI: `10.1007/978-3-540-24743-2_18`.

**De Santis, E., Di Benedetto, M. D., & Pola, G. (2006).**  
*Observability of Internal Variables in Interconnected Switching Systems.*  
IEEE CDC 2006.  
DOI: `10.1109/CDC.2006.377554`.

**Baglietto, M., Battistelli, G., & Scardovi, L. (2007).**  
*Active mode observability of switching linear systems.*  
Automatica, 43(8), 1442–1449.  
DOI: `10.1016/j.automatica.2007.01.006`.

**De Santis, E., Di Benedetto, M. D., & Pola, G. (2008).**  
*Observability and Detectability of Linear Switching Systems: A Structural Approach.*  
arXiv:0802.4045.

---

# PARTE VI — LIMITAÇÕES DA AUDITORIA

## 19. Limites epistemológicos

O fecho deste Passo 3 significa:

> **não foi encontrado, após busca adversarial multidomínio, um antecedente T0 para a composição específica de P3, nem para os mecanismos técnicos estreitos P5/P7.**

Não significa:

> **foi provado que nenhum antecedente existe.**

Limitações inevitáveis:

1. indexação bibliográfica incompleta;
2. papers não indexados, teses, livros ou literatura com terminologia muito distante podem ter sido omitidos;
3. ausência de correspondência textual não prova ausência de isomorfismo matemático oculto;
4. algumas fontes históricas foram avaliadas por abstract/full text disponível publicamente, não por reprodução matemática integral;
5. a auditoria foi conduzida dentro do mesmo programa de investigação — não substitui revisão por pares ou uma revisão bibliográfica independente por especialista externo.

---

## 20. Critérios de reabertura

O Passo 3 só deve ser reaberto se ocorrer pelo menos uma destas condições:

1. for localizado um paper anterior que proponha explicitamente uma estrutura equivalente a:

   `internal receiver context → relative interface relabeling → symmetry/isometry of receiver response geometry → exact observational/interventional invariance despite underlying causal difference`;

2. for localizado um resultado matemático anterior que torne P5 ou P7 um corolário direto já formulado no mesmo domínio substantivo;
3. um revisor ou especialista indicar literatura plausivelmente T0;
4. a formulação da claim de novidade for materialmente ampliada para além das fronteiras fixadas neste documento.

Nova literatura T2/T3, por si só, **não reabre** a auditoria: deve apenas ser incorporada na genealogia bibliográfica do artigo.

---

# PARTE VII — DECISÃO FORMAL

## 21. Estado final autorizado

```text
P1 = KNOWN_MATHEMATICS
P2 = SPECIFIC_APPLICATION_NO_INDEPENDENT_NOVELTY
P3 = PRIMARY_NOVELTY_CANDIDATE_SURVIVES_AUDIT
P4 = SPECIFIC_CONSEQUENCE_OF_P3_GENERAL_PRINCIPLE_CONCEDED
P5 = SECONDARY_TECHNICAL_NOVELTY_CANDIDATE
P6 = SYSTEM_SPECIFIC_ANALYTIC_RESULT
P7 = NARROW_TECHNICAL_NOVELTY_CANDIDATE
P8 = CONCEPTUAL_HYPOTHESIS_ONLY

T0_FOUND_FOR_P3 = false
T0_FOUND_FOR_P5 = false
T0_FOUND_FOR_P7_NARROW = false
```

### Interpretação correta de `T0_FOUND = false`

`false` significa:

> **nenhum antecedente essencialmente equivalente foi encontrado na auditoria realizada.**

Não significa:

> **foi demonstrado que nenhum antecedente existe.**

---

## 22. Relação com o resultado confirmatório

Nada neste documento modifica:

```text
resultado_confirmatorio_A = "negativo"
C1′ = 199/200
passa = false
```

A principal candidata a novidade surgiu da **explicação pós-confirmatória da falha**, não da aprovação do critério pré-registado.

Portanto:

- a falha de C1′ permanece uma falha;
- a descoberta pós-confirmatória pode ser cientificamente valiosa independentemente do resultado confirmatório negativo;
- qualquer artigo deve separar claramente:
  1. resultado confirmatório;
  2. autópsia pós-confirmatória;
  3. teoremas/resultados analíticos posteriores;
  4. posicionamento de novidade após prior-art audit.

---

## 23. Declaração de encerramento

> A auditoria de prior art procurou ativamente antecedentes capazes de eliminar as claims candidatas e identificou ancestrais fortes para praticamente todos os seus ingredientes genéricos. Em consequência, várias formulações amplas foram explicitamente concedidas à literatura existente. Contudo, não foi encontrado antecedente T0 para a composição causal específica em P3, nem para as formulações técnicas estreitas de P5 e P7. P3 é, por isso, mantida como a principal **novelty candidate**, com P5 e P7 como candidatos técnicos secundários, sempre dentro dos domínios e restrições explicitados neste documento.

```text
BOUNDARY I — PASSO 3
PRIOR-ART AUDIT — CLOSED
```

**Qualquer claim futura de prioridade deve citar este encerramento e respeitar as concessões e proibições aqui fixadas.**

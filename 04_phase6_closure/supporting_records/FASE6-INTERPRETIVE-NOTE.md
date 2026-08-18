# BOUNDARY I — PASSO 2: NOTA INTERPRETATIVA PÓS-ENCERRAMENTO DA FASE 6
**POST-CONFIRMATORY / INTERPRETIVE — Pré-registo A v8.3**

> Fontes autorizadas: `FASE6-FORMAL-CLOSURE.md` (sha256 `8ca9f960…49ca`,
> fonte canónica do estado fechado); `FASE6-MULTIAGENT-SYNTHESIS.md`
> (sha256 `bd8b19e5…e185`); WS1–WS5 e autópsia apenas para conferência de
> formulações; a leitura independente externa ao workflow, apenas como
> crítica/avaliação. Este documento NÃO reabre a Fase 6, NÃO altera nenhum
> artefacto, NÃO recalcula, NÃO executa código, NÃO consome sementes, NÃO faz
> pesquisa bibliográfica, NÃO propõe C1″, NÃO inicia o BOUNDARY II e NÃO
> escreve o artigo. Função exclusiva: **fixar a interpretação epistemológica
> autorizada dos resultados antes da auditoria final de prior art.**

---

## 1. Estatuto documental

> A Fase 6 está formalmente **CLOSED**. Esta nota não pertence à Fase 6
> experimental; é uma decisão interpretativa posterior baseada exclusivamente
> nos resultados fechados.

```text
resultado_confirmatorio_A = "negativo"
```

- C1′ = **199/200**;
- `passa = false`;
- **nenhuma conclusão desta nota modifica esse resultado.**

---

## 2. O que NÃO deve ser apresentado como novidade principal

### 2.1 Direção 1 — τ ∈ Iso(W) ⟹ d₀ = d₁

> Dada a factorização pelo campo de pesos W, esta direção é um caso de
> matemática clássica de invariância sob ação de grupo/isometrias.

Portanto: **correta**; **importante para o mecanismo**; **NÃO deve ser
apresentada como novo princípio matemático geral**; qualquer novidade deve
estar na construção causal concreta, não no facto abstrato de invariância.

### 2.2 Direção 2 — d₀ = d₁ ⟹ τ ∈ Iso(W)

Registo dos factos fechados:

- não é tautológica no lattice congelado;
- as nove intervenções não observam diretamente todos os seis graus de
  liberdade de W;
- lattice parcial dá **posto 2** (só bits isolados) ou **posto 4**
  (só `do(c=γ)`);
- lattice completo dá **posto 6, determinante −8**;
- o emparelhamento não sondado é recuperado **indiretamente**.

> A leitura interpretativa atual é que isto constitui uma aplicação específica
> da noção conhecida de conjunto determinante / separação de invariantes,
> salvo se a auditoria de prior art demonstrar algo diferente.

Classificação provisória para a futura auditoria:
**T2 provável — matemática conhecida aplicada à construção específica.**
**Não apresentar o determinante −8 como "grande novo teorema".**

---

## 3. Onde pode residir a novidade científica

### 3.1 Construção causal específica (alvo principal da auditoria)

O resultado interessante não é simplesmente "isometrias produzem invariância".
É a cadeia:

    estado interno do receptor → π_m → τ = π₁∘π₀⁻¹ → Iso(W_M)
    → invisibilidade de modulação causal real

onde:

- τ é produzido pelo **contexto interno do receptor**;
- W_M é uma geometria de resposta induzida pelo **próprio mecanismo M**;
- o grupo de invisibilidade depende, portanto, do **receptor concreto**;
- a modulação causal pode existir **ponto-a-ponto e no suporte realizado**
  (família 20: 4608 sítios/aresta; 9 sítios estritos/aresta; testemunhas
  observacionais sem cirurgia);
- apesar disso, o observável agregado declara invariância.

Esta cadeia é tratada como a **principal candidata a contribuição causal
original — pending prior-art audit.**

---

## 4. Formulação interpretativa da falsa invariância

Formulação conservadora autorizada:

> Um observável causal pode produzir falsa invariância não porque a modulação
> causal esteja ausente, mas porque o observável identifica estados/contextos
> apenas até ao quociente induzido pelas simetrias da geometria de resposta
> que conserva.

Para o domínio estudado:

    X₀ ≠ X₁   mas   F(X₀) = F(X₁)

quando o remapeamento relativo pertence ao grupo de invisibilidade do
observável.

> A ideia abstrata "observação + simetria → não-identificabilidade" não é
> reivindicada como nova. A questão de novidade é a sua instanciação causal
> específica e a consequência para individuação.

---

## 5. III-1 e III-2 — interpretação corrigida

### 5.1 Teorema III-1

> No instrumento congelado e a horizonte exatamente 1, III possui
> **especificidade estrutural**: a memória cancela exatamente no campo
> XOR-intervencional utilizado.

Não é um resultado meramente estatístico — é uma propriedade analítica do
passo III (0/4000 arestas; 0/500 na verificação do coordenador).

### 5.2 Teorema III-2

> A invariância de III a primeira ordem **não é estável sob composição
> temporal.**

A horizonte 2: **3996/4000 arestas III (99,90%)** apresentam dependência de
memória; o mesmo tipo de observável deixa de possuir a nulidade estrutural de
h=1.

Designações preferidas:
**não-estabilidade temporal da invariância de III** ·
**obstrução a extensões diretas por aumento de horizonte**.

### 5.3 Afirmações proibidas

- NÃO escrever: "nenhuma extensão de C1′ por horizonte pode funcionar."
- NÃO escrever: "provámos uma impossibilidade universal de individuação
  temporal."

O que está demonstrado é apenas:

> aplicar diretamente o mesmo tipo de contraste a T² destrói a especificidade
> estrutural existente em T.

Permanece logicamente possível que outro funcional utilize conjuntamente a
estrutura através de vários horizontes.

---

## 6. Consequência conceptual emergente

*(TEOREMA e INTERPRETAÇÃO rigorosamente separados.)*

Formulação de programa autorizada:

    ┌─────────────────────────────────────────────────────────────┐
    │  individuação observada = f(sistema, observável, horizonte)  │
    └─────────────────────────────────────────────────────────────┘

Interpretação:

> Os resultados mostram que, para C1′, a fronteira causal inferida não é
> exclusivamente uma propriedade do sistema causal subjacente. Ela depende da
> informação preservada pelo observável; III-2 mostra ainda que a
> acessibilidade dessa informação pode depender do horizonte temporal.

**INTERPRETAÇÃO / HIPÓTESE DE PROGRAMA — NÃO TEOREMA UNIVERSAL.**

Não se afirma ainda: *"não existe individuação causal independente do
observável/horizonte"* — essa seria uma hipótese futura mais forte.

---

## 7. Família 20 — interpretação correta

**Aresta C_BA→A:** Iso(W) = **S₄** — degenerescência máxima da geometria
agregada: **qualquer** τ é invisível nesse nível.

**Aresta C_AB→B:** Iso(W) = **{id, (23)}** — e o remapeamento realizado
coincide exatamente com a **única** isometria não trivial.

Interpretação fixada:

> A família 20 é a combinação de uma aresta **estruturalmente cega** para
> qualquer remapeamento e uma segunda aresta **contingentemente cega** para o
> remapeamento efetivamente sorteado.

**Não se chama a isto "não erro de C1′". C1′ errou formalmente e o resultado
confirmatório continua negativo.**

---

## 8. Interpretação correta da prevalência de 0,46%

    46/10000 ≈ 0,46%

Registada como:

> prevalência exploratória de falha completa de identificabilidade sob a
> **lei específica do gerador congelado**.

**NÃO** interpretar como: taxa universal de falha causal; prevalência natural;
propriedade de todos os sistemas; probabilidade universal de simetria.

A taxa depende de: alfabeto de quatro símbolos; distribuição de (F₀, G₀, π);
critérios de elegibilidade; desenho concreto do gerador.

---

## 9. Lição metodológica para futuros pré-registos

*(Incorpora a crítica válida da leitura independente, sem reinterpretar o
passado.)*

Regra futura de desenho:

> Antes de fixar uma regra confirmatória de totalidade para um observável
> candidato, caracterizar explicitamente o seu grupo/classe de invisibilidade
> e estimar a medida de configurações não-identificáveis sob a lei do gerador.

Simbolicamente:

    G_blind(F) = { g : F(gX) = F(X) }

— **princípio metodológico futuro, não novo critério C1″.**

A Fase A não tinha quantificado previamente este risco de colisão.

Formulação correta (a proibida seria "o confirmatório falhou sem erro de
C1′"):

> O critério falhou numa instância que pertence a uma classe de
> não-identificabilidade intrínseca do próprio observável; essa classe e a sua
> medida não tinham sido caracterizadas antes do confirmatório.

---

## 10. O que fica fora da claim científica

### Matemática conhecida / ancestral
invariância por grupos/isometrias; quocientes; maximal/separating invariants;
determining sets; álgebra linear do posto; S₄→S₃, V₄, quando aplicável.

### Resultado específico do instrumento
forma fechada de d; estrutura concreta das nove intervenções; det −8;
taxonomia L1/L2; prevalências do gerador.

### Candidatos reais a novidade (pending prior art)
1. contexto interno do receptor gerando τ cuja compatibilidade com Iso(W_M)
   torna modulação causal real invisível;
2. consequência dessa falsa invariância para a individuação causal
   ESTADO/SINAL;
3. caracterização L2/alinhamento, se não houver antecedente equivalente;
4. estrutura III-1/III-2 — cancelamento exato de primeira ordem e
   reaparecimento sob composição temporal — se não houver antecedente
   equivalente;
5. eventual interpretação integrada sistema–observável–horizonte.

---

## 11. Claims que a auditoria de prior art deve testar

| ID | Claim candidata | Estatuto antes do prior art | Prioridade |
|----|-----------------|-----------------------------|------------|
| P1 | invariância sob Iso(W) | matemática conhecida | não procurar como novidade |
| P2 | recíproca pelo lattice determinante | T2 provável | baixa |
| P3 | receptor-state → τ → Iso(W_M) → falsa invariância causal | novidade pendente | **máxima** |
| P4 | falsa invariância altera individuação causal | novidade pendente | **máxima** |
| P5 | teorema do alinhamento/L2 | novidade pendente | alta |
| P6 | III-1: nulidade estrutural em h=1 | novidade pendente | alta |
| P7 | III-2: nulidade não estável em h=2 | novidade pendente | **máxima** |
| P8 | individuação observada = f(sistema, observável, horizonte) | interpretação; não teorema | conceptual |

Finalidade: tornar o **passo 3** (auditoria de prior art) executável sem
ambiguidade.

---

## 12. Claims proibidas antes da auditoria

- "novo teorema geral de invariância causal";
- "nova matemática de isometrias";
- "C1′ validado";
- "C1′ quase passou";
- "resultado confirmatório essencialmente positivo";
- "0,46% é uma constante/universal";
- "nenhuma extensão temporal pode funcionar";
- "individuação causal depende necessariamente do observável";
- "resolvemos o problema das fronteiras causais";
- qualquer claim sobre consciência.

---

## 13. Veredicto interpretativo final

> **INTERPRETIVE VERDICT**
>
> A Fase 6 não revelou uma nova matemática geral de invariância. Revelou, no
> domínio estudado, uma limitação causal precisa: um remapeamento produzido
> pelo estado interno do receptor pode ser causalmente real e realizado, mas
> tornar-se invisível quando coincide com uma simetria da geometria de
> resposta preservada pelo observável. Essa invisibilidade pode alterar a
> individuação produzida pelo critério. Separadamente, a especificidade
> estrutural de III demonstrada em primeira ordem não é estável sob
> composição temporal. A novidade científica destas construções específicas
> permanece dependente da auditoria final de prior art.
>
> O resultado confirmatório permanece **NEGATIVO**.
>
> A Fase 6 permanece **CLOSED**.
>
> **Nenhuma C1″ é proposta.**

---

*Nota compilada exclusivamente a partir dos artefactos fechados
(`FASE6-FORMAL-CLOSURE.md`, `FASE6-MULTIAGENT-SYNTHESIS.md`, relatórios
WS1–WS5 para conferência) e da leitura independente externa como
crítica/avaliação. Nenhuma computação nova, nenhuma semente consumida,
nenhum artefacto anterior alterado. O passo 3 (prior art) só começa após
revisão humana desta nota.*

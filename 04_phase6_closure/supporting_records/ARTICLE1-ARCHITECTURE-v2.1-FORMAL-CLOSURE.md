# BOUNDARY I — PASSO 4-R2: VALIDAÇÃO DA v2.1 E FREEZE DA ARQUITETURA

**Data:** 17-08-2026  
**Objeto validado:** `ARTICLE1-SCIENTIFIC-ARCHITECTURE-v2.1.md`  
**SHA-256:** `8a426b6600516a0257caaffdaffd45c5484d185940ede9f64ee7b8693880cf69`  
**Diff auditado:** `ARTICLE1-SCIENTIFIC-ARCHITECTURE-v2-to-v2.1.diff`  
**SHA-256 do diff:** `e86dfd211a261c20c35fc3c035fb1502560d506226d01a4c9101fdf5c311ce0e`

---

## 1. Veredicto

**PASS.**

A v2.1 incorpora as correções mandatórias da red-team sem alterar:

- o resultado confirmatório;
- o protocolo;
- o scoring;
- a distinção confirmatório/pós-confirmatório;
- o estatuto da auditoria de prior art;
- os domínios formais já estabelecidos.

Nenhuma nova claim empírica foi introduzida.

Os novos rótulos `Lemma 1`, `Proposition 1`, `Theorem 1` e `Proposition 2` reorganizam resultados já existentes; não criam conteúdo científico novo.

---

## 2. Checklist das correções mandatórias

### RT-1 — L1 ≠ toda a cegueira de C1′
**PASS.**

A v2.1 separa:
- L1 = igualdade métrica exata;
- L2 = igualdade ordinal com diferença cardinal;
- STATE = L1 ∪ L2.

A condição `τ∈Iso(W_M)` é apresentada apenas como caracterização exata de L1.

### RT-2 — blindness ≠ false invariance
**PASS.**

A v2.1 distingue:
- blindness: `F(X₀)=F(X₁)`;
- causal aliasing: blindness + `X₀≠X₁`;
- strictly realized aliasing: diferença adicional no suporte causal comparável realizado.

### RT-3 — granularidade de realização
**PASS.**

“Strictly realized” é explicitamente restringido à granularidade causalmente suficiente `(r,c)`.

### RT-4 — C2/C3
**PASS.**

C2 e C3 entram no relato confirmatório:
- C2 = 74 erros;
- C3 = 75 erros.

A arquitetura não inventa autópsia para estes critérios.

### RT-5 — P3 não recebe estatuto unitário A
**PASS.**

A claim foi decomposta em:
- estrutura pull-back / invariância / L1: analítico;
- diferença causal da família 20: demonstrada pós-confirmatoriamente;
- realização estrita: analítica + verificação;
- prevalência: exploratória.

### RT-6 — validade de constructo
**PASS.**

Foram removidas formulações ontológicas como `genuinely belonged`; os targets são explicitamente `by construction` / operacionais.

---

## 3. Melhorias adicionais da red-team

- teorema abstrato separado do lema de realização no gerador: **PASS**;
- blind-set hierarchy com nomes + denominador 20 000: **PASS**;
- prevalência apresentada como generator-specific e com range entre amostras: **PASS**;
- Figure 1 mostra por que `199/200` é NEGATIVE: **PASS**;
- future validation dividida em Study G vs Study B: **PASS**;
- P7 removido da headline e colocado como Extended/Supplementary por defeito: **PASS**;
- L2 permanece no main text: **PASS**.

---

## 4. Claims que permanecem explicitamente NÃO autorizadas

A arquitetura congelada não autoriza:

- `C1′ almost passed`;
- `C1′ validated`;
- `τ∈Iso(W)` caracteriza toda a decisão STATE;
- `τ∈Iso(W)` implica necessariamente diferença causal;
- causal non-identifiability universal;
- STATE/SIGNAL como ontologia universal;
- `0.46%` como prevalência universal;
- `3996/4000` como teorema;
- impossibilidade universal de extensão temporal;
- nova matemática geral de isometrias;
- prioridade histórica absoluta;
- qualquer claim sobre consciência.

---

## 5. Elementos congelados

A partir deste freeze, não alterar sem reabertura explícita da arquitetura:

1. resultado confirmatório = NEGATIVE;
2. C1′ L1/L2 separados;
3. `τ∈Iso(W_M)` = caracterização exata da rota L1, não de toda C1′;
4. blindness separada de causal aliasing;
5. witness realizado definido a `(r,c)`;
6. STATE/SIGNAL como targets operacionais;
7. C2/C3 reportados mas não autopsiados;
8. hierarquia epistemológica confirmatório → pós-confirmatório;
9. P3 como eixo principal;
10. P5/L2 como suporte técnico;
11. P7 como resultado secundário/extended por defeito;
12. novelty wording subordinado ao prior-art audit fechado;
13. ausência de replicação científica externa.

---

## 6. Elementos que podem mudar sem reabrir a arquitetura

Durante a redação podem mudar:

- título;
- wording do abstract;
- estilo e ordem fina de parágrafos;
- nomes editoriais de subseções;
- composição gráfica das figuras;
- decisão final de colocar P7 no corpo ou Extended Data, desde que o seu estatuto não mude;
- escolha de journal e respetivo formato;
- quantidade de detalhe transferida entre Results, Methods e Supplement.

Estas mudanças não podem modificar a hierarquia epistemológica ou ampliar claims.

---

## 7. Próximo passo autorizado

**PASSO 4A — CLAIM–EVIDENCE LEDGER**

O ledger deverá atomizar todas as claims antes da redação do manuscrito.

---

```text
BOUNDARY I — PASSO 4
ARTICLE ARCHITECTURE v2.1 — FROZEN
SHA256 = 8a426b6600516a0257caaffdaffd45c5484d185940ede9f64ee7b8693880cf69
```

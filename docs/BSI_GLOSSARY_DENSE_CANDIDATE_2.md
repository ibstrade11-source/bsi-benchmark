# BSI Glossary — Judge Context Reference

## Purpose

This glossary is a **semantic disambiguation reference** for the independent benchmark judge:
it explains BSI-specific abbreviations, constructs, layers, and dimensions appearing in BSI
analyses. It is **not an evaluation rubric** and does not assert BSI superiority, correctness,
or acceptance of BSI conclusions. The judge must evaluate RAW and BSI using independent criteria.

---

## 1. Core Framework Terms

### BSI — Behmanesh Index / Behmanesh Structural Index

A structured epistemic evaluation framework for assessing the robustness of knowledge artifacts
through multi-layer analysis.

BSI evaluates **epistemic robustness**, not truth, popularity, authority, consensus, persuasion,
or social acceptance.

A high BSI score is therefore not equivalent to a true conclusion, and a low BSI score is not
equivalent to a false conclusion.

### ER — Epistemic Robustness

The primary construct evaluated by BSI.

Epistemic Robustness is the degree to which a knowledge artifact maintains structural coherence,
evidential grounding, mechanistic depth, explanatory integrity, causal consistency, and
longitudinal stability under multi-layer analysis.

ER does not by itself imply truth, scientific consensus, predictive success, or correctness.

### Knowledge Artifact

Any analyzable unit of knowledge, including scientific papers, articles, books, reports,
arguments, research claims, policy proposals, public statements, and theoretical frameworks.

### Claim

A proposition presented as knowledge, belief, explanation, prediction, interpretation, or
conclusion. Claims may be explicit or implicit.

### Evidence

Information used to support, justify, or strengthen a claim. Evidence may be empirical,
observational, statistical, historical, logical, or theoretical.

### Evidence Quality

The degree to which evidence is reliable, relevant, traceable, and appropriate for supporting
a particular claim.

### Mechanistic Depth

The extent to which an analysis explains underlying mechanisms rather than merely describing
outcomes. It addresses questions such as "How does this happen?"

### Causal Structure

The network of cause-effect relationships proposed within a knowledge artifact.

### Causal Consistency

The degree to which causal explanations remain internally coherent and non-contradictory.

### Predictive Depth

The degree to which a knowledge artifact generates meaningful expectations, implications,
scenarios, or future observations from its internal structure. It evaluates predictive
architecture and does not require successful prediction.

### Explanatory Depth

The degree to which a knowledge artifact provides coherent, layered explanations beyond
surface-level description.

### Structural Coherence

The degree to which concepts, claims, evidence, mechanisms, and conclusions form an internally
consistent structure.

### Longitudinal Coherence

The degree to which claims remain coherent across time, contexts, scales, and analytical layers.

---

## 2. BSI Analytical Layers

### Multi-Layer Analysis

Evaluation across multiple epistemic layers rather than isolated statements.

Typical BSI layers include Claim, Evidence, Mechanism, System, Temporal, and Meta layers.

### Manifest Layer

The directly observable layer of claims, evidence, stated methods, stated conclusions, and other
explicit content.

### Latent Layer

The layer concerned with underlying mechanisms, assumptions, implicit structures, causal chains,
and other elements not fully explicit at the surface level.

### Meta Layer

A higher-order layer examining the structure, implications, consistency, and broader organization
of the analysis or knowledge artifact.

**Important:** Manifest, Latent, and Meta are analytical layers, not three independent final BSI
scores.

---

## 3. BIO

### BIO — Behmanesh Index Ontology

The formal ontology used to structure BSI concepts, relationships, analytical dimensions, and
machine-readable outputs.

BIO provides the conceptual vocabulary and structural organization used by BSI.

BIO is an ontology; it is not itself a score and is not an independent judge.

---

## 4. CORE_BEHMANESH

### CORE_BEHMANESH

The foundational reasoning and execution architecture associated with the Behmanesh Index.

It functions as a meta-layer over BSI and is intended to improve analytical quality, scientific
rigor, explainability, uncertainty tracking, reproducibility, and structural consistency.

CORE_BEHMANESH is an execution/reasoning architecture, not a truth detector and not a standalone
score.

---

## 5. Epistemic Integrity Gap Family

### EIG — Epistemic Integrity Gap

A structural gap between what an analyst or knowledge artifact claims to know and what the available
evidence actually permits it to claim.

EIG is a complementary diagnostic subsystem operating within the BSI analytical architecture.

It is not a replacement for BSI and is not itself proof that a claim is false.

The EIG framework distinguishes several related gap types.

### CEG — Claim-Evidence Gap

A gap in which the strength or scope of a claim exceeds the available supporting evidence.

### MCG — Method-Conclusion Gap

A gap in which a conclusion exceeds what the employed methodology can justify.

### FCG — Framing-Content Gap

A gap in which presentation, framing, rhetoric, or wording implies stronger support than the
underlying content provides.

### LCG — Longitudinal Consistency Gap

A gap in which claims become inconsistent across temporal, contextual, or analytical perspectives.

The EIG documentation treats these gaps as members of one diagnostic family, not as unrelated
standalone tools.

### EIG Score

A descriptive numerical representation of the assessed EIG pattern.

It is not a truth judgment. The EIG documentation explicitly notes that equal EIG scores can have
different underlying causes.

### EIG Origins

An identified epistemic gap may arise from different sources, including analytical inability,
data limitations, or deliberate deception. EIG is not an automatic moral judgment about the
author.

### EIG Preconditions

The EIG procedure is intended to follow extraction of the relevant intellectual structure,
including the Core Claim, Assumption Map, Causal Chain, and Value Layer.

EIG is not intended to replace domain-specific technical validation.

---

## 6. ECC

### ECC — Epistemic Confidence Calibration

A calibration subsystem that evaluates the alignment between expressed confidence and the level
of confidence actually supported by evidence, methods, and reasoning.

ECC does **not** determine whether a claim is true or false.

The BSI architecture describes ECC as a quantitative/calibration subsystem related to EIG.

A useful conceptual distinction is:

- **EIG → Where is the epistemic gap?**
- **ECC → How large is the confidence mismatch associated with that gap?**

### ECC-C — Claim Confidence

ECC applied to the confidence expressed in a claim.

### ECC-E — Evidence Confidence

ECC applied to confidence warranted by the available evidence.

### ECC-M — Method Confidence

ECC applied to confidence warranted by the methodology used.

### ECC-L — Conclusion Confidence

ECC applied to confidence expressed in the conclusion.

ECC requires appropriate separation of factual statements and inferential statements. When the
required distinctions cannot be made reliably, the ECC documentation requires the assessment to
be treated as low-confidence.

---

## 7. REIG

### REIG — Recursive Epistemic Integrity Audit

A recursive audit of the **analysis itself**, rather than an EIG analysis of the original target
artifact.

REIG asks whether the analyst's own output complies with the epistemic standards that the
analysis applies to its target.

The fundamental distinction is:

- **EIG → evaluates epistemic gaps in the target being analyzed.**
- **REIG → audits the analysis produced about that target.**

REIG therefore operates on the draft analysis/output, not directly on the source article.

Typical recursive checks include causal compliance, generalization compliance, measurement
compliance, and framing compliance.

A REIG finding does not by itself mean that the entire analysis is false or must be rejected.

### Recursive Causal Compliance

Checks whether the analyst introduced causal claims where the source evidence supports only
correlation or association.

### Recursive Generalization Compliance

Checks whether the analysis generalized beyond the population, context, evidence, or scope
supported by the source.

### Recursive Measurement Compliance

Checks whether numerical scores or precision claims in the analysis exceed the analyst's actual
epistemic support.

### Recursive Framing Compliance

Checks whether the analysis introduces value judgments or stronger framing than the underlying
evidence supports.

---

## 8. D1–D7: BSI Dimensions

The current BIO v1.0-aligned calculation document defines seven principal dimensions.

These names describe BSI's internal dimensions. They are **not independent criteria that the
benchmark judge is required to adopt**.

| ID | Official BIO name | Weight |
|---|---|---:|
| D1 | ConditionalDepth | 0.22 |
| D2 | LongitudinalCoherence | 0.18 |
| D3 | AuthenticEthicalLayer | 0.18 |
| D4 | CreativeValueAdd | 0.17 |
| D5 | StrategicDepth | 0.12 |
| D6 | InterdisciplinaryBreadth | 0.08 |
| D7 | AntiPerformativeDrift | 0.05 |

### D1 — ConditionalDepth

Assesses the depth of conditional and predictive reasoning, especially whether the analysis
constructs meaningful mechanistic "if-then" relationships.

The documented subcomponents are causal-link density, testable predictions, counterfactual
resilience, and longitudinal accuracy.

**Important distinction:** D1 concerns the presence and robustness of conditional/causal structure;
it is not simply a measure of writing quality.

### D2 — LongitudinalCoherence

Assesses continuity and coherence of reasoning across time, texts, and contexts.

The documented subcomponents include trajectory stability, contradiction resolution, consistency
of stable conceptual nodes, and theme evolution.

The BSI documentation distinguishes intentional evolution from rupture/inconsistency.

### D3 — AuthenticEthicalLayer

Assesses the authenticity and verifiability of an ethical/value layer rather than merely the
presence of ethical language.

Documented subcomponents include value-hierarchy consistency, anti-performative score, ethical
provenance, and human alignment.

D3 has some conceptual overlap with D7 but operates at a different analytical layer.

### D4 — CreativeValueAdd

Assesses whether an analysis identifies a meaningful epistemic gap, addresses it through
purposeful synthesis, and generates useful new intellectual capacity.

Documented subcomponents:

- Combinatorial Synthesis
- Epistemic Gap Targeting
- Generative Capacity

Creative wording or metaphor alone does not constitute CreativeValueAdd unless it contributes
to generative capacity.

### D5 — StrategicDepth

Assesses analytical depth relative to volume, including how much mechanistic and evidential
insight is obtained per unit of analysis.

Documented subcomponents include mechanistic depth, evidence-quality density, conditional
reasoning strength, insight-compression ratio, and layered-analysis quality.

**D1 vs D5:** D1 concerns conditional/causal structure; D5 concerns the quality and density of
the resulting analysis.

### D6 — InterdisciplinaryBreadth

Assesses breadth across domains while preserving analytical precision.

Documented subcomponents include BIO ontology coverage, concept-graph density, cross-field
integration, and methodological diversity.

Breadth without depth is not intended to receive a high score merely because many domains are
mentioned.

### D7 — AntiPerformativeDrift

Assesses avoidance of performative, engagement-driven, or attention-optimized analytical output.

Documented subcomponents include claim-classification purity, implicit-assumption exposure,
and audience-pleasing detection.

D7 is a low-weight dimension and should not be interpreted as a general measure of analytical
quality.


---

## 9. BSI Score and Its Interpretation

### BSI Score

A numerical estimate generated by the BSI evaluation process.

The score is an indicator of epistemic robustness under the BSI framework, not a direct measure
of truth.

### Truth

Truth is not directly measured by BSI.

A claim may receive a high BSI score and still be false, or receive a low BSI score and still be
true.

### Scientific Consensus

Consensus is not treated as proof of truth by BSI. It may provide contextual evidence but is not
itself a validity criterion.

### EIG Penalty

The BSI calculation documentation describes an EIG-related penalty term that can reduce the
calculated BSI score. This is an internal scoring mechanism, not an independent truth test.

---

## 10. Terminology and Execution Concepts

### Specification

The formal analytical methodology defining objectives, procedures, constraints, and evaluation
criteria.

### Methodology

The procedural framework describing how an evaluation is conducted.

### Operationalization

The process of transforming conceptual constructs into observable and evaluable dimensions.

### Dimension

A measurable component used to operationalize a larger construct such as Epistemic Robustness.

### Confidence Calibration

The alignment between expressed confidence and the strength of available support.

### Overconfidence

Confidence that exceeds evidential support.

### Underconfidence

Confidence that is lower than what the available evidence would justify.

### Epistemic Humility

Maintaining confidence proportional to evidence and uncertainty.

### Interpretive Risk

The probability that a claim, conclusion, or analysis is distorted by unsupported assumptions,
ambiguity, or insufficient evidence.

### Assumption

A proposition accepted without explicit demonstration in the analyzed artifact.

### Hidden Assumption

An unstated proposition required for an argument or explanation to function.

### Inference

A conclusion derived from premises, evidence, or a reasoning process.

### Reasoning Chain

The sequence of inferential steps connecting evidence to conclusions.

---

## 11. Terminology Used in Recursive/Structural Auditing

### Framework Fidelity

The degree to which execution preserves the procedural structure, constraints, and intended
methodology defined by a formal framework.

### Interpretation Drift

A form of execution failure in which the executing model implicitly reinterprets the formal
specification before or during execution, causing structural deviation from the intended
framework.

### Execution Architecture

The architecture responsible for implementing a formal specification while preserving its
structural integrity.

### Execution Engine

The component that executes a formal analytical specification.

### Structural Validation

Independent assessment of execution structure rather than relying only on semantic correctness.

### Execution Traceability

The ability to trace how a formal specification is reflected in the execution.

### Decision Traceability

The ability to trace how analytical decisions are connected to the stated methodology and
evidence.

### Guardrails

Constraints intended to prevent execution from deviating from the governing analytical
specification.

---

## 12. Terms That Must Not Be Invented or Guessed

**Mandatory:** If an abbreviation or technical term is undefined in this glossary and the
analysis, the judge must not invent its meaning. `HHI`, `BHI`, `DDC`, and every unfamiliar
acronym must not receive BSI-specific meanings unless defined by the analysis or an authoritative
domain source.

---

## 13. Judge-Neutrality Boundary

This glossary exists only to reduce **semantic ambiguity**. It must not:
1. force use of BSI D1–D7 criteria;
2. assume BSI is superior to RAW;
3. treat BSI terminology as evidence of analytical quality;
4. treat EIG/ECC/REIG findings as proof that an underlying claim is false;
5. treat high BSI scores as proof of truth or low scores as proof of falsity;
6. infer meanings for undefined abbreviations;
7. replace independent human validation.

The benchmark judge remains responsible for independent criterion selection and application.

---

## 14. Source and Version Note

This glossary consolidates terminology from the BSI repository materials used to construct the
benchmark context, including:

- `docs/_reference/GLOSSARY.md`
- `Ontology/BIO_v1.0.md`
- `CORE-BEHMANESH/v1.0/CORE_BEHMANESH_v1.0.md`
- `CORE-BEHMANESH/Shared_Components/EIG/Epistemic_Integrity_Gap_Analyzer_v1.0.md`
- `CORE-BEHMANESH/Shared_Components/EIG/Epistemic_Confidence_Calibration_v2.0.md`
- `CORE-BEHMANESH/Shared_Components/EIG/Recursive_EIG_v1.0.md`
- `BSI_Calculation_Formula_Hybrid_v3x.md`
- `MASTER_PROMPT_BSI_v3.4.2.md`

Where definitions overlap, the more specific module documentation is used to clarify the
operational meaning of the term.

This glossary is a benchmark-side reference and does not modify the BSI framework itself.

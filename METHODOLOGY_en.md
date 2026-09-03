BSI Benchmark

Methodology for Evaluating LLM Analytical Frameworks

Document type: Methodology Specification
Status: Draft v0.1
Scope: Framework-agnostic
Parent specification: "BENCHMARK_SPEC.md"
Companion specification: "ONTOLOGY.md"

---

1. Scope and Purpose

This document specifies the execution methodology of BSI Benchmark.

The methodology operationalizes the concepts and relations defined in "ONTOLOGY.md" into an executable experimental protocol. It therefore does not redefine the ontology-level concepts; instead, it specifies how those concepts are applied in experimental design, output generation, evaluation, comparison, data recording, and result analysis.

The primary purpose of this methodology is to provide a controlled procedure for studying the following question:

«When a structured analytical framework is used in interaction with an LLM and a specified Artifact, what change does it produce in the quality and analytical value of the resulting output, and how is that change related to stability, Drift, framework realization, and execution burden?»

This question must be studied at the level of Framework × Model × Artifact and must not be generalized from a single execution into an intrinsic property of a Framework or Model.

---

2. General Design Logic

Every Benchmark study should establish, to the extent possible, a controlled comparison between at least two Conditions:

- a reference Condition;
- an intervention Condition.

In the baseline design, the reference Condition is "RAW" and the intervention Condition is "Framework".

Both Conditions should execute the same analytical task on the same Artifact to the extent possible.

Baseline design:

[
[Artifact + Model + Task \rightarrow {RAW,\ Framework}]
]

The resulting outputs are then subjected to a common evaluation process.

This structure permits estimation of an observed change without assuming in advance that the change is attributable to the Framework.

---

3. Pre-Execution Definition of Questions and Hypotheses

The evaluation question must be specified before Benchmark execution begins.

The question should make clear whether the study is intended to examine:

- change in analytical quality;
- incremental analytical value;
- change in output stability;
- change in Drift;
- realization or non-realization of Framework requirements;
- execution cost or burden;
- or a combination of these.

In comparative studies, hypotheses should be recorded before observation of the primary results.

The design may specify a directional or non-directional hypothesis concerning the difference between Conditions, but the Benchmark must not assume that improvement exists.

---

4. Artifact Selection

4.1. Selection Unit

The Artifact must be selected and assigned an identifier before output generation.

Each Artifact must have a unique identifier and sufficient provenance information to permit recovery of the version used.

Minimum information includes:

- Artifact ID;
- title;
- type;
- domain;
- source;
- version or retrieval date;
- full-text status;
- language;
- any preprocessing applied.

4.2. Artifact Consistency

For a direct RAW-versus-Framework comparison, the input content must be identical.

If technical constraints require the two Conditions to receive different text, the difference must be recorded as an execution variable.

Such a comparison must not be reported as a fully controlled Framework comparison without explicitly reporting this limitation.

---

5. Model Selection

For every Run, the Model and Provider must be recorded precisely.

At minimum:

- provider;
- model identifier;
- model version, when available;
- generation parameters;
- context limit;
- enabled tools;
- execution date and time.

If the exact Model version cannot be determined, that uncertainty must be recorded.

The Model should not be treated merely as an output-generation instrument; in multi-model designs, Model differences are part of the experimental structure.

---

6. Task Definition

The Task must be specified before execution.

The Task must remain identical across Conditions unless the study design explicitly makes Task variation an experimental factor.

The Task definition must be sufficiently precise to ensure that:

1. the analytical objective is clear;
2. the expected output is identifiable;
3. independent execution across Conditions is possible;
4. subsequent evaluation can be performed against the same objective.

---

7. RAW Condition Design

The RAW Condition must establish a valid operational baseline.

RAW does not mean removing all general instructions. The Model must still be informed of the Task it is expected to perform.

However, RAW must not contain an analytical intervention that effectively reconstructs the Framework under evaluation.

The baseline Prompt, constraints, and resources used in RAW must be recorded.

---

8. Framework Condition Design

The Framework Condition must execute the same Task using a specified version of the Framework.

For each Framework, the following must be recorded:

- Framework ID;
- version;
- specification used;
- Prompt or Execution Carrier;
- execution stages;
- dependencies on external tools or resources;
- mandatory requirements;
- optional requirements.

If the Framework is multi-stage, the sequence of stages must be reconstructible.

---

9. Condition Alignment

The validity of the comparison depends on alignment of Conditions.

Factor| RAW| Framework
Artifact| identical| identical
Task| identical| identical
Model| identical in within-model comparisons| identical
Language| identical| identical
External resources| controlled| controlled
Time constraint| identical or recorded| identical or recorded
Context limit| recorded| recorded
Generation settings| fixed or recorded| fixed or recorded

Any unavoidable difference must be recorded in the execution data.

---

10. Prompt and Execution Carrier

The Prompt is the means by which the Task is executed and the Framework is transmitted to the Model; it must not be conflated with the Framework itself.

Accordingly, a Prompt change may constitute a methodological change even when the Framework specification remains unchanged.

Each Run must permit identification of the Prompt version.

When a Prompt Template is used, its version must also be recorded.

---

11. Independent Execution

Each independent Run must be executed within an independent execution context.

Unless the experimental design explicitly requires dependency, the following must not occur:

- output from a previous Run entering a subsequent Run;
- persistence of a previous conversation history;
- transfer of hidden system state between Conditions;
- disclosure of one Condition's result to another Condition.

The purpose of this principle is to prevent confounding arising from residual state.

---

12. Randomness and Execution Settings

When the Model or Provider permits control of randomness, the relevant settings must be recorded.

Where available:

- seed;
- temperature;
- top-p;
- other influential parameters

should be stored.

If the Provider does not provide full control over randomness, this must be recorded as a limitation.

---

13. Repeated Runs

To study output variation and Drift, a Condition should, where feasible, be executed more than once.

Repeats must:

- be independent;
- use a fixed Artifact;
- use a fixed Task;
- have comparable Model and configuration settings.

The number of repetitions must be reported in the final study report.

Increasing the number of repetitions does not by itself substitute for controlled design.

---

14. Multi-Model Comparative Design

In multi-model studies, each Model should receive the same set of Conditions to the extent possible.

Baseline design:

[
[{M_1,M_2,\ldots,M_n}\times{RAW,Framework}\times{A_1,A_2,\ldots,A_k}]
]

This design permits investigation of whether an observed effect:

- is limited to one Model;
- recurs across multiple Models;
- or depends on interaction between the Framework and Model capabilities.

---

15. Multi-Artifact Design

A single Artifact is sufficient for examining one instance, but it is insufficient for inference about a general pattern.

In multi-Artifact designs, meaningful variation should be introduced, where possible, across:

- domain;
- text type;
- complexity;
- reasoning structure;
- length;
- analytical characteristics.

Artifact selection and sampling should be appropriate to the study question and, to the extent possible, protected against outcome-driven selection before final analysis.

---

16. Output Evaluation

16.1. Task-Based Evaluation

The Judge must evaluate the output relative to the Task and Artifact.

The presence of Framework-specific terminology or superficial complexity is not, by itself, a positive quality indicator.

Likewise, a longer output must not be penalized merely because it is longer.

Evaluation must be based on the actual quality and analytical value of the output relative to the problem.

---

17. Selection of Evaluation Criteria

Criteria must be appropriate to the Task and Artifact.

The Judge may determine the criteria required for evaluation, provided that:

- the criteria are relevant to the Task;
- they have operational definitions;
- they are not imposed retrospectively based on Framework characteristics.

If fixed criteria are specified for a study, they must be recorded before evaluation is performed.

---

18. Weighting

If criteria are weighted, the weights must be specified before the final result is calculated.

The rationale for each weight must be recordable.

Weights must not be changed merely because one Condition failed to produce an expected result.

If sensitivity analysis is conducted, changes in results under alternative weighting schemes must be reported separately.

---

19. Judge Independence

Judge independence does not require the Judge to be unaware that a Framework exists.

A Judge may know that an output was generated using a particular Framework, but must not be given the expected result or Framework-specific evaluation criteria as an evaluative directive.

Where feasible, neutral identifiers may be used for outputs; however, blind evaluation is not an intrinsic requirement of the Benchmark.

The central requirement is independence of the evaluation process, not mandatory blindness.

---

20. Judge Resource

A Judge Resource may be used to reduce semantic unfamiliarity when evaluating Frameworks containing specialized terminology.

The resource must provide only the information necessary to understand the meaning of Framework-specific terms and structures.

A Judge Resource must not:

- define evaluation criteria;
- impose criterion weights;
- introduce a preferred output;
- present the Framework as superior;
- equate Framework terminology with quality.

This principle is aligned with the Benchmark Glossary design: the Glossary functions as a semantic disambiguation reference and is not an evaluation rubric.

When a Judge Resource is used, its exact version must be stored with the Run or Evaluation Record.

---

21. Self-Compare

Self-Compare must be recorded as an independent evaluation design.

In this design, the Model or system that generated the analysis also evaluates the outputs.

Self-Compare is valid for studying within-system evaluation behavior, but its results must not be treated without qualification as equivalent to independent evaluation.

Where resources permit, Self-Compare may be compared with Independent Judge evaluation.

The purpose of such comparison is to examine differences in judgment patterns, not necessarily to establish that one Judge type is inherently correct.

---

22. Independent Evaluation

In designs using an independent Judge, the Judge must not have access to the result of another Condition unless the design explicitly requires pairwise comparison.

In Pairwise Comparison, the information necessary for comparison must be equivalent across the two outputs.

If the Judge has access to Framework identity or a Judge Resource, this must be recorded.

---

23. Recording the Basis of Judgment

When an LLM Judge is used, the final score should, where feasible, be accompanied by a structured judgment basis or evidence trace.

The recorded basis should make it possible to inspect:

- the basis of the judgment;
- the criteria applied;
- the reasoning supporting the resulting assessment.

However, Judge-generated rationale must not be treated as independent truth about the Artifact.

---

24. Measuring Quality Change

Quality change between two Conditions may be calculated as a score difference or another pre-specified measure:

[
\Delta Q = Q_F-Q_R
]

where:

- Q_F is the quality of the Framework Condition;
- Q_R is the quality of the reference Condition.

The operational definition of Q must be specified in the study protocol.

\Delta Q is an observed measure and does not, by itself, establish causation.

---

25. Incremental Analytical Value

Incremental analytical value must be measured separately from absolute quality.

The evaluation should determine whether the intervention Condition:

- generates new analysis;
- enriches an existing analytical structure;
- addresses a specific limitation or gap;
- or merely reproduces the same information at greater volume.

This evaluation must be relative to the Task and Artifact.

Therefore, increased output volume is not equivalent to increased analytical value.

---

26. Drift Protocol

To measure Drift, a fixed Artifact and Task are executed across multiple independent Runs.

Comparison may occur at multiple levels:

Content Level

Changes in claims, inferences, relations, and analytical elements.

Structural Level

Changes in organization and relationships among analytical components.

Judgment Level

Changes in the Model's evaluation of outputs or of the relative quality of two Conditions.

The type of Drift being measured must be specified before analysis.

---

27. Fixed-Artifact Repetition

A key Benchmark design is repeated analysis of a fixed Artifact.

In this design:

[
A=constant
]

and across multiple Runs:

[
Analysis(A,M,C)_1,\ldots,Analysis(A,M,C)_n
]

are compared.

This design permits study of Model variability when confronted with fixed content.

---

28. Judgment Drift

To study Judgment Drift, a fixed set of outputs may be evaluated on multiple occasions.

The study must specify:

- whether the outputs remained fixed;
- whether the Judge Model remained fixed;
- whether the evaluation Prompt remained fixed;
- whether the Judge Resource remained fixed.

Any observed change must be interpreted in relation to these conditions.

---

29. Framework-Conditioned Drift

Drift may be calculated separately for RAW and Framework Conditions.

For example:

[
D_{RAW}
]

and:

[
D_{Framework}
]

may be calculated and subsequently compared.

The difference alone does not establish that the Framework caused the Drift.

---

30. Fidelity Measurement

Framework realization must be evaluated against the specification of that Framework.

Where a Framework defines specific stages or constraints, the implementation must be assessed for:

- components executed;
- components omitted;
- components modified;
- components executed ambiguously.

This information is necessary for interpreting Framework Condition results.

Incomplete execution must not be treated as full Framework execution without being recorded as such.

---

31. Attribution

The Benchmark must distinguish among three statements:

1. A change was observed.
2. A change was observed in the presence of the Framework.
3. The Framework caused the change.

The third statement requires stronger evidence.

Attribution can be strengthened by examining changes across multiple Models, Artifacts, and Runs while controlling alternative explanations to the extent possible.

---

32. Execution Burden

The cost of executing a Framework must be measured separately from output quality.

Recordable factors include:

- number of requests;
- number of stages;
- input tokens;
- output tokens;
- execution time;
- number of retries;
- Provider errors;
- financial cost, where available;
- external resource consumption.

These data should be reported alongside quality results and must not automatically be incorporated into the quality score.

---

33. Context Limit and Truncation

If an Artifact exceeds the Model's context capacity, the method used to reduce the input must be specified before execution.

Possible methods include:

- truncation;
- segmentation;
- summarization;
- retrieval;
- selection.

The selected method must be recorded.

If different portions of the Artifact are available to the two Conditions, the comparison must be reported with this limitation.

---

34. External Retrieval

If the Framework or Model uses retrieval or external resources, the provenance of those resources must be recorded.

At minimum:

- source;
- identifier;
- retrieval time;
- query, where available;
- retrieved content or hash/identifier;
- differences in resources between Conditions.

Where resources differ, the observed effect must not be attributed to the Framework without further examination.

---

35. Failure Handling

A failed execution must not be converted into an artificial score.

Every Run must have an execution status.

Minimum statuses:

- "valid"
- "failed"
- "incomplete"
- "invalid"

The reason for failure must be recorded.

A Run lacking valid output or valid evaluation must not be treated as a valid result in aggregation.

This principle is consistent with the Evidence Gate mechanism implemented in the Benchmark: incomplete execution must not be stored as benchmark evidence, and failed execution must not receive an artificial score.

---

36. Missing Data

Missing data must be distinguished from zero-valued data.

For example:

- missing score;
- Judge failure;
- Generation failure;
- unavailable full text;
- Provider interruption

must not automatically be treated as "score = 0".

The handling rule for missing data must be specified before aggregation.

---

37. Quality Control

Before a Run enters final analysis, minimum validation checks must establish that:

1. the correct Artifact was used;
2. the correct Model was used;
3. the correct Condition was used;
4. Generation was complete;
5. the output is readable;
6. the Judge result is valid;
7. scores fall within the permitted range;
8. required metadata is present.

Runs that fail these checks must be marked "invalid" or "incomplete".

---

38. Aggregation

Aggregation should proceed hierarchically:

[
Run\rightarrow Artifact\rightarrow Model\rightarrow Domain\rightarrow Benchmark
]

The final result must not be presented solely as one global mean.

Where possible, reporting should also include:

- mean;
- median;
- dispersion;
- range;
- sample count;
- number of invalid Runs;
- differences across Models;
- differences across Artifacts.

---

39. Prevention of Simpson-Type Interpretation

A global mean may conceal important differences among groups.

For example, if a Framework produces positive effects in some Models and negative effects in others, a global mean may obscure this heterogeneity.

Therefore, general claims must be examined alongside effect distributions and major groupings.

---

40. Statistical Treatment

Statistical methods must be selected according to the structure of the data.

In repeated-measures designs, independence of observations must not be assumed without examination.

When multiple Runs exist for each Model and Artifact, the data contain within-group dependencies.

In larger studies, methods that treat Model and Artifact as structural factors or effects may be appropriate.

The statistical method, its assumptions, and the treatment of missing data must be recorded in the study report.

---

41. Effect Size and Uncertainty

Reporting differences solely through mean values is insufficient.

Where feasible, results should also include:

- effect size;
- interval uncertainty;
- distribution of effects.

If the statistical method does not permit a valid estimate of uncertainty, this limitation must be explicitly reported.

---

42. Multiple Comparisons

In studies involving many Models, Artifacts, criteria, or Conditions, the risk of false positives increases.

Such studies must:

- record the number of comparisons;
- specify any method used to control multiple comparisons;
- distinguish exploratory from confirmatory results.

---

43. Exploratory versus Confirmatory

Benchmark studies may be used both to test pre-specified hypotheses and to discover patterns.

These two modes must be distinguished in reporting.

A finding discovered after observing the data must not be presented, without qualification, as a previously confirmed hypothesis.

---

44. Heterogeneity Analysis

When Framework effects differ across Models or Artifacts, the heterogeneity must be preserved and reported.

For example:

[
\Delta Q_{M_1}>0
]

while:

[
\Delta Q_{M_2}<0
]

may indicate an interaction.

This does not, by itself, constitute a failure of the Benchmark; it may be part of the principal finding.

---

45. Robustness Analysis

The primary result should be examined under reasonable variations in evaluation methodology.

Where feasible, analyses may include:

- changing the Judge;
- changing criterion weights;
- removing a Model;
- removing an Artifact;
- changing the aggregation method;
- changing the handling of incomplete data.

If a result holds only under a particular configuration, that dependency must be reported.

---

46. Sensitivity to Judge

In important studies, an output may be evaluated by more than one Judge.

The purpose is to determine how dependent the result is on a particular Judge.

If substantial disagreement occurs, the result should be reported as Judge-sensitive rather than eliminating one Judge without an independent basis.

---

47. Provenance

Every derived value must be traceable to its underlying data.

At minimum:

[
Derived\ Metric\rightarrow Evaluation\rightarrow Run\rightarrow Condition\rightarrow Artifact
]

This chain must be traceable through unique identifiers in the Benchmark data.

---

48. Benchmark Record

A structured Record must be stored for every valid execution.

Where possible, the Record should include:

- Run ID;
- Artifact ID;
- Model ID;
- Framework ID;
- Condition;
- Prompt Version;
- configuration;
- generation output;
- execution metadata;
- Judge metadata;
- evaluation data;
- validation status.

The exact Schema structure must be defined in the technical Benchmark documentation rather than in this methodology document.

---

49. Raw Data Preservation

Raw data must not be reduced to aggregate results and then discarded.

Where possible, the following should be preserved:

- Artifact reference;
- Prompt;
- raw Model output;
- Judge input;
- Judge output;
- execution metadata;
- error logs;
- configuration.

If legal, privacy, or technical constraints prevent storage of a component, the limitation must be recorded.

---

50. Reproducibility Levels

Reproducibility may be reported at multiple levels:

Level 1 — Configuration Reproducibility

Settings and versions have been recorded.

Level 2 — Execution Reproducibility

Artifact, Prompt, Model, and configuration can be reconstructed.

Level 3 — Result Reproducibility

Raw data and the result-calculation process can be reconstructed.

Level 4 — Independent Replication

An independent execution outside the original run has successfully reproduced the protocol.

The claimed level of reproducibility must correspond to the actual evidence available.

---

51. Version Control

Every Benchmark Run must be linkable to the versions used.

At minimum, the following must be identifiable:

- Benchmark specification version;
- Framework version;
- Prompt version;
- Judge Resource version;
- Model identifier;
- evaluation configuration.

A material change to any major component may constitute a new execution or a new version of the Benchmark Record.

---

52. Evidence Classification

Every result should be classified according to its evidentiary status.

Minimum distinctions include:

- direct observation;
- derived measurement;
- interpretation;
- generalized inference.

A result observed in a single Run must not be presented at the same evidentiary level as a result replicated across multiple Models and Artifacts.

---

53. Claim Boundaries

The Benchmark may make claims about behavior observed under the experimental conditions.

However, results must not, without sufficient evidence, be converted into claims such as:

- the Framework is inherently superior;
- the Framework is the definitive cause of improvement;
- a Model is inherently more capable;
- Stability means Correctness;
- increased score is equivalent to Truth;
- the result from one Artifact generalizes to all domains.

---

54. Reporting Protocol

The final study report must include at least:

1. Research Question;
2. Experimental Design;
3. Artifact Selection;
4. Model Configuration;
5. Framework Version;
6. Conditions;
7. Prompt/Execution Carrier;
8. Judge Configuration;
9. Judge Resource;
10. Number of Runs;
11. Exclusion and Failure Rules;
12. Quality Results;
13. Incremental Value Results;
14. Drift Results;
15. Fidelity Results;
16. Execution Burden;
17. Uncertainty;
18. Robustness/Sensitivity Analysis;
19. Limitations;
20. Reproducibility Information.

---

55. Minimum Valid Comparison

A minimum comparison is considered valid when:

- the Artifact is specified;
- the Task is specified;
- the Model is specified;
- RAW and Framework Conditions are identifiable;
- outputs for both Conditions are available;
- the Judge result is valid;
- the evaluation criteria are identifiable;
- required metadata is recorded.

If any of these elements is absent, the result must be appropriately marked.

---

56. Minimum Evidence for Framework-Level Claims

A claim concerning a Framework at a general level must not be derived from a single comparison.

To strengthen such a claim, evidence should be replicated across multiple levels:

[
Run\rightarrow Artifact\rightarrow Model
]

and, where possible:

[
\rightarrow Domain
]

The more independent conditions under which a result is replicated, the stronger the basis for inferring a systematic pattern.

---

57. Interpretation of Negative Results

Failure to observe improvement is itself a valid result.

If, under specified conditions, a Framework:

- does not change quality;
- provides limited incremental value;
- increases Drift;
- or increases execution cost without proportional value,

this must not be treated as a methodological failure.

The Benchmark must support positive, neutral, and negative effects equally.

---

58. Interpretation of Mixed Results

When results differ across Models or Artifacts, findings must be reported conditionally.

For example:

«The Framework produced improvement under some tested conditions and reduced quality under others.»

Such a pattern must not be converted into an absolute claim through a single aggregate mean.

---

59. Cost–Value Analysis

Where execution cost matters, Quality and Incremental Value should be analyzed alongside Execution Burden.

A Framework may:

- provide high analytical value at high cost;
- provide limited value at high cost;
- provide moderate value at low cost;
- or produce no material effect.

The Benchmark must not impose a single trade-off function on all applications unless that function has been defined in advance.

---

60. Framework-Neutral Implementation

The Benchmark implementation must permit evaluation of different Frameworks without changing the core comparison logic.

No Framework should be required to adapt its conceptual architecture to BSI merely to enter the Benchmark.

What should be standardized is:

- Condition recording;
- Record generation;
- validation;
- evaluation interface;
- provenance;
- reporting.

Not the internal architecture of the Framework.

---

61. Relationship to BSI

BSI is one Framework subject to evaluation within this Benchmark.

BSI-specific characteristics—including terminology, internal dimensions, analytical methods, and proprietary indices—must not automatically become general Benchmark criteria.

Therefore:

[
BSI\subset Frameworks_{Evaluated}
]

and:

[
BSI\ Benchmark\neq BSI\ Evaluation\ Rubric
]

The Benchmark is the comparison infrastructure; the Framework is one of the objects being compared.

---

62. Relationship to the Ontology

This document deliberately avoids redefining core concepts.

The division of responsibility is:

Topic| Ontology| Methodology
Concept definitions| ✓| —
Relation definitions| ✓| —
Condition definition| ✓| —
Judge definition| ✓| —
Drift definition| ✓| —
Condition construction| —| ✓
Sampling| —| ✓
Repeated Runs| —| ✓
Evaluation procedure| —| ✓
Calculation| —| ✓
Aggregation| —| ✓
Error control| —| ✓
Reproducibility reporting| —| ✓

Where Implementation is inconsistent with the Ontology, the Implementation must be corrected or the limitation explicitly documented; the meaning of a Construct must not be changed merely to accommodate the Implementation.

---

63. Data Integrity Principle

No data may be fabricated merely to complete a result table.

In particular:

- "failure ≠ zero"
- "missing ≠ zero"
- "unavailable ≠ poor quality"
- "invalid ≠ low score"

Invalid data must remain invalid.

This principle is necessary to prevent artificial evidence and preserve Benchmark auditability.

---

64. Auditability

Every important result must be auditable.

An auditor should be able, to the extent possible, to follow the chain:

[
Claim\rightarrow Result\rightarrow Metric\rightarrow Evaluation\rightarrow Output\rightarrow Run\rightarrow Configuration
]

If any part of this chain cannot be recovered, the limitation must be disclosed.

---

65. Final Execution Principles

Benchmark execution must conform to the following principles:

1. Every comparison must be grounded in a specified Task and Artifact.
2. RAW and Framework Conditions must be aligned to the extent possible.
3. Model, Prompt, and configuration must be identifiable.
4. Independent execution must prevent carry-over from prior state.
5. Repeated Runs should be used to study variation and Drift.
6. The Judge must determine Task-appropriate criteria independently of Framework-specific preferences.
7. Judge Resources must serve only semantic disambiguation.
8. Self-Compare must be reported as a distinct design.
9. Framework Fidelity must be measured separately from Quality.
10. Drift must not be equated with Stability or Correctness.
11. Execution Burden must be recorded separately.
12. Failure and Missing Data must not be converted into artificial scores.
13. Raw data should be preserved to the extent possible.
14. Every Metric must be traceable to its underlying data.
15. Aggregation must not conceal Model or Artifact heterogeneity.
16. Exploratory and Confirmatory results must be distinguished.
17. Lack of improvement and negative results must be preserved as valid findings.
18. Causal claims must be proportionate to the strength of the experimental design.
19. Framework-level claims require replicated evidence.
20. No Framework may be presumed superior in the Benchmark design.

---

66. Compact Operational Definition

BSI Benchmark is a comparative and repeated-measures protocol in which an analytical Task is executed on specified Artifacts, under recordable Conditions, with and without a Framework; the resulting outputs are evaluated through an independent and auditable evaluation process; and observed differences in quality, analytical value, Framework realization, Drift, Stability, and execution burden are recorded and analyzed at the Run, Artifact, and Model levels.

The strength of any result depends on the number and diversity of executions, the quality of Condition control, the independence of evaluation, data traceability, and the degree of replication.

---

67. Final Methodological Principle

Benchmark methodology must first and foremost be reviewable, repeatable, and resistant to outcome-driven interpretation.

Its purpose is not to produce a predetermined winner. Its purpose is to create conditions under which the effect of a Framework can be observed, measured, compared, and interpreted at a level proportionate to the available evidence in its actual interaction with Models and Artifacts.

Within this framework, a valid result is not necessarily a result that demonstrates improvement. A valid result is one that is legitimately derived from a transparent design, traceable data, independent evaluation, and pre-specified rules.

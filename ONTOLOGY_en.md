BSI Benchmark

Ontology of LLM Analytical Framework Evaluation

Document type: Ontology Specification
Status: Draft v0.1
Scope: Framework-agnostic
Parent specification: "BENCHMARK_SPEC.md"
Companion document: "METHODOLOGY.md"

---

1. Introduction

BSI Benchmark is an evaluation framework for studying and measuring the effect of using structured analytical frameworks on the analytical performance of large language models (LLMs).

The subject of the Benchmark is not simply the question of whether a framework makes an analysis "better." Such a formulation is overly reductive, because LLM analysis is not a one-dimensional output, and the effect of a framework does not necessarily collapse into a single change in a summary score.

Instead, the Benchmark seeks to determine:

1. what changes the use of an analytical framework produces in an analysis;
2. what these changes mean in terms of analytical quality and value;
3. to what extent the framework is actually realized by the model in practice;
4. in which dimensions, and under what conditions, the framework's potential added value emerges;
5. how this effect interacts with the model's capability, the type of text, and the nature of the analytical problem;
6. and what effect using the framework has on the stability and degree of drift of the analysis across repeated runs.

Hence, the primary unit of study in the Benchmark is not a "score," but the pattern of the framework's effect on the LLM's analytical behavior and quality.

---

2. Scope of the Ontology

This ontology specifies which concepts the Benchmark treats as the primary entities of study, and what their relationships to one another are.

This document distinguishes among three levels:

First level — Empirical entities

Things that exist directly within the experimental process:

- the text or artifact under analysis;
- the language model;
- the raw analysis;
- the framework-mediated analysis;
- the analytical framework;
- the analysis execution;
- the repeated execution;
- the judgment;
- the Judge Resource.

Second level — Analytical constructs

Properties used to describe or evaluate these entities:

- analytical quality;
- incremental analytical value;
- framework realization;
- framework fidelity;
- Drift;
- stability;
- execution cost or burden;
- generalizability.

Third level — Explanatory relations and conditions

Relations that explain why an effect was observed:

- the interaction of framework and model;
- the interaction of framework and text;
- the interaction of model and text;
- the three-way interaction of framework × model × text;
- the distinction between the framework's true effect and the limitation of the model's ability to execute it.

This separation prevents an empirical observation from being converted directly into a causal conclusion.

---

3. The Fundamental Problem of the Benchmark

The fundamental problem of the Benchmark can be stated as follows:

"When a language model examines a fixed piece of content with and without the use of a structured analytical framework, what change occurs in the quality, richness, organization, reasoning capacity, and analytical value of the output; under what conditions does this change occur; and how does the use of the framework change the execution behavior and stability of the analysis?"

The Benchmark is therefore not a binary problem of the form:

"Framework = Better / Worse."

Rather, it is a problem of studying a multidimensional effect.

---

4. Central Principle: The Framework's Effect Is a Multidimensional Construct

The effect of an analytical framework must not be reduced to a simple difference between two scores.

For a framework F, model M, analyzed artifact A, and execution conditions T, the observed effect can be treated as a conceptual vector:

[
E(F \mid M,A,T)

{
\Delta Q,,
\Delta V,,
R,,
Fid,,
D,,
S,,
C
}
]

where:

- \Delta Q: the change in analytical quality;
- \Delta V: incremental analytical value;
- R: the framework's fit to the problem;
- Fid: the degree of the framework's executional realization/fidelity;
- D: the degree of Drift;
- S: the stability of the analysis execution;
- C: execution cost or burden.

This representation is a conceptual model, and does not necessarily mean the Benchmark must merge all these dimensions into a single combined index.

The important principle is that:

"A framework can be beneficial along one dimension and costly or unstable along another."

Hence, reporting the effect profile is epistemically prior to any combined index.

---

5. The Text or Artifact Under Analysis

5.1 Definition

The Analytical Artifact, or "artifact under analysis," is the content that the model must analyze.

Depending on the Benchmark's design, this artifact can include items such as:

- a scientific article;
- a philosophical article;
- a political text;
- a report;
- an analytical document;
- or any other textual content.

In each experiment, the artifact must be treated as a relatively fixed input across the comparative conditions.

5.2 Ontological Role

The artifact is not merely an "input."

Its type, complexity, structure, and content can determine:

- what kinds of analyses are possible;
- which criteria are meaningful for quality;
- which framework capabilities become observable;
- and to what extent the observed effect is generalizable.

Therefore:

"The framework's effect is always the framework's effect on a specific problem, not a property independent of content."

---

6. The Language Model (LLM)

6.1 Definition

The LLM is the computational agent that analyzes the artifact.

The model can:

1. produce an analysis without the framework;
2. produce an analysis with the framework;
3. in some designs, also evaluate the analyses that were produced.

6.2 Ontological Importance

The LLM is not merely a neutral instrument for executing the framework.

The model's ability to:

- understand instructions;
- maintain constraints;
- carry out steps;
- use the framework's concepts;
- reason;
- and produce stable output

can affect the outcome of the effect.

Therefore, observing weak performance under a framework does not, by itself, prove that the framework itself is weak.

It is possible that the framework requires a level of executional ability that the model under test lacks.

---

7. The Analytical Framework

7.1 Definition

An analytical framework is a structured set of concepts, instructions, relations, constraints, steps, or procedures used with the aim of shaping, guiding, or enriching the analysis process.

A framework can belong to any approach or researcher.

The BSI Benchmark is not inherently dependent on any one particular framework.

The Framework-Agnostic Principle

"The Benchmark must be able to examine different analytical frameworks under a shared evaluation logic, without imposing any particular framework's internal concepts as a general criterion."

In this architecture, BSI is one of the frameworks that can be evaluated, not the definer of the Benchmark's ontology.

---

8. The Raw Condition and the Framework Condition

To study the effect of a framework, two main analytical conditions of an artifact can be defined.

8.1 RAW Condition

Analysis under conditions in which the framework being evaluated is not made available to the model as a structured intervention.

RAW represents the "baseline analysis."

RAW does not necessarily mean:

- an analysis with no instructions at all;
- a weak analysis;
- or an unstructured analysis.

Rather, its operational definition depends on the experimental design.

8.2 FRAMEWORK Condition

Analysis of the same artifact under use of the framework being evaluated.

The FRAMEWORK Condition shows how the model changes its analysis upon receiving the structured intervention.

---

9. Incremental Analytical Value

One of the Benchmark's most important constructs is Incremental Analytical Value, or "added analytical value."

Incremental analytical value refers to the change that using the framework produces in the analysis's capability or quality relative to the baseline condition.

Conceptually:

[
IAV = Q_{Framework} - Q_{Raw}
]

However, this relation should not be treated as the complete definition of added value.

Because added value may appear along dimensions that are lost in a simple average; for example:

- discovering causal relations;
- identifying hidden assumptions;
- organizing the argument;
- increasing the depth of explanation;
- exposing contradictions;
- increasing the traceability of reasoning;
- or revising the initial analysis.

Therefore, the Benchmark must also allow observation of the type of added value, not only its magnitude.

---

10. Analytical Quality

10.1 Definition

Analytical quality is the quality of the model's performance in converting an artifact into a meaningful, well-reasoned analysis appropriate to the problem.

Quality is not a one-dimensional, universal concept.

Depending on the artifact and the goal of the analysis, relevant dimensions can include items such as:

- accuracy and reliability;
- relevance to the text;
- depth of reasoning;
- coherence;
- argumentative structure;
- causal explanation;
- identification of assumptions;
- coverage of important points;
- distinguishing claim from evidence;
- or other related capabilities.

Hence, the Benchmark avoids imposing a single fixed rubric on all content.

10.2 Article-Centered Criteria

Evaluation criteria can be shaped to fit the nature of the artifact.

This principle does not mean that evaluation is unstructured.

Rather:

"The structure of the evaluation is fixed, but the content of the evaluation criteria must be compatible with the analytical problem."

---

11. Judge

The Judge is the entity that evaluates and compares the produced analyses.

The Judge can be:

- the same analyzing model;
- a different model;
- or, in more developed designs, an independent evaluator.

The Judge must not decide based merely on the RAW or FRAMEWORK label.

Its goal is to evaluate the actual capabilities of the outputs.

---

12. Self-Compare as an Independent Experimental Condition

Self-Compare is one of the valid methods of study within the Benchmark, but it must not be equated with Blind Evaluation.

In Self-Compare:

1. one model can produce both the RAW and FRAMEWORK analyses;
2. the same system can observe both analyses;
3. it independently determines the criteria relevant to the artifact;
4. it evaluates both analyses according to those criteria;
5. and finally judges their relative value.

The goal of Self-Compare is to measure the added value recognized from within the same analytical system.

This design is not conceptually considered an inherent weakness.

---

13. The Epistemic Importance of Self-Compare

A system may hold a certain natural preference toward its own output or baseline condition.

From this perspective, if the same system, after producing the framework-mediated analysis, can — based on independently, not previously imposed, criteria — prefer the FRAMEWORK analysis over the RAW one, this observation carries particular informational value.

More precisely:

"Self-Compare can show whether the analytical system itself recognizes the difference created by the framework as analytically meaningful."

This feature matters especially when:

- the criteria were not arbitrarily predetermined in favor of the framework;
- there is no automatic score or reward for the FRAMEWORK;
- and the Judge can also declare RAW the winner.

Nevertheless, Self-Compare should not be treated as a substitute for independent evaluation for all research questions.

These two designs provide different estimators of the framework's value.

---

14. Blind Evaluation

Blind Evaluation is a different condition, in which the evaluator is unaware of the identity or label of the condition.

The goal of Blind Evaluation is mainly to reduce the effect of the label and the evaluator's expectation.

Therefore:

"Self-Compare and Blind Evaluation are not competing designs; they are two experimental conditions with different objectives."

Imposing blindness on Self-Compare can destroy Self-Compare's fundamental feature, since in Self-Compare the system's awareness of the condition is itself part of the subject under study.

---

15. Judge Resource

15.1 Definition

Every analytical framework may have concepts, terms, abbreviations, or specialized structures that are unfamiliar to an outside Judge.

To reduce error arising from unfamiliarity, every framework can provide a Judge Resource.

This Resource is meant to create semantic access to the framework.

15.2 The Philosophy of the Judge Resource

The Judge Resource must not persuade the Judge that the framework is good.

Its task is:

"To reduce the negative bias arising from unfamiliarity with the framework's language and concepts, not to increase positive bias in the framework's favor."

This distinction is fundamental.

A new framework may have terms that are unknown to the evaluator. If the Judge evaluates without understanding the meaning of these terms, part of the observed difference may stem from lack of familiarity, not from an analytical weakness of the framework.

The Judge Resource must reduce this problem.

---

16. The Boundaries of the Judge Resource

The Judge Resource is permitted to include:

- definitions of terms;
- explanation of abbreviations;
- explanation of the meaning of concepts;
- minimal operational explanation needed to understand a term;
- conceptual relations necessary to prevent misunderstanding.

But it must not include:

- claims of the framework's superiority;
- determining what conclusion the Judge should reach;
- imposing scoring criteria;
- setting the weight of criteria;
- proving the correctness of the framework's claims;
- or promoting the framework's findings.

Therefore:

"The Judge Resource is a tool for semantic access, not a tool for persuasion or scoring."

---

17. Framework Realization

A distinction must be drawn between "the presence of a framework in the prompt" and "its actual execution by the model."

Framework Realization shows the extent to which the model was able to realize the framework's expected logic in its output.

This concept is not identical to analysis quality.

It is possible that:

- the framework is executed well but the final analysis is weak;
- the framework is executed incompletely but the analysis is still very good;
- or both are high.

Therefore:

[
Framework\ Realization \neq Analytical\ Quality
]

---

18. Framework Fidelity

Fidelity refers to the degree to which the actual execution conforms to the framework's defined structure and constraints.

Fidelity differs from Quality.

A model may execute a framework very faithfully, yet the analytical result has limited value.

Conversely, the model may deviate from some of the framework's details while still producing a valuable analysis.

Hence, Fidelity should be used to interpret the framework's effect, not automatically assumed to be equivalent to quality.

---

19. Interpretation Drift

Interpretation Drift refers to the change in, or the distancing of, the model's actual execution from a framework's specifications, logic, or intended meaning during execution.

This concept, within the Benchmark, is part of the LLM's executional behavior.

Drift can arise from:

- the framework's complexity;
- the length of the pipeline;
- the model's limitations;
- ambiguity in the instructions;
- interaction among steps;
- or other executional factors.

Therefore, observing Drift alone does not prove that the framework is unsuitable.

---

20. Analytical Drift

Analytical Drift must also be distinguished from Interpretation Drift.

Analytical Drift refers to the changes observed across repeated analyses of a fixed artifact under repeated conditions.

These changes may include differences in:

- claims;
- arguments;
- causal relations;
- interpretations;
- key findings;
- the structure of the analysis;
- or the conclusion.

The purpose of measuring it is to study the stability of the model's analytical behavior, not merely the lexical difference between outputs.

---

21. Drift as a Secondary but Important Consequence

Drift is an independent and important subject within the Benchmark, but it must not replace the concept of quality.

The fundamental principle:

"Stability alone is not a sign of quality."

A model can repeatedly produce a weak analysis with high consistency.

Likewise, a framework may increase the quality of the analysis but, due to increased execution complexity, introduce a certain amount of instability.

Therefore, the Benchmark must be able to observe both:

[
Quality
\quad\text{and}\quad
Stability
]

and examine the relationship between them.

---

22. Evaluation Drift

Drift may not only fail to occur in the production of the analysis.

If a fixed set of analyses is evaluated by the Judge on multiple occasions, the judgment itself can also change.

This phenomenon is called Evaluation Drift.

Therefore, the Benchmark must separate two distinct processes:

Analysis Drift
     ↓
change in the analysis itself

Evaluation Drift
     ↓
change in the judgment of a fixed analysis

This distinction is of fundamental importance for assessing the validity of the Benchmark's results.

---

23. The Interaction of Framework × Model × Artifact

One of the central principles of the Benchmark's ontology is that an observed effect cannot necessarily be attributed to the Framework alone.

A more appropriate conceptual model is:

[
Outcome = f(F, M, A, F\times M, F\times A, M\times A, F\times M\times A)
]

where:

- F: Framework;
- M: Model;
- A: Artifact.

Therefore, if a framework performs poorly on a given model, several explanations are possible:

1. the framework itself has a limitation;
2. the model lacks sufficient ability to execute the framework;
3. the artifact is not compatible with the framework;
4. the interaction of Framework and Model is unfavorable;
5. the interaction of Framework and Artifact is unfavorable;
6. or a combination of these factors is present.

---

24. The Principle of Model Executional Capacity

The more complex a framework is, the higher the model capacity its execution may require.

Hence:

"Increased Drift or decreased Fidelity on a weak model is not, by itself, evidence against the Framework."

If the same pattern repeats across several models with different capabilities and architectures, this provides stronger evidence for the existence of a stable property within the Framework itself.

This principle protects the Benchmark from hastily attributing every result to the Framework.

---

25. The Framework's Effect versus the Effect of Model Ability

The Benchmark must distinguish between two propositions:

Proposition A

"The model failed to execute the framework well."

This proposition is about the model's behavior.

Proposition B

"The framework caused weak performance."

This proposition is a causal claim about the Framework and requires more evidence.

These two propositions are not ontologically equivalent.

---

26. Execution Cost and Burden

A framework may increase the quality of the analysis while, at the same time:

- consuming more tokens;
- requiring more execution time;
- creating more steps;
- increasing the probability of pipeline failure;
- or requiring a more powerful model.

These properties are part of the Execution Burden.

Therefore, evaluating a Framework based on raw quality alone is not sufficient.

In real-world applications, the more important question may be:

"How much analytical value was obtained for how much execution cost?"

---

27. Absolute Quality and Relative Added Value

The Benchmark must distinguish between two concepts:

Absolute Analytical Quality

How good is the analysis in itself?

Incremental Analytical Value

How much additional value did using the Framework create relative to the baseline?

These two may yield different results.

For example:

- RAW = high quality
- FRAMEWORK = slightly higher quality

In this situation, the Framework has added value, but it has not necessarily produced a fundamental transformation.

Or:

- RAW = low quality
- FRAMEWORK = moderate quality

In this case, the Framework's added value may be large, even if the final quality is still not ideal.

---

28. Article-Centered Criteria and the Independence of Judgment

The Benchmark must not mechanically impose a single fixed rubric across all domains.

Because the properties of a good analysis in a philosophical article are not necessarily the same as a good analysis of an empirical article, a political report, or a historical text.

At the same time, flexibility of criteria must not turn into unlimited freedom for the Judge.

The ontological principle is:

"The subject of evaluation is fixed; the criteria for observing it can be specialized to fit the nature of the subject."

This is precisely what distinguishes "article-adaptive evaluation" from unruly evaluation.

---

29. Criterion Independence and No Automatic Reward

The mere existence of a Framework must not automatically produce:

- an additional score;
- additional weight;
- a mandatory dedicated criterion;
- or a structural preference

in its favor.

Even if a Framework has powerful internal concepts, the Judge must still be able to declare RAW the winner based on the actual capability of the output.

This property is necessary to preserve the meaning of the comparison.

---

30. The Benchmark's Relation to Framework-Specific Concepts

A framework may have its own internal, specific concepts.

For example, BSI has a set of dedicated concepts and terminology.

But:

"A Framework's internal concepts are not part of the Benchmark's general ontology."

They belong at the level of Framework-specific Knowledge.

The conceptual structure is as follows:

BSI Benchmark Ontology
        │
        ├── Framework
        │       │
        │       ├── BSI
        │       │    └── BSI-specific concepts
        │       │
        │       ├── Framework X
        │       │    └── X-specific concepts
        │       │
        │       └── Framework Y
        │            └── Y-specific concepts
        │
        └── Common evaluation constructs

---

31. Benchmark Record

The unit of data recording in the Benchmark must represent a specific experimental condition.

A Record can conceptually include the following relation:

Artifact
   +
Model
   +
Framework Condition
   +
Execution Configuration
   +
Analysis Output
   +
Evaluation

In a comparative run, related Records can belong to a single RAW/FRAMEWORK pair.

This structure matters for the reproducibility and auditability of results.

---

32. Execution and Run

Each analysis is the product of an Execution.

A set of Executions under controlled conditions constitutes a Run.

Repetition of Runs makes it possible to study stability and Drift.

This distinction matters because:

"A single output represents one observation; a set of repeated executions makes it possible to study the system's behavior."

---

33. The Benchmark's Result

The Benchmark's result must not be treated merely as a number.

A more complete result includes the following:

Observed Outcome
+
Quality Profile
+
Incremental Value
+
Framework Realization/Fidelity
+
Drift/Stability
+
Execution Context
+
Uncertainty

Accordingly, a professional report must be able to answer the question:

"What changed, how much did it change, under what conditions did it change, and with what degree of confidence can this change be attributed to the Framework?"

---

34. Effect Claims and the Level of Evidence

The existence of a difference between RAW and FRAMEWORK is an observation.

But observing a difference is not the same as proving a causal effect.

The Benchmark must use a hierarchy of evidence:

Level 1 — Observation in a single run

A difference has been observed.

Level 2 — Repetition on the same model

The pattern has been observed in a repeated run.

Level 3 — Repetition across models

The pattern is not confined to a particular model.

Level 4 — Repetition across artifacts

The pattern is not confined to a particular text.

Level 5 — Repetition across domains

The pattern has also been observed across different domains.

The higher the level of evidence, the stronger the claim of generalizability.

---

35. Reproducibility

Reproducibility is part of the meaning of a Benchmark result.

For a reliable result, it should be possible, as far as possible, to specify:

- which artifact was used;
- which model and provider were used;
- which prompt/version was used;
- which version the Framework had;
- which model the Judge was;
- what the execution conditions were;
- what the exact output was;
- and how the result was obtained.

Hashing the analytical outputs can be used to guarantee the integrity of the recorded artifacts.

---

36. Limits of Statistical Inference

If a Record contains multiple criteria, the criteria within the same Record are not necessarily independent observations.

Therefore:

"The number of criteria must not, without regard to the structure of the data, be treated as equivalent to the number of independent samples."

The unit of statistical independence must be explicitly defined in the Methodology.

This principle prevents the sample size from appearing artificially large as the number of criteria in an analysis increases.

---

37. What the Benchmark Does Not Measure

The Benchmark must not interpret its results beyond the experimental design.

By default, the Benchmark does not claim that:

- a Framework produces absolute truth;
- a Framework is best for all models;
- a Framework is suitable for all domains;
- a model truly "understands" the Framework;
- or that a score increase alone proves the Framework's scientific superiority.

The Benchmark makes claims about the observable behavior of the analytical system under defined conditions.

---

38. Impartiality of the Benchmark

The impartiality of the Benchmark does not mean removing the Framework from evaluation.

Rather, it means that:

"The Framework must be able to demonstrate its effect, without the Benchmark having predetermined the outcome for it from the start."

Therefore, the Benchmark must allow for the possibility of observing the Framework's value as well as the possibility of its failure.

---

39. BSI as a Framework Under Evaluation

The BSI Framework can use all of the Benchmark's general mechanisms.

But:

- BSI's terminology;
- BSI's internal dimensions;
- BSI's concepts;
- and BSI's Judge Resource

must not become mandatory criteria for all other Frameworks.

This separation is fundamentally important for the Benchmark's independence from its creator.

---

40. The Principle of Separation between Benchmark and Framework

One strategic principle of this project is:

"The Benchmark must be able to evaluate the Framework without its own validity depending on that Framework's success."

This principle is realized when:

1. the Benchmark's ontology is general;
2. the methodology is applicable across different Frameworks;
3. each Framework's Judge Resource is defined separately;
4. a Framework's internal criteria are not imposed as general criteria;
5. and the Benchmark's result can turn out in favor of or against the Framework.

---

41. Final Conceptual Model

The main relations of the Benchmark's ontology can be summarized as follows:

                         ┌──────────────┐
                         │   Artifact   │
                         └──────┬───────┘
                                │
                                ▼
                         ┌──────────────┐
                         │     LLM      │
                         └──────┬───────┘
                                │
                 ┌──────────────┴──────────────┐
                 │                             │
                 ▼                             ▼
          ┌─────────────┐               ┌─────────────┐
          │ RAW         │               │ FRAMEWORK   │
          │ Condition   │               │ Condition   │
          └──────┬──────┘               └──────┬──────┘
                 │                             │
                 └──────────────┬──────────────┘
                                ▼
                       ┌─────────────────┐
                       │ Analytical      │
                       │ Outputs         │
                       └────────┬────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │ Evaluation      │
                       │ / Judge         │
                       └────────┬────────┘
                                │
             ┌──────────────────┼───────────────────┐
             ▼                  ▼                   ▼
        Quality          Incremental Value     Realization
             │                  │                   │
             └──────────────────┼───────────────────┘
                                │
                                ▼
                         Effect Profile
                                │
                                ├── Stability
                                ├── Drift
                                ├── Cost
                                └── Uncertainty

At a higher level, all these relations sit under the influence of three primary factors:

                 ┌───────────┐
                 │ Framework │
                 └─────┬─────┘
                       │
             ┌─────────┼─────────┐
             ▼         ▼         ▼
          Quality    Fidelity   Drift
             ▲         ▲         ▲
             │         │         │
             └─────────┼─────────┘
                       │
              ┌────────┴────────┐
              │                 │
           ┌──┴──┐           ┌──┴────┐
           │ LLM │           │Artifact│
           └─────┘           └────────┘

---

42. Fundamental Ontological Propositions

The Benchmark's ontology rests on several fundamental propositions:

O1 — Analysis is a multidimensional entity.

The quality of an analysis cannot be reduced to a single property.

O2 — The Framework's effect is multidimensional.

Quality change is only one component of the effect.

O3 — Relative added value is not the same as absolute quality.

A Framework may create added value without the final output reaching an absolute desired level.

O4 — Execution of the Framework is not the same as analysis quality.

Fidelity and Realization are constructs independent of Quality.

O5 — Drift does not mean the Framework is weak.

Drift may arise from the interaction of the Framework with the model's capacity.

O6 — Stability alone is not Quality.

The consistency of a weak analysis does not make it good.

O7 — Self-Compare is a valid and independent experimental condition.

Its value lies in measuring added value as recognized from within the analytical system itself.

O8 — Blind Evaluation has a different purpose.

It must not be conflated with Self-Compare.

O9 — The Judge Resource exists to reduce unfamiliarity bias.

This Resource must not impose a criterion or outcome on the Judge.

O10 — Framework-specific concepts are not general.

No Framework has the right to impose its own ontology on the entire Benchmark.

O11 — The observed effect depends on the Model and the Artifact.

A claim of generalization requires repetition across different models and artifacts.

O12 — The Benchmark's result is an Effect Profile, not merely a Score.

Every number must be interpreted within the context of its execution conditions.

---

43. The Boundary between Ontology and Methodology

This document specifies what the subject of study is.

But determining details such as:

- how many artifacts to select;
- how many times to repeat execution;
- which models to select;
- how criteria are extracted;
- how weights are determined;
- which statistical test to use;
- how the Confidence Interval is computed;
- or what threshold is used for drawing conclusions

falls within the domain of "METHODOLOGY.md."

Likewise, the details of CLI implementation, file schemas, the structure of result records, and the software pipeline belong in the project's technical documentation.

---

44. Compact Definition of the Benchmark

Based on this ontology, the BSI Benchmark can be defined compactly as follows:

"The BSI Benchmark is a framework-agnostic, empirical evaluation system for studying the effect of structured analytical frameworks on analyses produced by large language models; a system that, by comparing baseline and framework-mediated conditions, studies the profile of change in quality and analytical added value, while simultaneously treating framework realization, stability and Drift, execution cost, and the dependency of the effect on the model and the artifact as interpretive and complementary components."

---

45. Final Principle

The Benchmark's goal is not to find a "permanent winner."

Its goal is to determine:

"When an analytical framework is used by a language model to analyze specific content, exactly what does it change, what analytical value does this change have, to what extent is it truly the result of the framework's realization, under what conditions does it repeat, and what consequence does its use have for the system's stability and executional behavior?"

Accordingly, the desired output of the Benchmark is not merely:

RAW = X
FRAMEWORK = Y

but a revisable, empirical description of the framework's effect.

---

Status of This Document

This document should be regarded as the conceptual and ontological layer of the Benchmark.

Changes related to experimental design, sampling, condition control, repetition, evaluation, statistical testing, and reporting must be recorded in "METHODOLOGY.md" and must not, without necessity, alter this document's fundamental definitions.

"BENCHMARK_SPEC.md," as the parent document, determines the relationship among this Ontology, the Methodology, and the Benchmark's implementation.

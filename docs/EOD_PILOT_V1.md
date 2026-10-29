# EoD Pilot v1 — Is a first research contribution easier with a guide?

**Draft:** October 28, 2026 · **Status:** Proposed, not yet conducted.

## Research question

Does a low-friction, story-first biomedical resource experience help people with no specialist training correctly choose a research tool, verify a public-source fact, and explain its limitations, compared with the same resources presented as a conventional catalog?

This tests a **specific educational hypothesis** relevant to Evolution on Demand. It does not demonstrate accelerated biological evolution, discover a therapeutic target or measure medical outcomes.

## Testable predictions

1. People using the beginner guide should make an appropriate **first tool choice** more frequently than comparable people given only the full directory.
2. Guide users should complete **one source-backed microtask** more often and with fewer wrong steps.
3. Guide users should more often explain **why the tool fits** and identify at least one scientific limitation.
4. For story-first visitors, original source facts should be easier to distinguish from analogies and modern follow-up tasks.

Treat these as hypotheses. No improvement is guaranteed.

## Two stages

### Stage A — formative usability (first)
- Invite 6–10 adult volunteers with a range of educational backgrounds. Do not collect diagnoses or other sensitive health information.
- Ask them to speak aloud while trying the guide, story archive and contribution page on their own phones or computers.
- Observe whether they hesitate, scroll past the right button, misunderstand terminology or cannot complete an authentic public-source check.
- Measure **time to first appropriate action**, **whether the task is completed correctly**, and **what they say the source proved**.
- Revise wording and navigation based on observed problems before attempting outcome comparisons.
- Do not claim statistically generalizable results from this sample.

### Stage B — preregistered comparison (later)
- Assign volunteers with similar starting experience to either:
  A. **Standard catalog**: `catalog.html` and its normal search, or
  B. **Guided pathway**: `start.html` + a relevant story.
- Give each participant a matched public-data task. Counterbalance assignments or randomize and report sample sizes, exclusions and prior domain knowledge.
- Define primary outcome and the analysis plan **before** receiving responses. Consult a methods adviser for sample size and appropriate uncertainty reporting.
- Keep tasks educational; do not give medical-case scenarios that reveal patient information.

## Three candidate microtasks

| Prompt | Valid public tool | Objective observation |
|---|---|---|
| "Which cells show insulin protein in the pancreas?" | Human Protein Atlas INS page | Cite original URL and identify pancreatic endocrine / beta cells as reported, not treatment implications |
| "Find Penicillin G's unique compound identifier." | PubChem | CID 5904; explain what a chemical identifier **does not** establish |
| "Find what kind of experiments make DepMap useful for gene dependency." | DepMap | Identify cancer cell-line CRISPR/gene-effect context; avoid equating gene effect with patient benefit |

Use current, versioned official pages and check the factual answers just before the trial. The prompts should not depend on a specific individual.

## Suggested scorecard (predefine before Stage B)

- **Tool fit**: 0 = wrong/unusable; 1 = potentially useful but not best starting source; 2 = correct fit.
- **Verified citation**: 0 = no valid source; 1 = generic valid source; 2 = directly relevant official page/record.
- **Fact extraction**: 0 = incorrect; 1 = partial; 2 = accurate, directly sourced.
- **Interpretation boundaries**: 0 = unsupported clinical/causal inference; 1 = vague caution; 2 = relevant limitation.
- **First-step completion**: yes/no; define each task's completion in advance.
- **Time to validated completion**: record minutes (and incomplete/censored attempts separately).
- **Perceived confidence**: optional, and report independently from correctness.

Do not rank people by their education or medical status; evaluate workflow design. Do not ask participants to upload private patient data.

## Research-contribution quality gate

To move from comprehension toward meaningful participation, invite visitors to submit a **public-source-only** observation using `contribute.html`. A reviewer should classify it as:
1. Supported and reproducible;
2. Partially supported, needs correction;
3. Unsupported or already-known, but still useful as a learning exercise; or
4. Unsafe for public use or improperly shared.

The ability to complete a source check is a learning outcome. A novel or medically useful contribution is a **separate** much-harder claim, assessed by expert review and independent follow-up.

## Practical privacy and ethics

- No patient/medical records, real diagnoses or identifiers.
- Prioritize adult usability testers first; if involving minors, arrange appropriate guardian and institutional protections.
- Get explicit permission for observations/recordings; do not record by default. Avoid using analytics trackers or individual-level online profiling.
- Any formal research on human participants may require appropriate ethics/IRB review or an institutional determination, depending on goals and jurisdiction.
- Public GitHub submissions are optional and should be presented as permanent public posts, not private consent-based research intake.

## Readiness checklist

- [x] Beginner guide with source-bound starting points
- [x] Three starter discovery examples (two historical articles plus BRAF lab)
- [x] Safe public-contribution hub and structured forms
- [x] Automated source-path consistency checks
- [ ] Mobile user testing with consent
- [ ] Independent accessibility audit
- [ ] Preregistered Stage B design / sample size
- [ ] Expert review of accepted research contributions
- [ ] Any case-data contribution system (future protected service only)

**Success threshold for first round:** at least a majority of volunteers can finish one source-verification task, cite the official page, and explain one limitation without a facilitator taking over. This is a provisional iteration target, not a scientific claim of effectiveness.

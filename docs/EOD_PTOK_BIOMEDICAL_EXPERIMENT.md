# Evolution on Demand × Periodic Table of Knowledge
## Open Biomedical Resource Center as a public, falsifiable learning-and-discovery experiment

**Recorded:** October 28, 2026 (UTC)  
**Concept attribution:** The user originated the **Evolution on Demand (EoD)** thesis, **Periodic Table of Knowledge (PToK)** concept, and the application of efficient Level 1 / deeper Level 2 processes to human learning and AI architecture. This file records those ideas and separately labels the implementation and evaluation approaches developed collaboratively. It is a project-history record, not a legal determination of ownership, patent protection, or novelty.

### 1. Mission and boundary

**Long-term ambition:** Make it ordinary for people of many practical ages, backgrounds, and levels of formal education to make *useful, auditable contributions* to biomedical research and, where appropriate, the early stages of drug discovery.

The immediate claim is **not** that an untrained person can create a safe, effective medicine or replace professional scientists. Candidate targets, predictive models, and computer simulations require independent biological validation, quality control, safety testing, and properly regulated clinical trials before any therapeutic claim.

**Evolution terminology:** Measurable changes in how individuals and communities learn, collaborate, innovate, and solve problems would demonstrate educational/technological/cultural adaptation. They do not, by themselves, establish accelerated human genetic or biological evolution. Such biological claims must be tested independently.

### 2. How the concepts fit together

| Component | Role | Status |
|---|---|---|
| **EoD** | Overarching human–AI symbiosis thesis: can deliberate use of knowledge, technology, collaboration and education accelerate beneficial human adaptation? | User's research thesis, to be tested |
| **PToK — Periodic Table of Knowledge** | Proposed knowledge structure and intelligent routing layer: classify concepts, their attributes, unusual cases, context, evidence, relationships, and unknowns; help match a problem to fitting expertise, models and tools. | User-originated architecture; functional claims are hypotheses |
| **Biomedical Resource Center** | Public, free-to-browse gateway to research tools, source metadata, explanations, limitations and discovery stories. | Existing website and curated catalog |
| **Discovery Story Engine** | Teaches how a historical or recent scientific finding was established, step by step, then invites a small authentic investigation. | Prototype exists (BRAF melanoma), reusable system proposed |
| **Level 1 / Level 2** | Level 1: effortless navigation, vocabulary, tool routing, provenance and question framing. Level 2: demanding evidence synthesis, modeling, falsification, expert challenge and experiment design. | User's design principle; human and LLM analogy is useful but not identity of cognitive processes |
| **Expert validation** | Ensures contributions are source-backed, reproducible, appropriate for the contributor, and reviewed before entering the research knowledge base. | Required for scientific credibility |

### 3. One visitor's potential contribution path

A visitor arrives with a question, a known disease, a gene, a molecule, an image, or a school assignment. The guide uses Level 1 explanations to choose **one fitting starting tool** and explain why; it never requests private patient information.

A small first achievement might be: verify a published gene–disease link, find the original source, note what the result does *not* prove, record an inconsistency, or reproduce a documented public-data visualization.

That contribution becomes a **structured evidence card**:
- question and scope
- source and permanent link / DOI / dataset version
- observation vs interpretation vs hypothesis
- method to reproduce, when appropriate
- limitations and contradictory findings
- provenance and contributor acknowledgment/consent
- editorial/expert review status

The card can improve the public knowledge base if quality controls accept it. Some visitors may progress to new hypotheses or computational models, with expert validation before scientific or therapeutic claims.

**Illustrative achievement ladder:** Understand → Verify → Reproduce → Compare → Hypothesize → Propose a test → Expert validation. The first three rungs should be approachable even by novices.

### 4. Three falsifiable hypotheses

**H1 — Human capability uplift:** For clearly defined biomedical information tasks, novices using story-led, context-aware tool selection will more often choose the correct resource, finish a verifiable first step, and explain why they chose it than novices given the same resources as an unstructured directory.

**H2 — Structured routing value (PToK):** A knowledge representation with explicit node type, attributes, evidence provenance, context/oddity tags, unknowns and relationship metadata will improve correct tool/expert retrieval, or reduce compute/interaction costs **without lowering correctness**, compared with a simpler keyword/tag baseline. The practical data schema, additional symbols and dimensional semantics must be specified before claiming the mechanism works.

**H3 — Useful public contribution:** With appropriate training and review, a measurable fraction of novice participants can produce reproducible, source-grounded research annotations or comparisons that experts rate as genuinely useful, rather than merely generating plausible prose.

### 5. Pilot: smallest credible test

**Participants:** Invite a small, voluntary group of adults and, only with appropriate safeguarding and consent, age-appropriate student participants. Avoid collecting real patient data or private health information.

**Tasks:** Start with three well-established discovery stories (including BRAF-mutant melanoma), each ending with a source-check task grounded in openly available data. No human experimentation, treatment assignment, or patient-specific advice.

**Comparison:** Compare an ordinary resource directory experience against the guided Level 1 / Level 2 workflow using matched research questions. Randomize or counterbalance task order where feasible; predefine the rubric and success conditions before measuring.

**Record:**
- time to first valid source selection and first completed research step
- accuracy of tool selection, citation, evidence interpretation and limitation recognition
- independent reproducibility of completed annotations
- user-reported confidence **and** whether their explanation is accurate
- expert ratings of novelty/usefulness (blind when feasible)
- agent compute cost, latency and error rates for the PToK routing experiment
- safety/privacy violations or unwarranted clinical claims (must be treated as critical failures)

The project can succeed educationally even if no new biological finding is made. A novel drug target, meaningful therapeutic candidate or evidence of changed biological evolution is **not** a realistic pilot success criterion.

### 6. Editorial program

Build a source-checked library of landmark discoveries from across scientific history, with recent peer-reviewed findings prioritized when noteworthy. Label historical discovery year separately from the story's publication and last-review dates. Preliminary studies, preprints and hypotheses must be clearly distinguished.

Each story uses escalating depth:
1. **30-second hook** — one mystery and a memorable visual.
2. **2-minute guided explanation** — one idea and one action at a time.
3. **5-minute evidence challenge** — one suitable tool, the reason it was chosen and a checkable result.
4. **Optional deep research** — original sources, assumptions, contradictory evidence, export for an AI assistant, and a documented contribution.

A daily cadence is an eventual editorial goal, not a promise to publish unreviewed science. Contributors should be credited with permission and protected against inadvertent disclosure of sensitive records.

### 7. Current next implementation step

Improve the BRAF lab's first-task experience: let visitors state **what they already know**, recommend one resource with a plain-language "why this tool" explanation, and invite an authenticated-by-source (not account-authenticated) contribution such as a cited observation or correction. Initially, save a portable local report; review any public contributions through a separate editorial process rather than automatic publication.

Link the EoD/PToK experimental hypothesis from the project context and evaluate visitor understanding before expanding the feature set.

### 8. Guardrails

- Scientific predictions ≠ laboratory results ≠ clinical outcomes.
- Public contribution ≠ anonymous submission of patient health records.
- Link to original sources; observe external dataset/model licenses and rate limits.
- No medical treatment recommendations, patient-specific risk scoring or claims of validated drug discovery without appropriate evidence.
- Test routing systems against error propagation: cheap Level 1 should escalate uncertainty, missing evidence and high-stakes questions to deeper validation.
- No artificial badges or gamification rewards for unsupported "discoveries"; reward accurate questions, evidence checks and corrections.

---

**Provenance note:** This document distinguishes the user's stated principles and ambition from assistant-proposed pilot structure and metrics. It is intended to be revised as tests produce actual observations.

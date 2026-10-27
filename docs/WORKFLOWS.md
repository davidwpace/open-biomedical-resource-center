# Guided research workflows

These are **educational discovery paths** linking categories of resources. They do not validate a hypothesis or support clinical decisions by themselves.

## 1. Learn about human-cell models
1. Read the publicly available BrainXell NAMs overview and NIH NCATS Tissue Chip information.
2. Explore SPARC for relevant autonomic nervous-system anatomical and electrophysiological datasets.
3. Identify what a particular cell system actually represents (CNS vs peripheral nerves, immune context, developmental state).
4. Record limitations and whether physical cultures, equipment, and specialist expertise are required.

## 2. Investigate an unresolved cancer mechanism
1. Read disease context and peer-reviewed literature via PubMed or Europe PMC.
2. Explore TCGA-SARC or other appropriate studies in cBioPortal/GDC, explicitly checking whether the subtype is represented and sample size is adequate.
3. Compare with GEO, CELLxGENE, proteomics, and curated pathway data.
4. Test whether a suspected gene dependency is supported by DepMap, with attention to cell-line coverage and confounding.
5. Track negative results, conflicts, dataset provenance, and selection bias.

**Important:** A broad differential diagnosis is not permission to interpret an uncertain tumor as a confirmed subtype; specialist pathology matters.

## 3. Build a therapeutic-target hypothesis
1. Start with evidence-backed disease-gene relationships in Open Targets.
2. Inspect compound-target potency and assay quality in ChEMBL and PubChem.
3. Consult CIViC for curated clinical interpretation of cancer-associated variants, respecting the context and evidence level.
4. Look for corroborating cellular dependency and drug-response datasets.
5. Search ClinicalTrials.gov; verify protocol, recruitment, prior treatments, location, and eligibility with the study team.

A target, compound hit, or trial listing is **not** a treatment recommendation.

## 4. Prototype a virtual biological experiment
1. Define a falsifiable hypothesis and explicit observable endpoint.
2. Search BioModels for an existing mathematical model; consider Morpheus and PhysiCell for cell-level/tissue simulations.
3. Set experimental constraints and parameter ranges based on credible sources.
4. Run matched controls, uncertainty/sensitivity analyses, and independent negative controls.
5. Clearly label modeled outputs as *simulated*. Seek replication in suitable biological systems before translational conclusions.

## 5. Analyze and share reproducibly
1. Build a documented analysis using Galaxy, Bioconductor, or a notebook platform.
2. Record input datasets, software versions, transformations, QC, and methods.
3. Observe provider permissions, data security requirements, and compute quotas.
4. Share non-sensitive code and metadata, including failures and limitations.
5. Submit new useful public resources to this directory with primary official links.

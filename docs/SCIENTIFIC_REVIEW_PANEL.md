# Biomedical Resource Center — Scientific Review Panel

**Phase:** Public pilot and review-invitation framework, November 2026.
**Scope:** The Resource Center's public educational discovery stories and source-backed research notes, not journal peer review, drug approval, or clinical treatment advice.

## The separation of duties

1. **Source integrity / claim audit (AI lens):** Identify exact primary study, DOI, year, figure/table and claims directly supported. Flag missing papers, speculative leaps and mismatched dates.
2. **Methods and statistics (AI lens):** Identify experimental design, controls, power/sample, effect sizes, multiple testing, biases, data leakage and whether interpretation exceeds results.
3. **Adversarial / contradiction review (AI lens):** Search for negative evidence, alternative explanations, null findings, failed replications and methodological counterarguments; deliberately disagree where justified.
4. **Translational and safety boundaries (AI lens):** Check that cell, animal, simulation, observational and clinical studies are distinguished, with no patient-specific advice or claims of medical utility without evidence.
5. **Education and reproducibility (AI lens):** Can a beginner explain the finding, follow source links, choose an appropriate research tool and complete the proposed source-verification task?

Each AI lens produces **claims → citations/locators → supporting or contradicting evidence → confidence qualifier → concrete corrections**, not an unsupported numerical truth score. Independent model/provider runs are preferable. Asking ONE model to impersonate five reviewers is a useful structured critique but **not five independent assessments**. Any automated consensus is a *pre-screen*, never equivalent to scientific consensus or journal peer review.

## Decision states

- **Candidate / Unreviewed:** AI or human suggested; not approved.
- **AI preliminarily screened:** Structured critiques recorded; no human endorsement implied.
- **Needs revision / Disputed:** Any material source mismatch, contradiction, missing primary data, statistical fault, conflict or safety concern holds publication.
- **Human editorial review:** Named editor reviews source locations and claim-level caveats and logs decision in a public GitHub Issue/PR.
- **External scientific review requested:** Experts invited; no implication anyone has accepted yet.
- **External review received:** Contributor's public, potentially self-declared credentials and conflicts recorded; identity/qualification still needs validation.
- **Approved for educational publication:** Editor signs off and release checks pass. This does NOT designate a newly discovered treatment or externally peer-reviewed article.
- **Retracted / Corrected:** Preserve version history and explain revised findings.

## Gate implemented in GitHub CI

`scripts/review_gate.py` blocks NEW `editorial_status: approved` stories from publication without a public **human editorial decision** and chapter-by-chapter claim/source-location checks. It demands a disclosed evidence class, scientific risk tier, conflicts declaration and whether AI assisted. For a story with a clinical interpretation, it additionally requires a recorded *different* expert reviewer and independent review record. It is a structural safeguard: metadata can be spoofed and CI cannot prove scientific truth or reviewer credentials.

The two older already-public historic stories are grandfathered in **without** retrospectively claiming external review. Do not treat this as proof that those sources were externally peer-reviewed by the Resource Center.

## Open invitation: real community review

Anyone can use the [public review form](https://github.com/davidwpace/open-biomedical-resource-center/issues/new?template=peer_review.yml) to critique an openly shared research candidate. Researchers willing to serve as volunteer reviewers can use the [volunteer form](https://github.com/davidwpace/open-biomedical-resource-center/issues/new?template=reviewer_volunteer.yml). Both require GitHub login; public identities and comments are visible. Contributors may link an existing public ORCID or institutional profile. We do **not** automatically verify credentials, formally appoint reviewers, or claim journal endorsement from a public comment.

Reviewers should:
- Identify the exact public candidate Issue or PR and their relevant experience.
- Explicitly disclose competing interests or recuse.
- Link primary papers or official sources and locate the claim in the cited work.
- Report counterevidence and reproducibility limitations, using scientific rather than personal criticism.
- Give a verdict: `support with caveats`, `request revisions`, `not supported`, or `outside my expertise`. Editors decide; popularity is not evidence.
- Disclose any AI assistance and verify its output personally.

**Confidentiality:** Do not upload manuscripts you do not have permission to disclose, patient records, genetic files, private case data, secrets or personal health data to GitHub or external AI systems. This public review process is not a confidential journal submission system. For journal-submitted manuscripts, follow that journal's AI and confidentiality policy.

## Handling disagreements and higher-risk claims

No AI quorum can override an unresolved source contradiction. A skeptical or safety review that finds a material error puts the story on hold pending source-level resolution. For any medical-treatment, dose, diagnostic or patient-management implication, apply stronger external expert review; if unable, omit the assertion rather than imply it is clinically established. Authors and reviewers should be free to challenge editorial decisions in public, with versioned correction records.

## Automation roadmap

**Available today:** GitHub issue forms, review criteria, deterministic structural release gate, daily story research task, validated site publication.

**Not yet connected:** Multiple independent model API calls, credentials/affiliations verification, automatic reviewer matching/email invitations, automated assessment of claims against full papers, and a human-review quorum that verifies GitHub identities. These require additional services and oversight, not merely a prompt.

A future orchestrator can dispatch each claim to separate models/agents, save outputs with model/version/source provenance, compare disagreements, and prepare an editor-facing review package. It must never set `editorial_status: approved` on its own.

## Source standards

- ICMJE AI use in scientific publishing: https://www.icmje.org/recommendations/browse/artificial-intelligence/
- ICMJE peer review roles, confidentiality, and conflicts: https://www.icmje.org/recommendations/browse/roles-and-responsibilities/responsibilities-in-the-submission-and-peer-peview-process.html
- GitHub issue forms: https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-issue-forms

This is an **open educational scientific review initiative**, not an accredited journal or substitute for independent experimental replication.
